---
applies_to:
  load: "annex"
  annex_of: "GITHUB_ACTIONS.md"
  tasks: ["review", "test"]
---
# GITHUB_ACTIONS - Annex

## High-Risk Pitfalls
1. Floating action versions introducing unreviewed behavior changes.
2. Broad `GITHUB_TOKEN` permissions across all jobs by default.
3. Optional quality gates on protected branches.
4. Secret leakage through logs or committed workflow config.
5. Release workflows bypassing full validation gates.
6. Fragile cache keys causing stale/corrupt build state.
7. Overly broad trigger rules running deploy jobs unexpectedly.

## Do / Don't Examples
### 1. Action Pinning
```text
Don't: uses: actions/checkout@v4
Do:    uses: actions/checkout@<full-commit-sha>
```

### 2. Token Permissions
```text
Don't: permissions: write-all
Do:    set minimal read/write scopes per workflow/job need.
```

### 3. Release Safety
```text
Don't: publish release artifacts without test/security dependencies.
Do:    enforce full gate chain before publish/deploy.
```

## Code Review Checklist for GitHub Actions
- Are workflow triggers explicit and least-surprise?
- Are stages/gates explicit and complete?
- Are merge/release quality gates enforced?
- Are action versions pinned by full SHA?
- Are token permissions and secret handling least-privilege and safe?
- Are cache/artifact strategies deterministic and safe?
- Is release reproducibility from tag alone guaranteed?

## Testing Guidance
- Validate workflow YAML syntax and execution logic before merge.
- Run workflow changes on PR branches and verify required gates.
- Test release workflow on pre-release tags in staging when possible.
- Test failure scenarios (missing secrets, failing tests, vulnerability gates).
- Verify deploy jobs honor environment protections/required approvals.
