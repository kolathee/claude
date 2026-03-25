# Daily Note Rules

## Section Order

Correct order of sections in a daily note:

1. Planned Work
2. Unplanned
3. Pending Requests
4. On the Radar
5. Personal

## Sorting Within Sections

**Always put unchecked items above checked items** in every section (Planned Work, Unplanned, On the Radar, Pending Requests). Checked = done; they sink to the bottom.

## No Pending Requests Section

**Pending Requests is merged into Unplanned.** There is no separate Pending Requests section. Anything someone asked Cup to do unexpectedly goes into Unplanned alongside other unplanned work.

Section order (final):
1. Planned Work
2. Unplanned
3. On the Radar
4. Personal

## Unplanned vs On the Radar

- **Unplanned** — anything that was not originally planned for the day, regardless of type (investigation, monitoring, ad-hoc requests, etc.). Used to track the volume of unplanned work handled.
- **On the Radar** — only items where all code is merged and no development is needed. These are lightweight monitoring items (e.g. watching an experiment that's already running, a deployment that's already out, a rollout you're keeping an eye on). If a task still needs coding, investigation, code review, or any active development work, it belongs in **Planned Work**, not On the Radar.

If monitoring was triggered by someone asking you unexpectedly → **Unplanned**, not On the Radar.

## Writing Style

Never use `==highlight==` markup when writing the `latest` property value. Use plain text only.