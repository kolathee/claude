---
name: book-summary
description: Summarize any book — fiction, non-fiction, self-help, business, philosophy, biography, or any genre — into a structured Obsidian note with chapter breakdowns, key ideas, notable quotes, and a bottom line. Use this skill when the user asks to "summarize a book", "create book notes", "extract key ideas from a book", "summarize chapters", "make book notes", "save book summary", "write up my notes on [book]", or provides a book title/PDF requesting any form of structured summary or reading notes.
version: 0.1.0
---

# Book Summary

## Purpose

This skill produces a structured, comprehensive summary of any book — regardless of genre — and saves it to the Obsidian Books library. The output captures chapter-by-chapter content, key ideas and themes, notable quotes, and a concise bottom line.

## When to Use This Skill

Use this skill when:
- User provides a book title, PDF, or reference requesting a summary or reading notes
- User asks to capture key ideas or takeaways from a book they've read
- User wants to create or save Obsidian notes for a book

## Core Workflow

### Step 1: Identify the Resource

Determine how the book content is available:

**PDF Files:**
- Use Read tool with the file path
- For large PDFs (>10 pages), read in chunks: `Read(file_path="...", pages="1-20")`
- Work through the full book systematically before writing the summary

**Book Title Without File:**
- Use general knowledge for well-known books
- Inform the user the summary is based on published knowledge, not a provided source
- Offer to do a more detailed extraction if they can share a PDF

**Web Articles / Online Resources:**
- Use WebFetch to retrieve the content
- Filter out ads and navigation; focus on the main body

### Step 2: Analyze Structure

Before writing anything, map the book's organization:
- **Books**: Parts, chapters, sections — note the hierarchy
- **Short books / essays**: Main arguments, sections, big ideas
- **Memoirs / biography**: Timeline, life phases, key events

Understanding the structure first ensures the summary preserves the author's intended flow.

### Step 3: Extract and Write the Summary

Follow the output template below. Adapt sections as needed for the book's genre and structure.

**Chapter Summaries:**
- 2–4 sentences capturing the main argument or narrative of the chapter
- Focus on what the reader is meant to take away, not just what happens
- Maintain the original flow and sequence of ideas

**Key Ideas:**
- Specific, memorable principles, frameworks, arguments, or insights
- Things worth remembering or acting on — not just plot points
- Quote directly when the author's exact phrasing is part of the value

**Notable Quotes:**
- Collect the most memorable or illuminating lines from the book
- Include enough context so the quote stands on its own

**Key Themes:**
- 3–6 overarching ideas that run through the whole book
- These sit above the chapter level — patterns that connect the parts

**Bottom Line:**
- 2–3 sentences that capture the book's core message or argument
- Should answer: "What is this book ultimately about and why does it matter?"

### Step 4: Format the Output

Use this template:

```markdown
# [Book Title] by [Author] ([Year])

**Genre:** [e.g. Business / Self-Help / Philosophy / Biography / Fiction]
**Pages:** [approximate if known]

## Overview

[2–3 sentence description of the book's premise, what it sets out to do, and who it's for.]

---

## Part I: [Part Name] *(if book has parts)*

### Chapter X: [Chapter Title]

**Summary:**
[2–4 sentences capturing the chapter's main argument or narrative.]

**Key Ideas:**
- [Specific insight, principle, or argument]
- [Another takeaway worth remembering]
- [Framework, model, or memorable concept]

**Notable Quotes:**
> "[Memorable quote from this chapter]"

---

### Chapter Y: [Chapter Title]

...

---

## Key Themes

- **[Theme Name]:** [1–2 sentence explanation of the theme and how it runs through the book]
- **[Theme Name]:** [Explanation]
- **[Theme Name]:** [Explanation]

---

## Notable Quotes (Collected)

> "[Quote]" — [Chapter/context if helpful]

> "[Quote]"

---

## Bottom Line

[2–3 sentences synthesizing the book's core message, argument, or philosophy. What's the big idea? Why does this book matter?]
```

**Formatting notes:**
- Use `---` horizontal rules between major sections for readability
- Omit sections that don't apply (e.g., no "Parts" if book doesn't have them)
- For fiction: chapters become plot events; "Key Ideas" becomes "Themes & Observations"; skip the Master Checklist concept entirely
- For memoirs/biography: organize by life phase or timeline if no formal chapters

### Step 5: Save to Obsidian Books Folder

Before saving, **always check existing subfolders** in the Books directory:

```bash
ls ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/CupOb/Books/
```

Pick the most fitting existing subfolder based on the book's genre/topic. Only create a new subfolder if none of the existing ones are a reasonable match. Then write the full markdown summary to:

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Books/[Subfolder]/[Book Title] - SUMMARY.md
```

Use the Write tool to save the file. The filename format is:
- `[Book Title].md` — e.g., `Atomic Habits.md`

After saving, confirm to the user with the full file path.

---

## Handling Different Resource Types

### Non-Fiction / Business / Self-Help (Primary Use Case)

- Extract every chapter systematically
- Key Ideas section per chapter should be meaty — this is where the value is
- Collect 5–10 notable quotes across the book
- Key Themes should surface cross-cutting ideas not obvious from individual chapters

### Biography / Memoir

- Organize by life phases or chronological sections if no formal chapters
- "Key Ideas" becomes "Observations & Reflections" — what makes this person's story instructive
- Notable Quotes from the subject and the author

### Fiction

- Summarize by chapter or section — keep plot spoilers in mind if the user wants a "safe" version
- "Key Ideas" becomes "Themes & Literary Observations"
- Notable Quotes: dialogue, descriptions, lines that capture the book's voice
- Key Themes: the author's major preoccupations, symbols, motifs

### Articles / Essays

- Replace "chapters" with article sections or major arguments
- Shorter output is fine — not every section needs a full Key Ideas list
- Bottom Line captures the article's core thesis

---

## Quality Standards

**Completeness:** Don't skip chapters. Even short chapters deserve a summary line.

**Faithfulness:** Stay true to the author's actual argument. Don't impose external frameworks.

**Usability:** A reader who hasn't read the book should understand it. A reader who has should find the notes a useful reference.

**Clarity:** Plain language. Avoid jargon unless it's key terminology from the source.

---

## Workflow Summary

1. **Identify** — determine resource type and access method
2. **Analyze** — map the book's structure before writing
3. **Extract** — chapter summaries, key ideas, quotes, themes
4. **Format** — use the markdown template above, adapted for the genre
5. **Save** — check existing subfolders in `Books/`, pick the best fit (or create new if none match), write to `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Books/[Subfolder]/[Book Title].md`
6. **Confirm** — tell the user the file path and offer to refine anything
