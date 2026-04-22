---
name: work-daily-sync
description: Sync all tasks in today's daily note from Slack — fetch every Slack thread linked in the note, find what's new, and update both the daily note bullets and their linked work pages in one pass. Use when the user says "u" (with no topic), "sync", "sync today", "update all", or "check slack updates".
---

# Daily Note — Sync All (u)

**Read today's daily note, fetch every linked Slack thread, and update both the daily note and linked work pages in one pass.** No manual link pasting needed.

## Paths

- **Daily note folder:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Daily Note/`
- **Work board:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/<Quarter>/`
- **Quarter:** Jan–Jun → `YYYY H1`, Jul–Dec → `YYYY H2`

## Workflow

1. **Get today's date.** Run `date +%Y-%m-%d`. Open today's daily note at `Daily Note/YYYY-MM-DD.md`.

2. **Collect all tasks.** Scan every section (Planned Work, Unplanned, On the Radar) for **all** task bullets — both unchecked `- [ ]` and checked `- [x]`. For each one collect:
   - Task title
   - All sub-bullets (description, links, wiki-links)
   - Any Slack URLs in format `https://agoda.slack.com/archives/{channel_id}/p{ts}`
   - Any `📄 [[Page name]]` wiki-links (points to a work page)

3. **Fetch all Slack threads in parallel.** For every Slack URL found across all tasks, call `mcp__plugin_productivity_slack__slack_read_thread` (extract `channel_id` and `message_ts`: strip leading `p`, insert `.` after 10th digit). Fire all fetches at the same time.

4. **Determine what's new per task.** For each task with a linked work page (`📄 [[Page]]`), find the date of the last `📄 [[YYYY-MM-DD]]` entry in the work page's Latest Update section. Treat any Slack messages after that date as "new". For tasks with no work page, compare against yesterday's date.

5. **Update each task** that has new Slack activity:

   **If task has a linked work page:**
   - Add a `📄 [[today]]` Latest Update entry on the work page summarising what's new (decisions, replies, blockers, action items)
   - Update the `Latest` frontmatter with a one-line summary
   - Update the description sub-bullet on the daily note to reflect the latest state

   **If no work page exists:**
   - Update the description sub-bullet on the daily note only

   **If no new Slack activity** — leave both unchanged. Note it in the summary.

6. **Re-sort if needed.** After updates, if any task's status changed to waiting/blocked, move it to the bottom of its section (below actionable items).

7. **Report back** with a summary table:

   | Task | New activity | Updated |
   |------|-------------|---------|
   | (BWZP) Block SecureLink | Lalit replied — scope confirmed | Work page + daily note |
   | Re-review MR!499 | No new activity | - |
   | Kill switch FMS | Harshit asked for config example | Work page + daily note |

   List tasks with no Slack URL as "No Slack thread — skipped".

## Rules

- **Bidirectional sync** — never update one without the other. Work page and daily note must always reflect the same state.
- **Never use `==highlight==` markup in the `Latest` frontmatter** — plain text only.
- **Actionable items at top, waiting/blocked at bottom** after re-sort.
