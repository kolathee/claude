# trips-web: Run Tests from Correct Directory

## Pattern: Jest tests must run from `src/Clientside/`

In the `trips-web` monorepo, the jest config lives at `apps/trip-view-bff/src/Clientside/jest.config.js`.

Running tests from the wrong directory (e.g., `apps/trip-view-bff/`) causes parse errors because Babel/TypeScript transforms aren't configured at that level.

### Correct
```bash
cd /Users/kpayuhawatta/Gits/trips-web/apps/trip-view-bff/src/Clientside
npx jest --testPathPattern="YourTest" --no-coverage
```

### Wrong (will fail with SyntaxError)
```bash
cd /Users/kpayuhawatta/Gits/trips-web/apps/trip-view-bff
npx jest --testPathPattern="YourTest" --no-coverage
```

### Backend tests
```bash
cd /Users/kpayuhawatta/Gits/trips-web/apps/trip-view-bff/src/Serverside
dotnet test Agoda.Cronos.MmbUnitTests/Agoda.Cronos.MmbUnitTests.csproj --filter "FullyQualifiedName~TestName"
```
