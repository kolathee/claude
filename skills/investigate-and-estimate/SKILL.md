---
name: investigate-and-estimate
description: >-
  Investigate a requirement's implementation complexity and produce a refined
  effort estimate with exact file paths grouped by repository. Use when the
  user says "investigate", "estimate effort", "how many story points",
  "what files do I need to change", "trace the impact", "scope this out",
  or presents a requirement that needs sizing before implementation.
---

# Investigate and Estimate

A structured workflow for turning a requirement into a concrete effort
estimate backed by exact file paths, data flow traces, and story points —
without writing any implementation code.

## Core Principle

**Estimate from evidence, not assumptions.** Every file listed in the
estimate must be confirmed by reading its source. Every "data not available"
claim must be proven by tracing the full pipeline.

## Workflow

### Phase 1: Locate the Requirement

1. Find the source document — Obsidian work page, Jira ticket, Slack thread, or user description.
2. Summarize the requirement in plain language:
   - **What** changes for the end-user?
   - **Which surfaces** are affected (web page, email, mobile app, API)?
   - **Are there scenarios/variants?** (e.g., "all bookings" vs "only amended bookings")
3. Identify what we already know vs what needs investigation.

### Phase 2: Trace the Data Flow per Surface

For each affected surface, trace the full rendering/processing chain:

**Frontend (UI → client → server → external):**
1. Identify the UI component that renders the target element.
2. Trace what data it consumes and where that data comes from (context, props, API call).
3. Follow the API call to the backend handler/controller.
4. Follow the backend to any external service calls.
5. At each layer, record the **exact file path** and **key function/method**.

**Backend / Email / Other:**
1. Identify the entry point (mapper, handler, template).
2. Trace input data sources (database models, API responses, DTOs).
3. Check what fields are available vs what needs to be added.
4. At each layer, record the **exact file path** and **key function/method**.

#### Tracing Checklist

For each field/flag the requirement depends on, answer:
- [ ] Where is this field **defined** (model/type)?
- [ ] Where is this field **populated** (mapper/converter/query)?
- [ ] Where is this field **consumed** (component/template)?
- [ ] Is this field **available at the layer where the change is needed?**
- [ ] If not, what is the **gap** — which layers need plumbing?

### Phase 3: Create Data Flow Diagrams

For each affected surface, create a Mermaid flowchart showing:
- Subgraphs for each layer (Client, Service, Backend, External, etc.)
- Node labels with file/class names
- Data transformations between layers
- Use `<br>` for line breaks in node labels (not `\n`)

If scenarios exist (A vs B), create a separate diagram showing the
decision points and what changes per scenario.

### Phase 4: Identify Exact Files to Change

For each scenario, list every file that needs modification:

1. **Read each file** to confirm the change location (function, line range).
2. **Classify the change type**: new field, conditional logic, template change, type definition.
3. **Group files by repository**, then by layer (server-side vs client-side).
4. **Note existing patterns** — find a similar field/flag that already follows the same pipeline, to use as a reference for implementation.

Present as a table:

```
| # | File | Change | Effort |
|---|------|--------|--------|
| 1 | `path/to/file.ext` | Description of change | Low/Medium |
```

### Phase 5: Estimate Story Points

Use this calibration:

| SP | Guideline |
|----|-----------|
| **1** | 1-2 files, straightforward conditional or value change, no new plumbing |
| **2** | 2-4 files, new field threading through existing pipeline, established pattern |
| **3** | 4-6 files, new field across server + client boundary, tests needed |
| **5** | 6-10 files, new API field or cross-service coordination, multiple test files |
| **8** | 10+ files, new feature surface, significant refactoring or new patterns |

Present estimates in a table grouped by scenario and repo:

```
| Surface | Repo | Effort | SP | Files Changed |
|---------|------|--------|:--:|---------------|
```

Include a summary comparing scenarios (e.g., "A is a subset of B; combined = X SP").

### Phase 6: Update Documentation

Update the work page (Obsidian or other) with:

1. **Latest Update** entry with date and key findings.
2. **Data flow diagrams** (Mermaid).
3. **Files to change** tables grouped by repo.
4. **Effort estimate** tables with story points.
5. **Answered open questions** — strike through resolved items with findings.
6. **Remaining open questions** — anything still blocking estimation.

### Phase 7: Summarize for the User

Provide a concise verbal summary covering:
- Key findings (especially any "data not available" surprises).
- Story point estimates per scenario.
- Remaining blockers or open questions.
- Recommended next step (e.g., "confirm scenario choice with PM").

## Key Investigation Patterns

### "Is this field available?" Pattern
When a requirement needs a field at a specific layer:
1. Search for the field name across all layers (Grep across repo).
2. If found in server model but not in client DTO → **plumbing needed**.
3. If found in GraphQL query but not mapped → **mapping needed**.
4. If not found anywhere → **new field from scratch**.

### "How does similar feature X work?" Pattern
Find an existing field that follows the same pipeline:
1. Search for a similar boolean/field that flows server → client.
2. Read how it's computed, mapped, and consumed.
3. Use it as the blueprint for the new field (reference in the estimate).

### Cross-Repo Impact Pattern
When a requirement touches multiple repos:
1. Trace until the repo boundary (API contract, message schema).
2. Check if the needed data crosses the boundary or stays within one repo.
3. Group all files by repo in the final estimate.

## Interaction Guidelines

- **Show evidence** — when claiming "field X is not available at layer Y", cite the exact file and what IS available there.
- **Use tables** — file lists, effort matrices, and data availability tables are faster to scan than prose.
- **Pause at surprises** — if the trace reveals unexpected complexity (e.g., data not reaching the client), highlight it explicitly.
- **Don't implement** — this skill is for investigation only. Code snippets show *what* would change, not production-ready code.
- **Group by repo** — always categorize files by repository, especially in multi-repo projects.
