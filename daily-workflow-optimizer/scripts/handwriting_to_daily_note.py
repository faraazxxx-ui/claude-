#!/usr/bin/env python3
"""
Handwriting-to-Daily-Note Converter

Converts handwritten notes/drawings (from Surface/OneNote/Whiteboard exports)
into the structured daily note Markdown format.

Uses OCR (Tesseract or Windows Ink API) to extract text from images,
then maps recognized content to daily note sections.

Usage:
    python3 handwriting_to_daily_note.py --image /path/to/handwritten_note.png
    python3 handwriting_to_daily_note.py --image /path/to/note.jpg --output /path/to/daily_note.md

Requirements:
    pip install Pillow pytesseract
    apt install tesseract-ocr (Linux) or install Tesseract (Windows)
"""

import argparse
import os
import re
import sys
from datetime import datetime

try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("Install dependencies: pip install Pillow pytesseract")
    print("Also install Tesseract OCR: sudo apt install tesseract-ocr")
    sys.exit(1)


SECTION_KEYWORDS = {
    "wins": ["went well", "wins", "good", "positive", "success", "celebrate", "proud"],
    "improve": ["improve", "better", "fix", "change", "struggle", "challenge", "work on"],
    "goals": ["goal", "task", "todo", "to do", "plan", "focus", "priority", "target"],
    "events": ["event", "meeting", "call", "appointment", "schedule", "calendar"],
}

DAILY_NOTE_TEMPLATE = """---
date: "{date}"
day: "{day}"
tags: [daily-note, handwritten-import]
source: handwriting-ocr
---

# {day_full}

---

## Yesterday's Wins

{wins}

---

## Areas for Improvement

{improve}

---

## Today's Goals

{goals}

---

## Today's Events

{events}

---

## Raw OCR Text

> Auto-extracted from handwritten note. Review for accuracy.

```
{raw_text}
```
"""


def extract_text_from_image(image_path: str) -> str:
    """Extract text from an image using Tesseract OCR."""
    if not os.path.exists(image_path):
        print(f"ERROR: Image not found: {image_path}")
        sys.exit(1)

    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()


def classify_lines(lines: list) -> dict:
    """Classify extracted text lines into daily note sections."""
    sections = {"wins": [], "improve": [], "goals": [], "events": [], "uncategorized": []}
    current_section = "uncategorized"

    for line in lines:
        line_lower = line.lower().strip()
        if not line_lower:
            continue

        # Check if line is a section header
        matched = False
        for section, keywords in SECTION_KEYWORDS.items():
            if any(kw in line_lower for kw in keywords):
                current_section = section
                matched = True
                break

        if not matched:
            sections[current_section].append(line.strip())

    return sections


def format_section(items: list, numbered: bool = True, max_items: int = 3) -> str:
    """Format a list of items into numbered or bullet points."""
    if not items:
        return "1. \n2. \n3. " if numbered else "- [ ] \n- [ ] \n- [ ] "

    result = []
    for i, item in enumerate(items[:max_items], 1):
        if numbered:
            result.append(f"{i}. {item}")
        else:
            result.append(f"- [ ] **Goal {i}:** {item}")

    # Pad to 3 items if needed
    while len(result) < max_items:
        idx = len(result) + 1
        if numbered:
            result.append(f"{idx}. ")
        else:
            result.append(f"- [ ] **Goal {idx}:** ")

    return "\n".join(result)


def format_events(items: list, max_items: int = 3) -> str:
    """Format events into a table."""
    header = "| Time | Event | Location/Link |\n|------|-------|---------------|\n"
    rows = []
    for item in items[:max_items]:
        rows.append(f"|      | {item} |               |")
    while len(rows) < max_items:
        rows.append("|      |       |               |")
    return header + "\n".join(rows)


def generate_daily_note(raw_text: str, output_path: str = None) -> str:
    """Generate a structured daily note from OCR text."""
    now = datetime.now()
    lines = raw_text.split("\n")
    sections = classify_lines(lines)

    note = DAILY_NOTE_TEMPLATE.format(
        date=now.strftime("%Y-%m-%d"),
        day=now.strftime("%A"),
        day_full=now.strftime("%A, %B %d, %Y"),
        wins=format_section(sections["wins"], numbered=True),
        improve=format_section(sections["improve"], numbered=True),
        goals=format_section(sections["goals"], numbered=False),
        events=format_events(sections["events"]),
        raw_text=raw_text,
    )

    if output_path:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        with open(output_path, "w") as f:
            f.write(note)
        print(f"SUCCESS: Daily note saved to {output_path}")
    else:
        default_path = f"daily_note_{now.strftime('%Y-%m-%d')}.md"
        with open(default_path, "w") as f:
            f.write(note)
        print(f"SUCCESS: Daily note saved to {default_path}")

    return note


def main():
    parser = argparse.ArgumentParser(description="Convert handwritten notes to daily note format")
    parser.add_argument("--image", required=True, help="Path to handwritten note image")
    parser.add_argument("--output", default=None, help="Output path for the daily note Markdown")

    args = parser.parse_args()

    print(f"Extracting text from: {args.image}")
    raw_text = extract_text_from_image(args.image)

    if not raw_text:
        print("WARNING: No text detected. The image may be too unclear or contain only drawings.")
        raw_text = "(No text detected - manual entry required)"

    print(f"Detected {len(raw_text)} characters")
    generate_daily_note(raw_text, args.output)


if __name__ == "__main__":
    main()
