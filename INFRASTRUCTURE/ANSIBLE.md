---
applies_to:
  load: "conditional"
  when: "an Ansible playbook is present"
  tools: ["ansible"]
  annex: "ANSIBLE.ANNEX.md"
  purpose: "Ansible-specific rules for safe, repeatable infrastructure and configuration automation"
  inherits: ["INFRASTRUCTURE/INFRA_AS_CODE.md", "SECURITY/SECURITY.md", "COMPLIANCE/COMPLIANCE.md", "CI-CD/CI-CD.md", "CORE/VERSION_CONTROL_SYSTEM.md"]
---
# ANSIBLE

Guidance for AI agents implementing and reviewing Ansible automation changes.

## Defaults
- MUST keep playbooks idempotent and deterministic.
- SHOULD keep role boundaries cohesive and reusable.
- SHOULD keep inventory and variable scopes explicit per environment.
- SHOULD prefer module-based tasks over shell/command calls where possible.
- MUST keep privilege escalation explicit, minimal, and auditable.

## Execution and Change Rules
- SHOULD run syntax checks/lint before execution in shared branches.
- SHOULD use check mode/dry-run for preview where supported.
- SHOULD keep high-impact plays gated with explicit approval in CI workflows.
- SHOULD keep rollback/remediation steps documented for risky changes.

## Inventory and Variable Governance
- SHOULD keep inventory ownership and environment boundaries explicit.
- SHOULD avoid global variable sprawl; keep variable precedence predictable.
- MUST NOT embed secrets in plaintext variable files.
- MUST use vault/secret-manager integrations for sensitive values.

## Role and Task Discipline
- SHOULD keep tasks small and focused; avoid monolithic playbooks.
- SHOULD keep handlers explicit for service restart/reload side effects.
- SHOULD avoid hidden cross-host coupling and ordering assumptions.
- SHOULD use tags intentionally for scoped execution paths.

## Security and Access
- MUST keep SSH/API credentials out of repository content.
- MUST enforce least privilege for automation accounts.
- SHOULD avoid broad `become: true` defaults across all tasks.
- MUST keep logs free of sensitive values (`no_log` where needed).

## Override Notes
- Project-specific Ansible patterns MAY narrow implementation details, but
  idempotency, secret hygiene, least privilege, and environment isolation
  remain mandatory.
