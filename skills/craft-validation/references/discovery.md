# Discovery

Dispatch one `craft-onboard-explorer` per slice below, all in parallel.

## Slices

### Build & typecheck

```text
Slice: Build & typecheck
Investigate: build commands, toolchain, compiler flags, success/failure output,
common build failures and fixes. Check dependency files (go.mod, package.json,
Cargo.toml, etc.), tsconfig, Makefile, build scripts, Dockerfile.
```

### Test infrastructure

```text
Slice: Test infrastructure
Investigate: test framework, runner commands, how to run all vs a subset,
mocking approach, fixture conventions. Check test files, mock configs, CI test
steps.
```

### Lint & format

```text
Slice: Lint & format
Investigate: linter and formatter tools, configs, auto-fix commands. Check lint
configs, pre-commit hooks, CI lint steps.
```

### Local dev & smoke test

```text
Slice: Local dev & smoke test
Investigate: how to run locally (docker-compose, scripts, direct run), ports,
env vars, health check endpoints, hot reload. Check /etc/hosts, .env,
docker-compose extra_hosts, README, and project docs for custom domain
mappings — never assume localhost.
```

### CI pipeline & deploy

```text
Slice: CI pipeline & deploy
Investigate: CI system, pipeline steps in order, triggers, artifacts, deploy
commands. Check CI config files and deploy scripts.
```

### Debug

```text
Slice: Debug
Investigate: debugger setup, log format/location, how to attach, useful env
knobs. Check IDE launch configs, docker-compose debug ports, hot-reload configs.
```

### Authentication & API smoke tests

```text
Slice: Authentication & API smoke tests
Investigate: how to authenticate for local testing — check auth middleware, API
key sources (secret store names, env vars, config keys), session/cookie auth.
Identify 3-5 safe-to-call endpoints (no side effects) to verify the API works.
Check route definitions, swagger/OpenAPI specs, project docs. Check /etc/hosts
and .env for custom domain mappings.
```

### Frontend validation

Only dispatch if the project has a frontend.

```text
Slice: Frontend validation
Investigate: 3-5 key pages to verify in a browser. For each: the URL, what
should be visible, whether login is required. If login is needed, describe the
flow. Check router files, page components, .env, project docs. If no frontend
exists, say so.
```
