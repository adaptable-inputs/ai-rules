---
applies_to:
  load: "annex"
  annex_of: "TERRAFORM.md"
  tasks: ["review", "test"]
---
# TERRAFORM - Annex

## High-Risk Pitfalls
1. Unpinned providers causing unreviewed behavior changes.
2. Local state or unlocked shared state causing corruption.
3. Blind apply without reviewed plan output.
4. Secrets committed in tfvars or exposed via outputs/logs.
5. Overloaded root modules with poor ownership boundaries.
6. Manual console edits causing persistent drift.
7. Force replacement without rollback planning.

## Do / Don't Examples
### 1. Provider Versioning
```text
Don't: leave provider versions floating across environments.
Do:    pin provider versions and review upgrades explicitly.
```

### 2. State Safety
```text
Don't: keep production state in local files.
Do:    use remote backend with locking and audited access.
```

### 3. Plan Discipline
```text
Don't: run apply directly after edit with no plan review.
Do:    review plan diff and apply through gated workflow.
```

## Code Review Checklist for Terraform
- Are Terraform and every provider pinned to an exact version?
- Is remote state backend and locking configured safely?
- Does the plan show expected change scope and no unexplained destruction?
- Are module boundaries/ownership clear and maintainable?
- Are secrets excluded from config, outputs, and logs?
- Are migration/import/replacement steps explicit and low-risk?

## Testing Guidance
- Run `terraform fmt -check` and `terraform validate`.
- Run plan in CI and publish plan summary for review.
- Test module behavior in isolated non-production environments.
- Test drift detection and reconciliation for critical stacks.
- Test rollback/recovery path for destructive or broad-impact changes.
