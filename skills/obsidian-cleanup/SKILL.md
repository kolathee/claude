---
name: obsidian-cleanup
description: Use when the user asks to "clean up", "restructure", "organize", or "reformat" an Obsidian note or markdown file. Also use when user says "make this easier to read", "tidy up this page", or "format this note". Supports concise (c), balanced (b, default), and detailed (d) style modes.
---

# Obsidian Cleanup

Clean up an Obsidian Markdown page into a well-structured, easy-to-read document.

## Style Modes

| Mode | Alias | Behavior |
|------|-------|----------|
| concise | `c` | Keep only essential points, remove filler |
| balanced | `b` | Default. Organized with reasonable detail |
| detailed | `d` | Preserve context, details, and sub-items |

If no mode is specified, use **balanced**.

## Steps

1. **Identify the file** — use the remembered Obsidian vault path if no path is given
2. **Read the file**
3. **Analyze the content** — understand the topic, intent, and logical groupings
4. **Restructure** following the rules below
5. **Write the file back**

## Cleanup Rules

### Structure
- Add or improve `##` / `###` headings to group related content
- Create new sections if content clearly belongs together
- Move misplaced items to the right section
- Remove duplicate or redundant entries

### Formatting
- Remove unnecessary blank lines (max 1 blank line between items)
- Remove trailing whitespace and empty bullet points
- Flatten nested lists that are only 1 item deep
- Keep list items compact — no blank lines between bullets unless separating distinct groups

### Content (by mode)
- **concise**: Remove sub-items and notes that repeat the link label; keep only the core links/items
- **balanced**: Keep useful sub-items and brief notes; remove pure noise
- **detailed**: Preserve all sub-items, images, notes, and context

### Links
- Keep link text descriptive — if a raw URL is used as both label and href, shorten the label to a readable name
- Do not remove any links

### Images
- Keep embedded images (`![[...]]`) in place
- Remove blank lines around them unless needed for context

## Output

Overwrite the original file with the cleaned content. Confirm with a brief summary of what changed.
