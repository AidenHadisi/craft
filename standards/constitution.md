# Code Constitution

Hard contract for agents writing code and judging diffs. One unambiguous rule per bullet.

## When writing code

- NEVER invent a one-caller helper; keep it inline. Shared helpers only for real duplication at 3+ call sites. A genuine responsibility may become a deep module, not a one-caller helper. Narrow exceptions only: an API-required callback, or a genuinely non-obvious concept whose mechanics would drown the caller.
- NEVER validate inputs that internal typed code already guarantees. Validate at system boundaries only (API, UI, deserialization, untrusted I/O).
- NEVER add parameters, config knobs, hooks, or generality that no current caller needs.
- NEVER place an interface beside its only implementation or invent abstraction theater. A minimal consumer-owned interface at a real external seam is allowed. NEVER add a field-setting factory/builder or a wrapper that hides nothing.
- NEVER swallow errors. Handle them, propagate with context, or crash loudly. Logged-and-ignored counts as swallowed.
- MUST prefer the stdlib or an existing project dependency over hand-rolling dates, retries, validation, parsing, or serialization.
- MUST use guard clauses and early returns. Nesting depth 3+ is a defect — flatten before extracting.
- MUST write the least code that stays clear. Redundant or ceremonial length is a defect; raw line count is not the metric. Obscure brevity is also a defect.
- MUST keep changes inside the requested behavior. No drive-by refactors of unrelated code.
- MUST verify unfamiliar APIs, symbols, config keys, and version features against the repo or authoritative docs. Never invent by analogy.
- MUST preserve auth/authz, keep secrets out of code, and use parameterized or context-escaped primitives for untrusted data.
- MUST report what was Deleted and what was Deliberately not added. Silence about either is incomplete.

## When judging a diff

Delete-first anti-verbosity rubric. Correctness holds; an empty Pass is valid — never invent findings.

- Ask what can be deleted before asking what is missing. A net-negative diff can be good.
- Prefer deletion only when observable behavior and required public/wire contracts are preserved. Flag any semantic or contract drift. Never reward smaller wrong code.
- Findings must quote the offending lines. No vibes, no uncited taste, no "feels verbose."
- Hunt single-use helpers, speculative knobs, impossible-case guards, wrappers that hide nothing, ceremony comments that restate the code, and near-duplicate blocks.
- Verdict is Pass or Revise with actionable itemized fixes. No numeric scores. No 1–10 scales. Empty Pass is valid; never invent findings.
