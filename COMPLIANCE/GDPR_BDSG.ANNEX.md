---
applies_to:
  load: "annex"
  annex_of: "GDPR_BDSG.md"
  tasks: ["review", "test"]
---
# GDPR_BDSG - Annex

## High-Risk Pitfalls
1. Collecting personal data without explicit purpose and lawful basis mapping.
2. Logging full personal payloads or persistent identifiers unnecessarily.
3. Retaining personal data indefinitely with no deletion path.
4. Building features that require consent but have no withdrawal path.
5. Shipping high-risk processing changes without DPIA/privacy review.
6. Cross-border transfer enablement without legal/compliance validation.
7. DSAR workflows that cannot locate or delete all relevant data copies.

## Do / Don't Examples
### 1. Data Minimization
```text
Don't: add broad personal profile fields "just in case" for future analytics.
Do:    collect only fields required for documented current purpose.
```

### 2. Logging
```text
Don't: log full request bodies containing personal data by default.
Do:    log minimal identifiers and redact sensitive fields.
```

### 3. Retention
```text
Don't: keep personal records forever with no retention schedule.
Do:    enforce explicit retention TTLs and verified deletion workflows.
```

## Code Review Checklist for GDPR/BDSG
- Is personal-data processing purpose explicit and necessary?
- Is lawful basis mapping documented for each processing purpose?
- Are minimization and redaction controls applied to logs/telemetry?
- Are retention/deletion rules explicit and technically enforceable?
- Are DSAR-relevant data access/correction/deletion workflows feasible?
- Are cross-border transfer implications identified and reviewed?
- Were high-risk changes escalated for privacy/legal review where required?

## Testing Guidance
- Test that personal-data redaction rules apply to logs/errors/telemetry.
- Test retention and deletion workflows, including replica/cache behavior.
- Test consent-capture and withdrawal flows where consent is required.
- Test DSAR workflows for data lookup, export, correction, and deletion paths.
- Test authorization boundaries for personal-data access APIs and tooling.
