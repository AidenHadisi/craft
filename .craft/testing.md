# Testing

## Test layout

Python tests under `test/` cover agent parsing/rendering and sync behavior using temporary fixtures and fake CLI executables.

## Commands

Run `python3 -m unittest discover -s test`. Verified on 2026-10-18 with Python 3.13.1: all 13 tests passed, including missing or invalid source directories leaving installations untouched. `python3 -B sync.py --dry-run` reported all three clients, and `--help` exited successfully. Live client installation was not run. The prior JavaScript baseline had 6 passing and 4 failing tests due to a CLI-helper argument mismatch.

## Fixtures and environment

The sync tests create temporary directories and fake CLI programs; no external service or real client invocation is needed by those fixtures. Syncing the actual checkout modifies local client installations; see [development.md](development.md).

## Sources and gaps

Sources: `test/`, `README.md`, and `sync.py` (2026-10-18). No lint or typecheck command is configured.
