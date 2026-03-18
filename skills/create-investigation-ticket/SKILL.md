---
name: create-investigation-ticket
description: This skill should be used when the user provides a Slack thread URL and asks to "create an investigation ticket", "log this as a Jira", "create a bug ticket", "raise a ticket for this", "create ticket from this", "put this in the backlog", or "file a Jira for this issue". Reads the Slack thread, analyzes the issue, and creates a structured investigation Task in Jira PAYFLEX.
---

# Create Investigation Ticket from Slack Thread

Read a Slack alert/escalation thread, extract the issue details, and create a structured Jira investigation Task in PAYFLEX.

## Workflow

### Step 1: Parse the Slack URL

Extract `channel_id` and `message_ts` from the Slack URL:

```
URL format: https://agoda.slack.com/archives/{channel_id}/p{timestamp}
Example:    https://agoda.slack.com/archives/CBWNA1VGX/p1773308779637739
```

To convert the `p`-prefixed timestamp to Jira `message_ts` format:
- Take the digits after `p`: `1773308779637739`
- Insert a dot before the last 6 digits: `1773308779.637739`

### Step 2: Read the Slack Thread

Use `mcp__plugin_slack_slack__slack_read_thread` with the parsed values:

```
channel_id: {extracted channel_id}
message_ts: {converted timestamp with dot}
```

Read all replies to get the full picture — SRE AI summaries, team responses, and any follow-up diagnosis.

### Step 3: Analyze the Issue

From the thread, extract:

- **Error / alert pattern**: the exact error or log pattern that triggered the alert
- **Affected component**: which service/component is throwing the error (e.g., `cronos-cashback`, `mspa`)
- **Trigger**: what deployment, SDK bump, experiment, or change caused it
- **Root cause hypothesis**: what is actually failing and why (from SRE AI Agent reply or team diagnosis)
- **Severity**: LOW / MEDIUM / HIGH and whether it blocks users
- **Action items**: concrete steps needed to fix or investigate further
- **Stakeholders**: who is involved (Sangit, team handles, etc.)

### Step 4: Create the Jira Task

Use `mcp__plugin_productivity_atlassian__createJiraIssue` with:

```
cloudId:       agoda.atlassian.net
projectKey:    PAYFLEX
issueTypeName: Task
contentFormat: markdown
```

**Summary format**: `[Investigation] {short description of the error}`

**Description template**:

```markdown
## Summary

{1-2 sentence description of the error and when/where it occurs}

## Error Pattern

```
{exact error or log pattern}
```

{description of what fails and why}

## Trigger

- {what change/deployment/experiment introduced this}
- {related Jira ticket if mentioned, e.g. PAYFLEX-NNN}

## Hypothesis

{root cause hypothesis from SRE AI Agent or team discussion}

## Severity

**{LOW|MEDIUM|HIGH} / {Non-blocking|Blocking}** — {one-line impact statement}

## Action Items

- [ ] {first investigation step}
- [ ] {fix or guard to implement}
- [ ] {coordination needed, e.g. with SDK owner}

## References

- Slack thread: {original slack URL}
- Grafana log: {grafana link from thread, if any}
- Escalation: {escalation link, if any}
```

### Step 5: Return the Result

Share the created ticket key and link with the user, e.g.:

```
Ticket created: **PAYFLEX-416** — https://agoda.atlassian.net/browse/PAYFLEX-416
```

## Notes

- Project is always `PAYFLEX` unless the user specifies otherwise
- Issue type is always `Task` for investigation tickets
- No need to set assignee — leave unassigned so it goes to backlog
- Keep the summary concise but include `[Investigation]` prefix for discoverability
- If the SRE AI Agent reply is present in the thread, use it as the primary source for root cause and recommended actions
- If the thread has no clear root cause yet, still create the ticket — describe what is known and mark action items as "TBD"
