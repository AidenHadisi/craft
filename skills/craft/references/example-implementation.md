# Filter tasks by status

Add optional `--status open|done` filtering to `tasklist list`. Omitting the option keeps the full listing in its existing order; invalid values use the standard CLI usage error.

## 1. Add status filtering

### 1.1 Parse the option

`src/tasklist/cli.py` — in `build_parser()`, beside the existing list options:

```python
list_parser.add_argument("--status", choices=("open", "done"), default=None)
```

### 1.2 Filter before sorting

In the existing `run_list(args, store, output)`, select tasks before the existing sort and renderer:

```python
tasks = store.list_tasks()
if args.status is not None:
    tasks = [task for task in tasks if task.status == args.status]
tasks = sorted(tasks, key=lambda task: (task.created_at, task.id))
return render_tasks(tasks, output)
```
