---
name: investment-banking
description: Investment banking skill for M&A transaction analysis, pitch deck preparation, comparable company analysis, precedent transactions, and deal documentation. Use when the user asks to "prep a pitch", "run comps", "review this CIM", "build a transaction model", "draft an IOI", "analyze this deal", "build a merger model", or "prepare board materials".
---

# Investment Banking Skill

Support M&A and capital markets workflows: deal analysis, pitch preparation, transaction documentation review, and financial modeling.

## Capabilities

### 1. Transaction Analysis
- **Buy-side:** Screen targets, run initial valuation, flag synergies and risks
- **Sell-side:** Prepare company overview, position for buyer universe, support data room
- **Merger model:** Accretion/dilution analysis, combined pro forma financials, synergy bridge

### 2. Pitch Preparation (`/ib:pitch-prep`)
- Executive summary: company overview, situation, recommendation
- Strategic rationale for deal
- Comparable transactions and valuation football field
- Potential buyer/partner universe
- Process timeline and key milestones

### 3. Comparable Company Analysis (`/ib:comps`)
- Identify peer group (by size, sector, geography)
- Spread trading multiples: EV/Revenue, EV/EBITDA, P/E, P/B
- Benchmark subject company against median / 25th / 75th percentile
- Output formatted comps table

### 4. Precedent Transactions (`/ib:precedents`)
- Pull relevant M&A deal data (sector, size, timeframe)
- Spread transaction multiples
- Identify premium paid, deal structure (cash/stock/mixed)
- Note market conditions at time of deal

### 5. Document Review
- **CIM (Confidential Information Memorandum):** Extract key financials, business highlights, investment thesis, risks
- **NDA / LOI / IOI:** Flag key terms, unusual clauses, missing provisions
- **Data room documents:** Summarize by category (financials, legal, operations, HR)

### 6. Deal Documentation Drafting
- IOI (Indication of Interest) framework
- LOI (Letter of Intent) key terms
- Management presentation outline
- Board presentation structure

## Step-by-Step Workflow

1. **Identify deal type** — M&A buy-side, sell-side, capital raise, restructuring?
2. **Clarify deliverable** — Pitch deck, model, document review, comps table?
3. **Gather inputs** — Company name, sector, financials, relevant documents
4. **Execute analysis** — Apply relevant capability above
5. **Package output** — Structured memo, comps table, or pptx (invoke pptx skill for decks)

## Output Format

### Valuation Football Field
```
Method              Low     Mid     High
DCF                 $X      $X      $X
Trading Comps       $X      $X      $X
Precedent Txns      $X      $X      $X
52-week range       $X      $X      $X
```

### Deal Summary
```
Target:          [Name]
Sector:          [Sector]
Deal type:       [M&A / Recap / IPO]
Implied EV:      $X
EV/EBITDA:       Xx
Premium to spot: X%
Strategic rationale: [2–3 bullets]
Key risks:       [2–3 bullets]
```

## Notes
- For pitch decks: invoke the pptx skill
- For financial models: invoke the xlsx skill
- Treat all deal information as confidential
- Flag when public data is unavailable and estimation is used
