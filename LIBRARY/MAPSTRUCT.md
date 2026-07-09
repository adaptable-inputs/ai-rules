---
applies_to:
  load: "conditional"
  when: "mapstruct is a declared dependency"
  libraries: ["mapstruct"]
  annex: "MAPSTRUCT.ANNEX.md"
  purpose: "MapStruct mapping rules for explicit, type-safe DTO/entity conversion"
  inherits: ["LANGUAGE/JAVA/JAVA.md", "ARCHITECTURE/CLEAN_ARCHITECTURE.md"]
---
# MAPSTRUCT

Guidance for AI agents implementing and reviewing MapStruct mappings.

## Defaults
- SHOULD prefer MapStruct for repetitive structural mapping.
- SHOULD keep mapping logic explicit and compile-time verified.
- SHOULD keep mappers focused per bounded context/boundary.
- SHOULD keep business logic out of mappers.

## Mapping Policy
- SHOULD prefer explicit field mappings when names differ.
- SHOULD configure unmapped target policy intentionally (fail fast for unexpected gaps).
- SHOULD keep update mappings (`@MappingTarget`) explicit about null handling.
- SHOULD keep nested/collection mappings readable and test-covered.

## Null and Default Handling
- SHOULD define null value strategy intentionally.
- SHOULD avoid surprising defaults that hide missing source data.
- SHOULD keep partial-update semantics explicit and predictable.

## Composition and Reuse
- SHOULD split large mappers into cohesive units.
- SHOULD reuse helper mappers for shared value transformations.
- SHOULD avoid circular mapper dependencies.
- SHOULD keep generated code reviewable via explicit annotations/config.

## Override Notes
- Project-specific mapping standards MAY require stricter mapper granularity,
  but explicitness and business-logic separation here remain mandatory.
