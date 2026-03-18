---
name: test-cashback-card-flow
description: Automate testing the Cashback card payment flow using Playwright MCP. Use when the user asks to test the card flow, test cashback card, test card page, or verify the credit card form submission.
---

# Test Cashback Card Flow

Automates the Cashback credit card redemption flow via Playwright MCP on `localhost:5000`.

## Prerequisites

- Cashback dev server running on `localhost:5000`
- Playwright MCP server connected

## Test Flow

Run **both** scenarios (saved card and new card). Apply testing overrides before starting.

### Step 0: Apply Testing Overrides

Before testing, apply the overrides listed in the "Testing Overrides" section below. These mock the balance, saved cards, and routing so the flow works locally. Skip any override that is already applied.

### Step 1: Navigate to Cashback Summary

```
URL: http://localhost:5000/app/cashback?app_exp=CASH-3277,CASH-3683,ICXP-815-IOS,CASH-3538,CASH-3880
```

Use `browser_navigate` to open the URL. Wait for the page to load.

### Step 2: Click "Request Cashback Reward"

Take a `browser_snapshot`, find the "Request Cashback Reward" button, and click it. A currency bottom sheet will appear.

### Step 3: Select a Currency

From the currency bottom sheet, click a currency (e.g., USD). This navigates to `/app/cashback/cardTransfer`.

### Step 4: Wait for Card Page to Load

Use `browser_wait_for` (3 seconds) for the iframe CC form to load. Take a snapshot to verify saved cards or the new card form is visible inside the iframe.

### Step 5A: Test Saved Card Flow

If mock saved cards are applied, the iframe should show a saved card selector with pre-selected card.

1. Take a `browser_snapshot` and verify saved cards are visible in the iframe (look for card ending in `4242` or `8888`).
2. The first saved card should be auto-selected — no action needed in the iframe.
3. Fill user info section (see Step 5C below).
4. Verify submit button is enabled (see Step 6).

### Step 5B: Test New Card Flow

To test new card entry (when no saved cards exist, or after removing mock saved cards):

1. If saved cards are shown, click "CREDIT/DEBIT CARD" radio to switch to new card entry.
2. Fill CC fields inside the iframe (`ref` starting with `f1`):
   - Card holder name (textbox) — e.g., `Test User`
   - Credit/debit card number — use `4111111111111111`, type `slowly: true`
   - Expiry date (MM/YY) — use `1228`, type `slowly: true`
   - CVC/CVV — use `123`, type `slowly: true`
3. Fill user info section (see Step 5C below).
4. Verify submit button is enabled (see Step 6).

### Step 5C: Fill User Info Section (shared by both flows)

These fields are outside the iframe, on the main page:

- Email (textbox) — e.g., `test@agoda.com`
- Date of birth — click the field, a date picker opens. Navigate to a past month and select a date.
- Card issuing country (combobox) — use `browser_select_option` with a country like `Thailand`

### Step 6: Verify Submit Button

Take a `browser_snapshot` and check the Submit button state:
- `[disabled]` = form incomplete
- `[cursor=pointer]` = form valid, button enabled

## Validation Rules

The Submit button enables when ALL conditions are met:
1. `isCcFormReadyToSubmit` — SDK signals ready (auto for saved card, requires all CC fields for new card)
2. `paymentToken` — non-empty (SDK provides this)
3. `email` — non-empty and valid format
4. `dateOfBirth` — selected
5. `cardIssuingCountry` — selected and exists in supported countries list
6. If country requires address fields (street, city, state) — those must also be filled

## Key Files

| File | Purpose |
|------|---------|
| `src/ClientSide/src/cashbackapp/page/card/CashbackCardPage.tsx` | Card page, holds form state and submit logic |
| `src/ClientSide/src/cashbackapp/page/card/components/CcForm.tsx` | CC form wrapper, communicates with payment SDK iframe |
| `src/ClientSide/src/cashbackapp/page/card/utils/formValidationHelper.ts` | `isFormValid()` — controls submit button |
| `src/ClientSide/src/cashbackapp/page/card/components/UserInfoSection.tsx` | Email, DOB, country fields |
| `src/ClientSide/src/cashbackapp/page/summary/CashbackSummaryPage.tsx` | Summary page with "Request Cashback Reward" button |
| `src/ClientSide/src/cashbackapp/page/summary/components/cashbackSummaryInfoHelper.ts` | Controls request button enabled/disabled based on balance |

## Testing Overrides

When testing locally with zero balance, apply these overrides to unblock the flow. **Remember to revert before committing.**

### 1. Mock cashback balance on summary page

In `src/ClientSide/src/cashbackapp/page/summary/index.tsx`, after `pageParams` is loaded, override `availableBalance`:

```ts
const pageParams = getPageParams(Pages.CashbackWebViewSummary) as CashbackWebViewPageParams;

// TODO: Remove mock data — testing only
if (pageParams?.cashbackSummary) {
    const mockBalance = {
        balanceUSD: 50,
        balanceLocal: 1750,
        formattedUsdAmount: '50',
        formattedAmount: '1,750',
        formattedUsdAmountWithCurrency: 'US$50',
        formattedAmountWithCurrency: '฿1,750',
        localCurrency: 'THB',
    };
    pageParams.cashbackSummary.availableBalance = mockBalance;
}
```

This makes the "Request Cashback Reward" button enabled without needing real balance.

### 2. Always route to card page (skip option page)

In `src/ClientSide/src/cashbackapp/page/summary/CashbackSummaryPage.tsx`, inside `handleClaimOption`, replace the `switch (claimOption.preferredClaimOption)` block with:

```ts
await navigateToCardPageInternal(navigationParams);
```

### 3. Enable iframe bridge for payment SDK

In `src/ClientSide/src/cashbackapp/page/card/components/CcForm.tsx`, add `shouldUseIframeBridge: true` to `iframePaymentFormProps`:

```ts
const iframePaymentFormProps: IframePaymentFormProps = {
    setupPaymentDetails: availablePaymentMethods,
    onReceiveCreatePaymentDetails: handleReceiveCreatePaymentDetails,
    onIsReadyToSubmit: handleIsReadyToSubmit,
    onHandshakeSuccessful: () => setIsIframeLoaded(true),
    shouldUseIframeBridge: true,  // <-- add this
    ...
};
```

### 4. Mock saved cards

In `src/ClientSide/src/cashbackapp/page/card/CashbackCardPage.tsx`, replace the `savedCards` prop on `<CcForm>` with a hardcoded array:

```ts
savedCards={[
    {
        ccId: 1,
        lastFourDigits: '4242',
        cardTypeId: 1,
        icons: [{ type: 1, url: 'https://cdn6.agoda.net/images/mvc/default/ic_visa@2x_v3.png' }],
        isPaymentMethodSupported: true,
        expiryDate: { month: 12, year: 2027 },
        issuingBankCountryId: 1,
        ccToken: 'mock-token-001',
        ccName: 'Test User',
        isExpiryDateRequired: false,
        feeInfo: { feeType: '', isRecommended: false, paymentCharge: 0 },
        isExpired: false,
    },
    {
        ccId: 2,
        lastFourDigits: '8888',
        cardTypeId: 2,
        icons: [{ type: 1, url: 'https://cdn6.agoda.net/images/mvc/default/ic_mastercard@2x_v3.png' }],
        isPaymentMethodSupported: true,
        expiryDate: { month: 6, year: 2028 },
        issuingBankCountryId: 1,
        ccToken: 'mock-token-002',
        ccName: 'Test User',
        isExpiryDateRequired: false,
        feeInfo: { feeType: '', isRecommended: false, paymentCharge: 0 },
        isExpired: false,
    },
]}
```

Original reads from `payoutListData?.savedCards || []`.

## Tips

- The CC form lives in an **iframe**. Playwright refs inside the iframe start with `f1` prefix.
- The payment SDK fires `onIsReadyToSubmit` and `onReceiveCreatePaymentDetails` asynchronously — add short waits after filling CC fields.
- Test card number `4111111111111111` is a standard Visa test card.
- Always type card number, expiry, and CVC with `slowly: true` to trigger the SDK's key-by-key validation handlers.
