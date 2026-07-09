---
applies_to:
  load: "conditional"
  when: "the project deploys to GCP"
  tools: ["gcp"]
  annex: "GCP.ANNEX.md"
  purpose: "GCP-specific platform guardrails for secure and reliable operations"
  inherits: ["INFRASTRUCTURE/INFRASTRUCTURE.md", "INFRASTRUCTURE/INFRA_AS_CODE.md", "SECURITY/SECURITY.md", "COMPLIANCE/COMPLIANCE.md", "CI-CD/CI-CD.md", "CORE/VERSION_CONTROL_SYSTEM.md"]
---
# GCP

Guidance for AI agents implementing and reviewing Google Cloud Platform (GCP)
configuration and operations choices.

## Defaults
- SHOULD use org/folder/project hierarchy for environment and ownership isolation.
- MUST apply least privilege IAM by default for users, service accounts, and groups.
- SHOULD keep network access private by default; expose public endpoints intentionally.
- MUST enable encryption and key-management controls for sensitive data paths.
- SHOULD keep labeling standards mandatory for ownership, environment, and cost center.

## Identity and Access Guardrails
- SHOULD prefer workload identity federation and short-lived credentials.
- MUST minimize broad primitive roles and high-privilege grants.
- MUST keep service-account key creation heavily restricted and monitored.
- MUST keep cross-project access explicit and least-privilege.

## Network and Data Protection
- MUST keep VPC/firewall intent explicit and least-open.
- SHOULD avoid broad ingress/egress rules unless explicitly justified.
- MUST keep sensitive services private behind controlled access layers.
- MUST enforce key-management and secret handling controls for regulated data paths.

## Logging, Audit, and Detection
- SHOULD keep audit logging enabled at required levels for critical services.
- SHOULD centralize logs/metrics for operational and security analysis.
- SHOULD enable detection/monitoring controls for threat and misconfiguration signals.
- SHOULD keep alert ownership and escalation routing explicit.

## Reliability and Operational Safety
- SHOULD keep multi-zone/region resilience assumptions explicit for critical workloads.
- SHOULD use staged rollout for risky platform changes.
- SHOULD keep backup/restore and disaster-recovery procedures tested.
- SHOULD monitor quotas, API limits, and scaling boundaries proactively.

## Override Notes
- Project-specific GCP conventions MAY narrow implementation details, but
  least-privilege identity, private-by-default networking, auditability, and
  operational resilience controls remain mandatory.
