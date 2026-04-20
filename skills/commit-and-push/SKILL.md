---
name: commit-and-push
description: >-
  Group related changes into logical commits and push to remote.
  Use when the user says "commit and push", "separate into commits",
  "group changes into commits", "push changes", "commit push",
  or asks to organize, commit, and push their working tree changes.
---

# Commit and Push

Group unstaged/staged changes into logical commits and push to remote, with GitLab token fallback when SSH fails.

## Workflow

### Step 1: Gather Context

Run in parallel:
- `git status`
- `git diff --name-only` — all changed files
- `git diff --stat` — change size per file
- `git log --oneline -5` — recent commit style
- `git branch -vv | grep '\*'` — current branch and remote tracking

### Step 2: Understand the Changes

Read the diff for each changed file to understand what changed:
```bash
git diff <file>
```

Group files by logical change (e.g., core logic, data flow wiring, tests). Each group becomes one commit.

### Step 3: Run Local Tests

Before committing, run the local tests that cover the changed files to make sure nothing is broken.

**Detect the project and test runner:**
- Node / TypeScript / JavaScript — look for `package.json` and run the repo's test script (e.g., `npm test`, `yarn test`, `pnpm test`, `jest`, `vitest`)
- .NET / C# — look for `.sln` or `.csproj` and run `dotnet test`
- Scala / SBT — look for `build.sbt` and run `sbt test` (or the skill-provided runner, e.g., the `booking-query/dev` skill)
- Python — look for `pytest.ini` / `pyproject.toml` / `setup.py` and run `pytest`
- Other — use the repo's documented test command (check `README.md`, `CLAUDE.md`, or `Makefile`)

**Scope the run when possible:**
- Prefer running only the tests that cover the changed files (e.g., `jest <pattern>`, `pytest <path>`, `dotnet test --filter`)
- If scoping is unclear or the change is broad, run the full suite
- Use the repo's own conventions from `CLAUDE.md` / `AGENTS.md` / rule files when available

**If tests fail:**
1. Read the failure output carefully
2. Decide whether the test or the implementation is wrong
3. Fix the issue (edit code and/or tests)
4. Re-run the failing tests until they pass
5. Re-run the broader scope once more to confirm no regressions
6. Only then proceed to the next step

**If tests pass:** proceed to Step 4.

Include any fixes made here in the commit plan below (they may belong in the same commit as the related change, or in their own "fix tests" commit).

### Step 4: Plan Commits

Present a brief plan to the user showing:
- Number of commits
- What each commit contains (files + summary)

If the user has expressed a preference or the grouping is clear from context, skip confirmation and proceed.

### Step 5: Create Commits

For each logical group, stage and commit sequentially:

```bash
git add <file1> <file2> ...

git commit -m "$(cat <<'EOF'
Short summary line

Optional longer explanation of why, not what.
EOF
)"
```

**Commit message rules:**
- Follow the repo's existing commit style (check `git log`)
- First line: concise summary (imperative mood)
- Body (optional): explain *why*, not *what*
- No comments, no emojis unless the repo uses them

### Step 6: Push

```bash
git push
```

**If SSH fails** (permission denied, no identities):

1. Ask the user for a GitLab personal access token
2. Get the remote URL: `git remote get-url origin`
3. Extract the project path (e.g., `full-stack/mmb/mmbweb.git`)
4. Push via HTTPS:
   ```bash
   git push https://oauth2:<TOKEN>@<HOST>/<PROJECT_PATH> <BRANCH_NAME>
   ```

### Step 7: Verify

Run `git status` and `git log --oneline -<N>` (where N = number of new commits) to confirm everything is clean and pushed.

## Notes

- If there are no changes to commit, tell the user — don't create empty commits
- If the branch has no upstream, use `git push -u origin HEAD`
- Keep tests with their implementation in the same commit when possible
- Never amend commits that have already been pushed
