# <Feature name>

## What we're building

<One or two paragraphs: current state, the gap, what we're adding, and what done looks like.>

## Requirements

- <Observable requirement>
- <…>

## Out of scope

- <Explicit exclusion — with a brief reason if non-obvious>
- <…>

## Acceptance criteria

<The definition of done. Frozen after the user confirms. A box is checked only with evidence from a live run.>

- [ ] <Observable criterion> — proof: <request / page / command and the expected observable result>
- [ ] <…>

## Architecture

<The agreed design: components and the one job each owns, the seams between them (what crosses, which way it flows), and key decisions with a one-line why. This section keeps slices converging — keep it current when a slice changes the design.>

## Dossier

<Evidence for critics and coders, gathered by legwork agents; extend it when a critic reports missing evidence.>

- **Sibling features:** <`path` — how it does the comparable thing, with the relevant excerpt>
- **Conventions:** <convention implementers must follow — errors, stores, HTTP, tests, frontend layout> — exemplar: `<path>`
- **Already available:** <what the stdlib and current dependencies provide for this problem>
- **Worth considering:** <well-maintained packages, with what each would replace>

## Verification

- `<build / typecheck / lint command>`
- `<test command>`

## Live test

<How to start the dev environment, how to reach it (URL, port, credentials, test account), and which side effects to stub. Written before any code, refined as slices land.>

## Design rulings

<Append-only. One line per rival design and per risk a critic raised.>

- <lens> · Adopt | Reject · <reason>

## Slice log

<Append-only. An entry opens at design time with its criteria and is checked at commit. If stopped, the last entry records the blocker.>

- [x] **Slice 1 — <Name>** · `<commit sha>`
  - Criteria: <2–5 observable criteria, frozen at design>
  - Proven: <what was run and what was observed — or why nothing was runnable yet>
