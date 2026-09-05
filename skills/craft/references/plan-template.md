# Plan: <Feature name>

## What we're building

<One or two paragraphs: current state, the gap, what we're adding, and what done looks like.>

## Requirements

- <Observable requirement>
- <…>

## Out of scope

- <Explicit exclusion — with a brief reason if non-obvious>
- <…>

## Approach

<Short description of the chosen design: seams, ownership, data flow, how it fits the repo.>

## Conventions

- <Repo-specific conventions that implementers must follow for this feature — errors, stores, HTTP, tests, frontend layout, etc.>

## User actions

- [ ] **<Action title>**

```
<Literal command, SQL, or instructions the user must run before implementation>
```

## Changes

- [ ] **Task 1 — <Name>**

<What this Task delivers, in plain language.>

**<N.M> — <Step title>** · `<path>` · create|edit

<Detail a junior can follow for clean, reliable results: named contracts (signatures, endpoints, wire shapes, errors, props) and brief pseudocode when behavior is non-obvious — not a line-by-line walkthrough.>

## Tests

- [`<path>_test.<ext>`](<path>_test.<ext>)
  - <One behavior per bullet; each asserts an observable oracle>
  - <…>

## Verification

- `<build / typecheck / lint command>`
- `<test command>`

## Progress

<Phase tracker — check off as each completes. Task-level progress lives in the Changes checkboxes.>

- [ ] Plan approved
- [ ] User actions done
- [ ] All Tasks implemented and reviewed
- [ ] Polished
- [ ] Verification green
- [ ] Live-tested
