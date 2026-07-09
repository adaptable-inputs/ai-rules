---
applies_to:
  load: "conditional"
  when: "the declared compliance scope includes `eu-ai-act`, or no compliance scope is declared"
  annex: "EU_AI_ACT.ANNEX.md"
  purpose: "baseline engineering controls for AI-system lifecycle governance in EU-regulated contexts"
  inherits: ["COMPLIANCE/COMPLIANCE.md", "SECURITY/SECURITY.md", "CORE/LOGGING.md", "COMPLIANCE/GDPR_BDSG.md", "TEST/TEST.md", "REVIEW/CODE_REVIEW.md"]
---
# EU_AI_ACT

Engineering policy guidance for AI agents on EU AI Act relevant controls for software projects that build, integrate, or
operate AI systems.

This is engineering policy guidance, not legal advice. Consult qualified legal counsel for final legal decisions.

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
