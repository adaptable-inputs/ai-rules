---
applies_to:
  load: "conditional"
  when: "the project deploys to Azure"
  tools: ["azure"]
  annex: "AZURE.ANNEX.md"
  purpose: "Azure-specific platform guardrails for secure and reliable operations"
  inherits: ["INFRASTRUCTURE/INFRASTRUCTURE.md", "INFRASTRUCTURE/INFRA_AS_CODE.md", "SECURITY/SECURITY.md", "COMPLIANCE/COMPLIANCE.md", "CI-CD/CI-CD.md", "CORE/VERSION_CONTROL_SYSTEM.md"]
---
# AZURE

Guidance for AI agents implementing and reviewing Azure platform configuration
and operations choices.

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
