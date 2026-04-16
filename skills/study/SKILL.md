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

**Sub-pages can have their own sub-pages** when a sub-topic is itself broad enough to exceed the 5-minute rule AND its overflow content is conceptually distinct (not just "more of the same"). Maximum nesting depth: **2 levels** (index → sub-page → sub-sub-page). Never go deeper.

```
Level 0:  Topic/Topic - Overview.md
Level 1:  Topic/Sub-Topic.md           (or Topic/Sub-Topic/Sub-Topic - Overview.md if it splits further)
Level 2:  Topic/Sub-Topic/Detail.md    (deepest allowed)
```

When a sub-page needs to split: convert it into its own folder with an Overview page, then add the detail pages inside that folder.

### Step 2.5: Scan for Related Pages

Before writing, scan the Study folder for existing pages that are related to the current topic:

```bash
find ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/CupOb/Study -name "*.md" | sort
```

Note any pages that share concepts, prerequisites, or natural follow-ons with the topic being written. You will link to them in a **"Related Pages"** section at the bottom of each page (after Dive Deeper, before the quiz). Use Obsidian wikilinks: `[[Page Name]]`.

Examples of worth linking:
- JS DOM page → link to `[[JavaScript - Overview]]` (prerequisite)
- React State & Hooks → link to `[[JS DOM]]` (related browser concept)
- A data structures page → link to an algorithms page if one exists

Don't force links — only include pages where the connection is genuinely useful to a reader.

### Step 3: Write the Study Page(s)

Follow the output template in `references/template.md`. Key principles:

**Readability over format rigidity.** Use a mix of short paragraphs and bullet points — whichever makes the content easiest to follow. Avoid long prose blocks; keep paragraphs to 2–3 sentences max. Bullets work well for lists and comparisons; short paragraphs work well for explaining a concept or mental model.

**Lead with the mental model** — open each page with 1–2 sentences answering "what is this and why does it matter."

**Diagrams over walls of text** — use Mermaid for flows, relationships, and hierarchies wherever a visual helps more than words.

**Always show a concrete example** — after explaining a concept, include a minimal code snippet or real-world analogy.

**5-minute rule** — if the main section takes longer than 5 minutes to read, move overflow content below a `---` divider into a "Dive Deeper" section or a linked sub-page.

**Worth mentioning but verbose** — details, edge cases, and extended examples that are valuable but would break the concise flow of the main section belong in a **"More Detail"** section below the main content (before the quiz). This is separate from "Dive Deeper" (which is for entirely optional advanced content). Use "More Detail" for things like:
- A concept that needs a longer code example to fully illustrate
- An edge case that's common enough to know but too verbose for inline mention
- A worked example tracing through multiple steps

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

**Mermaid node label line breaks:** Use `<br/>` — NOT `\n`. Using `\n` renders literally as text.
```
✅ A["Line 1<br/>Line 2"]
❌ A["Line 1\nLine 2"]
```

**Node colors:** Color nodes for visual clarity — colors are aesthetic, not semantic. Use `classDef` for reuse:

```
classDef blue   fill:#3b82f6,stroke:#1d4ed8,color:#fff
classDef teal   fill:#14b8a6,stroke:#0f766e,color:#fff
classDef orange fill:#f97316,stroke:#ea580c,color:#fff
classDef purple fill:#a855f7,stroke:#7e22ce,color:#fff
classDef green  fill:#22c55e,stroke:#16a34a,color:#fff
classDef pink   fill:#ec4899,stroke:#be185d,color:#fff
classDef slate  fill:#475569,stroke:#1e293b,color:#fff
classDef amber  fill:#f59e0b,stroke:#b45309,color:#fff

A["Node"]:::blue
```

Assign colors freely — just make adjacent nodes visually distinct. No need to make color mean anything.

**Use tables for:**
- Quick comparisons (e.g., GET vs POST, SQL vs NoSQL)
- Key-value references (e.g., HTTP codes, command cheatsheets)

**Use code blocks for:**
- Syntax examples — always include a minimal working example
- Before/after patterns

---

## Quiz Section

Every study page must end with a **Quick Quiz** section. Quizzes are the primary active-learning mechanism — aim for **8–12 questions per page**, enough to cover every major concept, pattern, and gotcha presented. Fewer questions only if the page is genuinely narrow (< 3 concepts).

**Coverage rule:** After writing the quiz, mentally check off each section heading. If a section has no question against it, add one.

Mix question types to test different levels of understanding:

- **Concept check** — "What is X?" or "Why does Y happen?"
- **Apply it** — "Given this scenario, what would you do / what output do you expect?"
- **Compare/contrast** — "What's the difference between X and Y?"
- **Gotcha / common mistake** — "What's wrong with this code?" or "When does this approach break down?"
- **Predict output** — Show a code snippet, ask what it prints/returns — great for coercion, async order, scope
- **Design choice** — "When would you choose X over Y?" — tests judgment, not just recall

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

For multi-page topics, include a full quiz on each sub-page covering that page's content. The overview/index page quiz should span all sub-topics.

---

## Quality Checklist

Before saving, verify:
- [ ] Opens with a 1–2 sentence mental model
- [ ] Mix of short paragraphs and bullets — easy to scan and follow
- [ ] No paragraph longer than 3 sentences
- [ ] At least one diagram or visual aid
- [ ] At least one concrete code or real-world example
- [ ] Main section readable in ≤ 5 minutes
- [ ] Verbose-but-valuable content moved to "More Detail" section (before quiz)
- [ ] Truly advanced / optional content in "Dive Deeper" section (after quiz) or linked sub-pages
- [ ] Sub-page links use `[[wikilink]]` format for Obsidian compatibility
- [ ] Related existing study pages linked in a "Related Pages" section
- [ ] Sub-page nesting ≤ 2 levels deep
- [ ] Ends with a Quick Quiz (8–12 questions, covering every major concept/section)
- [ ] Quiz has at least one of each type: concept check, apply-it, compare/contrast, gotcha, predict output

---

## Additional Resources

- **`references/template.md`** — Full output template with all sections
