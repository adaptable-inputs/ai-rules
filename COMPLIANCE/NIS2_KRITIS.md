---
applies_to:
  load: "always"
  annex: "NIS2_KRITIS.ANNEX.md"
  purpose: "baseline engineering controls that support NIS2-style cybersecurity and resilience obligations in EU/German critical-operations contexts"
  inherits: ["COMPLIANCE/COMPLIANCE.md", "SECURITY/SECURITY.md", "INFRASTRUCTURE/**", "CI-CD/**", "CORE/LOGGING.md"]
---
# NIS2_KRITIS

Engineering policy guidance for AI agents on NIS2-oriented controls and German
KRITIS-context operational obligations.

This is engineering policy guidance, not legal advice.
Consult qualified legal counsel for final legal decisions.

## Defaults
- SHOULD keep security governance ownership explicit for critical services.
- SHOULD keep risk assessment and mitigation evidence current and auditable.
- SHOULD keep incident detection, classification, and escalation paths documented.
- SHOULD keep supply-chain and third-party dependency risk controls active.
- SHOULD keep business-continuity and recovery assumptions tested.

## Governance and Risk Controls
- SHOULD maintain current asset/service inventory for in-scope systems.
- SHOULD maintain risk register entries for major service and dependency risks.
- SHOULD track remediation actions with owner and due date.
- MUST require explicit approval for temporary risk exceptions and expiry dates.

## Incident Readiness and Reporting Hooks
- SHOULD define incident severity model and escalation ownership.
- SHOULD keep incident triage procedures and responder runbooks available.
- SHOULD keep timestamped evidence collection ready for forensic/regulatory needs.
- MUST ensure incident classification supports required reporting timelines.
- MUST block unresolved critical incident states from silent production progression.

## Supply Chain and Dependency Governance
- MUST keep dependency provenance and vulnerability scanning in CI.
- SHOULD evaluate third-party provider criticality and failure impact regularly.
- MUST keep third-party access and integration scopes least-privilege.
- SHOULD keep fallback and substitution plans for critical third-party services.

## Resilience, Continuity, and Recovery
- SHOULD keep backup, restore, and recovery objectives explicit for critical systems.
- SHOULD keep disaster-recovery exercises and failover validation periodic.
- SHOULD avoid single points of failure in infrastructure/control planes where feasible.
- MUST keep change management gates strong for critical production paths.
