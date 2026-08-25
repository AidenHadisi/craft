

<One paragraph describing the feature: current state, the gap, what we're adding, and what done looks like. Note explicit exclusions here if any.>

## Requirements

<One requirement per bullet, one or two sentences each: the outcome or constraint, not the design that satisfies it — design details live in the steps. If a bullet needs sub-bullets or an em-dash chain, it is several requirements; split it.>

- <…>
- <…>

## Architecture

<The agreed design, kept high-level: the capabilities the feature needs, the components that own them, the seams between them (what crosses, which way it flows), and key decisions with a one-line why. Keep it current if a step changes the design.>

## Conventions

<Pasted verbatim into every coder brief. Each entry names one repo-specific convention and the exemplar file to mirror. Cover errors, naming, tests, and layout as applicable.>

-  — mirror `<path>`



## Steps

<Starts as the provisional outline: one `- [ ] **Step N — <name>**` heading per anticipated step, in dependency order, names only. Each is then filled in with its full design during the loop. Split, merge, rename, and reorder undesigned headings freely as design work teaches you more.>

- [ ] **Step 1 —**

<The one job this component owns, in a sentence or two.>

<Sub-steps numbered 1.1, 1.2, … — one piece of the work each. Each explains what it does, pins the contracts it defines (signatures, endpoints, wire shapes, errors), and its edge and error paths. One fact or decision per line, split — never chained with em-dashes or parentheticals. Pseudocode for logic, code blocks for contracts, tables for enumerables, terse bullets for facts; prose only where it's the clearest form, max three sentences in a row. Rationale, when needed, is one short *Why:* line under the decision. No extra headings. Complete but concise — every line carries a fact or decision.>

**Tests:**

- `<path>_test.<ext>` — <one named behavior per bullet, one line each; each asserts an observable outcome — never several behaviors semicolon-joined into one bullet>



## Verification

Automated:

- `<build / typecheck / lint command>`
- `<test command>`

Manual:

- <human check, if any>
