# Claude Config

## Me
Kolathee Payuhawattana (Cup), Senior Software Engineer at Agoda — Payment Flexibility (PAYFLEX) team.

## Context Loading
Load on demand — only when the topic is relevant:
- Cashback issues, config, display logic → `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/AI Contexts/cashback.md`
- Cashback DB schema → `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/AI Contexts/cashback-schema.md`
- Cashback investigations → `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/AI Contexts/cashback-investigations.md`
- Agoda Cash, WalletAPI → `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/AI Contexts/agodacash.md`
- BWZP → `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/AI Contexts/bwzp.md`
- MCP tools, Notion, Outlook, API tokens → `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/AI Contexts/work-mcp-api-settings.md`
- Grafana → `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/AI Contexts/grafana.md`
- People, Terms, Projects, Tools, Preferences → `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/AI Contexts/work-context.md` (create if missing)
- Personal scheduling, routines → `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Personal/AI Contexts/personal.md`
- Investment evaluation → `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Investment/contexts/investment-rules.md`

## Rules Files
Live in `~/.claude/rules/`:
| File | Contents |
|------|----------|
| `task-assignment-rule.md` | Calendar overlap SOP, Outlook quirks, conflict ignore list |
| `investment-rules.md` | Investment rules/criteria |
| `calendar-rule.md` | Always check availability before creating calendar events |

## Git Rules
- **Always confirm before committing or pushing.** Show staged files + commit message, wait for approval.

## Tool Rules
- **Slack URLs**: Always use `mcp__plugin_productivity_slack__slack_read_thread` (channel_id + message_ts). Never use Playwright for Slack.
- **Calculon MCP**: All tools are read-only. Creating experiments requires Playwright (Calculon UI).
