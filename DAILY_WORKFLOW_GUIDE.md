# 📋 Science on Wheels - Daily Workflow Guide

> **For AI Assistants:** This guide contains detailed instructions so any AI model can help with this workflow.

---

## 🚀 Quick Daily Workflow (5 Steps)

### Step 1: Collect Data from Field Team
User provides:
- Date, Vehicle number (1 or 2)
- School names with Google Maps links
- Student counts (Total, Girls, Boys)
- District names
- Start/End point Google Maps links
- SharePoint gallery folder URLs

### Step 2: Input Format
User pastes data in this format:
```
**Date:** YYYY-MM-DD
**Vehicle:** Vehicle-1 or Vehicle-2
**Schools visited:**

SCHOOL NAME - Map Link: https://maps.app.goo.gl/xxx - Students: ### - Girls: ### - Boys: ### - District: DistrictName

**Start Point:** Location - Map Link: https://maps.app.goo.gl/xxx
**End Point:** Location - Map Link: https://maps.app.goo.gl/xxx

**Gallery Links:**
SCHOOL NAME: https://plakshauniversity1-my.sharepoint.com/...
```

---

### Step 3: Data Processing (AI Instructions)

#### 3.1 Extract Coordinates
**For each Google Maps short link (maps.app.goo.gl):**
1. Open the URL in browser or use HTTP request
2. Get the redirected full URL
3. Extract coordinates from URL pattern: `@LAT,LNG` or `!3dLAT!4dLNG`
4. Example: `@30.3789968,76.1517648` → lat=30.3789968, lng=76.1517648

#### 3.2 Calculate Distance
Use Haversine formula:
```python
import math
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))
```
Calculate: start → school1 → school2 → ... → end (sum all segments)

#### 3.3 Update data.json
Location: `Website/data.json`

**Add to `dailyUpdates` array (insert at position 0):**
```json
{
    "date": "YYYY-MM-DD",
    "vehicle": 1,
    "schools": [
        {
            "name": "SCHOOL NAME",
            "location": {"lat": 30.xxx, "lng": 76.xxx},
            "studentsReached": 500,
            "girlsCount": 250,
            "boysCount": 250,
            "district": "District Name",
            "galleryLink": "https://sharepoint-url...",
            "collageImage": "SCHOOL-NAME.jpg"
        }
    ],
    "route": {
        "startPoint": {"name": "Location", "lat": 30.xxx, "lng": 76.xxx},
        "endPoint": {"name": "Location", "lat": 30.xxx, "lng": 76.xxx},
        "distanceTravelled": 45
    },
    "totalStudents": 500,
    "schoolsVisited": 1
}
```

**Update cumulative stats in `mission` object:**
```python
data['mission']['schoolsCovered']['current'] += num_schools
data['mission']['studentsImpacted'] += total_students
data['mission']['genderBreakdown']['girls'] += total_girls
data['mission']['genderBreakdown']['boys'] += total_boys
data['mission']['distanceTravelled'] += distance
data['lastUpdated'] = "YYYY-MM-DD"
```

#### 3.4 Update schools-gallery.json
Location: `Website/schools-gallery.json`

**Append to `schools` array:**
```json
{
    "name": "SCHOOL NAME",
    "district": "District Name",
    "visitDate": "YYYY-MM-DD",
    "folderUrl": "https://sharepoint-gallery-url..."
}
```

#### 3.5 Provide Formatted Output
**Return to user in this exact format:**
```
**Date:** YYYY-MM-DD
**Vehicle:** Vehicle-X
**Schools visited:**

SCHOOL NAME - Coordinates: (LAT, LNG) - Students: ### - Girls: ### - Boys: ### - District: DistrictName

**Start Point:** Location Name (LAT, LNG)
**End Point:** Location Name (LAT, LNG)

**Gallery Links:**
SCHOOL NAME: https://sharepoint-url...

**Collage Images:**
SCHOOL NAME: SCHOOL-NAME.jpg
```

---

### Step 4: Collage Generation (AI Instructions)

#### 4.1 File Paths
- **AI Collage Tool:** `AI-Collage-Tool/collage_generator_final.py`
- **Logo:** `AI-Collage-Tool/science_on_wheels_logo.png`
- **Output folder:** `Website/gallery_school_collage/`
- **API Key:** `AI-Collage-Tool/api_key.py` (contains `API_KEY` variable)

#### 4.2 Generate Collage Script
Create and run a Python script:
```python
import os, sys, zipfile, tempfile, shutil, glob
sys.path.insert(0, "path/to/AI-Collage-Tool")
from collage_generator_final import (setup_gemini, get_best_photos, 
    create_collage_with_header, rate_collage, parse_grid_layout)
from api_key import API_KEY

# Configuration
LOGO = "path/to/science_on_wheels_logo.png"
GRID = "3x2"  # 6 photos
TARGET_SCORE = 8.0
MAX_RETRIES = 3
MODEL = "gemini-2.0-flash-exp"

# Extract zip to temp folder
temp_dir = tempfile.mkdtemp()
with zipfile.ZipFile("path/to/SCHOOL.zip", 'r') as z:
    z.extractall(temp_dir)

# Find images
images = glob.glob(os.path.join(temp_dir, "*.jpg")) + \
         glob.glob(os.path.join(temp_dir, "*.JPG"))

# Setup AI and generate
setup_gemini(API_KEY)
grid = parse_grid_layout(GRID)

for attempt in range(MAX_RETRIES):
    selected = get_best_photos(images, LOGO, "SCHOOL NAME", 
                               "District", "Date", count=6, model_name=MODEL)
    output = "path/to/gallery_school_collage/SCHOOL-NAME.jpg"
    create_collage_with_header(selected, output, "SCHOOL NAME", 
                               "District", "Date", LOGO, grid, (540, 405))
    rating, score = rate_collage(output, LOGO, "SCHOOL NAME", 
                                 "District", "Date", MODEL)
    if score >= TARGET_SCORE:
        break

shutil.rmtree(temp_dir)  # Cleanup
```

#### 4.3 File Naming Convention
| School Name in Data | Collage File Name |
|---------------------|-------------------|
| `GSSS G SAMANA` | `GSSS-G-SAMANA.jpg` |
| `GSSS(GIRLS) NABHA` | `GSSS-GIRLS-NABHA.jpg` |
| `GSSS DHANETHA` | `GSSS-DHANETHA.jpg` |

**Rules:** Spaces → hyphens, Remove `()` or convert to hyphens, Keep UPPERCASE

---

### Step 5: GitHub Upload (AI Instructions)

```bash
# Clone repo
git clone https://github.com/shashanktamaskar/science-on-wheels.git temp_repo

# Copy collage files
cp Website/gallery_school_collage/NEW-FILE.jpg temp_repo/gallery_school_collage/

# Commit and push
cd temp_repo
git add gallery_school_collage/*.jpg
git commit -m "Add collages for DATE: SCHOOL1 (V#), SCHOOL2 (V#)"
git push origin main

# Cleanup
cd ..
rm -rf temp_repo
```

---

## 📍 Key File Locations

| File | Path | Purpose |
|------|------|---------|
| Main data | `Website/data.json` | Cumulative stats & daily updates |
| Gallery data | `Website/schools-gallery.json` | Gallery links |
| Collages | `Website/gallery_school_collage/` | Generated images |
| AI Tool | `AI-Collage-Tool/` | Collage generator |
| Logo | `AI-Collage-Tool/science_on_wheels_logo.png` | Branding |

---

## ⚡ Quick Commands for User

| Action | Say This |
|--------|----------|
| Add school data | Paste in Step 2 format |
| Generate collage | "Generate collage from: [zip path]" |
| Upload to GitHub | "Upload collages to GitHub" |
| Get formatted output | "Give me data in output format" |
