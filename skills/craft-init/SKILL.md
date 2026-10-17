---
name: craft-init
description: Initialize or refresh the shared .craft/ repository guides when setting up Craft, when guides are missing, or when repository knowledge needs updating.
---

# Craft Init

Create or refresh concise project guides in `.craft/`. They complement `AGENTS.md` and do not replace project instructions or create rules and skills.

## 1. Initialize

Read current project instructions and existing `.craft/` content. Initialize all guides on first setup. For a refresh, update all guides or only the named area.

## 2. Explore

Inspect project structure, conventions, run and test commands, deployment, logs, and database access. Use documentation, manifests, configs, scripts, and project skills; current evidence takes precedence over cached notes.

Distinguish documented instructions from what you verified; include source, result, date, and scope. Use `Unknown` if unavailable and `N/A` only when confirmed.

## 3. Write

Adapt the templates to the repo, preserve useful custom content, and keep each fact in one place.

- [README.md](assets/templates/README.md) — overview, repo map, guide index, discovery status.
- [conventions.md](assets/templates/conventions.md) — coding patterns and example paths.
- [development.md](assets/templates/development.md) — setup, build, run, workflow.
- [testing.md](assets/templates/testing.md) — commands, fixtures, safe test data.
- [deployment.md](assets/templates/deployment.md) — CI/CD, release, rollback.
- [observability.md](assets/templates/observability.md) — logs, metrics, dashboards, alerts.
- [databases.md](assets/templates/databases.md) — data services, schemas, migrations, safe access.

Do not store secrets or mutate external systems; follow repo tracking policy.

## 4. Maintain

During ordinary Craft work, read relevant guides and make small, evidence-based corrections. Inspect only relevant gaps or the requested refresh area; do not rescan because a guide is old. Keep feature findings in the feature workspace.

## 5. Finish

Summarize files changed, checks performed, and remaining gaps.
