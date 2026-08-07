# Plan: Saved searches

## What we're building

The search page already supports free-text queries plus filters, but nothing about a query survives navigation — users who return to the same filtered view several times a day rebuild it by hand every visit. We're adding saved searches: a signed-in user gives the current query a name and saves it, and that name joins a list of their other saved searches. Picking one re-runs it and restores the search box and filters exactly as they were; one they no longer want can be deleted from the same list. Saved searches are private to the user who created them and persist across sessions and devices, so the same list is waiting on a laptop and a phone. Saving under a name that already exists overwrites that entry rather than creating a second one with the same label. Done means a user can save, list, run, and delete their own searches from the UI, backed by REST endpoints scoped to the authenticated user.

## Pacing

**All at once** — after plan approval, implement Tasks in dependency waves without per-Task user gates.

## Requirements

- Saving captures the full query (text + filters) with a user-chosen name.
- Names are required and trimmed; saving an existing name replaces that entry.
- A user only ever sees and modifies their own saved searches.
- Persists across sessions and devices.

## Out of scope

- Sharing saved searches between users — no requirement today.
- Renaming a saved search — save under the new name and delete the old one.

## Approach

A thin vertical slice: a store for saved-search rows, REST endpoints scoped to the authenticated user, and a small list component. Upsert on `(user_id, name)` so saving a duplicate name replaces the query.

## Conventions

- Errors: wrap with `fmt.Errorf("...: %w", err)`; sentinel errors in the package that owns them.
- Stores are structs over `pgxpool.Pool`; consumers declare the interface they need locally.
- HTTP handlers use the shared `writeJSON` / `writeError` helpers; camelCase JSON everywhere.
- Tests: table-driven with `t.Run`; hand-rolled fakes, no mock library.
- Frontend: fetch wrappers live in `web/src/api/`, one module per resource.

## Changes

- [ ] **Task 1 — Storage**

  Saved searches persist per user. Saving under a name that already exists updates that row's query instead of creating a duplicate.

  - **1.1** Ask the user to create the `saved_searches` table

    ```sql
    CREATE TABLE saved_searches (
    	id         bigserial   PRIMARY KEY,
    	user_id    bigint      NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    	name       text        NOT NULL,
    	query      jsonb       NOT NULL,
    	created_at timestamptz NOT NULL DEFAULT now(),
    	updated_at timestamptz NOT NULL DEFAULT now()
    );

    CREATE UNIQUE INDEX saved_searches_user_id_name_idx ON saved_searches (user_id, name);
    ```

  - **1.2** Store over the new table · `internal/savedsearch/store.go` · create
    - `List(ctx, userID int64) ([]SavedSearch, error)` — newest `updated_at` first.
    - `Upsert(ctx, userID int64, name string, query json.RawMessage) (SavedSearch, error)` — a single `INSERT ... ON CONFLICT (user_id, name) DO UPDATE`, so a repeated name replaces the query.
    - `Delete(ctx, userID, id int64) error` — scoped by `user_id`; no matching row returns `ErrNotFound`.
    - `SavedSearch` carries the table's columns; `ErrNotFound` is defined here.

- [ ] **Task 2 — HTTP API**

  Authenticated users list, save, and delete only their own searches. Blank names are rejected before anything is persisted.

  - **2.1** Saved-searches handler · `internal/httpapi/saved_searches.go` · create
    - `GET /api/saved-searches` → 200, `[{ id, name, query, updatedAt }]` newest first.
    - `POST /api/saved-searches`, body `{ name, query }` → 201 with the saved row.
    - `DELETE /api/saved-searches/{id}` → 204; `ErrNotFound` → 404.
    - Name is trimmed; blank or whitespace-only → 400 before any store call.
    - User ID always comes from the request context, never the body.
  - **2.2** Register the routes in the existing `requireAuth` group · `internal/httpapi/router.go` · edit

- [ ] **Task 3 — Frontend**

  Users see their saved searches, run one with a click, and delete one inline without a page reload.

  - **3.1** Fetch wrappers · `web/src/api/savedSearches.ts` · create
    - `listSavedSearches()`, `saveSearch(name, query)`, `deleteSavedSearch(id)` over the Task 2 endpoints, with a `SavedSearch` type mirroring the wire shape.
  - **3.2** Saved-search list · `web/src/components/SavedSearchList.tsx` · create
    - Takes an `onRun(query)` prop; picking a row calls it with that saved query.
    - Each row shows the name and when it was last updated, with an inline delete.
    - Empty state invites the user to save their first search.

## Tests

- [internal/httpapi/saved_searches_test.go](internal/httpapi/saved_searches_test.go) — table-driven with a hand-rolled fake store.
  - Saving a valid name returns 201 with the stored row.
  - A blank or whitespace-only name returns 400 and never reaches the store.
  - The name arrives at `Upsert` trimmed.
  - A store failure surfaces as 500.
  - Deleting a row owned by another user returns 404.

### Not tested

- Persistence behavior against a real database — the repo has no DB test harness; handler tests cover the store contract with its established fake style.

## Verification

- `go build ./... && go vet ./...`
- `go test ./internal/...`
- `cd web && npm run typecheck && npm run lint`
