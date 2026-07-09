---
applies_to:
  load: "always"
  annex: "GDPR_BDSG.ANNEX.md"
---
# GDPR_BDSG

Engineering policy guidance for AI agents on GDPR (DSGVO) and BDSG relevant
software decisions in EU/German contexts.

This is engineering policy guidance, not legal advice.
Consult qualified legal counsel for final legal decisions.

## Scope
- Define baseline engineering controls for personal-data handling aligned with
  GDPR/BDSG expectations.
- Apply this file when systems process, store, transfer, or log personal data
  (including pseudonymous identifiers where applicable).

## Semantic Dependencies
- Inherit compliance baseline from `COMPLIANCE/COMPLIANCE.md` and
  `COMPLIANCE/LICENSES.md`.
- Inherit security controls from `SECURITY/SECURITY.md`.
- Inherit logging/data-minimization constraints from `CORE/LOGGING.md`.
- Inherit testing and review constraints from `TEST/TEST.md` and
  `REVIEW/CODE_REVIEW.md`.

## Defaults
- SHOULD keep personal-data inventory explicit per system boundary.
- MUST apply purpose limitation and data minimization by default.
- SHOULD keep lawful basis mapping explicit for each processing purpose.
- SHOULD keep retention/deletion policies explicit and automatable.
- SHOULD keep privacy-relevant decisions and exceptions auditable.

## Data Classification and Collection Rules
- MUST classify data by sensitivity and purpose before implementation changes.
- MUST collect only fields required for current documented purpose.
- SHOULD avoid collecting special-category personal data unless explicitly justified and
  approved.
- MUST keep telemetry/analytics payloads free of unnecessary personal data.

## Lawful Basis and Transparency Hooks
- SHOULD map each processing purpose to a documented lawful basis.
- MUST keep user-facing disclosures aligned with actual processing behavior.
- MUST require explicit consent handling where consent is the legal basis.
- MUST keep consent capture, versioning, and withdrawal behavior traceable.

## Retention, Deletion, and Data Subject Rights
- SHOULD implement retention schedules with automatic expiry/deletion where possible.
- MUST support DSAR-relevant operations (access, correction, deletion, restriction/objection) through documented
  workflows.
- MUST keep deletion effective across primary data, replicas, caches, and derived stores where feasible.
- MUST keep legal-hold exceptions explicit, approved, and time-bounded.

## Access, Transfer, and Processor Controls
- MUST enforce least privilege for personal-data access paths.
- SHOULD keep processor/subprocessor usage documented and contract-aligned.
- MUST validate cross-border transfer constraints before enabling new data flows.
- MUST keep data exports/imports auditable and purpose-bound.

## DPIA and High-Risk Change Triggers
- MUST escalate to privacy/legal review when processing risk materially increases.
- MUST treat large-scale profiling, sensitive-category processing, or new surveillance-like capabilities as DPIA
  triggers.
- MUST block rollout of high-risk processing changes until required approvals exist.

## Override Notes
- Project-specific privacy policies MAY be stricter; stricter policy always
  wins.
