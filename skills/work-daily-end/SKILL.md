---
name: work-daily-end
description: Update today's daily note with end-of-day review, Continue section, and cleanup. Use when the user says "e", "end of day", "eod", "wrap up today", "end note", or "fill in end of day". Asks what was accomplished, what didn't get done, and fills the review sections.
---

# Daily Note — End of Day (e)

**Update the existing daily note for today** — do not create a new one.

## Paths

- **Daily note folder:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Daily Note/`
- **Work board:** `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/<Quarter>/`
- **Quarter:** Jan–Jun → `YYYY H1`, Jul–Dec → `YYYY H2`

## Workflow

1. **Get today's date.** Run `date +%Y-%m-%d`. Do not use user_info or any note. Open today's note at `Daily Note/YYYY-MM-DD.md`. If it doesn't exist, create it first (as in daily-note-create). If the note exists but lacks `# 🌙 **End-of-Day Review**` and `# 🌙 **Personal Review**`, append them before proceeding.

2. **Ask the user:**
   - What did you accomplish today? → **What I accomplished**
   - What didn't get done and why? → **What didn't get done & why**

3. **Check for unchecked items not mentioned.** After the user replies, scan today's note for any unchecked `- [ ]` items across all sections the user didn't mention. Ask about each one — unless obviously time-bound and not due today. Do not assume; ask.

4. **Pull follow-ups.** Scan `Agoda/<Quarter>/*.md` for `Status: In progress`. From each page, collect `==Follow up==` (or "follow up", "follow-up") bullets from Latest Update. Attach reference links under the related follow-up bullet (not a separate Reference section).

5. **Update the note.** Under `# 🌙 **End-of-Day Review**`:
   - Fill **What I accomplished** (planned work only)
   - Fill **What didn't get done & why** with planned items not done
   - **Continue section** — weekend-aware heading:
     - Today is Friday (or Sat/Sun) → `### **Continue on Monday**`
     - Otherwise → `### **Continue tomorrow**`
   - Continue bullets use the same format as Planned Work: bold title, sub-bullets for detail, links, wiki-link. New bullets at bottom.
   - Unplanned items → top-level `# ⚡ **Unplanned**` section (between Planned Work and Personal), not here.
   - On the Radar items → include in Continue only if something is relevant for the next workday. Exclude if timeline is clearly beyond next workday.
   - **Always convert vague time estimates to explicit dates** (e.g. "est. next week" → "est. week of YYYY-MM-DD").

6. **Clean up.** Remove any section that is empty (empty Personal, headings with only placeholders). Leave the note tidy.

## End-of-Day Review Format

Use bullets (not numbered lists). Sub-sections use `### **Title**` headers. First-level bullets are short plain-text labels (no bold). Sub-bullets hold detail. Do not bold sub-bullet labels.

Example:
```
### **What I accomplished**
- CMS
	- added logic for dynamic `placeholder` values; created batch `MR` (not ready for review).
### **What didn't get done & why**
- Testing the badge on SSR iOS
	- with the `response structure`. Waiting on `BE` tomorrow to confirm the open questions; if no changes needed, will test with that structure, get `MR` ready for review.
### **Continue tomorrow**
- **(BWZP) iOS SSR badge**
	- ==Follow up== with BE re data model
	- [MR!1234](https://...), [💬 Thread](https://...), [🎫 PAYFLEX-233](https://...)
	- 📄 [[(BWZP) iOS SSR badge]]
```

## Key Rules

- **Highlight important keywords** with backticks (`MR`, `BE`, `response structure`, `placeholder`) — don't overdo it.
- **Concise but not vague** — include enough context ("test what?", "BE confirmation about what?").
- **References under the related bullet**, not in a standalone Reference section.
- **Bidirectional sync** — if updating a task's status in the daily note, also update the linked work page (add Latest Update entry, update `Latest` frontmatter).
