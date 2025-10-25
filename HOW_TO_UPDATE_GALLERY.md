# How to Update the Photo Gallery

This guide explains how to add photos to the Science on Wheels gallery using OneDrive embed.

## Quick Steps

1. **Upload photos to OneDrive**
   - Go to [OneDrive.com](https://onedrive.live.com)
   - Create a folder called "Science on Wheels Photos" (or any name)
   - Upload all your photos to this folder

2. **Get the embed code**
   - In OneDrive, select your photo folder
   - Click the three dots menu (`...`) or right-click the folder
   - Select **"Embed"** from the menu
   - Copy the `<iframe>` code that appears

3. **Update index.html**
   - Open `index.html` in a text editor
   - Find the Gallery section (search for `"REPLACE THE IFRAME"`)
   - Replace the placeholder iframe with your OneDrive embed code
   - The section looks like this:
   ```html
   <!-- REPLACE THE IFRAME BELOW WITH YOUR ONEDRIVE EMBED CODE -->
   <iframe
       src="about:blank"
       frameborder="0"
       scrolling="no"
       allowfullscreen>
   </iframe>
   ```

4. **Save and deploy**
   - Save the `index.html` file
   - Commit your changes to Git
   - Push to GitHub
   - Your gallery will update automatically!

## Alternative: Using Google Photos

If you prefer Google Photos instead of OneDrive:

1. Upload photos to a Google Photos album
2. Make the album public/shareable
3. Use a Google Photos embed service or create a simple iframe
4. Replace the iframe code in `index.html` the same way

## Tips

- OneDrive automatically creates a beautiful gallery viewer with slideshow features
- Photos update automatically when you add new ones to the OneDrive folder
- You can organize photos in subfolders within your main folder
- Make sure your OneDrive folder sharing is set to "Anyone with the link can view"

## Need Help?

Contact Dr. Rucha Joshi at rucha.joshi@plaksha.edu.in or +91 8358082703
