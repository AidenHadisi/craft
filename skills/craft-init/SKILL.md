---
name: craft-init
description: Initialize or refresh the shared .craft/ repository guides when setting up Craft, when guides are missing, or when repository knowledge needs updating.
---

# Craft Init

Maintain durable project context for Craft in the target repository's `.craft/` directory. This guide complements host instructions such as `AGENTS.md`; it does not replace them or generate project rules and skills.

## Lifecycle

- When Craft begins work and `.craft/README.md` is missing, run this workflow automatically before feature planning. Initialize all seven guides, even when a topic is unavailable or does not apply.
- If `.craft/README.md` exists, read it and only the guides relevant to the current task. Reuse their verified context and check current repository instructions and sources when they conflict.
- On `refresh` or `refresh <area>`, re-investigate the requested areas. Without an area, refresh all seven guides. Preserve custom content and confirmed useful details; update only claims supported by current evidence, and record unresolved or changed claims.
- During ordinary Craft work, add or correct durable project facts when direct evidence establishes them. Keep feature-specific findings and decisions in that feature's folder, not in the project guide.

## Initialize or refresh

1. Read current project instructions and existing `.craft/` content. Start discovery from documentation, manifests, configs, scripts, and project skills. Current instructions, sources, and user direction take precedence over cached claims.
2. For a first initialization, inspect the repository broadly once. For an existing guide, inspect only gaps relevant to the task; a refresh rechecks only its requested area or areas. Do not rescan merely because a guide is old.
3. Delegate independent read-only discovery when agents are available: project map and conventions; development and testing; operations, observability, and databases. Keep the orchestrator responsible for merging findings and writing the guides. Do not delegate overlapping edits.
4. Adapt the linked templates into `.craft/`. Their headings are starting points: add, combine, reorder, or omit sections to fit the repo. Replace instructional prompts with facts or explicit gaps. Keep the README short; each fact has one home and other guides link to it. Beside commands and access instructions, distinguish documented claims from what was actually verified, with the result, date, scope, and source. Use `Unknown` for unavailable information and `N/A` only with a confirmed reason.
5. Include all seven guides initially, using concise `Unknown` or `N/A` notes where appropriate. On later runs, fill missing guides or sections only when relevant to the task or requested refresh. A README alone does not establish that all topics were investigated.
6. Merge into existing guides, preserving useful custom content. Keep them concise; do not store credentials, tokens, private keys, or copied secret values. Summarize what changed, what was checked, and any remaining gaps.

## Output files

- [`README.md`](assets/templates/README.md) — project overview, map, guide index, and discovery status.
- [`conventions.md`](assets/templates/conventions.md) — observed implementation patterns and representative paths.
- [`development.md`](assets/templates/development.md) — prerequisites, setup, build, run, and repository workflow.
- [`testing.md`](assets/templates/testing.md) — test commands, organization, fixtures, and safe test-data guidance.
- [`deployment.md`](assets/templates/deployment.md) — CI/CD, environments, release and rollback pointers.
- [`observability.md`](assets/templates/observability.md) — logs, metrics, dashboards, alerts, and access paths.
- [`databases.md`](assets/templates/databases.md) — databases and services, schema pointers, migrations, and safe access.

Keep these project guides Git-tracked subject to the repository's policy. Recheck them when relevant facts change or the user requests a refresh. Do not deploy, mutate external systems, or require credentials to complete initialization. If verification needs unavailable access, record the limitation and the documented source; never imply that it was verified.
