---
applies_to:
  load: "annex"
  annex_of: "JAXB.md"
  tasks: ["review", "test"]
---
# JAXB - Annex

## High-Risk Pitfalls
1. Mixing JAXB DTOs directly into domain/business logic.
2. Contract drift between code and XSD.
3. Insecure XML parser settings (XXE risk).
4. Silent parsing failures with partial object state.
5. Breaking XML compatibility without migration strategy.

## Do / Don't Examples
### 1. Boundary Separation
```text
Don't: expose JAXB-annotated classes across service core.
Do:    map JAXB DTOs to domain models at adapter boundary.
```

### 2. Contract Evolution
```text
Don't: remove required XML elements abruptly.
Do:    add new optional fields and deprecate with migration plan.
```

### 3. Parser Security
```text
Don't: enable external entity resolution on untrusted input.
Do:    use hardened parser configuration and schema validation.
```

## Code Review Checklist for JAXB
- Are JAXB models isolated from domain core?
- Are annotations explicit and contract-aligned?
- Is XML parser configuration secure?
- Is schema compatibility/evolution strategy documented?
- Are invalid XML paths handled safely and observably?

## Testing Guidance
- Add round-trip serialization/deserialization tests.
- Add schema-validation tests for representative fixtures.
- Add negative tests for malformed/unsafe XML input.
- Add compatibility regression tests for contract evolution.
