# How to Update the Photo Gallery

This guide explains how to add schools to the Science on Wheels gallery after each visit.

## Overview

The gallery is a **simple table** showing all school visits with direct links to OneDrive photo folders.

✅ **You only edit ONE file** - `schools-gallery.json`
✅ **Simple OneDrive links** - Just share links (no embed codes!)
✅ **Takes 2 minutes per school** - Super simple workflow
✅ **Automatic updates** - Gallery updates when you push changes

---

## Daily Workflow (After Visiting Schools)

### Step 1: Upload Photos to OneDrive

1. Log in to [OneDrive.com](https://onedrive.live.com)
2. Create a folder for each school: `SchoolName_District_Date`
   - Example: `PMShriSchool_SASNagar_Oct26`
3. Upload all photos for that school to its folder
4. Set sharing to **"Anyone with the link can view"**

### Step 2: Get OneDrive Folder Link

For each school folder:
1. Right-click on the folder
2. Select **"Share"**
3. Click **"Copy link"**
4. You'll get a link like: `https://1drv.ms/f/s!ABC123...`

**That's it!** Much simpler than embed codes.

### Step 3: Update `schools-gallery.json`

Open `schools-gallery.json` and add your new schools:

```json
{
  "schools": [
    {
      "name": "PM Shri Senior Secondary School",
      "district": "SAS Nagar",
      "visitDate": "2025-10-25",
      "folderUrl": "https://1drv.ms/f/s!ABC123..."
    },
    {
      "name": "PM Shri Government High School",
      "district": "Ludhiana",
      "visitDate": "2025-10-26",
      "folderUrl": "https://1drv.ms/f/s!XYZ789..."
    }
  ]
}
```

**Important:**
- Use exact district names (must match across all entries)
- Date format: `YYYY-MM-DD` (e.g., `2025-10-25`)
- Add commas between school entries
- `folderUrl` is the OneDrive share link (NOT embed code)

### Step 4: Commit and Push

```bash
git add schools-gallery.json
git commit -m "Add galleries for School ABC, School XYZ - Oct 25"
git push
```

**Done!** The website updates automatically within 1-2 minutes.

---

## Gallery Display

The gallery shows a simple table with:
- **Date** - When you visited
- **School Name** - Full school name
- **District** - District name
- **Photos** - Button that opens OneDrive folder in new tab

**Features:**
- Sorted by newest visit first (Oct 25 at top)
- Mobile-friendly (horizontal scroll on small screens)
- Clean, simple design
- Direct access to OneDrive folders

---

## JSON Field Reference

```json
{
  "name": "Full school name",
  "district": "District name (must be exact match across entries)",
  "visitDate": "YYYY-MM-DD format (used for sorting)",
  "folderUrl": "OneDrive folder share link starting with https://1drv.ms/..."
}
```

---

## Example: Adding 3 Schools After Daily Visits

```json
{
  "schools": [
    {
      "name": "PM Shri Model Senior Secondary School",
      "district": "SAS Nagar",
      "visitDate": "2025-10-25",
      "folderUrl": "https://1drv.ms/f/s!AoZ7X..."
    },
    {
      "name": "PM Shri Girls High School",
      "district": "SAS Nagar",
      "visitDate": "2025-10-25",
      "folderUrl": "https://1drv.ms/f/s!BpY6W..."
    },
    {
      "name": "PM Shri Senior Secondary School",
      "district": "SAS Nagar",
      "visitDate": "2025-10-24",
      "folderUrl": "https://1drv.ms/f/s!CqX5V..."
    }
  ]
}
```

---

## Tips

### Consistent Naming
- Use same district names: `"SAS Nagar"` not `"S.A.S. Nagar"` or `"Sahibzada Ajit Singh Nagar"`
- Be consistent across all 250 schools

### Date Format
- Always use: `YYYY-MM-DD`
- Good: `"2025-10-25"`
- Bad: `"25/10/2025"` or `"Oct 25, 2025"`

### OneDrive Folder Names
Suggested format: `SchoolName_District_Date`
- Example: `PMShriSchool_SASNagar_Oct26`
- Easy to find and organize

### Testing Links
Before adding to JSON, test the OneDrive link:
1. Click the link in browser
2. Should open OneDrive folder with photos
3. If it asks for sign-in, check permissions (must be "Anyone with link")

---

## Troubleshooting

### Link requires sign-in to view
**Fix:** Check sharing permissions
1. Right-click folder in OneDrive → Share
2. Change to "Anyone with the link can view"
3. Get new link

### School not appearing in gallery
- Check JSON syntax (commas, quotes, brackets)
- Use https://jsonlint.com/ to validate JSON
- Check file saved and pushed to GitHub

### Table looks wrong on mobile
- Table automatically scrolls horizontally on mobile
- This is normal and expected
- Students can swipe left/right to see all columns

### Date showing incorrectly
- Check format is `YYYY-MM-DD`
- Month is 01-12 (not 1-12)
- Example: `2025-10-05` not `2025-10-5`

---

## Daily Checklist

After visiting schools:
- [ ] Upload photos to OneDrive (one folder per school)
- [ ] Set folders to "Anyone with link can view"
- [ ] Get share links for each folder
- [ ] Add entries to `schools-gallery.json`
- [ ] Double-check district names match exactly
- [ ] Verify date format (`YYYY-MM-DD`)
- [ ] Add commas between entries
- [ ] Test JSON is valid (jsonlint.com)
- [ ] Commit with message: `"Add galleries for School A, School B - Oct 25"`
- [ ] Push to GitHub
- [ ] Verify gallery page updates (wait 1-2 minutes)

---

## Advantages of This Approach

✅ **Super Simple** - No embed codes, just share links
✅ **Fast Updates** - 2 minutes per school
✅ **Clean Display** - Table view, easy to scan
✅ **Mobile Friendly** - Scrollable on small screens
✅ **No Filters Needed** - Can see all schools at once
✅ **Future-Proof** - Easy to add search later if needed

---

## What Students See

1. Go to Gallery page
2. See table with all schools (newest first)
3. Find their school (scroll through table)
4. Click "View Photos" button
5. Opens OneDrive folder in new tab
6. Can view, zoom, download photos

**Simple and effective!**

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
