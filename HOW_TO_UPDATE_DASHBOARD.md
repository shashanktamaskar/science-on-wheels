# How to Update the Dashboard

This guide explains how to update the Science on Wheels project dashboard, including mission statistics, gallery photos, testimonials, and demographic data.

## Overview

The dashboard displays live data from `data.json`. All updates happen by editing this single file - no code knowledge required!

**Dashboard Location:** The project dashboard is on the **Home page** of the website.

---

## What You Can Update

### 1. Mission Statistics
### 2. School Demographics
### 3. Photo Gallery
### 4. Testimonials
### 5. Helpline Information

---

## 1. Mission Statistics

### Location in data.json: Lines 11-23

Update the mission progress as you visit schools:

```json
"mission": {
  "schoolsCovered": {
    "current": 50,        ← Update as you visit schools
    "total": 235
  },
  "districtsCovered": {
    "current": 3,         ← Update when you complete a district
    "total": 16
  },
  "studentsImpacted": 1500,    ← Update with total students reached
  "distanceTravelled": 250     ← Update with kilometers traveled
}
```

**Progress bars update automatically** based on these numbers!

---

## 2. School Demographics

### Location in data.json: Lines 150-155

Update the breakdown of schools by type:

```json
"demographics": {
  "tribal": 6,         ← Number of tribal schools visited
  "rural": 4,          ← Number of rural schools visited
  "semiUrban": 3,      ← Number of semi-urban schools visited
  "urban": 3           ← Number of urban schools visited
}
```

**Note:** These numbers should add up to the current schools covered.

---

## 3. Photo Gallery

The gallery feature is ready but requires you to add photos first.

### Step 1: Add Photos to Gallery Folder

1. Take photos during school visits
2. Rename them clearly (e.g., `ludhiana_school1.jpg`, `ludhiana_robotics_workshop.jpg`)
3. Copy photos to the `gallery/` folder in your project

### Step 2: Update data.json

Location in data.json: Lines 156-169

```json
"gallery": [
  {
    "district": "Ludhiana",
    "images": [
      "ludhiana_school1.jpg",
      "ludhiana_robotics_workshop.jpg",
      "ludhiana_students.jpg"
    ]
  },
  {
    "district": "Patiala",
    "images": [
      "patiala_water_testing.jpg",
      "patiala_group_photo.jpg"
    ]
  }
]
```

**Instructions:**
- Add a new district entry for each district you visit
- List all photo filenames for that district
- Use exact filenames (with .jpg or .png extension)
- Photos will appear on the website automatically!

---

## 4. Testimonials

### Location in data.json: Lines 170-183

Add student/teacher feedback:

```json
"testimonials": [
  {
    "name": "Rajveer Singh",
    "school": "PM Shri School, Ludhiana",
    "text": "The robotics workshop was amazing! I learned so much about coding and building robots.",
    "date": "2025-10-20"
  },
  {
    "name": "Ms. Priya Sharma",
    "school": "PM Shri School, Patiala",
    "text": "This program has inspired our students to pursue science and technology. Excellent initiative!",
    "date": "2025-10-22"
  }
]
```

**To add a new testimonial:**
1. Copy one testimonial block
2. Update: name, school, text, date
3. Add a comma before it if it's not the last item

---

## 5. Helpline Information

### Location in data.json: Lines 184-189

Update contact information and links:

```json
"helpline": {
  "feedbackForm": "https://forms.gle/your-form-link",     ← Google Form link
  "website": "https://shashanktamaskar.github.io/science-on-wheels/",
  "email": "rucha.joshi@plaksha.edu.in",
  "phone": "+91 8358082703"
}
```

---

## Complete Daily Update Workflow

### Every Day After Visiting Schools:

1. **Open `data.json`** in your text editor

2. **Update Mission Stats:**
   - Increment `schoolsCovered.current`
   - Update `studentsImpacted`
   - Update `distanceTravelled`
   - Update `districtsCovered.current` if you finished a district

3. **Update Demographics:**
   - Add 1 to the appropriate school type (tribal/rural/semiUrban/urban)

4. **Update Vehicle Location** (see `HOW_TO_UPDATE_VEHICLES.md`)

5. **Add Photos** (if you took any):
   - Copy photos to `gallery/` folder
   - Add filenames to the district's `images` array

6. **Add Testimonials** (if you collected any):
   - Add new testimonial entries

7. **Update Last Modified Date:**
   ```json
   "lastUpdated": "2025-10-20"    ← Today's date
   ```

8. **Save and Deploy:**
   ```bash
   git add data.json gallery/
   git commit -m "Daily update: [district name], [X] schools visited"
   git push
   ```

9. **Verify:** Wait 2-3 minutes, then check the website!

---

## Example: Complete Daily Update

**Date:** October 20, 2025
**Activity:** Visited 5 schools in Ludhiana (3 rural, 2 urban), reached 150 students, took 3 photos, got 1 testimonial

### Changes to Make:

```json
{
  "lastUpdated": "2025-10-20",        ← Changed from 2025-01-14

  "mission": {
    "schoolsCovered": {
      "current": 5,                    ← Changed from 0
      "total": 235
    },
    "districtsCovered": {
      "current": 1,                    ← Still in first district
      "total": 16
    },
    "studentsImpacted": 150,           ← Changed from 0
    "distanceTravelled": 45            ← Changed from 0
  },

  "demographics": {
    "tribal": 0,                       ← No change
    "rural": 3,                        ← Changed from 0
    "semiUrban": 0,                    ← No change
    "urban": 2                         ← Changed from 0
  },

  "gallery": [
    {
      "district": "Ludhiana",
      "images": [
        "ludhiana_school1.jpg",
        "ludhiana_robotics.jpg",
        "ludhiana_students.jpg"
      ]
    }
  ],

  "testimonials": [
    {
      "name": "Rajveer Singh",
      "school": "PM Shri School, Ludhiana",
      "text": "The robotics workshop was amazing!",
      "date": "2025-10-20"
    }
  ]
}
```

---

## Photo Guidelines

### Best Practices:
- ✅ Take photos of students engaged in activities
- ✅ Capture workshops, demonstrations, and hands-on learning
- ✅ Get group photos with teachers and students
- ✅ Show the Science on Wheels van in action
- ✅ Ask for verbal permission before photographing students

### Technical Requirements:
- Format: JPG or PNG
- File size: Under 2MB per photo (compress if needed)
- Naming: Use lowercase, no spaces (use underscores)
  - Good: `ludhiana_robotics_workshop.jpg`
  - Bad: `Ludhiana Robotics Workshop.JPG`

---

## Testimonial Guidelines

### What to Collect:
- Student reactions and learnings
- Teacher feedback on program impact
- School principal endorsements
- Parent observations (if available)

### How to Record:
1. Write down the exact quote
2. Get the person's name (or use "Anonymous Student")
3. Note the school name
4. Record the date

### Adding to Website:
- Keep quotes concise (1-3 sentences)
- Ensure proper grammar and spelling
- Include first name + last initial for privacy (e.g., "Rajveer S.")
- Or use generic titles: "Grade 9 Student", "Science Teacher", etc.

---

## Demographics Tracking

Keep a daily log of schools visited by type:

| Date | School Name | Type | Students |
|------|-------------|------|----------|
| Oct 20 | PM Shri School A | Rural | 30 |
| Oct 20 | PM Shri School B | Rural | 35 |
| Oct 20 | PM Shri School C | Urban | 40 |

At end of day, sum up each type and update demographics in data.json.

---

## Quick Reference: File Locations

```
Science_on_Wheels/
├── data.json                    ← Main file to edit
├── gallery/                     ← Put photos here
│   ├── ludhiana_school1.jpg
│   ├── patiala_robotics.jpg
│   └── ...
├── HOW_TO_UPDATE_VEHICLES.md    ← Vehicle location guide
└── HOW_TO_UPDATE_DASHBOARD.md   ← This file
```

---

## Troubleshooting

**Q: Dashboard not updating after pushing changes?**
- Wait 3-5 minutes for GitHub Actions
- Hard refresh browser (Ctrl+F5 or Cmd+Shift+R)
- Check GitHub Actions tab for deployment status

**Q: Photos not showing on website?**
- Verify photos are in `gallery/` folder
- Check filenames match exactly in data.json (case-sensitive!)
- Ensure photos were committed and pushed to GitHub

**Q: Numbers not adding up correctly?**
- `schoolsCovered.current` should equal sum of all demographics
- `districtsCovered.current` should not exceed `total` (16)

**Q: Invalid JSON error?**
- Use https://jsonlint.com/ to validate
- Common mistakes:
  - Missing comma between items
  - Extra comma after last item in array
  - Quotes around numbers (wrong: "5", right: 5)

---

## Need Help?

Contact:
- Dr. Rucha Joshi: rucha.joshi@plaksha.edu.in | +91 8358082703
- Dr. Shashank Tamaskar: shashank.tamaskar@plaksha.edu.in

---

**Last Updated:** January 14, 2025
