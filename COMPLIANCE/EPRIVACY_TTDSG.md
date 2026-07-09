---
applies_to:
  load: "always"
  annex: "EPRIVACY_TTDSG.ANNEX.md"
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

## Override Notes
- Project or sector-specific regulation MAY be stricter; stricter policy always
  wins.
