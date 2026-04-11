---
name: stock-analysis
description: Use when the user wants to do a full company or stock analysis from scratch — given just a company name and/or ticker. Runs an 8-step structured research process (business phase, management, business model, moat, financials, growth drivers, risks, market sentiment) and saves a complete two-part report to Obsidian under Investment/Stock Analysis/[Company Name]. Trigger when user says "analyze [company]", "do a stock analysis of [ticker]", "research [company] for me", "full analysis of [company]", or gives a company name/ticker and asks to analyze it as an investment. Also trigger when user says things like "run the steps on [company]" or "do the 8 steps for [ticker]".
version: 1.0.0
---

# Stock Analysis Skill

## Purpose

Produce a comprehensive 8-step investment research report for any publicly traded company, given only a name and/or ticker. Save a two-section Obsidian note: a quick-read summary (Section 1) and full deep-dive (Section 2).

## Obsidian Save Path

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Investment/Stock Analysis/[Company Name]/[Company Name] - Stock Analysis.md
```

Example:
```
.../Stock Analysis/Apple/Apple - Stock Analysis.md
```

Create the company folder if it doesn't exist. Use the `Write` tool to save.

---

## Workflow

### Step 0: Confirm the company

If only a ticker is given, confirm the full company name before proceeding. If both are given, proceed immediately.

### Step 1-8: Run all analysis steps

Read each reference file below and follow its exact output format. Run all steps in sequence. The output from Step 1 (business phase determination) informs Step 5 (financial health metrics) — carry the phase result forward.

| Step | Topic | Reference File |
|------|-------|----------------|
| 1 | Business Growth Cycle Phase | `references/step1-business-phase.md` |
| 2 | Management & Governance | *(no fixed format — see below)* |
| 3 | Business Understanding | `references/step3-business-understanding.md` |
| 4 | Competitive Position (Moat) | `references/step4-moat.md` |
| 5 | Financial Health (Key Metrics) | `references/step5-financial-health.md` |
| 6 | Growth Drivers | `references/step6-growth-drivers.md` |
| 7 | Risks | `references/step7-risks.md` |
| 8 | Market / People Sentiment | `references/step8-sentiment.md` |

**Step 2 - Management & Governance** has no fixed template. Research freely:
- CEO/leadership background, tenure, and track record
- Board composition and independence
- Compensation structure and alignment with shareholders
- Insider ownership and recent transactions
- Any governance controversies or red flags
- Capital allocation philosophy

### Visualizations (optional but encouraged)

Where data lends itself to it, use Obsidian-Charts plugin syntax or Mermaid to add a bar chart, table, or pie chart. Large numbers are easier to compare visually than in prose. Good candidates: revenue breakdown by segment, phase criteria match, financial scorecard, risk matrix.

### Step 9: Assemble the final note

Build the Obsidian note in two sections:

**Section 1 - Executive Summary** (quick read, ~1 page)
- Company name, ticker, date analyzed
- Business phase (from Step 1) with confidence level
- 3-sentence business description (from Step 3)
- Moat verdict: size + direction (from Step 4)
- Phase health scorecard (from Step 5): overall rating + green/yellow/red count
- Top 2 growth drivers (from Step 6)
- Top 2 risks (from Step 7)
- Market sentiment outlook: bullish/neutral/bearish (from Step 8)
- One-line investment thesis

**Section 2 - Deep Dive**
Full output from all 8 steps in order, each under its own `##` heading.

### Step 10: Save and confirm

Save to the Obsidian path above. Tell the user:
- File path saved
- The one-line investment thesis from Section 1

---

## Output Format (Note Structure)

```markdown
# [Company Name] ([TICKER]) - Stock Analysis
**Date:** [Today's date]
**Phase:** Phase [#] - [Phase Name] ([Confidence])

---

## Section 1 - Executive Summary

### Quick Snapshot
| Field | Value |
|-------|-------|
| Company | [Name] ([TICKER]) |
| Business Phase | Phase [#] - [Name] ([confidence emoji]) |
| Moat | [Size] [emoji] / [Direction] [emoji] |
| Phase Health | [🟢 Strong / 🟡 Mixed / 🔴 Weak] ([X]G [X]Y [X]R) |
| Market Sentiment | [🟢 Bullish / 🟡 Neutral / 🔴 Bearish] |
| Top Growth Drivers | [Driver 1], [Driver 2] |
| Top Risks | [Risk 1], [Risk 2] |

### Business in One Sentence
[Single sentence capturing what the company does and why it matters]

### Investment Thesis
[2-3 sentences: what makes this company interesting (or not) as an investment right now]

---

## Section 2 - Deep Dive

## Step 1 - Business Growth Cycle Phase
[Full Step 1 output]

## Step 2 - Management & Governance
[Step 2 findings]

## Step 3 - Business Understanding
[Full Step 3 output]

## Step 4 - Competitive Position (Moat)
[Full Step 4 output]

## Step 5 - Financial Health (Key Metrics)
[Full Step 5 output]

## Step 6 - Growth Drivers
[Full Step 6 output]

## Step 7 - Risks
[Full Step 7 output]

## Step 8 - Market / People Sentiment
[Full Step 8 output]
```

---

## Data Sources

Use web search and public sources. Prioritize:
- SEC EDGAR (10-K, 10-Q, proxy statements)
- Company investor relations pages
- MacroTrends, GuruFocus for historical financial data
- Morningstar for moat ratings
- Yahoo Finance / MarketBeat for price/sentiment data
- TipRanks for analyst consensus
- Recent news (Reuters, Bloomberg, CNBC) for sentiment

Never fabricate numbers, links, or quotes. If data is unavailable, state it explicitly.

---

## Notes on Formatting

- Tables must always have a blank line before them (Obsidian rendering requirement)
- Never use `==highlight==` markup
- Use emojis exactly as specified in each step's reference file — they serve as visual scanners
- Indent sub-bullets consistently (Obsidian uses tab indentation)
