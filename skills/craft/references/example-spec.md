# Saved searches

## Summary
Saved searches let a signed-in user name and store a search query so they can re-run it later with one click instead of re-typing filters. It's for power users who run the same searches repeatedly across sessions.

## Problem
Users who rely on the same filtered views (e.g. "open tickets assigned to me, sorted by priority") have to rebuild those filters by hand every visit. There's no way to keep a query around, so repeat work is slow and error-prone, and people fall back to bookmarking fragile URLs that break when filters change.

## Goals
- A user can save the current search with a name they choose.
- A user can see their saved searches and run one with a single action.
- A user can rename and delete their saved searches.
- Saved searches persist across sessions and devices for that user.

## Non-goals
- Sharing saved searches with other users or teams.
- Scheduling or alerting when a saved search gets new results.
- Saving searches for signed-out (anonymous) visitors.

## User stories
1. As a signed-in user, I want to save my current search with a name, so that I can return to it later without rebuilding filters.
2. As a signed-in user, I want to see a list of my saved searches, so that I can pick one to run.
3. As a signed-in user, I want to rename a saved search, so that its label stays meaningful as my needs change.
4. As a signed-in user, I want to delete a saved search I no longer use, so that my list stays uncluttered.

## Requirements
### Functional
- Saving captures the full query (search text and all active filters) and a user-supplied name.
- A user sees only their own saved searches, most recently created first.
- Running a saved search restores the exact query that was saved.
- Names are required and trimmed; an empty or whitespace-only name is rejected.
- A user can have at most one saved search with a given name; saving a duplicate name updates the existing one.
- Deleting a saved search is immediate and removes it from the list.

### Non-functional
- A user can only read, rename, or delete saved searches they own; cross-user access is denied.
- The saved-search list loads fast enough to feel instant for a typical user (tens of saved searches).
- A saved query is stored as structured data, not a raw URL, so it survives changes to URL formatting.

## Key scenarios
- **Save a new search.** The user applies filters, opens the save control, types a name, and confirms. The search appears at the top of their list.
- **Save over an existing name.** The user saves with a name that already exists in their list; the stored query for that name is replaced, and no duplicate entry is created.
- **Run a saved search.** The user selects an entry; the app restores its query and shows the matching results.
- **Empty name.** The user tries to save with a blank name; the app rejects it and explains why, without creating an entry.
- **Delete.** The user deletes an entry; it disappears immediately and is gone on the next visit.
- **Another user's entry.** A request to read or modify a saved search that belongs to someone else is denied.

## Open questions
- (none — resolved)
