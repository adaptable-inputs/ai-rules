---
applies_to:
  load: "annex"
  annex_of: "GITLAB.md"
  tasks: ["review", "test"]
---
# GITLAB - Annex

## High-Risk Pitfalls
1. Optional quality gates on protected branches.
2. Non-deterministic build/install in CI.
3. Secret leakage through logs or committed CI config.
4. Release tags bypassing full validation pipeline.
5. Fragile cache keys causing stale/corrupt build state.
6. Overly broad job rules running deploy jobs unexpectedly.

## Do / Don't Examples
### 1. Deterministic Install
```text
Don't: floating dependency install in release jobs.
Do:    use lockfile-frozen install mode.
```

### 2. Secret Handling
```text
Don't: echo $DEPLOY_TOKEN in script output.
Do:    keep token masked and pass only to required command flags/env.
```

### 3. Release Safety
```text
Don't: release job runs without tests/security stage dependencies.
Do:    enforce full gate chain before publish/deploy.
```

## Code Review Checklist for GitLab CI
- Are stages/gates explicit and complete?
- Are merge/release quality gates enforced?
- Are branch/tag rules and protected-job constraints correct?
- Are secrets managed via masked/protected variables?
- Are cache/artifact strategies deterministic and safe?
- Is release reproducibility from tag alone guaranteed?

## Testing Guidance
- Lint CI configuration in CI itself.
- Run pipeline dry-runs/validation on MR changes.
- Test release pipeline on pre-release tags in staging.
- Test failure scenarios (missing secrets, failing tests, vulnerability gates).
- Track and reduce flaky job/test incidence.
