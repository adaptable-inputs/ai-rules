---
applies_to:
  load: "conditional"
  when: "the project deploys to AWS"
  tools: ["aws"]
  annex: "AWS.ANNEX.md"
  purpose: "AWS-specific platform guardrails for secure and reliable operations"
  inherits: ["INFRASTRUCTURE/INFRASTRUCTURE.md", "INFRASTRUCTURE/INFRA_AS_CODE.md", "SECURITY/SECURITY.md", "COMPLIANCE/COMPLIANCE.md", "CI-CD/CI-CD.md", "CORE/VERSION_CONTROL_SYSTEM.md"]
---
# AWS

Guidance for AI agents implementing and reviewing AWS platform configuration and operations choices.

## Defaults
- SHOULD use multi-account strategies for environment and blast-radius isolation.
- MUST apply least privilege IAM by default for users, roles, and services.
- SHOULD keep network access private by default; expose public endpoints intentionally.
- MUST enable encryption in transit and at rest for sensitive data paths.
- SHOULD keep tagging standards mandatory for ownership, environment, and cost center.

## Identity and Access Guardrails
- SHOULD prefer role assumption and short-lived credentials over long-lived static access keys.
- MUST keep human admin access behind strong MFA and audit controls.
- MUST restrict cross-account trust with explicit conditions and least privilege.
- MUST review wildcard permissions (`*`) and high-risk actions as exceptions only.

## Network and Data Protection
- MUST keep VPC, subnet, and security-group intent explicit and least-open.
- SHOULD avoid unrestricted ingress/egress rules unless explicitly justified.
- MUST keep data services private and fronted by controlled access layers.
- MUST enforce key-management policy and rotation where required.

## Logging, Audit, and Detection
- SHOULD keep account/org audit logs enabled and protected from tampering.
- SHOULD keep service/application logs centralized and queryable.
- SHOULD enable detection/monitoring controls for threat and misconfiguration events.
- SHOULD keep alert routing and escalation ownership explicit.

## Reliability and Operational Safety
- SHOULD keep region/AZ resilience assumptions explicit for critical workloads.
- SHOULD use staged rollout for risky platform changes.
- SHOULD keep backup/restore and disaster-recovery procedures tested.
- SHOULD keep quotas/limits and scaling boundaries monitored proactively.
