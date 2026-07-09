---
applies_to:
  load: "annex"
  annex_of: "AZURE.md"
  tasks: ["review", "test"]
---
# AZURE - Annex

## High-Risk Pitfalls
1. Weak subscription/environment isolation increasing blast radius.
2. Broad RBAC assignments and unmanaged service principals.
3. Overly open NSG/network exposure by default.
4. Missing audit/diagnostic logging or weak retention controls.
5. Unencrypted data paths or unmanaged key/secret processes.
6. No tested backup/restore path for critical services.
7. Missing tags/ownership reducing governance and incident response quality.

## Do / Don't Examples
### 1. Identity
```text
Don't: store long-lived client secrets for routine automation.
Do:    use managed identities and least-privilege RBAC scopes.
```

### 2. Network Exposure
```text
Don't: allow wide-open internet ingress on sensitive services.
Do:    scope NSG rules to explicit trusted sources and ports.
```

### 3. Auditability
```text
Don't: operate production subscriptions without centralized diagnostics.
Do:    enforce activity and resource diagnostics with monitored alerting.
```

## Code Review Checklist for Azure
- Are subscription/resource-group boundaries explicit and safe?
- Are RBAC assignments least-privilege and scoped correctly?
- Are network controls least-open and intentional?
- Are encryption/key/secret controls configured correctly?
- Are logging/audit/detection controls enabled and useful?
- Are backup/restore and resilience assumptions explicit and testable?
- Are required ownership/cost tags present?

## Testing Guidance
- Validate RBAC and identity boundaries with least-privilege checks.
- Validate network exposure and policy compliance with automated controls.
- Validate logging/diagnostic collection and alert routes.
- Validate backup/restore drills for critical services.
- Validate rollout/rollback behavior for high-impact changes.
