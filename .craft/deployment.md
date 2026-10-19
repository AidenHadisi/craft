# Deployment

## Environments and pipeline

The README describes installing Craft locally into Cursor, Claude Code, and Codex by running `python3 sync.py`. No CI workflow or deployment pipeline was found in the inspected repository files.

## Release and rollback

No release, versioning, or rollback procedure is documented in the inspected sources. The manifest version is `0.4.0`; that value alone does not establish a release process.

## Configuration

Manifests are in `.cursor-plugin/plugin.json`, `.claude-plugin/plugin.json`, and `.codex-plugin/plugin.json`. `XDG_STATE_HOME`, `CODEX_HOME`, and `CLAUDE_CONFIG_DIR` customize locations, as documented in README. Syncing is a local filesystem/client operation.

## Sources and gaps

Sources: `README.md`, plugin manifests, and `sync.py` (2026-10-18). CI, published artifact, release gates, and rollback details are Unknown.
