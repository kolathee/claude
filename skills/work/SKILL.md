---
name: work
description: Router for Obsidian work page operations. Delegates to the appropriate skill. "c" or "create" → work-create-page. "u <topic>" or "update" → work-update-page. "f" or "reformat" → work-reformat-page. Daily note operations → daily-note-create (n), daily-note-end (e), daily-note-track (t), daily-note-sync (u with no topic).
---

# Work — Skill Router

Delegates to the appropriate skill based on the operation:

| Operation | Skill | Triggers |
|-----------|-------|---------|
| Create new page | `work-create-page` | "c", "create", "new task page", "new work page" |
| Update existing page | `work-update-page` | "u \<topic\>", "update", "add last update", "add MR", "mark done" |
| Reformat page | `work-reformat-page` | "f", "reformat", "fix page structure" |
| Create daily note | `work-daily-create` | "n", "new note" |
| End of day | `work-daily-end` | "e", "end of day" |
| Track item | `work-daily-track` | "t", "track" |
| Sync Slack | `work-daily-sync` | "u" (no topic), "sync" |

Use the matching skill directly for best results.

## Quarter & Workspace

**Quarter format:** `YYYY H1 or H2` (first or second half of the year).

Compute Quarter from the current date:
- Jan–Jun → `YYYY H1` (first half)
- Jul–Dec → `YYYY H2` (second half)

Use the current year (e.g. today is 2026-04-22 → `2026 H1`). The workspace folder name matches the Quarter value.

## Workspace Location

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/<Quarter>/
```

**Exception — Interview pages:** Go in a year subfolder under `Interviews/`, not the Quarter workspace:
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/Interviews/YYYY/
```

Template reference:
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/Work Template.md
```

## File Naming Convention

`(FEATURE_CODE) Platform Short Description.md`

Examples:
- `(BWZP) iOS SSR badge.md`
- `Integration DatePicker Fix (native).md`
- `Deintegration Cashback Redemption Nudge.md`

Use `(FEATURE_CODE)` prefix when the task is tied to a specific experiment/feature code. Otherwise use a plain descriptive name.

## Page Structure

New tasks default to `Status: Not started`, `Type: 🌟 feature`, saved into `Backlog/` subfolder.

```
---
Status: Not started
Created time: YYYY-MM-DDTHH:MM
Latest: [concise one-line summary of the most recent update]
Quarter: YYYY H1 or H2
Type: 🌟 feature
---
# **Latest Update**
[entries only when there are actual updates — see below]

# **What's about**
- [brief description of the task]

[optional: embed image if available]

# **Reference**
[only include sub-sections that have real content]
- ### Contacts
	- stakeholders
		- [name / role]
	- working groups
		- [group]
	- support channels
		- [channel]
- ### Links
	- Jira stories
		- [PAYFLEX-XXX](https://...)
	- merge requests
		- [MR title](https://...)
	- experiment
		- EXPERIMENT-ID-IOS

# **Implementation Details**
- **Data**:
	- [models, APIs, mappers]
- **Toggle** (if any):
	- [experiment ID]
- **UI / Logic** (if needed):
	- [when it shows, what users see]

# **Testing**
-
```

## Critical Rules

**Omit empty sections and sub-headers.** Never include a sub-header (Contacts, working groups, support channels, etc.) if there is no real content. An empty placeholder is worse than nothing.

**No placeholder dates in Latest Update.** Only add a `📄 [[YYYY-MM-DD]]` entry when there is an actual note to record. Leave `# **Latest Update**` empty if there are no updates yet.

**Contacts sub-section is usually absent.** Most task pages only have `### Links`. Only add `### Contacts` when stakeholders/working groups/support channels are actually known.

**Use bullets and sub-bullets so content is easy to scan.** Prefer a **bold action verb or label** as the lead bullet, then indent the detail as a sub-bullet.

Latest Update example:
- 📄 [[2026-03-16]]
	- **Switched**
		- `BWZP badge` to `CMS 560056` and added `room currency` in the placeholder.
	- **Fixed**
		- `payLaterOptions` GraphQL query — was `[Int]`, actually `[DFPayLaterOption]`.
	- **==Follow up==**
		- tomorrow: ask BE about the data model.

Implementation Details example:
- **Data**:
	- `payLaterOptions: [DFPayLaterOption]?` on `DFPayLater`, each with `code: String?` (GraphQL enum: `"BWZP"`).
- **Toggle**:
	- `PaymentLocalisationToggles.bookWithZeroPay` (`PAYFLEX-233-IOS`).

**Latest date on top, new bullets at bottom.** When adding a new date, insert it above older dates. When adding bullets under an existing date, append below existing bullets.

**Don't check off a task until it's fully done.** Daily progress goes in description sub-bullets — checkbox stays unchecked until finished.

**Latest Update is a history log — never trim it.** Keep full detail even if the approach was superseded. Implementation Details, Testing, Reference should only reflect the final working approach.

## Interview Pages

Interview notes live in:
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/Interviews/YYYY/
```

**Template:** `Agoda/Interviews/Interview Template.md`

**File naming:** `Interview - Candidate Name (YYYY-MM-DD).md`

**Frontmatter defaults:** `Type: 🎙️ interview`, `Status: In progress` (→ `Done` after), `Quarter: YYYY H1 or H2` (computed from interview date).

**Scorecard sections:** Problem solving, Coding efficiency, Communication, Testing, Understanding performance (each /5, total /25).

**After interview:** Fill Scorecard table, then write Summary (Excelled in / Struggled with / Conclusion with Recommendation + Pros + Cons). Update `Latest` frontmatter and set `Status: Done`.

## Workflow

### Creating a new work page (shorthand: "c")

**Type inference from title/content — always check before defaulting to feature:**
- "Investigation", "Investigate", "Debug", "Root cause" → `🔍 investigation`
- "Experiment", "Exp", "A/B", "Launch", "Allocation bias" → `🧪 experiment`
- "Bug", "Fix", "Issue", "Error" → `🐛 bug`
- "Refactor", "Cleanup", "Migration", "Migrate" → `🔧 refactor`
- Otherwise → `🌟 feature`

1. **Search first.** Run `find` across the entire `Agoda/<Quarter>/` tree (including all subfolders) for any file whose name contains key words from the task. If a match is found, open it instead.
2. Ask for missing details: task name, Jira ticket, MR link, experiment ID, type, brief description.
3. Determine the file name from the task context.
4. Write the file using `python3` (required for special characters in filenames):

```python
import datetime

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

### Updating an existing work page (shorthand: "u \<topic\>")

1. **Find the page** — search `Agoda/<Quarter>/` (and subfolders) for a file matching the topic keywords. Open it.
2. **Auto-fetch Slack threads** — scan the page for Slack URLs in format `https://agoda.slack.com/archives/{channel_id}/p{ts}`. For each one, call `mcp__plugin_productivity_slack__slack_read_thread` with the extracted `channel_id` and `message_ts` (strip leading `p`, insert `.` after 10th digit). Fetch all threads in parallel.
3. **Summarise what's new** — identify most recent messages since the last Latest Update entry date.
4. **Ask the user what to update** — present a one-line summary of what's new, then ask what to record (or proceed directly if already told).

**Adding a Latest Update entry** (most common update):
```python
workspace = '/Users/kpayuhawatta/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/2026 H1/'
filename = '(BWZP) iOS SSR badge.md'

with open(workspace + filename, 'r') as f:
    content = f.read()

new_entry = '- 📄 [[YYYY-MM-DD]]\n\t- [update note here]\n'
content = content.replace('# **Latest Update**\n', f'# **Latest Update**\n{new_entry}')

with open(workspace + filename, 'w') as f:
    f.write(content)
```

**Updating status** (e.g., to Done): Find `Status: In progress` in frontmatter and replace with `Status: Done`.

**When status is set to Done — move page to `Done/` folder:**
```python
import shutil

workspace = '/Users/kpayuhawatta/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/2026 H1/'
filename = '(BWZP) iOS SSR badge.md'

shutil.move(workspace + filename, workspace + 'Done/' + filename)
```

**Adding a link** (MR, Jira, etc.): Locate the relevant sub-section under `### Links` and append the new item.

**Always update `Latest` frontmatter** whenever adding a new Latest Update entry — concise one-line summary. Never use `==highlight==` in the `Latest` frontmatter — plain text only.

**Direction-change check:** When a Latest Update changes the approach, repo, owner, or requirements, scan **all** other sections for stale content:
- **What's about** → still accurate?
- **Implementation Details** → mark superseded content as "Previous approach (superseded)"
- **Testing** → still matches current approach?
- **Reference → Links** → add a note if something is no longer the approach

**Sync to today's daily note (MANDATORY):** After updating the work page, ALWAYS update today's daily note. Check for any bullet referencing the same page (via wikilink `[[Page name]]` or Jira ticket):
- **If a reference exists:** add a sub-bullet under the task summarising the update. In Planned Work, always linkify MR numbers and Jira tickets.
- **If no reference exists:** add a new bullet in the appropriate section (Planned Work if active, On the Radar if monitoring-only).

**Re-sort after status changes to waiting:** If the update makes a task waiting/non-actionable, move it to the bottom of its section in today's note.

**Bidirectional sync rule:** When updating the daily note for a task (checking it off, adding detail, changing status), also update the work page. Never update one without the other.

### Reformatting an existing work page (shorthand: "f")

Use when a page exists but lacks standard structure (no frontmatter, bare lists, etc.).

1. Read the existing file with `python3`.
2. Identify the content type — determine appropriate `Type`.
3. Preserve all existing content — map into correct sections. If content doesn't fit standard sections, keep as named `# **Section**` headings after `# **What's about**`.
4. Add frontmatter with `Created time` set to today, `Status: In progress`.
5. Add `# **Latest Update**` (empty) and `# **What's about**` with a one-line description inferred from the content.
6. Write the reformatted file back.

```python
workspace = '/Users/kpayuhawatta/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/2026 H1/'
filename = 'Pending Int + Deint.md'

with open(workspace + filename, 'r') as f:
    existing = f.read()

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

### Reading an existing work page

Use `python3` to read (avoids shell quoting issues with special characters):
```python
with open(workspace + filename, 'r') as f:
    print(f.read())
```

## Frontmatter Reference

| Field | Values |
|-------|--------|
| Status | `Not started`, `In progress`, `Next`, `Done`, `Blocked`, `On hold` |
| Type | `🌟 feature`, `🐛 bug`, `🔧 refactor`, `🧪 experiment`, `🔍 investigation` |
| Quarter | `YYYY H1 or H2` |
| Created time | `YYYY-MM-DDTHH:MM` |
