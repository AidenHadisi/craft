---
name: craft-init
description: Initialize or refresh the shared Craft repository guides when setting up Craft, when guides are missing, or when repository knowledge needs updating.
---

# Craft Init

Create or refresh concise project guides in `.craft/`. They complement `AGENTS.md` and do not replace project instructions or create rules and skills.

The file paths in this skill are defaults. When project instructions set other locations for Craft guides or documents, use those instead.

## 1. Initialize

Read current project instructions and existing `.craft/` content. Initialize all guides on first setup. For a refresh, update all guides or only the named area.

## 2. Explore

Inspect project structure, conventions, run and test commands, deployment, logs, and database access. Use documentation, manifests, configs, scripts, and project skills; current evidence takes precedence over cached notes.

Distinguish documented instructions from what you verified; include source, result, date, and scope. Use `Unknown` if unavailable and `N/A` only when confirmed.

## 3. Write

Preserve useful custom content and keep each fact in one place. Use the required H2 headings below in order, followed by `Sources and gaps` in every guide; add repo-specific H3 headings only when they help.

- `README.md`
  - `## Overview` — Summarize the project's purpose, users or callers, language/runtime, and important dependencies.
  - `## Architecture` — Describe major components, their responsibilities, relationships, and data flow.
  - `## Project map` — Point to the important directories and files and explain what each contains.
  - `## Guides` — Link to `conventions.md`, `development.md`, `testing.md`, `deployment.md`, `observability.md`, and `databases.md` with short descriptions, using paths relative to `README.md`.
- `conventions.md`
  - `## Code organization` — Describe observed naming and code layout patterns, linking to useful real examples.
  - `## Implementation patterns` — Record project-specific API, logging, and data-access patterns worth following, with real examples.
  - `## Errors and validation` — Explain how inputs and failures are handled, with links to representative code where available.
- `development.md`
  - `## Prerequisites` — List runtime/tool versions and other prerequisites needed to work in the repository.
  - `## Setup` — Give setup steps, working directories, environment configuration, and supporting services; point to secret sources without copying values.
  - `## Build and run` — Record exact build/start commands, working directories, URLs or ports, startup checks, and how to stop the process.
  - `## Development workflow` — Describe generated files and formatting or iteration steps; link to `testing.md` for checks and `databases.md` for data setup/access.
- `testing.md`
  - `## Test layout` — Describe frameworks, test locations, naming, and shared helpers.
  - `## Commands` — Give focused and full test commands, plus build, lint, and typecheck commands where applicable, with working directories and prerequisites; link to `development.md` for startup.
  - `## Fixtures and environment` — Record required services and fixtures/accounts, outbound effects to stub or avoid, and cleanup steps; link to `databases.md` for access details.
- `deployment.md`
  - `## Environments and pipeline` — Name environments and service targets, and point to CI/config paths and release gates.
  - `## Release and verification` — Describe the release mechanism or maintained runbook and how to verify completion.
  - `## Rollback` — Explain how to restore a prior working release and verify recovery.
  - `## Configuration` — Point to relevant configuration and infrastructure paths and secret-management sources.
- `observability.md`
  - `## Logs` — Identify services, log groups/tools, environment filters, and useful queries or filters.
  - `## Metrics and dashboards` — Describe available metrics and dashboards and what they help diagnose.
  - `## Alerts` — Record alert conditions, destinations, and the documented response path.
  - `## Access` — Explain required roles/tools/connections and access steps, distinguishing documented access from access actually checked; link to existing runbooks and summarize findings without copying raw output.
- `databases.md`
  - `## Systems and schemas` — Name data services and environments, their purpose and owners, and schema/model locations.
  - `## Access and local setup` — Describe tools/connections, authentication method, local services or seeds, and read/write boundaries; reference credentials without copying values.
  - `## Migrations` — Give migration locations, commands, required ordering, and maintained procedures.

Use concise prose, fenced commands/configuration/schemas, and diagrams when useful. Keep unavailable sections and mark them `Unknown`; use `N/A` only when the absence is confirmed. Link to applicable project instructions, rules, and skills rather than copying their contents.

End every guide with the H2 heading `## Sources and gaps`. List source paths and the inspected scope; distinguish documented from executed or accessed evidence, and give each check's result, date, and scope. Record remaining gaps.

Do not store secrets or mutate external systems; follow repo tracking policy.

## 4. Maintain

During ordinary Craft work, read relevant guides and make small, evidence-based corrections. Inspect only relevant gaps or the requested refresh area; do not rescan because a guide is old. Keep feature findings in the feature workspace.

## 5. Finish

Summarize files changed, checks performed, and remaining gaps.
