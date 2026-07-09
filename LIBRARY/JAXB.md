---
applies_to:
  load: "conditional"
  when: "jaxb is a declared dependency"
  libraries: ["jaxb"]
  annex: "JAXB.ANNEX.md"
  purpose: "JAXB usage rules for safe and stable XML serialization/deserialization"
  inherits: ["LANGUAGE/JAVA/JAVA.md", "SECURITY/SECURITY.md", "TEST/TEST.md", "COMPLIANCE/**"]
---
# JAXB

Guidance for AI agents implementing and reviewing JAXB XML binding.

## Defaults
- SHOULD use JAXB when XML contract interop requires it.
- SHOULD keep JAXB DTOs separate from core domain models.
- SHOULD prefer explicit annotations over implicit mapping defaults.
- SHOULD keep schema and binding models versioned and documented.

## Mapping and Contract Rules
- SHOULD keep field names/types aligned with external schema contract.
- SHOULD avoid leaking internal domain semantics into XML contract types.
- SHOULD keep namespace handling explicit and consistent.
- SHOULD preserve backward compatibility when evolving XML contracts.

## Validation and Parsing Safety
- SHOULD validate untrusted XML against schema where feasible.
- MUST fail fast on invalid payloads with actionable errors.
- MUST configure XML parser securely (XXE/entity expansion protections).
- SHOULD avoid permissive parsing that masks malformed input.

## Override Notes
- If alternative XML libraries are used for specific needs, maintain the same
  contract compatibility and parser security constraints.
