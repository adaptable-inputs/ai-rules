---
applies_to:
  load: "annex"
  annex_of: "DOCKER.md"
  tasks: ["review", "test"]
---
# DOCKER - Annex

## High-Risk Pitfalls
1. Unpinned base image drift.
2. Running as root in production containers.
3. Secrets leaked via Dockerfile args/env/layers.
4. Shipping build tools in runtime image.
5. Opaque entrypoints swallowing signals.
6. Large context copies bloating image/cache churn.

## Do / Don't Examples
### 1. Multi-Stage Build
```text
Don't: build and run from same full SDK image.
Do:    compile in builder stage, copy artifact to slim runtime stage.
```

### 2. User Privileges
```text
Don't: default root user in runtime image.
Do:    create/use dedicated non-root user.
```

### 3. Secrets
```text
Don't: ARG API_KEY=... in Dockerfile.
Do:    inject secrets at runtime via platform secret store.
```

## Code Review Checklist for Docker
- Is base image pinned and maintained?
- Is build multi-stage and runtime image minimal?
- Is container running as non-root with least privilege?
- Are secrets excluded from image/layers?
- Are health/shutdown/logging behaviors orchestration-friendly?
- Is image size/cache behavior controlled?

## Testing Guidance
- Build image from clean cache in CI to verify determinism.
- Run vulnerability scan on produced images.
- Run container startup/healthcheck/shutdown integration tests.
- Validate runtime user/permissions and secret injection behavior.
