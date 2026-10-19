# craft

Shared skills, subagents, and rules for Cursor, Claude Code, and Codex. Plan with the main agent, then delegate implementation, review, and testing.

## Skills

| Skill | Purpose |
|---|---|
| [craft](skills/craft/SKILL.md) | Plan, build, review, and test a feature |
| [craft-quick](skills/craft-quick/SKILL.md) | Build a small change with one approval |
| [craft-brainstorm](skills/craft-brainstorm/SKILL.md) | Explore and discuss an idea |
| [craft-init](skills/craft-init/SKILL.md) | Create or refresh shared repository guides |
| [craft-design](skills/craft-design/SKILL.md) | Compare UI directions and build the chosen design |
| [craft-refactor](skills/craft-refactor/SKILL.md) | Simplify code while preserving behavior |
| [craft-test](skills/craft-test/SKILL.md) | Verify a feature in a live process |
| [craft-monitor](skills/craft-monitor/SKILL.md) | Check a shipped feature |
| [craft-research](skills/craft-research/SKILL.md) | Research a topic |
| [craft-paper](skills/craft-paper/SKILL.md) | Write and review research papers |

Invoke skills with `/craft`, `/craft-quick`, etc. Claude uses namespaced commands such as `/craft:craft`. Each skill contains its workflow; [subagents](agents/) provide the supporting roles.

## Setup and sync

Requires Python 3.11+, Cursor, and the Claude Code and Codex CLIs on your PATH. No Python packages are needed.
Clone this repository, then run from its root:

```bash
python3 sync.py
```

The command installs Craft as a local plugin in all three clients, converts subagents to each client's format, and applies shared rules across your projects. Reload Cursor and start fresh Claude Code/Codex sessions afterward.

## Making changes

- **Skill:** add or edit `skills/<name>/SKILL.md`, with `name` and `description` frontmatter. Keep assets in the same folder.
- **Subagent:** add or edit `agents/craft-<name>.md`, with matching `name` and a `description`. Optional fields: `readonly: true|false` and `model`; omit `model` to inherit. Use simple scalar frontmatter.
- **Rule:** edit `AGENTS.md` for instructions shared across all projects.

Run `python3 sync.py` after any change, including additions or deletions. Each run replaces Craft’s installed plugin files and `craft-*` agents, and updates its rules block. Edit this checkout; local edits need no version bump. Unrelated agents and instructions are preserved.

`--dry-run` lists the clients without changing files or calling CLIs. Custom locations use `XDG_STATE_HOME`, `CODEX_HOME`, and `CLAUDE_CONFIG_DIR`.

## Tests

All sync logic lives in `sync.py`. Run the tests with Python’s standard library:

```bash
python3 -m unittest discover -s test
```

Tests use temporary directories and fake client CLIs.

## License

MIT — see [LICENSE](LICENSE).
