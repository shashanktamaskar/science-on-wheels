# Automated Data Update Workflow

## Overview
The `update_data_automated.py` script provides a **complete end-to-end automation** for daily school visit updates, including:
- ✅ Coordinate extraction from shortened Google Maps links
- ✅ Distance calculation
- ✅ AI-powered collage generation with retry logic
- ✅ Automatic updates to `data.json` and `schools-gallery.json`

## Quick Start

### Step 1: Download Images from OneDrive
1. Open the OneDrive gallery link in your browser
2. Click the "Download" button (downloads as a zip file)
3. Note the path to the downloaded zip file

### Step 2: Run the Script
```bash
python update_data_automated.py \
  --date "2025-12-03" \
  --school_name "GSSS-EXAMPLE" \
  --school_link "https://maps.app.goo.gl/..." \
  --students 150 \
  --girls 75 \
  --boys 75 \
  --district "Ludhiana" \
  --gallery_link "https://plakshauniversity1-my.sharepoint.com/..." \
  --start_link "https://maps.app.goo.gl/..." \
  --end_link "https://maps.app.goo.gl/..." \
  --images "C:\Users\...\Downloaded_Images.zip" \
  --api_key "YOUR_GEMINI_API_KEY"
```

### Step 3: Review & Commit
```bash
git add .
git commit -m "Update data for GSSS-EXAMPLE"
git push
```

## Using with `data-entry.html`

The data entry tool generates text in this format:
```
**Date:** 2025-12-03
**Schools visited:**

GSSS-EXAMPLE - Map Link: https://maps.app.goo.gl/... - Students: 150 - Girls: 75 - Boys: 75 - District: Ludhiana

**Start Point:** Location - Map Link: https://maps.app.goo.gl/...
**End Point:** Location - Map Link: https://maps.app.goo.gl/...

**Gallery Links:**
GSSS-EXAMPLE: https://onedrive.link...

**Collage Images:**
GSSS-EXAMPLE: GSSS-EXAMPLE.jpg
```

You can easily convert this to the command:
```bash
python update_data_automated.py \
  --date "2025-12-03" \
  --school_name "GSSS-EXAMPLE" \
  --school_link "https://maps.app.goo.gl/..." \
  --students 150 --girls 75 --boys 75 \
  --district "Ludhiana" \
  --gallery_link "https://onedrive.link..." \
  --start_link "https://maps.app.goo.gl/..." \
  --end_link "https://maps.app.goo.gl/..." \
  --images "path/to/images.zip" \
  --api_key "YOUR_KEY"
```

## Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--date` | Yes | Visit date | `2025-12-03` |
| `--school_name` | Yes | School name | `GSSS-KASABAD` |
| `--school_link` | Yes | Google Maps link | `https://maps.app.goo.gl/...` |
| `--students` | Yes | Total students | `150` |
| `--girls` | Yes | Number of girls | `75` |
| `--boys` | Yes | Number of boys | `75` |
| `--district` | Yes | District name | `Ludhiana` |
| `--gallery_link` | Yes | OneDrive gallery URL | `https://onedrive.link...` |
| `--start_link` | Yes | Start point map link | `https://maps.app.goo.gl/...` |
| `--end_link` | Yes | End point map link | `https://maps.app.goo.gl/...` |
| `--images` | Yes | Path to images (zip or folder) | `C:\path\to\images.zip` |
| `--api_key` | Yes | Gemini API key | `AIza...` |
| `--skip_collage` | No | Skip collage generation | (flag, no value) |

## What Happens When You Run It

The script will:

1. **Extract Coordinates** from all map links
   ```
   Extracting coordinates...
   ✅ School Coords: (30.6597498, 76.7451944)
   ```

2. **Calculate Distance** using the Haversine formula
   ```
   ✅ Total Distance: 45 km
   ```

3. **Generate Collage** with AI optimization (up to 3 attempts)
   ```
   ============================================================
   COLLAGE GENERATION WITH AI OPTIMIZATION
   ============================================================
   Found 24 images.
   
   ────────────────────────────────────────────────────────────
   Attempt 1/3
   ────────────────────────────────────────────────────────────
   Selected: ['IMG001.jpg', 'IMG005.jpg', 'IMG012.jpg', 'IMG018.jpg']
   📊 Score: 7.5/10
   💬 AI Feedback: Good composition but could be more engaging...
   ⚠️  Score below target. Retrying...
   
   ────────────────────────────────────────────────────────────
   Attempt 2/3
   ────────────────────────────────────────────────────────────
   Selected: ['IMG003.jpg', 'IMG007.jpg', 'IMG014.jpg', 'IMG020.jpg']
   📊 Score: 9.2/10
   💬 AI Feedback: Excellent visual impact with strong emotional appeal!
   
   🎉 SUCCESS! Achieved target score of 9.0/10
   
   ============================================================
   FINAL RESULT
   ============================================================
   ✅ Best Score: 9.2/10
   📁 Saved to: gallery_school_collage/GSSS-EXAMPLE.jpg
   🎯 Target achieved!
   ```

4. **Update JSON Files**
   ```
   Updating data.json...
   ✅ Updated data.json
   Updating schools-gallery.json...
   ✅ Updated schools-gallery.json
   ```

5. **Complete!**
   ```
   ============================================================
   🎉 ALL DONE! Data updated successfully.
   ============================================================
   ```

## Advanced Usage

### Skip Collage Generation
If you want to update data without generating a new collage:
```bash
python update_data_automated.py ... --skip_collage
```

### Use a Directory Instead of Zip
```bash
--images "C:\path\to\extracted\images\folder"
```

## Troubleshooting

### Issue: "Not enough images (need at least 4)"
**Solution:** Make sure your zip file or directory contains at least 4 image files (.jpg, .jpeg, or .png)

### Issue: "Failed to get school coordinates"
**Solution:** Check that the Google Maps link is valid and accessible

### Issue: "Collage generation failed"
**Solution:** 
- Verify your Gemini API key is correct
- Check that you have internet connection
- Ensure images are valid and not corrupted

## Tips for Best Results

1. **Download images immediately** after the school visit
2. **Use the data-entry.html tool** to format the data correctly
3. **Keep the API key secure** - don't share it or commit it to git
4. **Review the collage** before committing - you can re-run if needed
5. **Test with a small dataset first** before processing real data

## Next Steps

After running the script:
1. Check the generated collage in `gallery_school_collage/`
2. Review the changes in `data.json` and `schools-gallery.json`
3. Verify the website displays correctly (run local server)
4. Commit and push to your git repository
