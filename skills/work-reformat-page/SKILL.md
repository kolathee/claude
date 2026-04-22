---
name: work-reformat-page
description: Reformat an existing Obsidian work page that lacks standard structure — adds frontmatter, wraps content in the correct sections, preserves all existing data. Use when the user says "reformat work page", "fix page structure", "f", or when a page exists but is missing frontmatter or proper sections.
---

# Work Page — Reformat

Reformat an existing Obsidian task page that lacks standard structure (no frontmatter, bare lists, etc.). The goal is to wrap the existing content in the standard template without losing any data.

## Paths

- **Workspace:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/<Quarter>/`

## Quarter Computation

- Jan–Jun → `YYYY H1`
- Jul–Dec → `YYYY H2`

## Workflow

1. **Read the existing file** with `python3`.

2. **Identify the content type** — determine appropriate `Type` from the content:
   - "Investigation", "Investigate", "Debug", "Root cause" → `🔍 investigation`
   - "Experiment", "Exp", "A/B" → `🧪 experiment`
   - "Bug", "Fix", "Issue", "Error" → `🐛 bug`
   - "Refactor", "Cleanup", "Migration" → `🔧 refactor`
   - Otherwise → `🌟 feature`

3. **Preserve all existing content.** Map it into correct sections. If content doesn't fit standard sections (e.g. custom tracking lists), keep it as named `# **Section**` headings after `# **What's about**`.

4. **Add frontmatter** with `Created time` set to today, `Status: In progress`.

5. **Add `# **Latest Update**`** (empty) and `# **What's about**` with a one-line description inferred from the content.

6. **Write the reformatted file back.**

```python
workspace = '/Users/kpayuhawatta/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/2026 H1/'
filename = 'Pending Int + Deint.md'

with open(workspace + filename, 'r') as f:
    existing = f.read()

# Rewrite with frontmatter + standard sections + preserved content
content = '''---
Status: In progress
Created time: YYYY-MM-DDTHH:MM
Quarter: YYYY H1 or H2
Type: 🔧 refactor
---
# **Latest Update**

# **What\\'s about**
- [inferred one-line description]

[preserved sections follow]
'''

with open(workspace + filename, 'w') as f:
    f.write(content)
```

## Critical Rules

- **Never lose data.** All existing content must appear somewhere in the reformatted file.
- **Omit empty sections.** Never write a heading with no content under it.
- **`# **Latest Update**` stays empty** unless there are actual update notes to record.
- **Infer `What's about`** from the existing content — write a concise one-line description.

## Standard Page Structure (for reference)

```
---
Status: In progress
Created time: YYYY-MM-DDTHH:MM
Latest: [one-line summary]
Quarter: YYYY H1 or H2
Type: 🌟 feature
---
# **Latest Update**

# **What's about**
- [description]

# **Reference**
- ### Links
	- Jira stories / merge requests / experiment

# **Implementation Details**
- **Data**: ...
- **Toggle**: ...
- **UI / Logic**: ...

# **Testing**
-
```

## Frontmatter Reference

| Field | Values |
|-------|--------|
| Status | `Not started`, `In progress`, `Next`, `Done`, `Blocked`, `On hold` |
| Type | `🌟 feature`, `🐛 bug`, `🔧 refactor`, `🧪 experiment`, `🔍 investigation` |
| Quarter | `YYYY H1 or H2` |
| Created time | `YYYY-MM-DDTHH:MM` |
