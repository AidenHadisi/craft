## Standards

These standards bind everyone who writes or reviews the spec. The spec is the contract; it says what and why, never how.

### Shape

Write the feature contract in `.craft/<feature>/spec.md`. Use a concise, scannable list with headings that fit the feature. Include:

- Observable behaviors (happy path, error cases, and edge cases).
- Stable, useful requirement IDs, such as `REQ-1`, that can be referenced by implementation and testing documents.
- Explicit out-of-scope exclusions.

### What a good spec is

- **A short, clear list:** Short, readable bullets. Avoid dense paragraphs or unnecessary bureaucratic sections.
- **Observable behavior:** Every requirement is something a user, caller, or test can see or verify — never an implementation detail, file path, component, or library choice.
- **Stable identifiers:** Give each requirement an ID. Keep it when wording changes without changing meaning; retire it only when the requirement is removed or split, and record material changes in `progress.md`.
- **Unambiguous:** Two implementers would build the same behavior. Avoid hand-waving words like "should", "fast", "simple", "user-friendly", or "etc."
- **Failures and edge cases specified:** State behavior for invalid inputs, missing data, empty states, and errors when relevant.
- **Preserves existing behavior:** Existing behavior is maintained unless a requirement explicitly specifies a change.
- **Testable:** Every requirement can be tested or verified in this repo.
- **Holds user intent:** Capture what the user asked for without adding unrequested extras. Scope creep is a defect.

## Write and review

Write the spec in `spec.md`, starting from [`../assets/templates/spec.md`](../assets/templates/spec.md). Adapt its shape to the feature while preserving the contract above; there is no required schema or fixed heading layout.

If `craft-reviewer` sends the spec back, rule on each point in `progress.md`: **Adopt** when it sharpens or corrects the spec without losing user intent; **Reject** with a reason when it does not. Rewrite the spec for adopted points; do not append reviewer replies as a competing spec.
