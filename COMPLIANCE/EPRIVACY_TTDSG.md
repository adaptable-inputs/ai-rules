---
applies_to:
  load: "always"
---
# EPRIVACY_TTDSG

Engineering policy guidance for AI agents on ePrivacy-oriented and TTDSG
controls for client-side storage and tracking technologies.

This is engineering policy guidance, not legal advice.
Consult qualified legal counsel for final legal decisions.

## Scope
- Define baseline engineering controls for cookie/device storage and
  communications-tracking behavior in EU/German contexts.
- Apply this file when implementing web/mobile telemetry, tracking,
  personalization, or client-side identifier storage.

## Semantic Dependencies
- Inherit compliance baseline from `COMPLIANCE/COMPLIANCE.md`.
- Inherit privacy controls from `COMPLIANCE/GDPR_BDSG.md`.
- Inherit security controls from `SECURITY/SECURITY.md`.
- Inherit logging constraints from `CORE/LOGGING.md`.

## Defaults
- MUST disable non-essential tracking/storage by default until valid consent exists.
- MUST keep consent categories explicit and purpose-bound.
- MUST keep telemetry payloads minimal and privacy-preserving.
- SHOULD keep consent state auditable with versioned policy metadata.
- MUST keep withdrawal/revocation behavior equivalent to grant behavior.

## Consent and Purpose Controls
- MUST gate non-essential cookies/storage and similar tracking technologies behind explicit consent where required.
- MUST keep strict separation between essential and non-essential categories.
- MUST keep consent prompts clear, non-deceptive, and purpose-specific.
- MUST prevent implicit bundling of unrelated consent purposes.

## Client-Side Identifier and Storage Rules
- SHOULD minimize persistent identifiers and storage duration.
- SHOULD avoid hidden fingerprinting-like techniques without explicit legal approval.
- SHOULD rotate or scope identifiers where feasible to reduce tracking surface.
- MUST keep client-side storage contents free of unnecessary personal data.

## Telemetry and Analytics Boundaries
- SHOULD use aggregated/anonymized data where possible for analytics.
- SHOULD avoid transmitting raw user-content or sensitive fields in telemetry.
- MUST keep third-party analytics integrations bounded and configurable by consent state.
- MUST ensure consent state is enforced across all telemetry emitters.

## Revocation, Retention, and Auditability
- MUST implement immediate effect for consent withdrawal on non-essential tracking.
- MUST delete or disable non-essential identifiers/tokens upon revocation where feasible.
- SHOULD keep retention windows explicit for tracking-related data.
- SHOULD keep consent records and policy-version linkage auditable.

## High-Risk Pitfalls
1. Loading non-essential trackers before consent.
2. Treating pre-checked boxes or passive interaction as valid consent.
3. Storing long-lived identifiers with no necessity justification.
4. Sending sensitive user data into analytics payloads.
5. Ignoring withdrawal requests or delaying revocation effect.
6. Inconsistent consent enforcement across first-party and third-party scripts.
7. Missing consent audit evidence for policy/version in effect.

## Do / Don't Examples
### 1. Consent Gating
```text
Don't: initialize analytics scripts on initial page load by default.
Do:    delay non-essential trackers until valid consent is recorded.
```

### 2. Identifier Scope
```text
Don't: create persistent cross-context identifiers without necessity.
Do:    minimize identifier scope/lifetime and document purpose.
```

### 3. Withdrawal Handling
```text
Don't: keep tracking active after user revokes consent.
Do:    disable non-essential tracking immediately on revocation.
```

## Code Review Checklist for ePrivacy/TTDSG
- Are non-essential tracking/storage paths gated behind valid consent?
- Are consent categories clear, purpose-bound, and non-bundled?
- Are telemetry payloads minimized and free of sensitive content?
- Are third-party trackers/integrations fully consent-aware?
- Are identifier lifetime/scope choices justified and minimal?
- Are revocation and retention behaviors explicit and testable?
- Is consent evidence and policy-version linkage auditable?

## Testing Guidance
- Test tracker initialization behavior before and after consent.
- Test consent withdrawal effects across first-party and third-party scripts.
- Test category-specific consent toggles and enforcement consistency.
- Test telemetry payload redaction/minimization for sensitive fields.
- Test consent-record auditability including policy/version references.

## Override Notes
- Project or sector-specific regulation MAY be stricter; stricter policy always
  wins.
