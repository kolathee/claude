---
name: private-equity
description: Private equity skill for deal sourcing, LBO modeling, due diligence, large document review, investment committee memos, and portfolio company monitoring. Use when the user asks to "screen deals", "build an LBO", "run diligence", "review the data room", "write an IC memo", "model a buyout", "analyze a target", "review the CIM", or "track portfolio performance".
---

# Private Equity Skill

Support the full PE deal lifecycle: sourcing, underwriting, due diligence, IC presentation, and portfolio monitoring.

## Capabilities

### 1. Deal Sourcing & Screening
- Screen targets against fund mandate (sector, size, geography, EBITDA range)
- Quick-pass checklist: revenue scale, margin profile, growth rate, leverage capacity, management quality
- Identify deal source (proprietary vs. intermediary-run)
- Flag conflicts and competitive dynamics

### 2. LBO Modeling (`/pe:lbo`)
- Entry assumptions: purchase price, EV/EBITDA multiple, EBITDA
- Capital structure: senior debt, subordinated debt, equity contribution
- Operating model: revenue growth, margin expansion, FCF generation
- Exit: multiple assumptions, hold period, returns at exit
- Returns: IRR, MOIC, DPI at various entry/exit scenarios
- Sensitivity table: IRR vs. entry multiple × exit multiple

### 3. Due Diligence Support
- **Financial DD:** Quality of earnings, EBITDA bridge, working capital normalization, capex analysis
- **Commercial DD:** Market size, competitive positioning, customer concentration, churn analysis
- **Legal DD:** Key contract review, IP ownership, litigation flag, regulatory issues
- **Management DD:** Track record, retention risk, compensation structure
- Data room document summarization by workstream

### 4. Investment Committee Memo (`/pe:ic-memo`)
- Executive summary: deal overview, investment thesis, price, structure
- Company overview: business model, financials, market position
- Investment highlights (bull case)
- Key risks and mitigants
- Financial projections and returns analysis
- Deal structure and terms
- Management and governance
- Exit strategy

### 5. Portfolio Monitoring
- Track KPIs vs. budget: revenue, EBITDA, FCF, leverage
- Flag covenants at risk
- Summarize management updates
- Board pack preparation outline
- Value creation plan progress tracking

### 6. Large Document Review
- Process CIMs, management presentations, data room materials efficiently
- Extract: business description, financials, customer data, market data, risk factors
- Flag: gaps, inconsistencies, items needing follow-up
- Produce diligence tracker

## Step-by-Step Workflow

1. **Identify deal stage** — Sourcing? IOI? LOI? Full diligence? IC?
2. **Clarify deliverable** — LBO model, DD summary, IC memo, document review?
3. **Gather inputs** — CIM, financials, data room documents, market data
4. **Execute** — Apply relevant capability above
5. **Deliver** — Structured output or formatted document

## Output Formats

### LBO Returns Summary
```
Entry:
  EV:              $X      Entry multiple: Xx EV/EBITDA
  Debt:            $X      Leverage:       Xx net debt/EBITDA
  Equity:          $X      Equity %:       X%

Base Case Returns (5-year hold, Xx exit):
  Revenue CAGR:    X%
  EBITDA exit:     $X
  Exit EV:         $X
  Equity proceeds: $X
  Gross IRR:       X%      MOIC: Xx

Sensitivity (Gross IRR):
              Exit 7x   Exit 8x   Exit 9x
  Entry 7x    X%        X%        X%
  Entry 8x    X%        X%        X%
  Entry 9x    X%        X%        X%
```

### IC Memo Structure
```
1. Executive Summary (1 page)
2. Investment Highlights (3–5 bullets)
3. Business Overview
4. Market & Competitive Position
5. Financial Analysis
6. LBO Returns Analysis
7. Key Risks & Mitigants
8. Deal Structure & Terms
9. Exit Pathways
10. Recommendation
```

## Notes
- Treat all deal materials as strictly confidential
- Flag when assumptions are estimated vs. management-provided vs. third-party verified
- For financial models: invoke xlsx skill
- For IC memos and board packs: invoke docx or pptx skill as appropriate
- For large PDF data rooms: invoke pdf skill for extraction
