---
applies_to:
  load: "conditional"
  when: "the project authors YAML"
  languages: ["yaml"]
  globs: ["**/*.yml", "**/*.yaml"]
  annex: "YAML.ANNEX.md"
  purpose: "YAML authoring rules for correctness, readability, and secure configuration management"
  inherits: ["SECURITY/SECURITY.md", "LANGUAGE/CONVENTIONS.md", "LANGUAGE/READABILITY.md"]
---
# YAML

Guidance for AI agents implementing and reviewing YAML configuration files.

## Defaults
- SHOULD keep YAML files deterministic and explicit.
- SHOULD prefer spaces over tabs (tabs are invalid in YAML indentation).
- SHOULD keep indentation consistent (typically 2 spaces unless ecosystem demands 4).
- SHOULD keep keys stable and semantically named.
- SHOULD keep list item structure consistent across entries.

## Type and Parsing Safety
- Quote ambiguous scalars when type ambiguity is risky (`on`, `off`, `yes`,
  `no`, version-like numbers, leading-zero values).
- SHOULD prefer explicit booleans and numbers when schema expects them.
- SHOULD avoid relying on parser-specific coercion behavior.
- SHOULD keep date/time values explicit and consistently formatted.

## Anchors, Aliases, and Merge Keys
- SHOULD use anchors/aliases sparingly and only when they improve maintainability.
- SHOULD avoid deep merge trees that obscure effective configuration.
- SHOULD prefer explicit repetition over complex indirection when readability suffers.
- SHOULD document non-obvious anchor/merge usage in nearby comments.

## Secrets and Security
- MUST NOT commit plaintext secrets in YAML files.
- MUST use secret references/injection mechanisms provided by target platform.
- MUST keep environment-specific secret values outside source control.
- MUST validate secret key names and expected presence in deployment pipelines.

## Environment and Drift Management
- SHOULD keep base and environment overlays aligned with clear override intent.
- SHOULD avoid copy-paste divergence across environment files.
- SHOULD track schema version fields explicitly when supported.
- SHOULD keep default values safe; production overrides SHOULD be minimal and explicit.

## Override Notes
- Platform/tool docs MAY add schema-specific constraints.
- Baseline parsing safety and secret-handling rules in this file remain
  mandatory.
