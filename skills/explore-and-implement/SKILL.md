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

Once the full path is traced, present two complementary views:

**(a) Numbered data flow summary** showing:

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

**(b) Mermaid data-flow diagram** — REQUIRED whenever the flow crosses **two or more services/repos**. Prose alone is hard to hold in your head across 4+ hops; a diagram is not optional for cross-service work.

Guidelines for the diagram:

- Use `flowchart TD` (or `LR` if the flow is short and wide).
- Group nodes by service using `subgraph` — one subgraph per repo/service. This makes service boundaries visually explicit.
- If there is both a **write path** (state-producing) and a **read path** (state-consuming) — a very common pattern for "where does this flag come from?" questions — split them into two subgraphs and connect them with a dotted edge labeled with what's persisted between them (e.g. `A7 -. customer state persisted .-> B3`).
- Keep node labels short: service name + method/class + one-line intent. Use `<br/>` for line breaks inside nodes.
- Color-code the **entry node**, **exit node**, and **the specific nodes that need to change** with `style` directives — this makes "where do I edit?" pop visually.
- Avoid parentheses inside node text (they're mermaid node-shape syntax); avoid Unicode arrows like `⇒`, `⊇`; stick to ASCII.

Example shape (adapt to the specific flow):

```mermaid
flowchart TD
    subgraph Write["WRITE PATH — what sets the flag"]
        A1[Service A entry]
        A2[Service B write]
        A3[DB / state store]
        A1 --> A2 --> A3
    end

    subgraph Read["READ PATH — what reads the flag"]
        B1[UI trigger]
        B2[Gateway mapper]
        B3[UI render]
        B1 --> B2 --> B3
    end

    A3 -. state persisted .-> B2

    style A1 fill:#e1f5ff
    style B3 fill:#d4edda
    style A3 fill:#fff3cd
    style B2 fill:#fff3cd
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

When saving to the user's knowledge base (Obsidian work page, etc.):

- Keep the daily-log / "Latest Update" entry **short** — one or two lines that point to the implementation section. It is a log entry, not a design doc.
- Put the full detail (rationale, chosen approach, trade-offs, operational gates) in the **Implementation Details** section.
- Always include the **mermaid data-flow diagram** from Phase 3 in Implementation Details — it is the single most re-readable artifact for the next person (or future you) picking this up.

## Interaction Guidelines

- **Explain as you go** — don't silently search 10 files and dump a conclusion. Share findings incrementally.
- **Use visuals** — numbered flows, short code snapshots, clear file paths, and mermaid diagrams (see Phase 3) help the user build a mental model. For cross-service flows the mermaid diagram is mandatory, not optional.
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
