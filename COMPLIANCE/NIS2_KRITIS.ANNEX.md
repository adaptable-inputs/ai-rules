---
applies_to:
  load: "annex"
  annex_of: "NIS2_KRITIS.md"
  tasks: ["review", "test"]
---
# NIS2_KRITIS - Annex

## High-Risk Pitfalls
1. No explicit ownership for operational cybersecurity controls.
2. Incident processes that cannot support required reporting timelines.
3. Missing evidence trails for incident decisions and remediation.
4. Critical third-party dependencies without fallback strategy.
5. Untracked risk exceptions with no expiry/approval.
6. Recovery plans that are documented but never tested.
7. Security controls bypassed for urgent changes without post-control closure.

## Do / Don't Examples
### 1. Incident Readiness
```text
Don't: rely on ad-hoc chat coordination with no severity/escalation model.
Do:    maintain documented triage/severity workflow and response ownership.
```

### 2. Third-Party Risk
```text
Don't: treat critical vendor dependencies as low-risk by default.
Do:    assess vendor criticality and define fallback/continuity paths.
```

### 3. Recovery Validation
```text
Don't: assume backups are sufficient without restore drills.
Do:    run and document periodic restore/failover tests.
```

## Code Review Checklist for NIS2/KRITIS Context
- Are critical-service ownership and risk controls explicit?
- Are incident detection/classification/escalation paths defined and usable?
- Are logging/evidence trails sufficient for incident reporting obligations?
- Are supply-chain and third-party dependency controls active?
- Are recovery objectives and tested continuity paths documented?
- Are temporary risk exceptions approved, bounded, and tracked to closure?

## Testing Guidance
- Test incident-detection and escalation workflows end-to-end.
- Test incident evidence capture and timeline reconstruction ability.
- Test dependency-failure scenarios and fallback behavior.
- Test backup/restore and failover for critical services.
- Test CI security/vulnerability gates for dependency and pipeline changes.
