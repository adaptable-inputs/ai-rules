---
applies_to:
  load: "annex"
  annex_of: "PLAYWRIGHT.md"
  tasks: ["review", "test"]
---
# PLAYWRIGHT - Annex

## High-Risk Pitfalls
1. Brittle selectors coupled to markup churn.
2. Arbitrary sleeps causing flaky and slow tests.
3. Shared state leakage between tests.
4. Overbroad E2E coverage duplicating lower-level tests.
5. Ignoring artifact capture, slowing triage.
6. Uncontrolled retries hiding real instability.

## Do / Don't Examples
### 1. Locator Strategy
```text
Don't: page.locator("div:nth-child(4) > span").click()
Do:    page.getByRole("button", { name: "Submit" }).click()
```

### 2. Waiting
```text
Don't: await page.waitForTimeout(5000)
Do:    await expect(page.getByText("Saved")).toBeVisible()
```

### 3. Test Isolation
```text
Don't: rely on leftover account/session from previous test.
Do:    create/seed needed state per test fixture.
```

## Code Review Checklist for Playwright
- Are scenarios focused on critical journeys?
- Are locators stable and accessibility-aligned?
- Are waits assertion/event-based (no arbitrary sleeps)?
- Is test state isolated and parallel-safe?
- Are failure artifacts and diagnostics configured?
- Is retry usage justified and bounded?

## Testing Guidance
- Run tests in CI with representative browser matrix as required.
- Track flaky tests and failure categories.
- Add visual/interaction regression coverage only where high value.
- Keep test runtime budget monitored and optimized.
