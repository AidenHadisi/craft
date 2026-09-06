

[One short paragraph describing the feature: current state, the gap, what we're adding, and what done looks like. Note explicit exclusions here if any.]

## Requirements

- [One requirement per bullet, one or two sentences each: the outcome or constraint, not the design that satisfies it — design details live in the steps.]


## Architecture

[The agreed design, kept high-level: the capabilities the feature needs, the components that own them, the seams between them (what crosses, which way it flows), and key decisions with a one-line why. Keep it current if a step changes the design.]

## Conventions

- [Pasted verbatim into every coder brief. Each entry names one repo-specific convention and the exemplar file to mirror. Cover errors, naming, tests, and layout as applicable.]

## Steps

[Starts as a provisional outline: one `### Step N — <one sentence description>` heading per anticipated step, in dependency order, no design yet. Each step is one smallest standalone component: a schema, a small package, an endpoint. Split, merge, rename, and reorder undesigned headings freely as design work teaches you more. Each heading is then filled in during the loop using the format below. Keep the Progress section's step list in sync with these headings.]

### Step 1 — <one sentence description of the step>

[Sub-steps numbered 1.1, 1.2, … — one piece of the work each: what it does, the contracts it pins (signatures, endpoints, wire shapes, errors), its edge and error paths, and pseudocode for every non-trivial path. No extra headings. The step has two readers — a coder who needs every detail and a user verifying each decision in one quick read:
- One fact or decision per line — never several chained into one sentence with em-dashes, semicolons, or nested parentheticals; split so each can be verified alone.
- Pseudocode for logic; code blocks for contracts; tables for anything enumerable (rules, fields, endpoints, config keys, error cases); terse bullets for facts; prose only where it is genuinely the clearest form.
- Cut words, never information — every line carries a fact or decision the implementer needs.]

**Tests:**

- [one named behavior per bullet, one line each; each asserts an observable outcome — never several behaviors joined into one bullet]


## Verification

Automated:

- `<build / typecheck / lint command>`
- `<test command>`

Manual:

- [human check, if any]

## Progress

[The only progress tracker. Check off as each completes. One line per step, mirroring the Steps headings; a step is checked when its code review passes, never earlier.]

- [ ] Plan approved
- [ ] Step 1 — <one sentence description of the step>
- [ ] Step 2 — <one sentence description of the step>
- [ ] Polished
- [ ] Verification green
- [ ] Live-tested
