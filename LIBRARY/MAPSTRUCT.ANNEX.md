---
applies_to:
  load: "annex"
  annex_of: "MAPSTRUCT.md"
  tasks: ["review", "test"]
---
# MAPSTRUCT - Annex

## High-Risk Pitfalls
1. Silent unmapped fields after DTO evolution.
2. Business rules embedded in mapping expressions.
3. Unclear null/update semantics causing data loss.
4. Massive mapper interfaces with mixed domain boundaries.
5. Hidden conversion logic hard to test/debug.

## Do / Don't Examples
### 1. Unmapped Fields
```text
Don't: ignore newly added target fields accidentally.
Do:    configure strict unmapped target policy and handle explicitly.
```

### 2. Business Logic Placement
```text
Don't: complex domain rules in @Mapping(expression = ...).
Do:    keep mapper structural; perform domain rules in service/use-case layer.
```

### 3. Update Semantics
```text
Don't: overwrite existing target fields with null unintentionally.
Do:    define null-value property mapping strategy explicitly.
```

## Code Review Checklist for MapStruct
- Are mapper boundaries cohesive and domain-aligned?
- Are field mappings explicit where required?
- Are unmapped-field policies strict enough?
- Are null/update semantics intentional and safe?
- Is business logic kept outside mapping layer?
- Are nested/collection mappings readable and tested?

## Testing Guidance
- Add mapper unit tests for representative DTO/entity pairs.
- Add tests for null and partial-update semantics.
- Add regression tests when source/target models evolve.
- Validate compile-time mapping failures are surfaced in CI.
