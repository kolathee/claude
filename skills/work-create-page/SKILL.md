---
name: work-create-page
description: Create a new Obsidian work page for a task in the Agoda Workspace. Use when the user says "create a work page", "new task page", "add a work page", "c", or describes a new task that needs a page. Also handles interview pages.
---

# Work Page — Create

Create a new Obsidian task page in the Agoda Workspace folder.

## Paths

- **Workspace:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/<Quarter>/`
- **Backlog subfolder:** `<workspace>Backlog/`
- **Interview pages:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/Interviews/YYYY/`
- **Template reference:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/Work Template.md`

## Quarter Computation

- Jan–Jun → `YYYY H1`
- Jul–Dec → `YYYY H2`

## File Naming

`(FEATURE_CODE) Platform Short Description.md`

Examples:
- `(BWZP) iOS SSR badge.md`
- `Integration DatePicker Fix (native).md`
- `Deintegration Cashback Redemption Nudge.md`

Use `(FEATURE_CODE)` prefix when tied to a specific experiment/feature code. Otherwise use a plain descriptive name.

## Type Inference — always check before defaulting to feature

- "Investigation", "Investigate", "Debug", "Root cause" → `🔍 investigation`
- "Experiment", "Exp", "A/B", "Launch", "Allocation bias" → `🧪 experiment`
- "Bug", "Fix", "Issue", "Error" → `🐛 bug`
- "Refactor", "Cleanup", "Migration", "Migrate" → `🔧 refactor`
- Otherwise → `🌟 feature`

## Workflow

1. **Search first.** Run `find` across the entire `Agoda/<Quarter>/` tree (including all subfolders) for any file whose name contains key words from the task. If a match is found, open it instead of creating a new one.

2. **Gather details.** Ask for missing info: task name, Jira ticket, MR link, experiment ID, type (defaults above), brief description. Skip sections for anything unknown.

3. **Determine the file name** from the task context.

4. **Write the file using `python3`** (required for special characters in filenames). New tasks default to `Status: Not started`, `Type: 🌟 feature`, saved into `Backlog/`:

```python
import datetime

# Compute quarter from current date
workspace = '/Users/kpayuhawatta/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/2026 H1/Backlog/'
filename = '(BWZP) iOS SSR badge.md'

content = '''---
Status: Not started
Created time: YYYY-MM-DDTHH:MM
Quarter: YYYY H1 or H2
Type: 🌟 feature
---
# **Latest Update**

# **What's about**
- [description]

# **Reference**
- ### Links
\t- Jira stories
\t\t- [🎫 PAYFLEX-233](https://agoda.atlassian.net/browse/PAYFLEX-233)
\t- merge requests
\t\t- [MR title](https://gitlab.agodadev.io/...)
\t- experiment
\t\t- PAYFLEX-233-IOS

# **Implementation Details**
- **Data**:
\t- [models, APIs, mappers]
- **Toggle** (if any):
\t- [experiment ID]
- **UI / Logic** (if needed):
\t- [when it shows, what users see]

# **Testing**
-
'''

with open(workspace + filename, 'w') as f:
    f.write(content)
```

## Page Structure

```
---
Status: Not started
Created time: YYYY-MM-DDTHH:MM
Latest: [concise one-line summary of the most recent update]
Quarter: YYYY H1 or H2
Type: 🌟 feature
---
# **Latest Update**
[entries only when there are actual updates]

# **What's about**
- [brief description of the task]

# **Reference**
[only include sub-sections that have real content]
- ### Contacts
	- stakeholders / working groups / support channels
- ### Links
	- Jira stories
	- merge requests
	- experiment

# **Implementation Details**
- **Data**: [models, APIs, mappers]
- **Toggle** (if any): [experiment ID]
- **UI / Logic** (if needed): [when it shows, what users see]

# **Testing**
-
```

## Critical Rules

- **Omit empty sections and sub-headers.** Never write a sub-header with no content.
- **No placeholder dates in Latest Update.** Leave `# **Latest Update**` empty if there are no updates yet.
- **Contacts sub-section is usually absent.** Only add when stakeholders are actually known.
- **Use bullets and sub-bullets** so content is easy to scan. Bold action verb as lead, detail indented.

## Interview Pages

**Location:** `Agoda/Interviews/YYYY/`
**Template:** `Agoda/Interviews/Interview Template.md`
**File naming:** `Interview - Candidate Name (YYYY-MM-DD).md`
**Frontmatter:** `Type: 🎙️ interview`, `Status: In progress`, `Quarter: YYYY H1 or H2` (from interview date).
**Scorecard:** Problem solving, Coding efficiency, Communication, Testing, Understanding performance (each /5, total /25).
**After:** Fill Scorecard, write Summary (Excelled in / Struggled with / Conclusion). Update `Latest` frontmatter, set `Status: Done`.

## Frontmatter Reference

| Field | Values |
|-------|--------|
| Status | `Not started`, `In progress`, `Next`, `Done`, `Blocked`, `On hold` |
| Type | `🌟 feature`, `🐛 bug`, `🔧 refactor`, `🧪 experiment`, `🔍 investigation` |
| Quarter | `YYYY H1 or H2` |
| Created time | `YYYY-MM-DDTHH:MM` |
