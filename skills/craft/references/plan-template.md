

<A concise paragraph describing the feature and what we are building>

## Requirements

- <One requirement per bullet>


## Architecture

<The agreed design, kept high-level.>

## Conventions

- <Pasted verbatim into every coder brief. Repo-specific convention and the exemplar file to mirror.>

## Steps

<Starts as a provisional outline: one heading per anticipated step — `- [ ] **Step N — <one sentence description>**` — in dependency order, no design yet. Each step is one smallest standalone component: a schema, a small package, an endpoint. Split, merge, rename, and reorder undesigned headings freely as design work teaches you more. Each heading is then filled in during the loop using the format below. Checkboxes track implementation only — an approved step stays unchecked until its code review passes.>

- [ ] **Step 1 — <one sentence description of the step>**

<Sub-steps numbered 1.1, 1.2, … — one piece of the work each: what it does, the contracts it pins (signatures, endpoints, wire shapes, errors), its edge and error paths, and pseudocode for every non-trivial path. No extra headings:
- One fact or decision per line
- Pseudocode for logic
- Code blocks for contracts
- Tables for anything enumerable (rules, fields, endpoints, config keys, error cases)
- Terse bullets for facts
- Prose only where it is genuinely the clearest form>

## Tests

- <one bullet point naming each test case>


## Verification

Automated:

- `<build / typecheck / lint command>`
- `<test command>`

Manual:

- <human check, if any>

## Progress

<Phase tracker — check off as each completes. Step-level progress lives in the Steps checkboxes.>

- [ ] Plan approved
- [ ] All steps implemented and reviewed
- [ ] Polished
- [ ] Verification green
- [ ] Live-tested
