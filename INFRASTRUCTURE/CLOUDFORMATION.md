---
applies_to:
  load: "conditional"
  when: "a CloudFormation template is present"
  tools: ["cloudformation"]
  annex: "CLOUDFORMATION.ANNEX.md"
  purpose: "CloudFormation-specific rules for safe and reproducible AWS infrastructure delivery"
  inherits: ["INFRASTRUCTURE/INFRA_AS_CODE.md", "SECURITY/SECURITY.md", "COMPLIANCE/COMPLIANCE.md", "CI-CD/CI-CD.md", "CORE/VERSION_CONTROL_SYSTEM.md"]
---
# CLOUDFORMATION

Guidance for AI agents implementing and reviewing AWS CloudFormation infrastructure changes.

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
