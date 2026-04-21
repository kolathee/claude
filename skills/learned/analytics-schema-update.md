# Analytics Schema Update (messaging-client-messages)

## Pattern: Adding new analytics values for trip-view-bff

When a new `action_element_value` is needed for analytics in `trips-web`:

1. The TypeScript types are **generated** from C# enums in `full-stack/fe-data/messaging-client-messages`
2. Find the relevant enum by checking `package.json` → `repository` field in the analytics package under `node_modules/@agoda/analytics-messages-definition-trip-view-bff/`
3. The source enum for trip footer actions is `TripFooterActionFunnel` in `src/MessagingClient.Messages/Enums/TripActionFunnel.cs`
4. Enum values are auto-converted to kebab-case in the generated TypeScript (e.g., `PayNow` → `'pay-now'`)
5. After merging the schema MR, bump the package version in `trips-web` and remove any `as` type assertions

## Example MR
- Reference: https://gitlab.agodadev.io/full-stack/fe-data/messaging-client-messages/-/merge_requests/7066
- Maintainers: FE Data Team — fe-data@agoda.com / Slack #C40LW4S4Q
