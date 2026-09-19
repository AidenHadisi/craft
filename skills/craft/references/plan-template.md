# <Feature name>

## Summary

<one or two paragraphs: current state, the gap, what we add, what done looks like>

## Criteria

- <observable behavior a live test can prove>

## Out of scope

- <exclusion> — <reason when non-obvious>

## Findings

Facts about this repo: paths, current behavior, siblings, conventions, packages present, and things checked and found absent. Later entries win over earlier ones.

- <fact, with the path or command that shows it>

## Architecture

### Components

- **<name>** — <the one job it owns>. Files: `<path>`, `<path>`. Mirrors `<sibling path>` when there is one.

### Seams

- <from> → <to>: <what crosses>

### Key decisions

- <decision> — <why, one line>

## Steps

Starts as a heading-only outline: one `### N. <short title>` per anticipated step, in dependency order, no design yet. Split, merge, rename, and reorder undesigned headings freely as design work teaches you more. Each heading is then filled in using the format below. Keep the Progress section's step list in sync with these headings.

### 1. <short title>

<One sentence: what this step delivers and which component(s) it builds.>

1.1 <One piece of the work: what it does, in which file.>

```ts
<the contract it pins — signature, endpoint, wire shape, error — when a later step depends on it>
```

1.2 <Next piece, including its edge and error paths.>

**Criteria:**

- <observable behavior a branch review can check in the diff or a tester can run>

**Tests:**

- <one named behavior, one line, asserting one observable outcome>

## Rulings

Append-only. One line per reviewer point.

- <point> · Adopt | Reject · <reason>

## Conventions

- <Repo-specific convention implementers must follow — errors, naming, tests, layout as applicable> — exemplar: `<path>`

## Verification

Automated:

- `<build / typecheck / lint command>`
- `<test command>`

Manual:

- [human check, if any]

## Progress

The only progress tracker. Check off as each completes. One line per step, mirroring the Steps headings; a step is checked when its coder reports done, never earlier.

- [ ] Spec approved
- [ ] Plan approved
- [ ] Step 1 — <one sentence description of the step>
- [ ] Code review passed
- [ ] Polished
- [ ] Verification green
- [ ] Live-tested
