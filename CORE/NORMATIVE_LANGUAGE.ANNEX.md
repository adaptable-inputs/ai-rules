---
applies_to:
  load: "annex"
  annex_of: "NORMATIVE_LANGUAGE.md"
  tasks: ["review", "test"]
---
# NORMATIVE_LANGUAGE - Annex

## Do / Don't Examples
### 1. Obligation Level
```text
Don't: Prefer constructor injection.
Do:    SHOULD prefer constructor injection over field injection.
```

### 2. Absolute Prohibition
```text
Don't: Never push directly to protected branches.
Do:    MUST NOT push directly to protected branches.
```

### 3. Genuine Option
```text
Don't: Use a BOM where appropriate.
Do:    MAY centralize versions with a BOM when more than one module depends on
       the same artifact.
```
