

<One paragraph describing the feature: current state, the gap, what we're adding, and what done looks like. Note explicit exclusions here if any.>

## Requirements

- <…>
- <…>

## Architecture

<The agreed design, kept high-level: the capabilities the feature needs, the components that own them, the seams between them (what crosses, which way it flows), and key decisions with a one-line why. Keep it current if a step changes the design.>

## Conventions

<Pasted verbatim into every coder brief. Each entry names one repo-specific convention and the exemplar file to mirror. Cover errors, naming, tests, and layout as applicable.>

-  — mirror `<path>`



## Steps

<Appended one at a time during the loop, in the order they are designed.>

- [ ] **Step 1 —**

<The one job this component owns, in a sentence or two.>

<Sub-steps numbered 1.1, 1.2, … — one piece of the work each. Each explains what it does, pins the contracts it defines (signatures, endpoints, wire shapes, errors), and its edge and error paths. Written dense: pseudocode for logic, signatures for contracts, terse bullets for facts, prose only where it's the clearest form. No extra headings. Complete but concise — every line carries a fact or decision.>

**Tests:**

- `<path>_test.<ext>` — <one behavior per bullet; each asserts an observable outcome>



## Verification

Automated:

- `<build / typecheck / lint command>`
- `<test command>`

Manual:

- <human check, if any>
