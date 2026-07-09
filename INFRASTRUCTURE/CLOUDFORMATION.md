---
applies_to:
  load: "conditional"
  when: "a CloudFormation template is present"
  tools: ["cloudformation"]
---
# CLOUDFORMATION

Guidance for AI agents implementing and reviewing AWS CloudFormation
infrastructure changes.

## Scope
- Define CloudFormation-specific rules for safe and reproducible AWS
  infrastructure delivery.
- Apply this file to CloudFormation templates, stacks, change sets, and related
  deployment workflows.

## Semantic Dependencies
- Inherit IaC baseline from `INFRASTRUCTURE/INFRA_AS_CODE.md`.
- Inherit security and compliance constraints from `SECURITY/SECURITY.md` and
  `COMPLIANCE/COMPLIANCE.md`.
- Inherit CI and workflow constraints from `CI-CD/CI-CD.md` and
  `CORE/VERSION_CONTROL_SYSTEM.md`.

## Defaults
- SHOULD keep templates declarative, parameterized, and environment-aware.
- SHOULD keep stack boundaries cohesive and ownership explicit.
- SHOULD prefer nested stacks/modules for reuse over copy-pasted large templates.
- SHOULD keep change sets as the default review path before stack updates.
- SHOULD keep stack policies/termination protection enabled for critical stacks.

## Change Set and Update Rules
- SHOULD create and review change sets before executing updates.
- MUST block execution when change sets show unexpected replacement/deletion impact.
- SHOULD keep production updates gated with explicit approvals.
- MUST keep rollback behavior enabled unless a bounded exception is documented.

## Stack Governance
- SHOULD keep stack naming conventions stable across environments.
- SHOULD separate environments/accounts to reduce blast radius.
- SHOULD keep resource tags/metadata mandatory for ownership and cost governance.
- SHOULD avoid unmanaged/manual changes outside stack control.

## Drift, Import, and Migration
- SHOULD run drift detection for critical stacks regularly.
- SHOULD use resource import and stack refactor workflows deliberately and documented.
- SHOULD validate replacement impact before updates on stateful resources.
- SHOULD keep migration and rollback steps explicit for high-impact changes.

## Secrets and Access
- MUST NOT hardcode secrets in templates or parameter defaults.
- MUST retrieve secrets through secure references/services.
- MUST keep IAM permissions least-privilege for deploy roles.
- SHOULD keep stack outputs free of sensitive data where possible.

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

## Override Notes
- Project-specific CloudFormation patterns MAY narrow implementation details,
  but change-set review discipline, stack protection, least privilege, and
  secret hygiene remain mandatory.
