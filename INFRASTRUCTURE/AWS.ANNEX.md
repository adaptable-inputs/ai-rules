---
applies_to:
  load: "annex"
  annex_of: "AWS.md"
  tasks: ["review", "test"]
---
# AWS - Annex

## High-Risk Pitfalls
1. Single-account designs with no blast-radius isolation.
2. Broad IAM permissions and unused long-lived access keys.
3. Publicly exposed resources by default with weak ingress controls.
4. Missing audit logs or mutable log destinations.
5. Unencrypted data stores or unmanaged key usage.
6. No tested backup/restore path for critical data/services.
7. Missing tagging/ownership causing operational blind spots.

## Do / Don't Examples
### 1. Identity
```text
Don't: rely on static admin access keys for automation.
Do:    use assumed roles and short-lived credentials.
```

### 2. Network Exposure
```text
Don't: open broad inbound CIDR ranges by default.
Do:    scope security-group rules to explicit trusted sources.
```

### 3. Auditability
```text
Don't: run critical environments without centralized audit logging.
Do:    enable immutable audit trails with monitored alerting.
```

## Code Review Checklist for AWS
- Are account/environment isolation boundaries explicit and safe?
- Are IAM permissions least-privilege with no unjustified wildcards?
- Are network controls least-open and intentional?
- Are encryption/key-management requirements satisfied?
- Are logging/audit/detection controls enabled and tamper-resistant?
- Are backup/restore and resilience assumptions explicit and testable?
- Are required ownership/cost tags present?

## Testing Guidance
- Validate IAM policies/role trust with least-privilege tests.
- Validate network exposure with automated policy/security checks.
- Validate audit/logging pipelines and alert routes.
- Validate backup/restore drills for critical services.
- Validate staged rollout and rollback procedures for high-impact changes.
