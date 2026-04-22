---
name: work-update-page
description: Update an existing Obsidian work page — add a Latest Update entry, change status, add MR/Jira links, or log any progress. Use when the user says "update work page", "log update", "add last update", "add MR", "add Jira", "mark as done", "u <topic>", or describes progress on an existing task.
---

# Work Page — Update

Update an existing Obsidian task page in the Agoda Workspace folder.

## Paths

- **Workspace:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/<Quarter>/`
- **Done folder:** `<workspace>Done/`
- **Daily note folder:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Daily Note/`

## Quarter Computation

- Jan–Jun → `YYYY H1`
- Jul–Dec → `YYYY H2`

## Workflow

1. **Find the page.** Search `Agoda/<Quarter>/` (and all subfolders) for a file matching the topic keywords. Open it with `python3`.

2. **Auto-fetch Slack threads.** Scan the entire page for Slack URLs in format `https://agoda.slack.com/archives/{channel_id}/p{ts}`. For each one, call `mcp__plugin_productivity_slack__slack_read_thread` with the extracted `channel_id` and `message_ts` (strip leading `p`, insert `.` after 10th digit). Fetch all threads in parallel.

3. **Summarise what's new.** Identify most recent messages since the last Latest Update entry date. Note decisions, replies, blockers, action items.

4. **Ask the user what to update** — present a one-line summary of what's new in each thread, then ask what to record (or proceed directly if already told).

## Common Operations

### Adding a Latest Update entry (most common)

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

### Updating status to Done

Find `Status: In progress` in frontmatter, replace with `Status: Done`, then move the file:

```python
import shutil

workspace = '/Users/kpayuhawatta/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/2026 H1/'
filename = '(BWZP) iOS SSR badge.md'

shutil.move(workspace + filename, workspace + 'Done/' + filename)
```

### Adding a link (MR, Jira, etc.)

Locate the relevant sub-section under `### Links` and append the new item.

## Rules

**Always update `Latest` frontmatter** whenever adding a Latest Update entry — concise one-line summary. Never use `==highlight==` in `Latest` frontmatter — plain text only.

**Latest date on top, new bullets at bottom.** Insert new date entries above older dates. Append new bullets under an existing date below existing ones.

**Latest Update is a history log — never trim it.** Keep full detail even if the approach was superseded. Other sections (Implementation Details, Testing, Reference) should only reflect the final working approach.

**Direction-change check.** When a Latest Update changes the approach, repo, owner, or requirements, scan **all** other sections for stale content before finishing:
- **What's about** → still accurate?
- **Implementation Details** → mark superseded content as "Previous approach (superseded)"
- **Testing** → still matches current approach?
- **Reference → Links** → add a note if something is no longer the approach

**Add all provided references.** Any URLs or references provided as input (Slack threads, Jira tickets, MRs, docs, etc.) that are relevant to the task must be added under `### Links` in the work page.

**Sync to today's daily note (MANDATORY).** After updating the work page, ALWAYS update today's daily note. Check for any bullet referencing the same page (via wikilink `[[Page name]]` or Jira ticket):
- **If a reference exists:** add a concise sub-bullet (1-2 lines max) summarising the update. Always linkify MR numbers and Jira tickets.
- **If no reference exists:** add a new bullet in the appropriate section (Planned Work if active, On the Radar if monitoring-only).

**Re-sort after status changes to waiting.** If the update makes a task waiting/non-actionable, move it to the bottom of its section in today's note.

**Bidirectional sync rule.** When updating the daily note for a task, also update the work page. Never update one without the other.

## Reading a work page

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
