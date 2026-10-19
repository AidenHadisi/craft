# Conventions

## Implementation patterns

- All sync implementation lives in [sync.py](../sync.py), using Python standard-library functions, one shared client sync routine, one agent renderer, and focused metadata parsing. Client paths are a small literal mapping; errors and file writes are handled directly.
- Agent files use Markdown frontmatter with `name` and `description`; README documents optional `readonly` and `model` scalars. See [agents/](../agents/).
- Tests use Python's `unittest`; see [test/](../test/).

## Project instructions

- [AGENTS.md](../AGENTS.md) contains shared working rules.
- [README.md](../README.md) documents plugin authoring and sync behavior.

## Sources and gaps

Source inspection of the listed files on 2026-10-18. No formatter or lint configuration was found in the inspected root files.
