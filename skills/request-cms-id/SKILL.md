---
name: request-cms-id
description: This skill should be used when the user asks to "request a CMS ID", "request CMS", "submit a CMS request", "create CMS ID", "request translation", or "fill CMS form". Guides the user through filling and submitting the Agoda Translation Request Form on ClickUp, including preparing the CMS Excel template.
---

# CMS ID Request

Automate filling the Agoda Translation Request Form at:
`https://forms.clickup.com/9018034443/f/8cr8j8b-76598/M32EZJJCRLFHMJRO1L`

## Workflow

### Step 1 — Gather request-specific info from the user

Ask the user for the following (these change every request):

1. **Request title / subject** — Format: `CMS ID & Translation of {element} in {page} for {feature}`
2. **English copy** — The exact text to translate (use `{0}`, `{1}`, etc. for dynamic placeholders)
3. **Placeholder values** — Explain each `{n}` placeholder (e.g. `{0}` is the currency symbol)
4. **ID/Copy Description** — Purpose, placement, market, and any context for translators

If the user provides context (e.g. a screenshot or description), draft the fields yourself and confirm before proceeding.

### Step 2 — Prepare the CMS Excel template

Fill in the CSV template (saved at `assets/CMS_Content_Template.csv`) with only the required fields:

| Column | Value |
|--------|-------|
| ID/Copy Description | Drafted from user context |
| English Copy | Exact copy with `{n}` placeholders |
| Placeholder value | Explanation of each `{n}` |

Leave all other columns blank. Save the filled file to `~/Downloads/CMS_Request_{feature}.csv`.

### Step 3 — Fill the ClickUp form via Playwright

Open the form and fill in each field:

**Always ask the user for:**
- Request title / subject (unique per request)

**Pre-fill from context then confirm:**
- Detailed instructions (draft from user's description)

**Use defaults (fill automatically, no need to ask):**

| Field | Default |
|-------|---------|
| Request type | Create and translate new CMS ID |
| Content type | Front-end Website (Non-Whitelabel) |
| Has English copy been reviewed? | My copy has been reviewed already |
| Languages needed | All 38 Front-end Languages |
| Volume / delivery time | Under 1000 words - Up to 5 working days |
| Your first name / nickname | Cup |
| Your email | kolathee.payuhawattana@agoda.com |
| Add your team in CC | team-it-payment-flexibility@agoda.com |

**Upload:**
- Text file / CMS template → upload the filled CSV from Step 2
- Reference images → upload if user provides any

**Fill if provided:**
- Reference links → Figma, Confluence, or Jira URL

### Step 4 — Let user review and submit manually

After filling all fields, take a full-page screenshot and show a summary table of all filled values. **Do NOT click Submit** — the user will review and submit manually.

## Detailed Instructions Template

Use this structure for the "Detailed instructions" field:

```
Purpose: Request CMS ID and translations for {element} on the {page} introducing the {feature}.

Content: "{English copy with ₹/$ symbol as example}"

Context: {What the copy communicates to the user and when it appears}

Market: {Target market, e.g. India only}

Platform/Placement: {Page name} — {where on the page}. {Any size/character constraints}.

Tone: {e.g. Clear, concise, informative}
```

## Notes

- **Do not auto-submit** — always leave form submission to the user
- The CMS template CSV is at `assets/CMS_Content_Template.csv`
- The ClickUp form file upload requires triggering the hidden file input via JavaScript: `document.querySelector('#cu-form-file-field-input-1').click()`
- If the user changes a default (e.g. languages, delivery time), update it for this request only — defaults remain unchanged
