# Example Quick Plan

A complete worked example of a quick-mode plan (`docs/plans/<feature>.md`). The level: since there is no spec file, the `## Goal` section carries the problem and requirements — a short paragraph plus requirement bullets, lighter than a spec but enough that the plan stands alone. The `## Conventions` section captures the repo's idioms from exploration and is pasted verbatim into every coder dispatch.

The plan reads top-down: each Task opens with one sentence on what it delivers, and each subtask is a bolded one-sentence headline saying WHAT, with the file and action on a quiet line below. Detail bullets appear under a subtask only where the coder would otherwise guess wrong — a signature, an endpoint, a tricky rule. Most subtasks have none. HOW is the coder's job.

---

# Plan: Saved searches

## Goal

Users who rely on the same filtered views rebuild them by hand every visit; there's no way to keep a query around. Let a signed-in user save the current search under a name, see their saved searches, run one with a single click, and delete ones they no longer need.

Requirements:
- Saving captures the full query (text + filters) with a user-chosen name.
- Names are required and trimmed; saving an existing name replaces that entry.
- A user only ever sees and modifies their own saved searches.
- Persists across sessions and devices.

## Approach

A thin vertical slice: a store for saved-search rows, REST endpoints scoped to the authenticated user, and a small list component. Upsert on (user_id, name) so saving a duplicate name replaces the query.

## Conventions

- Errors: wrap with `fmt.Errorf("...: %w", err)`; sentinel errors in the package that owns them.
- Stores are structs over `pgxpool.Pool`; consumers declare the interface they need locally.
- HTTP handlers use the shared `writeJSON` / `writeError` helpers; camelCase JSON everywhere.
- Tests: table-driven with `t.Run`; hand-rolled fakes, no mock library.
- Frontend: fetch wrappers live in `web/src/api/`, one module per resource.

## Changes

### Task 1 — Storage   (depends on: none)

A table and a store that owns all saved-search persistence.

**1.1 — Create the `saved_searches` table.**
· manual

- Columns: id, user_id, name, query jsonb, timestamps; unique index on (user_id, name).

**1.2 — Build the store with List, Upsert, and Delete.**
`internal/savedsearch/store.go` · create

- Contract: `List(ctx, userID) ([]SavedSearch, error)` newest first, `Upsert(ctx, userID, name string, query json.RawMessage) (SavedSearch, error)`, `Delete(ctx, userID, id int64) error` scoped by userID.
- Upsert in one statement: `INSERT ... ON CONFLICT (user_id, name) DO UPDATE`.

### Task 2 — HTTP API   (depends on: Task 1)

Authenticated REST endpoints exposing the store.

**2.1 — Add the saved-searches handler with List/Save/Delete.**
`internal/httpapi/saved_searches.go` · create

- Declares the store interface it needs locally.
- Rejects blank/whitespace names with 400 before any store call; trims names.

**2.2 — Register the routes in the authenticated group.**
`internal/httpapi/router.go` · edit

- GET/POST `/api/saved-searches` and DELETE `/api/saved-searches/{id}`, inside requireAuth.

### Task 3 — Frontend   (depends on: Task 2)

The saved-searches list in the search page, backed by a typed API module.

**3.1 — Add typed list/save/delete fetch wrappers.**
`web/src/api/savedSearches.ts` · create

**3.2 — Build the saved-search list component.**
`web/src/components/SavedSearchList.tsx` · create

- Loads on mount, runs a search on click via an `onRun` prop, deletes inline.

## Tests

- [internal/httpapi/saved_searches_test.go](internal/httpapi/saved_searches_test.go) — valid save returns 201; blank name 400 with no store call; name trimmed; store failure surfaces as 500. Table-driven with a hand-rolled fake store.

## Verification

- `go build ./... && go vet ./...`
- `go test ./internal/...`
- `cd web && npm run typecheck && npm run lint`
- Live: `make dev` then `curl -s localhost:8080/api/saved-searches -H "Authorization: Bearer $(grep API_TOKEN .env | cut -d= -f2)"` — expect 200 and camelCase JSON
- Live: save, re-save the same name, delete via curl; verify the list reflects each step
- Live (browser): open /search, save a search, see it in the list, run it, delete it
