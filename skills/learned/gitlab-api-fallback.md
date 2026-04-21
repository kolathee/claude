# GitLab API Fallback When MCP Token Expires

## Pattern: Use curl with personal access token

When the GitLab MCP server returns `401 Unauthorized` / `Token is expired`, fall back to direct API calls with the user's personal access token.

### Common operations

**List unresolved MR discussions:**
```bash
curl -s --header "PRIVATE-TOKEN: $TOKEN" \
  "https://gitlab.agodadev.io/api/v4/projects/$PROJECT/merge_requests/$IID/discussions?per_page=100"
```

**Reply to a discussion thread:**
```bash
curl -s --request POST --header "PRIVATE-TOKEN: $TOKEN" \
  "https://gitlab.agodadev.io/api/v4/projects/$PROJECT/merge_requests/$IID/discussions/$DISCUSSION_ID/notes" \
  --data-urlencode "body=Your reply"
```

**Resolve a thread:**
```bash
curl -s --request PUT --header "PRIVATE-TOKEN: $TOKEN" \
  "https://gitlab.agodadev.io/api/v4/projects/$PROJECT/merge_requests/$IID/discussions/$DISCUSSION_ID" \
  --data "resolved=true"
```

**Get MR diffs:**
```bash
curl -s --header "PRIVATE-TOKEN: $TOKEN" \
  "https://gitlab.agodadev.io/api/v4/projects/$PROJECT/merge_requests/$IID/changes?per_page=100"
```

Note: URL-encode the project path (e.g., `full-stack%2Fcart%2Ftrips-web`).
