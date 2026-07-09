---
applies_to:
  load: "always"
---
# EU_AI_ACT

Engineering policy guidance for AI agents on EU AI Act relevant controls for
software projects that build, integrate, or operate AI systems.

This is engineering policy guidance, not legal advice.
Consult qualified legal counsel for final legal decisions.

## Scope
- Define baseline engineering controls for AI-system lifecycle governance in
  EU-regulated contexts.
- Apply this file when software includes AI features, models, or AI-assisted
  decision flows that MAY be subject to EU AI Act obligations.

## Semantic Dependencies
- Inherit compliance baseline from `COMPLIANCE/COMPLIANCE.md`.
- Inherit security controls from `SECURITY/SECURITY.md`.
- Inherit logging and traceability constraints from `CORE/LOGGING.md`.
- Inherit privacy controls from `COMPLIANCE/GDPR_BDSG.md` where personal data
  processing is involved.
- Inherit testing and review constraints from `TEST/TEST.md` and
  `REVIEW/CODE_REVIEW.md`.

## Defaults
- SHOULD keep AI feature inventory explicit by model, purpose, and owner.
- MUST classify AI use-cases by applicable risk category before rollout.
- SHOULD keep documentation and traceability for model/data/version lineage.
- MUST keep human oversight and fallback controls explicit where required.
- SHOULD keep monitoring and incident escalation for AI behavior deviations.

## Use-Case Classification and Scope Control
- MUST classify each AI use-case against prohibited/high-risk/limited/minimal-risk expectations before production use.
- MUST block rollout when risk classification is unknown or unresolved.
- SHOULD keep ownership explicit for classification decisions and updates.
- MUST reassess classification when use-case scope or model behavior changes.

## Transparency and User-Facing Controls
- MUST ensure users are informed when interacting with AI systems where required.
- MUST keep generated/synthetic content disclosure controls where applicable.
- SHOULD keep user-facing limitations and confidence caveats explicit for decision-support outputs.
- SHOULD avoid presenting probabilistic outputs as deterministic facts.

## Human Oversight and Decision Boundaries
- MUST keep human review/override controls for high-impact decision contexts.
- MUST define clear escalation and fallback paths when AI confidence/quality is low.
- MUST prevent fully automated high-impact decisions without required controls.
- SHOULD keep accountability explicit between AI output and final business action.

## Data, Model, and Logging Governance
- SHOULD keep training/evaluation data provenance and quality assumptions documented.
- MUST keep model/prompt/config/version changes auditable and reproducible.
- SHOULD log AI-system events needed for traceability.
- MUST NOT expose sensitive data in AI-system logs.
- SHOULD keep bias/safety/performance monitoring controls active post-deployment.

## Third-Party AI Dependency Controls
- SHOULD keep third-party model/provider usage documented with contractual boundaries.
- SHOULD assess provider limitations, retention behavior, and security posture.
- SHOULD keep fallback plans for provider outages or policy-breaking behavior changes.
- MUST restrict sensitive data exposure to external AI providers unless explicitly approved.

## High-Risk Pitfalls
1. Shipping AI features without explicit risk classification.
2. Missing transparency controls for AI-generated interactions/content.
3. No human-oversight path for high-impact AI-assisted decisions.
4. Untracked model/prompt/version changes in production.
5. No monitoring for harmful drift, bias, or reliability regressions.
6. Over-sharing sensitive data with external AI providers by default.
7. Treating AI outputs as deterministic truth without confidence handling.

## Do / Don't Examples
### 1. Risk Classification
```text
Don't: ship new AI use-case with "we'll classify later" mindset.
Do:    classify risk category before rollout and gate release on completion.
```

### 2. Human Oversight
```text
Don't: allow fully automated high-impact actions with no review path.
Do:    keep human review/override controls and escalation hooks.
```

### 3. Traceability
```text
Don't: deploy model/prompt changes with no versioned audit trail.
Do:    record model, prompt/config, and release lineage for each change.
```

## Code Review Checklist for EU AI Act Context
- Is AI use-case risk classification explicit and current?
- Are transparency/user-disclosure controls present where required?
- Are human oversight/fallback controls sufficient for decision impact?
- Are model/data/version lineage and change logs auditable?
- Are monitoring controls in place for harmful drift/bias/reliability risks?
- Are third-party AI integrations bounded and data-safe?

## Testing Guidance
- Test risk-classification gating before production rollout.
- Test user-facing transparency/disclosure behavior.
- Test human-oversight and fallback workflows under degraded AI quality.
- Test model/prompt/config version traceability and rollback.
- Test monitoring/alerting for drift, bias signals, and reliability anomalies.

## Override Notes
- Project or sector-specific regulation MAY be stricter; stricter policy always
  wins.
