---
name: monitor-pipeline
description: >-
  Monitor a GitLab CI/CD pipeline, diagnose failures, fix code, and
  retry until all jobs pass. Use when the user says "monitor pipeline",
  "watch pipeline", "fix pipeline", "check pipeline", "babysit pipeline",
  "make pipeline green", or asks to monitor/fix CI until it passes.
---

# Monitor Pipeline

Poll a GitLab MR pipeline via the REST API, diagnose any job failure,
apply a fix, **verify locally**, push, and repeat until the pipeline is green.

## Prerequisites

- A GitLab personal access token (ask the user if not already provided in the conversation)
- The project ID or URL-encoded path (extract from `git remote get-url origin`)
- The MR number or branch name

## Workflow

### Step 0: Local Verification (MANDATORY before every push)

**Never push code without running affected tests locally first.**
The remote pipeline takes 10-40 minutes. A local test run takes 1-2 minutes.
Pushing known-broken code and waiting for the pipeline to confirm the failure is a waste of time.

1. **Identify affected test files.** Use `git diff --name-only` to find changed source files,
   then locate their corresponding test files (same directory, `.test.ts` / `.test.tsx` suffix).
   Also find tests that *import* the changed files — they can break transitively.

2. **Run affected tests locally:**
   ```bash
   cd src/Clientside
   npx jest --no-cache --testPathPattern="(File1\.test|File2\.test|File3\.test)"
   ```

3. **Interpret results:**
   - **All pass** → safe to push
   - **Failures** → fix them, re-run locally, repeat until green
   - **Test suite fails to run** (e.g. `Cannot spy`, `Cannot read properties of undefined`) →
     usually a mock problem. Check if `jest.mock` is replacing entire modules and wiping
     out exports that other utilities (like `mockCmsValues`) depend on.
     Use `jest.requireActual` to preserve originals, or include needed exports in the mock.
   - **`jest.mock` vs `jest.spyOn` conflict** → If the test uses `jest.spyOn(module, 'fn')`
     *and* you added `jest.mock('module')`, the mock replaces the module with non-configurable
     properties that `spyOn` can't redefine. Solution: don't `jest.mock` that module —
     let existing `spyOn` patterns handle it. Or if you must mock, include all properties
     that downstream `spyOn` calls need.

4. **For C# / serverside changes**, build locally if possible:
   ```bash
   cd src/Serverside
   dotnet build Agoda.Cronos.MmbUnitTests/
   dotnet test Agoda.Cronos.MmbUnitTests/ --filter "FullyQualifiedName~RelevantTestClass"
   ```

**CRITICAL: Do NOT skip this step.** Every fix must be verified locally before pushing.
The goal is to push *once* with confidence, not ping-pong between local and remote.

### Step 1: Identify the Pipeline

Resolve the project and latest pipeline:

```bash
# Get project path from remote
git remote get-url origin
# e.g. git@gitlab.agodadev.io:full-stack/mmb/mmbweb.git
# project path → full-stack/mmb/mmbweb  (URL-encode slashes as %2F)
```

Find the latest pipeline for the MR or branch:

```bash
# By MR number
curl -s --header "PRIVATE-TOKEN: <TOKEN>" \
  "https://<HOST>/api/v4/projects/<PROJECT>/merge_requests/<MR_IID>/pipelines?per_page=1"

# By branch (fallback)
curl -s --header "PRIVATE-TOKEN: <TOKEN>" \
  "https://<HOST>/api/v4/projects/<PROJECT>/pipelines?ref=<BRANCH>&per_page=1"
```

Extract the pipeline `id` from the response.

### Step 2: Poll Jobs

List all jobs for the pipeline and summarise their statuses:

```bash
curl -s --header "PRIVATE-TOKEN: <TOKEN>" \
  "https://<HOST>/api/v4/projects/<PROJECT>/pipelines/<PIPELINE_ID>/jobs?per_page=50"
```

Print a compact summary using a python one-liner that groups by status
(success / failed / running / created / manual / skipped).

### Step 3: Wait Loop

If all required jobs are still running or created:

1. Wait 2-5 minutes (scale up for Playwright / integration tests)
2. Re-poll and print the summary
3. Repeat until the pipeline reaches a terminal state (success, failed)

### Step 4: Diagnose Failures

For each **failed** job:

1. Fetch the job trace (log):
   ```bash
   curl -s --header "PRIVATE-TOKEN: <TOKEN>" \
     "https://<HOST>/api/v4/projects/<PROJECT>/jobs/<JOB_ID>/trace" | tail -120
   ```
2. Search for the root cause:
   - `FAIL` / `FAILED` / `Error` lines for test failures
   - `exit code 137` → OOM kill (retry the job, not a code issue)
   - `exit code 1` with no test failure → build/lint error
   - Compiler errors (`error CS`, `error TS`)

### Step 5: Fix or Retry

**OOM / infra flake (exit code 137, timeout, runner issue):**
Retry the job without code changes:
```bash
curl -s --request POST --header "PRIVATE-TOKEN: <TOKEN>" \
  "https://<HOST>/api/v4/projects/<PROJECT>/jobs/<JOB_ID>/retry"
```

**Actual code failure:**
1. Read the failing file(s) locally
2. Apply the fix
3. **Run Step 0 (Local Verification)** — run all affected tests locally until they pass
4. If multiple jobs failed, fix them ALL and verify ALL locally before pushing
5. Commit with a descriptive message explaining the fix
6. Push (use HTTPS token fallback if SSH fails):
   ```bash
   git push https://oauth2:<TOKEN>@<HOST>/<PROJECT_PATH> <BRANCH>
   ```
7. Wait for the new pipeline to start (~30s), then go back to Step 2

### Step 6: Confirm Green

Once the pipeline status is `success`:
- Print the final job summary (all green)
- Report the pipeline URL to the user

## Common Local Test Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Cannot read properties of undefined (reading 'pageTypeId')` | `getEnabledFeatures()` called without mock | Add `jest.mock('@common/windowService', ...)` with `jest.requireActual` |
| `Cannot spy the X property because it is not a function` | `jest.mock` replaced the module, wiping exports that `jest.spyOn` needs | Don't `jest.mock` the module if tests use `spyOn` on it; or include all needed exports |
| `Cannot redefine property: X` | `jest.mock` made property non-configurable, then `spyOn` tries to redefine | Remove the `jest.mock` and let existing `spyOn`-based mocking handle it |
| `exit code 137` (remote only) | OOM — not a code issue | Retry the job via API |
| Flaky test unrelated to your changes | Pre-existing instability | Retry the job; note it for the user |

## API Quick Reference

| Action | Endpoint |
|--------|----------|
| List MR pipelines | `GET /projects/:id/merge_requests/:iid/pipelines` |
| Get pipeline | `GET /projects/:id/pipelines/:pipeline_id` |
| List jobs | `GET /projects/:id/pipelines/:pipeline_id/jobs` |
| Get job trace | `GET /projects/:id/jobs/:job_id/trace` |
| Retry job | `POST /projects/:id/jobs/:job_id/retry` |
| Retry pipeline | `POST /projects/:id/pipelines/:pipeline_id/retry` |

## Notes

- Always use `--header "PRIVATE-TOKEN: <TOKEN>"` (not `--header "Authorization: Bearer"`)
- URL-encode the project path: `full-stack/mmb/mmbweb` → `full-stack%2Fmmb%2Fmmbweb`
- The host is the company GitLab instance (e.g. `gitlab.agodadev.io`), not `gitlab.com`
- For large test suites, wait at least 5 minutes between polls
- For Playwright integration tests, wait 8-10 minutes — they routinely take 30-40 min
- Cap retries at 3 for the same OOM job before escalating to the user
- When multiple jobs fail, fix them all in one commit if possible
- **Batch all fixes and verify locally before pushing — one push, not five**
