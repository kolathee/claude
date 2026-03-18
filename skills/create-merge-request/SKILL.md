---
name: create-merge-request
description: Create a GitLab merge request with the repo's MR description template. Use when the user says "create MR", "open merge request", "create merge request", "push and create MR", or "open MR".
---

# Create GitLab Merge Request

Create a merge request on GitLab using the repo's own MR description template via the GitLab MCP.

## Prerequisites

- GitLab MCP server (`@zereight/mcp-gitlab`) must be configured and running
- Changes committed and pushed to a remote branch

## Workflow

### Step 1: Gather Context

Run these in parallel:
- `git status` — check for uncommitted changes
- `git log --oneline -5` — recent commits for the branch
- `git branch -vv | grep '\*'` — current branch and remote tracking
- `git diff develop...HEAD --stat` — files changed vs develop
- `git remote get-url origin` — get GitLab project path

If there are uncommitted changes, ask the user if they want to commit first.
If the branch hasn't been pushed, push with `git push -u origin HEAD`.

### Step 2: Read the MR Template

Look for the repo's MR description template:

```
# Common locations (check in order):
.gitlab/merge_request_templates/Default.md
.gitlab/merge_request_templates/default.md
docs/merge_request_templates/Default.md
```

Read the template file. If no template exists, use a simple summary format.

### Step 3: Extract Info

From the branch name and commits, infer:
- **Jira ID**: extract from branch name or commit messages (e.g., `PAYFLEX-387`)
- **Title**: use the commit message or branch context (e.g., `[PAYFLEX-387] Description`)
- **Project path**: extract from `git remote get-url origin` (e.g., `full-stack/mobile/ios/client-ios`)

### Step 4: Fill the Template

Take the template from Step 2 and fill it in:

1. **Replace placeholder comments** like `<!-- IMPORTANT: WRITE YOUR DESCRIPTION -->` with the actual description summarizing changes from the diff
2. **Replace Jira placeholders** like `[JiraID](...)` with the real Jira link
3. **Remove sections the user hasn't provided info for** (e.g., "Story design", "UI design") — remove the line entirely rather than leaving it blank
4. **Fill in test spec** with relevant test items based on the changes
5. **Keep all boilerplate sections** (How to merge, Reminder, etc.) as-is from the template
6. **Add `Related to {JIRA_ID}`** at the bottom if not already present

### Step 5: Confirm with the User

**MANDATORY**: Present the proposed **title** and **filled-in description** to the user. Ask if they want to adjust or change anything. Do NOT create the MR until the user explicitly confirms.

### Step 6: Create MR via GitLab MCP

Only after user confirmation, use the `create_merge_request` tool:

```
CallMcpTool(
  server: "user-gitlab",
  toolName: "create_merge_request",
  arguments: {
    "project_id": "{PROJECT_PATH}",
    "title": "{MR_TITLE}",
    "source_branch": "{BRANCH_NAME}",
    "target_branch": "develop",
    "remove_source_branch": true,
    "description": "{FILLED_TEMPLATE}"
  }
)
```

### Step 7: Return the MR URL

Extract `web_url` from the response and share it with the user.

## Notes

- Target branch is always `develop` unless user specifies otherwise
- Set `remove_source_branch: true` by default
- Each repo may have a different template — always read from the repo, never hardcode
- If GitLab MCP is not available, fall back to providing the MR creation URL from `git push` output
- NEVER create the MR without user confirmation first
