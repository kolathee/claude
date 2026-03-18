---
name: news-summary
description: This skill should be used when the user asks to "fetch news", "get news summary", "show latest news", "summarize news", "get today's headlines", or requests news from Thai sources (Bangkok Post, Matichon, Khaosod, Thairath, MGR Online, The Standard, Mitihoon, Bangkok Biz News, Finnomena, Longtunman, The Standard Wealth) or international business news (HBR).
---

# News Summary Skill

## Purpose

Fetch and summarize news headlines from multiple sources (Thai and international), categorize them by topic across 14 categories (WORLD, INVESTMENT, ECONOMY, BUSINESS, TECH, ENERGY, CRYPTO, COMMODITIES, REAL ESTATE, HEALTHCARE, MANUFACTURING, CONSUMER, AUTOMOTIVE, THAILAND), and present in a clean, readable format with clickable links.

## When to Use

Use this skill when the user requests:
- Daily news summaries
- Headlines from specific news sources
- Categorized news updates
- Latest news across multiple sources

## News Sources

Fetch news from these sources:

### Thai News - General & Politics
1. **Bangkok Post** - https://www.bangkokpost.com/thailand (English, Thailand News)
2. **Matichon** - https://www.matichon.co.th (Thai, General News)
3. **Khaosod** - https://www.khaosod.co.th/home (Thai, General News)
4. **Thairath** - https://www.thairath.co.th/home (Thai, General News)
5. **MGR Online** - https://mgronline.com (Thai, General News)
6. **The Standard** - https://thestandard.co/homepage (Thai, Politics & Current Affairs)

### Thai News - Business & Investment
7. **Thairath Money** - https://www.thairath.co.th/money (Thai, Finance)
8. **Longtunman** - https://www.longtunman.com (Thai, Investment & Finance)
9. **Mitihoon** - https://www.mitihoon.com/ (Thai, Business & Finance)
10. **Bangkok Biz News** - https://www.bangkokbiznews.com/ (Thai, Business)
11. **Finnomena** - https://www.finnomena.com (Thai, Investment & Analysis)
12. **The Standard Wealth** - https://thestandard.co/wealth/ (Thai, Personal Finance & Investment)

### International News - Business & Management
13. **Harvard Business Review** - https://hbr.org/the-latest (English, Business & Management)

## Workflow

### 1. Fetch News Content with Links

Use WebFetch tool to retrieve content from each source, including article URLs:

```
WebFetch(
  url: "https://www.bangkokpost.com/thailand",
  prompt: "Extract the LATEST and most recent news headlines from this page (prioritize today's news). For each headline, provide: 1) The headline title, 2) The full article URL. Format as: 'Headline Title | URL'. One per line. Focus on the top/featured stories that are most recent."
)
```

Repeat for all 13 sources. Fetch news sources in parallel when possible to maximize efficiency.

**Special Note for HBR:** HBR returns relative URLs (starting with `/`). Construct full URLs by prepending `https://hbr.org` to the relative paths.

**Important Notes:**
- Always request both headline text AND article URLs in the WebFetch prompt
- Emphasize "latest", "recent", or "today" in the prompt to prioritize current news
- Most news sites display newest articles first, but explicitly requesting recent news helps

### 2. Filter for Recency and Prioritize Headlines

**Recency Filter (Apply First):**
- **Prioritize today's news**: Focus on headlines from today (2026-03-05)
- **Check for date indicators**: Look for "today", "this morning", present tense verbs, or recent timestamps
- **Avoid old news**: Skip headlines that clearly reference past dates (e.g., "yesterday", "last week", specific old dates)
- **When in doubt**: Include the headline if it appears in the top section of the news site (sites typically show newest first)

**Importance Prioritization (Apply Second):**
Sort remaining headlines by importance, prioritizing:
1. **Breaking news** - Events happening right now, major announcements
2. **Major events** - Significant market moves, policy changes, major incidents
3. **Important updates** - Notable developments in ongoing stories
4. **Regular news** - Standard business/tech/world updates

**Indicators of breaking/major news:**
- Market crashes, circuit breakers, significant percentage moves (>5%)
- Political upheavals, conflicts, major diplomatic events
- Major corporate actions (M&A, CEO changes at large companies, bankruptcies)
- Significant tech launches or breakthroughs
- Natural disasters, crises, emergencies

**Rephrasing Guidelines:**
- **Simplify**: Make headlines clear and easy to understand at a glance
- **Translate Thai**: Convert Thai headlines to clear English while preserving meaning
- **Keep original Thai**: For Thai headlines, ALWAYS add the original Thai text in parentheses after the English translation
- **Remove jargon**: Replace technical terms with plain language where possible
- **Be concise**: Keep English translation to 10-15 words maximum
- **Maintain accuracy**: Don't editorialize or change the factual content
- **Add context**: If helpful, add brief clarification (e.g., "Thailand's SET Index" instead of just "SET")

**Example transformations:**
- Original: "เปิดใจ 'สินนท์' BANPU ในวันที่หุ้นไทยแดงเดือดจนโดน Circuit Breaker"
- Rephrased: "BANPU CEO discusses strategy as Thai stock market triggers circuit breaker (เปิดใจ 'สินนท์' BANPU ในวันที่หุ้นไทยแดงเดือดจนโดน Circuit Breaker)"

- Original: "ยอดลบ ChatGPT พุ่งเกือบ 300%"
- Rephrased: "ChatGPT usage decline surges nearly 300% (ยอดลบ ChatGPT พุ่งเกือบ 300%)"

- Original: "Countdown to new parliament session begins" (English source)
- Rephrased: "Countdown to new parliament session begins" (no Thai text needed for English sources)

### 3. Categorize Headlines

Analyze each rephrased headline and categorize into:

**Core Categories (always check first):**
- **🌍 WORLD** - International affairs, politics, geopolitics, regional news
- **📊 INVESTMENT** - Stock markets, investing strategies, fund performance, portfolio management, trading, gold prices
- **🏦 ECONOMY** - GDP, inflation, interest rates, unemployment, central bank policy, trade balances, economic growth
- **💼 BUSINESS** - Corporate news, company earnings, CEO changes, mergers & acquisitions, industry trends
- **💻 TECH** - Technology, innovation, digital transformation, startups, AI, software

**Sector Categories (if specific sector focus):**
- **⚡ ENERGY** - Oil, gas, renewables, energy prices, OPEC, power generation, energy policy
- **🪙 CRYPTO** - Cryptocurrency, blockchain, Bitcoin, Ethereum, digital assets, Web3, NFTs
- **📦 COMMODITIES** - Metals, agriculture, raw materials (copper, wheat, etc.), commodity prices
- **🏠 REAL ESTATE** - Property market, REITs, housing prices, commercial real estate, mortgages
- **🏥 HEALTHCARE** - Pharmaceuticals, biotech, hospitals, medical devices, drug approvals
- **🏭 MANUFACTURING** - Industrial production, factories, PMI data, supply chains, capacity
- **🛒 CONSUMER** - Retail, consumer goods, spending trends, retail sales, consumer confidence
- **🚗 AUTOMOTIVE** - Auto industry, EVs, autonomous driving, car sales, mobility

**Regional Category:**
- **🇹🇭 THAILAND** - Thai domestic news, local incidents, social issues, crime, weather, cultural events, general Thai affairs that don't fit business/world categories

**Categorization Guidelines:**
- International relations, conflicts, elections → WORLD
- Stock market movements, investment funds, trading strategies, gold prices, circuit breakers → INVESTMENT
- GDP reports, inflation data, central bank decisions, unemployment, economic policy → ECONOMY
- Company earnings, mergers, CEO changes, corporate strategy → BUSINESS
- AI, software, gadgets, tech companies, digital services → TECH
- Oil/gas prices, renewable energy, OPEC decisions → ENERGY
- Bitcoin, Ethereum, crypto regulations, blockchain → CRYPTO
- Metals, agriculture, raw materials → COMMODITIES
- Housing market, property prices, REITs → REAL ESTATE
- Drug approvals, pharma M&A, biotech breakthroughs → HEALTHCARE
- Factory output, industrial production, supply chains → MANUFACTURING
- Retail sales, consumer spending, major retailers → CONSUMER
- EV adoption, car sales, autonomous vehicles → AUTOMOTIVE
- Thai domestic news (crime, accidents, weather, social issues, local politics, cultural events) → THAILAND
- Longtunman articles → typically INVESTMENT
- Thai energy companies (PTT, BANPU energy) → Can be ENERGY or BUSINESS depending on focus
- If a headline fits multiple categories, choose the most specific one
- Bangkok Post, Matichon, Khaosod, Thairath, MGR Online, The Standard → often THAILAND category for general news

### 4. Format Output with Links

Present news in this exact format with clickable markdown links:

```
📰 News Summary [YYYY-MM-DD]

🌍 WORLD
- [English headline 1](article_url_1)
- [English headline 2 (Thai original if from Thai source)](article_url_2)

📊 INVESTMENT
- [English headline 1 (Thai original if from Thai source)](article_url_1)
- [English headline 2 (Thai original if from Thai source)](article_url_2)

🏦 ECONOMY
- [Rephrased headline 1](article_url_1)
- [Rephrased headline 2](article_url_2)

💼 BUSINESS
- [Rephrased headline 1](article_url_1)
- [Rephrased headline 2](article_url_2)

💻 TECH
- [Rephrased headline 1](article_url_1)
- [Rephrased headline 2](article_url_2)

⚡ ENERGY
- [Rephrased headline 1](article_url_1)

🪙 CRYPTO
- [Rephrased headline 1](article_url_1)

📦 COMMODITIES
- [Rephrased headline 1](article_url_1)

🏠 REAL ESTATE
- [Rephrased headline 1](article_url_1)

🏥 HEALTHCARE
- [Rephrased headline 1](article_url_1)

🏭 MANUFACTURING
- [Rephrased headline 1](article_url_1)

🛒 CONSUMER
- [Rephrased headline 1](article_url_1)

🚗 AUTOMOTIVE
- [Rephrased headline 1](article_url_1)

🇹🇭 THAILAND
- [Rephrased headline 1](article_url_1)
```

**Formatting Rules:**
- Use current date in YYYY-MM-DD format
- **Section order must be**: WORLD → INVESTMENT → ECONOMY → BUSINESS → TECH → ENERGY → CRYPTO → COMMODITIES → REAL ESTATE → HEALTHCARE → MANUFACTURING → CONSUMER → AUTOMOTIVE → THAILAND
- **Each headline MUST be a clickable markdown link**: `[headline text](article_url)`
- **For Thai headlines**: Format as `[English translation (Thai original)](url)`
- **For English headlines**: Format as `[English headline](url)` (no Thai text)
- List in order of importance (breaking news first, then major events, then regular news)
- Headlines should be rephrased for clarity per guidelines in step 2
- **If a category has no headlines, omit that section entirely** (very important for sector categories)
- Limit to top 5-8 most important headlines per category for readability
- Within each category, sort by priority: breaking → major → important → regular
- Core categories (WORLD/INVESTMENT/ECONOMY/BUSINESS/TECH) appear first, sector categories in the middle, THAILAND at the end

### 5. Handle Errors Gracefully

If a source fails to load:
- Continue with remaining sources
- Note which source failed at the end: "⚠️ Could not fetch: [source name]"
- Do not halt the entire process

If article URLs are not available:
- Use the source homepage URL as fallback
- Indicate in the warning section that URLs may not link directly to articles

## Example Usage

**User asks:** "Get me today's news summary"

**Process:**
1. Fetch from all 13 sources in parallel (request "latest" and "recent" news)
2. Extract headlines from each
3. Filter for recency (prioritize today's news, skip old headlines)
4. Categorize into 14 possible categories (core + sectors + regional)
5. Format and present (only showing categories with headlines)

**Output:**
```
📰 News Summary 2026-03-05

🌍 WORLD
- [UK sets ambitious 2030 climate targets](https://www.bbc.com/news/climate-targets-2030)
- [G7 summit tackles escalating trade tensions](https://www.bloomberg.com/news/g7-trade)
- [Humanitarian crisis deepens in conflict zone](https://www.bbc.com/news/crisis-update)

📊 INVESTMENT
- [Thai stock market circuit breaker triggered after 8% plunge (หุ้นไทยแดงเดือดจนโดน Circuit Breaker ร่วง 8%)](https://www.longtunman.com/circuit-breaker)
- [Gold prices drop 1,550 baht to 78,500 per baht-weight (ราคาทองวันนี้ร่วง 1,550 บาท ขายออก 78,500 บาท)](https://www.thairath.co.th/money/gold-price)
- [TTB fund surpasses 20,000 million baht in assets (กองทุน TTB ทะลุ 20,000 ล้านบาท)](https://www.longtunman.com/ttb-fund)
- [Dow Jones crashes over 1,000 points as dollar strengthens (ดาวโจนส์ร่วงกว่า 1,000 จุด ดอลลาร์แข็งค่า)](https://www.longtunman.com/dow-crash)

🏦 ECONOMY
- [Federal Reserve signals Q2 rate cut amid inflation concerns](https://www.bloomberg.com/news/fed-rate-cut)
- [Thailand's GDP growth slows to 2.1% in Q4 2025 (GDP ไทยชะลอตัวเหลือ 2.1% ในไตรมาส 4)](https://www.bloomberg.com/news/thailand-gdp)
- [US unemployment rate drops to 3.5% as jobs market strengthens](https://www.bloomberg.com/news/us-jobs)

💼 BUSINESS
- [Siam Commercial Bank names new CEO effective May 1 (ธนาคารไทยพาณิชย์แต่งตั้ง CEO คนใหม่ มีผล 1 พ.ค.)](https://www.thairath.co.th/money/scb-ceo)
- [BANPU CEO remains confident amid market turbulence (CEO BANPU มั่นใจท่ามกลางตลาดผันผวน)](https://www.thairath.co.th/money/banpu-ceo)
- [GGC proposes B10 biodiesel to save 25 billion baht (GGC เสนอไบโอดีเซล B10 ประหยัด 25,000 ล้านบาท)](https://www.thairath.co.th/money/b10-proposal)
- [Booking Holdings posts record quarterly revenue](https://www.bloomberg.com/news/booking-earnings)

💻 TECH
- [Apple unveils major AI features for iOS 19](https://www.bbc.com/news/apple-ai)
- [ChatGPT usage decline surges 300% (ยอดลบ ChatGPT พุ่งเกือบ 300%)](https://www.thairath.co.th/money/chatgpt-decline)
- [BANPU energy giant positions for AI investment wave (BANPU ยักษ์พลังงานเตรียมรับคลื่น AI)](https://www.longtunman.com/banpu-ai)

🇹🇭 THAILAND
- [94 Vietnamese arrested in online gambling raid](https://www.bangkokpost.com/thailand/general/3209854)
- [Court bans Senator Keskamol for false professor claim](https://www.bangkokpost.com/thailand/politics/3209805)
- [Fuel tanker explosion near border kills 1 worker (บึ้มสนั่น รถบรรทุกน้ำมันระเบิด มีผู้เสียชีวิต 1 ราย)](https://www.khaosod.co.th/breaking-news/news_10159315)
- [Police officer shot dead in Yala, gun stolen (กระหน่ำยิง ส.ต.อ. ตำรวจนปพ.เสียชีวิต ชิงปืนพก)](https://www.khaosod.co.th/breaking-news/news_10159259)

⚠️ Note: All 13 sources successfully fetched
```

## Tips for Effective Summaries

1. **Focus on today's news**: Prioritize headlines from today, skip clearly outdated news
2. **Prioritize breaking news**: Put market crashes, major events, and breaking developments first
3. **Rephrase for clarity**: Transform headlines into easy-to-understand English sentences
4. **Preserve Thai context**: ALWAYS include original Thai text in parentheses for Thai headlines
5. **Always include article links**: Every headline must be a clickable markdown link
6. **Avoid duplicates**: If multiple sources report the same story, include only once with the best link
7. **Balance sources**: Try to include headlines from multiple sources in each category
8. **Sort by importance**: Within each category, list breaking → major → important → regular news
9. **Be concise but clear**: 10-15 words per English translation, with enough context to be understandable
10. **Maintain accuracy**: Don't editorialize, but do simplify complex terms

## Troubleshooting

**Issue:** WebFetch returns too much content or full articles

**Solution:** Refine the prompt to specifically ask for "headline titles only, not full articles"

**Issue:** Unable to categorize a headline

**Solution:** Use the dominant theme. If it mentions both business and tech, choose the primary focus. When truly ambiguous, default to BUSINESS for financial news, WORLD for everything else.

**Issue:** Source website structure changed

**Solution:** Adjust WebFetch prompt to match new structure. Try prompts like "Find the main headlines section and extract titles" or "Look for article titles in the homepage layout"

## HTML Output

When the user asks to save as HTML or open in browser:

1. Fetch the template from `skill://news-summary/templates/news-summary.html`
2. Replace `{{DATE}}` with `YYYY-MM-DD` and `{{DATE_LONG}}` with the full date (e.g. `Thursday, March 6, 2026`)
3. Fill in the news items, removing any category blocks that have no headlines
4. Save to `~/daily-reports/news-summary-YYYY-MM-DD.html`
5. Open with `open ~/daily-reports/news-summary-YYYY-MM-DD.html`

**Layout rules:**
- `full-width` single-column: WORLD, ENERGY, CRYPTO, THAILAND (and any lone sector categories)
- `category-grid` 2-column pairs: INVESTMENT+ECONOMY, BUSINESS+TECH, COMMODITIES+REAL ESTATE, HEALTHCARE+MANUFACTURING, CONSUMER+AUTOMOTIVE
- Omit any category block entirely if no headlines were found that day

## Notes

- News sources may have rate limiting or access restrictions
- Some sites may require specific prompts to extract headlines properly
- The skill focuses on headline aggregation, not full article summarization
- For real-time critical news, consider using dedicated news APIs instead of web scraping
