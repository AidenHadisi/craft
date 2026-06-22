# Validation — FunnelJam

## Build

- Command: `go build ./internal/... ./cmd/...`
- Full build: `make build`
- Common failures:
  - Missing sibling repos — clone them as siblings per `go.mod` replace directives
  - `go mod tidy` breaks on `pkg/` — use `go mod tidy -e`

Always scope go commands to `./internal/... ./cmd/...` to skip broken `pkg/`.

## Typecheck

- Command: `go vet ./internal/... ./cmd/...`

## Lint & format

No linter config or pre-commit hooks. CI does not lint.

- Lint: `golangci-lint run ./internal/... ./cmd/...` (optional)
- Format check: `gofmt -l ./internal ./cmd`
- Auto-fix: `gofmt -w ./internal ./cmd && goimports -w ./internal ./cmd`

## Unit tests

- Run all: `GOEXPERIMENT=jsonv2 go test ./internal/... ./cmd/...`
- Run subset: `GOEXPERIMENT=jsonv2 go test ./internal/lead/ -run TestReassign`
- Framework: stdlib `testing` + `testify/require`
- Mocking: Mockery v2, in-package, `with-expecter: true`. Regenerate: `make mocks`
- Fixtures: `platform.NewMock(t)` for the mock bag. SQLite in-memory DB via `newTestDB`.

`GOEXPERIMENT=jsonv2` is required — without it 44+ tests fail.

## Integration / E2E tests

None exist.

## Run locally

- Command: `./start_container.sh` (or `--rebuild`)
- URL: `https://l.ezoic.com:9098` (via `/etc/hosts`, not `localhost`)
- Ports: API `:9098`, Delve `:40000`
- Env overrides: `FUNNELJAM_` prefix, double underscores = dots (`FUNNELJAM_LOGGING__LEVEL=DEBUG`)
- Health check: `curl -k https://l.ezoic.com:9098/ping`
- Prerequisites: Docker, `~/sniper-ssl/` certs, `~/.aws/` credentials, sibling repos, `/etc/hosts` entry

## Authentication

- Header: `X-Api-Key`
- Get the key:
  ```bash
  KEY=$(aws secretsmanager get-secret-value \
    --secret-id "sales/funneljam/api" \
    --query SecretString --output text)
  ```

## API smoke tests

All require `-k` for self-signed TLS.

| Endpoint | Method | Auth | Test request | Expected |
|---|---|---|---|---|
| `/ping` | GET | none | `curl -k https://l.ezoic.com:9098/ping` | 200 |
| `/docs/swagger.yaml` | GET | none | `curl -k https://l.ezoic.com:9098/docs/swagger.yaml` | 200 + YAML |
| `/leads` | GET | API key | `curl -k -H "X-Api-Key: $KEY" "https://l.ezoic.com:9098/leads?limit=1"` | 200 + JSON |
| `/accounts` | GET | API key | `curl -k -H "X-Api-Key: $KEY" "https://l.ezoic.com:9098/accounts"` | 200 + JSON |
| `/prospects` | POST | API key | `curl -k -X POST -H "X-Api-Key: $KEY" -H "Content-Type: application/json" -d '{"limit":1}' "https://l.ezoic.com:9098/prospects/search"` | 200 + JSON |

**Skip** (side effects): `/mail/*`, `/notifications` POST, `/connect`, `/pull`

## Frontend validation

Frontend is in `funneljam-dashboard` (`~/ezoicgit/funneljam-dashboard`), runs on `https://l.ezoic.com:5173`. Skip if only changing backend.

| Page | URL | Login | What to verify |
|---|---|---|---|
| Dashboard | `https://l.ezoic.com:5173/` | yes | Sidebar, stats cards |
| Leads | `https://l.ezoic.com:5173/leads` | yes | Table with rows |
| Automations | `https://l.ezoic.com:5173/automations` | yes | List renders |
| Settings | `https://l.ezoic.com:5173/settings` | yes | Form renders |

Login: navigate to `/`, app redirects to Ezoic login. Ask user to authenticate first.

## Smoke test checklist

1. `go build ./internal/... ./cmd/...`
2. `GOEXPERIMENT=jsonv2 go test ./internal/... ./cmd/...`
3. `./start_container.sh` — starts, Air builds, Delve listens
4. `curl -k https://l.ezoic.com:9098/ping` — 200
5. Hit 2-3 authenticated endpoints from the table
6. If frontend changed, open dashboard pages in browser

## Debug

- Delve on `:40000`, `--continue` flag (API starts without attaching)
- Logs: `log/slog` JSON to stdout. `FUNNELJAM_LOGGING__FORMAT=text` for readable, `FUNNELJAM_LOGGING__LEVEL=DEBUG` for verbose
- Build errors: `tmp/build-errors.log`

## CI

- AWS CodeBuild, project `funneljam--master`
- Steps: GOPATH setup, dependency resolution, test, build binaries, Docker build, ECR push
- Deploy: `user-deploy-backend` MCP with `directory: "funneljam"`
