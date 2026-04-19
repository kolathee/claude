---
name: plan-calendar
description: Schedule tasks into free calendar slots and create Google Calendar events. Use for: plan my day/week/biweekly, assign/schedule/time-block tasks, add to calendar, book a slot, reschedule/move/shift an event, cancel/drop/remove an event, or any request to create, move, or remove a calendar event.
---

# Assign Tasks Skill

Fetch free time from the calendar, collect Todoist and Jira tasks, ask the user to estimate durations, suggest a time-blocked schedule, and on confirmation create calendar events.

**Modes:**
- **Daily** (default): `/plan-calendar` or `/plan-calendar today`
- **Weekly**: `/plan-calendar week` · `w` · `7d` · `7 days` · `1w`
- **Biweekly**: `/plan-calendar biweekly` · `2w` · `14d` · `2 weeks`
- **Reschedule**: `/plan-calendar re [task name]` — move a specific task to a new time slot
- **Add**: `/plan-calendar add [description]` or natural language like `/plan-calendar I'm going to have Sushio at 4-5pm` — add a new event, detecting and resolving any conflicts
- **Cancel**: natural language like "cancel [event]", "remove [event] from calendar", "delete that event" — removes the calendar event AND completes/deletes the Todoist task (fully done with it)
- **Drop**: natural language like "drop [event]", "skip [event]", "remove the block for [event]", "not doing this anymore" — removes the calendar event AND resets the Todoist task (clears due date + resets priority to none), leaving it in the inbox without priority for future rescheduling

---

## Step 0: Determine Mode

- If the argument starts with `re `, `reschedule `, or `move ` followed by a task name → **reschedule mode** (see below)
- If the user said "biweekly", "2 weeks", "two weeks", "14 days", "14d", or "2w" → **biweekly mode** (14 days starting today)
- If the user said "week", "weekly", "7 days", "7d", "1w", "w", or "in advance" → **weekly mode** (7 days starting today)
- If the user implies removing an event completely ("cancel", "cancel that", "remove from calendar", "delete that event", "I'm not going anymore") → **cancel mode** (see below)
- If the user implies removing the calendar block but keeping the task ("drop", "skip", "remove the block", "not doing this today", "unschedule") → **drop mode** (see below)
- Otherwise → **daily mode** (today only)

### Cancel Mode

"Cancel [event]" = fully done with it — remove everything.

1. Search Google Calendar for the event by name (today + upcoming 7 days)
2. If found, confirm: `Cancel "📝 Do Dev survey" (Sat Mar 7, 16:00–16:15)? This will also delete the Todoist task. Reply "ok" or "keep task" to only remove the calendar event.`
3. On "ok": delete calendar event + delete/complete Todoist task
4. On "keep task": delete calendar event only (same as drop)
5. Report: `✅ Cancelled "Do Dev survey" — removed from calendar and Todoist.`

### Drop Mode

"Drop [event]" = remove the time block and reset the task in Todoist (no date, no priority) so it sits in the inbox until replanned.

1. Search Google Calendar for the event by name
2. If found, confirm: `Drop "📝 Do Dev survey" (Sat Mar 7, 16:00–16:15)? The calendar block will be removed and the Todoist task will have its due date and priority cleared. Reply "ok".`
3. On "ok":
   - Delete the calendar event
   - Update the Todoist task: clear due date (`dueString: null`) and reset priority to none (`priority: 4`)
4. Report: `✅ Dropped "Do Dev survey" — calendar block removed. Todoist task reset (no date, no priority).`

### Reschedule Mode

When invoked as `/task-assignment re [task name]` (e.g. `/task-assignment re devSurvey`):

1. **Find the task** — search Todoist for a task matching the name (fuzzy match OK). If multiple match, list them and ask user to confirm which one.

2. **Find the existing calendar event** — search Google Calendar for a recent/upcoming event whose title contains the task name (e.g. `📝 Do Dev survey`). If found, note its current time.

3. **Ask for the new time** — present two options:
   > Found: 📝 Do Dev survey — currently scheduled Sat Mar 7, 16:00–16:15
   > When would you like to reschedule it to? Options:
   > a) Next available slot (I'll find it)
   > b) Specific date/time — tell me when

4. **On "next available"** — fetch Google Calendar for the next 7 days and find the first free slot matching the task duration, respecting all zone rules (work zone for Work tasks, personal zone for personal, no-overlap, no weekends for [FU] tasks, etc.)

5. **On specific date/time** — use the date/time provided, validate no conflicts.

6. **Confirm with user** — show the new proposed slot and wait for "ok".

7. **On confirm:**
   - Delete the old calendar event (if found)
   - Create new calendar event at the new time
   - Update Todoist task due date to match new date
   - Report: `✅ Rescheduled "Do Dev survey" → Mon Mar 9, 10:00–10:15`

### Add Mode

Triggered by `/task-assignment add [description]` OR natural language that implies adding a new event (e.g. "I'm going to have Sushio at 4-5pm", "add workout push day 1 hour").

**Step 1 — Parse the request:**
Extract from natural language:
- **Event name**: e.g. "Sushio", "Workout - Push Day"
- **Date**: today if not specified; "next" = next available slot in the future
- **Time**: specific time ("4-5pm" → 16:00–17:00) or vague ("next" → find next free slot)
- **Duration**: from the time range, or explicitly stated ("1 hour")
- **Type**: personal/social event vs workout vs task

**Step 2 — Fetch today's/target day's calendar** (Google Calendar + Outlook if weekday)

**Step 3 — Conflict detection:**
Check if the requested time slot overlaps any existing event. If it does:

> ⚠️ "Sushio 16:00–17:00" conflicts with:
>   - 📊 What is derivatives — 17:55–18:55 (partially overlaps? → no)
>   - OR: 🏋️ Workout at 18:00–19:30 (back to back — leave buffer? → ask)
>
> The slot is free. Shall I add it?
> OR
> The following task would be displaced: 📊 What is derivatives (17:55–18:55). I'll move it to [next available time]. Confirm?

**Step 4 — For conflicting tasks: propose reschedule**
- Find the next available slot for each displaced task, respecting zone rules
- Present the full picture:
  > Plan:
  > ✅ Add: 🍱 Sushio — today 16:00–17:00
  > 🔀 Move: 📊 What is derivatives → tomorrow Sun 14:00–15:00 (next free slot)
  >
  > Reply "ok" to apply all, or "cancel".

**Step 5 — On confirm:**
- Create the new event
- For each displaced task: delete old event, create new event at new time, update Todoist due date
- Report all changes

**For "next" slot requests** (e.g. "workout push day 1 hour next"):
- Determine current position in workout cycle from most recent workout event in calendar
- Infer the next workout type (e.g. if last was Pull Day → next is Leg & Core)
- Find the next available 18:00–19:30 slot on a weekday
- Propose: `🏋️ Workout - Leg & Core — tomorrow Mon Mar 9, 18:00–19:30. Add?`

---

Set `PERIOD_START = today`, `PERIOD_END`:
- Daily → today
- Weekly → today + 6 days
- Biweekly → today + 13 days

---

## Step 0.5: Load Personal Context

Before fetching any data, read `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Personal/contexts/personal.md`. This file is the **source of truth** for all personal scheduling decisions. It contains:
- Timezone and Jira project details
- Scheduling zones (hours, allowed task types)
- Duration rules (dinner, shopping, workout)
- Recurring calendar blocks (do not reschedule or duplicate)
- Daily routine
- Workout cycle

---

## Step 1: Fetch Data (IN PARALLEL)

Also fetch **past task events** (last 14 days) from Google Calendar to detect carry-overs — add this to the parallel fetch.

**⚠️ Outlook is required for weekday scheduling.** If Outlook fails, apply the pre-flight validation rule (Step 1b) — stop and ask the user to re-authenticate before finalizing any Mon–Fri schedule. Without Outlook, work meetings are unknown and the weekday schedule may have conflicts.

**⚠️ Outlook API timezone bug:** Outlook returns event times without a proper timezone offset even when `preferredTimeZone: Asia/Bangkok` is requested. The returned times appear to be off by ~1 hour. Always cross-check Outlook times against Google Calendar or screenshots when times seem inconsistent.

**Google Calendar — full period (for free slot calculation):**
```
mcp__google-workspace__list_events:
- timeMin: "{PERIOD_START}T00:00:00+07:00"
- timeMax: "{PERIOD_END}T23:59:59+07:00"
- timeZone: "Asia/Bangkok"
- maxResults: 100
```

**Google Calendar — past 14 days (for carry-over detection):**
```
mcp__google-workspace__list_events:
- timeMin: "{TODAY - 14 days}T00:00:00+07:00"
- timeMax: "{TODAY - 1 day}T23:59:59+07:00"
- timeZone: "Asia/Bangkok"
- maxResults: 100
- q: "[Todoist]"     ← filter by this skill's prefix to avoid noise
```
Also fetch past Jira events separately with `q: "[PAYFLEX"` to cover Jira carry-overs.

**Outlook Calendar — full period (work meetings):**
```
mcp__plugin_agoda-skills_outlook__list_events:
- startDateTime: "{PERIOD_START}T00:00:00+07:00"
- endDateTime: "{PERIOD_END}T23:59:59+07:00"
- preferredTimeZone: Asia/Bangkok
```

**Todoist — always fetch all three sources in parallel:**

```
mcp__todoist__find-tasks-by-date:        ← tasks due today/overdue (daily) or this week (weekly)
- startDate: "today"
- limit: 50

mcp__todoist__find-tasks:               ← Inbox tasks (unassigned, unfiled)
- filter: "##Inbox & !p4"
- limit: 30
```

*Weekly mode additionally:*
```
mcp__todoist__find-tasks:               ← all tasks (inside and outside inbox) with priority p1–p3
- filter: "!p4"
- limit: 50
```

Merge all Todoist results, deduplicate by task ID.

**⚠️ Priority filter — applied after fetching:** After merging all Todoist results, **exclude any task with priority 4 (p4) or no priority set**. These are "someday" tasks with no committed date — do not schedule them. Only tasks with p1, p2, or p3 are considered for scheduling.

**Jira — active issues assigned to current user:**
```
mcp__plugin_agoda-skills_at__searchJiraIssuesUsingJql:
- cloudId: agoda.atlassian.net
- jql: project = PAYFLEX AND assignee = currentUser() AND status IN ("To Do", "In Progress", "Testing", "Code Review") ORDER BY priority ASC, updated DESC
- fields: ["summary", "status", "priority", "duedate", "story_points", "customfield_10016"]
- maxResults: 15
```
`customfield_10016` is the standard Jira story points field. Use whichever returns a value.

---

## Step 1b: Detect Carry-Over Tasks

After fetching, cross-reference past calendar events against current Todoist/Jira data to find tasks that were scheduled but never completed.

**How to identify carry-overs:**
- Look through past calendar events (last 14 days) for events with `[Todoist]` or `[PAYFLEX` in the title — these were created by a previous `/task-assignment` run
- For each such past event, check if the corresponding task **still exists** in the current Todoist/Jira results (i.e., still incomplete)
- If it does → it's a **carry-over** (was scheduled but not done)

**If carry-overs are found**, notify the user before proceeding:

```
⚠️ Found 3 tasks from previous schedule that weren't completed:

  🔁 Fix payment bug (Todoist p1) — was scheduled Mon Mar 3
  🔁 Write unit tests for card page (Todoist p2) — was scheduled Tue Mar 4
  🔁 PAYFLEX-380 — Decode payment method — was scheduled Wed Mar 5

These will be re-scheduled with higher priority. Reply "ok" to continue, or "skip [task]" to exclude one.
```

Wait for reply, then proceed. Carry-over tasks get **top scheduling priority** in Step 4 — placed before other tasks of the same type, regardless of their original priority label.

If no carry-overs → proceed silently.

---

## Step 2: Build the Day Map

For each day in the period, calculate scheduling zones. Zone hours and recurring blocks come from `personal.md` — use those values. Summary:
- **Weekdays**: Work zone (10:00–18:00) → Exercise (18:00–19:30, workout days) → Personal zone (19:30–21:00)
- **Weekends**: Personal zone all day (09:00–21:00)

**Work tasks during off-work time (weekends + 19:30–21:00 on weekdays):**
Work-labeled Todoist tasks and Jira issues are normally restricted to the work zone. Exceptions:

1. **Light work tasks** (surveys, resume updates, simple uploads, quick admin) → OK to schedule on weekends/off-work time without asking
2. **Tasks with explicit urgency signal** in description (e.g., "urgent", "deadline tonight", "critical") → schedule in personal zone
3. **All other work tasks** → ask the user before placing in off-work time
- Never silently schedule heavy work tasks (feature work, bug fixes, Jira stories) in off-work time

Merge Google and Outlook events per day. For overlapping events, merge into a single busy block. Subtract busy blocks to get free windows per zone per day.

**Scheduling window start:** always use the actual current time (rounded up to next 15 min) — never assume it's the start of the day. Check the system date/time before building the schedule. If today's morning slots are already gone, overflow tasks to the next available day (e.g. Sunday if Saturday morning has passed).

**Workout schedule:** Use cycle and timing from `personal.md`. Always check the most recent workout event in Google Calendar to find current position in the cycle, then apply forward. Weekends: if no existing workout event, suggest a morning slot (e.g. 10:00–11:30).

**Minimum slot:** 30 minutes — ignore gaps shorter than this

**⚠️ Calendar overlap SOP (STRICTLY ENFORCED):** Before creating ANY calendar event, always fetch that day's full Google Calendar events and verify the proposed slot is free. Never create an event without checking first. This applies to every single add, even small ones.

**Conflict handling (applies to all event creation, not just Add Mode):**
- **If free** → create the event immediately, no need to ask
- **If conflict exists** → do NOT create. Instead:
  - Tell the user what's already there (event name + time)
  - Ask what they want to do
  - Suggest options: keep new event & move the existing one, reschedule the new event (suggest alternative free slots), or override/create anyway (if user insists)
- **Exception — leave reminders / travel buffer events:** still check, but if the only conflict is the destination event itself, that's expected — create the reminder anyway

**Ignore list — not real conflicts:**
- **Unnamed Outlook recurring block Mon–Fri 12:00–14:00 Bangkok** = personal time blocking by Cup. Ignore entirely — never treat as a conflict, never move Google Calendar tasks because of it. (Shows as 13:00–15:00 in Outlook API due to timezone bug above.)

**No-overlap rule (STRICTLY ENFORCED):** Before placing any task block, verify it does not overlap with ANY existing calendar event, including recurring blocks. The 09:30–10:00 RemNote slot is busy every single day — never schedule a task that starts before 10:00 or ends after 09:30 on the same morning. Run a conflict check against the full Google Calendar fetch before finalizing each slot.

**Displaced task rescheduling (STRICTLY ENFORCED):** When a task is displaced by a new event (in Add Mode or Reschedule Mode), NEVER suggest a new time slot without first fetching the target day's full calendar. Always call `mcp__google-workspace__list_events` for every target day before proposing slots. Only suggest times that are confirmed free after checking actual events.

**Travel buffer:** when a task slot is followed by an event that requires leaving the house (party, appointment, dinner out, etc.), always check if travel time is needed. Ask "how long is the drive?" and leave a buffer before the event. Never schedule tasks ending right at the event start time.

---

## Step 3: Ask for Task Duration Estimates

Present all unique tasks once (across the full period). Group by source, show due date if set.

```
Here are your tasks for the week. Confirm or adjust durations (e.g. "2=45m, 5=2h"):

TODOIST — Work
  1. [p1] Fix payment bug                    → suggested: 1h    (due Mon)
  2. [p2] Review PR from Tor                 → suggested: 30m   (due today)
  3. [p2] Write unit tests for card page     → suggested: 1.5h  (no due date)

TODOIST — House work / Other
  4. [p3] Buy groceries                      → suggested: 30m   (due today)
  5. [p3] Study investing chapter 3          → suggested: 1h    (no due date)

JIRA
  6. PAYFLEX-380 — Decode payment method     → suggested: 1h    [In Progress]
  7. PAYFLEX-391 — Fix CCToken null crash    → suggested: 1h    [To Do]

Duration options: 15m / 30m / 45m / 1h / 1.5h / 2h / 3h / half-day
Reply "ok" to accept all, or correct specific ones.
```

**Study/research tasks with unclear scope** (e.g. "what is X", "learn about Y", "study Z") — ask the user: "Quick overview (30m–1h) or deep dive (2h+)?" before assigning a duration. Don't default to 1h without checking.

**Duration suggestions for Todoist tasks:**
- `[FU]` prefix = Follow Up task → **default 10 min**, **weekdays only** (requires a live response — never schedule on weekends)
- p1 tasks → 1h; Code review / PR review → 30m; Bug fix → 1h
- Writing / documentation → 30m; Feature implementation → 1.5h
- Survey / form → 15m; Simple upload / git push → 30m; Resume update → 30m
- **Shopping label tasks** → minimum **1 hour** (searching, comparing, deciding all takes time — even for online purchases)

**Duration for Jira tasks — use story points:**

| Story Points | Estimated Days | Schedule as |
|---|---|---|
| 0.5 | < 1 day | Time block (4h default) |
| 1 | 1–2 days | All-day event × 1 day |
| 2 | 2–3 days | All-day event × 2 days |
| 3 | 3–5 days | All-day event × 4 days |
| 5 | 5–8 days | All-day event × 6 days |
| No SP | unknown | Ask user |

Use the midpoint of each range as the default day count. Show the SP and estimated days to the user:
```
JIRA
  5. PAYFLEX-380 — Decode payment method  [In Progress]  SP: 2  → suggested: 2-day all-day block
  6. PAYFLEX-391 — Fix CCToken null crash  [To Do]       SP: 1  → suggested: 1-day all-day block
  7. PAYFLEX-405 — Card page migration     [To Do]       SP: 3  → suggested: 4-day all-day block
  8. PAYFLEX-412 — Quick config fix        [To Do]       SP: 0.5 → suggested: 4h time block
```

Wait for reply before proceeding.

---

## Step 4: Distribute Tasks Across Days

After duration confirmations, assign each task to a day then fill time slots.

**Day assignment rules (in order):**
1. Tasks with a **specific due date** → assign to that day (or earliest available day if that day is full)
2. Tasks that are **overdue** → assign to today first, then overflow to tomorrow
3. Jira "In Progress" → assign to earliest available weekday
4. Remaining tasks (no due date) → fill days in order (Mon → Fri → Sat → Sun) by priority

**Within each day**, fill zones sequentially by priority:

*Work zone (weekdays):*
1. Work Todoist p1 → 2. Jira In Progress → 3. Work Todoist p2 → 4. Jira To Do/Review → 5. Work Todoist p3

*Personal zone:*
1. Non-work Todoist tasks by priority

**Slot rules:**
- Lunch placeholder at 12:00–13:00 on weekdays if free (🍽️)
- Exercise placeholder at 18:00–19:30 on weekdays (🏋️)
- Tasks that overflow a day → move to next available day
- Tasks with no room in the full period → **Unscheduled** list

---

## Step 5: Present the Schedule

**Daily mode** — single day view (same as before).

**Weekly mode** — show each day as a collapsible section:

```
📅 Weekly Schedule — March 7–13, 2026

─── Saturday, March 7 (Personal day) ───────────────────
09:00 – 10:00   📚 Study investing chapter 3
10:00 – 10:30   🛒 Buy groceries
20:30 – 21:00   🕐 Buffer

─── Sunday, March 8 (Personal day) ────────────────────
(free — no personal tasks remaining)

─── Monday, March 9 ────────────────────────────────────
09:00 – 10:00   🔨 Fix payment bug (Todoist p1)
10:00 – 10:30   👀 Review PR from Tor (Todoist p2)
...
12:00 – 13:00   🍽️ Lunch
...
18:00 – 19:30   🏋️ Exercise
(no personal tasks)

─── ... (Tue–Fri) ───────────────────────────────────────

⚠️ Unscheduled (no room this week):
  - Task X (p3) — consider next week

Total: 14 work blocks, 4 personal blocks across 5 days

Reply "confirm" to create all as Google Calendar blocks, "edit [day]" to adjust a specific day, or "cancel".
```

Wait for reply.

---

## Step 6: Create Calendar Events (on "confirm")

Create all events in parallel across all days.

**Todoist tasks and 0.5 SP Jira tasks — timed blocks:**
```
mcp__google-workspace__create_event:
- summary: "{emoji} {task name}" — pick emoji based on task type:
  - 📞 [FU] / follow-up tasks
  - 📝 survey / form / documentation
  - 📤 upload / git push
  - 🛍️ shopping / buying items
  - 📄 resume / CV / admin documents
  - 💰 investment purchases (buying stock, fund, ETF)
  - 📊 investment study / research (use 📊 not 📈 — renders better in calendar)
  - ✈️ travel planning
  - 📚 learning / studying
  - ✅ sign-off / approval
  - 🧪 testing / QA
  - 🚀 launch / deploy / release
  - 🔍 investigation / research / find
  - 🔨 bug fix / implementation / coding (default for generic work tasks)
  - 🏋️ workout / exercise events (always prefix workout events)
  - 🔷 PAYFLEX-XXX — {summary} (Jira timed block)
- start: "{date}T{start_time}:00+07:00"
- end: "{date}T{end_time}:00+07:00"
- description: "Priority: {p1/p2/etc} | Source: Todoist/Jira | SP: {story_points}"
- colorId: Todoist Work → "9" (blueberry), Todoist Personal → "7" (teal), Jira 0.5SP → "6" (tangerine)
```

**Jira tasks with SP ≥ 1 — all-day events spanning N weekdays:**
```
mcp__google-workspace__create_event:
- summary: "[PAYFLEX-XXX] {summary}  (SP: {story_points})"
- start: "{start_date}"          ← date only, no time (all-day format)
- end: "{end_date}"              ← date only, exclusive end (last day + 1)
- allDay: true
- description: "SP: {story_points} | Est: {N} days | Status: {status}"
- colorId: "6" (tangerine)
```

All-day events span only **weekdays** — skip Saturdays and Sundays when counting days. Start from the earliest available day in the schedule.

After creating calendar events, **update Todoist task due dates** to match the scheduled day — run in parallel with the calendar event creation:

```
mcp__todoist__update-tasks:
- id: {task_id}
- dueString: "{YYYY-MM-DD}"   ← the day the task is scheduled
```

Do this for every Todoist task that was assigned to a specific day. Skip tasks that were already excluded by the user or placed in Unscheduled.

After all events and task updates are complete:
```
✅ Created 18 calendar blocks across 5 days (Mar 7–13).
   Updated 12 Todoist task due dates to match.
   Open Google Calendar to review: https://calendar.google.com
```

If "edit [day]" → re-present just that day, wait for confirmation, update only that day's events.
If "cancel" → acknowledge and stop.

---

## Step 7: Verify — No Overlaps Before Declaring Done

**MANDATORY after any batch of calendar changes** (creating, updating, or deleting events).

Do NOT say "done", "clean", or "no more overlaps" based on mental reasoning alone. Always verify:

1. Re-fetch the affected day(s) using `gcal_list_events`
2. Sort all timed events by start time
3. Walk through consecutive pairs: if `event[i].end > event[i+1].start` → overlap found
4. Ignore expected soft overlaps: Jira all-day blocks (10:00–17:00) containing Lunch (12:00–13:00) — this is by design
5. Only after this check passes → report "✅ Calendar is clean"

**If new overlaps are found after changes:** fix them first, then re-verify. Repeat until the check passes clean.

---

## Notes

- Notion is intentionally excluded — it's a reference/second brain, not an action list.
- If calendar data is unavailable for the period, assume full free windows and note the assumption.
- Weekly mode deduplicates tasks — each task appears only once in the schedule, not repeated each day.

## Recurring Blocks & Daily Routine

See `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Personal/contexts/personal.md` → **Scheduling Context** section. It contains the full recurring blocks table, daily routine, zone hours, and duration rules. Treat all recurring blocks as busy — never reschedule or duplicate them.
