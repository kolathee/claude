---
name: invest-fund-switch
description: Record a fund switch in the Invest sheet correctly — updating D, E, F, G columns for both sending and receiving funds without double-counting.
---

# Fund Switch Recording — Invest Sheet

## When to use
When the user says a fund was switched, transferred, or moved to another fund in the Invest sheet. Also use when fixing existing switch entries.

## Sheet Column Conventions
- **C** = pre-year market value (opening balance)
- **D** = cost/flow this year (positive = inflow, negative = outflow)
- **E** = C + D (always, no exceptions)
- **F** = all-time cost basis accumulated
- **G** = current market value from app (today's value only)
- **H** = G - E (diff from pre-year)
- **I** = H / E (% diff from pre-year)
- **J** = G - F (all-time diff)
- **K** = J / F (all-time %)

## Critical Rules — Read Before Touching Any Cell

### G column — NEVER use for switch amounts
G always = current market value from the app today. Never store switch proceeds or historical values here.

### D column — market value that physically moved
- **Receiving fund:** hardcode `units_switched × NAV_at_switch_date` as a positive static value
- **Sending fund (partial):** hardcode `-(units_switched × NAV_at_switch_date)` as a negative static value
- **Sending fund (100% out):** `=-C` (formula referencing pre-year value)
- Document in cell note: "{units} units × NAV {nav} at switch date {date} = {amount} THB"
- **No helper cells** — embed the computed value directly, note documents the working

### E column — always C + D, no exceptions
`=C+D` for every row, including switch rows. Never compute manually.

### F column — all-time cost basis

**Receiving fund:**
`= prior_F_of_receiving + C_of_sending_fund`
- Use **C of the sending fund** (pre-year market value = what actually transferred in)
- NOT original cost basis of sending fund
- NOT units × NAV

**Sending fund (partial):**
`= prior_F_of_sending - prior_F_of_sending × D_sending_absolute / C_sending`
- Cost basis removed = proportional share by market value moved vs total pre-year value
- D_sending_absolute = absolute value of D (the market value that left)
- C_sending = pre-year market value of sending fund

**Sending fund (100% out):** F = 0 (full cost basis transferred)

**NEVER add both D and a separate cost basis term** — that double counts.

### F column — verify cell references
Before writing any F formula, read the B column label of every F cell you plan to reference. Confirm it matches the fund name you intend. Never assume row numbers — always look up.

## Workflow for Each Switch

### Step 1 — Gather inputs from user
- Which fund out, which fund in?
- Partial or 100%?
- For partial: total units switched, NAV at switch date
- Current market value of remaining units (from app) for sending fund G cell

### Step 2 — Find the correct row numbers
Read B column to identify exact row for each fund. Read C, F of each fund to confirm values before writing.

### Step 3 — Update sending fund row
- D = hardcoded `-(units × NAV)` with note, or `=-C` if 100%
- E = `=C+D`
- F = `=prior_F - prior_F * ABS(D) / C` (partial) or 0 (100%)
- G = current market value from user

### Step 4 — Update receiving fund row
- D = hardcoded `units × NAV` with note (same absolute value as sending D)
- E = `=C+D`
- F = `=prior_F_receiving + C_sending`
- G = unchanged (current app value, do not touch)

### Step 5 — Fix H, I, J, K if hardcoded
Check all four columns. Replace any hardcoded values with formulas:
- H = `=G-E`
- I = `=H/E`
- J = `=G-F`
- K = `=J/F`

### Step 6 — Verify by reading back
Read all changed cells and confirm:
- E = C + D exactly
- F_receiving + F_sending ≈ original combined F (conservation check)
- K% is reasonable — not wildly inflated vs prior year

## Done when
All 6 steps verified. No hardcoded H/I/J/K in switch rows.
