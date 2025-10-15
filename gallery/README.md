# Gallery Folder

This folder contains photos from Science on Wheels school visits.

## How to Add Photos

1. **Copy photos to this folder**
   ```
   gallery/
   ├── ludhiana_school1.jpg
   ├── ludhiana_robotics_workshop.jpg
   ├── patiala_water_testing.jpg
   └── ...
   ```

2. **Update data.json** with the filenames:
   ```json
   "gallery": [
     {
       "district": "Ludhiana",
       "images": [
         "ludhiana_school1.jpg",
         "ludhiana_robotics_workshop.jpg"
       ]
     }
   ]
   ```

3. **Commit and push:**
   ```bash
   git add gallery/
   git commit -m "Add photos from Ludhiana visit"
   git push
   ```

## Photo Naming Convention

Use descriptive, lowercase names with underscores:
- ✅ `ludhiana_robotics_workshop.jpg`
- ✅ `patiala_students_group_photo.jpg`
- ❌ `IMG_1234.jpg`
- ❌ `Photo 1.JPG`

## Photo Guidelines

- Format: JPG or PNG
- Size: Under 2MB (compress if needed)
- Content: Students learning, workshops, activities, van in action
- Privacy: Get verbal permission before photographing students

## Organizing by District

Group photos by district for easy organization:
```
ludhiana_school1.jpg
ludhiana_school2.jpg
ludhiana_robotics.jpg
patiala_water_test.jpg
patiala_students.jpg
```

For detailed instructions, see `HOW_TO_UPDATE_DASHBOARD.md`.
