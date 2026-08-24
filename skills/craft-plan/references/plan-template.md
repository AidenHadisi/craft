# <Name>

<One paragraph describing the feature: current state, the gap, what we're adding, and what done looks like. Note explicit exclusions here if any.>

## Requirements

- <…>
- <…>

## Architecture

<The agreed design, kept high-level: the capabilities the feature needs, the components that own them, the seams between them (what crosses, which way it flows), and key decisions with a one-line why. Keep it current if a step changes the design.>

## Conventions

<Pasted verbatim into every coder brief. Each entry names one repo-specific convention and the exemplar file to mirror. Cover errors, naming, tests, and layout as applicable.>

- <Convention> — mirror `<path>`

## Steps

<Appended one at a time during the loop, in the order they are designed.>

- [ ] **Step 1 — <name>**

<The one job this component owns, in a sentence or two.>

<Numbered sub-steps. Each describes one piece of the work in detail — the files it touches, the contracts it pins (signatures, endpoints, wire shapes, errors), and its edge and error paths — with pseudocode wherever the logic is non-trivial. No extra headings; the precision lives in the prose.>

**Tests:**

- `<path>_test.<ext>` — <one behavior per bullet; each asserts an observable outcome>

## Verification

Automated:

- `<build / typecheck / lint command>`
- `<test command>`

Manual:

- <human check, if any>
