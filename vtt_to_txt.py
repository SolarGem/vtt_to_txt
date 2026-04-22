#!/usr/bin/env python3
"""
Convert all .vtt (WebVTT subtitle) files in a folder to plain .txt files.
Usage: python vtt_to_txt.py <folder_path>
"""

import re
import sys
from pathlib import Path


def vtt_to_text(vtt_path: Path) -> str:
    """Parse a VTT file and return clean transcript text."""
    text = vtt_path.read_text(encoding="utf-8")

    # Remove the WEBVTT header block
    text = re.sub(r"^WEBVTT.*?\n\n", "", text, flags=re.DOTALL)

    lines = []
    for line in text.splitlines():
        line = line.strip()

        # Skip empty lines
        if not line:
            continue
        # Skip timestamps (e.g. "00:00:01.000 --> 00:00:04.000")
        if re.match(r"^\d{2}:\d{2}:\d{2}[\.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[\.,]\d{3}", line):
            continue
        # Skip cue identifiers (pure numbers or NOTE lines)
        if re.match(r"^\d+$", line) or line.startswith("NOTE") or line.startswith("STYLE"):
            continue

        # Strip inline VTT tags like <c>, <b>, <i>, <00:00:01.000>, etc.
        line = re.sub(r"<[^>]+>", "", line)

        if line:
            lines.append(line)

    # Deduplicate consecutive identical lines (common in auto-generated captions)
    deduped = [lines[i] for i in range(len(lines)) if i == 0 or lines[i] != lines[i - 1]]

    return "\n".join(deduped)


def convert_folder(folder: Path) -> None:
    vtt_files = sorted(folder.glob("*.vtt"))

    if not vtt_files:
        print(f"No .vtt files found in '{folder}'.")
        return

    print(f"Found {len(vtt_files)} .vtt file(s) in '{folder}'.\n")

    for vtt_file in vtt_files:
        txt_file = vtt_file.with_suffix(".txt")
        try:
            content = vtt_to_text(vtt_file)
            txt_file.write_text(content, encoding="utf-8")
            print(f"  ✓  {vtt_file.name}  →  {txt_file.name}")
        except Exception as e:
            print(f"  ✗  {vtt_file.name}  →  ERROR: {e}")

    print("\nDone.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vtt_to_txt.py <folder_path>")
        sys.exit(1)

    folder = Path(sys.argv[1])

    if not folder.is_dir():
        print(f"Error: '{folder}' is not a valid directory.")
        sys.exit(1)

    convert_folder(folder)
