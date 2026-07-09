---
applies_to:
  load: "annex"
  annex_of: "GRAPHQL.md"
  tasks: ["review", "test"]
---
# GRAPHQL - Annex

## High-Risk Pitfalls
1. N+1 resolver query explosions.
2. Unbounded query complexity without cost controls.
3. Breaking field changes without deprecation path.
4. Authorization inconsistencies between top-level and nested resolvers.
5. Ambiguous nullability contracts causing client/runtime bugs.
6. Leaking internal exception details in GraphQL errors.
7. Mutations with hidden side effects and no clear contract.

## Do / Don't Examples
### 1. N+1 Pattern
```text
Don't: query database once per parent row in field resolver.
Do:    batch child loads with DataLoader per request scope.
```

### 2. Schema Evolution
```text
Don't: rename existing field without transition.
Do:    add new field, deprecate old field, publish migration window.
```

### 3. Error Extensions
```jsonc
// Don't
{"errors":[{"message":"failed"}]}

// Do
{"errors":[{"message":"Validation failed",
             "extensions":{"code":"VALIDATION_ERROR"}}]}
```

## Code Review Checklist for GraphQL
- Is schema design explicit and domain-oriented?
- Are compatibility/deprecation policies respected?
- Are resolvers thin and business logic extracted?
- Is N+1 prevention implemented for nested fields?
- Are depth/complexity limits and pagination present?
- Are auth/authz checks consistent on nested and top-level paths?
- Are error payloads safe and machine-readable?

## Testing Guidance for GraphQL
- Add schema contract tests for key queries/mutations.
- Test authorization on nested and top-level resolvers.
- Test complexity/depth guard behavior for abusive queries.
- Test N+1-sensitive queries with query-count assertions.
- Test deprecation compatibility for legacy clients.
