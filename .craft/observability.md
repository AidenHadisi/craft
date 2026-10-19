# Observability

## Logs

`sync.py` writes per-client status to stdout and failures to stderr; it returns a nonzero process exit code on errors. No hosted runtime or centralized logging configuration was found.

## Metrics and dashboards

No metrics, dashboards, or alert configuration were found in the inspected repository.

## Access

The sync command runs locally and may invoke the installed Claude and Codex CLIs. No service observability access procedure is documented.

## Sources and gaps

Sources: `sync.py` and root file inventory (2026-10-18). Findings cover repository runtime only; external client logs and dashboards are Unknown.
