# How to Update Vehicle Locations Daily

This guide explains how to update the Science on Wheels vehicle locations and progress on the website **without touching any code**.

## Overview

All vehicle information, including current locations and mission statistics, is stored in a single file called **`data.json`**. By editing this file, you can update the entire website automatically!

---

## Daily Update Procedure

### Step 1: Open the Data File

1. Navigate to your project folder:
   ```
   Science_on_Wheels/data.json
   ```

2. Open `data.json` in any text editor (Notepad, VS Code, etc.)

### Step 2: Update Vehicle Current Location

Find the section for each vehicle (lines 24-68) and update the `currentLocation` object:

```json
"currentLocation": {
  "name": "District Name or School Name",
  "district": "District Name",
  "lat": 30.xxxx,
  "lng": 76.xxxx,
  "date": "2025-10-20",
  "status": "active"
}
```

**What to update:**
- `name`: Where the vehicle is right now (e.g., "PM Shri School XYZ" or "Ludhiana")
- `district`: Current district name
- `lat` & `lng`: GPS coordinates (see coordinate list below)
- `date`: Today's date in YYYY-MM-DD format
- `status`: Change from "planned" to "active" when vehicle starts, or "completed" when done

### Step 3: Update Mission Statistics

Update the progress counters at the top of the file (lines 11-22):

```json
"mission": {
  "schoolsCovered": {
    "current": 15,    ← Update this number as you visit schools
    "total": 235
  },
  "districtsCovered": {
    "current": 2,     ← Update when you complete a district
    "total": 16
  },
  "studentsImpacted": 450,     ← Total students reached
  "distanceTravelled": 120     ← Total kilometers traveled
}
```

### Step 4: Update the Last Modified Date

At the very top of the file (line 2):

```json
"lastUpdated": "2025-10-20"    ← Change to today's date
```

### Step 5: Save and Upload

1. **Save** the `data.json` file
2. **Commit and push** to GitHub:
   ```bash
   git add data.json
   git commit -m "Update vehicle locations for [date]"
   git push
   ```

3. Wait 2-3 minutes for GitHub Pages to rebuild
4. Check your website: https://shashanktamaskar.github.io/science-on-wheels/

---

## GPS Coordinates Reference

Here are the coordinates for each district in the schedule:

### Vehicle 1 Route:
| District | Latitude | Longitude |
|----------|----------|-----------|
| SAS Nagar | 30.7046 | 76.7179 |
| Fatehgarh Sahib | 30.6444 | 76.3965 |
| Roopnagar | 31.0374 | 76.5265 |
| Ludhiana | 30.9010 | 75.8573 |
| Sangroor | 30.2458 | 75.8421 |
| Mansa | 29.9988 | 75.3936 |
| Barnala | 30.3784 | 75.5489 |
| Bathinda | 30.2084 | 74.9456 |
| Mukatsar Sahib | 30.4755 | 74.5151 |

### Vehicle 2 Route:
| District | Latitude | Longitude |
|----------|----------|-----------|
| Patiala | 30.3398 | 76.3869 |
| Malerkotla | 30.5311 | 75.8819 |
| Fazilka | 30.4028 | 74.0281 |
| Ferozepur | 30.9191 | 74.8750 |
| Faridkot | 30.6705 | 74.7570 |
| Moga | 30.8158 | 75.1705 |
| Pathankot | 32.2746 | 75.6521 |

### Special Location:
| Location | Latitude | Longitude |
|----------|----------|-----------|
| Plaksha University | 30.6310588 | 76.7255981 |

---

## Example: Daily Update

**Scenario:** It's October 20, 2025. Vehicle 1 is now in Ludhiana, has covered 3 districts, visited 50 schools total, impacted 1,500 students, and traveled 200 km.

### What to Change:

```json
{
  "lastUpdated": "2025-10-20",    ← Update date

  "mission": {
    "schoolsCovered": {
      "current": 50,                ← Was 0, now 50
      "total": 235
    },
    "districtsCovered": {
      "current": 3,                 ← Was 0, now 3
      "total": 16
    },
    "studentsImpacted": 1500,       ← Was 0, now 1500
    "distanceTravelled": 200        ← Was 0, now 200
  },

  "vehicles": [
    {
      "id": 1,
      "name": "Vehicle 1",
      "currentLocation": {
        "name": "Ludhiana",         ← Update name
        "district": "Ludhiana",     ← Update district
        "lat": 30.9010,             ← Update lat
        "lng": 75.8573,             ← Update lng
        "date": "2025-10-20",       ← Update date
        "status": "active"          ← Change to active
      },
      "schedule": [
        ...
      ]
    }
  ]
}
```

---

## Getting Specific School Coordinates

If you want to show the vehicle at a specific school (not just district center):

1. **Find the school on Google Maps**
2. **Right-click** on the school location
3. **Click the coordinates** that appear
4. **Copy** the latitude and longitude
5. **Paste** into the `lat` and `lng` fields in data.json

---

## Quick Commands Cheat Sheet

### Update and Deploy in 3 Commands:

```bash
# 1. Stage your changes
git add data.json

# 2. Commit with a descriptive message
git commit -m "Daily update: Vehicle 1 in Ludhiana, 50 schools visited"

# 3. Push to GitHub (triggers auto-deployment)
git push
```

---

## Troubleshooting

**Q: Website not updating after I pushed?**
- Wait 3-5 minutes for GitHub Actions to complete
- Check the "Actions" tab in your GitHub repository
- Make sure the deployment workflow succeeded

**Q: Map not showing vehicles correctly?**
- Double-check latitude and longitude values
- Make sure coordinates are numbers, not strings
- Verify the format is: `"lat": 30.xxxx` (no quotes around numbers)

**Q: Invalid JSON error?**
- Use a JSON validator: https://jsonlint.com/
- Common mistakes:
  - Missing commas between items
  - Extra comma after last item
  - Missing closing brackets `}` or `]`

---

## Need Help?

Contact:
- Dr. Rucha Joshi: rucha.joshi@plaksha.edu.in | +91 8358082703
- Dr. Shashank Tamaskar: shashank.tamaskar@plaksha.edu.in

---

**Last Updated:** January 14, 2025
