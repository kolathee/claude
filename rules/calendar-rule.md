# Calendar Rule — Always Check Before Creating

## Rule

**Before creating any event** in Google Calendar (or any managed calendar), always check if the time slot is free first.

## Workflow

1. Call `gcal_list_events` or `gcal_find_meeting_times` to check the target time slot
2. **If free** -> create the event immediately, no need to ask
3. **If conflict exists** -> do NOT create. Instead:
   - Tell the user what's already there (event name + time)
   - Ask what they want to do
   - Suggest options:
     - Keep new event, move the existing one
     - Reschedule the new event (suggest alternative free slots)
     - Override / create anyway (if user insists)

## Applies To

- All `gcal_create_event` calls
- All `mcp__plugin_agoda-skills_outlook__create_event` calls
- Any calendar event creation regardless of the tool used

## Exception

- "Leave reminder" / travel buffer events: still check, but if the conflict is the event itself (e.g., the destination event), that's expected — create the reminder anyway.
