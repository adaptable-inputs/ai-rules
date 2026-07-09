---
applies_to:
  load: "annex"
  annex_of: "CLOUDFORMATION.md"
  tasks: ["review", "test"]
---
# CLOUDFORMATION - Annex

## High-Risk Pitfalls
1. Updating stacks without reviewed change sets.
2. Ignoring replacement impact on stateful resources.
3. Missing termination protection on critical stacks.
4. Template-embedded secrets or sensitive outputs.
5. Manual console edits creating unmanaged drift.
6. Broad deploy-role permissions with weak guardrails.
7. Oversized templates with unclear ownership boundaries.

## Do / Don't Examples
### 1. Change-Set Discipline
```text
Don't: deploy stack updates directly with no change-set review.
Do:    review change set and execute only expected changes.
```

### 2. Stack Protection
```text
Don't: allow critical stacks to be deleted accidentally.
Do:    enable termination protection and restrictive stack policies.
```

### 3. Secret Handling
```text
Don't: store secret values directly in template parameters/defaults.
Do:    reference secrets from managed secret services.
```

## Code Review Checklist for CloudFormation
- Is change-set evidence provided and reviewed?
- Are destructive/replacement actions expected and justified?
- Are stack policies/termination protection configured correctly?
- Are environment/account boundaries explicit and safe?
- Are secrets absent from templates/outputs and deploy logs?
- Are drift, migration, and rollback paths explicit?

## Testing Guidance
- Validate templates syntactically and semantically before deployment.
- Generate and review change sets in CI/staging prior to production execution.
- Test stack updates and rollback behavior in non-production.
- Test drift detection and reconciliation for critical stacks.
- Test migration/import paths for complex stack evolution.
