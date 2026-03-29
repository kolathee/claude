---
name: explore-and-implement
description: Guided codebase exploration and implementation for cross-service requirements. Use when the user says "explore", "trace the flow", "where do I need to change", "figure out how this works", "I have new requirements", or presents a task where the affected code/services are unclear. Emphasizes understanding before implementation — the user must understand how the system works before any code changes are made.
---

# Explore and Implement

A structured workflow for taking ambiguous requirements and turning them into
well-understood, targeted code changes. Prioritizes the user's understanding
of the system over speed of implementation.

## Core Principle

**Never implement without understanding.** The user should be able to explain
*why* a change is made in a specific file, *how* data flows to that point, and
*what* downstream effects the change has — before any code is written.

## Workflow

### Phase 1: Gather Requirements

1. Read the requirements source (Obsidian work page, Jira ticket, Slack thread, or user description).
2. Summarize the goal in plain language and confirm with the user:
   - **What** behavior needs to change?
   - **Who** is affected (end-user, agent, system)?
   - **Where** does the user *think* the change goes (if they have a guess)?
3. Identify unknowns — what do we need to figure out before we can act?

### Phase 2: Map the System

Trace the data/control flow that relates to the requirement. Work outward
from whatever is known:

1. **Start from what we know** — a flag name, a UI element, an API field, a class name.
2. **Search the current workspace repos** using Grep, Glob, and code exploration.
3. **Search across repos** using Sourcegraph when the flow crosses repo boundaries.
4. **Read internal docs** using Glean MCP or Confluence for architecture context.
5. **Ask the user to add repos** to the workspace when the trail leads outside the current repos.

At each step, explain what you found and how it connects to what we already know.
Build the picture incrementally with the user.

#### Tracing Techniques

- **Flag/field tracing**: Search for a field name across repos to see where it's set, mapped, and consumed.
- **API contract tracing**: Find the DTO/model that carries a field, then find who produces and consumes that DTO.
- **UI-to-backend tracing**: Start from a UI element, find what data it reads, trace that data back through API calls to the source.
- **Backend-to-UI tracing**: Start from a backend computation, trace the field through DTOs, API responses, and UI rendering.

### Phase 3: Present the Flow

Once the full path is traced, present a **numbered data flow summary** showing:

- Each service/layer involved
- The specific file, class, and function at each step
- How data transforms between steps
- Short code snapshots (5-15 lines) of the key logic at each step

Example format:

```
## Data Flow: [Feature Name]

1. **[Service A] — [Class.method()]** (`path/to/file.scala`)
   - [What happens here]
   
2. **[Service B] — [Class.method()]** (`path/to/file.scala`)
   - [What happens here, how it connects to step 1]

...
```

Ask the user: *"Does this flow make sense? Any questions before we proceed?"*

### Phase 4: Identify Changes

Based on the traced flow, propose the minimal set of changes:

1. **Where** — exact file(s) and function(s) to modify.
2. **What** — the logic change in plain language.
3. **Why here** — explain why this is the right layer/service for the change.
4. **Downstream effect** — what happens automatically because of this change (e.g., flag propagates through DTOs without extra work).

Confirm the plan with the user before writing any code.

### Phase 5: Implement

Only after the user confirms understanding:

1. Make the code change.
2. Write/update tests.
3. Show the user the change and explain it.
4. Run compilation, tests, and formatting per project rules.

### Phase 6: Summarize

After implementation, provide a concise summary:

- What was changed and why.
- The full data flow path (for future reference).
- Any follow-up items or related areas to watch.

Offer to save learnings to the user's knowledge base (Obsidian work page, etc.).

## Interaction Guidelines

- **Explain as you go** — don't silently search 10 files and dump a conclusion. Share findings incrementally.
- **Use visuals** — numbered flows, short code snapshots, and clear file paths help the user build a mental model.
- **Pause at decision points** — when you find something significant (e.g., "this flag doesn't reach the UI directly"), stop and discuss it with the user.
- **Suggest repos to add** — if the trace leads to a repo not in the workspace, tell the user which repo and why.
- **Use internal tools** — Glean MCP for docs, Sourcegraph for cross-repo search, Confluence for architecture diagrams.
- **Don't over-implement** — if the user asks "how does X work?", explain it. Don't jump to changing code.
- **Confirm before coding** — always get explicit confirmation before making changes.

## Anti-Patterns

- Implementing a fix before the user understands the system.
- Searching silently for 5 minutes then presenting a wall of findings.
- Assuming the user knows which service/layer is responsible.
- Making changes in multiple repos when one targeted change is sufficient.
- Skipping the "why here" explanation.
