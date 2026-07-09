---
applies_to:
  load: "conditional"
  when: "Pulumi.yaml is present"
  tools: ["pulumi"]
---
# PULUMI

Guidance for AI agents implementing and reviewing Pulumi infrastructure changes.

## Scope
- Define Pulumi-specific rules for predictable and safe infrastructure
  provisioning.
- Apply this file to Pulumi programs, stack configuration, and Pulumi-driven
  CI workflows.

## Semantic Dependencies
- Inherit IaC baseline from `INFRASTRUCTURE/INFRA_AS_CODE.md`.
- Inherit security and compliance constraints from `SECURITY/SECURITY.md` and
  `COMPLIANCE/COMPLIANCE.md`.
- Inherit CI and workflow constraints from `CI-CD/CI-CD.md` and
  `CORE/VERSION_CONTROL_SYSTEM.md`.

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

## Override Notes
- Project-specific Pulumi patterns MAY narrow implementation details, but
  version pinning, preview-review discipline, state safety, and secret hygiene
  remain mandatory.
