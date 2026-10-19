# Project guide

## Overview

Craft is a shared plugin source for Cursor, Claude Code, and Codex. It distributes skills, agent definitions, and shared instructions through one Python script.

## Project map

- `skills/` — workflow skills and their references/assets.
- `agents/` — shared agent definitions.
- `sync.py` — standalone sync script using only the Python standard library.
- `test/` — Python unittest coverage with isolated filesystem and client fixtures.

## Guides

- [Conventions](conventions.md) — source patterns and repository instructions.
- [Development](development.md) — prerequisites and local workflow.
- [Testing](testing.md) — test layout and command status.
- [Deployment](deployment.md) — sync and release status.
- [Observability](observability.md) — runtime output and gaps.
- [Databases](databases.md) — data services and access.

## Sources and gaps

Sources: `README.md`, `AGENTS.md`, manifests, `sync.py`, and `test/` (2026-10-18). See the testing guide for execution evidence. Release and external client operations remain Unknown.
