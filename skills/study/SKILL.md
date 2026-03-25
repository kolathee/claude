---
name: study
description: This skill should be used when the user asks to "study", "summarize a topic", "create a study page", "make study notes", "explain [topic] for review", "create a cheat sheet", "5-minute summary", "quick reference for [topic]", or provides a topic (with or without resources) and wants it saved as a study note in Obsidian. Also trigger when the user says "I want to learn about X" or "create study material for X".
version: 0.1.0
---

# Study Skill

## Purpose

Produce a concise, visually structured study page for any topic — reviewable in under 5 minutes — and save it to the Obsidian Study folder. When a topic is too broad for one page, break it into sub-pages with clickable Obsidian links.

## Obsidian Study Path

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Study/
```

## Core Workflow

### Step 1: Gather Source Material

**If resources are provided (URL, PDF, file, paste):**
- URL → use `WebFetch` to retrieve content
- PDF → use `Read` with pages parameter for large files
- Pasted text → use directly

**If no resources provided:**
- Use internal knowledge first
- Supplement with `WebSearch` for recent topics, technical specs, or anything that benefits from up-to-date sources
- Prefer authoritative sources (official docs, Wikipedia, reputable tutorials)

### Step 2: Assess Scope

Before writing, judge whether the topic fits a single 5-minute page:

- **Narrow topic** (e.g., "Python list comprehensions", "HTTP status codes") → single page
- **Medium topic** (e.g., "REST APIs", "Docker basics") → single page with a "Dive Deeper" section at the bottom
- **Broad topic** (e.g., "Machine Learning", "System Design", "React") → index page + linked sub-pages

For broad topics: create a main index page first, then create each sub-page and link them using Obsidian wikilinks: `[[Sub-Page Title]]`.

### Step 3: Write the Study Page(s)

Follow the output template in `references/template.md`. Key principles:

**Readability over format rigidity.** Use a mix of short paragraphs and bullet points — whichever makes the content easiest to follow. Avoid long prose blocks; keep paragraphs to 2–3 sentences max. Bullets work well for lists and comparisons; short paragraphs work well for explaining a concept or mental model.

**Lead with the mental model** — open each page with 1–2 sentences answering "what is this and why does it matter."

**Diagrams over walls of text** — use Mermaid for flows, relationships, and hierarchies wherever a visual helps more than words.

**Always show a concrete example** — after explaining a concept, include a minimal code snippet or real-world analogy.

**5-minute rule** — if the main section takes longer than 5 minutes to read, move overflow content below a `---` divider into a "Dive Deeper" section or a linked sub-page.

### Step 4: Save to Obsidian

**Single page:**
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Study/[Topic].md
```

**Multi-page (broad topics):**
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Study/[Topic]/[Topic] - Overview.md
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Study/[Topic]/[Sub-Topic 1].md
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Study/[Topic]/[Sub-Topic 2].md
```

Create the subdirectory first if needed:
```bash
mkdir -p ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/CupOb/Study/[Topic]
```

Use the `Write` tool to save each file.

### Step 5: Confirm

After saving, tell the user:
- File path(s) created
- A one-line summary of what was covered
- If multi-page: list all pages created

---

## Diagram Guidelines

**Use Mermaid for:**
- Processes / flows → `flowchart LR`
- Hierarchies / trees → `graph TD`
- Sequences → `sequenceDiagram`
- State transitions → `stateDiagram-v2`

**Use tables for:**
- Quick comparisons (e.g., GET vs POST, SQL vs NoSQL)
- Key-value references (e.g., HTTP codes, command cheatsheets)

**Use code blocks for:**
- Syntax examples — always include a minimal working example
- Before/after patterns

---

## Quiz Section

Every study page must end with a **Quick Quiz** section — 4–6 questions that test understanding, not just recall. Good quizzes mix question types:

- **Concept check** — "What is X?" or "Why does Y happen?"
- **Apply it** — "Given this scenario, what would you do / what output do you expect?"
- **Compare/contrast** — "What's the difference between X and Y?"
- **Gotcha / common mistake** — "What's wrong with this code?" or "When does this approach break down?"

Format as a collapsible spoiler so the user can attempt before seeing the answer:

```markdown
## Quick Quiz

**1. [Question]**

<details>
<summary>Answer</summary>

[Answer — keep it concise but complete. Include a code example if it helps.]

</details>

**2. [Question]**
...
```

For multi-page topics, include a quiz on each sub-page covering that page's content. The overview/index page can have a broader quiz spanning all sub-topics.

---

## Quality Checklist

Before saving, verify:
- [ ] Opens with a 1–2 sentence mental model
- [ ] Mix of short paragraphs and bullets — easy to scan and follow
- [ ] No paragraph longer than 3 sentences
- [ ] At least one diagram or visual aid
- [ ] At least one concrete code or real-world example
- [ ] Main section readable in ≤ 5 minutes
- [ ] Overflow content in "Dive Deeper" or linked sub-pages
- [ ] Sub-page links use `[[wikilink]]` format for Obsidian compatibility
- [ ] Ends with a Quick Quiz (4–6 questions with collapsible answers)

---

## Additional Resources

- **`references/template.md`** — Full output template with all sections
