---
name: financial-analysis
description: Financial analysis skill for market research, financial modeling, ratio analysis, and investment due diligence. Use when the user asks to "analyze financials", "build a financial model", "do market research", "compare companies", "analyze this stock", "calculate valuation", "run scenario analysis", or "build a DCF".
---

# Financial Analysis Skill

Perform rigorous financial analysis including market research, financial modeling, valuation, and scenario analysis.

## Capabilities

### 1. Financial Statement Analysis
- Parse and interpret income statements, balance sheets, and cash flow statements
- Calculate key ratios: P/E, EV/EBITDA, P/B, ROE, ROA, ROIC, debt/equity, current ratio, quick ratio
- Identify trends across reporting periods
- Flag anomalies or red flags (e.g., diverging earnings vs. cash flow, rising DSO)

### 2. Valuation Models
- **DCF (Discounted Cash Flow):** Project FCF, set discount rate (WACC), calculate terminal value, derive intrinsic value
- **Comparable Company Analysis (Comps):** Pull trading multiples from peer group, apply to subject company
- **Precedent Transaction Analysis:** Apply deal multiples from comparable M&A transactions
- **Sum-of-the-Parts:** Value business segments independently

### 3. Market Research
- Identify total addressable market (TAM), serviceable addressable market (SAM)
- Competitive landscape and positioning
- Industry growth drivers, headwinds, and regulatory context
- Market share analysis

### 4. Scenario & Sensitivity Analysis
- Build base / bull / bear scenarios
- Sensitivity tables on key assumptions (revenue growth, margin, discount rate)
- Monte Carlo framing for probabilistic outcomes

### 5. Reporting
- Summarize findings in structured investment memo format
- Create Excel models (invoke xlsx skill for deliverable)
- Executive summary with key takeaways and recommendation

## Step-by-Step Workflow

1. **Clarify the ask** — What company/sector? What decision does this analysis support? (buy/sell, M&A, internal planning)
2. **Gather inputs** — Request financial statements, ticker, or sector. Use web search for public data.
3. **Run analysis** — Apply the relevant model(s) above.
4. **Sanity check** — Cross-validate using at least two methods (e.g., DCF + comps).
5. **Deliver** — Structured memo + Excel model if needed.

## Output Format

```
## Financial Analysis: [Company / Topic]

### Key Metrics
| Metric | Value | vs. Peers |
|--------|-------|-----------|
| ...    | ...   | ...       |

### Valuation
- Method: [DCF / Comps / Precedent]
- Implied value: [range]
- Current price: [price] → [Undervalued / Fairly valued / Overvalued]

### Key Risks
1. ...
2. ...

### Recommendation
[Buy / Hold / Sell / Further diligence needed] — [1–2 sentence rationale]
```

## Notes
- Always state assumptions explicitly
- Flag data quality issues (stale data, estimated figures)
- For Excel deliverables, invoke the xlsx skill
