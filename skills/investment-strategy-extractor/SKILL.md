---
name: extract-investment-strategy
description: This skill should be used when the user asks to "extract investment strategy", "summarize investment book", "analyze investment principles", "get key ideas from investment resource", "extract principles from chapters", or provides investment books/articles/videos requesting structured analysis with actionable takeaways and master checklist.
version: 0.1.0
---

# Investment Strategy Extractor

## Purpose

This skill provides a structured approach to analyzing investment resources (books, articles, videos) and extracting actionable principles, regardless of the specific investment strategy. The output follows a consistent format with chapter-by-chapter summaries, key takeaways, a master checklist, and saves to Obsidian for knowledge management.

## When to Use This Skill

Use this skill when:
- User provides investment books (PDFs, titles, or references) for analysis
- User shares investment articles or YouTube videos requesting principle extraction
- User asks to "summarize the content of each chapter and highlight key ideas"

## Core Workflow

### Step 1: Identify the Resource

Determine the resource type and access method:

**PDF Files:**
- Use Read tool with file path to access PDF content
- For large PDFs (>10 pages), read in chunks using the `pages` parameter
- Example: `Read(file_path="/path/to/book.pdf", pages="1-20")`

**Web Articles:**
- Use WebFetch tool to retrieve article content
- Extract main content, filtering out ads and navigation

**YouTube Videos:**
- Use WebFetch to access video transcripts or descriptions
- If transcript unavailable, request user to provide text summary or key points

**Book Titles Without Files:**
- Use general knowledge about well-known investment books
- Inform user that analysis will be based on published summaries and known principles
- Request PDF or detailed source for more comprehensive analysis

### Step 2: Analyze Structure

Identify the resource's organization:
- **Books**: Parts, chapters, sections
- **Articles**: Main sections, arguments, case studies
- **Videos**: Timestamps, key segments, main themes

Create a mental map of the content hierarchy before beginning extraction.

### Step 3: Extract Content Using the Standard Format

Follow the output template structure documented in `references/output-template.md`. The format includes:

1. **Title Header**: Resource name and author
2. **Part/Chapter Breakdown**: Hierarchical structure with:
   - Part titles (if applicable)
   - Chapter titles and summaries
   - Key ideas and principles from each chapter
3. **Master Checklist**: Actionable items in table format
4. **Bottom Line**: Concise overall summary

**Extraction Guidelines:**

**Chapter Summaries:**
- Capture the main argument or theme in 2-4 sentences
- Focus on what the author is teaching, not just what they discuss
- Maintain the original structure and flow of ideas

**Key Ideas:**
- Extract specific, actionable principles
- Look for rules, frameworks, criteria, or decision-making guidelines
- Prioritize ideas that can be applied to investment strategy
- Quote memorable phrases or formulas when relevant

**Case Studies:**
- List concrete examples, historical events, or case studies the author uses to illustrate the chapter's principles
- Include company names, events, dates, or numbers where mentioned (e.g., "Spain Fund trading at 2× NAV in 1989", "Esco Electronics spinoff at $3 vs. NCAV of $15+")
- Omit this section entirely if the chapter contains no illustrative examples or case studies

**Key Ideas / Case Studies bullets (inside each chapter section):**
- **NEVER add chapter references** — no `_(Ch. X)_`, no `_[Ch. X]_`, nothing — the bullets already live inside the chapter, so the reference is implicit
- Chapter references belong ONLY in the Master Checklist section, nowhere else
- Just write the principle or insight directly

**Master Checklist:**
- Consolidate all actionable principles into a single checklist — this is the ONLY place chapter references belong
- Group items into logical sections (e.g. Durable Competitive Advantage, Quantitative Screens, Price & Timing, Sell Signals, Arbitrage) — adapt sections to fit the book's themes
- Frame items as yes/no questions or evaluation criteria
- Make items specific enough to use in actual investment decisions
- Append a chapter reference to every item using numbers or Roman numerals only — no descriptive labels
  - For books with numbered chapters: `[Ch. 5]`, `[Ch. 12, 18, 23]`, `[Ch. 3, 7, 14, 22]` — list as many as apply
  - For books with named (unnumbered) chapters: assign sequential numbers by order of appearance (chapter 1 = first chapter, chapter 2 = second, etc.)
  - For books organized by parts only (no chapters): use `[Part I]`, `[Part II]`
  - **Never** write `[Part 3: DANGER SIGNS]` or `[Ch. EFFICIENCY]` — only numbers or Roman numerals
- In markdown: append `_[Ch. X]_` italicized at the end of the line

**Bottom Line:**
- Synthesize the core philosophy in 2-3 sentences
- Capture the "big idea" that unifies all chapters
- Make it memorable and actionable

### Step 4: Format the Output

Structure the analysis using markdown with proper hierarchy:

```markdown
# [Book Title] by [Author]

## Part I: [Part Name]

### Chapter X: [Chapter Title]

**Summary:**
[2-4 sentence summary of the chapter's main argument]

**Key Ideas:**
- [Specific principle or insight]
- [Another actionable takeaway]
- [Framework or criteria mentioned]
*(NO chapter references here — ONLY the Master Checklist uses chapter refs)*

**Case Studies:**
- [Concrete example or case study from the book, with specifics]
- [Another example if present]
*(Omit this section if the chapter has no examples or case studies)*

### Chapter Y: [Chapter Title]
...

## Master Checklist

**[Section Name — e.g. Durable Competitive Advantage]:**

- [Evaluation question] _[Ch. 5]_
- [Another criterion] _[Ch. 5, 12]_

**[Section Name — e.g. Quantitative Screens]:**

- [Criterion] _[Ch. 9]_

**[Section Name — e.g. Price & Timing]:**

- [Criterion] _[Ch. 14]_

**[Section Name — e.g. Sell Signals]:**

- [Criterion] _[Ch. 18]_

*(Add or remove sections to fit the book's themes. Every item must have a chapter reference in [Ch. X] format — numbers or Roman numerals only, never descriptive labels.)*

## Bottom Line

[2-3 sentence synthesis of the book's core philosophy]
```

Refer to `examples/format-example.md` for a complete working example.

### Step 5: Two Output Locations (Required Every Time)

Every extraction must produce **both outputs**. Do not skip any.

| # | Location | Format | Purpose |
|---|---|---|---|
| 1 | **`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Investment/contexts/investment-rules.md`** | Concise rules only, appended | Other investing skills reference |
| 2 | **`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Books/[Book Title] - SUMMARY.md`** | Full markdown summary | Centralized library of all extracted books |

Create `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Books/` if it doesn't exist.

---

## Handling Different Resource Types

### Books (Primary Use Case)

**For Complete Books:**
- Read entire PDF if provided
- Extract every chapter systematically
- Build comprehensive master checklist (15-30+ items)
- Include part divisions if book is structured that way

**For Book Chapters/Excerpts:**
- Focus on available chapters
- Note that master checklist may be partial
- Suggest reading full book for complete principles

### Articles

**Adaptation Needed:**
- Replace "chapters" with article sections
- Focus on case studies, arguments, and frameworks
- Master checklist may be shorter (5-10 items)
- Bottom line captures the article's main thesis

### YouTube Videos

**Adaptation Needed:**
- Organize by video segments or timestamps
- Extract principles from spoken content
- May have less structured content than books
- Focus on memorable quotes and frameworks mentioned

## Quality Standards

**Comprehensiveness:**
- Don't skip chapters or sections
- Capture all major principles, even if they seem similar
- Include both strategic and tactical insights

**Clarity:**
- Write summaries in clear, direct language
- Avoid jargon unless it's key terminology from the source
- Make checklist items unambiguous and actionable

**Accuracy:**
- Stay faithful to the author's actual arguments
- Don't inject external frameworks unless requested
- Quote directly when capturing key phrases or formulas

**Usability:**
- Master checklist should be practical for actual investment evaluation
- Each checklist item should be verifiable with available information
- Bottom line should be memorable and capture the essence

## Additional Resources

### Reference Files

For detailed formatting and integration:
- **`references/output-template.md`** - Complete format specification with field descriptions
- **`references/notion-integration.md`** - Step-by-step Notion database integration guide

### Example Files

Working example in `examples/`:
- **`examples/format-example.md`** - Format template showing proper structure, master checklist format, and quality standards

## Common Scenarios

**Scenario: User provides PDF without context**
- Ask: "I'll analyze this investment resource. Should I extract all chapters or focus on specific sections?"

**Scenario: User requests analysis of famous book**
- Inform: "I can provide analysis based on published knowledge, but a PDF would allow more comprehensive extraction."
- Proceed: Use general knowledge but note any limitations

**Scenario: User shares YouTube video**
- Check: Look for transcript availability
- Adapt: Extract principles from available content
- Format: Organize by video segments rather than chapters

**Scenario: Master checklist seems too short**
- Review: Ensure all actionable principles were captured
- Consolidate: Combine similar principles if there's legitimate overlap
- Explain: Some resources naturally yield fewer actionable items

## Tips for Effective Extraction

1. **Read completely first**: Don't start extracting until structure is clear
2. **Maintain hierarchy**: Preserve the author's organization (parts/chapters)
3. **Focus on principles**: Look for "how to" not just "what is"
4. **Make checklists actionable**: Frame as questions you'd ask about a specific investment
5. **Test the bottom line**: Can you explain the book's philosophy to someone in 30 seconds?

## Additional Notes

**Future Enhancements:**
- Could add scripts for batch processing multiple books
- Could integrate with citation management tools
- Could generate comparison reports across multiple resources

### Step 5a: Save Summary MD File (Location 2)

Write the full markdown summary to the centralized library:

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Books/[Book Title] - SUMMARY.md
```

Create the directory if it doesn't exist: `mkdir -p ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/CupOb/Books`

The markdown format matches Step 4 output exactly (parts, chapters, summaries, key ideas, master checklist, bottom line).

---

### Step 5b: Save Rules to Context File (Location 1)

Extract a **concise rules file** for use by the investment evaluator skill.

**File location**: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Investment/contexts/investment-rules.md`

**Format standard — follow exactly, append to existing file (do not overwrite):**

```markdown
---

## Book Title — Author (Year)

**Section Name**
- Rule stated concisely _(Ch. X)_
- Another rule _(Ch. X, Y)_

**Section Name**
- Rule _(Ch. Z)_
```

**Rules for each element:**

| Element | Format | Example |
|---|---|---|
| Separator | `---` blank line before every book entry | — |
| Book title line | `## Title — Author (Year)` | `## The New Buffettology — Mary Buffett & David Clark (2002)` |
| Section header | `**Section Name**` bold, no colon | `**Business Quality**` |
| Rule line | `- Rule text _(Ch. X)_` | `- ROE must exceed 12% _(Ch. 13)_` |
| Multi-chapter ref | comma-separated numbers, no limit | `_(Ch. 13, 18, 24)_` |
| Part reference | `_(Part I)_` — only when book has no chapters | `_(Part VIII)_` |

**What NOT to do:**
- Do not use `### headings` for sections — use `**bold**` only
- Do not use a table format
- Do not omit the year from the book title line
- Do not omit chapter references from any rule
- Do not add a `---` divider at the very end of the file
- **Do not use descriptive labels in references** — write `_(Ch. 5)_` not `_(Ch. DANGER SIGNS)_` or `_(Part 3: Pricing Power)_`; numbers or Roman numerals only

**Section naming** — use the same logical sections as the master checklist, adapted to fit the book. Common sections: Business Quality, Quantitative Screens, Price & Timing, Sell Rules, Valuation, Earnings Analysis, Balance Sheet, Portfolio & Risk Management, etc.

**What to include:**
- Every actionable rule, criterion, or principle (same as master checklist items + key ideas that are rules)
- Specific quantitative thresholds (e.g., "coverage ratio ≥ 3×", "current ratio ≥ 2:1", "7–10 year average earnings")
- Decision frameworks (e.g., "buy only when price < NCAV", "avoid if leverage > X")
- Red flags and disqualifiers (e.g., "big bath accounting", "pyramided holding structures")

**What to exclude:**
- Historical context or stories
- Summaries of what the chapter is about
- Redundant restatements of the same rule
- Anything that isn't actionable in an investment decision

**Example entry:**

```markdown
---

## Security Analysis — Graham & Dodd (2008)

**Earnings Analysis**
- Never use single-year earnings; normalize over 7–10 years through a full cycle _(Ch. 37)_
- Restructuring charges recurring every 2–3 years are normal operating costs, not extraordinary _(Ch. 32)_

**Valuation**
- NCAV = Current Assets − Total Liabilities; stocks below NCAV are clearest form of undervaluation _(Ch. 43)_
- Apply P/E to normalized earnings only — never to peak or trough _(Ch. 39)_

**Balance Sheet**
- Current ratio ≥ 2:1; quick ratio ≥ 1:1 as minimum financial health _(Ch. 45)_

**Red Flags**
- Avoid pyramided holding structures — leverage amplifies losses exponentially _(Ch. 48)_
```

This file feeds directly into the future investment evaluator skill, so prioritize precision and brevity over completeness.

---

## Workflow Summary

1. **Identify**: Determine resource type and access method
2. **Analyze**: Map content structure (parts/chapters/sections)
3. **Extract**: Follow standard format with summaries, key ideas, checklist
4. **Format**: Use markdown hierarchy for clarity
5. **Two outputs** (both required):
   - **5a** — `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Books/[Book Title] - SUMMARY.md`
   - **5b** — Append concise rules to `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Investment/contexts/investment-rules.md`
6. **Confirm**: Provide user with the file paths written

Follow this workflow systematically to produce consistent, high-quality investment strategy extractions.
