---
name: note
description: Save learnings from the current conversation to the appropriate context file in the Obsidian CupOb vault. Use after resolving an issue, answering a domain question, or exploring a system — any time knowledge was discovered, updated, or expanded that would help in future sessions.
---

# /note

Extract new knowledge from this conversation and save it to the right context file so it builds up over time.

## Context Files

| File | What goes here |
|------|----------------|
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Personal/contexts/personal.md` | Personal preferences, routines, scheduling rules |
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/contexts/cashback.md` | Cashback domain — components, config, versions, gotchas, business rules |
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/contexts/agodacash.md` | Agoda Cash domain — BWZP, WalletAPI, earn/burn rules |
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/contexts/mcp-settings.md` | MCP tool names, Notion auth, Outlook config, report templates |
| `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/contexts/grafana.md` | Grafana queries, Loki/LogQL patterns, datasource UIDs, monitoring gotchas |

## Steps

1. **Scan the conversation** for new, durable facts worth keeping:
   - How-to steps, processes, and workflows
   - Tools, commands, APIs, config locations, and their quirks
   - Key concepts, terminology, and domain rules
   - Contacts, roles, and team structure
   - Gotchas, non-obvious behaviors, known bugs or limitations
   - Investment principles, strategies, or frameworks
   - Personal routines, preferences, or life decisions
   - Solutions to recurring problems
   - **Links and resources**: Confluence pages, Slack channels, Metabase dashboards, Jira tickets, GitLab repos, runbooks — any URL that was useful for resolving or understanding something

2. **Skip** anything that's session-specific, temporary, or unconfirmed speculation.

3. **Pick the right file** — match each piece of knowledge to the most relevant context file. Split across files if it spans domains. If the knowledge doesn't fit any existing file, create a new context file in the appropriate CupOb subfolder (e.g. `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/contexts/new-topic.md`) and add it to the table above.

4. **Read the target file** first, then update it:
   - Add new knowledge under the right section
   - Update or expand existing entries if this conversation adds more detail or corrects something
   - Never duplicate — update in place
   - Keep it concise (bullets and tables over paragraphs)
   - **Include links** inline with the relevant entry (e.g. Confluence page, Slack channel ID, Metabase dashboard, GitLab path) so they're easy to reference later

5. **Confirm** briefly: tell the user what was saved, updated, or created and where.
