# Development

## Setup

The README requires Python 3.11+, Cursor, and the Claude Code and Codex CLIs on `PATH`. No Python packages are needed. Python 3.13.1 is available in the current environment (verified 2026-10-18).

## Build and run

Run `python3 sync.py` to synchronize local client plugin files, agent definitions, and shared rules and register plugins through the Claude and Codex CLIs. `python3 sync.py --dry-run` reports clients without writing files or invoking CLIs. Test execution evidence lives in [testing.md](testing.md).

## Development workflow

Edit skill sources under `skills/`, agents under `agents/`, or shared rules in `AGENTS.md`, then run the sync command when updating installations. Change the standalone `sync.py` to update sync behavior.

## Sources and gaps

Sources: `README.md` and `sync.py` (2026-10-18). Python 3.13.1 availability was verified the same date. Installed client CLI versions and live installation are unverified; no build step is required.
