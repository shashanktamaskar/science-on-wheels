# Daily Update Instructions for Science on Wheels

This guide provides detailed, step-by-step instructions for adding daily school visit data to the repository. These instructions can be followed by any AI tool or developer.

## Quick Overview

**Two files need updating:**
1. `data.json` - Mission statistics and daily visit records
2. `schools-gallery.json` - Gallery index with school photo links

**Current Statistics** (as of 2025-12-05):
- Schools covered: 69
- Students impacted: 33,676
- Girls: 19,118
- Boys: 14,586
- Districts: 6 (SAS Nagar, Ludhiana, Fatehgarh Sahib, Roopnagar, Malerkotla, Patiala)

---

## Input Data Format

You'll receive data in this format:

```
Date: 2025-MM-DD
Vehicle: Vehicle-1 (or Vehicle-2)
Schools visited:

SCHOOL-NAME - Coordinates: (latitude, longitude) - Students: XXX - Girls: XX - Boys: XX - District: District Name

Start Point: Location Name (latitude, longitude)
End Point: Location Name (latitude, longitude)

Gallery Links:
SCHOOL-NAME: https://sharepoint-url

Collage Images:
SCHOOL-NAME: SCHOOL-NAME.jpg
```

---

## Step 1: Calculate New Statistics

### 1.1: Count New Schools and Students

```
New schools = Current schools + Number of schools in today's data
New students = Current students + Sum of all students today
New girls = Current girls + Sum of all girls today
New boys = Current boys + Sum of all boys today
```

### 1.2: Check Districts

Current districts: SAS Nagar, Ludhiana, Fatehgarh Sahib, Roopnagar, Malerkotla, Patiala

If the visit includes a NEW district not in this list:
```
New districts = Current districts + 1
```
Otherwise, keep districts the same.

---

## Step 2: Update data.json

### 2.1: Update Header Information

**Location:** Lines 2, 13, 20, 22-23

```json
{
  "lastUpdated": "2025-MM-DD",  // Update to today's date
  ...
  "mission": {
    "schoolsCovered": {
      "current": XX,  // New school count
      "total": 235
    },
    "districtsCovered": {
      "current": X,  // New district count (usually stays same)
      "total": 16
    },
    "studentsImpacted": XXXXX,  // New total students
    "genderBreakdown": {
      "girls": XXXXX,  // New total girls
      "boys": XXXXX   // New total boys
    },
    "distanceTravelled": 480,
    "targetAudience": "Students from Classes 6-12"
  }
}
```

### 2.2: Add New Daily Update Entry

**Location:** Add at the **BEGINNING** of the `dailyUpdates` array (line 28, right after `"dailyUpdates": [`)

**Template:**
```json
{
  "date": "2025-MM-DD",
  "vehicle": 1,  // or 2, based on which vehicle
  "schools": [
    {
      "name": "SCHOOL-NAME-WITH-HYPHENS",
      "location": {
        "lat": 30.1234567,
        "lng": 76.1234567
      },
      "studentsReached": XXX,
      "girlsCount": XXX,
      "boysCount": XXX,
      "district": "District Name",
      "galleryLink": "https://sharepoint-url",
      "collageImage": "SCHOOL-NAME-WITH-HYPHENS.jpg"
    }
    // Add more schools here if multiple schools visited
  ],
  "route": {
    "startPoint": {
      "name": "Location Name",
      "lat": 30.1234567,
      "lng": 76.1234567
    },
    "endPoint": {
      "name": "Location Name",
      "lat": 30.1234567,
      "lng": 76.1234567
    },
    "distanceTravelled": 0  // Usually set to 0
  },
  "totalStudents": XXX,  // Sum of all studentsReached
  "schoolsVisited": X     // Count of schools in array
},
```

**Critical Notes:**
- Add a **comma** after the closing `}` (since there are existing entries below)
- School names must use **hyphens not spaces** (e.g., "GSSS-SCHOOL-NAME" not "GSSS SCHOOL NAME")
- This ensures names match the collage image filenames
- For multiple schools in one day, add multiple objects in the `schools` array

### 2.3: Multiple Vehicles on Same Day

If both Vehicle 1 and Vehicle 2 operated on the same date:
- Create TWO separate daily update entries
- One entry for Vehicle 1 (with `"vehicle": 1`)
- One entry for Vehicle 2 (with `"vehicle": 2`)
- Both entries have the same date
- Add both entries at the beginning of the array

---

## Step 3: Update schools-gallery.json

### 3.1: Add School Entries

**Location:** Add at the **BEGINNING** of the `schools` array (line 2, right after `"schools": [`)

**Template for each school:**
```json
{
  "name": "SCHOOL-NAME-WITH-HYPHENS",
  "district": "District Name",
  "visitDate": "2025-MM-DD",
  "folderUrl": "https://sharepoint-gallery-url"
},
```

**Critical Notes:**
- Add one entry for **each** school visited
- School name must **exactly match** the name in data.json
- Add a **comma** after the closing `}` (since there are existing entries below)
- Newest schools go at the top (chronological order, newest first)

---

## Step 4: Validate JSON Files

**Run these commands to check for syntax errors:**

```bash
python3 -c "import json; json.load(open('data.json'))" && echo "data.json is valid"
python3 -c "import json; json.load(open('schools-gallery.json'))" && echo "schools-gallery.json is valid"
```

**If validation fails:**
- Check for missing commas between objects in arrays
- Check for extra commas after the last item in an array
- Check for mismatched brackets `{}` or braces `[]`
- Check for unescaped characters in URLs (though most should be fine)

---

## Step 5: Commit and Push

```bash
# Stage the modified files
git add data.json schools-gallery.json

# Commit with descriptive message
git commit -m "Add school visit data for YYYY-MM-DD - Vehicle X

- Added [school names] ([student counts])
- Updated mission statistics (X schools, X,XXX total students)
- Added gallery entries
- District: [district name]"

# Push to branch
git push origin [branch-name]
```

---

## Complete Example

### Input Data:
```
Date: 2025-12-06
Vehicle: Vehicle-1
Schools visited:

GSSS-EXAMPLE - Coordinates: (30.5000000, 76.5000000) - Students: 500 - Girls: 250 - Boys: 250 - District: Patiala

Start Point: Patiala, Punjab (30.3449167, 76.39775)
End Point: Patiala, Punjab (30.3449167, 76.39775)

Gallery Links:
GSSS-EXAMPLE: https://plakshauniversity1-my.sharepoint.com/:f:/example

Collage Images:
GSSS-EXAMPLE: GSSS-EXAMPLE.jpg
```

### Step 1: Calculate Statistics

**Current** (from data.json):
- Schools: 69
- Students: 33,676
- Girls: 19,118
- Boys: 14,586
- Districts: 6 (Patiala already counted)

**New** (adding today's data):
- Schools: 69 + 1 = **70**
- Students: 33,676 + 500 = **34,176**
- Girls: 19,118 + 250 = **19,368**
- Boys: 14,586 + 250 = **14,836**
- Districts: **6** (no change, Patiala already in list)

### Step 2: Update data.json

**Update lines 2, 13, 20, 22-23:**
```json
"lastUpdated": "2025-12-06",
...
"current": 70,
...
"studentsImpacted": 34176,
"genderBreakdown": {
  "girls": 19368,
  "boys": 14836
}
```

**Add at line 28 (beginning of dailyUpdates array):**
```json
{
  "date": "2025-12-06",
  "vehicle": 1,
  "schools": [
    {
      "name": "GSSS-EXAMPLE",
      "location": {
        "lat": 30.5000000,
        "lng": 76.5000000
      },
      "studentsReached": 500,
      "girlsCount": 250,
      "boysCount": 250,
      "district": "Patiala",
      "galleryLink": "https://plakshauniversity1-my.sharepoint.com/:f:/example",
      "collageImage": "GSSS-EXAMPLE.jpg"
    }
  ],
  "route": {
    "startPoint": {
      "name": "Patiala, Punjab",
      "lat": 30.3449167,
      "lng": 76.39775
    },
    "endPoint": {
      "name": "Patiala, Punjab",
      "lat": 30.3449167,
      "lng": 76.39775
    },
    "distanceTravelled": 0
  },
  "totalStudents": 500,
  "schoolsVisited": 1
},
```

### Step 3: Update schools-gallery.json

**Add at line 2 (beginning of schools array):**
```json
{
  "name": "GSSS-EXAMPLE",
  "district": "Patiala",
  "visitDate": "2025-12-06",
  "folderUrl": "https://plakshauniversity1-my.sharepoint.com/:f:/example"
},
```

### Step 4: Validate and Commit

```bash
python3 -c "import json; json.load(open('data.json'))" && echo "valid"
python3 -c "import json; json.load(open('schools-gallery.json'))" && echo "valid"

git add data.json schools-gallery.json
git commit -m "Add school visit data for December 6, 2025 - Vehicle 1

- Added GSSS-EXAMPLE (500 students: 250 girls, 250 boys)
- Updated mission statistics (70 schools, 34,176 total students)
- Added gallery entry
- District: Patiala"

git push origin claude/add-school-visit-data-01N2BzaEyuWyRGZoaT3Xynu3
```

---

## Common Mistakes to Avoid

1. **School Name Formatting**
   - ❌ "GSSS SCHOOL NAME" (spaces)
   - ✅ "GSSS-SCHOOL-NAME" (hyphens)
   - Must match collage filename exactly

2. **Missing Commas**
   - Add comma after `}` when there are more entries below
   - Don't add comma after the last entry in an array

3. **Wrong Insertion Point**
   - ❌ Adding new entries at the end of arrays
   - ✅ Adding new entries at the BEGINNING of arrays

4. **Statistics Errors**
   - Always double-check your addition
   - Use current values from data.json, not old values

5. **District Counting**
   - Only increment if it's a NEW district
   - Current districts: SAS Nagar, Ludhiana, Fatehgarh Sahib, Roopnagar, Malerkotla, Patiala

6. **Date Format**
   - ❌ "12-05-2025" or "05/12/2025"
   - ✅ "2025-12-05" (YYYY-MM-DD)

7. **Coordinate Precision**
   - Use 7 decimal places (e.g., 30.1234567)
   - Don't round to fewer decimals

---

## Verification Checklist

Before committing, verify:
- [ ] JSON files are syntactically valid (ran validation commands)
- [ ] `lastUpdated` date matches today's date
- [ ] Mission statistics are correctly calculated
- [ ] New daily update entry is at the BEGINNING of dailyUpdates array
- [ ] School names use hyphens (match collage filenames)
- [ ] `totalStudents` and `schoolsVisited` match the data in the entry
- [ ] New school entries are at the BEGINNING of schools array in schools-gallery.json
- [ ] All required fields are present
- [ ] Commit message is descriptive
- [ ] Pushing to correct branch

---

## Key Field Descriptions

### data.json Structure

```json
{
  "lastUpdated": "YYYY-MM-DD",  // Date of last update
  "mission": {
    "schoolsCovered": {
      "current": XX,  // Schools visited so far
      "total": 235    // Total target schools
    },
    "studentsImpacted": XXXXX,  // Total students reached
    "genderBreakdown": {
      "girls": XXXXX,
      "boys": XXXXX
    }
  },
  "dailyUpdates": [
    {
      "date": "YYYY-MM-DD",
      "vehicle": 1,  // Which vehicle (1 or 2)
      "schools": [...],  // Array of schools visited
      "route": {...},    // Start/end points
      "totalStudents": XXX,     // Sum for this day
      "schoolsVisited": X       // Count for this day
    }
  ]
}
```

### schools-gallery.json Structure

```json
{
  "schools": [
    {
      "name": "SCHOOL-NAME",    // Must match data.json exactly
      "district": "District",   // District name
      "visitDate": "YYYY-MM-DD",
      "folderUrl": "https://..."  // Gallery link
    }
  ]
}
```

---

## Current Statistics Reference

**As of 2025-12-05:**
- **Schools covered**: 69
- **Students impacted**: 33,676
- **Girls**: 19,118
- **Boys**: 14,586
- **Districts covered**: 6

**Current Districts:**
1. SAS Nagar
2. Ludhiana
3. Fatehgarh Sahib
4. Roopnagar
5. Malerkotla
6. Patiala

---

## Troubleshooting

### JSON Validation Errors

**Error: "Expecting ',' delimiter"**
- Missing comma between array/object elements
- Add comma after previous entry

**Error: "Extra data"**
- Trailing comma after last array element
- Remove comma after final entry

**Error: "Unterminated string"**
- Check for unescaped quotes in URLs
- Ensure all strings are properly closed

### Git Errors

**Error: "Updates were rejected"**
- Run `git pull origin [branch-name]` first
- Then try pushing again

**Error: "Permission denied"**
- Check branch name is correct
- Verify you have write access

---

## Additional Resources

- **Repository**: https://github.com/shashanktamaskar/science-on-wheels
- **Website**: https://shashanktamaskar.github.io/science-on-wheels/
- **Current Branch**: claude/add-school-visit-data-01N2BzaEyuWyRGZoaT3Xynu3

---

**Last Updated**: 2025-12-05
**Current Statistics**: 69 schools, 33,676 students (19,118 girls, 14,586 boys)
