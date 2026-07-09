---
applies_to:
  load: "annex"
  annex_of: "EPRIVACY_TTDSG.md"
  tasks: ["review", "test"]
---
# EPRIVACY_TTDSG - Annex

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
