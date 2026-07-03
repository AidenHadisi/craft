# Plan: Saved searches

## Goal

Users who rely on the same filtered views rebuild them by hand every visit; there's no way to keep a query around. Let a signed-in user save the current search under a name, see their saved searches, run one with a single click, and delete ones they no longer need.

Requirements:
- Saving captures the full query (text + filters) with a user-chosen name.
- Names are required and trimmed; saving an existing name replaces that entry.
- A user only ever sees and modifies their own saved searches.
- Persists across sessions and devices.

## Out of scope

- Sharing saved searches between users — no requirement today.
- Renaming a saved search — save under the new name and delete the old one.

## Approach

A thin vertical slice: a store for saved-search rows, REST endpoints scoped to the authenticated user, and a small list component. Upsert on (user_id, name) so saving a duplicate name replaces the query.

## Conventions

- Errors: wrap with `fmt.Errorf("...: %w", err)`; sentinel errors in the package that owns them.
- Stores are structs over `pgxpool.Pool`; consumers declare the interface they need locally.
- HTTP handlers use the shared `writeJSON` / `writeError` helpers; camelCase JSON everywhere.
- Tests: table-driven with `t.Run`; hand-rolled fakes, no mock library.
- Frontend: fetch wrappers live in `web/src/api/`, one module per resource.

## Contracts

- Store (Task 1, consumed by Task 2): `List(ctx, userID) ([]SavedSearch, error)` newest first · `Upsert(ctx, userID, name string, query json.RawMessage) (SavedSearch, error)` · `Delete(ctx, userID, id int64) error` scoped by userID.
- Routes (Task 2, consumed by Task 3): GET/POST `/api/saved-searches`, DELETE `/api/saved-searches/{id}` — camelCase JSON.

## Changes

### Task 1 — Storage   (depends on: none)

A table and a store that owns all saved-search persistence.

**Done when:** the store round-trips a row per the contract, and re-upserting a name replaces its query.

**1.1 — Create the `saved_searches` table.**
· manual

- Columns: id, user_id, name, query jsonb, timestamps; unique index on (user_id, name).

**1.2 — Build the store with List, Upsert, and Delete.**
`internal/savedsearch/store.go` · create

- Upsert in one statement: `INSERT ... ON CONFLICT (user_id, name) DO UPDATE`.

### Task 2 — HTTP API   (depends on: Task 1)

Authenticated REST endpoints exposing the store.

**Done when:** `GET /api/saved-searches` returns only the caller's rows, newest first; a blank name gets 400 without touching the store.

**2.1 — Add the saved-searches handler with List/Save/Delete.**
`internal/httpapi/saved_searches.go` · create

- Declares the store interface it needs locally.
- Rejects blank/whitespace names with 400 before any store call; trims names.

**2.2 — Register the routes in the authenticated group.**
`internal/httpapi/router.go` · edit

- Inside the existing requireAuth group.

### Task 3 — Frontend   (depends on: Task 2)

The saved-searches list in the search page, backed by a typed API module.

**Done when:** the list loads on mount, clicking an entry runs its search, and delete removes it inline.

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
