---
name: report-for-today
description: Generate an interactive HTML daily summary report with calendar, Todoist, Jira, and Notion tasks
---

# Today Report Skill

Generate a beautiful, interactive HTML report of today's tasks and calendar events.

## Step 0: Load Context

Before doing anything else, read `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/contexts/mcp-settings.md`. It contains:
- Tool names for each data source (Outlook, Google Calendar, Todoist, Jira, Notion)
- Notion auth token and database IDs
- Outlook MCP URL and troubleshooting notes
- Report template location and output path

Use those values throughout this skill.

---

## Execution Steps

### 1. Query All Data Sources (IN PARALLEL)

Execute these queries in parallel for maximum speed. Treat each result as either ✅ success or ❌ error — track which tools failed.

**Outlook Calendar:**
```
mcp__plugin_agoda-skills_outlook__list_events:
- startDateTime: "{TODAY}T00:00:00+07:00"
- endDateTime: "{TODAY}T23:59:59+07:00"
- preferredTimeZone: Asia/Bangkok
```

**Google Calendar:**
```
mcp__google-workspace__list_events:
- timeMin: "{TODAY}T00:00:00+07:00"
- timeMax: "{TODAY}T23:59:59+07:00"
- timeZone: "Asia/Bangkok"
- maxResults: 50
```

**Todoist:**
```
mcp__todoist__find-tasks-by-date:
- startDate: "today"
- limit: 25
```

**Jira:**
```
mcp__plugin_agoda-skills_at__searchJiraIssuesUsingJql:
- cloudId: agoda.atlassian.net
- jql: project = PAYFLEX AND assignee = currentUser() AND status IN ("To Do", "In Progress", "Testing", "Code Review") ORDER BY status DESC, updated DESC
- fields: ["summary", "status", "priority"]
- maxResults: 15
```

**Notion Work List:**

The `notion-search` tool does NOT support property-based filtering — it only does semantic/keyword search on page content. The only reliable approach is a broad search scoped to the Work List database, then verify each page's Status by fetching it.

```
mcp__plugin_productivity_notion__notion-search:
- query: "a"
- query_type: "internal"
- data_source_url: "collection://87609b4b-ec27-4b71-a779-6337cf482ec0"
```

This returns the 10 most recently modified pages in the Work List. Then fetch ALL returned pages in parallel using `mcp__plugin_productivity_notion__notion-fetch` to read the `Status` property from each page's `<properties>` block.

Show only pages whose Status is one of: "In progress", "Monitoring", "Blocked", "Review | Testing", "Merging", "Wait to run", "Backlog"
Exclude: "Done", "Not started", "Suspended"

### 1b. Pre-flight Validation (REQUIRED before generating report)

After the parallel fetch completes, check every source for errors **before doing anything else**.

A source has **failed** if its tool call returned an error, exception, or auth-related message (e.g., "unauthorized", "token expired", "failed to fetch"). Empty results (zero events, zero tasks) are **not** failures — that's valid data.

**If ALL sources succeeded** → proceed directly to step 2.

**If ANY source failed:**

1. **Stop** — do not generate the report yet.
2. **Notify the user** with a clear summary, for example:
   > ⚠️ Some data sources need re-authentication before I can generate the report:
   > - ❌ Outlook Calendar — auth error
   > - ❌ Notion — failed to fetch
   > - ✅ Google Calendar — OK
   > - ✅ Todoist — OK
   > - ✅ Jira — OK
   >
   > Please re-authenticate the failed sources, then reply "retry" (or "skip [source]" to omit a source).

3. **Wait for the user's reply.**
4. On "retry" → re-fetch **only the failed sources** in parallel, then repeat this validation step.
5. On "skip [source]" → mark that source as intentionally empty and proceed.
6. Repeat until all sources are either successful or explicitly skipped.

Only proceed to step 2 once all sources are resolved.

### 2. Load HTML Template

Read the template file from:
```
~/.claude/skills/today-report/templates/daily-report.html
```

### 3. Process Data and Generate HTML Content

#### Calendar Content
Merge Google and Outlook calendars. Format as:

```html
<div class="event all-day">🚨KTC Payment Due</div>
<div class="event"><strong>18:00</strong> - Push day 🏋️</div>
<div class="ooo"><strong>OOO:</strong> Gaurav (until Feb 24), Tor (Feb 23-27), Harshit (until Mar 6), Jadis (maternity until Jun 15)</div>
```

Rules:
- **EXCLUDE events with empty/blank titles** - skip any calendar events that have no subject/title
- All-day events (except OOO/PTO) get `class="event all-day"`
- Timed events show time in bold
- **OOO/PTO events: ALWAYS include the date range or return date** (e.g., "Gaurav (until Feb 24)", "Tor (Feb 23-27)")
  - Format: "Name (until Date)" for single end date, "Name (StartDate-EndDate)" for date ranges
  - List names with dates in `<div class="ooo">` but don't show individual OOO events in the timeline
- If no events: `<div class="no-data">No events today</div>`

#### Todoist Content
**IMPORTANT: Always group tasks by Labels dynamically**

**Process:**
1. Analyze all tasks and collect unique labels from the API response
2. Group tasks by their labels (tasks can have multiple labels - include them in the first label group)
3. Create one subsection per unique label found
4. Tasks with no labels go in "No Label" section at the end

Generate grouped table HTML with subsections for each label:

```html
<div class="subsection">
    <h3 class="subsection-title">Work</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 40px;"></th>
                <th style="width: 35%;">Task</th>
                <th>Notes</th>
                <th style="width: 80px;">Priority</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><input type="checkbox" class="task-checkbox" data-task-id="TASK_ID" onchange="toggleTaskComplete(this, 'TASK_ID')"></td>
                <td><span class="task-text">Task name here</span></td>
                <td><div class="task-desc">• Some note<br>• <a href="https://example.com" target="_blank">Link text</a></div></td>
                <td><span class="priority-p4">p4</span></td>
            </tr>
            <tr>
                <td><input type="checkbox" class="task-checkbox" data-task-id="TASK_ID2" onchange="toggleTaskComplete(this, 'TASK_ID2')"></td>
                <td><span class="task-text">Task with no description</span></td>
                <td></td>
                <td><span class="priority-p2">p2</span></td>
            </tr>
        </tbody>
    </table>
</div>

<div class="subsection">
    <h3 class="subsection-title">No Label</h3>
    <table>
        <thead>
            <tr>
                <th style="width: 40px;"></th>
                <th style="width: 35%;">Task</th>
                <th>Notes</th>
                <th style="width: 80px;">Priority</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><input type="checkbox" class="task-checkbox" data-task-id="TASK_ID3" onchange="toggleTaskComplete(this, 'TASK_ID3')"></td>
                <td><span class="task-text">Unlabeled task</span></td>
                <td></td>
                <td><span class="priority-p2">p2</span></td>
            </tr>
        </tbody>
    </table>
</div>
```

**Important:**
- **Dynamically discover labels** - don't hardcode label names, use whatever labels exist in the API response
- **Group tasks by their first label** - if a task has multiple labels, place it under its first label only
- Tasks with empty labels array should go in "No Label" section at the end
- Within each label group, sort tasks by priority (p1 → p2 → p3 → p4)
- Each checkbox must have a unique `data-task-id` attribute (use the actual Todoist task ID)
- Task name goes in `<span class="task-text">` inside its own `<td>` for strikethrough effect
- **Task description** goes in a separate `<td>` as `<div class="task-desc">`:
  - Convert markdown links `[text](url)` → `<a href="url" target="_blank">text</a>`
  - Convert leading `- ` on each line → `• `
  - Skip blank lines and `---` separator lines
  - Convert newlines → `<br>`
  - If description is empty, render an empty `<td></td>`
- Priority classes: `priority-p1`, `priority-p2`, `priority-p3`, `priority-p4`
- Checkbox state persists via localStorage
- If no tasks: `<div class="no-data">No tasks for today</div>`

#### Jira Content
Generate table HTML:

```html
<table class="jira-table">
    <thead>
        <tr>
            <th style="width: 120px;">Key</th>
            <th>Summary</th>
            <th style="width: 110px;">Status</th>
            <th style="width: 90px;">Priority</th>
            <th style="width: 70px;">Link</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>PAYFLEX-380</strong></td>
            <td>[Card Page] Workaround: decode and verify selected payment method type</td>
            <td><span class="status-badge status-in-progress">In Progress</span></td>
            <td><span class="jira-priority-medium">Medium</span></td>
            <td><a href="https://agoda.atlassian.net/browse/PAYFLEX-380" target="_blank" class="link-btn">Open</a></td>
        </tr>
    </tbody>
</table>
```

Status badge classes: `status-in-progress`, `status-monitoring`, etc.
Priority classes: `jira-priority-medium`, `jira-priority-low`, `jira-priority-high`
If no issues: `<div class="no-data">No open issues</div>`

#### Notion Content
Generate grouped tables by status:

```html
<div class="subsection">
    <table class="notion-table">
        <thead>
            <tr>
                <th>Task</th>
                <th style="width: 110px;">Status</th>
                <th style="width: 150px;">Component</th>
                <th style="width: 100px;">Type</th>
                <th style="width: 70px;">Link</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Card Page Migration (webview)</td>
                <td><span class="status-badge status-in-progress">In progress</span></td>
                <td>CronosCashback</td>
                <td>🌟 feature</td>
                <td><a href="https://www.notion.so/PAGE_ID" target="_blank" class="link-btn">Open</a></td>
            </tr>
        </tbody>
    </table>
</div>
```

Group by status: "In Progress", "Monitoring", "Review | Testing", "Merging", "Wait to run", "Backlog"
If no tasks: `<div class="no-data">No active work items</div>`

### 4. Replace Placeholders

Replace these placeholders in the template:

- `{{DATE}}` - ISO date (e.g., "2026-02-22")
- `{{DATE_FULL}}` - Full date (e.g., "Saturday, February 22, 2026")
- `{{CALENDAR_CONTENT}}` - Generated calendar HTML
- `{{TODOIST_COUNT}}` - Number of tasks
- `{{TODOIST_CONTENT}}` - Generated Todoist table HTML
- `{{JIRA_COUNT}}` - Number of open issues
- `{{JIRA_CONTENT}}` - Generated Jira table HTML
- `{{NOTION_COUNT}}` - Number of active work items
- `{{NOTION_CONTENT}}` - Generated Notion grouped tables HTML

### 5. Save and Open Report

1. **Ensure directory exists**:
   - Create `~/daily-reports/` if it doesn't exist

2. **Archive old report** (if exists):
   - Check if `~/daily-reports/daily-summary-{TODAY}.html` exists
   - If yes, archive it: move to `~/daily-reports/daily-summary-{TODAY}-{TIMESTAMP}.html`

3. **Save new report**:
   - Write final HTML to `~/daily-reports/daily-summary-{TODAY}.html`

4. **Auto-open**:
   - Use `open ~/daily-reports/daily-summary-{TODAY}.html` to open in default browser
   - Inform user: "Report generated and opened: ~/daily-reports/daily-summary-{TODAY}.html"

## Features

- **Dark Mode**: Toggle button in header (persists via localStorage)
- **Print Friendly**: Print button generates clean printable version
- **Clickable Links**: Direct links to Jira tickets and Notion pages
- **Responsive Design**: Works on all screen sizes
- **Color Coded**: Visual indicators for priorities and statuses
- **Archived Reports**: Old reports saved to `~/daily-reports/`

## Error Handling

Auth errors and tool failures are caught in step 1b — the report is never generated with missing data unless the user explicitly skips a source.

If a source returns empty results (zero events, zero tasks) after a successful call, that's valid — render `<div class="no-data">...</div>` for that section as normal.

## Output Location

Primary: `~/daily-reports/daily-summary-{YYYY-MM-DD}.html`
Archive: `~/daily-reports/daily-summary-{YYYY-MM-DD}-{TIMESTAMP}.html`

## Example Usage

User runs: `/today-report`
Result:
1. Queries all data sources in parallel
2. Generates beautiful HTML report
3. Archives old report if exists
4. Opens new report in browser
5. Shows: "✅ Report generated: ~/daily-reports/daily-summary-2026-02-22.html"
