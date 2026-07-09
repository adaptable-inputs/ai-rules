---
applies_to:
  load: "annex"
  annex_of: "YAML.md"
  tasks: ["review", "test"]
---
# YAML - Annex

## High-Risk Pitfalls
1. Indentation errors producing silent semantic changes.
2. Ambiguous scalar parsing (`on`, `off`, `yes`, `no`) causing type bugs.
3. Overuse of anchors/merges making effective config opaque.
4. Committing secrets or token-like values into version control.
5. Environment overlays drifting without validation.
6. Mixed list item shapes causing runtime parser/schema failures.

## Do / Don't Examples
### 1. Ambiguous Scalars
```yaml
# Don't: ambiguous values
featureFlag: on
releaseVersion: 01.02

# Do: explicit typing
featureFlag: true
releaseVersion: "01.02"
```

### 2. Secret Handling
```yaml
# Don't: commit plaintext secrets
database:
  password: super-secret
```

```yaml
# Do: reference an external secret source (valid Kubernetes example)
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
    - name: app
      image: example/app:1.0.0
      env:
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-password
```

### 3. Anchor Overuse
```yaml
# Don't: nested merges make effective config hard to reason about
appDefaults: &appDefaults
  image: app:1.2.3
  resources:
    requests: { cpu: "100m", memory: "128Mi" }
    limits: { cpu: "500m", memory: "512Mi" }
prod:
  <<: *appDefaults
  resources:
    <<: { requests: { cpu: "200m", memory: "256Mi" } }
```

```yaml
# Do: keep overrides explicit and shallow
prod:
  image: app:1.2.3
  resources:
    requests: { cpu: "200m", memory: "256Mi" }
    limits: { cpu: "500m", memory: "512Mi" }
```

## Code Review Checklist for YAML
- Is indentation/style consistent and parser-safe?
- Are ambiguous scalars quoted/typed explicitly?
- Are secrets excluded from committed YAML?
- Are anchors/aliases used sparingly and clearly?
- Are environment overrides intentional and minimal?
- Does file shape conform to expected schema/tool contract?

## Testing Guidance for YAML
- Validate YAML syntax in CI.
- Validate against target schemas (where available).
- Run dry-run/plan validation for deployment-related YAML.
- Test environment overlays to ensure expected effective config.
- Add checks preventing committed secrets.
