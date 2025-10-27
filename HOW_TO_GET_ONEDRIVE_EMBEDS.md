# How to Get OneDrive Embed Codes for Photo Gallery

This guide explains step-by-step how to get OneDrive embed codes for school photo galleries.

---

## Prerequisites

- Microsoft OneDrive account (free with any Microsoft account)
- Photos already taken from school visits
- Access to onedrive.live.com

---

## Step 1: Upload Photos to OneDrive

### A. Go to OneDrive
1. Open browser and go to: **https://onedrive.live.com**
2. Log in with your Microsoft account

### B. Create Folder for Each School
1. Click **"+ New"** button (top left)
2. Select **"Folder"**
3. Name it clearly, for example:
   - `PMShri_Mohali_SASNagar_Oct25`
   - `School_Village_District_Date`

### C. Upload Photos
1. Open the folder you just created
2. Click **"Upload"** → **"Files"**
3. Select all photos from that school
4. Wait for upload to complete

**Tip:** Keep each school's photos in separate folders for easy management.

---

## Step 2: Get the Embed Code

### Method 1: Using "Embed" Feature (RECOMMENDED)

#### For a Photo Folder:

1. **Go back to main OneDrive view** (click "OneDrive" at top)

2. **Right-click the folder** containing your photos

3. **Select "Embed"** from the menu
   - If you don't see "Embed", see Method 2 below

4. **A dialog box appears** with embed options

5. **Click "Generate"** (if shown)

6. **Copy the embed code**
   - You'll see an `<iframe>` code
   - It looks like:
   ```html
   <iframe src="https://onedrive.live.com/embed?resid=ABC123XYZ..." width="800" height="600" frameborder="0" scrolling="no" allowfullscreen></iframe>
   ```

7. **Copy ONLY the URL part**
   - From the iframe code, copy only: `https://onedrive.live.com/embed?resid=ABC123XYZ...`
   - This is what you'll put in schools-gallery.json

---

### Method 2: Using Share Link (If Embed Not Available)

If you don't see "Embed" option:

1. **Right-click the folder**
2. **Select "Share"**
3. **Click "Anyone with the link can view"** (change permissions)
4. **Copy the share link**
   - It looks like: `https://1drv.ms/f/s!ABC123...` OR
   - `https://onedrive.live.com/view.aspx?resid=...`

5. **Convert to Embed URL:**
   - Replace `/view.aspx` with `/embed`
   - OR replace `1drv.ms/f/s!` with `onedrive.live.com/embed?resid=`

   Example:
   - **Share URL:** `https://onedrive.live.com/view.aspx?resid=ABC123&id=456`
   - **Embed URL:** `https://onedrive.live.com/embed?resid=ABC123&id=456`

---

### Method 3: Using "Embed" Menu (Alternative)

1. **Click the folder** (single click to select it)

2. **Look for three dots (...)** at the top or right side

3. **Click the three dots menu**

4. **Select "Embed"**

5. **Copy the iframe code** and extract the URL

---

## Step 3: Test Your Embed URL

**Before adding to JSON, test it works:**

1. Copy your embed URL
2. Open a new browser tab
3. Paste the URL in the address bar
4. Press Enter
5. **You should see:** OneDrive photo gallery viewer with your photos

**If it doesn't work:**
- Check the folder is set to "Anyone with link can view"
- Try Method 2 (convert share link to embed)
- See troubleshooting below

---

## Step 4: Add to schools-gallery.json

Once you have the working embed URL:

```json
{
  "name": "PM Shri Senior Secondary School",
  "district": "SAS Nagar",
  "village": "Mohali",
  "visitDate": "2025-10-26",
  "embedUrl": "https://onedrive.live.com/embed?resid=ABC123XYZ..."
}
```

**Important:**
- Use the full URL starting with `https://`
- Keep the `resid=` parameter
- Don't include `<iframe>` tags in JSON (just the URL)

---

## Complete Example Workflow

### Real Example:

1. **Upload:** 25 photos from "PM Shri School Mohali" to folder `Mohali_SASNagar_Oct26`

2. **Get Embed:**
   - Right-click folder → Embed
   - Get: `<iframe src="https://onedrive.live.com/embed?resid=F123ABC456XYZ!789&authkey=!AaBbCc..." width="800" height="600"></iframe>`

3. **Extract URL:**
   - `https://onedrive.live.com/embed?resid=F123ABC456XYZ!789&authkey=!AaBbCc...`

4. **Add to JSON:**
```json
{
  "schools": [
    {
      "name": "PM Shri Senior Secondary School",
      "district": "SAS Nagar",
      "village": "Mohali",
      "visitDate": "2025-10-26",
      "embedUrl": "https://onedrive.live.com/embed?resid=F123ABC456XYZ!789&authkey=!AaBbCc..."
    }
  ]
}
```

5. **Save, commit, push** → Done!

---

## Sharing Permissions (IMPORTANT)

**Your OneDrive folder MUST be publicly viewable:**

1. Right-click folder
2. Select "Share"
3. Click the link settings (or "Anyone with link...")
4. Select: **"Anyone with the link can view"**
5. **DO NOT** select "Specific people" or "Organization only"

**Why:** Students need to view without logging in to Microsoft.

---

## Troubleshooting

### Problem: "Embed" option not showing

**Solution 1: Use Share Link**
- Get share link → Convert to embed URL (see Method 2)

**Solution 2: Check File Type**
- Embed works for photo folders
- Make sure you're right-clicking the folder, not individual files

**Solution 3: Use OneDrive Web**
- Make sure you're on onedrive.live.com (not OneDrive desktop app)

---

### Problem: Embed shows "Access Denied" or "Sign In Required"

**Solution:** Fix permissions
1. Right-click folder → Share
2. Change to "Anyone with link can view"
3. Get new embed code

---

### Problem: Embed URL doesn't work when tested

**Check URL format:**
- ✅ Good: `https://onedrive.live.com/embed?resid=ABC...`
- ❌ Bad: `https://1drv.ms/f/s!ABC...` (share link, not embed)
- ❌ Bad: `https://onedrive.live.com/view.aspx?...` (view link, not embed)

**Solution:** Convert to embed format (change `/view.aspx` to `/embed`)

---

### Problem: Only shows first few photos

**Solution:** This is normal
- OneDrive embed shows photos in a scrollable gallery
- Students can scroll through all photos
- All photos are accessible

---

### Problem: Photos don't load on school computers

**Possible causes:**
1. School firewall blocking OneDrive
2. Slow internet connection
3. OneDrive folder not set to public

**Solutions:**
- Check folder permissions
- Test on different network
- Consider alternative (Google Photos) if OneDrive consistently blocked

---

## Alternative: Google Photos

If OneDrive doesn't work well (firewall, access issues):

### Using Google Photos:

1. **Upload to Google Photos**
   - Go to photos.google.com
   - Create album for each school
   - Upload photos

2. **Share Album**
   - Open album → Share button
   - Turn on "Link sharing"
   - Copy link

3. **Use in JSON**
```json
{
  "embedUrl": "https://photos.app.goo.gl/ABC123..."
}
```

**Note:** Google Photos links show a gallery page (not iframe embed), but still work.

---

## Quick Reference Card

### Daily Workflow Checklist:

**After visiting schools:**

- [ ] Upload photos to OneDrive folder (one per school)
- [ ] Right-click folder → Share → "Anyone can view"
- [ ] Right-click folder → Embed → Copy code
- [ ] Extract URL from iframe (starts with https://onedrive.live.com/embed)
- [ ] Test URL in browser (should show gallery)
- [ ] Add entry to schools-gallery.json with embedUrl
- [ ] Commit and push to GitHub
- [ ] Verify gallery page updates (wait 1-2 minutes)

---

## Video Tutorial (Coming Soon)

We'll create a video walkthrough showing:
- Uploading photos to OneDrive
- Getting embed code
- Testing the URL
- Adding to JSON

---

## Common URL Formats

### OneDrive Embed URL (CORRECT):
```
https://onedrive.live.com/embed?resid=ABC123XYZ!456&authkey=!AaBbCcDd
```

### OneDrive Share URL (needs conversion):
```
https://1drv.ms/f/s!ABC123XYZ456
```
Convert to: `https://onedrive.live.com/embed?resid=ABC123XYZ456`

### OneDrive View URL (needs conversion):
```
https://onedrive.live.com/view.aspx?resid=ABC...
```
Convert to: `https://onedrive.live.com/embed?resid=ABC...`

---

## Tips for Success

1. **Consistent Naming**
   - Use same format for all folders: `SchoolName_Village_District_Date`
   - Easier to find later

2. **Test First**
   - Always test embed URL before adding to JSON
   - Open in browser, verify photos load

3. **Organize Well**
   - Create main folder: "Science on Wheels Photos"
   - Subfolders for each school
   - Easy to manage 250 schools

4. **Backup**
   - Keep original photos backed up locally
   - OneDrive is convenient, not the only copy

5. **Photo Quality**
   - Upload full resolution
   - OneDrive handles optimization automatically
   - Students can zoom in

---

## Need Help?

**Can't get embed working?**
Contact: rucha.joshi@plaksha.edu.in or shashank.tamaskar@plaksha.edu.in

**Technical Issues?**
- Check HOW_TO_UPDATE_GALLERY.md for JSON format
- Verify folder permissions
- Try alternative browser

---

**Last Updated:** October 2025
**Maintained by:** Plaksha University Science on Wheels Team
