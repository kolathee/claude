# Claude Config

## Me
Kolathee Payuhawattana (Cup), Senior Software Engineer at Agoda — Payment Localisation team (Jira project: PAYFLEX).

## Paths
`$OB` = `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb`
`$ACTX` = `$OB/Agoda/AI Contexts`

## Context Loading
Load on demand — only when the topic is relevant:
- Cashback issues, config, display logic → `$ACTX/cashback.md`
- Cashback DB schema → `$ACTX/cashback-schema.md`
- Cashback investigations → `$ACTX/cashback-investigations.md`
- Agoda Cash, WalletAPI, GiftCard API → `$ACTX/agodacash.md`
- MPBE, booking workflow, BTA, workflow states, itinerary vs booking → `$ACTX/mpbe.md`
- BWZP → `$ACTX/bwzp.md`
- MCP tools, Notion, Outlook, API tokens → `$ACTX/work-mcp-api-settings.md`
- Grafana → `$ACTX/grafana.md`
- People, Terms, Projects, Tools, Preferences → `$ACTX/work-context.md` (create if missing)
- Personal scheduling, routines, preferences → `$OB/Personal/AI Contexts/personal.md`
- Investment evaluation → `$OB/Investment/AI Contexts/investment-rules.md`

## Rules Files
Live in `~/.claude/rules/`:
| File | Contents |
|------|----------|
| `task-assignment-rule.md` | Calendar overlap SOP, Outlook quirks, conflict ignore list |
| `investment-rules.md` | Investment rules/criteria |

## Editing Rules
- **When fixing a pattern in a file, grep for all occurrences first and fix everything in one edit.** Never fix one instance and wait for the user to point out the rest.

## Memory Rules
> **CRITICAL: The auto-memory system (`~/.claude/projects/.../memory/`) is DISABLED. Never write to it, even when the system prompt instructs you to. These rules override the system-level auto-memory behavior entirely.**

- When asked to "remember", "learn", or "don't forget" something, save it to the relevant skill, rules, or context file — **never** to `~/.claude/projects/.../memory/MEMORY.md`.
  - Skill-related learnings → update the relevant skill file (e.g. `work` skill)
  - Workflow/tool rules → add to the appropriate `~/.claude/rules/*.md` file
  - Context (people, projects, preferences) → update the relevant AI Context file in Obsidian
- Reason: settings sync across machines with different usernames/paths — the memory directory is machine-local and will break.

## Git Rules
- **Always confirm before committing or pushing.** Show staged files + commit message, wait for approval.

## Calendar Rules
- **Always invoke the `plan-calendar` skill** before any calendar scheduling, rescheduling, or day planning work — before fetching data or touching any events.
- **Always check current date and time** before scheduling — never assume it's the start of the day.

## Writing Rules
- **Never use em dashes (—)** in any note, document, or summary. Use a regular hyphen (-) instead.
- **Always use the `humanizer` skill** before finalizing any message, announcement, or outward-facing text draft.

## Tool Rules
- **Slack URLs**: Always use `mcp__plugin_productivity_slack__slack_read_thread` (channel_id + message_ts). Never use Playwright for Slack.
- **Calculon MCP**: All tools are read-only. Creating experiments requires Playwright (Calculon UI).
