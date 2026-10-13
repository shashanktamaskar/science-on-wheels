# Adding Schools

Use this when new school visits need to be added to `data-sow.json` through `admin.html`.

## Fields Needed

Each school entry should match this shape:

```json
{
  "state": "Punjab",
  "district": "Patiala",
  "visitDate": "2026-09-16",
  "school_name": "Saheed Sandeep sing S. S. S. school mangewal",
  "mediaLink": "OneDrive folder link",
  "imageName": "Collage_File.jpg",
  "girlsCount": 48,
  "boysCount": 42,
  "coordinates": {
    "lat": 30.474393204479366,
    "lng": 76.20123731534473
  },
  "locationLink": "Google Maps link"
}
```

Collect these values before opening `admin.html`:

- `state`
- `district`
- `visitDate`
- `school_name`
- `mediaLink`
- `imageName`
- `girlsCount`
- `boysCount`
- `coordinates.lat`
- `coordinates.lng`
- `locationLink`

Use this sheet for school visit details:

```text
https://docs.google.com/spreadsheets/d/1gkP96ZeWccTXhooUJ2AKTAKQZlgDhw8c1OFpoyBoBSE/edit?gid=0#gid=0
```

Do not use the photo link from the sheet. Those links may only work for Plaksha members. Create a fresh OneDrive sharing link for `mediaLink`.

## OneDrive Link

For each school photo folder:

1. Open the folder in OneDrive.
2. Click `Share`.
3. In `The link works for:`, select `Anyone`.
4. Set permission to `Can view` only.
5. Copy the link.
6. Test it in a private/incognito browser window.

Use this tested link as `mediaLink`.

## Coordinates

Add latitude and longitude, not only the map link.

1. Open the school in Google Maps.
2. Right-click the exact school location.
3. Click the coordinate pair, for example `30.474393, 76.201237`.
4. Put the first number in `coordinates.lat`.
5. Put the second number in `coordinates.lng`.
6. Put the Google Maps link in `locationLink`.

`admin.html` can auto-fill coordinates from many Google Maps links, but still check both fields before publishing.

## Add In Admin

1. Open `admin.html`.
2. Pick `visitDate` and `state`.
3. Add one school card per school.
4. Fill `school_name`, `locationLink`, `coordinates.lat`, `coordinates.lng`, `district`, `girlsCount`, `boysCount`, `mediaLink`, and `imageName`.
5. Click `Calculate & preview update`.
6. Check the preview JSON.
7. Publish from the page, or download `data-sow.json` and upload it manually.

## Collage Image

If `imageName` is filled:

1. Put that image file in `gallery_collages/`.
2. Use the exact same filename in `imageName`.
3. Include the extension, for example `.jpg`.

If no collage is ready, leave `imageName` blank.

## Last Check

Before publishing or pushing:

- Date is `YYYY-MM-DD`
- School name is spelled correctly
- District is consistent
- `girlsCount + boysCount` is correct
- `coordinates.lat` and `coordinates.lng` are filled
- `locationLink` opens the right school
- `mediaLink` opens without sign-in
- `mediaLink` is OneDrive `Anyone` + `Can view`
- Sheet photo link was not used
- Collage file exists in `gallery_collages/` if `imageName` is filled

## Git Commands

Check what changed:

```bash
git status
```

Add the changed files:

```bash
git add data-sow.json
git add gallery_collages/NAME_OF_COLLAGE.jpg
```

Commit:

```bash
git commit -m "Add school visits for YYYY-MM-DD"
```

Push:

```bash
git push
```

After pushing, wait a few minutes and open the website to confirm the schools appear.
