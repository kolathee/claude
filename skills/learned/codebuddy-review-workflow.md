# CodeBuddy Review Thread Workflow

## Pattern: Systematic review of automated code suggestions

When the user asks to check unresolved threads on a GitLab MR:

1. **Fetch discussions** via GitLab API, filter for `resolvable && !resolved`
2. **Assess each thread** — categorize as:
   - **Fix now**: Clear improvement, safe to apply (e.g., `async void` → `async Task`, missing null guards)
   - **Fix separately**: Requires external dependency change (e.g., analytics schema update)
   - **Dismiss**: Stylistic or low-value suggestion
3. **Apply fixes locally**, run tests from correct directory, then commit and push
4. **Reply and resolve** threads via GitLab API with either the fix commit or an explanation

## Common CodeBuddy suggestions worth fixing
- `async void` → `async Task` in xUnit tests
- Missing null/empty guards that cause broken UI labels
- Feature flag gating on data passed to functions
- Unused imports after removing type assertions

## Typical xUnit async test fix
```csharp
// Bad: xUnit won't observe failures
public async void MyTest() { ... }

// Good: proper async test
public async Task MyTest() { ... }
```
