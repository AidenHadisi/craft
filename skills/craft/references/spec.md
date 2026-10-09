## Standards

These standards bind everyone who writes or reviews the spec. The spec is the contract; it says what and why, never how.

### Shape

A clean, short list of bullet items under `## Spec` in the plan:
- What the feature does and observable behaviors (happy path, error cases, edge cases)
- Explicit out-of-scope exclusions (as bullet items, e.g. `- Out of scope: ...`)

### What a good spec is

- **A short, clear list:** Short, readable bullet items. Avoid dense paragraphs or unnecessary bureaucratic sections.
- **Observable behavior:** Every item is an observable behavior — what a user, caller, or test can see or verify — never an implementation detail, file path, component, or library choice (those belong in architecture and steps).
- **Two implementers would build the same thing from it:** Precise and unambiguous. No hand-waving words like "should", "fast", "simple", "user-friendly", or "etc."
- **Failures and edge cases specified:** Clear behavior for invalid inputs, missing data, empty states, and errors.
- **Preserves existing behavior:** Existing behavior is maintained unless a spec item explicitly specifies a change.
- **Testable:** Every item can be tested or verified in this repo.
- **Holds user intent:** Captures what the user asked for without adding unrequested extras. Scope creep is a defect.

## Write

Write the spec directly as bullet items under `## Spec` in the plan file. Keep it concise and scannable.

If `craft-reviewer` sends the spec back, rule on each point under `## Notes` in the plan: **Adopt** when it sharpens or corrects the spec without losing user intent; **Reject** with a reason when it does not. Rewrite the spec list for adopted points; do not append replies.
