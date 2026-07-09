---
applies_to:
  load: "annex"
  annex_of: "ANSIBLE.md"
  tasks: ["review", "test"]
---
# ANSIBLE - Annex

## High-Risk Pitfalls
1. Non-idempotent shell scripts masquerading as configuration management.
2. Plaintext secrets in inventory/group vars.
3. Unbounded privilege escalation across playbooks.
4. Environment inventory mixing that expands blast radius.
5. Task ordering assumptions that break under parallelism/partial runs.
6. Missing dry-run/validation before production execution.
7. Overly broad tags causing unintended production changes.

## Do / Don't Examples
### 1. Idempotency
```text
Don't: rely on ad-hoc shell commands for core state management.
Do:    use idempotent Ansible modules with explicit desired state.
```

### 2. Secret Handling
```text
Don't: commit plaintext credentials in group_vars.
Do:    store secrets in Ansible Vault or external secret manager.
```

### 3. Privilege Scope
```text
Don't: set broad privilege escalation globally by default.
Do:    scope privilege escalation only to tasks that require it.
```

## Code Review Checklist for Ansible
- Are playbooks and roles idempotent and deterministic?
- Are inventory and variable scopes environment-safe and maintainable?
- Are secrets excluded from plaintext files and logs?
- Is privilege escalation minimal and justified?
- Are dry-run/check-mode and validation steps present?
- Are rollback/remediation paths documented for risky changes?

## Testing Guidance
- Run `ansible-lint` and syntax checks in CI.
- Run check mode/dry-run in non-production for high-impact changes.
- Test role/playbook behavior with representative inventory fixtures.
- Test secret handling and redaction behavior in logs.
- Test rollback/remediation procedures for critical automation paths.
