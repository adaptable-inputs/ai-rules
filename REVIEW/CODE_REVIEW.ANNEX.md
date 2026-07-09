---
applies_to:
  load: "annex"
  annex_of: "CODE_REVIEW.md"
  tasks: ["review", "test"]
---
# CODE_REVIEW - Annex

## High-Risk Pitfalls
1. Style-only feedback while missing correctness/security defects.
2. Vague findings without actionable remediation.
3. Missing boundary/dependency risk checks.
4. No distinction between critical risk and low-impact nits.
5. Ignoring test gaps for changed behavior.

## Do / Don't Examples
### 1. Finding Specificity
```text
Don't: "This looks wrong."
Do:    "High - `service/x.ts:87`: timeout is ignored; retries can hang request
        path under dependency outage. Add bounded timeout and failure mapping."
```

### 2. Priority Discipline
```text
Don't: spend review on naming nits while auth check is missing.
Do:    report missing auth as primary finding, then lower-priority nits.
```

### 3. Verification Transparency
```text
Don't: imply tests were run when they were not.
Do:    state which checks were run and what remains unverified.
```
