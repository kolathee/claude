---
name: pack-cowork-skills
description: Package Claude Code skills as ZIPs for uploading to Claude Cowork. Fixes frontmatter, descriptions, and paths. Use when asked to pack, export, or rebuild Cowork skills.
---

# Pack Cowork Skills

Package local Claude Code skills (`~/.claude/skills/`) into Cowork-compatible ZIPs ready for upload at [claude.ai/customize/skills](https://claude.ai/customize/skills).

## When to Use

- User says "pack skills", "export skills for cowork", "rebuild cowork zips", "repack skills"
- After editing a skill and wanting to update the Cowork version

## Cowork Constraints

| Rule | Detail |
|------|--------|
| Entry file | Must be `SKILL.md` (uppercase) |
| `name` | Max 64 chars |
| `description` | Max 200 chars, no XML tags (`<...>`), must be YAML-safe (quote if contains colons) |
| Frontmatter | Only `name`, `description`, `dependencies` — remove `allowed-tools`, `version` |
| ZIP structure | `skill-name.zip` -> `skill-name/` -> `SKILL.md` + supporting files |
| No secrets | No API keys, tokens, credentials |

## Skill Registry

These skills are portable (not Agoda-specific) and should be packed:

```yaml
skills:
  humanizer:
    description: "Remove signs of AI-generated writing from text. Detects and fixes inflated symbolism, promotional language, em dash overuse, AI vocabulary, and other common AI writing patterns."
  book-summary:
    description: "Summarize any book into structured notes with chapter breakdowns, key ideas, notable quotes, and a bottom line. Use when asked to summarize a book or create book notes."
  study:
    description: "Create structured study notes for any topic, reviewable in under 5 minutes. Supports single-page and multi-page formats with diagrams, examples, and quizzes."
  save-article:
    description: "Save and summarize an article from a URL (blog post, newsletter, Twitter thread) into a structured note with summary, key insights, and action items."
  obsidian-cleanup:
    description: "Clean up, restructure, or reformat a markdown note into a well-organized document. Supports concise, balanced (default), and detailed style modes."
  financial-analysis:
    description: "Financial analysis for market research, financial modeling, ratio analysis, valuation (DCF, comps, precedents), scenario analysis, and investment due diligence."
  equity-research:
    description: "Equity research to analyze earnings transcripts, update financial models, write research notes, develop investment theses with bull/bear/base cases."
  investment-analysis:
    description: "Analyze investment documents (10-K, earnings transcripts, filings) and produce a structured investment thesis with risks, catalysts, and actionable takeaways."
  investment-banking:
    description: "Investment banking for M&A transaction analysis, pitch prep, comparable company analysis, precedent transactions, CIM review, and deal documentation."
  investment-strategy-extractor:
    description: "Extract actionable investment principles from books, articles, or videos. Produces chapter summaries, key ideas, a master checklist, and a bottom line."
  private-equity:
    description: "Private equity for deal sourcing, LBO modeling, due diligence, data room review, IC memo preparation, and portfolio company monitoring."
  stock-analysis:
    description: "Full 8-step stock analysis from a company name or ticker covering business phase, management, moat, financials, growth drivers, risks, and sentiment."
  flashcard-explain:
    description: "Create an English vocabulary flashcard from a word or phrase seen in context (sentence, meme, headline). Saves to Obsidian with meaning, patterns, alternatives, and tone."
  flashcard-translate:
    description: "Create a Thai-to-English translation flashcard from a Thai sentence. Saves to Obsidian with the best English version, tone alternatives, and phrasing notes."
  web-fetch:
    description: "Fetch web content when WebFetch is blocked (403, paywall, JS-rendered pages). Uses Gemini CLI via tmux as primary method, curl as fallback."
  pack-cowork-skills:
    description: "Package Claude Code skills as ZIPs for uploading to Claude Cowork. Fixes frontmatter, descriptions, and paths. Use when asked to pack, export, or rebuild Cowork skills."
```

To add a new skill: add its key + description to the registry above.

## Path Handling

Keep the iCloud Obsidian vault path as-is (synced across machines via iCloud):

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb
```

Only replace the absolute username prefix with `~`:

| Original | Replacement |
|----------|-------------|
| `/Users/kpayuhawatta` | `~` |

## Files to Exclude

Skip these when copying into the ZIP:

- `.git/` directories
- `__pycache__/` directories
- `cache/` directories
- `LICENSE`, `README.md`, `WARP.md`, `.DS_Store`

## Output

Write all ZIPs to `~/Desktop/cowork-skills/`. Create the directory if needed.

## Workflow

1. Read the skill registry above
2. For each skill:
   a. Read `~/.claude/skills/<name>/SKILL.md`
   b. Replace frontmatter: keep only `name`, set `description` from registry (quoted), remove `allowed-tools`/`version`
   c. Generalize paths in all `.md` files
   d. Copy supporting files (references/, examples/, scripts/) excluding skip list
   e. Package as `<name>.zip` with correct structure: `<name>/SKILL.md` + supporting files
3. Print summary with file count and size per ZIP
4. Report any errors

## Verification

After building, verify each ZIP:
- `SKILL.md` exists at `<name>/SKILL.md` inside the ZIP
- Description is under 200 chars
- No XML tags in description
- YAML parses without error

## Quick Run

User says "pack" or "repack" -> run the full workflow with no questions asked.
