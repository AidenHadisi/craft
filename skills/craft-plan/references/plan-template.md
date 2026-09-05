

<One short paragraph describing the feature: current state, the gap, what we're adding, and what done looks like. Note explicit exclusions here if any.>

## Requirements

- <One requirement per bullet, one or two sentences each: the outcome or constraint, not the design that satisfies it — design details live in the steps.>


## Architecture

<The agreed design, kept high-level: the capabilities the feature needs, the components that own them, the seams between them (what crosses, which way it flows), and key decisions with a one-line why. Keep it current if a step changes the design.>

## Conventions

- <Pasted verbatim into every coder brief. Each entry names one repo-specific convention and the exemplar file to mirror. Cover errors, naming, tests, and layout as applicable.>

## Steps

<Heading-only placeholders first, filled in one at a time during the loop.>

- [ ] **Step 1 — <one sentence description of the step>**

<Sub-steps numbered 1.1, 1.2, … — one piece of the work each: what it does, the contracts it defines (signatures, endpoints, wire shapes, errors), and its edge and error paths. No extra headings.>

**Tests:**

- <one named behavior per bullet, one line each; each asserts an observable outcome>


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
