# Daily Update Instructions for Science on Wheels Website

## Overview
This document provides step-by-step instructions for updating the Science on Wheels website with daily school visit data. These instructions can be followed by any AI model or developer.

## Project Structure
```
science-on-wheels/
├── data.json              # Main data file with mission stats and daily updates
├── schools-gallery.json   # Gallery data with school photos
├── index.html            # Website (auto-updates from JSON files)
├── gallery_school_collage/  # School collage images folder
│   ├── GHS-Balongi.jpg
│   ├── GHS-Kurali.jpg
│   └── [SchoolName].jpg   # One image per school (must match JSON name)
└── DAILY_UPDATE_INSTRUCTIONS.md  # This file
```

## Files to Update

### 1. data.json
Contains:
- `lastUpdated`: Date of last update (YYYY-MM-DD format)
- `mission`: Cumulative statistics
  - `schoolsCovered.current`: Total schools visited so far
  - `districtsCovered.current`: Total unique districts visited
  - `studentsImpacted`: Total students reached
  - `distanceTravelled`: Total kilometers travelled
- `dailyUpdates`: Array of daily visit records (newest first)

### 2. schools-gallery.json
Contains:
- `schools`: Array of school entries with photo links
  - `name`: School name
  - `district`: District name
  - `visitDate`: Visit date (YYYY-MM-DD)
  - `folderUrl`: OneDrive link to photos

## Input Data Format

User will provide:
```
Date: YYYY-MM-DD
Schools visited:
1. School Name - Coordinates: (latitude, longitude) - Students: number - District: District Name
2. School Name - Coordinates: (latitude, longitude) - Students: number - District: District Name
...

Start/End: Plaksha University (30.6310588, 76.7230178)

Gallery:
- School Name: OneDrive URL
- School Name: OneDrive URL
...

Collage Images:
- School Name: Filename.jpg
- School Name: Filename.jpg
...
```

## Step-by-Step Instructions

### STEP 1: Read Current Data
```bash
# Read both JSON files
cat data.json
cat schools-gallery.json
```

Extract current values:
- Current schools count: `data.mission.schoolsCovered.current`
- Current districts count: `data.mission.districtsCovered.current`
- Current students: `data.mission.studentsImpacted`
- Current distance: `data.mission.distanceTravelled`
- All districts visited so far (from `dailyUpdates` array)

### STEP 2: Calculate Route Distance

Use the Haversine formula to calculate distances:
```python
import math

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in kilometers"""
    R = 6371  # Earth's radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c

    return round(distance, 2)

# Calculate route:
# Plaksha → School1 → School2 → ... → Plaksha
# Sum all segments and round to nearest km
```

**Route Logic:**
- Start at Plaksha University
- Visit each school in order provided
- Return to Plaksha University
- Sum all segment distances
- Round to nearest whole number

### STEP 3: Calculate New Cumulative Statistics
```
new_schools_count = old_schools_count + number_of_schools_visited_today
new_students = old_students + sum_of_students_today
new_distance = old_distance + today_route_distance

# For districts: check if any new district was visited
new_districts = count unique districts from all dailyUpdates including today
```

### STEP 4: Update data.json

**4a. Update top-level fields:**
```json
"lastUpdated": "YYYY-MM-DD"  // Today's date
```

**4b. Update mission statistics:**
```json
"mission": {
  "schoolsCovered": {
    "current": <new_schools_count>,
    "total": 235
  },
  "districtsCovered": {
    "current": <new_districts_count>,
    "total": 16
  },
  "studentsImpacted": <new_students>,
  "distanceTravelled": <new_distance>,
  "targetAudience": "Students from Classes 6-12"
}
```

**4c. Add new daily update entry:**

Insert the new entry at the BEGINNING of the `dailyUpdates` array (after the opening `[`):
```json
{
  "date": "YYYY-MM-DD",
  "vehicle": 1,
  "schools": [
    {
      "name": "School Name 1",
      "location": {
        "lat": latitude,
        "lng": longitude
      },
      "studentsReached": number,
      "district": "District Name"
    },
    {
      "name": "School Name 2",
      "location": {
        "lat": latitude,
        "lng": longitude
      },
      "studentsReached": number,
      "district": "District Name"
    }
  ],
  "route": {
    "startPoint": {
      "name": "Plaksha University",
      "lat": 30.6310588,
      "lng": 76.7230178
    },
    "endPoint": {
      "name": "Plaksha University",
      "lat": 30.6310588,
      "lng": 76.7230178
    },
    "distanceTravelled": <calculated_distance>
  },
  "totalStudents": <sum_of_students_today>,
  "schoolsVisited": <count_of_schools_today>
}
```

**IMPORTANT:** Add a comma after the closing `}` if there are existing entries below.

### STEP 5: Update schools-gallery.json

Add new school entries to the `schools` array at the END (before the closing `]`):
```json
{
  "name": "School Name",
  "district": "District Name",
  "visitDate": "YYYY-MM-DD",
  "folderUrl": "OneDrive URL"
}
```

**IMPORTANT:**
- Add a comma after the previous entry
- Add one entry for EACH school visited
- Use the exact school name as provided

### STEP 5.5: Upload Collage Images to Gallery

Upload the collage images to the `gallery_school_collage/` folder on the remote repository.

**File Naming Rules (CRITICAL):**
- School name in JSON: `"name": "GHS-Balongi"`
- Image filename must match EXACTLY: `GHS-Balongi.jpg`
- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`
- The carousel reads school names from `schools-gallery.json` and loads images matching those names

**Upload Process:**
1. Ensure image filename matches the school name in JSON exactly
2. Upload to: `gallery_school_collage/[SchoolName].jpg`
3. Use one of these methods:
   - Push via Git: `git add gallery_school_collage/[SchoolName].jpg`
   - Upload via GitHub web interface
   - Use repository file upload feature

**Example Matching:**
```json
// In schools-gallery.json
{
  "name": "GHS Phase-5",
  ...
}
```
```
// Image file location
gallery_school_collage/GHS Phase-5.jpg
```

**If Image is Missing:**
- Carousel will display a placeholder
- Always ensure filenames match JSON names exactly
- Check for spelling, capitalization, spaces, and special characters

### STEP 6: Validate JSON Files
```bash
# Validate JSON syntax
python3 -c "import json; json.load(open('data.json'))"
python3 -c "import json; json.load(open('schools-gallery.json'))"
```

If validation fails, fix syntax errors before proceeding.

### STEP 7: Git Workflow
```bash
# Check current branch
git branch

# Ensure on correct branch: claude/session-<ID>
# If not, create new branch:
# git checkout -b claude/session-<ID>

# Stage files
git add data.json schools-gallery.json
git add gallery_school_collage/*.jpg gallery_school_collage/*.jpeg gallery_school_collage/*.png gallery_school_collage/*.webp

# View changes
git diff --cached

# Commit with descriptive message
git commit -m "$(cat <<'EOF'
Update website with <Month> <Day>, 2025 school visits

- Add <School1> (<students1> students) and <School2> (<students2> students) to daily updates
- Update mission stats: <new_schools> schools covered, <new_students> total students, <new_distance> km travelled
- Add schools to gallery with OneDrive photo links
- Upload collage images to gallery_school_collage/ folder
- Route: Plaksha → <School1> → <School2> → Plaksha (<distance> km)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# Push to remote
git push -u origin claude/session-<ID>
```

### STEP 8: Create Pull Request

Provide the user with the GitHub PR creation URL (from git push output) and the following PR template:
```markdown
## Summary
- Added <School1> (<students1> students) and <School2> (<students2> students) to daily updates for <date>
- Updated mission statistics: <new_schools> schools covered, <new_students> total students impacted, <new_distance> km travelled
- Added schools to gallery page with OneDrive photo links
- Uploaded collage images to gallery_school_collage/ folder
- Route: Plaksha University → <School1> → <School2> → Plaksha University (<distance> km total)

## Changes
### data.json
- Updated `lastUpdated` to <date>
- Updated mission stats:
  - Schools covered: <old> → <new>
  - Districts covered: <old> → <new>
  - Students impacted: <old> → <new>
  - Distance travelled: <old> km → <new> km
- Added new daily update entry for <date>

### schools-gallery.json
- Added <School1> with OneDrive link
- Added <School2> with OneDrive link

### gallery_school_collage/
- Uploaded <School1>.jpg collage image
- Uploaded <School2>.jpg collage image

## Test plan
- [x] Verified data.json is valid JSON
- [x] Verified schools-gallery.json is valid JSON
- [x] Checked that coordinates are correct
- [x] Confirmed distance calculations are accurate
- [x] Verified collage image filenames match school names in JSON exactly
- [x] Confirmed images are in correct format (.jpg, .jpeg, .png, or .webp)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Example Complete Workflow

### Input:
```
Date: 2025-10-29
Schools visited:
1. GHS-Balongi - Coordinates: (30.7234, 76.7123) - Students: 300
2. GHS-Kurali - Coordinates: (30.7845, 76.7956) - Students: 275

Start/End: Plaksha University (30.6310588, 76.7230178)

Gallery:
- GHS-Balongi: https://plakshauniversity1-my.sharepoint.com/:f:/g/personal/scienceonwheels_plaksha_edu_in/ExampleLink1
- GHS-Kurali: https://plakshauniversity1-my.sharepoint.com/:f:/g/personal/scienceonwheels_plaksha_edu_in/ExampleLink2
```

### Processing:

1. **Read current data:**
   - Schools: 4 → 6 (adding 2)
   - Students: 1341 → 1916 (adding 575)
   - Districts: Check if "SAS Nagar" or new district
   - Distance: 47 → (47 + calculated)

2. **Calculate distance:**
   - Plaksha (30.6310588, 76.7230178) → Balongi (30.7234, 76.7123) = ~10.5 km
   - Balongi (30.7234, 76.7123) → Kurali (30.7845, 76.7956) = ~9.8 km
   - Kurali (30.7845, 76.7956) → Plaksha (30.6310588, 76.7230178) = ~19.1 km
   - **Total: 39 km (rounded from 39.4)**

3. **Update data.json:**
   - Set `lastUpdated` to "2025-10-29"
   - Update mission: schools=6, students=1916, distance=86
   - Add new dailyUpdates entry at beginning

4. **Update schools-gallery.json:**
   - Add GHS-Balongi entry
   - Add GHS-Kurali entry

5. **Commit and push:**
   - Create descriptive commit message
   - Push to branch
   - Provide PR creation link

## Important Notes

### Gallery Image Management
- **Filename Matching:** The school name in `schools-gallery.json` must match the image filename EXACTLY
- **Supported Formats:** `.jpg`, `.jpeg`, `.png`, `.webp`
- **Location:** All images go in the `gallery_school_collage/` folder
- **Naming Convention:** Use the exact school name from JSON
  - Example: If JSON has `"name": "GHS-Saneta"`, file must be `GHS-Saneta.jpg`
  - Capitalization, spaces, and special characters MUST match
- **Missing Images:** If an image filename doesn't match, the carousel will show a placeholder
- **Multiple Schools:** Each school needs its own unique image file

**Gallery Folder Structure Example:**
```
gallery_school_collage/
  ├── GHS-Balongi.jpg      ✓ matches JSON entry "GHS-Balongi"
  ├── GHS-Kurali.png       ✓ matches JSON entry "GHS-Kurali"
  ├── GHS Phase-5.jpg      ✓ matches JSON entry "GHS Phase-5" (note: spaces matter!)
  └── GHS Kumbra.jpeg      ✓ matches JSON entry "GHS Kumbra"
```

**Verification Checklist for Images:**
- [ ] Each image filename matches corresponding school name in JSON
- [ ] No typos in filenames
- [ ] Proper capitalization maintained
- [ ] Spaces preserved correctly
- [ ] File extension is one of: .jpg, .jpeg, .png, .webp
- [ ] Images are uploaded to gallery_school_collage/ folder
- [ ] Images are included in git commit

### District Counting
- Count UNIQUE districts across ALL dailyUpdates entries
- Districts visited so far (as of 2025-10-28): SAS Nagar
- If a new district is visited for the first time, increment the counter
- District names should match existing entries (check spelling)

### Common Districts in Punjab
SAS Nagar, Patiala, Ludhiana, Fatehgarh Sahib, Roopnagar, Sangroor, Mansa, Barnala, Bathinda, Mukatsar Sahib, Malerkotla, Fazilka, Ferozepur, Faridkot, Moga, Pathankot

### Data Integrity
- Always validate JSON syntax before committing
- Verify coordinates are in decimal degrees format
- Ensure student counts are positive integers
- Check that dates follow YYYY-MM-DD format
- Verify OneDrive links are complete and accessible

### Git Branch Naming
- Always use pattern: `claude/session-<ID>`
- ID should be unique for each session
- Never push to `main` directly
- Never force push

### Error Handling
If errors occur:
1. Validate JSON syntax first
2. Check for missing commas in arrays/objects
3. Verify all required fields are present
4. Ensure numbers are not quoted
5. Confirm coordinates are valid lat/lng values

## Quick Reference

### Haversine Formula (Python)
```python
import math

def calculate_route_distance(waypoints):
    """
    waypoints: list of (lat, lng) tuples
    Returns: total distance in km (rounded)
    """
    R = 6371
    total = 0

    for i in range(len(waypoints) - 1):
        lat1, lon1 = waypoints[i]
        lat2, lon2 = waypoints[i + 1]

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        total += R * c

    return round(total)

# Usage:
waypoints = [
    (30.6310588, 76.7230178),  # Plaksha
    (30.7234, 76.7123),        # School 1
    (30.7845, 76.7956),        # School 2
    (30.6310588, 76.7230178)   # Back to Plaksha
]
distance = calculate_route_distance(waypoints)
```

### JSON Editing Tips
- Use `Edit` tool for targeted changes (preferred)
- Preserve exact indentation (2 spaces per level)
- Add commas between array/object elements
- Don't add comma after last element
- Strings must be double-quoted
- Numbers should not be quoted

### File Locations
- Repository: `science-on-wheels`
- Data file: `/home/user/science-on-wheels/data.json`
- Gallery file: `/home/user/science-on-wheels/schools-gallery.json`
- Website URL: https://shashanktamaskar.github.io/science-on-wheels/

---

## Checklist

Before committing, verify:
- [ ] Both JSON files are valid (syntax check)
- [ ] lastUpdated date is correct
- [ ] Mission statistics are correctly calculated
- [ ] Distance calculation is accurate
- [ ] New dailyUpdates entry is at beginning of array
- [ ] All schools added to gallery
- [ ] OneDrive links are complete
- [ ] Collage images uploaded to gallery_school_collage/ folder
- [ ] Image filenames match school names in JSON EXACTLY
- [ ] Image formats are supported (.jpg, .jpeg, .png, or .webp)
- [ ] No spelling/capitalization mismatches between JSON and filenames
- [ ] Commit message is descriptive
- [ ] Changes pushed to correct branch
- [ ] PR link provided to user

---

**Last Updated:** 2025-10-28
**Maintained By:** Science on Wheels Team
**Repository:** https://github.com/shashanktamaskar/science-on-wheels