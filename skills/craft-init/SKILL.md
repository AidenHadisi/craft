---
name: craft-init
description: Initialize or refresh the shared .craft/ repository guides when setting up Craft, when guides are missing, or when repository knowledge needs updating.
---

# Craft Init

Maintain concise, durable project context in the target repo's `.craft/`. These guides complement `AGENTS.md`; they do not replace it or create project rules or skills.

## Initialize or refresh

Read current repo instructions and `.craft/` content. Use docs, manifests, configs, scripts, and skills as sources; current instructions and evidence take precedence over cached notes. Inspect broadly once for first setup; otherwise investigate only relevant gaps or the requested refresh area, not merely because a guide is old. Refresh all seven guides by default or only the named area.

- Adapt templates to the repo, preserve useful custom content, and keep each fact in one place. Include all seven guides on first setup.
- Distinguish documented instructions from commands or access actually verified; record the source, result, date, and scope.
- Use `Unknown` when information is unavailable and `N/A` only with a confirmed reason.
- Do not store secrets or mutate external systems. Follow repo tracking policy.

Return a concise summary of files, checks, and gaps.

During ordinary work with existing guides, read only relevant ones and make small evidence-based corrections. Keep feature findings in the feature workspace.

## Guide templates

- [README.md](assets/templates/README.md) — overview, repo map, guide index, discovery status.
- [conventions.md](assets/templates/conventions.md) — coding patterns and example paths.
- [development.md](assets/templates/development.md) — setup, build, run, workflow.
- [testing.md](assets/templates/testing.md) — commands, fixtures, safe test data.
- [deployment.md](assets/templates/deployment.md) — CI/CD, release, rollback.
- [observability.md](assets/templates/observability.md) — logs, metrics, dashboards, alerts.
- [databases.md](assets/templates/databases.md) — data services, schemas, migrations, safe access.
