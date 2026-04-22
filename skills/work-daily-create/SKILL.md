---
name: work-daily-create
description: Create today's daily note in Obsidian. Use when the user says "n", "new note", "create daily note", "start today's note", or "morning note". Handles weekday vs weekend, carry-forward from previous note, archiving old notes, and Monday special items.
---

# Daily Note — Create (n)

Create a **new daily note for today** under the Daily Note folder.

## Paths

- **Daily note folder:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Daily Note/`
- **Daily template:** `Daily Note/Archive/Daily Template.md`
- **Work board:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/<Quarter>/`
- **File naming:** `YYYY-MM-DD.md`

## Quarter Computation

- Jan–Jun → `YYYY H1`
- Jul–Dec → `YYYY H2`

## Workflow

1. **Get today's date.** Run `date +%Y-%m-%d` and `date +%A`. Never use user_info or any note — it may be stale.

2. **Weekend check.** If target date is Saturday or Sunday, create a personal-only note — skip all work sections. Structure:
   ```
   **Day**: Saturday

   ---
   # 🏠 **Personal**
   - 
   ```
   Archive any previous notes still in the top-level `Daily Note/` folder (move to `Daily Note/Archive/`). Stop — do not proceed further.

3. **Read the Daily Template** for exact structure.

4. **Carry-forward into Planned Work.** Find the latest existing weekday daily note before the target date:
   - List all `YYYY-MM-DD.md` files in both `Daily Note/` and `Daily Note/Archive/`
   - Filter to dates < target date that fall on Mon–Fri
   - Pick the most recent one (may not be yesterday — e.g. Monday → check Thursday/Wednesday)
   - Read its **Continue** section (titled "Continue tomorrow", "Continue on Monday", or similar)
   - Copy those bullets directly into **Planned Work** in the new note
   - If no previous weekday note exists, start from work board status only

   **CRITICAL — preserve every reference without exception.** When copying any bullet (from Continue, Planned Work, On the Radar, or Pending Requests), carry over **all** sub-bullets verbatim — every Slack thread link, every Jira ticket, every MR link, every Confluence/doc link, every wiki-link `📄 [[Page]]`. Never summarise, merge, or drop any sub-bullet. If a bullet had 5 sub-bullets in the source note, the new note must have exactly 5.

   Apply the universal bullet format: **bold title** on first line, description/action as sub-bullet, then links, then wiki-link — never put description on the same line as the title.

5. **Archive the previous note.** After reading it (step 4), move it to `Daily Note/Archive/`. Also archive any other notes still at the top level.

6. **Carry over unchecked sections.** From the previous daily note, copy unchecked `- [ ]` items from **📬 Pending Requests** and **👀 On the Radar** into the new note. Skip completed `- [x]` ones. Same preserve-every-reference rule applies.

7. **List work.** For each unchecked task from the previous Planned Work section:
   - **Planned Work (active)** — task requires active work today
   - **Planned Work (Next - keep as-is)** — if a task had a sub-bullet containing "Next (when in-progress tasks are done)", carry it forward **exactly as-is** with the same "Next" sub-bullet. **Do NOT promote it to active.** Never reclassify a "Next" item.
   - **On the Radar (`==(Monitoring)==`)** — code fully merged, no dev needed; just monitoring. Tasks waiting on code review or blocked on others stay in Planned Work with `==(Waiting)==`, not On the Radar.

   Also scan `Agoda/<Quarter>/*.md` for `Status: In progress` tasks not already in the note. Then list `Status: Next` tasks in Planned Work with sub-bullet *Next (when in-progress tasks are done)* — only if not already present.

8. **No duplicates across sections.** An item must appear in exactly one section. If it already exists anywhere in the note, update in place.

9. **Create the note.** Write `YYYY-MM-DD.md` using the template. Fill **Day** with weekday. Planned Work: active tasks + Next tasks. On the Radar: passive/monitoring tasks. **Omit any section with no content** — never write empty headings. **Do NOT include End-of-Day Review or Personal Review** — added only in `e` mode.

10. **Monday check.** If today is Monday, add as the **first item** in Planned Work:
    ```
    - [ ] **Sign off iOS + Android**
    	- ==Review== and ==sign off== iOS & Android builds
    ```

## Daily Note Conventions

See the shared conventions below — these apply to all daily note modes.

### Template structure

Day line, then `# 📋 **Planned Work**`. Remaining H1s separated by `---`: `# ⚡ **Unplanned**` (omit if empty), `# 👀 **On the Radar**`, `# 🏠 **Personal**`. No Morning Brief. No separate Pending Requests — unplanned asks go into Unplanned.

**Section order:** 1. Planned Work → 2. Unplanned → 3. On the Radar → 4. Personal

### Universal bullet format (ALL sections)

1. **Title** — short and concise (`(BWZP) iOS SSR badge`). Never a full sentence.
2. **Description / detail text** — sub-bullets explaining what/why
3. **Links** — MR + Slack thread + Jira on **one sub-bullet, comma-separated**. Standalone doc/Confluence links each get their own sub-bullet.
4. **Wiki-links `📄 [[Page]]`** — always last, each on its own sub-bullet

Example:
```
- [ ] **(BWZP) iOS SSR badge**
	- ==Waiting== for BE to confirm data model
	- [MR!1234](https://...), [💬 Thread](https://...), [🎫 PAYFLEX-233](https://...)
	- 📄 [[(BWZP) iOS SSR badge]]
- [ ] **(BWZP) iOS MMB CTA**
	- Next (when in-progress tasks are done)
	- [🎫 PAYFLEX-349](https://...)
	- 📄 [[(BWZP) iOS MMB CTA]]
```

### Sorting

- Unchecked items above checked items in every section
- Actionable items at the top, waiting/non-actionable at the bottom

### On the Radar = code done, just monitoring

Strictly for items where all code is merged and no dev is needed (experiments running, deployments out). Time horizon: 1–2 weeks max. If a task still needs coding, investigation, or code review → Planned Work.

### Highlight action verbs

Use `==verb==` in ALL sections: `==Relaunch==`, `==Waiting==`, `==Start==`, `==Follow up==`, `==Review==`, `==Ask==`, `==Merge==`, `==Close==`.

### Work board reference

- **In progress** = `Status: In progress` — list first
- **Next** = `Status: Next` — list after In progress with "Next (when in-progress tasks are done)" sub-bullet
