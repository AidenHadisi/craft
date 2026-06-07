# Implementation plan template

Use this to write `docs/plans/<feature>.md`. The plan is the source of truth a `craft-coder` implements verbatim, so it must be exact — and it should also be a pleasant, well-formatted document.

## The fidelity bar

- **Complete and literal.** Every step gives the full file content or the full block to insert — imports, types, error handling, edge cases. No `// ...`, no "implement X here", no TODOs. A coder reproduces it with zero invention.
- **Matches the repo.** Mirror existing conventions, import style, naming, and error handling found during exploration. Use the target runtime version's idioms.
- **Idiomatic and clean.** Apply the architect's design: deep modules, linear flow with early returns, no pointless tiny wrappers, popular libraries over hand-rolled utilities, names that carry meaning.
- **Comments explain *why* only** — invariants, trade-offs, external constraints. No narration, no banner separators, no section-label comments.

## Make it beautiful

Use markdown features so the plan reads cleanly:

- **Headers / subheaders** to structure steps and group related work.
- **Fenced code blocks** with a language tag for every code segment.
- **Links to files** — reference the spec and touched files as markdown links, e.g. `[src/auth/session.ts](src/auth/session.ts)`.
- **Tables** for the file-ownership groups and for any structured comparison.
- **Checklists** for verification commands.
- Inline `code` for symbols, paths, and commands.

## File-ownership groups

So coders can run in parallel without conflicts:

- Partition steps into **groups**, each owning a disjoint set of files.
- Note dependencies (Group B needs Group A's module to exist).
- Independent groups run in parallel; dependent groups run in later waves.

## Structure

```markdown
# Implementation Plan: <feature>

> Spec: [docs/specs/<feature>.md](docs/specs/<feature>.md)

## Design summary

The architect's design — approach, module map, boundaries, data flow, libraries, test seams.

## File-ownership groups

| Group | Owns | Depends on | Steps |
|---|---|---|---|
| A (parallel-safe) | `path1`, `path2` | none | 1-3 |
| B | `path3` | A | 4-5 |

## Steps

### Step 1 — <short title>

`target/path` · create | edit · **Why:** one line.

\`\`\`<lang>
<complete literal code>
\`\`\`

### Step 2 — ...

## Verification

- [ ] `<build/typecheck command>` → passes
- [ ] `<lint command>` → passes
- [ ] `<test command>` → passes

New tests are written as their own steps above, with full code.
```
