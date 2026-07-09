---
applies_to:
  load: "annex"
  annex_of: "DORA.md"
  tasks: ["review", "test"]
---
# DORA - Annex

## High-Risk Pitfalls
1. Critical ICT services without explicit risk/control ownership.
2. Incident workflows that do not produce auditable reporting evidence.
3. Recovery assumptions untested in realistic failure scenarios.
4. Third-party critical dependencies with no fallback strategy.
5. Change velocity that bypasses resilience and approval gates.
6. Risk exceptions granted with no expiry or remediation plan.
7. Post-incident actions not tracked through completion.

## Do / Don't Examples
### 1. Incident Evidence
```text
Don't: run major incident response with no structured decision logging.
Do:    keep timestamped incident timelines and remediation evidence.
```

### 2. Third-Party Dependency
```text
Don't: rely on a critical vendor with no continuity or exit planning.
Do:    maintain fallback and recovery strategy for critical dependencies.
```

### 3. Recovery Validation
```text
Don't: accept untested recovery objectives as operationally proven.
Do:    test restore/failover scenarios and record outcomes.
```

## Code Review Checklist for DORA Context
- Is critical-service and dependency ownership explicit?
- Are ICT risk controls and mitigation responsibilities documented?
- Are incident detection/response/reporting hooks operationally usable?
- Are continuity/recovery objectives explicit and tested?
- Are third-party ICT dependencies controlled with fallback/exit planning?
- Are risk exceptions bounded, approved, and tracked to closure?

## Testing Guidance
- Test incident-response workflows and reporting evidence capture.
- Test continuity/failover/restore exercises for critical services.
- Test dependency-outage scenarios for critical third-party integrations.
- Test CI/CD controls that enforce high-impact change gates.
- Test closure tracking for incident and resilience remediation actions.
