---
name: work-daily-track
description: Quickly capture something into today's daily note — from a Slack thread, image, or description. Use when the user says "t", "track", "add to today", "capture this", "log this", or pastes a Slack link or screenshot to add to the note. Infers the right section (Unplanned, On the Radar, Personal) without asking.
---

# Daily Note — Track (t)

**Quickly capture something to act on or monitor** from a Slack thread, image, or description. If the content clearly relates to an existing work page, add a Latest Update entry there and sync to today's note. Otherwise add a checkbox bullet to the correct section in today's note.

## Paths

- **Daily note folder:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Daily Note/`
- **Work board:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/<Quarter>/`

## Workflow

1. **Read the input.** Slack link, image screenshot, or user description. Extract: what it is, who's involved, what action (if any) is needed.

2. **Draft the bullet** using the universal format:
   ```
   - [ ] **Short title**
   	- context / detail
   	- [💬 Slack thread](https://...)
   ```

3. **Determine the section** based on context:
   - **Unplanned** — something that already happened today and took time
   - **On the Radar** — code fully merged, no dev needed; just monitoring (experiment running, deployment out, scheduled maintenance). Always prefix title with `==(Monitoring)==`. If the task still needs coding, investigation, or code review → Planned Work instead. **Before adding here, check all other sections.** If the item already exists anywhere in the note, update that bullet in place.
   - **Personal** — non-work item (events, appointments, errands). For events with a physical location, include a Google Maps search link: `[Venue Name](https://www.google.com/maps/search/?api=1&query=Venue+Name+City)`. For events with a time, include it in the title (e.g. `Event Name 🎟️ 18:00 – 22:00`).

   > Note: "Pending Requests" no longer exists as a separate section — anything someone unexpectedly asked Cup to do goes into **Unplanned**.

4. **Write immediately** — no confirmation needed. Append the bullet to the correct section using `python3`. Replace the placeholder (`- \n` or `- [ ] \n`) if the section is still empty, otherwise append after the last bullet in that section.

5. **Report back** with the bullet added and which section it went into.

## Rules

- **No duplicates.** If the item already exists in any section, update in place.
- **Actionable items at top, waiting/non-actionable at bottom** within each section.
- **Highlight action verbs** with `==verb==`.
- **Bidirectional sync** — if this relates to an existing work page, also add a Latest Update entry on the work page and update `Latest` frontmatter.
