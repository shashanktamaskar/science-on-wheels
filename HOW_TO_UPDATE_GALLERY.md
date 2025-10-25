# How to Update the Photo Gallery

This guide will help you embed your OneDrive photo gallery into the Science on Wheels website.

## Overview

The gallery page uses OneDrive's embed feature to display photos. This approach:
- ✅ Keeps your GitHub repository lightweight (no large image files)
- ✅ Provides a beautiful, built-in photo viewer with slideshow and zoom
- ✅ Auto-updates when you add new photos to OneDrive
- ✅ Handles image optimization automatically

## Step-by-Step Instructions

### 1. Upload Photos to OneDrive

1. Log in to your OneDrive account at [onedrive.live.com](https://onedrive.live.com)
2. Create a new folder called "Science on Wheels Gallery" (or any name you prefer)
3. Upload all your Science on Wheels photos to this folder
4. Optionally, organize photos into subfolders by district or event

**Tips:**
- Use descriptive filenames like `sasnagar_robotics_workshop.jpg`
- Recommended image format: JPG or PNG
- OneDrive handles image optimization automatically

### 2. Get the OneDrive Embed Code

#### Option A: Using the Web Interface
1. In OneDrive, navigate to your photo folder
2. Click the **"..."** (three dots) menu at the top
3. Select **"Embed"**
4. A dialog will appear with an `<iframe>` code
5. Click **"Generate"** if needed, then **"Copy"** the embed code

#### Option B: Using Share Menu
1. Right-click on your photo folder
2. Select **"Share"** → **"Embed"**
3. Copy the `<iframe>` code that appears

**The embed code will look like this:**
```html
<iframe src="https://onedrive.live.com/embed?resid=..." width="800" height="600" frameborder="0" scrolling="no" allowfullscreen></iframe>
```

### 3. Update the Website

1. Open the `index.html` file in a text editor
2. Search for the text: `REPLACE THE IFRAME BELOW`
3. You'll find this section around line 649:

```html
<!-- REPLACE THE IFRAME BELOW WITH YOUR ONEDRIVE EMBED CODE -->
<iframe
    src="about:blank"
    frameborder="0"
    scrolling="no"
    allowfullscreen>
</iframe>
```

4. Replace the entire `<iframe>...</iframe>` tag with your OneDrive embed code
5. Save the file

**Before:**
```html
<iframe
    src="about:blank"
    frameborder="0"
    scrolling="no"
    allowfullscreen>
</iframe>
```

**After:**
```html
<iframe
    src="https://onedrive.live.com/embed?resid=YOUR_ACTUAL_CODE_HERE"
    width="800"
    height="600"
    frameborder="0"
    scrolling="no"
    allowfullscreen>
</iframe>
```

### 4. Commit and Push Changes

```bash
git add index.html
git commit -m "Update gallery with OneDrive embed"
git push
```

GitHub Pages will automatically rebuild your site (takes 1-2 minutes).

## Updating Photos

**Good news:** Once the embed is set up, you don't need to touch the code again!

To add new photos:
1. Upload new photos to your OneDrive folder
2. The gallery updates automatically - no code changes needed!

## Troubleshooting

### Gallery shows "Gallery Coming Soon!" message
- The placeholder `<iframe src="about:blank">` is still in place
- Follow Step 3 above to replace it with your OneDrive embed code

### Gallery doesn't display or shows an error
- Check that you copied the complete `<iframe>` code from OneDrive
- Ensure the OneDrive folder is set to "Anyone with the link can view"
- Try refreshing the page with Ctrl+F5 (hard refresh)

### Gallery is too small/large
- You can adjust the `width` and `height` attributes in the iframe code
- The CSS will keep it responsive on mobile devices

### Photos aren't updating
- Check that you uploaded to the correct OneDrive folder
- OneDrive may take a few minutes to sync
- Try refreshing your browser cache (Ctrl+F5)

## Alternative: Google Photos

If you prefer Google Photos instead of OneDrive:

1. Upload photos to Google Photos
2. Create an album
3. Get the embed code (Share → Create Link → More Options → Embed)
4. Replace the iframe the same way as with OneDrive

## Questions?

For technical assistance with the gallery, contact:
- **Dr. Rucha Joshi**: rucha.joshi@plaksha.edu.in
- **Dr. Shashank Tamaskar**: shashank.tamaskar@plaksha.edu.in

---

**Last Updated:** October 2025
**Maintained by:** Plaksha University Science on Wheels Team
