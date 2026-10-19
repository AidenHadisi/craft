import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('craft_sync', ROOT / 'sync.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode('utf-8'))


def snapshot(path, timestamps=False):
    if not path.exists():
        return None
    if path.is_file():
        return path.read_bytes()
    return {str(p.relative_to(path)): (None if p.is_dir() else p.read_bytes(),
                                     p.stat().st_mtime_ns if timestamps else None)
            for p in [path, *sorted(path.rglob('*'))]}


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repo'
        self.repo.mkdir()
        for name in ['sync.py', '.cursor-plugin', '.claude-plugin', '.codex-plugin',
                     'skills', 'agents', 'AGENTS.md', 'LICENSE']:
            source = ROOT / name
            if source.exists():
                if source.is_dir():
                    shutil.copytree(source, self.repo / name)
                else:
                    shutil.copyfile(source, self.repo / name)
        self.home = self.base / 'home'
        self.home.mkdir()
        self.claude = self.base / 'claude'
        self.codex = self.base / 'codex'
        self.state = self.base / 'state'
        self.store = self.state / 'craft-sync'
        self.log = self.base / 'calls.jsonl'
        bin_path = self.base / 'bin'
        for client in ['claude', 'codex']:
            executable = bin_path / client
            write(executable, f'''#!{sys.executable}
import json, os, sys
from pathlib import Path
client = Path(sys.argv[0]).name
args = sys.argv[1:]
with open(os.environ['FAKE_LOG'], 'a') as log:
    log.write(json.dumps({{"client": client, "args": args}}) + '\\n')
if client == os.environ.get('FAIL_CLIENT') and args[:2] == ['plugin', 'install']:
    print('intentional install failure', file=sys.stderr)
    sys.exit(1)
''')
            executable.chmod(0o755)
        self.env = dict(os.environ, HOME=str(self.home), XDG_STATE_HOME=str(self.state),
                        CODEX_HOME=str(self.codex), CLAUDE_CONFIG_DIR=str(self.claude),
                        PATH=str(bin_path), FAKE_LOG=str(self.log), FAIL_CLIENT='')
        self.plugins = [self.home / '.cursor/plugins/local/craft', self.store / 'plugin',
                        self.store / 'codex/plugin']
        self.agents = [(self.home / '.cursor/agents', '.md'), (self.claude / 'agents', '.md'),
                       (self.codex / 'agents', '.toml')]
        self.rules = [self.claude / 'CLAUDE.md', self.codex / 'AGENTS.md']

    def run_sync(self, *args, **overrides):
        return subprocess.run([sys.executable, '-B', str(self.repo / 'sync.py'), *args],
                              cwd=self.base, env=self.env | overrides,
                              capture_output=True, text=True, timeout=30)

    def succeeds(self, result):
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def calls(self):
        return [json.loads(line) for line in self.log.read_text().splitlines()] if self.log.exists() else []

    def test_dry_run_reports_clients_without_writes_or_cli_calls(self):
        before = snapshot(self.base, timestamps=True)
        result = self.run_sync('--dry-run')
        self.succeeds(result)
        for client in ['cursor', 'claude', 'codex']:
            self.assertIn(client + ': would sync', result.stdout)
        self.assertEqual(snapshot(self.base, timestamps=True), before)
        self.assertEqual(self.calls(), [])

    def expected_calls(self):
        return [
            {'client': 'claude', 'args': ['plugin', 'marketplace', 'add', str(self.store), '--scope', 'user']},
            {'client': 'claude', 'args': ['plugin', 'install', 'craft@craft-sync', '--scope', 'user']},
            {'client': 'codex', 'args': ['plugin', 'marketplace', 'add', str(self.store)]},
            {'client': 'codex', 'args': ['plugin', 'add', 'craft@craft-sync']},
        ]

    def seed_unrelated(self):
        files = []
        for directory, extension in self.agents:
            files.extend([(directory / ('personal' + extension), 'Personal agent\r\n'),
                          (directory / ('craft-other' + ('.toml' if extension == '.md' else '.md')),
                           'Other extension\n')])
        for path, text in files:
            write(path, text)
        for path in self.rules:
            write(path, "Personal $& $` $'\r\n")
        return files

    def test_help_and_unknown_arguments_do_not_sync(self):
        before = snapshot(self.base)
        self.succeeds(self.run_sync('--help'))
        self.assertNotEqual(self.run_sync('--unknown').returncode, 0)
        self.assertEqual(snapshot(self.base), before)

    def test_sync_copies_native_payloads_catalogs_and_is_repeatable(self):
        unrelated = self.seed_unrelated()
        self.succeeds(self.run_sync())
        self.assertEqual(self.calls(), self.expected_calls())
        for plugin, manifest in zip(self.plugins, ['.cursor-plugin', '.claude-plugin', '.codex-plugin']):
            self.assertEqual(set(p.name for p in plugin.iterdir()), {manifest, 'skills', 'AGENTS.md', 'LICENSE'})
            for name in [manifest, 'skills', 'AGENTS.md', 'LICENSE']:
                self.assertEqual(snapshot(plugin / name), snapshot(self.repo / name))
        for source in (self.repo / 'agents').glob('*.md'):
            agent = sync.parse_agent(source.read_bytes().decode('utf-8'), source.name)
            self.assertEqual((self.agents[0][0] / source.name).read_bytes(), source.read_bytes())
            claude = (self.agents[1][0] / source.name).read_text()
            self.assertIn('name: ' + agent['name'], claude)
            self.assertEqual('disallowedTools:' in claude, agent['readonly'])
            native = tomllib.loads((self.agents[2][0] / (source.stem + '.toml')).read_text())
            self.assertEqual(native['name'], source.stem)
            self.assertEqual(native['developer_instructions'], agent['body'])
            if agent['model'] in (None, 'inherit'):
                self.assertNotIn('model', native)
        for path, text in unrelated:
            self.assertEqual(path.read_bytes(), text.encode())
        for path in self.rules:
            self.assertTrue(path.read_bytes().startswith(b"Personal $& $` $'\r\n\n<!-- craft:rules -->"))
        for catalog, source in [('.claude-plugin/marketplace.json', './plugin'),
                                ('.agents/plugins/marketplace.json', {'source': 'local', 'path': './codex/plugin'})]:
            self.assertEqual(json.loads((self.store / catalog).read_text()),
                             {'name': 'craft-sync', 'owner': {'name': 'Craft'},
                              'plugins': [{'name': 'craft', 'source': source}]})
        before = [snapshot(p) for p in [self.home, self.claude, self.codex, self.state]]
        self.succeeds(self.run_sync())
        self.assertEqual([snapshot(p) for p in [self.home, self.claude, self.codex, self.state]], before)
        self.assertEqual(self.calls(), self.expected_calls() * 2)
        for path in self.rules:
            self.assertEqual(path.read_text().count('<!-- craft:rules -->'), 1)
        self.assertFalse((self.store / 'state.json').exists())
        self.assertFalse((self.store / 'backups').exists())

    def test_refresh_replaces_owned_files_and_preserves_surrounding_rules_bytes(self):
        unrelated = self.seed_unrelated()
        self.succeeds(self.run_sync())
        names = sorted((self.repo / 'agents').glob('*.md'))
        removed, updated = names[:2]
        copies = [(directory / (updated.stem + ext)).read_bytes() for directory, ext in self.agents]
        skill = next((self.repo / 'skills').glob('*/SKILL.md')).relative_to(self.repo)
        removed_skill = next(p for p in (self.repo / 'skills').iterdir() if p.is_dir() and p != (self.repo / skill).parent)
        for plugin in self.plugins:
            write(plugin / skill, 'Installed local edits')
            write(plugin / 'stale.txt', 'Stale')
        for directory, ext in self.agents:
            write(directory / ('craft-stale' + ext), 'Stale')
            write(directory / (updated.stem + ext), 'Installed local edits')
        write(self.repo / skill, 'Updated skill\n')
        shutil.rmtree(removed_skill)
        removed.unlink()
        shared = "# New guidance\r\nLiteral $& $` $'\r\n"
        write(self.repo / 'AGENTS.md', shared)
        prefix, suffix = "Prefix $& $` $'\r\n", "\r\nSuffix $& $` $'\r\n"
        for path in self.rules:
            write(path, prefix + '<!-- craft:rules -->\nOld\n<!-- /craft:rules -->' + suffix)
        self.succeeds(self.run_sync())
        for plugin in self.plugins:
            self.assertEqual((plugin / skill).read_bytes(), b'Updated skill\n')
            self.assertFalse((plugin / 'skills' / removed_skill.name).exists())
            self.assertFalse((plugin / 'stale.txt').exists())
        for (directory, ext), old in zip(self.agents, copies):
            self.assertFalse((directory / (removed.stem + ext)).exists())
            self.assertFalse((directory / ('craft-stale' + ext)).exists())
            self.assertEqual((directory / (updated.stem + ext)).read_bytes(), old)
        for path, text in unrelated:
            self.assertEqual(path.read_bytes(), text.encode())
        expected = (prefix + '<!-- craft:rules -->\n' + shared.rstrip() + '\n<!-- /craft:rules -->' + suffix).encode()
        for path in self.rules:
            self.assertEqual(path.read_bytes(), expected)
        self.succeeds(self.run_sync())
        for path in self.rules:
            self.assertEqual(path.read_bytes(), expected)

    def test_invalid_source_is_rejected_before_destination_changes(self):
        self.seed_unrelated()
        write(self.repo / 'agents/craft-invalid.md', '---\nname: different\ndescription: Invalid\n---\nBody')
        before = snapshot(self.base)
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('identity mismatch', result.stderr)
        self.assertEqual(snapshot(self.base), before)
        self.assertEqual(self.calls(), [])

    def test_unreadable_source_agents_directory_preserves_installed_content(self):
        self.succeeds(self.run_sync())
        agents = self.repo / 'agents'
        shutil.rmtree(agents)
        for non_directory in (False, True):
            with self.subTest(non_directory=non_directory):
                if non_directory:
                    write(agents, 'Not a directory')
                destinations = [snapshot(p) for p in [self.home, self.claude, self.codex, self.state]]
                calls = self.calls()
                result = self.run_sync()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(str(agents), result.stderr)
                self.assertEqual([snapshot(p) for p in [self.home, self.claude, self.codex, self.state]], destinations)
                self.assertEqual(self.calls(), calls)

    def test_cli_failure_reports_client_continues_and_retry_succeeds(self):
        result = self.run_sync(FAIL_CLIENT='claude')
        self.assertEqual(result.returncode, 1)
        self.assertIn('claude: intentional install failure', result.stderr)
        self.assertIn('cursor: synced', result.stdout)
        self.assertIn('codex: synced', result.stdout)
        self.assertEqual(self.calls(), self.expected_calls())
        self.assertTrue((self.plugins[2] / '.codex-plugin/plugin.json').exists())
        self.succeeds(self.run_sync())
        self.assertEqual(self.calls(), self.expected_calls() * 2)

    def test_bom_crlf_source_preserves_cursor_bytes_and_codex_body(self):
        source = "\ufeff---\r\nname: craft-windows\r\ndescription: 'It''s quoted'\r\nreadonly: false\r\n---\r\nBody.\r\n"
        write(self.repo / 'agents/craft-windows.md', source)
        self.succeeds(self.run_sync())
        self.assertEqual((self.agents[0][0] / 'craft-windows.md').read_bytes(), source.encode())
        native = tomllib.loads((self.codex / 'agents/craft-windows.toml').read_text())
        self.assertEqual(native['developer_instructions'], 'Body.\r\n')

    def test_default_paths_use_isolated_home_when_overrides_are_empty(self):
        self.succeeds(self.run_sync(XDG_STATE_HOME='', CODEX_HOME='', CLAUDE_CONFIG_DIR=''))
        self.assertTrue((self.home / '.local/state/craft-sync/plugin/.claude-plugin/plugin.json').exists())
        self.assertTrue((self.home / '.claude/CLAUDE.md').exists())
        self.assertTrue((self.home / '.codex/AGENTS.md').exists())


def source(metadata='', body='Do the work.'):
    return '---\nname: example\ndescription: Example agent\n' + metadata + '---\n' + body


class AgentTests(unittest.TestCase):
    def test_quoted_scalars_bom_crlf_and_windows_filename(self):
        agent = sync.parse_agent("\ufeff---\r\nname: example\r\ndescription: 'It''s \"quoted\"'\r\nmodel: \"model\\tname\"\r\nreadonly: false\r\n---\r\nBody.\r\n", 'folder\\example.MD')
        self.assertEqual({k: v for k, v in agent.items() if k != 'source'},
                         dict(name='example', description='It\'s "quoted"', model='model\tname', readonly=False, body='Body.\r\n'))

    def test_readonly_adds_prose_once_and_disallows_claude_write_tools(self):
        agent = sync.parse_agent(source('readonly: true\nmodel: inherit\n'), 'example.md')
        self.assertEqual(agent['body'], 'Do the work.\n\nThis agent is read-only and must not modify files.')
        self.assertEqual(sync.render_agent(agent, 'claude'), '---\nname: example\ndescription: "Example agent"\ndisallowedTools:\n  - Write\n  - Edit\n  - NotebookEdit\n---\nDo the work.\n\nThis agent is read-only and must not modify files.\n')
        self.assertNotIn('model =', sync.render_agent(agent, 'codex'))
        self.assertEqual(sync.parse_agent(source('readonly: true\n', 'Do not edit files.'))['body'], 'Do not edit files.')

    def test_rendered_toml_roundtrips_control_characters_and_unicode(self):
        description = 'Quote " slash \\ tab\t newline\n return\r nul\0 del\x7f emoji 😃'
        agent = sync.parse_agent(source('model: special\n').replace('description: Example agent', 'description: ' + json.dumps(description)))
        agent['body'] = 'First\n"second" \\ \b\f\t\r\0\x7f 😃\n'
        rendered = sync.render_agent(agent, 'codex')
        self.assertEqual(tomllib.loads(rendered), dict(name='example', description=description, model='special', developer_instructions=agent['body']))
        self.assertIn('\\u007f', rendered)
        self.assertNotRegex(rendered, r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')
        claude = sync.render_agent(agent, 'claude')
        self.assertEqual(json.loads(re.search(r'^description: (.*)$', claude, re.M)[1]), description)
        self.assertIn('model: "special"', claude)

    def test_invalid_metadata_and_identity_are_rejected(self):
        cases = [('', 'frontmatter'), (source('unknown: value\n'), 'unsupported metadata'),
                 (source('name: example\n'), 'duplicate'), (source('  model: small\n'), 'malformed'),
                 (source('model:\n'), 'scalar'), (source('model: ""\n'), 'non-empty'),
                 (source('readonly: "true"\n'), 'unquoted boolean'),
                 (source("readonly: 'false'\n"), 'unquoted boolean'),
                 (source('readonly: yes\n'), 'unquoted boolean')]
        for model in ['[a, b]', '{a: b}', '|\n  body', '>', '&anchor', 'x # comment', 'x: y']:
            cases.append((source('model: ' + model + '\n'), 'complex YAML'))
        for model in ['"unfinished', '"value" trailing']:
            cases.append((source('model: ' + model + '\n'), 'JSON-quoted'))
        cases.extend([(source("model: 'can't'\n"), 'unpaired'),
                      (source("model: 'unfinished\n"), 'single-quoted'),
                      (source().replace('name: example', 'name: "bad name"'), 'identifier'),
                      (source().replace('description: Example agent', 'description: " "'), 'non-empty'),
                      (source('', '  \n'), 'body must not be empty')])
        for text, error in cases:
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, error):
                    sync.parse_agent(text, 'example.md')
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            sync.parse_agent(source(), 'different.md')


if __name__ == '__main__':
    unittest.main()
