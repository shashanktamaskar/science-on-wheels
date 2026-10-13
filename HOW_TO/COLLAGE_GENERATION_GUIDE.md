# Collage Generation Guide

Use `generate_collage.py` to make one collage per school from a master folder.

## 1. What To Prepare

Download multi schools folders from [OneDrive](https://plakshauniversity1-my.sharepoint.com/:f:/g/personal/scienceonwheels_plaksha_edu_in/IgBZxdO4AHe1TodsPUfqVni0AYtNPuCQT63H7LFsEpm9k0E). After unzipping, the folder should look like this:

```text
master-folder/
  School One/
    Photos/
      photo1.jpg
      photo2.jpg
  School Two/
    Photos/
      photo1.jpg
      photo2.jpg
```

Supported photo types: `.jpg`, `.jpeg`, `.png`, `.webp`.

## 2. Select images

Run this from the project folder:

```bash
python3 generate_collage.py --mode select --master_dir "/path/to/master-folder" --output_root output-images
```

1. `master_dir` stores the images like demonstrated in `1. What to Prepare` exactly.
2. `output_root` stores the selected images. Use `output-images` unless you have a reason to use another folder.
3. This selects up to 6 images per school and stores them in `output_root`.
4. Review the selected images once. Replace any weak image before making the collage.

### Output Folders

Selected photos are copied to `output-images/`.

```text
output-images/
  School_One/
    selection-manifest.json
    photo1.jpg
    photo2.jpg
```


## 3. Review And Make Collage

If a collage needs different photos:

1. Open that school's folder inside `output-images/`.
2. Add or remove photos there.
3. Build collages with:

```bash
python3 generate_collage.py --mode collage --master_dir output-images
```

This does not reselect photos. It only builds collages from the edited `output-images/` folders.

Final collages are saved in `gallery_collages/`.

```text
gallery_collages/
  School_One.jpg
  School_Two.jpg
```

School folder names are cleaned for file names. For example, `School One` becomes `School_One`.

## Useful Options

`--selected_count 8`:
Choose up to 8 photos per school instead of the default 6.

`--photos_dir_name "photos"`:
Use this if the photo folder is named `photos` instead of `Photos`.

`--clear_selected_dir`:
Remove old photos from each school's `output-images/` folder before copying the new selection. Use this when rerunning selection for the same schools.

`--output_root "my-selected-photos"`:
Change where selected photos are saved. Default: `output-images`.

`--collage_output_dir "my-collages"`:
Change where final collages are saved. Default: `gallery_collages`.

`--seed 123`:
Use the same automatic selection each time.

## Notes

The current script uses automatic selection, not Gemini selection. No API key is needed.

Folders without a `Photos` folder are skipped. Schools with no supported photos are also skipped.

Each selected-photo folder includes `selection-manifest.json`. It records when the folder was created, where the photos came from, and which photos were selected.
