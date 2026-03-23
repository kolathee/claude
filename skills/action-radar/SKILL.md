---
name: action-radar
description: This skill should be used when the user asks to "scan my daily note", "what do I need to do today", "show my actions for today", "review my daily note", "what's on my list today", "action radar", "give me an action table from my note", or "what can I act on". Reads today's Obsidian daily note, extracts all unchecked tasks, and produces a structured action table with topics, suggested follow-up messages, and direct links to where action should be taken (Slack threads, Jira tickets, or people).
version: 0.1.0
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

### 3. Build the Action Table

Produce a Markdown table with these columns:

| # | Topic | Action Verb | Suggested Message / Action | Where to Act |
|---|-------|-------------|---------------------------|--------------|

**Column definitions:**

- **#** — sequence number
- **Topic** — short label inferred from the task title (e.g. "Experiment PAYFLEX-371", "AgodaCash Refund — 27 Bookings", "Kill Switch System Design")
- **Action Verb** — the `==Verb==` annotation if present; otherwise infer from context (Ask, Share, Check, Prepare, Test, Follow up, etc.)
- **Suggested Message / Action** — 1–3 ready-to-send sentences Cup can use verbatim or lightly edit. Write in first person. Match the tone to the verb:
  - **Ask** → a question directed at the relevant team/person
  - **Share** → a brief update summarising findings or next steps
  - **Check** → a short note about what to look at and what decision to make after
  - **Prepare** → a framing sentence for starting the work
  - **Test / Help** → a coordination message to align with the counterpart
  - **Waiting** → a polite follow-up nudge
- **Where to Act** — extract the most actionable link from the item's sub-bullets, in priority order:
  1. Slack thread URL → render as `[💬 Thread](url)`
  2. Slack channel mention (e.g. `#channel-name`) → render as `[#channel-name](slack://channel?...)`; if no deep link is available, just name the channel
  3. Jira ticket → render as `[🎫 TICKET-ID](url)`
  4. Calculon experiment → render as `[🧪 Experiment](url)`
  5. Obsidian wikilink (`[[Note Name]]`) → render as a clickable deep link: `[📄 Note Name](obsidian://open?vault=CupOb&file=NOTE_NAME_URL_ENCODED)`. URL-encode spaces as `%20`. Use when the action is doc-based (Prepare, Write, Draft).
  6. Person name → render as `@Name`
  7. If multiple links exist, show the most direct one first

### 4. Notes Section

After the table, add a short **Notes** section:

- List any items that have `==Waiting==` status separately with a nudge message
- Flag items with no links/context (cannot determine where to act)
- Mention total count: "X unchecked items found across all sections"

## Output Format

```markdown
## 📋 Action Table — [Date]

| # | Topic | Action | Suggested Message | Where to Act |
|---|-------|--------|------------------|--------------|
| 1 | ... | Ask | "Hi team, ..." | [💬 Thread](url) |
...

---
### ⏳ Waiting Items
...

### ℹ️ Notes
- X unchecked items found
- Items without links: ...
```

## Handling Special Cases

**Calculon experiments** — topic should include the experiment name/ID; suggested message should mention checking metrics or asking PO for status update.

**Items with no action annotation** — infer verb from context. "Help Sangit test" → verb is "Coordinate"; suggested message is a Slack DM to Sangit.

**Items referencing Obsidian notes** (`[[Note Name]]`) — include the wikilink in "Where to Act" when the primary action is doc-based (e.g. Prepare, Write, Draft). Render as `📄 [[Note Name]]`. For communication-first actions (Ask, Share), prefer Slack/Jira links over the wikilink.

**Waiting items** — suggest a polite follow-up message to the relevant PO, team, or person asking for a status update.
