---
name: craft-monitor
description: Monitor a shipped feature against live production data. The first invocation works out how to observe the feature and writes docs/monitor/<feature>.md; every invocation after follows that guide and reports what changed. Use right after shipping something, or whenever the user wants to know how a feature is really behaving in production.
---

# Craft Monitor

A feature behaves differently under real traffic. Go look — not only for what broke, but for how well it does its job. Identify the feature from the invocation or session; ask if unclear. Missing `docs/monitor/<feature>.md` means first run (write the guide); present means follow it. Dispatch subagents for legwork; skip what you already know.

### 1. Write the guide

Start from what you already know and research only the gaps. Settle four things — take each from context if you have it; dispatch in parallel only for the ones you don't:

- **State** — tables and columns the feature writes (status, steps, timestamps)
- **Logs** — error statements the code emits, and the service or stream they land in
- **Metrics** — dashboards or alerts already covering this path
- **Access** — exact MCP, connection, or command for each, including name mismatches across systems (`prod` vs `blue-prod`)

Pick four to six checks — questions you'd ask the morning after a deploy (stuck, failing, erroring, quiet, throughput, and at least one about how *well* the feature works). Always include throughput. Run every check before writing it down; record observed normals; drop anything you can't answer. If you can't reach the data, stop and say what's missing.

Write `docs/monitor/<feature>.md` using [monitor-template](references/monitor-template.md). Show the user, then go straight into step 2.

### 2. Run the monitor

Read the doc and run each check. Compare every result to its Normal line and to the log.

Then look around beyond the checks: error types they don't cover, impossible statuses, where time goes, thin output, real usage vs design. Dig into firing checks first.

Report only what a person would want to know:

- **Problems** — new, worse, or resolved relative to the log and Normal. A check that errors, or returns empty where it should return rows, is itself a problem.
- **Observations** — not broken, but actionable and not already logged. Don't pad; most runs have nothing new — say so.

Append one entry to `## Log` (newest first). Propose new recurring checks in the log entry; don't edit the Checks section yourself — a human decides what this file watches.

## Hard rules

- Read-only against production. Always. Query, never write.
- Bound every query with a time window and a `LIMIT`.
- An empty result is a broken check, not a pass.
- Never paste raw log output into the doc — quote error strings short and inline.
- Say when you can't tell.
