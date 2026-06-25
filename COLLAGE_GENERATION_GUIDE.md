# Collage Generation Guide

This repo now has a local `generate_collage.py` script that does two separate jobs:

1. Select the most representative images from a raw photo folder using Gemini.
2. Build a tighter collage from any images already inside a folder, with no API call.

That split is deliberate:
- Use Gemini once to pick a good base set.
- Copy those selected images into a reusable folder inside `output-images/`.
- Add or remove extra images manually in that folder.
- Rebuild the collage as many times as needed without calling Gemini again.

## Output Structure

The script writes files under `output-images/` by default:

```text
output-images/
  <run-name>/
    selected-images/
      selection-manifest.json
      <selected image files>
    collage/
      <run-name>.jpg
```

You can change the root folder with `--output_root`, or point the script at a different selected-image folder with `--selected_dir`.

## Modes

### `both`
Default mode.

- Runs Gemini selection on the source folder.
- Copies the selected images into `selected-images/`.
- Builds the final collage from that folder immediately.

### `select`

- Runs Gemini selection only.
- Copies the chosen images into `selected-images/`.
- Does not build the collage.

Use this when you want to prepare a reusable image set first, then add extra images by hand later.

### `collage`

- Skips Gemini completely.
- Builds a collage from the images already inside `--collage_input_dir`.

Use this after you manually add extra images into the selected-image folder and want a fresh collage without another API call.

## Command Examples

### 1. Select and build in one step

```bash
python3 generate_collage.py \
  --mode both \
  --input_dir "/path/to/downloads/folder" \
  --school_name "GSSS-KASABAD" \
  --district "Ludhiana" \
  --date "2026-06-25" \
  --api_key "YOUR_GEMINI_API_KEY"
```

### 2. Select only, then edit the folder manually

```bash
python3 generate_collage.py \
  --mode select \
  --input_dir "/path/to/downloads/folder" \
  --school_name "GSSS-KASABAD" \
  --api_key "YOUR_GEMINI_API_KEY"
```

After this runs, open:

```text
output-images/GSSS-KASABAD/selected-images/
```

Add any extra images you want to include, then run collage mode.

### 3. Rebuild collage without Gemini

```bash
python3 generate_collage.py \
  --mode collage \
  --collage_input_dir "output-images/GSSS-KASABAD/selected-images" \
  --output "output-images/GSSS-KASABAD/collage/GSSS-KASABAD.jpg"
```

This uses every supported image inside the folder you point to. No API key is needed for collage-only mode.

## Command Options

### `--mode`
Controls what the script does.

- `select`: choose images only
- `collage`: build collage only
- `both`: do both in one run

### `--input_dir`
Source folder containing the raw event images.

Required for `select` and `both`.

The script searches this folder recursively and accepts:
- `.jpg`
- `.jpeg`
- `.png`
- `.webp`

### `--collage_input_dir`
Folder to use when building the final collage.

If omitted:
- `both` uses the generated `selected-images` folder
- `collage` also defaults to the selected-images folder under `output-images/`

Use this when you want to rebuild a collage from a folder you edited manually.

### `--output`
Final collage file path.

If you do not pass this, the script saves the collage to:

```text
output-images/<run-name>/collage/<run-name>.jpg
```

### `--output_root`
Base directory for generated output.

Default:

```text
output-images
```

This is where the run folder, selected images folder, and collage folder are created.

### `--selected_dir`
Custom folder where the selected images are copied.

By default, the script uses:

```text
output-images/<run-name>/selected-images
```

Override this if you want to keep multiple curated sets in different places.

### `--api_key`
Google AI Studio / Gemini API key.

Required for:
- `select`
- `both`

Not needed for:
- `collage`

You can also set the environment variable `GEMINI_API_KEY` instead of passing this flag.

### `--model`
Gemini model used for the selection step.

Default:

```text
gemini-2.5-flash
```

You can override this if you want to test a different model.

### `--school_name`
Optional label used for naming the output folders and files.

If omitted, the script falls back to the source folder name.

### `--district`
Optional context passed into Gemini so selection is better aligned with the event.

### `--date`
Optional event date passed into Gemini.

Use ISO format:

```text
2026-06-25
```

### `--selected_count`
How many images Gemini should choose for the base set.

Default:

```text
6
```

If the source folder has fewer images than this, the script uses what is available.

### `--max_retries`
How many Gemini selection attempts to try.

Default:

```text
3
```

The script keeps the best-scoring attempt and stops early if the target score is reached.

### `--target_score`
Target selection score.

Default:

```text
9.0
```

If Gemini returns a score at or above this value, the script stops retrying.

### `--page_size`
How many thumbnails are packed into each Gemini contact-sheet page.

Default:

```text
12
```

This is only used during the selection step.

### `--seed`
Base random seed for the selection retries.

Use this if you want repeatable selection attempts from the same source set.

### `--clear_selected_dir`
Clears existing supported image files from the selected-images folder before copying the newly selected set.

Use this when you want the selected folder to contain only the latest Gemini selection.

## What Changed in the Collage Output

The final collage now:
- does **not** print file names on the image tiles
- uses much tighter spacing between images
- crops images more aggressively so the collage feels less padded and more focused

That makes the collage read as a visual summary instead of a labeled contact sheet.

## Manifest File

Every selection run writes a small manifest:

```text
output-images/<run-name>/selected-images/selection-manifest.json
```

This records:
- the mode used
- source folder
- collage input folder
- selected image names
- Gemini score and reason, if selection was used

## Suggested Workflow

1. Run `--mode select` or `--mode both` on the raw downloads folder.
2. Open the generated `selected-images/` folder.
3. Add any extra images you want to include.
4. Run `--mode collage` pointing at that same folder.
5. Repeat step 4 any time you want a new collage without another API call.

## Practical Notes

- Keep the source photos in a normal folder, preferably with 10+ images if you want Gemini to make a better representative selection.
- If you manually add images to the selected-images folder, they will be included the next time you run collage mode.
- For the website, keep the collage output filename aligned with the school name convention used in the repo.
