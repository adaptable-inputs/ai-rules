---
applies_to:
  load: "conditional"
  when: "the declared compliance scope includes `dora`, or no compliance scope is declared"
  annex: "DORA.ANNEX.md"
  purpose: "baseline engineering controls that support DORA-style ICT risk and resilience obligations"
  inherits: ["COMPLIANCE/COMPLIANCE.md", "SECURITY/SECURITY.md", "INFRASTRUCTURE/**", "CI-CD/**", "CORE/LOGGING.md"]
---
# DORA

Engineering policy guidance for AI agents on EU Digital Operational Resilience Act (DORA) relevant software and
operations controls.

This is engineering policy guidance, not legal advice. Consult qualified legal counsel for final legal decisions.

## Defaults
- SHOULD keep ICT risk ownership explicit for critical business services.
- SHOULD keep resilience-by-design controls integrated in delivery pipelines.
- SHOULD keep incident handling, communication, and evidence trails auditable.
- SHOULD keep third-party ICT dependency risk continuously managed.
- SHOULD keep recovery and continuity controls validated through regular exercises.

## ICT Risk Management Controls
- SHOULD keep critical-service inventory and dependency mapping current.
- SHOULD track risk scenarios, mitigation owners, and remediation deadlines.
- MUST enforce change-management controls for high-impact ICT changes.
- MUST require bounded approval for temporary control exceptions.

## Incident Handling and Reporting Readiness
- SHOULD define incident severity classification tied to escalation obligations.
- SHOULD keep detection, triage, containment, and recovery workflows documented.
- SHOULD keep event timelines and decision logs suitable for reporting obligations.
- SHOULD ensure post-incident corrective actions are tracked to closure.

## Resilience Testing and Continuity
- SHOULD keep backup, restore, and failover objectives explicit.
- SHOULD run periodic resilience testing for critical services.
- SHOULD validate recovery time and recovery point assumptions against targets.
- SHOULD keep scenario tests for dependency outage and degradation events.

## Third-Party ICT Risk Controls
- SHOULD keep critical vendor/service dependency register current.
- SHOULD define fallback/exit strategies for high-criticality third-party services.
- MUST keep integration privileges scoped and auditable.
- SHOULD reassess third-party risk after major incidents or material changes.
