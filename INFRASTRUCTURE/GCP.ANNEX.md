---
applies_to:
  load: "annex"
  annex_of: "GCP.md"
  tasks: ["review", "test"]
---
# GCP - Annex

## High-Risk Pitfalls
1. Weak project/folder isolation increasing blast radius.
2. Broad IAM grants and unmanaged service-account keys.
3. Overly permissive firewall/network defaults.
4. Missing audit logs or weak retention controls.
5. Unencrypted data paths or unmanaged key usage.
6. No tested backup/restore path for critical services.
7. Missing labels/ownership reducing governance and response quality.

## Do / Don't Examples
### 1. Identity
```text
Don't: rely on long-lived service-account keys for normal automation.
Do:    use workload identity federation and least-privilege IAM.
```

### 2. Network Exposure
```text
Don't: allow broad internet ingress by default.
Do:    scope firewall rules to explicit trusted sources and ports.
```

### 3. Auditability
```text
Don't: operate production projects without strong audit logging.
Do:    enable and retain audit logs with monitored alerting.
```

## Code Review Checklist for GCP
- Are org/folder/project boundaries explicit and safe?
- Are IAM assignments least-privilege and scoped correctly?
- Are service-account key controls restrictive and auditable?
- Are network controls least-open and intentional?
- Are encryption/key/secret controls configured correctly?
- Are logging/audit/detection controls enabled and useful?
- Are backup/restore and resilience assumptions explicit and testable?
- Are required ownership/cost labels present?

## Testing Guidance
- Validate IAM boundaries with least-privilege checks.
- Validate service-account key restrictions and monitoring controls.
- Validate network exposure and policy compliance with automated checks.
- Validate logging/audit collection and alert routes.
- Validate backup/restore drills for critical services.
- Validate rollout/rollback behavior for high-impact changes.
