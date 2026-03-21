---
name: equity-research
description: Equity research skill for analyzing public companies, parsing earnings transcripts, updating financial models, writing initiation reports, and producing investment theses. Use when the user asks to "analyze this earnings call", "update my model", "write a research note", "initiate coverage", "what's the investment thesis", "parse this transcript", "check analyst consensus", or "write a bull/bear case".
---

# Equity Research Skill

Produce institutional-quality equity research: earnings analysis, financial model updates, investment thesis development, and research notes.

## Capabilities

### 1. Earnings Transcript Analysis (`/equity:parse-transcript`)
- Extract: revenue, EPS, guidance, key metrics vs. consensus estimates
- Identify management tone and confidence signals
- Pull key quotes on strategy, macro environment, and forward outlook
- Flag guidance changes vs. prior quarter
- Output structured earnings summary

### 2. Financial Model Update
- Update income statement, balance sheet, cash flow with new actuals
- Revise forward estimates based on guidance and trends
- Recalculate valuation (P/E, EV/EBITDA, P/FCF) at updated estimates
- Flag estimate revisions vs. prior model and street consensus

### 3. Investment Thesis
- Bull case: key growth drivers, upside catalysts, underappreciated assets
- Bear case: key risks, competitive threats, macro headwinds
- Base case: probability-weighted view with price target rationale
- Variant perception: where your view differs from consensus and why

### 4. Research Notes
- **Initiation of Coverage:** Company overview, industry context, investment thesis, valuation, risks, price target
- **Earnings Update:** Quick 1–2 page note with actuals vs. estimates, guidance changes, model revision, maintained/changed rating
- **Sector Note:** Thematic analysis across multiple names in a sector
- **Flash Note:** Same-day reaction to a significant event (earnings beat/miss, guidance cut, M&A announcement)

### 5. Sector & Competitive Analysis
- Map competitive positioning on key dimensions
- Identify secular growth vs. cyclical exposure
- Benchmark margins, growth, and returns vs. peer group

## Step-by-Step Workflow

1. **Identify company and trigger** — Earnings release? Model update? New coverage initiation?
2. **Gather data** — Earnings transcript, recent filings (10-K/10-Q), consensus estimates
3. **Run analysis** — Apply relevant capability above
4. **Update model** — Revise estimates and price target
5. **Draft note** — Follow output format below

## Output Format

### Earnings Summary
```
Company: [Name] ([Ticker])          Report date: [Date]
Quarter: Q[X] [Year]

                        Actual    Estimate    Beat/Miss
Revenue                 $X        $X          +X%
Gross Margin            X%        X%          +Xbps
EBITDA                  $X        $X          +X%
EPS                     $X        $X          +$X

Guidance:
- Q[X+1] Revenue: $X–$X (Street: $X)
- FY Revenue: $X–$X (prior: $X–$X)

Key takeaways:
1. ...
2. ...
3. ...

Rating: [Buy / Hold / Sell]   PT: $X (prior: $X)
```

### Investment Thesis (One Page)
```
## [Company] — [Rating], PT $X

**Thesis in one sentence:** [...]

**Bull case (40%):** [...]
**Base case (50%):** [...]
**Bear case (10%):** [...]

**Variant perception:** [Where view differs from consensus]

**Key catalysts:** [...]
**Key risks:** [...]
```

## Notes
- Always cite data sources and note staleness
- Flag where estimates are your own vs. management guidance vs. consensus
- For Excel models: invoke xlsx skill
- For full research PDFs: invoke pdf skill
