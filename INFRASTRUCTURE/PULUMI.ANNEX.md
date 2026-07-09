---
applies_to:
  load: "annex"
  annex_of: "PULUMI.md"
  tasks: ["review", "test"]
---
# PULUMI - Annex

## High-Risk Pitfalls
1. Unpinned provider/plugin versions causing non-deterministic updates.
2. Plaintext secrets committed in stack config.
3. Running `pulumi up` without reviewed preview output.
4. Overloaded stacks with excessive blast radius.
5. Implicit provider context causing cross-account/region mistakes.
6. Hidden side effects in infrastructure program code.
7. Risky replacements with no rollback plan.

## Do / Don't Examples
### 1. Preview Discipline
```text
Don't: run `pulumi up` directly in production with no preview review.
Do:    review preview diff and execute updates through gated workflow.
```

### 2. Secret Safety
```text
Don't: commit plain API keys in stack YAML config.
Do:    store sensitive values as Pulumi secrets and secure backend entries.
```

### 3. Stack Isolation
```text
Don't: mix unrelated production systems in one stack.
Do:    keep stacks narrowly scoped by environment and ownership.
```

## Code Review Checklist for Pulumi
- Are Pulumi and every provider/plugin pinned to an exact version?
- Is stack scope/environment isolation explicit and safe?
- Is preview evidence provided with expected change scope?
- Are secret config values protected and absent from logs?
- Are provider contexts explicit to avoid cross-environment mistakes?
- Are replacement/migration/rollback steps explicit and low-risk?

## Testing Guidance
- Validate Pulumi program compilation/linting and preview generation in CI.
- Validate preview diffs for expected change set and no unexplained destruction.
- Test updates in non-production before production rollout.
- Test drift detection workflows for critical stacks.
- Test rollback/recovery procedures for broad-impact updates.
