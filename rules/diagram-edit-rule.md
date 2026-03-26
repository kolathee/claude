# Diagram Edit Rule — Fix All Instances in One Pass

## Rule

When asked to fix a syntax issue in a diagram (e.g. `\n` to `<br>` in Mermaid node labels), **always grep the entire file for all occurrences of the pattern first**, then fix everything in a single edit.

## Why

Fixing piecemeal caused two rounds of edits when all six `\n` instances in a Mermaid diagram should have been caught and fixed at once.

## How to Apply

1. Run a content grep for the pattern across the whole file before touching anything
2. Review all matches
3. Fix all occurrences in one edit - never fix one and wait for the user to point out the rest
