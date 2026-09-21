# Collage Generation Guide

`generate_collage.py` now works in batches from a master directory.

## Expected Folder Layout

For selection or `both` mode, the master directory should contain one folder per school. Each school folder must contain a `Photos/` folder:

```text
master-directory/
  School One/
    Photos/
      image1.jpg
      image2.jpg
  School Two/
    Photos/
      image1.jpg
      image2.jpg
```

Selection output is written to `output-images/`, using the school folder name with spaces replaced by underscores:

```text
output-images/
  School_One/
    selection-manifest.json
    image1.jpg
    image2.jpg
  School_Two/
    selection-manifest.json
    image1.jpg
    image2.jpg
```

Collage output is written to `gallery_collages/`:

```text
gallery_collages/
  School_One.jpg
  School_Two.jpg
```

## Modes

`select`:
Runs Gemini selection for every school under `--master_dir`, reading from each school’s `Photos/` folder and writing selected images to `output-images/<School_Name>/`.

`collage`:
Skips Gemini. Uses `--master_dir` as the selected-image root, normally `output-images/`, and writes final collages to `gallery_collages/`.

`both`:
Runs selection from the original master directory and immediately builds collages from the selected images created in that run.

## Examples

Select images for all schools:

```bash
python3 generate_collage.py \
  --mode select \
  --master_dir "/path/to/master-directory" \
  --api_key "YOUR_GEMINI_API_KEY"
```

Build collages from selected images without API calls:

```bash
python3 generate_collage.py \
  --mode collage \
  --master_dir "output-images"
```

Select and build collages in one command:

```bash
python3 generate_collage.py \
  --mode both \
  --master_dir "/path/to/master-directory" \
  --api_key "YOUR_GEMINI_API_KEY"
```

Use a different photo folder name:

```bash
python3 generate_collage.py \
  --mode select \
  --master_dir "/path/to/master-directory" \
  --photos_dir_name "photos" \
  --api_key "YOUR_GEMINI_API_KEY"
```

## Command Options

`--mode`:
Choose `select`, `collage`, or `both`. Default is `both`.

`--master_dir`:
Required. In `select` and `both`, this is the original school master folder. In `collage`, this should usually be `output-images`.

`--photos_dir_name`:
Name of the image folder inside each school folder. Default is `Photos`.

`--output_root`:
Where selected images are written. Default is `output-images`.

`--collage_output_dir`:
Where finished collages are written. Default is `gallery_collages`.

`--api_key`:
Google AI Studio / Gemini API key. Required for `select` and `both`. Not needed for `collage`.

`--model`:
Gemini model used for image selection. Default is `gemini-2.5-flash`.

`--district`:
Optional district context passed to Gemini during selection.

`--date`:
Optional event date context passed to Gemini during selection.

`--selected_count`:
How many images Gemini should choose per school. Default is `6`.

`--max_retries`:
Maximum Gemini selection attempts per school. Default is `3`.

`--target_score`:
Stop retrying once Gemini returns this score or higher. Default is `9.0`.

`--page_size`:
How many thumbnails are packed into each Gemini contact-sheet page. Default is `12`.

`--seed`:
Base random seed for repeatable selection attempts.

`--clear_selected_dir`:
Before copying a new selection, remove existing image files from each `output-images/<School_Name>/` folder.

## Manual Edit Workflow

1. Run `select` on the original master directory.
2. Open the relevant folder under `output-images/`.
3. Add or remove images manually.
4. Run `collage` with `--master_dir output-images`.

This rebuilds the collages from the edited selected-image folders without another Gemini call.
