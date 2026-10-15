import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("refresh", ROOT / "scripts/refresh.py")
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)


class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo with spaces"
        for folder in ("skills", "agents", "references", ".cursor-plugin"):
            shutil.copytree(ROOT / folder, self.root / folder)
        shutil.copy2(ROOT / "LICENSE", self.root / "LICENSE")

    def test_shared_prompts_and_restrictions_survive_conversion(self):
        refresh.build(self.root)
        for source in (self.root / "agents").glob("*.md"):
            metadata, instructions = refresh.read_agent(source)
            codex = tomllib.loads((self.root / ".generated/codex-agents" / f"{source.stem}.toml").read_text())
            claude = (self.root / ".generated/claude/agents" / source.name).read_text()
            self.assertEqual(codex["developer_instructions"], instructions)
            self.assertTrue(claude.endswith(instructions))
            self.assertNotIn("model", codex)
            self.assertNotIn("readonly:", claude)
            self.assertEqual("disallowedTools:" in claude, metadata.get("readonly") == "true")
        for host in ("codex", "claude"):
            manifest = json.loads((self.root / f".generated/{host}/.{host}-plugin/plugin.json").read_text())
            self.assertEqual(manifest["name"], "craft")
            self.assertEqual(len(list((self.root / f".generated/{host}/skills").glob("*/SKILL.md"))), 9)

    def test_edits_and_deletions_propagate_and_check_does_not_write(self):
        refresh.build(self.root)
        source = self.root / "skills/craft/SKILL.md"
        source.write_text(source.read_text() + "\nA new instruction.\n")
        generated = self.root / ".generated/codex/skills/craft/SKILL.md"
        before = generated.read_bytes()
        with self.assertRaises(ValueError):
            refresh.build(self.root, check=True)
        self.assertEqual(generated.read_bytes(), before)
        stale = self.root / ".generated/codex/skills/removed/SKILL.md"
        stale.parent.mkdir()
        stale.write_text("obsolete")
        refresh.build(self.root)
        self.assertEqual(generated.read_bytes(), source.read_bytes())
        self.assertFalse(stale.exists())
        refresh.build(self.root, check=True)
        refresh.build(self.root)
        refresh.build(self.root, check=True)

    def test_links_follow_source_updates(self):
        refresh.build(self.root)
        home = Path(self.temp.name) / "codex"
        refresh.agent_links(self.root, home, install=True)
        target = home / "agents/craft-coder.toml"
        self.assertTrue(target.is_symlink())
        source = self.root / "agents/craft-coder.md"
        source.write_text(source.read_text() + '\nPreserve "quotes", backslashes \\, and Unicode →.\n')
        refresh.build(self.root)
        refresh.agent_links(self.root, home, install=True)
        self.assertIn('Preserve "quotes", backslashes \\, and Unicode →.', tomllib.loads(target.read_text())["developer_instructions"])

    def test_existing_equivalent_files_can_be_migrated(self):
        refresh.build(self.root)
        home = Path(self.temp.name) / "codex"
        (home / "agents").mkdir(parents=True)
        source = self.root / ".generated/codex-agents/craft-coder.toml"
        target = home / "agents/craft-coder.toml"
        target.write_text(source.read_text().split("\n", 1)[1])
        refresh.agent_links(self.root, home, install=True)
        self.assertTrue(target.is_symlink())

    def test_conflict_leaves_all_destinations_untouched(self):
        refresh.build(self.root)
        home = Path(self.temp.name) / "codex"
        (home / "agents").mkdir(parents=True)
        target = home / "agents/craft-tester.toml"
        target.write_text('name = "custom"\n')
        with self.assertRaises(ValueError):
            refresh.agent_links(self.root, home, install=True)
        self.assertEqual(list((home / "agents").iterdir()), [target])
        self.assertEqual(target.read_text(), 'name = "custom"\n')

    def test_generated_symlink_is_not_replaced(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (outside / "keep").write_text("important")
        (self.root / ".generated").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            refresh.build(self.root)
        self.assertEqual((outside / "keep").read_text(), "important")

    def test_failed_marketplace_switch_restores_previous_source(self):
        refresh.build(self.root)
        old = {"name": "craft-local", "root": "/old/craft", "marketplaceSource": {"sourceType": "local", "source": "/old/craft"}}
        failure = subprocess.CalledProcessError(1, ["codex"])
        with patch.object(refresh, "agent_links"), patch.object(refresh, "run", side_effect=[{"marketplaces": [old]}, None, failure, None]) as run:
            with self.assertRaises(subprocess.CalledProcessError):
                refresh.install_codex(self.root)
            self.assertEqual(run.call_args.args, ("codex", "plugin", "marketplace", "add", "/old/craft"))

    def test_claude_install_validates_and_uses_user_scope(self):
        with patch.object(refresh, "run", side_effect=[None, [], None, None, None]) as run:
            refresh.install_claude(self.root)
        calls = [call.args for call in run.call_args_list]
        self.assertEqual(calls[0], ("claude", "plugin", "validate", str(self.root / ".generated/claude")))
        self.assertEqual(calls[-2], ("claude", "plugin", "install", "craft@craft-local", "--scope", "user"))
        self.assertEqual(calls[-1], ("claude", "plugin", "update", "craft@craft-local", "--scope", "user"))


if __name__ == "__main__":
    unittest.main()
