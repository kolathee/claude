---
name: web-fetch
description: Fetch web content when Claude's WebFetch is blocked (403, paywall, JS-rendered pages). Use when accessing any URL that fails — news sites, company pages, investment data, Reddit, documentation, etc.
---

# Web Fetch

Use when `WebFetch` is blocked, returns 403, or the site requires JavaScript rendering.

## Method 1: Gemini CLI via tmux (Try First)

Gemini can browse and summarize any URL. Best for JS-heavy sites, paywalls, or complex queries.

Pick a unique session name (e.g., `gemini_abc123`) and use it consistently.

### Setup

```bash
tmux new-session -d -s <session_name> -x 200 -y 50
tmux send-keys -t <session_name> 'gemini' Enter
sleep 3
```

If you need a specific model: replace `gemini` with `gemini -m gemini-2.5-pro`. If that returns API/quota errors, kill the session and retry with just `gemini`.

### Send query and capture output

```bash
tmux send-keys -t <session_name> 'Fetch and summarize https://example.com — extract X, Y, Z' Enter
sleep 30  # adjust up to 90s for complex pages
tmux capture-pane -t <session_name> -p -S -500
```

### How to tell if Enter was sent

**Enter NOT sent** — query is still INSIDE the input box:
```
╭─────────────────────────────────────╮
│ > Your query text here              │
╰─────────────────────────────────────╯
```

**Enter WAS sent** — query is OUTSIDE the box, processing activity visible:
```
> Your query text here

⠋ Thinking...

╭────────────────────────────────────────────╮
│ >   Type your message or @path/to/file     │
╰─────────────────────────────────────────────╯
```

If query is still inside, run: `tmux send-keys -t <session_name> Enter`

### Cleanup

```bash
tmux kill-session -t <session_name>
```

---

## Method 2: curl (Fallback)

Best for sites with clean JSON APIs or when Gemini is unavailable.

### Basic fetch

```bash
curl -s -L \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -o /tmp/web_result.html \
  -w "%{http_code}" \
  "https://example.com/page"
```

`-o /tmp/file` saves response, `-w "%{http_code}"` prints HTTP status for debugging.

### Sites with JSON APIs

Some sites expose clean JSON — append `.json` or use API endpoints directly:

```bash
# Reddit
curl -s -L -H "User-Agent: ..." "https://old.reddit.com/r/SUBREDDIT/hot.json?limit=15"

# Parse with jq
jq -r '.data.children[] | .data | "\(.title)\n  \(.score) pts | u/\(.author)\n"' /tmp/web_result.html
```

### Rate limiting tips

- Make requests sequentially with `sleep 2` between each — never parallel
- Empty response (0 bytes): wait 3-5s and retry
- HTTP 429: back off 10-15s
