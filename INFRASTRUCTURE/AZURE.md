---
applies_to:
  load: "conditional"
  when: "the project deploys to Azure"
  tools: ["azure"]
---
# AZURE

Guidance for AI agents implementing and reviewing Azure platform configuration
and operations choices.

## Scope
- Define Azure-specific platform guardrails for secure and reliable operations.
- Apply this file when architecture or infrastructure changes materially affect
  Azure tenant, subscription, network, identity, data, or observability
  posture.

## Semantic Dependencies
- Inherit infrastructure baseline from `INFRASTRUCTURE/INFRASTRUCTURE.md`.
- Inherit IaC/process constraints from `INFRASTRUCTURE/INFRA_AS_CODE.md`.
- Inherit security/compliance constraints from `SECURITY/SECURITY.md` and
  `COMPLIANCE/COMPLIANCE.md`.
- Inherit CI/CD and workflow constraints from `CI-CD/CI-CD.md` and
  `CORE/VERSION_CONTROL_SYSTEM.md`.

## Defaults
- SHOULD use subscription/resource-group isolation for environments and ownership.
- MUST apply least privilege RBAC by default for identities and automation.
- SHOULD keep network access private by default; expose public endpoints intentionally.
- MUST enable encryption at rest/in transit for sensitive data paths.
- SHOULD keep tagging standards mandatory for ownership, environment, and cost center.

## Identity and Access Guardrails
- SHOULD prefer managed identities and short-lived auth flows over static secrets.
- MUST keep privileged role assignments minimal, time-bound, and auditable.
- MUST restrict cross-subscription access with explicit scopes and conditions.
- MUST treat broad built-in role assignments as exceptions requiring justification.

## Network and Data Protection
- MUST keep virtual network and NSG intent explicit and least-open.
- SHOULD avoid unrestricted inbound/outbound rules unless explicitly justified.
- MUST keep critical data services private and fronted by controlled access paths.
- MUST enforce key-management and secret-store controls where required.

## Logging, Audit, and Detection
- SHOULD keep platform activity/audit logs enabled and retained per policy.
- SHOULD centralize diagnostic logs and metrics for actionable analysis.
- SHOULD enable detection controls for threat and misconfiguration signals.
- SHOULD keep alert ownership and escalation routing explicit.

## Reliability and Operational Safety
- SHOULD keep region/zone resilience assumptions explicit for critical workloads.
- SHOULD use staged rollout for risky platform changes.
- SHOULD keep backup/restore and disaster-recovery procedures tested.
- SHOULD monitor quota/limit headroom and scaling boundaries proactively.

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

## Override Notes
- Project-specific Azure conventions MAY narrow implementation details, but
  least-privilege identity, private-by-default networking, auditability, and
  operational resilience controls remain mandatory.
