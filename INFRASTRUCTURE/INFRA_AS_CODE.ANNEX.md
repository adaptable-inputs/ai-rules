---
applies_to:
  load: "annex"
  annex_of: "INFRA_AS_CODE.md"
  tasks: ["review", "test"]
---
# INFRA_AS_CODE - Annex

## High-Risk Pitfalls
1. Applying changes without reviewing plan/preview output.
2. Shared state backend without locking or access boundaries.
3. Manual console changes causing unmanaged drift.
4. Static privileged credentials embedded in IaC config.
5. Cross-environment coupling that allows blast-radius expansion.
6. Destructive changes with no tested rollback path.
7. Weak tagging/ownership metadata blocking operations and cost governance.

## Do / Don't Examples
### 1. Plan/Apply Discipline
```text
Don't: apply infrastructure changes directly from a local machine with no
       reviewed plan output.
Do:    generate plan/preview, review it, and apply through gated workflow.
```

### 2. Drift Handling
```text
Don't: keep manual console edits as undocumented permanent state.
Do:    codify approved changes in IaC and converge environments.
```

### 3. Secret Safety
```text
Don't: store cloud access keys in plain IaC variable files.
Do:    use secret managers and short-lived identity federation.
```

## Code Review Checklist for IaC
- Is plan/preview evidence provided and reviewed?
- Are destructive operations expected, justified, and gated?
- Is state backend protection/locking configured correctly?
- Are identity permissions least-privilege for provisioning and runtime?
- Are environment boundaries explicit and safe?
- Are rollback and failure-handling paths documented?
- Are tags/metadata sufficient for ownership/audit/cost control?

## Testing Guidance
- Validate IaC syntax and policy checks in CI.
- Validate plan/preview output for expected resource diff.
- Test apply in non-production before production rollout.
- Test rollback/recovery path for high-impact changes.
- Test drift detection and reconciliation for critical stacks.
