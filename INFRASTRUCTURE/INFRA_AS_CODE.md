---
applies_to:
  load: "conditional"
  when: "the project declares any infrastructure as code"
  annex: "INFRA_AS_CODE.ANNEX.md"
  purpose: "tool-neutral IaC guardrails for provisioning and evolving infrastructure safely"
  inherits: ["INFRASTRUCTURE/INFRASTRUCTURE.md", "SECURITY/SECURITY.md", "COMPLIANCE/COMPLIANCE.md", "TEST/TEST.md", "CI-CD/CI-CD.md", "CORE/VERSION_CONTROL_SYSTEM.md"]
---
# INFRA_AS_CODE

Guidance for AI agents implementing and reviewing Infrastructure as Code (IaC) changes.

## IaC Defaults
- SHOULD keep infrastructure declarative, versioned, and reproducible.
- SHOULD treat IaC as the source of truth; avoid manual console drift.
- SHOULD keep changes small, reviewable, and environment-scoped.
- SHOULD prefer immutable replacements over ad-hoc in-place mutation for high-risk components where feasible.

## Change Management and Approval Gates
- MUST require plan/preview output before apply for every non-trivial change.
- SHOULD separate plan generation from apply execution in CI/CD where possible.
- MUST gate production apply with explicit approval controls.
- MUST block apply when plan/preview shows unexpected destructive impact.

## State, Drift, and Convergence
- SHOULD keep state backends protected, access-controlled, and auditable.
- MUST use locking/concurrency controls to avoid concurrent apply corruption.
- SHOULD run periodic drift detection and reconcile intentionally.
- MUST NOT normalize unmanaged/manual changes as acceptable steady state.

## Secrets, Identity, and Access
- MUST NOT commit secrets or static privileged keys in IaC code or variables.
- SHOULD prefer short-lived credentials (for example OIDC/workload identity) over long-lived static credentials.
- MUST enforce least privilege for provisioning identities and runtime roles.
- MUST keep sensitive outputs minimized and redacted in logs/artifacts.

## Environment and Isolation Rules
- SHOULD keep dev/test/stage/prod separation explicit in code and state.
- MUST prevent cross-environment resource references unless explicitly required and reviewed.
- SHOULD keep naming/tagging/ownership metadata mandatory for auditability and cost control.

## Reliability and Rollback
- MUST define rollback strategy before risky changes (revert, redeploy, or replacement path).
- SHOULD validate dependency ordering for create/update/delete operations.
- SHOULD prefer staged rollout for broad-impact infrastructure changes.
- MUST keep disaster-recovery-sensitive resources protected from accidental destruction.
