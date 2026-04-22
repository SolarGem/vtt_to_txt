# vtt_to_txt

A simple Python script that batch-converts WebVTT subtitle files (`.vtt`) in a folder to plain text (`.txt`).

## Requirements

- Python 3.6+
- No third-party dependencies

## Usage

```bash
python vtt_to_txt.py <folder_path>
```

**Example:**

```bash
python vtt_to_txt.py ./subtitles
```

Each `.vtt` file in the folder will produce a corresponding `.txt` file in the same location (e.g. `lecture.vtt` → `lecture.txt`).

## What it does

- Removes the `WEBVTT` header
- Strips all timestamps (e.g. `00:00:01.000 --> 00:00:04.000`)
- Removes cue identifiers, `NOTE`, and `STYLE` blocks
- Strips inline tags such as `<b>`, `<i>`, `<c>`, and `<00:00:01.000>`
- Deduplicates consecutive identical lines (common in auto-generated captions)
- Prints a per-file ✓ / ✗ summary so errors are easy to spot

## Output

```
Found 3 .vtt file(s) in './subtitles'.

  ✓  lecture1.vtt  →  lecture1.txt
  ✓  lecture2.vtt  →  lecture2.txt
  ✗  broken.vtt    →  ERROR: 'utf-8' codec can't decode byte ...

Done.
```

## Notes

- Files are read and written as UTF-8.
- Existing `.txt` files with the same name will be overwritten without warning.
- Only files with the `.vtt` extension at the top level of the folder are processed (no recursive search).
