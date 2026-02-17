#!/usr/bin/env python3
"""Fix missing coordinates for GSSS-GHAROTA and GGSSS-SUJANPUR"""
import json
import urllib.request
import re
import sys

def get_coords_from_url(url):
    """Extract coordinates from Google Maps URL."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=30)
        final_url = resp.geturl()
        
        # Try to extract from @lat,lng pattern
        match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', final_url)
        if match:
            return float(match.group(1)), float(match.group(2))
        
        # Try from /place/ pattern
        match = re.search(r'/place/[^/]*/@(-?\d+\.\d+),(-?\d+\.\d+)', final_url)
        if match:
            return float(match.group(1)), float(match.group(2))

        # Try !3d !4d pattern
        match = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', final_url)
        if match:
            return float(match.group(1)), float(match.group(2))
        
        # Read content
        content = resp.read().decode('utf-8', errors='ignore')
        match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', content)
        if match:
            return float(match.group(1)), float(match.group(2))
            
        return None, None
    except Exception as e:
        print(f"  Error: {e}")
        return None, None

# URLs for the missing schools
fixes = {
    'GSSS-GHAROTA': 'https://maps.app.goo.gl/RMuUwQxWxCVPYMV26',
    'GGSSS-SUJANPUR': 'https://maps.app.goo.gl/M7KTviQfop6km2bA6',
}

d = json.load(open('data.json', 'r', encoding='utf-8'))

for u in d['dailyUpdates']:
    for s in u['schools']:
        if s['name'] in fixes:
            print(f"Fixing {s['name']}...")
            url = fixes[s['name']]
            lat, lng = get_coords_from_url(url)
            if lat and lng:
                s['location']['lat'] = lat
                s['location']['lng'] = lng
                print(f"  Set coords: {lat}, {lng}")
            else:
                print(f"  FAILED to extract coords from {url}")
                print(f"  Please provide coords manually")

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

print("\nDone!")
