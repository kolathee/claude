---
name: commit-skills
description: >-
  Commit and push skill file changes in ~/.claude to the GitHub remote.
  Use when the user says "commit skill changes", "push skills to github",
  "save skills", or after modifying/creating skills in ~/.claude/skills/.
---

# Commit Skills to GitHub

Commit and push changes in `~/.claude` to `https://github.com/kolathee/claude`.

## Repo

```
~/.claude   →   https://github.com/kolathee/claude.git (main)
```

## Workflow

### Step 1: Check Status

```bash
git -C ~/.claude status
git -C ~/.claude diff --stat
```

### Step 2: Show the User What Will Be Committed

List the changed/untracked files. If nothing to commit, say so and stop.

### Step 3: Stage and Commit

Stage all relevant skill changes:

```bash
git -C ~/.claude add skills/ MEMORY.md settings.json
# or scope to specific files if only some changed
```

Commit with a short message describing what changed:

```bash
git -C ~/.claude commit -m "$(cat <<'EOF'
u
EOF
)"
```

Use commit message `u` to match the repo's existing style (check `git -C ~/.claude log --oneline -3`).

### Step 4: Push

```bash
git -C ~/.claude push
```

**If push fails (auth):** Ask user to run `! git -C ~/.claude push` in terminal — GitHub credential prompt may require interactive input.

### Step 5: Verify

```bash
git -C ~/.claude log --oneline -3
git -C ~/.claude status
```

Confirm branch is up to date with `origin/main`.
