---
applies_to:
  load: "annex"
  annex_of: "C_SHARP.md"
  tasks: ["review", "test"]
---
# C_SHARP - Annex

## High-Risk Pitfalls
1. Ignoring nullable warnings and relying on runtime null failures.
2. Blocking async request paths with `.Result`/`.Wait()`.
3. Missing cancellation propagation in external calls.
4. Catch-all exceptions that hide root causes.
5. Hidden dependencies through statics/singletons.
6. Blurred domain/infrastructure boundaries in one class.
7. Resource leaks from missing disposal patterns.

## Do / Don't Examples
### 1. Async Discipline
```text
Don't: call `.Result` inside an ASP.NET request path.
Do:    use `await` end-to-end and propagate cancellation.
```

### 2. Nullability
```text
Don't: disable nullable warnings to silence contract issues.
Do:    model nullable intent explicitly and validate boundaries.
```

### 3. Error Handling
```text
Don't: catch Exception and ignore it.
Do:    catch specific exceptions and preserve context.
```

## Code Review Checklist for C#/.NET
- Are nullable contracts explicit and respected?
- Are async paths non-blocking with proper cancellation flow?
- Are exception mappings specific and context-rich?
- Are disposal/resource lifecycles handled deterministically?
- Are architectural boundaries cohesive and explicit?
- Are dependency additions justified and maintainable?

## Testing Guidance
- Test nullability/validation behavior at API boundaries.
- Test async cancellation and timeout behavior for external IO.
- Test exception mapping and preserved root-cause details.
- Test concurrency-sensitive code for race/deadlock risks.
- Add regression tests for previously observed bug classes.
