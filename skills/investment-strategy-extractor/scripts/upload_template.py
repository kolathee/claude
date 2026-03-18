#!/usr/bin/env python3
"""
Template for uploading a new book summary to Notion.

Usage:
    cp upload_template.py upload_my_book.py
    # Edit: set TITLE and populate all_blocks
    python3 upload_my_book.py

The script will:
  1. Create a new page in the Investment Books database
  2. Upload all blocks in batches of 20
  3. Print the Notion URL
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from notion_helpers import *

# ── Configure ──────────────────────────────────────────────────────────────────
TITLE = "Book Title Here"

# ── Blocks ─────────────────────────────────────────────────────────────────────
all_blocks = [
    callout("Book Title by Author (Year) — one-line description.", "📚", "blue_background"),
    divider(),

    h1("Introduction"),
    callout("Summary of introduction.", "📋", "gray_background"),
    bullet("Key point"),
    divider(),

    h2("Chapter 1: Title"),
    callout("2–4 sentence chapter summary.", "📋", "gray_background"),
    para("Key Ideas:", bold=True),
    bullet("Principle one"),
    bullet("Principle two"),
    para("Examples:", bold=True),
    bullet("Example or case study"),
    divider(),

    # ... repeat for each chapter ...

    h1("Master Checklist"),
    para("Section Name:", bold=True),
    bullet("Checklist item", source="Ch. 1"),
    bullet("Checklist item", source="Ch. 2, 3"),
    divider(),

    callout("Bottom line synthesis in 2–3 sentences.", "💡", "blue_background"),
]

# ── Run ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    page_id = create_page(TITLE)
    url = upload_blocks(page_id, all_blocks)
    print(f"\nNotion URL: {url}")
