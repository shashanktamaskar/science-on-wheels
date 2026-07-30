Perfect! Let me clarify this for you:

## Gallery Link Field

**What to enter**: OneDrive **FOLDER** link (not a zip file)

**Example**: 
```
https://plakshauniversity1-my.sharepoint.com/:f:/g/personal/scienceonwheels_plaksha_edu_in/IgBMabPvuTnVT5muBgE-kNV-AfYENxV9Xu1iE4maW5DcKWc?e=jYE5wj
```

## Two Different Links You'll Use

| Purpose | Type | Where | Example |
|---------|------|-------|---------|
| **Gallery Link** (in data-entry form) | OneDrive folder URL | Goes into `schools-gallery.json` for website display | `https://...sharepoint.com/:f:/...` |
| **Images** (for command line script) | PATH to downloaded ZIP file | For collage generation | `C:\Downloads\School_Photos.zip` |

## Workflow Summary

1. **In data-entry.html**: Paste the OneDrive FOLDER link
2. **Download separately**: Visit that same link, click "Download" to get the ZIP
3. **In command line**: Point the script to the downloaded ZIP file path

The folder link displays the gallery on your website.  
The zip file is used locally to generate the collage.

I've already removed the redundant "Collage Filename" field, so you're all set! The filename will be auto-generated from the school name (e.g., `GSSS-KASABAD.jpg`).
