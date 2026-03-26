---
name: investment-analysis
description: Use when the user wants to analyze an investment document from an investor's perspective — annual reports (10-K/10-Q), earnings transcripts, financial news, analyst reports, company filings, or any content where the output should be a structured investment thesis with risks, catalysts, and an actionable takeaway. Also trigger when user says "analyze this for investment", "investment analysis of...", or "what do I think about [company] as an investment".
version: 1.0.0
---

# Investment Analysis Skill

## Purpose

Produce a structured, investment-grade analysis of any source document — annual reports, earnings transcripts, financial news, analyst notes — and save it to the Obsidian Watching List folder.

## Strict Rules (Non-Negotiable)

- Do NOT make up, assume, or infer facts not supported by the provided content.
- If information is missing, explicitly state: "Not mentioned in the source."
- If a section is not applicable, omit it entirely — do not fabricate content.
- Clearly distinguish between:
  - **Fact** — directly from the source
  - **Interpretation** — your reasoning based on facts (always label it)
- Be concise, precise, and avoid fluff.

---

## Workflow

### Step 1: Gather the Source

- File path provided → use `Read`
- URL provided → use `WebFetch`
- Pasted text → use directly
- No source → ask the user to provide one before proceeding

### Step 2: Identify the Company / Topic

Extract or confirm:
- Company name and ticker (if applicable)
- Document type (10-K, earnings transcript, news article, etc.)
- Period covered (FY year, quarter, date)

### Step 3: Write the Analysis

Follow the output format below. Omit any section that is truly not applicable — never pad with fabricated content.

### Step 4: Save to Obsidian

**Default save path:**
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Investment/Watching List/[Company]/[Title].md
```

Example:
```
.../Watching List/Adobe/Adobe FY2024 10-K - Investment Analysis.md
```

- If the company folder doesn't exist, create it.
- If no company is identifiable (e.g., a macro article), save to:
  ```
  .../Watching List/General/[Title].md
  ```

Use the `Write` tool to save.

### Step 5: Confirm

Tell the user:
- File path saved
- The one-liner summary (section 12)

---

## Output Format

```markdown
# [Company / Topic] — Investment Analysis
**Source:** [Document type, period]
**Date analyzed:** [Today's date]

---

## 1. Core Thesis
- What is the main idea?
- Why it matters financially
- Implied investment angle

---

## 2. Key Facts & Data
- Important numbers, metrics, or statements directly from the source
- Timeline (if relevant)
- Management guidance (if any)

---

## 3. Market / Business Impact
- Who benefits / who is negatively affected
- Short-term vs long-term implications

---

## 4. What the Market Might Be Pricing In
- Is this new information or already expected?
- Possible investor reaction *(Interpretation)*

---

## 5. Risks / What Could Go Wrong
- [At least 3 risks if supported by the content]
- If not enough information: "Insufficient information to assess risks"

---

## 6. What's Missing / Blind Spots
- Key data or context not provided by the source
- What would be needed to validate the thesis

---

## 7. Key Questions to Investigate
- Thoughtful follow-up questions an investor should ask

---

## 8. Comparable / Competitor Context
- Direct competitors mentioned or implied
- How this compares vs peers (growth, margins, positioning, strategy)
- Industry benchmarks or historical parallels

---

## 9. Valuation Angle
- Any mention or implication of valuation

---

## 10. Catalysts
- Upcoming events or triggers that could move the stock/thesis

---

## 11. Actionable Takeaway
**[Bullish / Bearish / Neutral / Watchlist]**
- Brief reasoning
- What would change this view

---

## 12. One-Liner Summary
[A single sentence capturing the full picture]
```

> Sections 8, 9, and 10 should be omitted if there is no relevant content — do not fabricate.

---

## Style Guidelines

- Bullet points, not paragraphs
- Concise but insightful — avoid repeating the same point across sections
- Prioritize clarity over complexity
- Facts and interpretations must always be clearly labeled
- Tables must always have a blank line before them (Obsidian rendering requirement)
