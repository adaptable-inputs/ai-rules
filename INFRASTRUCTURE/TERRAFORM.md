---
applies_to:
  load: "conditional"
  when: "*.tf files are present"
  tools: ["terraform"]
  globs: ["**/*.tf"]
  annex: "TERRAFORM.ANNEX.md"
  purpose: "Terraform-specific rules for predictable and safe infrastructure delivery"
  inherits: ["INFRASTRUCTURE/INFRA_AS_CODE.md", "SECURITY/SECURITY.md", "COMPLIANCE/COMPLIANCE.md", "CI-CD/CI-CD.md", "CORE/VERSION_CONTROL_SYSTEM.md"]
---
# TERRAFORM

Guidance for AI agents implementing and reviewing Terraform infrastructure
changes.

## Defaults
- MUST pin Terraform version and provider versions with explicit constraints.
- SHOULD use remote state backends with locking enabled.
- SHOULD keep module boundaries clear and reusable; avoid monolithic root configs.
- SHOULD keep variable and output contracts explicit and documented.
- SHOULD prefer declarative data sources over imperative external scripts.

## Planning and Apply Rules
- SHOULD run `terraform fmt` and `terraform validate` before plan/apply.
- SHOULD generate and review plan output for every non-trivial change.
- SHOULD use non-interactive, reviewed apply workflows in CI for shared environments.
- MUST block apply when plan includes unexpected destructive operations.

## State and Workspace Governance
- SHOULD store state in secured remote backend, never in VCS.
- Scope state per environment/workload to reduce blast radius.
- MUST use locks to prevent concurrent apply corruption.
- SHOULD use workspaces intentionally; avoid hidden multi-environment coupling.
- MUST keep state access audited and least-privilege.

## Module and Dependency Discipline
- SHOULD keep modules cohesive with clear inputs/outputs.
- SHOULD avoid circular module dependencies and hidden provider coupling.
- SHOULD keep provider aliases explicit when multi-account/multi-region applies.
- SHOULD prefer explicit `depends_on` only when implicit graph is insufficient.

## Secrets and Sensitive Data
- MUST NOT commit secrets in `.tf`, `.tfvars`, or generated plan artifacts.
- MUST mark sensitive outputs as `sensitive = true`.
- Source secrets from secure stores and runtime injection paths.
- MUST keep CI logs redacted for sensitive values.

## Drift, Import, and Migration
- SHOULD run periodic drift checks (`terraform plan`) for critical environments.
- SHOULD use `import` and `moved` blocks deliberately during migration/refactors.
- SHOULD keep migration steps documented for state/schema changes.
- SHOULD validate replacement impact before forcing resource recreation.

## Override Notes
- Project-specific Terraform patterns MAY narrow implementation details, but
  version pinning, plan-review discipline, state safety, and secret hygiene
  remain mandatory.
