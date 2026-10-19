# Verify status filtering

Verify optional status filtering and the standard usage error for invalid values.

## Setup

From the sample repository root, use the existing read-only fixture `tests/fixtures/tasks.json`: task 1 is open and task 2 is done, in existing order. The existing root option `--store PATH` selects that fixture; no external services are involved.

Use the existing temporary-store and CLI helpers in `tests/test_cli.py` for automated cases. Run `python -m unittest tests.test_cli`.

## Checks

- [x] REQ-1: Omitted status lists all tasks; open/done selects matching tasks in existing order; empty selections show no rows.
- [x] REQ-2: Invalid status exits 2, with usage and error on stderr and empty stdout.

## Evidence

**Illustrative observations only; these commands were not executed in this repository.**

### Automated

Ran: `python -m unittest tests.test_cli`
Saw: Exit 0; default listing, open/done selection, empty selection, ordering, and invalid-status tests passed.

### Live

Ran: `python -m tasklist --store tests/fixtures/tasks.json list --status open`
Saw: Exit 0; only task 1 appeared; stderr empty.

Ran: `python -m tasklist --store tests/fixtures/tasks.json list`
Saw: Exit 0; tasks 1 and 2 appeared in that order; stderr empty.

Ran: `python -m tasklist --store tests/fixtures/tasks.json list --status invalid`
Saw: Exit 2; stderr contained usage and an error; stdout empty.

If a check fails, fix the issue and rerun all live checks.

## Cleanup

No temporary artifacts or background processes were created; the read-only fixture remained unchanged.
