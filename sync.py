#!/usr/bin/env python3
"""Sync Craft skills, agents and instructions to local coding clients."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def parse_scalar(raw):
    value = raw.strip()
    if not value:
        raise ValueError('craft agent: metadata values must be a scalar')
    if value.startswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            raise ValueError('craft agent: invalid JSON-quoted scalar') from None
    if value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            raise ValueError('craft agent: invalid YAML single-quoted scalar or unpaired interior apostrophe')
        return value[1:-1].replace("''", "'")
    if re.search(r'^[\[{|>&*!%@`]|:\s|\s+#', value):
        raise ValueError('craft agent: unsupported complex YAML; use a simple scalar')
    return value


def parse_agent(source, filename=None):
    match = re.fullmatch(r'\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)', source, re.S)
    if not match:
        raise ValueError('craft agent: expected simple YAML frontmatter delimited by --- and a Markdown body')
    fields = {}
    for index, line in enumerate(re.split(r'\r?\n', match[1]), 2):
        if not line.strip():
            continue
        field = re.fullmatch(r'([A-Za-z_][A-Za-z0-9_-]*):(?:\s+|$)(.*)', line)
        if not field:
            raise ValueError(f"craft agent: malformed frontmatter on line {index}; expected 'key: scalar'")
        key, raw = field.groups()
        if key not in ('name', 'description', 'readonly', 'model'):
            raise ValueError(f"craft agent: unsupported metadata '{key}'")
        if key in fields:
            raise ValueError(f"craft agent: duplicate metadata '{key}'")
        if key == 'readonly' and raw.strip() not in ('true', 'false'):
            raise ValueError("craft agent: metadata 'readonly' must be the unquoted boolean true or false")
        fields[key] = parse_scalar(raw)
    name = fields.get('name', '')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', name):
        raise ValueError("craft agent: required metadata 'name' must be a non-empty agent identifier")
    if not fields.get('description', '').strip():
        raise ValueError("craft agent: required metadata 'description' must be a non-empty string")
    if 'model' in fields and not fields['model'].strip():
        raise ValueError("craft agent: metadata 'model' must be omitted or a non-empty string")
    if filename:
        stem = re.sub(r'\.md$', '', str(filename).replace('\\', '/').split('/')[-1], flags=re.I)
        if stem != name:
            raise ValueError(f"craft agent: filename identity mismatch: metadata name '{name}' does not match '{stem}'")
    body = match[2]
    if not body.strip():
        raise ValueError('craft agent: Markdown body must not be empty')
    readonly = fields.get('readonly') == 'true'
    if readonly and not re.search(r'\b(read[- ]only|(?:do|must) not (?:edit|modify|write))\b', body, re.I):
        body += '\n\nThis agent is read-only and must not modify files.'
    return {'name': name, 'description': fields['description'], 'model': fields.get('model'),
            'readonly': readonly, 'body': body, 'source': source}


def render_agent(agent, client):
    if client == 'cursor':
        return agent['source']
    fields = {'name': agent['name'], 'description': agent['description']}
    if agent['model'] and agent['model'] != 'inherit':
        fields['model'] = agent['model']
    if client == 'codex':
        fields['developer_instructions'] = agent['body']
    lines = [] if client == 'codex' else ['---']
    separator = ' = ' if client == 'codex' else ': '
    for key, value in fields.items():
        if client != 'claude' or key != 'name':
            value = json.dumps(value, ensure_ascii=False).replace('\x7f', '\\u007f')
        lines.append(key + separator + value)
    if client == 'claude':
        if agent['readonly']:
            lines.extend(['disallowedTools:', '  - Write', '  - Edit', '  - NotebookEdit'])
        lines.extend(['---', agent['body']])
    return '\n'.join(lines) + ('' if client == 'claude' and agent['body'].endswith('\n') else '\n')


def sync_client(client, root, home, store, agents):
    target, plugin = {
        'cursor': (home / '.cursor', home / '.cursor/plugins/local/craft'),
        'claude': (Path(os.environ.get('CLAUDE_CONFIG_DIR') or home / '.claude'), store / 'plugin'),
        'codex': (Path(os.environ.get('CODEX_HOME') or home / '.codex'), store / 'codex/plugin'),
    }[client]
    if plugin.exists():
        shutil.rmtree(plugin)
    plugin.mkdir(parents=True)
    for name in ('skills', f'.{client}-plugin', 'AGENTS.md', 'LICENSE'):
        source = root / name
        if source.is_dir():
            shutil.copytree(source, plugin / name)
        else:
            shutil.copyfile(source, plugin / name)

    agent_dir = target / 'agents'
    agent_dir.mkdir(parents=True, exist_ok=True)
    extension = '.toml' if client == 'codex' else '.md'
    for path in agent_dir.iterdir():
        if path.name.startswith('craft-') and path.name.endswith(extension):
            path.unlink()
    for agent in agents:
        path = agent_dir / (agent['name'] + extension)
        path.write_bytes(render_agent(agent, client).encode('utf-8'))
    if client == 'cursor':
        return

    rules = target / ('CLAUDE.md' if client == 'claude' else 'AGENTS.md')
    guidance = (root / 'AGENTS.md').read_bytes().decode('utf-8').rstrip()
    block = f'<!-- craft:rules -->\n{guidance}\n<!-- /craft:rules -->'
    text = rules.read_bytes().decode('utf-8') if rules.exists() else ''
    text, replaced = re.subn(r'<!-- craft:rules -->[\s\S]*?<!-- /craft:rules -->',
                             lambda match: block, text, count=1)
    if not replaced:
        text += ('\n' if text else '') + block + '\n'
    rules.write_bytes(text.encode('utf-8'))

    catalog = '.claude-plugin/marketplace.json' if client == 'claude' else '.agents/plugins/marketplace.json'
    catalog_source = './plugin' if client == 'claude' else {'source': 'local', 'path': './codex/plugin'}
    catalog_data = {'name': 'craft-sync', 'owner': {'name': 'Craft'},
                    'plugins': [{'name': 'craft', 'source': catalog_source}]}
    catalog_path = store / catalog
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_bytes((json.dumps(catalog_data, indent=2) + '\n').encode('utf-8'))
    scope = ['--scope', 'user'] if client == 'claude' else []
    install = 'install' if client == 'claude' else 'add'
    for args in (['plugin', 'marketplace', 'add', str(store), *scope],
                 ['plugin', install, 'craft@craft-sync', *scope]):
        result = subprocess.run([client, *args], capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise RuntimeError(result.stderr or result.stdout or f'exited with status {result.returncode}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    home = Path.home()
    agents = []
    for path in sorted((root / 'agents').iterdir()):
        if path.name.endswith('.md'):
            agent = parse_agent(path.read_bytes().decode('utf-8'), path.name)
            if not agent['name'].startswith('craft-'):
                raise ValueError(f'Agent names must start with craft-: {path.name}')
            agents.append(agent)
    store = Path(os.environ.get('XDG_STATE_HOME') or home / '.local/state') / 'craft-sync'
    status = 0
    for client in ('cursor', 'claude', 'codex'):
        try:
            if not args.dry_run:
                sync_client(client, root, home, store, agents)
            print(f"{client}: {'would sync' if args.dry_run else 'synced'}")
        except Exception as error:
            print(f'{client}: {error}', file=sys.stderr)
            status = 1
    return status


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
