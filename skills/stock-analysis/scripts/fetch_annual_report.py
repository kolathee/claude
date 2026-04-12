#!/usr/bin/env python3
"""
Annual Report Fetcher - Global Coverage
=========================================
Downloads and extracts narrative sections from annual reports for any
publicly traded company worldwide.

Source strategy by exchange:
  US (NYSE/NASDAQ)   → SEC EDGAR 10-K (HTML) via official API
  Thailand (SET)     → IR page PDF
  Singapore (SGX)    → IR page PDF
  Hong Kong (HKEX)   → IR page PDF
  Other              → IR page PDF

Extracted sections:
  ceo_letter          - Letter to Shareholders / Chairman's Message
  mda                 - Management Discussion & Analysis
  business_overview   - Business Description / About Us
  corporate_governance - Governance Report / Board Report
  risk_factors        - Risk Factors / Principal Risks
  esg_sustainability  - Sustainability / ESG / CSR
  auditor_report      - Independent Auditor's Report

Output:
  Summary JSON to stdout. Full sections cached to:
  ~/.claude/skills/stock-analysis/cache/{TICKER}_{YEAR}_annual_report.json

Usage:
  python fetch_annual_report.py AAPL
  python fetch_annual_report.py SCB.BK
  python fetch_annual_report.py D05.SI
  python fetch_annual_report.py --pdf /path/to/report.pdf --ticker ACME
  python fetch_annual_report.py AAPL --section mda
  python fetch_annual_report.py AAPL --no-cache

Requirements:
  pip install pdfplumber beautifulsoup4 lxml yfinance requests
"""

import sys
import os
import re
import json
import time
import argparse
import tempfile
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

# Per-section word limits — critical sections get higher caps
# business_overview and risk_factors are top priority: capture as fully as possible
SECTION_MAX_WORDS = {
    "business_overview":    20000,  # CRITICAL — capture fully
    "risk_factors":         20000,  # CRITICAL — capture fully
    "mda":                  12000,  # Important — financial commentary + outlook
    "ceo_letter":            8000,  # Important — management tone
    "corporate_governance":  5000,  # Lower priority — partial OK
    "esg_sustainability":    4000,  # Lower priority — partial OK
    "auditor_report":        3000,  # Lower priority — going concern flag only
}
DEFAULT_MAX_SECTION_WORDS = 8000  # fallback for any unlisted section
CACHE_DIR = Path.home() / ".claude/skills/stock-analysis/cache"
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/pdf,*/*",
}
SEC_HEADERS = {
    # SEC requires a real contact in User-Agent per their policy
    "User-Agent": "annual-report-fetcher research@example.com",
    "Accept": "application/json, text/html",
}
US_EXCHANGES = {"NYQ", "NMS", "NGM", "PCX", "ASE", "BATS"}
HK_EXCHANGES  = {"HKG", "HKS"}
VN_EXCHANGES  = {"VSE", "HNX"}   # Ho Chi Minh SE, Hanoi SE

# ---------------------------------------------------------------------------
# Section patterns
# ---------------------------------------------------------------------------

# Maps section keys to (regex_patterns, SEC_item_numbers)
SECTIONS = {
    "ceo_letter": {
        "patterns": [
            r"letter\s+to\s+shareholders",
            r"letter\s+from\s+(the\s+)?(chairman|ceo|president|group\s+ceo|board)",
            r"dear\s+(fellow\s+)?shareholders",
            r"message\s+from\s+(the\s+)?(chairman|ceo|president|group\s+ceo)",
            r"chairman[''']?s?\s+(letter|message|statement|review)",
            r"ceo[''']?s?\s+(letter|message|statement|reflections)",
            r"ceo\s+reflections",
            r"to\s+our\s+(shareholders|stockholders|investors)",
            r"message\s+from\s+(the\s+)?board",
            # Vietnamese
            r"th[uư]\s+c[uủ]a\s+(ch[uủ]\s+t[ịi]ch|t[ổo][nể]g\s+gi[aá]m\s+[dđ][oố]c)",
            r"th[uư]\s+g[uử]i\s+c[oổ]\s+[dđ][oô]ng",
        ],
        "sec_items": [],      # Not in 10-K body
        "sec_20f_items": [],  # Not in 20-F body either
    },
    "business_overview": {
        "patterns": [
            r"item\s+1[\.\s](?!a[\.\s])",
            r"business\s+overview", r"description\s+of\s+(our\s+)?business",
            r"about\s+(us|the\s+company)", r"company\s+overview",
            r"our\s+business", r"group\s+overview", r"nature\s+of\s+business",
            r"gi[oớ]i\s+thi[eệ]u\s+(c[oô]ng\s+ty|doanh\s+nghi[eệ]p)",  # Vietnamese
        ],
        "sec_items": ["1"],       # 10-K: Item 1
        "sec_20f_items": ["4"],   # 20-F: Item 4 – Information on the Company
    },
    "risk_factors": {
        "patterns": [
            r"item\s+1a[\.\s]",
            r"risk\s+factors", r"principal\s+risks?\s+and\s+uncertainties",
            r"key\s+risks?", r"material\s+risks?",
            r"y[eế]u\s+t[oố]\s+r[uủ]i\s+ro",  # Vietnamese
        ],
        "sec_items": ["1A"],      # 10-K: Item 1A
        "sec_20f_items": ["3D"],  # 20-F: Item 3.D – Risk Factors
    },
    "mda": {
        "patterns": [
            r"item\s+7[\.\s]",
            r"management[''']?s?\s+discussion\s+and\s+analysis",
            r"management\s+discussion\s+(&|and)\s+analysis",
            r"\bmd&a\b", r"operating\s+and\s+financial\s+review",
            r"financial\s+review\s+and\s+analysis", r"review\s+of\s+operations",
            r"b[aá]o\s+c[aá]o\s+ban\s+[dđ]i[eề]u\s+h[aà]nh",  # Vietnamese
        ],
        "sec_items": ["7"],       # 10-K: Item 7
        "sec_20f_items": ["5"],   # 20-F: Item 5 – Operating and Financial Review
    },
    "corporate_governance": {
        "patterns": [
            r"corporate\s+governance\s+report",
            r"corporate\s+governance\s+statement",
            r"governance\s+report", r"directors[''']?\s+report",
            r"statement\s+on\s+corporate\s+governance",
            r"report\s+on\s+corporate\s+governance",
            r"qu[aả]n\s+tr[ịi]\s+c[oô]ng\s+ty",  # Vietnamese
        ],
        "sec_items": [],      # In DEF 14A proxy, not 10-K body
        "sec_20f_items": [],  # Not in 20-F body
    },
    "esg_sustainability": {
        "patterns": [
            r"sustainability\s+report", r"sustainability\s+(and|&)\s+responsibility",
            r"environmental,?\s+social\s+(and|&|,)\s+governance",
            r"\besg\b", r"corporate\s+social\s+responsibility",
            r"\bcsr\b", r"sustainable\s+development",
            r"ph[aá]t\s+tri[eể]n\s+b[eề]n\s+v[uữ]ng",  # Vietnamese
        ],
        "sec_items": [],
        "sec_20f_items": [],
    },
    "auditor_report": {
        "patterns": [
            r"independent\s+(registered\s+public\s+accounting\s+firm|auditor)[''']?s?\s+report",
            r"report\s+of\s+independent\s+(registered\s+public\s+accounting|auditors?)",
            r"auditors?[''']?\s+report",
            r"b[aá]o\s+c[aá]o\s+ki[eể]m\s+to[aá]n",  # Vietnamese
        ],
        "sec_items": [],
        "sec_20f_items": [],
    },
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _log(msg): print(f"  {msg}", file=sys.stderr)

def _clean(text):
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = re.sub(r'-\n([a-z])', r'\1', text)
    return text.strip()

def _truncate(text, max_words=None, section_key=None):
    """Truncate text to max_words. Uses per-section limits when section_key is provided."""
    if max_words is None:
        max_words = SECTION_MAX_WORDS.get(section_key, DEFAULT_MAX_SECTION_WORDS) if section_key else DEFAULT_MAX_SECTION_WORDS
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + f"\n\n[... truncated at {max_words} of {len(words)} words ...]"

def _cache_path(ticker, year):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{ticker.upper()}_{year}_annual_report.json"


# ---------------------------------------------------------------------------
# SEC EDGAR path (US stocks)
# ---------------------------------------------------------------------------

def fetch_sec_10k(ticker: str) -> dict:
    """
    Download and parse annual report from SEC EDGAR.

    Handles both form types:
    - 10-K  : US domestic companies (NYSE, NASDAQ)
    - 20-F  : Foreign private issuers with US ADR/listings
               (e.g. Alibaba as BABA, HSBC as HSBC, Toyota as TM)

    The parsing logic is the same since 20-F uses the same Item 1 / 1A / 7
    structure as 10-K for the narrative sections.
    """
    import requests
    from bs4 import BeautifulSoup

    sections = {k: None for k in SECTIONS}

    # Step 1: Ticker → CIK
    _log("Looking up CIK on SEC EDGAR...")
    try:
        r = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers=SEC_HEADERS, timeout=15
        )
        tickers_map = r.json()
        match = next(
            (v for v in tickers_map.values() if v["ticker"].upper() == ticker.upper()),
            None
        )
        if not match:
            _log(f"Ticker {ticker} not found in SEC EDGAR")
            return sections
        cik = str(match["cik_str"]).zfill(10)
        company_name = match["title"]
        _log(f"Found: {company_name} | CIK: {cik}")
    except Exception as e:
        _log(f"CIK lookup failed: {e}")
        return sections

    # Step 2: Get latest 10-K or 20-F filing (prefer 10-K if both exist)
    try:
        r = requests.get(
            f"https://data.sec.gov/submissions/CIK{cik}.json",
            headers=SEC_HEADERS, timeout=15
        )
        filings = r.json()["filings"]["recent"]
        forms = filings["form"]

        # Try 10-K first, fall back to 20-F (foreign private issuer annual report)
        filing_idx = next((i for i, f in enumerate(forms) if f == "10-K"), None)
        form_type = "10-K"
        if filing_idx is None:
            filing_idx = next((i for i, f in enumerate(forms) if f == "20-F"), None)
            form_type = "20-F"

        if filing_idx is None:
            _log("No 10-K or 20-F filing found on SEC EDGAR")
            return sections

        acc_raw = filings["accessionNumber"][filing_idx]
        acc = acc_raw.replace("-", "")
        primary_doc = filings["primaryDocument"][filing_idx]
        filing_date = filings["filingDate"][filing_idx]
        cik_int = int(cik)
        doc_url = f"https://www.sec.gov/Archives/edgar/data/{cik_int}/{acc}/{primary_doc}"
        _log(f"{form_type} filed {filing_date}: {doc_url}")
    except Exception as e:
        _log(f"Filing lookup failed: {e}")
        return sections

    # Step 3: Download and parse the 10-K HTML
    try:
        r = requests.get(doc_url, headers=SEC_HEADERS, timeout=60)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")

        # Remove script/style noise
        for tag in soup(["script", "style", "ix:header"]):
            tag.decompose()

        full_text = soup.get_text(separator="\n")
        _log(f"Downloaded {form_type} HTML ({len(full_text):,} chars)")

        sections = _parse_sec_text(full_text, form_type)
    except Exception as e:
        _log(f"{form_type} download/parse failed: {e}")

    return sections


def _parse_sec_text(text: str, form_type: str = "10-K") -> dict:
    """
    Parse SEC annual report text by finding ITEM X boundaries.

    Supports both form types:
    - 10-K (US domestic):  Item 1, Item 1A, Item 7
    - 20-F (foreign filer): Item 4, Item 3.D / 3D, Item 5

    The item numbering in each SECTIONS entry is specified separately as
    sec_items (10-K) and sec_20f_items (20-F).
    """
    sections = {k: None for k in SECTIONS}

    # Build item → section_key mapping depending on form type
    item_key = "sec_20f_items" if form_type == "20-F" else "sec_items"
    item_to_section = {}
    for sec_key, config in SECTIONS.items():
        for item in config.get(item_key, []):
            item_to_section[item.upper()] = sec_key

    if not item_to_section:
        return sections

    # Item number pattern covers both 10-K style (1A, 7A) and 20-F style (3D, 3.D)
    item_re = re.compile(
        r'(?:^|\n)\s*ITEM\s+(1[A-B]?|2|3[A-D]?|4[A-B]?|5|6|7[A-B]?|8|9[A-B]?|'
        r'10|11|12|13|14|15)\s*[.\-:\s]',
        re.IGNORECASE | re.MULTILINE
    )
    matches = list(item_re.finditer(text))

    for i, m in enumerate(matches):
        # Normalise: "3.D" → "3D", "3D" → "3D"
        raw = m.group(1).upper().replace(".", "")
        if raw not in item_to_section:
            continue

        sec_key = item_to_section[raw]
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)

        chunk = text[start:end]
        if len(chunk.split()) < 100:   # skip table-of-contents hits
            continue

        if sections[sec_key] is None:
            sections[sec_key] = _truncate(_clean(chunk), section_key=sec_key)
            _log(f"  [SEC/{form_type}] [{sec_key}] Item {raw} → {len(chunk.split())} words")

    return sections


# Keep the old name as an alias so nothing breaks
def _parse_10k_text(text: str) -> dict:
    return _parse_sec_text(text, "10-K")


# ---------------------------------------------------------------------------
# PDF path (non-US stocks)
# ---------------------------------------------------------------------------

def _extract_pdf_from_page_source(html: str, page_url: str) -> list[str]:
    """
    Extract PDF URLs embedded in page HTML/JavaScript.

    Handles multiple patterns:
    - Direct .pdf hrefs in <a> tags
    - PDF URLs in Vue/React component attributes (e.g. <pdf-viewer src="...">)
    - PDF URLs anywhere in inline JS or JSON blobs
    - Two-level viewer indirection: if a URL resolves to another HTML page
      that contains a PDF URL (e.g. optiwise.io viewer pages)
    """
    import requests as _req

    found = []

    # 1. Direct .pdf URLs anywhere in source (href, src, JS strings, etc.)
    for m in re.finditer(r'https?://[^\s"\'<>\)]+\.pdf[^\s"\'<>\)]*', html):
        url = m.group(0).rstrip(".,;)")
        found.append(url)

    # 2. Component attribute src/data-src that might be PDF viewer pages
    #    e.g. <pdf-viewer src="https://hub.optiwise.io/en/documents/123/report.pdf">
    for m in re.finditer(r'src=["\']?(https?://[^\s"\'<>]+)["\']?', html):
        candidate = m.group(1).rstrip(".,;)")
        if "document" in candidate or "report" in candidate or "annual" in candidate:
            found.append(candidate)

    # 3. De-dup
    found = list(dict.fromkeys(found))

    # 4. For any non-PDF URL that looks like a viewer page, try one more level
    resolved = []
    for url in found:
        if url.lower().endswith(".pdf"):
            resolved.append(url)
        else:
            # Might be a viewer page — fetch it and extract the storage PDF URL
            try:
                r = _req.get(url, headers=BROWSER_HEADERS, timeout=10, allow_redirects=True)
                if r.status_code == 200 and "html" in r.headers.get("Content-Type", ""):
                    for m2 in re.finditer(r'https?://[^\s"\'<>\)]+\.pdf[^\s"\'<>\)]*', r.text):
                        inner = m2.group(0).rstrip(".,;)")
                        resolved.append(inner)
                    # Also check src= attributes
                    for m2 in re.finditer(r'src=["\']?(https?://[^\s"\'<>]+\.pdf[^\s"\'<>]*)["\']?', r.text):
                        resolved.append(m2.group(1).rstrip(".,;)"))
            except Exception:
                pass

    return list(dict.fromkeys(resolved))  # dedupe, preserve order


def _get_base_urls(website: str) -> list[str]:
    """
    Given a company's main website URL, return candidate base URLs to try.
    Adds investor.* and ir.* subdomain variants.
    """
    from urllib.parse import urlparse
    parsed = urlparse(website)
    domain = parsed.netloc  # e.g. www.scbx.com
    scheme = parsed.scheme or "https"

    # Strip common www prefix for subdomain variants
    bare_domain = re.sub(r'^www\.', '', domain)

    bases = [website.rstrip("/")]
    for sub in ("investor", "ir", "investors"):
        if not domain.startswith(sub):
            bases.append(f"{scheme}://{sub}.{bare_domain}")
    return bases


def find_pdf_on_ir_page(base_url: str) -> str | None:
    """
    Scan IR page and common sub-paths for annual report PDF links.

    Strategy:
    1. Try investor.*, ir.* subdomains as well as the main website
    2. For each base, try common IR sub-paths
    3. If a link looks like a document viewer (not a direct PDF), fetch that
       viewer page and extract the embedded PDF URL from page source
    """
    import requests
    from bs4 import BeautifulSoup

    ir_paths = [
        "", "/investor-relations", "/investors", "/ir",
        "/investor-relations/annual-reports", "/investors/annual-reports",
        "/en/investor-relations", "/en/investors",
        "/annual-report", "/annual-reports",
        "/en/document/annual-reports", "/en/annual-report",
        "/document/annual-reports",
        # Vietnamese exchange paths (VSE/HNX companies)
        "/quan-he-co-dong", "/nha-dau-tu", "/bao-cao-thuong-nien",
        "/vi/quan-he-co-dong", "/vi/nha-dau-tu",
        "/en/investor-relations/annual-reports",
    ]

    annual_keywords = [
        "annual", "annual-report", "annualreport", "ar20", "56-1", "one-report",
    ]

    candidates = []

    # Build list of base URLs to try (main site + investor.* / ir.*)
    bases_to_try = _get_base_urls(base_url)

    for base in bases_to_try:
        if candidates:
            break
        for path in ir_paths:
            url = base.rstrip("/") + path
            try:
                r = requests.get(url, headers=BROWSER_HEADERS, timeout=15, allow_redirects=True)
                if r.status_code != 200:
                    continue
                soup = BeautifulSoup(r.text, "lxml")

                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    link_text = a.get_text(strip=True).lower()
                    full = href if href.startswith("http") else urljoin(url, href)
                    is_annual = any(kw in link_text or kw in full.lower() for kw in annual_keywords)

                    if href.lower().endswith(".pdf") and is_annual:
                        # Direct PDF link
                        candidates.append((full, link_text))

                    elif is_annual and "viewer" in full.lower() and "annual" in full.lower():
                        # Viewer page — try to extract embedded PDF URL
                        try:
                            vr = requests.get(full, headers=BROWSER_HEADERS, timeout=15)
                            if vr.status_code == 200:
                                embedded = _extract_pdf_from_page_source(vr.text, full)
                                for ep in embedded:
                                    if any(kw in ep.lower() for kw in annual_keywords + ["scb", "report", "annual"]):
                                        candidates.append((ep, link_text + " [via viewer]"))
                                        _log(f"  Extracted PDF from viewer: {ep}")
                        except Exception:
                            pass

                if candidates:
                    break
                time.sleep(0.3)
            except Exception:
                continue

    # Level-2 crawl: if no direct PDFs found yet, follow "annual report" page
    # links and look for PDFs on those pages (handles HSBC-style sites where
    # the main IR page links to /investors/results-and-announcements/annual-report
    # which in turn has the actual PDF download links).
    if not candidates:
        visited = set()
        for base in bases_to_try:
            if candidates:
                break
            for path in ir_paths:
                url = base.rstrip("/") + path
                if url in visited:
                    continue
                try:
                    r = requests.get(url, headers=BROWSER_HEADERS, timeout=15, allow_redirects=True)
                    if r.status_code != 200:
                        continue
                    visited.add(r.url)
                    soup = BeautifulSoup(r.text, "lxml")

                    # Collect links whose text/href strongly suggests "annual report" page
                    ar_page_links = []
                    for a in soup.find_all("a", href=True):
                        href = a["href"]
                        text = a.get_text(strip=True).lower()
                        combined = text + " " + href.lower()
                        if "annual" in combined and ("report" in combined or "filing" in combined):
                            full = href if href.startswith("http") else urljoin(url, href)
                            if full not in visited:
                                ar_page_links.append(full)

                    # Visit each "annual report" page and look for PDFs
                    for ar_url in ar_page_links[:5]:  # cap at 5 to avoid crawling too broadly
                        try:
                            visited.add(ar_url)
                            ar_r = requests.get(ar_url, headers=BROWSER_HEADERS, timeout=15, allow_redirects=True)
                            if ar_r.status_code != 200:
                                continue
                            ar_soup = BeautifulSoup(ar_r.text, "lxml")
                            for a in ar_soup.find_all("a", href=True):
                                href = a["href"]
                                link_text = a.get_text(strip=True).lower()
                                combined = href.lower() + " " + link_text
                                if ".pdf" in href.lower() and any(kw in combined for kw in annual_keywords):
                                    full = href if href.startswith("http") else urljoin(ar_url, href)
                                    candidates.append((full, link_text + " [via AR page]"))
                                    _log(f"  Found PDF via AR page: {full[:80]}")
                        except Exception:
                            continue

                    if candidates:
                        break
                except Exception:
                    continue

    if not candidates:
        return None

    # Prefer most recent year
    def year_score(item):
        m = re.findall(r'20(2[0-9])', item[0] + item[1])
        return max([int(y) for y in m], default=0)

    candidates.sort(key=year_score, reverse=True)
    _log(f"Best PDF candidate: {candidates[0][1][:50]} → {candidates[0][0]}")
    return candidates[0][0]


def download_pdf(url: str) -> str | None:
    """
    Download a PDF from url to a temp file.

    Some IR portals use URLs ending in .pdf that actually serve an HTML viewer
    page (e.g. optiwise.io /en/documents/... URLs). When that happens, try to
    extract the real storage PDF URL from the viewer HTML and follow it.
    """
    import requests
    _log(f"Downloading PDF...")
    try:
        r = requests.get(url, headers=BROWSER_HEADERS, timeout=90)
        r.raise_for_status()
        content = r.content

        # Check if we got HTML instead of a real PDF
        if not content.startswith(b"%PDF") and b"<html" in content[:200].lower():
            _log("  Got HTML viewer page — extracting real PDF URL...")
            html = content.decode("utf-8", errors="replace")
            # Look for .pdf URLs in source (common in Vue/React viewer pages)
            inner_pdfs = re.findall(r'https?://[^\s"\'<>]+\.pdf[^\s"\'<>]*', html)
            # Also check src= attributes that might be PDF viewer storage paths
            src_attrs = re.findall(r'src=["\']?(https?://[^\s"\'<>]+)["\']?', html)
            inner_pdfs += [s for s in src_attrs if s.endswith(".pdf")]
            inner_pdfs = list(dict.fromkeys(inner_pdfs))

            if inner_pdfs:
                _log(f"  Found embedded PDF URL: {inner_pdfs[0]}")
                # Recurse once (only one level deep)
                r2 = requests.get(inner_pdfs[0], headers=BROWSER_HEADERS, timeout=90)
                r2.raise_for_status()
                content = r2.content
                if not content.startswith(b"%PDF"):
                    _log("  Embedded URL also returned non-PDF content; giving up")
                    return None
            else:
                _log("  Could not find embedded PDF URL in viewer page")
                return None

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp.write(content)
        tmp.close()
        mb = os.path.getsize(tmp.name) / 1_000_000
        _log(f"Downloaded {mb:.1f} MB")
        return tmp.name
    except Exception as e:
        _log(f"Download failed: {e}")
        return None


def extract_pdf_sections(pdf_path: str) -> dict:
    """Extract sections from PDF using bookmarks first, then heading scan."""
    try:
        import pdfplumber
    except ImportError:
        return {k: None for k in SECTIONS}

    sections = {k: None for k in SECTIONS}

    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        _log(f"PDF: {total} pages")

        # Try bookmarks
        toc = []
        try:
            toc = pdf.doc.get_toc() or []
        except Exception:
            pass

        if toc:
            _log(f"Using bookmarks ({len(toc)} entries)")
            sections = _extract_by_bookmarks(pdf, toc, sections)
        else:
            _log("No bookmarks — scanning headings")
            sections = _extract_by_scan(pdf, sections)

    return sections


def _match_section(text_lower: str) -> str | None:
    """Return section key if text matches any pattern."""
    for sec_key, config in SECTIONS.items():
        for pat in config["patterns"]:
            if re.search(pat, text_lower):
                return sec_key
    return None


def _extract_by_bookmarks(pdf, toc, sections):
    for i, entry in enumerate(toc):
        level, title, page_num = entry[0], str(entry[1]).strip(), int(entry[2])
        sec_key = _match_section(title.lower())
        if not sec_key or sections[sec_key]:
            continue

        # End = next same-or-higher-level entry
        end_page = len(pdf.pages)
        for j in range(i + 1, len(toc)):
            if toc[j][0] <= level:
                end_page = min(int(toc[j][2]) + 1, len(pdf.pages))
                break
        end_page = min(end_page, page_num + 80)  # cap section at 80 pages

        parts = []
        for pg in pdf.pages[page_num - 1:end_page]:
            try:
                t = pg.extract_text()
                if t:
                    parts.append(t)
            except Exception:
                pass

        if parts:
            text = _truncate(_clean("\n".join(parts)), section_key=sec_key)
            sections[sec_key] = text
            _log(f"  [{sec_key}] '{title}' pp{page_num}-{end_page} ({len(text.split())} words)")

    return sections


def _extract_by_scan(pdf, sections):
    current = None
    buffers = {k: [] for k in SECTIONS}

    for page in pdf.pages:
        try:
            text = page.extract_text() or ""
        except Exception:
            continue

        heading_zone = text[:500].lower()
        matched = _match_section(heading_zone)
        if matched:
            current = matched

        if current:
            buffers[current].append(text)

    for k, parts in buffers.items():
        if parts:
            sections[k] = _truncate(_clean("\n".join(parts)), section_key=k)

    return sections


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

def fetch(ticker: str, pdf_path: str = None) -> dict:
    import yfinance as yf

    ticker_upper = ticker.upper()
    year = datetime.now().year
    cache_file = _cache_path(ticker_upper, year)

    if cache_file.exists():
        _log(f"Loading from cache: {cache_file}")
        with open(cache_file) as f:
            return json.load(f)

    out = {
        "ticker": ticker_upper,
        "year": year,
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "source": None,
        "pdf_url": None,
        "sections": {k: None for k in SECTIONS},
        "sections_found": [],
        "sections_missing": [],
        "notes": [],
    }

    if pdf_path:
        # Manual PDF provided
        _log(f"Using provided PDF: {pdf_path}")
        out["source"] = "manual_pdf"
        out["sections"] = extract_pdf_sections(pdf_path)
    else:
        info = yf.Ticker(ticker).info or {}
        exchange = info.get("exchange", "")
        website = info.get("website", "")
        company = info.get("longName", ticker)
        _log(f"{company} | {exchange} | {website}")

        if exchange in US_EXCHANGES:
            # US: parse SEC 10-K HTML (also handles 20-F for foreign ADRs on US exchanges)
            out["source"] = "sec_edgar_10k"
            out["sections"] = fetch_sec_10k(ticker)
        elif exchange in HK_EXCHANGES:
            # HK-listed stock: try SEC 20-F first (for dual-listed companies like Alibaba),
            # then fall back to PDF from IR page.
            _log("HK-listed stock — trying SEC EDGAR (20-F) first...")
            sec_sections = fetch_sec_10k(ticker)
            if any(v for v in sec_sections.values()):
                out["source"] = "sec_edgar_20f"
                out["sections"] = sec_sections
            else:
                _log("SEC EDGAR returned no data — falling back to IR page PDF")
                out["source"] = "ir_page_pdf"
        elif exchange in VN_EXCHANGES:
            # Vietnamese stock (VSE/HNX): always use IR page PDF
            _log("Vietnamese exchange — using IR page PDF path")
            out["source"] = "ir_page_pdf"
        else:
            # SGX, LSE, SET, and all others: IR page PDF
            out["source"] = "ir_page_pdf"

        # PDF path for all non-SEC sources
        if out["source"] == "ir_page_pdf":
            pdf_url = None
            if website:
                pdf_url = find_pdf_on_ir_page(website)
            if pdf_url:
                out["pdf_url"] = pdf_url
                tmp = download_pdf(pdf_url)
                if tmp:
                    out["sections"] = extract_pdf_sections(tmp)
                    try:
                        os.unlink(tmp)
                    except Exception:
                        pass
                else:
                    out["notes"].append(f"PDF download failed: {pdf_url}")
            else:
                out["notes"].append(
                    "Could not find annual report PDF automatically. "
                    "Use: python fetch_annual_report.py --pdf /path/to/report.pdf "
                    f"--ticker {ticker}"
                )

    # Summarise
    out["sections_found"] = [k for k, v in out["sections"].items() if v]
    out["sections_missing"] = [k for k, v in out["sections"].items() if not v]
    if out["sections_missing"]:
        out["notes"].append(f"Sections not extracted: {out['sections_missing']}")

    # Cache
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(cache_file, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    _log(f"Cached: {cache_file}")

    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker", nargs="?", help="e.g. AAPL, SCB.BK, D05.SI")
    parser.add_argument("--pdf", help="Path to a local PDF")
    parser.add_argument("--ticker", dest="ticker_flag", help="Ticker alias (alternative to positional arg)")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--section", help="Print one section: mda, risk_factors, ceo_letter, ...")
    args = parser.parse_args()

    # --ticker flag overrides positional arg (allows: --pdf /path --ticker BDMS.BK)
    resolved_ticker = args.ticker_flag or args.ticker

    if not resolved_ticker and not args.pdf:
        parser.print_help()
        sys.exit(1)

    t = (resolved_ticker or "MANUAL").upper()

    if args.no_cache:
        c = _cache_path(t, datetime.now().year)
        if c.exists():
            c.unlink()

    print(f"Fetching annual report: {t}", file=sys.stderr)
    result = fetch(t, pdf_path=args.pdf)

    if args.section:
        text = result["sections"].get(args.section)
        print(text if text else f"Section '{args.section}' not found. Available: {result['sections_found']}")
    else:
        summary = {k: v for k, v in result.items() if k != "sections"}
        print(json.dumps(summary, indent=2, ensure_ascii=False))
