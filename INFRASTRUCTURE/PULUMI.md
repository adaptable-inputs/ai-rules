---
applies_to:
  load: "conditional"
  when: "Pulumi.yaml is present"
  tools: ["pulumi"]
  annex: "PULUMI.ANNEX.md"
  purpose: "Pulumi-specific rules for predictable and safe infrastructure provisioning"
  inherits: ["INFRASTRUCTURE/INFRA_AS_CODE.md", "SECURITY/SECURITY.md", "COMPLIANCE/COMPLIANCE.md", "CI-CD/CI-CD.md", "CORE/VERSION_CONTROL_SYSTEM.md"]
---
# PULUMI

Guidance for AI agents implementing and reviewing Pulumi infrastructure changes.

## Defaults
- MUST pin Pulumi CLI and provider/plugin versions for reproducibility.
- SHOULD keep stacks environment-scoped with explicit ownership boundaries.
- SHOULD keep stack config explicit and minimize implicit defaults for critical values.
- SHOULD keep infrastructure logic deterministic and free of hidden side effects.
- SHOULD keep project code modular; separate reusable components from stack entrypoints.

## Preview and Update Rules
- SHOULD run `pulumi preview` and review the diff before `pulumi up`.
- SHOULD apply changes through gated CI/CD workflows for shared environments.
- MUST block updates when preview includes unexpected replacements/deletions.
- SHOULD keep non-interactive execution for automated environments.

## Policy as Code and Organizational Guardrails
- MUST enforce Pulumi policy checks (for example, Policy Packs/CrossGuard) in shared environments.
- MUST run required policy checks as part of preview/update gates in CI.
- MUST block updates when required policies fail unless an explicit, approved, time-bounded exception exists.
- SHOULD keep policy versions and exception approvals auditable.

## Stack and State Governance
- SHOULD use secure backend/state storage and controlled access.
- SHOULD keep stack isolation strict across dev/test/stage/prod.
- SHOULD avoid sharing one stack across unrelated systems/teams.
- MUST keep state access audited and least-privilege.

## Config and Secret Handling
- MUST use Pulumi secret config for sensitive values.
- MUST NOT commit plaintext secrets in stack config files.
- SHOULD prefer short-lived workload identity over static cloud credentials.
- MUST keep sensitive outputs minimized and redacted in logs.

## Component and Dependency Discipline
- SHOULD keep component abstractions cohesive and narrowly scoped.
- SHOULD avoid hidden provider selection; pass provider context explicitly.
- SHOULD keep cross-stack references explicit, versioned, and bounded.
- SHOULD prevent cyclic dependencies across stacks/components.

## Drift and Migration
- SHOULD run periodic previews for drift detection on critical stacks.
- SHOULD keep import/refactor operations explicit and documented.
- SHOULD validate replacement impact before updates that can recreate resources.
- SHOULD keep rollback/recovery steps documented for high-impact changes.

## Override Notes
- Project-specific Pulumi patterns MAY narrow implementation details, but
  version pinning, preview-review discipline, state safety, and secret hygiene
  remain mandatory.
