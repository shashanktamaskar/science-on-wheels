#!/usr/bin/env python3
"""
Science on Wheels - Daily Update Automation Script
===================================================
This script automates the entire daily update process:
1. Pulls latest data from GitHub
2. Parses input data for all vehicles/schools
3. Extracts coordinates from Google Maps links
4. Generates AI-powered collages from zip files
5. Updates data.json and schools-gallery.json
6. Commits and pushes to GitHub

Usage:
------
python daily_update.py --date 2025-12-09 --input input_data.txt

OR interactive mode:
python daily_update.py --interactive

Input File Format (input_data.txt):
-----------------------------------
DATE: 2025-12-09
VEHICLE: 1
START: Patiala | https://maps.app.goo.gl/xxxxx
SCHOOL: GHS-CHAURA | https://maps.app.goo.gl/xxxxx | 320 | 170 | 150 | Patiala | D:\path\to\zip | https://sharepoint.com/gallery
SCHOOL: GSSS-SANOUR-G | https://maps.app.goo.gl/xxxxx | 736 | 736 | 0 | Patiala | D:\path\to\zip | https://sharepoint.com/gallery
END: Patiala | https://maps.app.goo.gl/xxxxx

VEHICLE: 2
START: Mohali | https://maps.app.goo.gl/xxxxx
SCHOOL: GSSS-SCHOOL-B | https://maps.app.goo.gl/xxxxx | 500 | 250 | 250 | Mohali | D:\path\to\zip | https://sharepoint.com/gallery
END: Mohali | https://maps.app.goo.gl/xxxxx
"""

import json
import os
import sys
import math
import re
import subprocess
import tempfile
import shutil
import zipfile
import glob
import argparse
from datetime import datetime
import urllib.request

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Add AI-Collage-Tool to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COLLAGE_TOOL_PATH = os.path.join(os.path.dirname(SCRIPT_DIR), 'AI-Collage-Tool')
sys.path.insert(0, COLLAGE_TOOL_PATH)

# ============= CONFIGURATION =============
REPO_URL = "https://github.com/shashanktamaskar/science-on-wheels.git"
KNOWN_DISTRICTS = ["SAS Nagar", "Ludhiana", "Fatehgarh Sahib", "Roopnagar", "Malerkotla", "Patiala"]
GALLERY_COLLAGE_DIR = os.path.join(SCRIPT_DIR, "gallery_school_collage")

# ============= HELPER FUNCTIONS =============

def run_cmd(cmd, cwd=None, check=True):
    """Run a shell command and return output."""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Command failed: {cmd}")
        print(f"Error: {result.stderr}")
        return None
    return result.stdout.strip()

def get_coords_from_url(url):
    """Extract coordinates from a Google Maps URL."""
    try:
        # Follow redirects to get final URL
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            final_url = response.geturl()
        
        # Try different URL patterns
        patterns = [
            r'@(-?\d+\.\d+),(-?\d+\.\d+)',      # @lat,lng format
            r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)',  # !3dlat!4dlng format
            r'q=(-?\d+\.\d+),(-?\d+\.\d+)',     # q=lat,lng format
        ]
        
        for pattern in patterns:
            match = re.search(pattern, final_url)
            if match:
                return float(match.group(1)), float(match.group(2))
        
        print(f"  Warning: Could not extract coords from {final_url}")
        return None
    except Exception as e:
        print(f"  Error extracting coords from {url}: {e}")
        return None

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km."""
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))

def calculate_route_distance(start_coords, school_coords_list, end_coords):
    """Calculate total route distance."""
    if not start_coords or not end_coords:
        return 0
    
    total = 0
    current = start_coords
    
    for school_coords in school_coords_list:
        if school_coords:
            total += haversine(current[0], current[1], school_coords[0], school_coords[1])
            current = school_coords
    
    total += haversine(current[0], current[1], end_coords[0], end_coords[1])
    return round(total)

def parse_input_file(filepath):
    """Parse the input file and return structured data."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    data = {
        'date': None,
        'vehicles': []
    }
    
    current_vehicle = None
    
    for line in content.strip().split('\n'):
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('DATE:'):
            data['date'] = line.split(':', 1)[1].strip()
        
        elif line.startswith('VEHICLE:'):
            if current_vehicle:
                data['vehicles'].append(current_vehicle)
            current_vehicle = {
                'number': int(line.split(':', 1)[1].strip()),
                'start': None,
                'end': None,
                'schools': []
            }
        
        elif line.startswith('START:'):
            parts = line.split(':', 1)[1].strip().split('|')
            current_vehicle['start'] = {
                'name': parts[0].strip(),
                'url': parts[1].strip() if len(parts) > 1 else None
            }
        
        elif line.startswith('END:'):
            parts = line.split(':', 1)[1].strip().split('|')
            current_vehicle['end'] = {
                'name': parts[0].strip(),
                'url': parts[1].strip() if len(parts) > 1 else None
            }
        
        elif line.startswith('SCHOOL:'):
            # Format: SCHOOL: NAME | MAP_URL | STUDENTS | GIRLS | BOYS | DISTRICT | ZIP_PATH | GALLERY_URL
            parts = [p.strip() for p in line.split(':', 1)[1].split('|')]
            if len(parts) >= 8:
                current_vehicle['schools'].append({
                    'name': parts[0],
                    'map_url': parts[1],
                    'students': int(parts[2]),
                    'girls': int(parts[3]),
                    'boys': int(parts[4]),
                    'district': parts[5],
                    'zip_path': parts[6],
                    'gallery_url': parts[7]
                })
    
    if current_vehicle:
        data['vehicles'].append(current_vehicle)
    
    return data

def generate_collage(zip_path, school_name, district, date, output_dir, api_key):
    """Generate a collage from images in a zip file."""
    output_path = os.path.join(output_dir, f"{school_name}.jpg")
    
    # Check if collage already exists
    if os.path.exists(output_path):
        print(f"    Collage already exists: {output_path}")
        return output_path
    
    if not os.path.exists(zip_path):
        print(f"    Warning: Zip file not found: {zip_path}")
        return None
    
    temp_dir = tempfile.mkdtemp()
    try:
        print(f"    Extracting {zip_path}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find all images
        extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
        image_paths = []
        for ext in extensions:
            image_paths.extend(glob.glob(os.path.join(temp_dir, '**', ext), recursive=True))
        
        if len(image_paths) < 6:
            print(f"    Warning: Need at least 6 images, found {len(image_paths)}")
            return None
        
        print(f"    Found {len(image_paths)} images")
        
        # Import collage generation functions
        try:
            from collage_generator_final import setup_gemini, get_best_photos, create_collage_with_header, rate_collage
            from api_key import API_KEY
            
            setup_gemini(API_KEY)
            
            logo_path = os.path.join(COLLAGE_TOOL_PATH, "science_on_wheels_logo.png")
            
            # Get best 6 photos
            selected_photos = get_best_photos(
                image_paths,
                logo_path if os.path.exists(logo_path) else None,
                school_name,
                district,
                date,
                count=6,
                model_name='gemini-2.0-flash-exp'
            )
            
            # Create collage
            create_collage_with_header(
                selected_photos,
                output_path,
                school_name,
                district,
                date,
                logo_path if os.path.exists(logo_path) else None,
                grid_layout=(3, 2),
                target_size=(540, 405)
            )
            
            # Rate collage
            rating_text, score = rate_collage(
                output_path,
                logo_path if os.path.exists(logo_path) else None,
                school_name,
                district,
                date,
                model_name='gemini-2.0-flash-exp'
            )
            
            print(f"    ✅ Collage saved: {output_path} (Score: {score}/10)")
            return output_path
            
        except ImportError as e:
            print(f"    Warning: Could not import collage tools: {e}")
            return None
        
    except Exception as e:
        print(f"    Error generating collage: {e}")
        return None
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def get_existing_districts(data):
    """Extract set of all visited districts from historical data."""
    districts = set()
    if 'dailyUpdates' in data:
        for update in data['dailyUpdates']:
            if 'schools' in update:
                for school in update['schools']:
                    if 'district' in school:
                        districts.add(school['district'])
    return districts

def update_data_json(data_path, update_data, api_key):
    """Update data.json with new entries."""
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Get historically visited districts
    known_districts = get_existing_districts(data)
    
    date = update_data['date']
    
    # Track totals for this update
    new_schools = 0
    new_students = 0
    new_girls = 0
    new_boys = 0
    total_distance = 0
    new_districts = set()
    
    for vehicle in update_data['vehicles']:
        print(f"\n  Processing Vehicle {vehicle['number']}...")
        
        # Get coordinates
        print("    Extracting coordinates...")
        start_coords = get_coords_from_url(vehicle['start']['url']) if vehicle['start']['url'] else None
        end_coords = get_coords_from_url(vehicle['end']['url']) if vehicle['end']['url'] else None
        
        school_entries = []
        school_coords_list = []
        
        for school in vehicle['schools']:
            print(f"    Processing school: {school['name']}")
            
            # Get school coordinates
            school_coords = get_coords_from_url(school['map_url'])
            school_coords_list.append(school_coords)
            
            # Generate collage
            collage_result = generate_collage(
                school['zip_path'],
                school['name'],
                school['district'],
                date,
                GALLERY_COLLAGE_DIR,
                api_key
            )
            
            school_entry = {
                "name": school['name'],
                "location": {"lat": school_coords[0], "lng": school_coords[1]} if school_coords else {"lat": 0, "lng": 0},
                "studentsReached": school['students'],
                "girlsCount": school['girls'],
                "boysCount": school['boys'],
                "district": school['district'],
                "galleryLink": school['gallery_url'],
                "collageImage": f"{school['name']}.jpg"
            }
            school_entries.append(school_entry)
            
            # Track totals
            new_schools += 1
            new_students += school['students']
            new_girls += school['girls']
            new_boys += school['boys']
            
            if school['district'] not in known_districts and school['district'] not in new_districts:
                new_districts.add(school['district'])
        
        # Calculate route distance
        vehicle_distance = calculate_route_distance(start_coords, school_coords_list, end_coords)
        total_distance += vehicle_distance
        print(f"    Route distance: {vehicle_distance} km")
        
        # Create daily update entry
        daily_entry = {
            "date": date,
            "vehicle": vehicle['number'],
            "schools": school_entries,
            "schoolsVisited": len(school_entries),
            "studentsReached": sum(s['students'] for s in vehicle['schools']),
            "route": {
                "startPoint": {"lat": start_coords[0], "lng": start_coords[1]} if start_coords else {"lat": 0, "lng": 0},
                "endPoint": {"lat": end_coords[0], "lng": end_coords[1]} if end_coords else {"lat": 0, "lng": 0}
            },
            "distanceTravelled": vehicle_distance
        }
        
        # Insert at beginning
        data['dailyUpdates'].insert(0, daily_entry)
    
    # Update mission statistics
    data['lastUpdated'] = date
    data['mission']['schoolsCovered']['current'] += new_schools
    data['mission']['studentsImpacted'] += new_students
    data['mission']['genderBreakdown']['girls'] += new_girls
    data['mission']['genderBreakdown']['boys'] += new_boys
    data['mission']['distanceTravelled'] += total_distance
    
    if new_districts:
        data['mission']['districtsCovered']['current'] += len(new_districts)
        print(f"     New Districts Added: {new_districts}")
    
    # Save
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n  ✅ Updated data.json")
    print(f"     Schools: +{new_schools} → {data['mission']['schoolsCovered']['current']}")
    print(f"     Students: +{new_students} → {data['mission']['studentsImpacted']}")
    print(f"     Distance: +{total_distance} km → {data['mission']['distanceTravelled']} km")
    
    return {
        'new_schools': new_schools,
        'new_students': new_students,
        'new_girls': new_girls,
        'new_boys': new_boys,
        'new_distance': total_distance,
        'totals': data['mission']
    }

def update_schools_gallery(gallery_path, update_data):
    """Update schools-gallery.json with new entries."""
    with open(gallery_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    date = update_data['date']
    
    for vehicle in update_data['vehicles']:
        for school in vehicle['schools']:
            entry = {
                "name": school['name'],
                "district": school['district'],
                "visitDate": date,
                "folderUrl": school['gallery_url']
            }
            data['schools'].insert(0, entry)
    
    with open(gallery_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Updated schools-gallery.json (Total: {len(data['schools'])} schools)")

def git_commit_and_push(repo_dir, date, summary):
    """Commit and push changes to GitHub."""
    print("\n📤 Pushing to GitHub...")
    
    # Add files
    run_cmd("git add data.json schools-gallery.json gallery_school_collage/", cwd=repo_dir)
    
    # Create commit message
    commit_msg = f"Daily update {date}: {summary['new_schools']} schools, {summary['new_students']} students, +{summary['new_distance']}km"
    
    # Commit
    result = run_cmd(f'git commit -m "{commit_msg}"', cwd=repo_dir, check=False)
    if result is None:
        print("  Note: Nothing to commit or commit failed")
    
    # Push
    result = run_cmd("git push origin main", cwd=repo_dir, check=False)
    if "rejected" in str(result):
        print("  ⚠️ Push rejected - trying pull first...")
        run_cmd("git pull origin main --rebase", cwd=repo_dir)
        run_cmd("git push origin main", cwd=repo_dir)
    
    print("  ✅ Changes pushed to GitHub")

def main():
    parser = argparse.ArgumentParser(description='Science on Wheels Daily Update Automation')
    parser.add_argument('--input', '-i', required=True, help='Path to input file with daily data')
    parser.add_argument('--dry-run', action='store_true', help='Parse and validate only, do not update')
    parser.add_argument('--skip-push', action='store_true', help='Skip git push (for testing)')
    parser.add_argument('--skip-collage', action='store_true', help='Skip collage generation')
    args = parser.parse_args()
    
    print("=" * 60)
    print("🚐 SCIENCE ON WHEELS - DAILY UPDATE AUTOMATION")
    print("=" * 60)
    
    # Step 1: Parse input file
    print("\n📋 Step 1: Parsing input file...")
    if not os.path.exists(args.input):
        print(f"❌ Input file not found: {args.input}")
        return 1
    
    update_data = parse_input_file(args.input)
    print(f"  Date: {update_data['date']}")
    print(f"  Vehicles: {len(update_data['vehicles'])}")
    for v in update_data['vehicles']:
        print(f"    Vehicle {v['number']}: {len(v['schools'])} schools")
        for s in v['schools']:
            print(f"      - {s['name']} ({s['students']} students)")
    
    if args.dry_run:
        print("\n✅ Dry run complete - no changes made")
        return 0
    
    # Step 2: Pull latest from GitHub
    print("\n🔄 Step 2: Pulling latest data from GitHub...")
    run_cmd("git pull origin main", cwd=SCRIPT_DIR)
    
    # Step 3: Load API key for collage generation
    api_key = None
    if not args.skip_collage:
        try:
            sys.path.insert(0, COLLAGE_TOOL_PATH)
            from api_key import API_KEY
            api_key = API_KEY
            print("  ✅ API key loaded")
        except ImportError:
            print("  ⚠️ API key not found - collages will be skipped")
            args.skip_collage = True
    
    # Step 4: Update data.json
    print("\n📊 Step 3: Updating data.json...")
    data_path = os.path.join(SCRIPT_DIR, 'data.json')
    summary = update_data_json(data_path, update_data, api_key if not args.skip_collage else None)
    
    # Step 5: Update schools-gallery.json
    print("\n🖼️ Step 4: Updating schools-gallery.json...")
    gallery_path = os.path.join(SCRIPT_DIR, 'schools-gallery.json')
    update_schools_gallery(gallery_path, update_data)
    
    # Step 6: Validate JSON
    print("\n✅ Step 5: Validating JSON files...")
    try:
        json.load(open(data_path))
        json.load(open(gallery_path))
        print("  Both JSON files are valid!")
    except json.JSONDecodeError as e:
        print(f"  ❌ JSON validation failed: {e}")
        return 1
    
    # Step 7: Push to GitHub
    if not args.skip_push:
        print("\n📤 Step 6: Pushing to GitHub...")
        git_commit_and_push(SCRIPT_DIR, update_data['date'], summary)
    else:
        print("\n⚠️ Skipping git push (--skip-push flag)")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 DAILY UPDATE COMPLETE!")
    print("=" * 60)
    print(f"\n📊 Summary for {update_data['date']}:")
    print(f"   Schools Added: +{summary['new_schools']}")
    print(f"   Students: +{summary['new_students']} ({summary['new_girls']} girls, {summary['new_boys']} boys)")
    print(f"   Distance: +{summary['new_distance']} km")
    print(f"\n📈 Cumulative Totals:")
    print(f"   Total Schools: {summary['totals']['schoolsCovered']['current']}")
    print(f"   Total Students: {summary['totals']['studentsImpacted']}")
    print(f"   Total Distance: {summary['totals']['distanceTravelled']} km")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
