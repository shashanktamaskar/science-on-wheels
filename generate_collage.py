#!/usr/bin/env python3
"""
Select representative event photos with Gemini and build a tighter collage.

Workflow:
1. `select` or `both` uses Gemini to choose the most representative images.
2. The selected images are copied into `output-images/<run_name>/selected-images/`.
3. `collage` can later rebuild a collage from any images already inside that
   directory, including extra images you add manually, without any API call.
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import os
import random
import re
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps


API_BASE = "https://generativelanguage.googleapis.com/v1beta"
DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
DEFAULT_TARGET_SCORE = 9.0
DEFAULT_MAX_RETRIES = 3
DEFAULT_OUTPUT_ROOT = "output-images"
DEFAULT_SELECTED_DIRNAME = "selected-images"
DEFAULT_COLLAGE_DIRNAME = "collage"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"}


@dataclass
class SelectionResult:
    selected_paths: list[Path]
    score: float
    reason: str
    raw_text: str
    attempt: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Select representative event photos with Gemini and build a collage."
    )
    parser.add_argument(
        "--mode",
        choices=("select", "collage", "both"),
        default="both",
        help="select = choose images only, collage = build from existing images only, both = do both (default).",
    )
    parser.add_argument(
        "--input_dir",
        help="Folder containing source images for Gemini selection. Required for select/both.",
    )
    parser.add_argument(
        "--collage_input_dir",
        help="Folder containing images to collage. Defaults to the selected-images folder inside output-images.",
    )
    parser.add_argument(
        "--output",
        help="Final collage file path. Defaults to output-images/<run_name>/collage/<run_name>.jpg",
    )
    parser.add_argument(
        "--output_root",
        default=DEFAULT_OUTPUT_ROOT,
        help=f"Root directory used for generated folders (default: {DEFAULT_OUTPUT_ROOT}).",
    )
    parser.add_argument(
        "--selected_dir",
        help="Directory where selected images are copied. Defaults to output_root/<run_name>/selected-images.",
    )
    parser.add_argument(
        "--api_key",
        default=os.environ.get("GEMINI_API_KEY"),
        help="Google AI Studio / Gemini API key. Required for select/both.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gemini model to use for image selection (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument("--school_name", help="Optional school name used for folder/file naming.")
    parser.add_argument("--district", help="Optional district used in the Gemini prompt.")
    parser.add_argument("--date", help="Optional event date used in the Gemini prompt.")
    parser.add_argument(
        "--selected_count",
        type=int,
        default=6,
        help="How many images Gemini should pick for the collage (default: 6).",
    )
    parser.add_argument(
        "--max_retries",
        type=int,
        default=DEFAULT_MAX_RETRIES,
        help=f"Maximum Gemini attempts when selecting images (default: {DEFAULT_MAX_RETRIES}).",
    )
    parser.add_argument(
        "--target_score",
        type=float,
        default=DEFAULT_TARGET_SCORE,
        help=f"Stop retrying once Gemini returns at least this score (default: {DEFAULT_TARGET_SCORE}).",
    )
    parser.add_argument(
        "--page_size",
        type=int,
        default=12,
        help="How many thumbnails to show per Gemini contact-sheet page (default: 12).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Base random seed used for selection retries.",
    )
    parser.add_argument(
        "--clear_selected_dir",
        action="store_true",
        help="Remove supported image files from the selected-images folder before copying the new selection.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    value = re.sub(r"[^\w.-]+", "-", value.strip())
    value = re.sub(r"-{2,}", "-", value).strip("-._")
    return value or "collage-run"


def collect_images(folder: Path) -> list[Path]:
    images: list[Path] = []
    for path in sorted(folder.rglob("*")):
        if path.is_file() and path.suffix in SUPPORTED_EXTENSIONS:
            images.append(path)
    return images


def open_image(path: Path) -> Image.Image:
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    if img.mode == "RGBA":
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    return img


def load_font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def build_contact_sheet(
    image_paths: Sequence[Path],
    output_path: Path,
    *,
    columns: int,
    thumb_size: tuple[int, int],
    labels: Sequence[str],
) -> None:
    pad = 6
    tile_w, tile_h = thumb_size
    rows = math.ceil(len(image_paths) / columns)
    width = pad + columns * (tile_w + pad)
    height = pad + rows * (tile_h + pad)

    sheet = Image.new("RGB", (width, height), (18, 18, 18))
    draw = ImageDraw.Draw(sheet)
    font = load_font(18)

    for idx, path in enumerate(image_paths):
        col = idx % columns
        row = idx // columns
        x = pad + col * (tile_w + pad)
        y = pad + row * (tile_h + pad)

        try:
            img = ImageOps.fit(open_image(path), thumb_size, method=Image.Resampling.LANCZOS)
        except Exception:
            continue

        sheet.paste(img, (x, y))
        draw.rectangle((x, y, x + tile_w, y + tile_h), outline=(255, 255, 255), width=2)
        draw.rectangle((x + 8, y + 8, x + 50, y + 36), fill=(15, 23, 42))
        draw.text((x + 20, y + 11), labels[idx], fill=(255, 255, 255), font=font)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)


def choose_grid(count: int) -> tuple[int, int]:
    if count <= 1:
        return 1, 1
    if count == 2:
        return 2, 1
    if count in (3, 4):
        return 2, 2
    if count in (5, 6):
        return 3, 2
    if count in (7, 8, 9):
        return 3, 3
    cols = min(4, max(3, math.ceil(math.sqrt(count))))
    rows = math.ceil(count / cols)
    return cols, rows


def encode_file(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def extract_text_from_response(response_json: dict) -> str:
    parts: list[str] = []
    candidates = response_json.get("candidates") or []
    for candidate in candidates:
        content = candidate.get("content") or {}
        for part in content.get("parts") or []:
            text = part.get("text")
            if text:
                parts.append(text)
    if parts:
        return "\n".join(parts).strip()

    # Fallback for unexpected response shapes.
    for key in ("text", "output_text", "output"):
        value = response_json.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def extract_json(text: str) -> dict:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.S)
        if match:
            return json.loads(match.group(0))
        raise


def parse_score(value) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        match = re.search(r"(\d+(?:\.\d+)?)", value)
        if match:
            return float(match.group(1))
    return 0.0


def prompt_variants() -> list[str]:
    return [
        "Prioritize variety, story coverage, and audience engagement. Avoid duplicates.",
        "Choose images that summarize the full event from start to finish.",
        "Prefer a balanced narrative: setup, activity, reactions, group moments, and closing.",
    ]


def send_gemini_selection_request(
    *,
    api_key: str,
    model: str,
    prompt: str,
    images: Sequence[Path],
) -> dict:
    parts = [{"text": prompt}]
    for path in images:
        mime_type = "image/png"
        suffix = path.suffix.lower()
        if suffix in {".jpg", ".jpeg"}:
            mime_type = "image/jpeg"
        elif suffix == ".webp":
            mime_type = "image/webp"
        parts.append(
            {
                "inline_data": {
                    "mime_type": mime_type,
                    "data": encode_file(path),
                }
            }
        )

    payload = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.95,
            "maxOutputTokens": 512,
            "responseMimeType": "application/json",
        },
    }

    url = f"{API_BASE}/models/{model}:generateContent?key={api_key}"
    response = requests.post(url, json=payload, timeout=180)
    response.raise_for_status()
    return response.json()


def run_selection_round(
    *,
    api_key: str,
    model: str,
    image_paths: Sequence[Path],
    selected_count: int,
    seed: int,
    school_name: str | None,
    district: str | None,
    date: str | None,
    attempt: int,
    page_size: int,
) -> SelectionResult:
    rng = random.Random(seed)
    shuffled = list(image_paths)
    rng.shuffle(shuffled)

    event_bits = [part for part in [school_name, district, date] if part]
    event_context = ", ".join(event_bits) if event_bits else "an event photo set"
    numbered_list = "\n".join(f"{idx + 1}. {path.name}" for idx, path in enumerate(shuffled))
    prompt = f"""
You are selecting images for a collage from {event_context}.

Goal:
- Pick up to {selected_count} images that best represent the full event.
- Favor story coverage and variety over pure sharpness.
- Avoid duplicate or nearly duplicate scenes.
- Include a balance of setup, participation, demonstrations, reactions, and closing/group moments when available.

Return strict JSON only with this shape:
{{
  "selected_indices": [1, 2, 3, 4, 5, 6],
  "score": 9.1,
  "reason": "short explanation"
}}

Rules:
- selected_indices must use the numbered list below.
- Use at most {selected_count} images.
- score must be from 0 to 10 and should reflect how representative the set is, not just image clarity.
- If the event has fewer than {selected_count} useful images, choose the best available ones.

Numbered image list:
{numbered_list}

Attempt {attempt} focus:
{prompt_variants()[attempt - 1]}
""".strip()

    pages = make_pages_for_selection(shuffled, page_size)
    temp_dir = Path(tempfile.mkdtemp(prefix="collage_sheets_"))
    try:
        sheet_paths: list[Path] = []
        for page_index, page in enumerate(pages, start=1):
            sheet_path = temp_dir / f"page_{page_index:02d}.png"
            labels = [str((page_index - 1) * page_size + offset + 1) for offset in range(len(page))]
            build_contact_sheet(
                page,
                sheet_path,
                columns=min(4, max(1, len(page))),
                thumb_size=(240, 160),
                labels=labels,
            )
            sheet_paths.append(sheet_path)

        response_json = send_gemini_selection_request(
            api_key=api_key,
            model=model,
            prompt=prompt,
            images=sheet_paths,
        )
        output_text = extract_text_from_response(response_json)
        parsed = extract_json(output_text)

        selected_indices = parsed.get("selected_indices") or parsed.get("selected") or []
        if not isinstance(selected_indices, list):
            selected_indices = []

        normalized_indices: list[int] = []
        for item in selected_indices:
            try:
                idx = int(item)
            except (TypeError, ValueError):
                continue
            if 1 <= idx <= len(shuffled) and idx not in normalized_indices:
                normalized_indices.append(idx)

        if not normalized_indices:
            normalized_indices = list(range(1, min(selected_count, len(shuffled)) + 1))

        score = parse_score(parsed.get("score"))
        reason = str(parsed.get("reason") or parsed.get("rationale") or "").strip()
        selected_paths = [shuffled[i - 1] for i in normalized_indices[:selected_count]]
        return SelectionResult(
            selected_paths=selected_paths,
            score=score,
            reason=reason,
            raw_text=output_text,
            attempt=attempt,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def make_pages_for_selection(items: Sequence[Path], page_size: int) -> list[list[Path]]:
    return [list(items[i : i + page_size]) for i in range(0, len(items), page_size)]


def fallback_selection(image_paths: Sequence[Path], selected_count: int) -> list[Path]:
    if not image_paths:
        return []
    if len(image_paths) <= selected_count:
        return list(image_paths)

    step = len(image_paths) / selected_count
    indexes = [min(len(image_paths) - 1, round(i * step)) for i in range(selected_count)]
    selected: list[Path] = []
    for idx in indexes:
        item = image_paths[idx]
        if item not in selected:
            selected.append(item)
    for item in image_paths:
        if len(selected) >= selected_count:
            break
        if item not in selected:
            selected.append(item)
    return selected[:selected_count]


def copy_selected_images(selected_paths: Sequence[Path], selected_dir: Path, *, clear_existing: bool) -> None:
    selected_dir.mkdir(parents=True, exist_ok=True)
    if clear_existing:
        for path in selected_dir.iterdir():
            if path.is_file() and path.suffix in SUPPORTED_EXTENSIONS:
                path.unlink()

    for source in selected_paths:
        destination = selected_dir / source.name
        shutil.copy2(source, destination)


def save_manifest(
    *,
    selected_dir: Path,
    source_dir: Path | None,
    collage_input_dir: Path | None,
    selection: SelectionResult | None,
    selected_images: Sequence[Path],
    mode: str,
) -> None:
    manifest = {
        "mode": mode,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "sourceDir": str(source_dir) if source_dir else None,
        "collageInputDir": str(collage_input_dir) if collage_input_dir else None,
        "selectedImages": [path.name for path in selected_images],
        "selectedCount": len(selected_images),
    }
    if selection is not None:
        manifest["selectionScore"] = selection.score
        manifest["selectionReason"] = selection.reason
        manifest["selectionAttempt"] = selection.attempt
    (selected_dir / "selection-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def build_final_collage(image_paths: Sequence[Path], output_path: Path) -> None:
    count = len(image_paths)
    cols, rows = choose_grid(count)
    cell_w, cell_h = 620, 465
    gap = 4

    width = cols * cell_w + (cols + 1) * gap
    height = rows * cell_h + (rows + 1) * gap
    canvas = Image.new("RGB", (width, height), (12, 12, 12))

    for idx, path in enumerate(image_paths):
        row = idx // cols
        col = idx % cols
        x = gap + col * (cell_w + gap)
        y = gap + row * (cell_h + gap)

        try:
            img = ImageOps.fit(open_image(path), (cell_w, cell_h), method=Image.Resampling.LANCZOS)
        except Exception as exc:
            print(f"WARNING: Skipping unreadable image {path.name}: {exc}")
            continue

        canvas.paste(img, (x, y))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    suffix = output_path.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        canvas.save(output_path, quality=92, optimize=True, progressive=True)
    elif suffix == ".png":
        canvas.save(output_path, optimize=True)
    else:
        canvas.save(output_path.with_suffix(".jpg"), quality=92, optimize=True, progressive=True)


def resolve_paths(args: argparse.Namespace, run_name: str) -> tuple[Path, Path, Path]:
    output_root = Path(args.output_root).expanduser()
    selected_dir = Path(args.selected_dir).expanduser() if args.selected_dir else output_root / run_name / DEFAULT_SELECTED_DIRNAME
    collage_dir = output_root / run_name / DEFAULT_COLLAGE_DIRNAME
    if args.output:
        collage_output = Path(args.output).expanduser()
        if not collage_output.suffix:
            collage_output = collage_output.with_suffix(".jpg")
    else:
        collage_output = collage_dir / f"{run_name}.jpg"
    return selected_dir, collage_dir, collage_output


def determine_run_name(args: argparse.Namespace, source_dir: Path | None, collage_input_dir: Path | None) -> str:
    for candidate in (args.school_name, source_dir.name if source_dir else None, collage_input_dir.name if collage_input_dir else None):
        if candidate:
            return slugify(candidate)
    return "collage-run"


def load_images_for_collage(collage_input_dir: Path) -> list[Path]:
    images = collect_images(collage_input_dir)
    if not images:
        raise FileNotFoundError(f"No supported images found in {collage_input_dir}")
    return images


def main() -> int:
    args = parse_args()

    source_dir = Path(args.input_dir).expanduser().resolve() if args.input_dir else None
    collage_input_dir = Path(args.collage_input_dir).expanduser().resolve() if args.collage_input_dir else None

    if args.mode in {"select", "both"} and source_dir is None:
        print("ERROR: --input_dir is required for select/both modes.")
        return 1

    if args.mode in {"select", "both"} and not args.api_key:
        print("ERROR: --api_key or GEMINI_API_KEY is required for select/both modes.")
        return 1

    run_name = determine_run_name(args, source_dir, collage_input_dir)
    selected_dir, collage_dir, default_output_path = resolve_paths(args, run_name)

    selection_result: SelectionResult | None = None
    selected_images: list[Path] = []

    if args.mode in {"select", "both"}:
        assert source_dir is not None
        source_images = collect_images(source_dir)
        if not source_images:
            print(f"ERROR: no supported images found in {source_dir}")
            return 1

        print(f"Found {len(source_images)} source images in {source_dir}")
        print(f"Selected images will be copied to: {selected_dir}")

        attempt_limit = max(1, min(args.max_retries, 3))
        best_result: SelectionResult | None = None
        base_seed = args.seed if args.seed is not None else random.randint(1, 10_000_000)

        for attempt in range(1, attempt_limit + 1):
            print(f"\n=== Selection attempt {attempt}/{attempt_limit} ===")
            try:
                result = run_selection_round(
                    api_key=args.api_key,
                    model=args.model,
                    image_paths=source_images,
                    selected_count=min(args.selected_count, len(source_images)),
                    seed=base_seed + attempt,
                    school_name=args.school_name,
                    district=args.district,
                    date=args.date,
                    attempt=attempt,
                    page_size=max(4, args.page_size),
                )
                print(f"Selected: {[p.name for p in result.selected_paths]}")
                print(f"Score: {result.score}/10")
                if result.reason:
                    print(f"Reason: {result.reason}")

                if best_result is None or result.score > best_result.score:
                    best_result = result

                if result.score >= args.target_score:
                    best_result = result
                    print(f"✅ Target reached: {args.target_score}/10")
                    break
            except Exception as exc:
                print(f"WARNING: Gemini selection failed on attempt {attempt}: {exc}")

        if best_result is None:
            print("Gemini selection failed. Falling back to a deterministic spread of images.")
            selected_images = fallback_selection(source_images, min(args.selected_count, len(source_images)))
        else:
            selected_images = best_result.selected_paths
            selection_result = best_result

        copy_selected_images(
            selected_images,
            selected_dir,
            clear_existing=args.clear_selected_dir,
        )
        save_manifest(
            selected_dir=selected_dir,
            source_dir=source_dir,
            collage_input_dir=selected_dir,
            selection=selection_result,
            selected_images=selected_images,
            mode=args.mode,
        )
        print(f"✅ Copied selected images to: {selected_dir}")

    if args.mode in {"collage", "both"}:
        if collage_input_dir is None:
            collage_input_dir = selected_dir

        collage_images = load_images_for_collage(collage_input_dir)
        if len(collage_images) == 0:
            print(f"ERROR: no supported images found in {collage_input_dir}")
            return 1

        output_path = default_output_path
        print(f"Building collage from {len(collage_images)} images in {collage_input_dir}")
        print(f"Collage output: {output_path}")
        build_final_collage(collage_images, output_path)
        print(f"✅ Collage saved to: {output_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
