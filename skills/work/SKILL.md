---
name: work
description: Create or update Obsidian work pages for tasks in the Agoda Workspace folder. Use when the user says "create a work page", "add a work page", "update work page", "log update to work page", "new task page", "add last update", "add MR to work page", "add Jira to work page", or mentions creating/editing a task page in the current H1/H2 workspace. Also use when formatting or fixing an existing work page to follow the work template. Shorthand triggers — "c" = create work page, "u" = update work page, "f" = reformat work page, "n" = note (create daily note), "e" = end (update today's daily note), "t" = track (add a checkbox item to today's note from a Slack thread or image).
---

# Work Page Skill

Create or update Obsidian task pages in the Agoda Workspace folder, following the standard Work Template.

## Quarter & Workspace

**Quarter format:** `YYYY H1 or H2` (first or second half of the year).

Compute Quarter from the current date:
- Jan–Jun → `YYYY H1` (first half)
- Jul–Dec → `YYYY H2` (second half)

Use the current year (e.g. today is 2026-03-16 → `2026 H1`). The workspace folder name matches the Quarter value (e.g. for today, `2026 H1`).

## Workspace Location

Compute Quarter from the current date (Jan–Jun → `YYYY H1`, Jul–Dec → `YYYY H2`). The workspace path uses that value:

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/<Quarter>/
```

Example: for the current day (e.g. March 2026), Quarter = `2026 H1`, so the path is `.../Agoda/2026 H1/`.

**Exception — Interview pages:** Pages for candidate interviews go in a year subfolder under `Interviews/`, not in the Quarter workspace:
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/Interviews/YYYY/
```
Example: `Interviews/2026/Interview - Mahesh K (2026-03-18).md`

Template reference:
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/Work Template.md
```

## Daily Note (for modes "n" and "e")

Daily notes live in a separate folder and use a different template.

**Always use the real current date for "today" and "tomorrow".** Run a shell command to get it (e.g. `date +%Y-%m-%d` for `YYYY-MM-DD`, `date +%A` for weekday). Do not use the date from user_info or from any note — it may be stale.

**Daily note folder:**
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Daily Note/
```

**Daily template (example structure):**
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Daily Note/Archive/Daily Template.md
```

**File naming:** one note per day, `YYYY-MM-DD.md` (e.g. `2026-03-16.md`).

**Template structure:** Day, then straight into `# 📋 **Planned Work**` (no Morning Brief section). Remaining H1s separated by `---`: `# ⚡ **Unplanned**` (omit if empty), `# 📬 **Pending Requests**`, `# 👀 **On the Radar**`, `# 🌙 **End-of-Day Review**` (accomplished, didn't get done, continue next workday), `# 🏠 **Personal**`, `# 🌙 **Personal Review**` (accomplished, continue next workday). Personal and Personal Review always come after the work End-of-Day Review.

**Work board:** Work pages in `Agoda/<Quarter>/` (same as workspace; Quarter = computed value e.g. `2026 H1`). **In progress** = `Status: In progress`; **Next** = `Status: Next` (to pick up when in-progress tasks are done). Use both when building daily notes: list In progress first, then Next with a note that they are next.

### Daily note conventions (apply in Note "n" and End "e" modes)

**Universal bullet format (applies to ALL sections):** Every item follows the same order:
1. **Title** — short and concise (e.g. `(BWZP) iOS SSR badge`, `Pending Int + Deint`). Never a full sentence.
2. **Description / detail text** — sub-bullets explaining what/why
3. **Links** (Jira, Slack, doc, etc.) — each on its own sub-bullet
4. **Wiki-links `📄 [[Page]]`** — always last, each on its own sub-bullet

Never mix description text and links on the same line. Never concatenate multiple references on one line.

**Planned Work section:** The first section in the note — starts right after the Day line. Heading is **Planned Work** (not "Work"). Each task uses `- [ ] **Task name**` (checkbox + bold title). List **In progress** tasks first (including items carried forward from the previous day's "Continue" section); then **Next** tasks with a sub-bullet note *Next (when in-progress tasks are done)*.

**Actionable items go to the top, waiting/non-actionable items go to the bottom** — applies to ALL sections (Planned Work, Unplanned, Pending Requests, On the Radar). An item is waiting/non-actionable if it requires confirmation from someone else, is blocked, or has no action you can take right now. Actionable items at the top let you focus immediately on what can be worked on.

**On the Radar time horizon — 1–2 weeks max.** Only keep items in On the Radar if they are expected to be actionable within ~2 weeks. If something will take longer (e.g. "est. next month", "after X which is 3+ weeks away"), drop it from On the Radar entirely until it becomes relevant.

**"drop" keyword** — when the user says "drop [item]", remove it from today's daily note and, if it's a work page, move it to the `Backlog/` subfolder and set `Status: On hold`. Add a `[[YYYY-MM-DD]]` Latest Update entry explaining why it was dropped (e.g. "not in this sprint", "timeline too long", "blocked on design"). This is the standard way to deprioritize something.

**Highlight action verbs with `==verb==`** in ALL sections — in the description sub-bullet and in the title if the verb appears there. Examples: `==Relaunch==`, `==Waiting==`, `==Start==`, `==Follow up==`, `==Review==`, `==Ask==`, `==Merge==`, `==Close==`. This helps scan tasks at a glance. Example:
- [ ] **(BWZP) iOS SSR badge**
	- [PAYFLEX-233](https://...)
	- 📄 [[(BWZP) iOS SSR badge]]
- [ ] **Pending Int + Deint**
	- List bugs/int/deint exps for iOS & Android.
	- 📄 [[Pending Int + Deint]]
- [ ] **(BWZP) iOS MMB CTA**
	- Next (when in-progress tasks are done)
	- [PAYFLEX-349](https://...)
	- 📄 [[(BWZP) iOS MMB CTA]]

**Unplanned section:** A top-level `# ⚡ **Unplanned**` section sits between Planned Work and Personal. Add it only when there are actual unplanned items; omit if empty. Each item uses `- [ ] **Title**` (checkbox + bold title), then sub-bullets for detail/links. Example:
- [ ] **Reviewed two `MRs`**
- [ ] **Allocation bias investigation (Card Page webview migration experiment)**
	- Looked into [Slack thread](https://...).
	- 📄 [[(Card Page) Allocation Bias Investigation]]

**End-of-Day Review:** Use bullets (not numbered lists). Sub-sections use `### **Title**` headers; under each, first-level bullets are short labels in plain text (no bold); sub-bullets hold the detail. Do not bold the sub-bullet labels. Example:
### **What I accomplished**
- CMS
	- added logic for dynamic `placeholder` values; created batch `MR` (not ready for review).
### **What didn't get done & why**
- Testing the badge on SSR iOS
	- with the `response structure`. Waiting on `BE` tomorrow to confirm the open questions; if no changes are needed, will test with that structure, get the `MR` ready for review.

**Highlight important keywords** with backticks (e.g. `MR`, `BE`, `response structure`, `placeholder`) so they stand out—but don't overdo it.

**References:** Put links under the related bullet (e.g. Sourcegraph or doc link under the specific follow-up), not in a standalone Reference section.

**Carry-forward from previous day:** When **creating** a daily note (Note "n"), find the most recent previous weekday note (see step 3 below) and copy all bullets from its **Continue** section directly into **Planned Work**. If there is no previous note, start Planned Work from work board status only. The **Continue** section in the new note stays empty until the user fills it at end of day (End "e" mode).

**Concise but clear:** When writing End-of-Day Review from user input, keep it concise but do not cut important details (e.g. "test what?", "BE confirmation about what?"—include enough context so it's not vague).

**End (e) cleanup:** When updating today's daily note, remove any section that is empty (e.g. empty Personal, or any heading whose content is only placeholders or blank bullets). Treat it as cleaning up at the end of the day.

## File Naming Convention

`(FEATURE_CODE) Platform Short Description.md`

Examples:
- `(BWZP) iOS SSR badge.md`
- `Integration DatePicker Fix (native).md`
- `Deintegration Cashback Redemption Nudge.md`

Use `(FEATURE_CODE)` prefix when the task is tied to a specific experiment/feature code. Otherwise use a plain descriptive name.

## Page Structure

New tasks default to `Status: Not started`, `Type: 🌟 feature`, and are saved into the `Backlog/` subfolder.

```
---
Status: Not started
Created time: YYYY-MM-DDTHH:MM
Latest: [concise one-line summary of the most recent update]
Quarter: YYYY H1 or H2
Type: 🌟 feature
---
# **Latest Update**
[entries only when there are actual updates — see below]

# **What's about**
- [brief description of the task]

[optional: embed image if available]

# **Reference**
[only include sub-sections that have real content]
- ### Contacts
	- stakeholders
		- [name / role]
	- working groups
		- [group]
	- support channels
		- [channel]
- ### Links
	- Jira stories
		- [PAYFLEX-XXX](https://...)
	- merge requests
		- [MR title](https://...)
	- experiment
		- EXPERIMENT-ID-IOS

# **Implementation Details**
- **Data**:
	- [models, APIs, mappers]
- **Toggle** (if any):
	- [experiment ID]
- **UI / Logic** (if needed):
	- [when it shows, what users see]

# **Testing**
-
```

## Critical Rules

**Omit empty sections and sub-headers.** Never include a sub-header (Contacts, working groups, support channels, etc.) if there is no real content to put in it. An empty placeholder is worse than nothing.

**No placeholder dates in Latest Update.** Only add a `📄 [[YYYY-MM-DD]]` entry when there is an actual note to record. Leave `# **Latest Update**` empty if there are no updates yet.

**Contacts sub-section is usually absent.** Most task pages only have `### Links`. Only add `### Contacts` when stakeholders/working groups/support channels are actually known.

**Use bullets and sub-bullets so content is easy to scan.** Avoid long single-line bullets. Prefer a **bold action verb or label** as the lead bullet, then indent the detail as a sub-bullet. This applies everywhere (Implementation Details, Latest Update, What's about, etc.).

Latest Update example:
- 📄 [[2026-03-16]]
	- **Switched**
		- `BWZP badge` to `CMS 560056` and added `room currency` in the placeholder.
	- **Fixed**
		- `payLaterOptions` GraphQL query — was `[Int]`, actually `[DFPayLaterOption]`.
	- **==Follow up==**
		- tomorrow: ask BE about the data model.

Implementation Details example:
- **Data**:
	- `payLaterOptions: [DFPayLaterOption]?` on `DFPayLater`, each with `code: String?` (GraphQL enum: `"BWZP"`).
- **Toggle**:
	- `PaymentLocalisationToggles.bookWithZeroPay` (`PAYFLEX-233-IOS`).

**Latest date on top, new bullets at bottom.** When adding a new date, insert it above older dates. When adding bullets under an existing date, append below the existing bullets. Omit any group or sub-section that has no content.


## Interview Pages

Interview notes live in a separate folder, organised by year:
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/Interviews/YYYY/
```

**Template:**
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/Interviews/Interview Template.md
```

**File naming:** `Interview - Candidate Name (YYYY-MM-DD).md` (e.g. `Interview - Mahesh K (2026-03-18).md`)

**Frontmatter defaults:** `Type: 🎙️ interview`, `Status: In progress` (→ `Done` after), `Quarter: YYYY H1 or H2` (computed from interview date).

**Scorecard sections:** Problem solving, Coding efficiency, Communication, Testing, Understanding performance (each /5, total /25).

**After interview:** Fill Scorecard table, then write Summary (Excelled in / Struggled with / Conclusion with Recommendation + Pros + Cons). Update `Latest` frontmatter with one-line outcome and set `Status: Done`.

## Workflow

### Creating a new work page

**Default for new tasks:** `Status: Not started`, `Type: 🌟 feature`, saved into `Backlog/` subfolder (override type if the user says bug/refactor/etc.).

**Type inference from title/content — always check before defaulting to feature:**
- Title contains "Investigation", "Investigate", "Debug", "Root cause" → `🔍 investigation`
- Title contains "Experiment", "Exp", "A/B", "Launch", "Allocation bias" → `🧪 experiment`
- Title contains "Bug", "Fix", "Issue", "Error" → `🐛 bug`
- Title contains "Refactor", "Cleanup", "Migration", "Migrate" → `🔧 refactor`
- Otherwise → `🌟 feature`

1. **Search first.** Before creating, run `find` across the entire `Agoda/<Quarter>/` tree (including all subfolders) for any file whose name contains key words from the task. If a match is found, open it instead of creating a new one.
2. Ask the user for any missing key details: task name, Jira ticket, MR link, experiment ID, type (default feature), brief description. Collect what's available — skip sections for anything unknown.
3. Determine the file name from the task context.
4. Write the file using `python3` (required to handle special characters in filenames):

```python
import datetime

# Compute quarter from current date (e.g. 2026 H1 for Jan–Jun 2026)
workspace = '/Users/kpayuhawatta/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/2026 H1/Backlog/'
filename = '(BWZP) iOS SSR badge.md'

content = '''---
Status: Not started
Created time: YYYY-MM-DDTHH:MM
Quarter: YYYY H1 or H2
Type: 🌟 feature
---
# **Latest Update**

# **What's about**
- [description]

# **Reference**
- ### Links
\t- Jira stories
\t\t- [🎫 PAYFLEX-233](https://agoda.atlassian.net/browse/PAYFLEX-233)
\t- merge requests
\t\t- [MR title](https://gitlab.agodadev.io/...)
\t- experiment
\t\t- PAYFLEX-233-IOS

# **Implementation Details**
- **Data**:
\t- [models, APIs, mappers]
- **Toggle** (if any):
\t- [experiment ID]
- **UI / Logic** (if needed):
\t- [when it shows, what users see]

# **Testing**
-
'''

with open(workspace + filename, 'w') as f:
    f.write(content)
```

### Updating an existing work page (shorthand: "u")

**Adding a Latest Update entry** (most common update):
```python
# Quarter = computed from current date (e.g. 2026 H1)
workspace = '/Users/kpayuhawatta/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/2026 H1/'
filename = '(BWZP) iOS SSR badge.md'

with open(workspace + filename, 'r') as f:
    content = f.read()

new_entry = '- 📄 [[YYYY-MM-DD]]\n\t- [update note here]\n'
content = content.replace('# **Latest Update**\n', f'# **Latest Update**\n{new_entry}')

with open(workspace + filename, 'w') as f:
    f.write(content)
```

**Updating status** (e.g., to Done):
Find `Status: In progress` in frontmatter and replace with `Status: Done`.

**When status is set to Done — move page to `Done/` folder:**
```python
import os, shutil

workspace = '/Users/kpayuhawatta/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/2026 H1/'
filename = '(BWZP) iOS SSR badge.md'

shutil.move(workspace + filename, workspace + 'Done/' + filename)
```
Always move the file after writing the updated content. The `Done/` folder path is `<workspace>Done/`.

**Adding a link** (MR, Jira, etc.):
Locate the relevant sub-section under `### Links` and append the new item.

**Always update `Latest update` frontmatter** whenever adding a new Latest Update entry — replace with a concise one-line summary of what changed (e.g. `Sent MR for review; waiting on BE re data model`).

**Sync to today's daily note:** After updating the work page, check today's daily note for any bullet that references the same page (via wikilink `[[Page name]]` or Jira ticket). If found:
- In **Planned Work** — add a sub-bullet under the task summarising the update. Always linkify MR numbers and Jira tickets (e.g. `- [MR!39784](https://...) ready for review`).
- In **On the Radar** / **Pending Requests** — update the description sub-bullet to reflect the latest state
- If no reference exists in the daily note, skip silently (do not add one)

**Re-sort after status changes to waiting:** If the update makes a task waiting/non-actionable (e.g. the update says "waiting on X", "==waiting==", blocked, or sent for review), also reorder that bullet within its section in today's note — move it to the **bottom** of the section (below all actionable items), following the ordering rule. Do this as part of the same sync step.

The goal is to keep the daily note in sync without requiring a separate `/work t` step.

### Reformatting an existing work page (shorthand: "f")

Use when a page exists but lacks standard structure (no frontmatter, bare lists, etc.). The goal is to wrap the existing content in the standard template without losing any data.

1. Read the existing file with `python3`.
2. Identify the content type — determine appropriate `Type` from the content (feature, refactor, etc.).
3. Preserve all existing content — map it into the correct sections. If content doesn't fit standard sections (e.g., custom tracking lists), keep it as named `# **Section**` headings after `# **What's about**`.
4. Add frontmatter with `Created time` set to today, `Status: In progress`, leave `Updated time` empty.
5. Add `# **Latest Update**` (empty) and `# **What's about**` with a one-line description inferred from the content.
6. Write the reformatted file back.

```python
# Quarter = computed from current date (e.g. 2026 H1)
workspace = '/Users/kpayuhawatta/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/2026 H1/'
filename = 'Pending Int + Deint.md'

# Read existing content first, then rewrite with standard template wrapping it
with open(workspace + filename, 'r') as f:
    existing = f.read()

# Rewrite with frontmatter + standard sections + preserved content
content = '''---
Status: In progress
Created time: YYYY-MM-DDTHH:MM
Quarter: YYYY H1 or H2
Type: 🔧 refactor
---
# **Latest Update**

# **What\\'s about**
- [inferred one-line description]

[preserved sections follow]
'''

with open(workspace + filename, 'w') as f:
    f.write(content)
```

### Note (n) — Create daily note

Create a **new daily note for today** under the Daily Note folder. Use the Daily Template structure and the **Daily note conventions** above (Planned Work section format, top-level Unplanned section after Planned Work, backticks for keywords, references under related bullets).

1. **Get today's date:** Run `date +%Y-%m-%d` and `date +%A` (or equivalent) to get the real current date and weekday. Do not use user_info or any note. Use this for "today"; for "tomorrow" use the next calendar day. **Resolve paths:** Daily note folder = `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Daily Note/`. Template = `Daily Note/Archive/Daily Template.md`. Target file = `YYYY-MM-DD.md` (today or tomorrow as requested).
2. **Weekend check:** If the target date falls on Saturday or Sunday, create a **personal-only note** — skip all work sections (Planned Work, Pending Requests, On the Radar) and only include **Personal**. Structure:
   ```
   **Day**: Saturday

   ---
   # 🏠 **Personal**
   - 
   ```
   Archive any previous notes still in the top-level `Daily Note/` folder (move to `Daily Note/Archive/`). Then stop — do not proceed to steps 3–9.
3. **Read the Daily Template** to get the exact structure (Day, Planned Work, Pending Requests, On the Radar, Personal, End-of-Day Review). Use **bullets** for End-of-Day Review (not numbered lists).
4. **Carry-forward into Planned Work:** Find the **latest existing weekday daily note** before the target date. To do this: list all `YYYY-MM-DD.md` files in both `Daily Note/` and `Daily Note/Archive/`, filter to dates < target date that fall on weekdays (Mon–Fri), then pick the most recent one. It may not be "yesterday" — e.g. if today is Monday, the latest weekday note could be Thursday or Wednesday (if Friday's note doesn't exist). Read that note's **Continue** section (titled "Continue tomorrow", "Continue on Monday", or similar). Those bullets go directly into **Planned Work** in the new note. If no previous weekday note exists, start Planned Work from work board status only. Apply the universal bullet format: **bold title** on the first line, description/action as a sub-bullet, then links, then wiki-link — never put description or action on the same line as the title.
5. **Archive the previous note:** After reading the previous daily note (from step 4), move it into the `Daily Note/Archive/` folder. This keeps the main `Daily Note/` folder clean — only the current day's note lives at the top level. Also archive any other notes still at the top level (e.g. weekend notes).
6. **Carry over unchecked sections:** From the previous daily note, copy any unchecked () items from **📬 Pending Requests** and **👀 On the Radar** sections into the new note (same sections, same content). Only carry items that are still unchecked — skip completed () ones.
7. **List work:** Look at the **previous daily note's Planned Work** section. For each unchecked task, decide where it goes in the new note:
   - **Planned Work** — task requires active work today (coding, investigation, decision, etc.)
   - **On the Radar** (`==(Waiting)==`) — task requires no action from me today (e.g. MR out for review, waiting on BE/someone else). Include key links and wiki-link.
   Also scan `Agoda/<Quarter>/*.md` for any `Status: In progress` tasks not already covered. Then list **Next** tasks (from work pages) in Planned Work with a sub-bullet *Next (when in-progress tasks are done)*. Leave the **Continue** section empty (it's filled at end of day).
8. **No duplicates across sections.** An item must appear in exactly one section across the entire note — Planned Work, Unplanned, Pending Requests, On the Radar, Personal. If an item already exists anywhere in the note, update it in place rather than adding it to another section.
9. **Create the note:** Write `YYYY-MM-DD.md` using the template. Fill **Day** with the weekday. **Planned Work:** active tasks + Next tasks. **On the Radar:** passive/waiting tasks from previous Planned Work + carried-over On the Radar items. Leave **Personal** empty for the user to fill. **Do NOT include End-of-Day Review or Personal Review sections** — these are added only during `e` (end-of-day) mode.
10. **Monday check:** If today is Monday, add the following as the **first item** in Planned Work (before all other tasks):
    ```
    - [ ] **Sign off iOS + Android**
    	- ==Review== and ==sign off== iOS & Android builds
    ```

### End (e) — Update today's daily note

**Update the existing daily note for today** (do not create a new one). Ask the user for what they accomplished and what didn't get done, then pull follow-ups from In Progress work. Use the **Daily note conventions** (End-of-Day Review format: section bold, lead bullets plain, sub-bullets for detail; backticks for keywords; concise but not vague). Note: Unplanned items go in the top-level `# **Unplanned**` section (between Planned Work and Personal), not in the End-of-Day Review.

1. **Get today's date:** Run `date +%Y-%m-%d` to get the real current date (do not use user_info or any note). **Open today's note:** Path = `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Daily Note/YYYY-MM-DD.md`. If it does not exist, create it from the Daily Template first (as in Note mode). If the note exists but does not yet have `# 🌙 **End-of-Day Review**` and `# 🌙 **Personal Review**` sections, append them now before proceeding.
2. **Ask the user (concise):**
   - What did you accomplish today? (for **What I accomplished**)
   - What didn't get done and why? (for **What didn't get done & why**)
3. **Check for unchecked items not mentioned:** After the user replies, scan today's note for any unchecked (`- [ ]`) items across all sections that the user didn't mention. For each one, ask about it — unless it's obviously time-bound and not due today (e.g. a monitoring event scheduled for a future date). Do not assume; ask.
4. **Pull follow-ups:** Scan `Agoda/<Quarter>/*.md` (Quarter = computed from current date, e.g. `2026 H1`) for `Status: In progress`. From each page, collect **==Follow up==** (or "follow up", "follow-up") bullets from Latest Update. Attach any reference links under the related follow-up bullet (not a separate Reference section).
5. **Update the note:** Under **End-of-Day Review**, fill using the convention: **What I accomplished** (planned work only); **What didn't get done & why** with planned items not done; short plain-text lead bullets and sub-bullet detail; highlight terms with backticks; keep concise but include enough context. **Continue section** — use a weekend-aware heading: if today is Friday (or Sat/Sun), title it `### **Continue on Monday**`; otherwise title it `### **Continue tomorrow**`. Bullets from In Progress; new bullets at bottom. Each item uses the same format as Planned Work: bold title, sub-bullets for detail, links, and wiki-link. If there are unplanned items to add, insert/append them in the top-level `# **Unplanned**` section (between Planned Work and Personal), not in End-of-Day Review. **When deciding whether to include an On the Radar item in the Continue section:** include it only if there is something relevant for the next workday (e.g. a monitoring event). Exclude it if the timeline is clearly beyond the next workday. **Always convert vague time estimates to explicit dates** when writing Continue sub-bullets (e.g. replace "est. next week" with "est. week of YYYY-MM-DD") — this makes future notes easier to reason about and avoids stale carry-overs.
6. **Clean up:** Remove any section that is empty (e.g. empty Personal, or headings with only placeholders). Leave the note tidy at end of day.

### Track (t) — Capture into today's note or related work page

**Quickly capture something to act on or monitor**, from a Slack thread, image, or description. If the content is clearly related to an existing work page, add a Latest Update entry there (and sync to today's note). Otherwise, add a `- [ ] **Title**` checkbox bullet to the appropriate section in today's note. Use context clues (Jira ticket, keywords, names) to infer the project and section. Only ask if genuinely ambiguous after reading the content.

1. **Read the input** — Slack link, image screenshot, or user description. Extract: what it is, who's involved, what action (if any) is needed.
2. **Draft the bullet** using the universal format:
   ```
   - [ ] **Short title**
   	- context / detail
   	- [💬 Slack thread](https://...)
   ```
3. **Determine the section** based on context:
   - **Unplanned** — something that already happened today and took time
   - **Pending Requests** — someone asked *me* to do something (review code, set something up, help with a task)
   - **On the Radar** — *I'm waiting on others* to respond, or an upcoming event/maintenance to monitor; not urgent. Always prefix the title with a highlight category: `==(Waiting)==`, `==(Monitoring)==`, or `==(Blocked)==`. **Before adding here, check all other sections.** If the item already exists anywhere in the note (e.g. already in Planned Work), update that bullet in place instead of duplicating it here.
   - **Personal** — non-work item (events, appointments, errands). For events with a physical location, include a Google Maps search link: `[Venue Name](https://www.google.com/maps/search/?api=1&query=Venue+Name+City)`. For events with a time, include it in the title (e.g. `Event Name 🎟️ 18:00 – 22:00`).
4. **Write immediately** — no confirmation needed. Append the bullet to the correct section in today's note using `python3`. Replace the placeholder (`- \n` or `- [ ] \n`) if the section is still empty, otherwise append after the last bullet in that section.
5. **Report back** with the bullet added and which section it went into.

### Reading an existing work page

Use `python3` to read (avoids shell quoting issues with special characters):
```python
with open(workspace + filename, 'r') as f:
    print(f.read())
```

## Frontmatter Reference

| Field | Values |
|-------|--------|
| Status | `Not started`, `In progress`, `Next`, `Done`, `Blocked`, `On hold` |
| Type | `🌟 feature`, `🐛 bug`, `🔧 refactor`, `🧪 experiment`, `🔍 investigation` |
| Quarter | `YYYY H1 or H2` |
| Created time | `YYYY-MM-DDTHH:MM` |
