---
name: resolve-merge-conflict
description: >-
  Resolve merge conflicts on a branch/MR, verify locally with lint and tests,
  commit, push, and monitor the pipeline until green. Use when the user says
  "resolve merge conflict", "resolve conflicts and push", "fix conflicts on
  this MR", "merge main and monitor", or provides an MR URL and asks to
  resolve conflicts end-to-end. Delegates to /commit-and-push and
  /monitor-pipeline after the conflict resolution is done.
---

# Resolve Merge Conflict

End-to-end flow for an MR that has conflicts with its target branch:

1. Merge the target branch into the MR branch
2. Resolve every conflict (and every broken auto-merge) using the MR's intent
3. Run lint + affected tests locally (see `/commit-and-push` Step 3)
4. Commit the merge and push (see `/commit-and-push` Steps 5–6)
5. Monitor the pipeline until green (see `/monitor-pipeline`)

This skill is a thin wrapper that adds the conflict-resolution step in front
of the commit-and-push and monitor-pipeline skills. For commit, push, and
pipeline monitoring details, **follow those skills** — do not duplicate their
logic here.

## Inputs

Accept any of:
- An MR URL (preferred — gives project, branch, and target in one)
- A branch name + target branch (fallback when no MR exists yet)

If only a branch name is given, assume target = `main` (or the repo's
default branch) unless the user says otherwise.

## Workflow

### Step 1: Identify Project, Branch, and Target

Resolve:
- The repo on disk (the MR's project path should match `git remote get-url origin`)
- The current branch (should match the MR source branch — `cd` to the repo
  and verify with `git branch --show-current`)
- The target branch from the MR (`main`, `master`, `develop`, etc.)

If you have a GitLab token and an MR URL, confirm the MR actually has
conflicts before merging:

```bash
curl -s --header "PRIVATE-TOKEN: <TOKEN>" \
  "https://<HOST>/api/v4/projects/<PROJECT>/merge_requests/<MR_IID>" \
  | python3 -c "import sys, json; d=json.load(sys.stdin); \
    print('has_conflicts:', d.get('has_conflicts'), \
          'merge_status:', d.get('detailed_merge_status'), \
          'source:', d['source_branch'], 'target:', d['target_branch'])"
```

If `has_conflicts` is `false` and the MR is already mergeable, skip to Step 4
(there may still be CI failures to investigate, but no conflict work).

### Step 2: Merge the Target Branch

```bash
git fetch origin <target>
git merge origin/<target> --no-edit
```

Expect `Automatic merge failed; fix conflicts and then commit the result.`
Inspect the conflict set:

```bash
git status --short
```

Conflict markers appear as:
- `UU <file>` — both sides modified (content conflict)
- `AA <file>` — both sides added the same path (add/add)
- `DU` / `UD` — deleted by one side, modified by the other
- `AU` / `UA` — added on one side, modified on the other

**Also watch for silent auto-merges that are wrong.** Auto-merge can cleanly
combine two diffs that together produce duplicate kwargs, duplicate GraphQL
fields, or renamed types from one side that the other side still uses. Grep
broadly for anomalies introduced by the merge (see Step 3c).

### Step 3: Resolve Every Conflict

Default bias: **preserve the MR's intent** (the side being merged into) and
**absorb new structure from target** (renames, signature changes, new
required parameters).

#### 3a: Read both sides first

For each `UU` / `AA` file, read the full file (not just the conflict
hunk) to understand the surrounding context. Conflicts are often a
symptom of structural changes on target that will also break code
elsewhere in the file or repo.

Useful diagnostics:
```bash
git log --oneline HEAD ^MERGE_HEAD -- <file>   # commits only on our side
git log --oneline MERGE_HEAD ^HEAD -- <file>   # commits only on target side
git show :1:<file>  # common ancestor
git show :2:<file>  # our side (HEAD)
git show :3:<file>  # their side (MERGE_HEAD)
```

#### 3b: Edit the file to remove markers

Replace the `<<<<<<< / ======= / >>>>>>>` block with a combined version
that keeps:
- The MR's new fields / methods / tests
- Target's renamed types, new required parameters, and any
  signature/nullability changes

For `AA` test files, merge both sets of tests into the union — rewrite
older-style tests to use the newer builders/helpers the target branch
standardized on, rather than reintroducing deprecated mocks.

Verify all markers are gone across the whole working tree:

```bash
rg -n '^(<<<<<<<|=======$|>>>>>>>)' -- . || echo "all clean"
```

#### 3c: Fix silent auto-merge breakage

Examples that compile-check won't catch from `git status` alone:

- **Duplicate kwargs in generated-type constructors** (e.g. two `paymentDetails = ...` inside the same `.PaymentDetails(...)` call after both sides added one field)
- **Duplicate GraphQL field blocks** (e.g. two `paymentDetails { ... }` blocks on the same selection set — consolidate into one)
- **Renamed generated types** (e.g. target renamed `Address` → `Address1` in Apollo-generated classes; any `TripDetailByBookingIdsQuery.Address` references our side added must be updated)
- **New required constructor parameters** on target (e.g. target added `summary` to a data class; builders we added on our side now need `summary = null`)
- **Deleted files our branch still imports**
- **Lock files** (`yarn.lock` / `pnpm-lock.yaml` / `package-lock.json`) — if the target migrated lockfiles (e.g. yarn → pnpm), delete the stale one and regenerate with `pnpm install --lockfile-only` / `yarn install` as appropriate

#### 3d: `git add` each resolved file

```bash
git add <file>
```

Do this incrementally as you finish each file — `git status` then only
shows remaining conflicts.

### Step 4: Local Verification (lint + tests)

**This is mandatory before the merge commit.** Follow `/commit-and-push`
Step 3 (lint) and Step 3b (tests) on the changed file set:

```bash
git diff --name-only HEAD          # files the merge commit will touch
git diff --name-only --diff-filter=U  # (empty now, but sanity-check)
```

Project-specific pointers:

- **Gradle / Kotlin (trip-api-style)**:
  ```bash
  export JAVA_HOME=$(/usr/libexec/java_home -v 17)  # if multiple JDKs installed
  ./gradlew :<module>:compileKotlin :<module>:compileTestKotlin
  ./gradlew :<module>:test
  ```
  Apollo/GraphQL types are regenerated during compile — a GraphQL
  merge mistake surfaces here as `No value passed for parameter ...`
  or `Unresolved reference: ...`.

- **.NET / C#**:
  ```bash
  dotnet build <Solution>.sln
  dotnet test <UnitTestProject> --filter "FullyQualifiedName~<RelevantClass>"
  ```

- **Node / TypeScript (Jest or Vitest)**: follow the existing
  `/commit-and-push` guidance. Always run lint + `tsc --noEmit` on
  touched files in addition to tests.

If **anything fails**, go back to Step 3b (re-edit) — do not push a
half-resolved merge.

### Step 5: Commit and Push

Delegate to `/commit-and-push` starting at its Step 5, with these
merge-specific notes:

- One commit is fine — the merge commit itself. Don't split the merge
  into multiple commits.
- Use a clear merge commit title, e.g.
  `Merge branch 'main' into feature/<branch-name>`, and a short body
  explaining any non-trivial reconciliation you did.
- Push normally. If SSH fails, fall back to the HTTPS-token push from
  `/commit-and-push` Step 6.

### Step 6: Monitor the Pipeline

Delegate to `/monitor-pipeline` with the same MR/branch. A common
first-failure on the merge commit is `semver_validate_mr` or similar
MR-title validation — fix the MR title and retry the job per
`/monitor-pipeline` Step 5.

### Step 7: Report

Once the pipeline is green, report to the user:
- MR URL
- Pipeline URL and final status
- A one-line summary of the conflicts and how you resolved each
- Local verification result (e.g. "770 tests passed")

## Common Conflict Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| `No value passed for parameter 'X'` after merge | Target added a required field to a generated/data class; our-side builders don't set it | Add the new field (usually `= null` or a sensible default) to every constructor call in test builders |
| `Unresolved reference: TypeName` | Target renamed a generated type (`Address` → `Address1`) | Update all references on our side to the new name |
| Duplicate kwarg compile error (`Argument passed multiple times`) | Auto-merge combined two `foo = ...` lines into the same constructor call | Merge them into a single argument that passes all needed fields |
| GraphQL query has two blocks with the same selection root | Auto-merge kept both sides' `paymentDetails { ... }` | Consolidate into one block with the union of fields |
| Mysterious test failures after clean merge | Stale lockfile or the target migrated package manager | Delete old lockfile, regenerate with new tool |
| `semver_validate_mr` fails on merge commit | MR title doesn't match conventional commits | Update MR title to `feat:` / `fix:` / `chore:` etc., retry the job |

## Notes

- Never push a merge with unresolved `<<<<<<<` markers — always `rg` for
  them before committing.
- Never push a merge that hasn't at least compiled locally. Remote CI
  round-trips for "did it compile?" waste 10–40 minutes each.
- When the target branch carried a huge refactor (renames, moves,
  deletions), expect that the conflict set in `git status` is
  incomplete — walk the diff and grep the repo for stale references
  before committing.
- Do not `--no-ff` or `--ff-only` unless the repo convention requires
  it; plain `git merge origin/<target>` with a merge commit is
  standard.
- If the user's real intent is "rebase onto main" instead of a merge,
  confirm before destroying the branch's commit shape. This skill
  defaults to **merge**, not rebase.
