---
name: save-article
description: Save and summarize an article from a URL (X/Twitter thread, blog post, newsletter, website) into the Obsidian Article folder. Use when the user says "save this article", "summarize and save", "save article <url>", or pastes a URL and asks to save/summarize it.
---

# Save Article Skill

Fetch an article or thread from a URL, summarize it, and save it to the Obsidian Article folder with a consistent format.

## Save Location

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Article/
```

## File Naming

Use the article title as the filename. Clean it up — remove special characters, shorten if too long.

Examples:
- `I Tested All 21 Claude Cowork Plugins - Tier List.md`
- `Why LLMs Struggle With Long-Context Reasoning.md`
- `The SaaSpocalypse - How Anthropic Killed Vertical SaaS.md`

## Output Format

Match the format of existing articles in the folder exactly:

```markdown
# [Article Title]

**Author:** [Author name or @handle]
**Source:** [Full URL]
**Saved:** [YYYY-MM-DD]

---

## Summary

[2–4 sentence overview of the article's core argument and why it matters. Be direct — lead with the thesis, not background.]

---

[Content sections — adapt based on article type, see below]

---

## Key Insight — [Theme]

[The single most important takeaway. One paragraph, direct.]

---

## Action Items

1. [Concrete thing to do based on the article]
2. [Another concrete action]
3. [...]
```

## Content Sections by Article Type

Adapt the sections between Summary and Key Insight based on what the article is about. Do not use generic section names — name them after the actual content.

**Tier list / ranking article:**
- `## Tier List` with a table per tier (S, A, B, C etc.)

**How-to / tutorial:**
- `## Steps` or `## How It Works` — numbered steps or structured breakdown

**Opinion / analysis piece:**
- `## The Argument` — the core claim
- `## Evidence / Examples` — supporting points
- `## Counterpoints` (if the article addresses them)

**Research / data article:**
- `## Key Findings` — bullet list of findings
- `## Methodology` (brief, only if relevant)

**News / announcement:**
- `## What Happened`
- `## Why It Matters`

**Thread (X/Twitter):**
- Treat as an opinion/analysis piece. Reconstruct the narrative from the thread.

**If sections don't fit a type above**, use your judgment — name sections after what they actually contain.

## Workflow

1. **Get today's date** — run `date +%Y-%m-%d`.

2. **Fetch the article** — use `WebFetch` with a prompt that extracts:
   - Full article title
   - Author name / handle
   - Publication date (if shown)
   - Full article body / thread content

   For X/Twitter threads: fetch the thread URL and reconstruct the full narrative from the tweets in order.

3. **Write the summary** — read the full content, then:
   - Write a 2–4 sentence Summary that leads with the thesis
   - Choose the right content sections for the article type
   - Write Key Insight (one clear paragraph)
   - Write Action Items (concrete, specific — not vague)

4. **Determine filename** from the article title.

5. **Check for duplicates** — run a quick `find` in the Article folder for files with similar names. If one exists, tell the user and ask whether to overwrite or create a new file.

6. **Save the file** using `python3`:

```python
import subprocess
from datetime import date

folder = '/Users/kpayuhawatta/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Article/'
filename = 'Article Title Here.md'
today = date.today().strftime('%Y-%m-%d')

content = '''# Article Title

**Author:** Author Name
**Source:** https://...
**Saved:** YYYY-MM-DD

---

## Summary

[summary text]

---

## [Section]

[content]

---

## Key Insight — [Theme]

[insight text]

---

## Action Items

1. [action]
2. [action]
'''

with open(folder + filename, 'w') as f:
    f.write(content)

print('Saved:', folder + filename)
```

7. **Report back** — confirm the file was saved and give a one-line summary of the article's main point.

## Quality Rules

- **No AI filler.** No "In today's rapidly evolving landscape...", no "This article explores...", no trailing "I hope this helps." Lead with facts and arguments.
- **Action Items must be specific.** "Install Data Analysis plugin and connect it to Snowflake" not "Consider using the plugin."
- **Key Insight is one thing.** Not a list. The single sharpest takeaway from the whole piece.
- **Preserve direct quotes** where they add punch — wrap in `> blockquote` format.
- **Section names reflect content**, not generic labels.
