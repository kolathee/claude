#!/usr/bin/env python3
"""
Stock Analysis Data Fetcher
============================
Fetches all financial metrics needed for the 8-step stock analysis.

Strategy:
  - yfinance `info` dict   → current snapshot: price, valuation, margins, ROE, analysts
  - yfinance `earnings`    → multi-year EPS + revenue for CAGR calculations
  - yfinance `dividends`   → dividend payment history (5+ year check)
  - yfinance `history`     → 1-year price performance
  - FinanceDataReader      → SET index 1-year return for relative comparison

Usage:
  python fetch_stock_data.py <TICKER>

Ticker format:
  Thai SET : SCB.BK   (yfinance uses .BK suffix)
  US       : AAPL
  SGX      : D05.SI

Output: JSON to stdout. Fetch errors go to stderr.
"""

import sys
import json
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings("ignore")

try:
    import yfinance as yf
except ImportError:
    print(json.dumps({"error": "yfinance not installed. Run: pip install yfinance"}))
    sys.exit(1)

try:
    import FinanceDataReader as fdr
    HAS_FDR = True
except ImportError:
    HAS_FDR = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _f(val, decimals=4, default=None):
    """Safe float, rounded."""
    try:
        return round(float(val), decimals) if val is not None else default
    except (TypeError, ValueError):
        return default


def _pct(val, default=None):
    """Convert decimal ratio to %, e.g. 0.09678 → 9.68."""
    if val is None:
        return default
    v = float(val)
    # yfinance is inconsistent: some fields already in %, detect by magnitude
    return _f(v * 100 if abs(v) < 2 else v, 2)


def _div_yield(info):
    """Extract dividend yield % reliably - prefer trailingAnnualDividendYield (always decimal)."""
    val = info.get("trailingAnnualDividendYield")
    if val:
        return _f(float(val) * 100, 2)
    val = info.get("dividendYield")
    if val:
        v = float(val)
        return _f(v if v > 2 else v * 100, 2)  # >2 means it's already %
    return None


def _cagr(start, end, years):
    try:
        if start and end and start > 0 and years > 0:
            return round(((end / start) ** (1 / years) - 1) * 100, 2)
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# Main fetch
# ---------------------------------------------------------------------------

def fetch(ticker_symbol: str) -> dict:
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info or {}

    out = {
        "ticker": ticker_symbol,
        "company_name": info.get("longName") or info.get("shortName"),
        "exchange": info.get("exchange"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "currency": info.get("currency"),
        "country": info.get("country"),
        "website": info.get("website"),
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "data_coverage": [],
        "notes": [],
    }

    # -----------------------------------------------------------------------
    # 1. Price & Valuation
    # -----------------------------------------------------------------------
    out["price"] = {
        "current": _f(info.get("currentPrice") or info.get("regularMarketPrice")),
        "52w_high": _f(info.get("fiftyTwoWeekHigh")),
        "52w_low": _f(info.get("fiftyTwoWeekLow")),
        "52w_change_pct": _pct(info.get("52WeekChange")),
        "ma_50d": _f(info.get("fiftyDayAverage")),
        "ma_200d": _f(info.get("twoHundredDayAverage")),
        "market_cap": _f(info.get("marketCap")),
        "beta": _f(info.get("beta")),
        "avg_volume_3m": _f(info.get("averageVolume")),
    }

    out["valuation"] = {
        "price_to_book": _f(info.get("priceToBook")),
        "book_value_per_share": _f(info.get("bookValue")),
        "trailing_pe": _f(info.get("trailingPE")),
        "forward_pe": _f(info.get("forwardPE")),
        "eps_ttm": _f(info.get("trailingEps")),
        "eps_forward": _f(info.get("forwardEps")),
        "eps_current_year": _f(info.get("epsCurrentYear")),
        "price_to_sales_ttm": _f(info.get("priceToSalesTrailing12Months") or info.get("priceToSalesTrailingTwelveMonths")),
        "peg_ratio": _f(info.get("trailingPegRatio")),
    }
    out["data_coverage"].append("price_and_valuation")

    # -----------------------------------------------------------------------
    # 2. Current Financials (TTM snapshot from info)
    # -----------------------------------------------------------------------
    out["financials_ttm"] = {
        "revenue": _f(info.get("totalRevenue")),
        "revenue_per_share": _f(info.get("revenuePerShare")),
        "gross_profit": _f(info.get("grossProfits")),
        "net_income": _f(info.get("netIncomeToCommon")),
        "operating_cashflow": _f(info.get("operatingCashflow")),
        "free_cashflow": _f(info.get("freeCashflow")),
        "total_cash": _f(info.get("totalCash")),
        "total_debt": _f(info.get("totalDebt")),
        "shares_outstanding": _f(info.get("sharesOutstanding")),
        "float_shares": _f(info.get("floatShares")),
    }
    out["data_coverage"].append("financials_ttm")

    # -----------------------------------------------------------------------
    # 3. Profitability & Growth (from info)
    # -----------------------------------------------------------------------
    out["profitability"] = {
        "roe_pct": _pct(info.get("returnOnEquity")),
        "roa_pct": _pct(info.get("returnOnAssets")),
        "net_margin_pct": _pct(info.get("profitMargins")),
        "operating_margin_pct": _pct(info.get("operatingMargins")),
        "gross_margin_pct": _pct(info.get("grossMargins")),
        "ebitda_margin_pct": _pct(info.get("ebitdaMargins")),
    }

    out["growth_yoy"] = {
        "revenue_growth_pct": _pct(info.get("revenueGrowth")),
        "earnings_growth_pct": _pct(info.get("earningsGrowth")),
        "earnings_quarterly_growth_pct": _pct(info.get("earningsQuarterlyGrowth")),
    }
    out["data_coverage"].append("profitability_and_growth_yoy")

    # -----------------------------------------------------------------------
    # 4. Dividends
    # -----------------------------------------------------------------------
    out["dividends"] = {
        "yield_pct": _div_yield(info),
        "annual_rate": _f(info.get("dividendRate") or info.get("trailingAnnualDividendRate")),
        "payout_ratio_pct": _pct(info.get("payoutRatio")),
        "last_dividend_value": _f(info.get("lastDividendValue")),
        "history": {},
        "years_paying": None,
        "pays_5_plus_years": False,
    }
    try:
        div_hist = ticker.dividends
        if not div_hist.empty:
            recent = div_hist.tail(12)
            out["dividends"]["history"] = {str(k.date()): _f(v) for k, v in recent.items()}
            span = (div_hist.index[-1] - div_hist.index[0]).days / 365
            out["dividends"]["years_paying"] = round(span, 1)
            out["dividends"]["pays_5_plus_years"] = span >= 5
            out["data_coverage"].append("dividend_history")
    except Exception as e:
        out["notes"].append(f"dividends history: {e}")

    # -----------------------------------------------------------------------
    # 5. Multi-year EPS & Revenue (for CAGR)
    # -----------------------------------------------------------------------
    out["earnings_history"] = {}
    try:
        # Try income_stmt first (newer API)
        stmt = ticker.income_stmt
        if stmt is not None and not stmt.empty and len(stmt.columns) > 1:
            for col in stmt.columns[:4]:
                yr = str(col.year) if hasattr(col, "year") else str(col)[:4]
                row_data = {}
                for idx in stmt.index:
                    row_data[str(idx)] = _f(stmt.loc[idx, col])
                out["earnings_history"][yr] = row_data
            out["data_coverage"].append("income_stmt_multiyear")
        else:
            # Fallback: try earnings (older API - returns EPS + Revenue by year)
            earn = ticker.earnings
            if earn is not None and not earn.empty:
                for yr_idx, row in earn.iterrows():
                    yr = str(yr_idx)
                    out["earnings_history"][yr] = {
                        "revenue": _f(row.get("Revenue")),
                        "earnings": _f(row.get("Earnings")),
                    }
                out["data_coverage"].append("earnings_history_multiyear")
    except Exception as e:
        out["notes"].append(f"earnings history: {e}")

    # -----------------------------------------------------------------------
    # 6. Derived / Calculated Metrics
    # -----------------------------------------------------------------------
    derived = {}

    # Multi-year CAGR from earnings history
    yrs = sorted(out["earnings_history"].keys(), reverse=True)
    if len(yrs) >= 4:
        def get_val(yr_key, *keys):
            d = out["earnings_history"].get(yr_key) or {}
            for k in keys:
                if d.get(k) is not None:
                    return d[k]
            return None

        # Revenue 3YR CAGR (if revenue data available)
        r_latest = get_val(yrs[0], "Total Revenue", "revenue")
        r_3ago = get_val(yrs[3], "Total Revenue", "revenue")
        if r_latest and r_3ago:
            derived["revenue_3yr_cagr_pct"] = _cagr(r_3ago, r_latest, 3)

        # EPS 3YR CAGR (proxy for earnings growth when revenue not available)
        e_latest = get_val(yrs[0], "Diluted EPS", "Basic EPS", "earnings")
        e_3ago = get_val(yrs[3], "Diluted EPS", "Basic EPS", "earnings")
        if e_latest and e_3ago:
            derived["eps_3yr_cagr_pct"] = _cagr(e_3ago, e_latest, 3)

    # FCF / Net Income
    fcf = out["financials_ttm"].get("free_cashflow")
    ni = out["financials_ttm"].get("net_income")
    if fcf and ni and ni != 0:
        derived["fcf_to_net_income_pct"] = round((fcf / ni) * 100, 2)

    # FCF Margin
    rev = out["financials_ttm"].get("revenue")
    if fcf and rev and rev > 0:
        derived["fcf_margin_pct"] = round((fcf / rev) * 100, 2)

    # Net Income Margin (cross-check vs profitability.net_margin_pct)
    if ni and rev and rev > 0:
        derived["net_income_margin_pct"] = round((ni / rev) * 100, 2)

    # Operating CF / Net Income (quality of earnings proxy)
    ocf = out["financials_ttm"].get("operating_cashflow")
    if ocf and ni and ni != 0:
        derived["ocf_to_net_income_pct"] = round((ocf / ni) * 100, 2)

    # Payout sustainability: dividends paid vs net income
    div_rate = out["dividends"].get("annual_rate")
    shares = out["financials_ttm"].get("shares_outstanding")
    eps = out["valuation"].get("eps_ttm")
    if div_rate and eps and eps > 0:
        derived["dividend_coverage_ratio"] = round(eps / div_rate, 2)

    # Price vs 200d MA
    current_px = out["price"].get("current")
    ma200 = out["price"].get("ma_200d")
    if current_px and ma200 and ma200 > 0:
        derived["price_vs_200d_ma_pct"] = round(((current_px - ma200) / ma200) * 100, 2)

    out["derived"] = derived
    out["data_coverage"].append("derived_metrics")

    # -----------------------------------------------------------------------
    # 7. Analyst Consensus
    # -----------------------------------------------------------------------
    out["analyst_consensus"] = {
        "recommendation": info.get("recommendationKey"),
        "rating_text": info.get("averageAnalystRating"),
        "mean_score": _f(info.get("recommendationMean")),   # 1=Strong Buy, 5=Sell
        "number_of_analysts": info.get("numberOfAnalystOpinions"),
        "target_price_mean": _f(info.get("targetMeanPrice")),
        "target_price_median": _f(info.get("targetMedianPrice")),
        "target_price_high": _f(info.get("targetHighPrice")),
        "target_price_low": _f(info.get("targetLowPrice")),
        "upside_pct": round(
            ((info.get("targetMeanPrice") or 0) - (info.get("currentPrice") or 1))
            / (info.get("currentPrice") or 1) * 100, 1
        ) if info.get("targetMeanPrice") and info.get("currentPrice") else None,
    }
    out["data_coverage"].append("analyst_consensus")

    # -----------------------------------------------------------------------
    # 8. Management / Officers
    # -----------------------------------------------------------------------
    officers = info.get("companyOfficers") or []
    out["management"] = [
        {
            "name": o.get("name"),
            "title": o.get("title"),
            "age": o.get("age"),
            "year_born": o.get("yearBorn"),
        }
        for o in officers[:8]  # top 8 officers
    ]
    if out["management"]:
        out["data_coverage"].append("management_officers")

    # -----------------------------------------------------------------------
    # 9. Ownership
    # -----------------------------------------------------------------------
    out["ownership"] = {
        "insiders_pct": _pct(info.get("heldPercentInsiders")),
        "institutions_pct": _pct(info.get("heldPercentInstitutions")),
    }

    # -----------------------------------------------------------------------
    # 10. 1-Year Price History
    # -----------------------------------------------------------------------
    out["price_1y"] = {}
    try:
        hist = ticker.history(period="1y")
        if not hist.empty:
            s = float(hist["Close"].iloc[0])
            e = float(hist["Close"].iloc[-1])
            out["price_1y"] = {
                "start_price": _f(s),
                "end_price": _f(e),
                "change_pct": round((e - s) / s * 100, 2),
                "high_1y": _f(float(hist["High"].max())),
                "low_1y": _f(float(hist["Low"].min())),
                "avg_daily_volume": round(float(hist["Volume"].mean())),
            }
            out["data_coverage"].append("price_1y_history")
    except Exception as e:
        out["notes"].append(f"price history: {e}")

    # -----------------------------------------------------------------------
    # 11. Market Index comparison
    # Detect exchange and compare against the right benchmark index.
    # Uses yfinance directly (more reliable than FinanceDataReader for Asian indices).
    # -----------------------------------------------------------------------
    out["market_comparison"] = {}
    exchange = out.get("exchange", "")
    index_map = {
        "SET": "^SET.BK",    # Thailand SET
        "SES": "^STI",       # Singapore STI (yfinance uses SES)
        "SGX": "^STI",       # Singapore STI (alias)
        "HKG": "^HSI",       # Hong Kong HSI
        "HKS": "^HSI",       # Hong Kong HSI (small-cap board alias)
        "NYQ": "^GSPC",      # NYSE → S&P 500
        "NMS": "^IXIC",      # NASDAQ
        "NGM": "^IXIC",
        "VSE": "^VNINDEX",   # Vietnam Ho Chi Minh SE
        "HNX": "^VNINDEX",   # Vietnam Hanoi SE
        "LSE": "^FTSE",      # London SE → FTSE 100
    }
    index_ticker = index_map.get(exchange, "^GSPC")  # default S&P 500
    try:
        idx = yf.Ticker(index_ticker)
        idx_hist = idx.history(period="1y")
        if not idx_hist.empty:
            idx_s = float(idx_hist["Close"].iloc[0])
            idx_e = float(idx_hist["Close"].iloc[-1])
            idx_1y = round((idx_e - idx_s) / idx_s * 100, 2)
            stock_1y = out["price_1y"].get("change_pct")
            out["market_comparison"] = {
                "index_ticker": index_ticker,
                "index_1y_pct": idx_1y,
                "stock_1y_pct": stock_1y,
                "vs_index_pct": round(float(stock_1y) - idx_1y, 2) if stock_1y is not None else None,
            }
            out["data_coverage"].append("market_index_comparison")
    except Exception as e:
        out["notes"].append(f"market index comparison ({index_ticker}): {e}")

    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_stock_data.py <TICKER>", file=sys.stderr)
        print("  Thai SET:  SCB.BK", file=sys.stderr)
        print("  US:        AAPL", file=sys.stderr)
        print("  SGX:       D05.SI", file=sys.stderr)
        sys.exit(1)

    sym = sys.argv[1].upper()
    print(f"Fetching {sym} ...", file=sys.stderr)
    result = fetch(sym)
    print(json.dumps(result, indent=2, default=str))
