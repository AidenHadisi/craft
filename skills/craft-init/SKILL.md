---
name: craft-init
description: Initialize or refresh the shared Craft repository guides when setting up Craft, when guides are missing, or when repository knowledge needs updating.
---

# Craft Init

Create or refresh concise project guides in `.craft/`. They complement `AGENTS.md` and do not replace project instructions or create rules and skills.

The file paths in this skill are defaults. When project instructions set other locations for Craft guides or documents, use those instead. Follow stricter host policies on what shared guides may contain.

## 1. Initialize

Read current project instructions and existing `.craft/` content. Initialize applicable guides on first setup. For a refresh, update all guides or only the named area.

### Admission

Shared guides hold stable, project-wide conventions and architecture, plus reusable setup, testing, and operating instructions. Add a fact only when it helps future work across the project and belongs in a shared guide. Most ordinary work needs no guide update.

Keep individual function behavior, feature contracts, one-off decisions, code/config inventories, and source or verification logs out of shared guides. Keep task findings and evidence with the work that produced them. Link to maintained code or runbooks when needed to apply guidance, rather than cataloging or restating them.

## 2. Explore

Inspect project structure, conventions, run and test commands, deployment, logs, and database access. Use documentation, manifests, configs, scripts, and project skills; current evidence takes precedence over cached notes.

Verify guidance against current evidence. Put uncertainty beside the affected instruction when it matters to using it; do not imply untested access or commands were verified.

## 3. Write

Preserve useful custom content that meets Admission and keep each fact in one place. Use the applicable H2 headings below in order; omit empty or unavailable sections and guides. Add repo-specific H3 headings only when they help.

- `README.md`
  - `## Overview` — Summarize the project's purpose, users or callers, language/runtime, and important dependencies.
  - `## Architecture` — Describe major components, their responsibilities, relationships, and data flow.
  - `## Project map` — Point to the main architectural entry points needed to navigate the repository.
  - `## Guides` — Link to the guides present with short descriptions, using paths relative to `README.md`.
- `conventions.md`
  - `## Code organization` — Describe project-wide naming and code layout conventions.
  - `## Implementation patterns` — Record shared API, logging, and data-access conventions; link an example only when it clarifies the guidance.
  - `## Errors and validation` — Explain shared input-validation and error-handling conventions.
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
  - `## Configuration` — Explain how to manage release configuration and secrets, linking maintained instructions where available.
- `observability.md`
  - `## Logs` — Identify services, log groups/tools, environment filters, and useful queries or filters.
  - `## Metrics and dashboards` — Describe available metrics and dashboards and what they help diagnose.
  - `## Alerts` — Record alert conditions, destinations, and the documented response path.
  - `## Access` — Explain required roles/tools/connections and access steps; link to maintained runbooks and qualify unverified access where it affects the instructions.
- `databases.md`
  - `## Systems and schemas` — Name data services and environments, their purpose and owners, and schema/model locations.
  - `## Access and local setup` — Describe tools/connections, authentication method, local services or seeds, and read/write boundaries; reference credentials without copying values.
  - `## Migrations` — Give migration locations, commands, required ordering, and maintained procedures.

Use concise prose, fenced commands/configuration/schemas, and diagrams when useful. Preserve exact reusable commands, their prerequisites, and production cautions needed to run them safely. Link to applicable project instructions, rules, and skills rather than copying their contents. Do not add placeholder sections or source and verification logs.

Do not store secrets or mutate external systems; follow repo tracking policy.

## 4. Maintain

During ordinary Craft work, read relevant guides and correct stale guidance when needed. Apply Admission before adding anything. Inspect only relevant gaps or the requested refresh area; do not rescan because a guide is old.

## 5. Finish

Summarize files changed, checks performed, and remaining gaps.
