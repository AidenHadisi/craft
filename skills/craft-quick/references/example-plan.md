# Add a limit to task listing

Add an optional `--limit N` flag to `tasklist list` to show only the first N tasks in the existing order. Keep the full listing when the flag is omitted and reject invalid limits with the standard CLI usage error.

## Progress

- [x] Initialize the task
- [x] Explore the relevant code
- [x] Resolve open questions, if any
- [x] Write the plan
- [ ] Critique and refine the plan
- [ ] Get approval
- [ ] Build and run checks
  - [ ] 1. Add the list limit
    - [ ] 1.1 Parse and validate the option
    - [ ] 1.2 Limit the sorted tasks
    - [ ] 1.3 Verify CLI behavior
- [ ] Polish
- [ ] Summarize the result

## Approach

Task listing flows from command input through task retrieval and ordering to output rendering. The command layer coordinates this flow, the store owns retrieval, and the renderer owns presentation.

Apply the limit in the command layer after ordering and before rendering. This keeps selection consistent with existing output while preserving the responsibilities of storage and presentation. Validate the option at the input boundary, before accessing tasks. The change preserves full listings when the option is omitted and requires no storage changes or new dependencies.

## Implementation

### 1. Add the list limit

#### 1.1 Parse and validate the option

`src/tasklist/cli.py` — add the validator and register it with the existing list parser:

```python
def positive_int(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed

# In build_parser(), alongside the existing list options:
list_parser.add_argument("--limit", type=positive_int, default=None)
```

#### 1.2 Limit the sorted tasks

In `run_list(args, store, output)`, select tasks after the existing sort:

```python
tasks = sorted(store.list_tasks(), key=lambda task: (task.created_at, task.id))
if args.limit is not None:
    tasks = tasks[:args.limit]
return render_tasks(tasks, output)
```

#### 1.3 Verify CLI behavior

`tests/test_cli.py` — use the temporary store and existing `run_cli(*argv) -> (exit_code, stdout, stderr)` helper. Add these cases:

```text
Given tasks inserted as IDs [3, 1, 2] with identical created_at:
  list --limit 2   -> exit 0; task IDs [1, 2]
  list            -> exit 0; task IDs [1, 2, 3]
  list --limit 10  -> exit 0; task IDs [1, 2, 3]

Given an empty store:
  list --limit 2   -> exit 0; no task rows

For each limit in ["0", "-1", "abc"]:
  list --limit N   -> exit 2; stderr contains usage and an error
```

Run after implementation and again after polish:

```sh
python -m unittest tests.test_cli
```

## Checks

- [ ] A positive limit prints the first N tasks in the existing sorted order.
- [ ] Omitting the limit preserves the full listing.
- [ ] A limit larger than the task count returns every task.
- [ ] An empty store produces no task rows.
- [ ] Zero, negative, and non-integer limits exit with code 2 and print usage and an error to stderr.
