# How to Update the Photo Gallery

This guide explains how to add schools to the Science on Wheels gallery after each visit.

## Overview

The gallery is **fully data-driven** from a single JSON file: `schools-gallery.json`

✅ **You only edit ONE file** - No HTML/CSS/design changes needed
✅ **Districts/villages appear automatically** - Only visited locations show in filters
✅ **Recently Visited updates automatically** - Newest schools appear first
✅ **Takes 5 minutes per day** - Simple workflow

---

## Daily Workflow (After Visiting Schools)

### Step 1: Upload Photos to OneDrive

1. Log in to [OneDrive.com](https://onedrive.live.com)
2. Create a folder for each school: `SchoolName_Village_District`
3. Upload all photos for that school to its folder
4. Set sharing to **"Anyone with the link can view"**

### Step 2: Get OneDrive Embed Code

For each school folder:
1. Click the `...` menu on the folder
2. Select **"Embed"**
3. Copy the embed URL (starts with `https://onedrive.live.com/embed?resid=...`)

### Step 3: Update `schools-gallery.json`

Open `schools-gallery.json` and add your new schools:

```json
{
  "schools": [
    {
      "name": "PM Shri Senior Secondary School",
      "district": "SAS Nagar",
      "village": "Mohali",
      "visitDate": "2025-10-25",
      "embedUrl": "https://onedrive.live.com/embed?resid=ABC123..."
    },
    {
      "name": "PM Shri Government High School",
      "district": "Ludhiana",
      "village": "Raikot",
      "visitDate": "2025-10-26",
      "embedUrl": "https://onedrive.live.com/embed?resid=XYZ789..."
    }
    // Add more schools here...
  ]
}
```

**Important:**
- Use exact district names (must match across all entries)
- Use exact village names (must match across all entries)
- Date format: `YYYY-MM-DD` (e.g., `2025-10-25`)
- Add commas between school entries

### Step 4: Commit and Push

```bash
git add schools-gallery.json
git commit -m "Add galleries for School ABC, School XYZ - Oct 25"
git push
```

**Done!** The website updates automatically within 1-2 minutes.

---

## How It Works

### Progressive Filters (Only Visited Locations Appear)

**Week 1** - Visited only SAS Nagar:
- District filter shows: **[SAS Nagar]** only
- Other 15 districts are hidden

**Week 3** - Visited 3 districts:
- District filter shows: **[SAS Nagar, Ludhiana, Patiala]**
- Villages only from those 3 districts appear

**Month 3** - Visited all 16 districts:
- All districts now appear in filter
- No code changes needed!

### Recently Visited Section

- Automatically shows last 10 schools visited
- Sorted by most recent first
- Click any school → Gallery loads instantly

### Student Experience

1. Student opens Gallery page
2. Sees "Recently Visited" with last 10 schools
3. Can click their school directly, OR
4. Use filters: District → Village → School
5. Gallery loads automatically when school is selected

---

## JSON Field Reference

```json
{
  "name": "Full school name",
  "district": "District name (must be exact match across entries)",
  "village": "Village name (must be exact match across entries)",
  "visitDate": "YYYY-MM-DD format (used for sorting)",
  "embedUrl": "OneDrive embed URL starting with https://onedrive.live.com/embed..."
}
```

---

## Example: Adding 3 Schools After Daily Visits

```json
{
  "schools": [
    // NEW: Schools visited today (Oct 25)
    {
      "name": "PM Shri Model Senior Secondary School",
      "district": "SAS Nagar",
      "village": "Kurali",
      "visitDate": "2025-10-25",
      "embedUrl": "https://onedrive.live.com/embed?resid=NEW1..."
    },
    {
      "name": "PM Shri Girls High School",
      "district": "SAS Nagar",
      "village": "Kharar",
      "visitDate": "2025-10-25",
      "embedUrl": "https://onedrive.live.com/embed?resid=NEW2..."
    },

    // Previously added schools below...
    {
      "name": "PM Shri Senior Secondary School",
      "district": "SAS Nagar",
      "village": "Mohali",
      "visitDate": "2025-10-24",
      "embedUrl": "https://onedrive.live.com/embed?resid=OLD1..."
    }
  ]
}
```

---

## Tips

### Consistent Naming
- Use same district names: `"SAS Nagar"` not `"S.A.S. Nagar"` or `"Sahibzada Ajit Singh Nagar"`
- Use same village names: `"Mohali"` not `"Mohali City"` or `"Mohali Town"`

### Date Format
- Always use: `YYYY-MM-DD`
- Good: `"2025-10-25"`
- Bad: `"25/10/2025"` or `"Oct 25, 2025"`

### OneDrive Folder Names
Suggested format: `SchoolName_Village_Date`
- Example: `PMShriSchool_Mohali_Oct25`

### Testing Embed URLs
Before adding to JSON, test the embed URL:
1. Open a new browser tab
2. Paste: `https://onedrive.live.com/embed?resid=YOUR_ID_HERE`
3. Should show OneDrive photo viewer

---

## Troubleshooting

### District not appearing in filter
- Check spelling matches exactly across all schools
- Case-sensitive: `"SAS Nagar"` ≠ `"sas nagar"`

### Village not appearing after selecting district
- Check village name spelling
- Ensure district for that school is correct

### School not appearing after selecting village
- Check all three fields (name, district, village) are correct
- Check for typos

### Gallery shows blank/error
- Check OneDrive embed URL is correct
- Ensure OneDrive folder is set to "Anyone can view"
- Try opening the embed URL directly in browser

### Recent visits not updating
- Check `visitDate` format is `YYYY-MM-DD`
- Ensure dates are correctly sorted (most recent first)

---

## Daily Checklist

After visiting schools:
- [ ] Upload photos to OneDrive (one folder per school)
- [ ] Set folders to "Anyone can view"
- [ ] Get embed URLs for each school
- [ ] Add entries to `schools-gallery.json`
- [ ] Double-check district/village spelling
- [ ] Verify date format (`YYYY-MM-DD`)
- [ ] Add commas between entries
- [ ] Test JSON is valid (no syntax errors)
- [ ] Commit with message: `"Add galleries for School A, School B - Oct 25"`
- [ ] Push to GitHub
- [ ] Verify gallery page updates (wait 1-2 minutes)

---

## Need Help?

**For technical assistance:**
- Dr. Rucha Joshi: rucha.joshi@plaksha.edu.in | +91 8358082703
- Dr. Shashank Tamaskar: shashank.tamaskar@plaksha.edu.in | +91 9041791024

**JSON Syntax Validator:**
- https://jsonlint.com/ - Paste your JSON to check for errors

---

**Last Updated:** October 2025
**Maintained by:** Plaksha University Science on Wheels Team
