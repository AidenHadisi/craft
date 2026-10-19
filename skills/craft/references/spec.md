## Standards

These standards bind everyone who writes or reviews the spec. The spec is the contract; it says what and why, never how. Follow the document shape in `SKILL.md`.

### What a good spec is

- **A short, clear list:** Short, readable bullets. Avoid dense paragraphs or unnecessary bureaucratic sections.
- **Observable behavior:** Every requirement is something a user, caller, or test can see or verify — never an implementation detail, file path, component, or library choice.
- **Stable identifiers:** Give each requirement an ID. Keep it when wording changes without changing meaning; retire it only when the requirement is removed or split. Substantive requirement changes reopen the spec approval gate.
- **Unambiguous:** Two implementers would build the same behavior. Avoid hand-waving words like "should", "fast", "simple", "user-friendly", or "etc."
- **Failures and edge cases specified:** State behavior for invalid inputs, missing data, empty states, and errors when relevant.
- **Preserves existing behavior:** Existing behavior is maintained unless a requirement explicitly specifies a change.
- **Testable:** Every requirement can be tested or verified in this repo.
- **Holds user intent:** Capture what the user asked for without adding unrequested extras. Scope creep is a defect.

## Write and review

Write the spec in `.craft/<feature>/spec.md` using the shape defined in `SKILL.md`.

If `craft-reviewer` sends the spec back, evaluate each point: **Adopt** when it sharpens or corrects the spec without losing user intent; **Reject** with a reason when it does not. Rewrite the spec for adopted points; do not append reviewer replies as a competing spec.
