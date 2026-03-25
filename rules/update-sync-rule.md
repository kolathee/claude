# Update Sync Rule

## Rule

Whenever new information comes in (Slack thread update, query result, user confirms something is resolved, etc.), **always check and update all related pages before responding**.

## What to check

1. **Work/investigation page** (in `Agoda/<Quarter>/` or `Reference/`)
   - Add a `Latest Update` entry under the relevant date
   - Update the `Latest` frontmatter property with a concise one-line summary of the new status
   - Update `Status` frontmatter if the task is now done/resolved

2. **Today's daily note** (`Daily Note/YYYY-MM-DD.md`)
   - Find any bullet that references the same page (via wikilink `[[Page name]]`, Jira ticket, or topic keyword)
   - Update the sub-bullet to reflect the latest state
   - If the update makes the item resolved/waiting/no longer actionable, re-sort it within its section (completed items or waiting items sink to the bottom)

## Triggers

- Reading a new Slack message or thread reply
- Running a query and getting a result
- User tells you something is resolved, blocked, or has a new finding
- Any conversation where status changes (e.g. "it's fixed", "Art confirmed", "still waiting")

## Priority order

Always update in this order:
1. Work page `Latest` frontmatter (one-liner, plain text, no `==highlight==`)
2. Work page `Latest Update` section (detailed entry under today's date)
3. Daily note bullet (concise sync, link any MRs or tickets)

Never skip step 1 - the `Latest` property is what Cup sees first when scanning work pages.
