---
name: action-radar
description: This skill should be used when the user asks to "scan my daily note", "what do I need to do today", "show my actions for today", "review my daily note", "what's on my list today", "action radar", "give me an action table from my note", or "what can I act on". Supports an F/Fetch mode (triggered by appending "F", "f", "fetch", or "-f") that syncs the latest Slack thread replies for each item before building the table. Reads today's Obsidian daily note, extracts all unchecked tasks, and produces a structured action table with topics, suggested follow-up messages, and direct links to where action should be taken (Slack threads, Jira tickets, or people).
---

# Action Radar

Read today's Obsidian daily note, extract all unchecked tasks, and produce an **Action Table** that tells Cup exactly what to do and where to do it.

## Daily Note Location

Today's note lives at:
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Daily Note/YYYY-MM-DD.md
```

Always derive the filename from today's date (`currentDate` in system context).

## Step-by-Step Process

### 1. Read the Daily Note

Read the full file. Do not skip any section — scan **all sections** (Planned Work, Unplanned, On the Radar, etc.).

### 2. Extract Unchecked Items

Collect every line that starts with `- [ ]`. These are the pending actions.

For each item, also collect:
- Sub-bullet context (indented lines beneath it)
- The `==Action==` annotation (e.g., `==Ask==`, `==Share==`, `==Check==`, `==Prepare==`) — this is the intended verb
- Any embedded links: Slack thread URLs, Jira ticket URLs, Calculon experiment URLs, Obsidian note wikilinks

### 2.5. Enrich Missing Contact Sources with Glean

For any item where the **"Where to Act"** is unclear or missing (no Slack URL, no channel name, no person link), use **Glean MCP** (`mcp__plugin_agoda-skills_glean__search`) to find the most accurate contact point:

- Search for the Slack channel: e.g. `"#ceg-wizard-flow slack channel"` or `"<team name> slack channel"`
- Search for the person: e.g. `"Sangit Agoda"` to find their Slack handle or team
- Search for the Jira project or team: e.g. `"PAYFLEX-352 owner"` or `"FMS team Agoda"`

Use the Glean results to fill in the **Where to Act** column with the most direct contact source found.

Only call Glean for items that genuinely lack a contact source — do not call it for items that already have a Slack URL or clear channel link.

### 3. Build the Action Table

Produce a **single Markdown table** covering all unchecked items — active, waiting, and on the radar — all in one place. Do not split into separate tables or sections. Add a **Status** column so Cup can tell at a glance what state each item is in.

| # | Status | Topic | Action | Suggested Message / Action | Where to Act |
|---|--------|-------|--------|---------------------------|--------------|

**Column definitions:**

- **#** — sequence number
- **Status** — one of: `Active`, `Waiting`, `Monitoring`
  - `Active` — something Cup can act on right now
  - `Waiting` — blocked on someone else; suggest a nudge message
  - `Monitoring` — experiment or deployment to keep an eye on
- **Topic** — short label inferred from the task title (e.g. "Experiment PAYFLEX-371", "AgodaCash Refund - 27 Bookings", "Kill Switch System Design")
- **Action** — the `==Verb==` annotation if present; otherwise infer from context (Ask, Share, Check, Prepare, Follow up, Monitor, etc.)
- **Suggested Message / Action** — 1-3 ready-to-send sentences Cup can use verbatim or lightly edit. Write in first person. Match the tone to the verb:
  - **Ask** → a question directed at the relevant team/person
  - **Share** → a brief update summarising findings or next steps
  - **Check / Prepare** → a framing sentence for starting the work
  - **Waiting** → a polite follow-up nudge to whoever is blocking
  - **Monitor** → what metric or signal to check
- **Where to Act** — extract the most actionable link from the item's sub-bullets, in priority order:
  1. Slack thread URL → render as `[💬 Thread](url)`
  2. Slack channel mention → just name the channel
  3. Jira ticket → render as `[🎫 TICKET-ID](url)`
  4. Calculon experiment → render as `[🧪 Experiment](url)`
  5. Obsidian wikilink → render as `[📄 Note Name](obsidian://open?vault=CupOb&file=NOTE_NAME_URL_ENCODED)`. Use when the action is doc-based (Prepare, Write, Draft).
  6. Person name → render as `@Name`
  7. If multiple links exist, show the most direct one first

### 4. Notes Section

After the table, add a brief **Notes** line only if needed:
- Flag items with no links/context (cannot determine where to act)
- Mention total count: "X unchecked items found across all sections"

## Output Format

```markdown
## Action Table - [Date]

| # | Status | Topic | Action | Suggested Message | Where to Act |
|---|--------|-------|--------|------------------|--------------|
| 1 | Active | ... | Share | "Hi team, ..." | [💬 Thread](url) |
| 2 | Waiting | ... | Follow up | "Just checking in on..." | [💬 Thread](url) |
| 3 | Monitoring | ... | Monitor | Check metrics in Calculon | [🧪 Experiment](url) |

---
### Notes
- X unchecked items found
```

## Modes

### Default Mode (no flag)

Run the full step-by-step process above: read daily note → extract unchecked items → enrich with Glean → build the Action Table.

---

### F Mode (Fetch Mode)

**Trigger:** User appends `F`, `f`, `fetch`, or `-f` to the invocation (e.g. "action radar F", "action radar fetch", "/action-radar -f").

**Purpose:** Same as Default Mode, but **before building the table**, proactively fetch fresh information from Slack for every ongoing item that has a Slack thread URL. This surfaces what's new since the last check, so the "Suggested Message / Action" and Status columns reflect the latest state.

#### F Mode Extra Steps (insert between Step 2 and Step 2.5)

**Step 2F. Fetch Latest Slack Context**

For each unchecked item that contains one or more Slack thread URLs:

1. Call `mcp__plugin_productivity_slack__slack_read_thread` with the `channel_id` and `message_ts` extracted from the URL.
   - Slack URL format: `https://agoda.slack.com/archives/{channel_id}/p{message_ts_no_dot}` — strip the leading `p` and insert a `.` after the 10th digit to reconstruct the `ts`.
2. Read the fetched thread. Look for:
   - Any new replies since the last time Cup acted
   - Decisions made, approvals given, blockers resolved, or new blockers raised
   - Names of people who replied (for attribution in the suggested message)
3. Summarise what's new as a one-liner per item (used in step 3).

If a thread returns no new messages → note "No new activity" for that item.

If an item has no Slack URL → skip fetch for that item; proceed with daily note context only.

#### F Mode Adjustments to the Action Table

After fetching, update each row with the latest context:

- **Status** — re-evaluate based on fetched content:
  - If someone replied asking for input → `Active`
  - If the item is still waiting on someone with no reply → `Waiting`
  - If an experiment/deployment is still running with no decision → `Monitoring`
- **Suggested Message / Action** — incorporate what's new:
  - Reference the latest reply if relevant (e.g. "Since [Name] said X, I should…")
  - If no new activity, keep the default nudge but note "(no new activity)"
- Add a **Latest Update** column to the table (rightmost, after "Where to Act"):

| # | Status | Topic | Action | Suggested Message | Where to Act | Latest Update |
|---|--------|-------|--------|------------------|--------------|---------------|

- **Latest Update** — one-line summary of the most recent Slack activity (or "No new activity").

#### F Mode Output Header

Replace the table header with:

```markdown
## Action Table (Fetch Mode) - [Date]
_Slack threads synced at [current time]_
```

---

## Handling Special Cases

**Calculon experiments** — topic should include the experiment name/ID; suggested message should mention checking metrics or asking PO for status update.

**Items with no action annotation** — infer verb from context. "Help Sangit test" → verb is "Coordinate"; suggested message is a Slack DM to Sangit.

**Items referencing Obsidian notes** (`[[Note Name]]`) — include the wikilink in "Where to Act" when the primary action is doc-based (e.g. Prepare, Write, Draft). Render as `📄 [[Note Name]]`. For communication-first actions (Ask, Share), prefer Slack/Jira links over the wikilink.

**Waiting items** — set Status to `Waiting`, Action to `Follow up`, and write a polite nudge message directed at whoever is blocking. Include in the main table, not a separate section.
