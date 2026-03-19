# Memory

## Context Files

Live in `~/.claude/contexts/`:

| File | Contents |
|------|----------|
| `personal.md` | Full personal profile — routines, scheduling rules, workout cycle, investments, preferences |
| `work-cashback.md` | Cashback domain — components, architecture, scripts, gotchas |
| `work-cashback-schema.md` | bi_cashback StarRocks DB — full table & column reference (all 7 categories, relationships, enum values) |
| `work-agodacash.md` | Agoda Cash domain — components, BWZP, business rules, gotchas |
| `work-mcp-settings.md` | MCP tool names, Notion auth, Outlook config, report template paths |

## Rules Files

Live in `~/.claude/rules/`:

| File | Contents |
|------|----------|
| `task-assignment-rule.md` | Calendar overlap SOP, Outlook quirks, conflict ignore list |
| `investment-rules.md` | Concise investment rules/criteria extracted from books, tagged by source. Used by investment evaluator skill. |
| `calendar-rule.md` | Always check calendar availability before creating any event. If conflict, ask user — suggest options (move existing, reschedule new, override). |

## Tool Rules

- **Slack URLs**: Always use `mcp__plugin_productivity_slack__slack_read_thread` (channel_id + message_ts from URL) to fetch Slack message content. Never use Playwright browser for Slack.
- **Calculon MCP**: All 10 tools are read-only (search, get details, check status, etc.). Creating experiments requires Playwright (Calculon UI).
