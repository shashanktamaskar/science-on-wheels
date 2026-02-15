# Updated Generate Collage Script - Features

## What's New ✨

The `generate_collage.py` script now includes **intelligent retry logic** to achieve higher virality scores, matching the behavior of the original AI-Collage-Generator tool.

## Key Features

### 1. **Retry Logic (Up to 3 Attempts)**
- The script will try up to 3 times to create a collage with a high impact score
- Each attempt selects a different combination of the "best" 4 photos
- Keeps only the highest-scoring collage

### 2. **Target Score System**
- Default target: **9.0/10**
- If achieved, stops retrying early
- Customizable via command-line arguments

### 3. **Smart Behavior**
- If you have exactly 4 images: Uses all of them (no retries)
- If you have more than 4 images: Tries multiple combinations to find the best

## Usage

### Basic Usage (Default Settings)
```bash
python generate_collage.py \
  --input_dir "path/to/images" \
  --output "path/to/output.jpg" \
  --api_key "YOUR_API_KEY"
```

### Custom Settings
```bash
python generate_collage.py \
  --input_dir "path/to/images" \
  --output "path/to/output.jpg" \
  --api_key "YOUR_API_KEY" \
  --max_retries 5 \
  --target_score 8.5
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--input_dir` | Required | Directory containing source images |
| `--output` | Required | Path to save the final collage |
| `--api_key` | Required | Gemini API key |
| `--max_retries` | 3 | Maximum number of attempts |
| `--target_score` | 9.0 | Stop if this score is achieved |

## Example Output

```
Found 24 images.

=== Attempt 1/3 ===
Selecting best 4 photos...
Selected: ['IMG001.jpg', 'IMG005.jpg', 'IMG012.jpg', 'IMG018.jpg']
Creating collage...
Rating collage...
AI Rating: Impact Score: 6.5/10. Good composition but lacks visual impact.
Score: 6.5/10
Score was 6.5/10. Retrying to improve...

=== Attempt 2/3 ===
Selecting best 4 photos...
Selected: ['IMG003.jpg', 'IMG007.jpg', 'IMG014.jpg', 'IMG020.jpg']
Creating collage...
Rating collage...
AI Rating: Impact Score: 9.2/10. Excellent composition with strong emotional appeal!
Score: 9.2/10

✅ SUCCESS! Achieved target score of 9.0/10

=== FINAL RESULT ===
Best Score: 9.2/10
Best Rating: Impact Score: 9.2/10. Excellent composition with strong emotional appeal!
Collage saved to: path/to/output.jpg
Target achieved in attempt 2!
```

## Next Steps

Now you can re-run the collage generation for GSSS-KASABAD to get a better score!
