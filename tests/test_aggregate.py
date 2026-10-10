import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runner"))
from aggregate import normalize  # noqa: E402
from workspace import resolve_workspace_path  # noqa: E402


class WorkspacePathTests(unittest.TestCase):
    def test_resolves_existing_workspace_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = root / "modrelease.toml"
            config.write_text("[scan]\n", encoding="utf-8")
            self.assertEqual(resolve_workspace_path(root, "modrelease.toml", label="config-file", require_file=True), config)

    def test_rejects_parent_traversal_and_absolute_outside_path(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            root = Path(temp)
            outside_file = Path(outside) / "outside.toml"
            outside_file.write_text("[scan]\n", encoding="utf-8")
            for raw in ("../outside.toml", str(outside_file)):
                with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, "must stay inside"):
                    resolve_workspace_path(root, raw, label="config-file", require_file=True)

    def test_rejects_missing_config_and_directory_when_file_required(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaisesRegex(ValueError, "does not exist"):
                resolve_workspace_path(root, "missing.toml", label="config-file", require_file=True)
            (root / "directory").mkdir()
            with self.assertRaisesRegex(ValueError, "must be a file"):
                resolve_workspace_path(root, "directory", label="config-file", require_file=True)

    def test_rejects_symlink_that_resolves_outside_workspace(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            root = Path(temp)
            target = Path(outside) / "real.toml"
            target.write_text("[scan]\n", encoding="utf-8")
            link = root / "escape.toml"
            link.symlink_to(target)
            with self.assertRaisesRegex(ValueError, "must stay inside"):
                resolve_workspace_path(root, "escape.toml", label="config-file", require_file=True)


class AggregateTests(unittest.TestCase):
    def test_normalizes_findings_without_local_paths(self):
        report = normalize(
            {"version": "0.2.1", "target": "C:/Users/alice/mod", "findings": [
                {"code": "SECRET", "severity": "ERROR", "path": "common/x.txt", "message": "Potential token"}]},
            {"version": "0.2.1", "findings": [
                {"code": "PARSE", "severity": "warning", "mod": "A", "path": "events/a.txt", "line": 12, "message": "Unbalanced brace"}]},
        )
        self.assertEqual(report["counts"], {"error": 1, "warning": 1, "notice": 0})
        self.assertEqual(report["version"], (ROOT / "VERSION").read_text(encoding="utf-8").strip())
        self.assertEqual(report["findings"][1]["path"], "events/a.txt")
        self.assertEqual(report["findings"][1]["mod"], "A")
        self.assertNotIn("alice", json.dumps(report))

    def test_invalid_report_is_actionable_and_exit_2(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "bad.json").write_text("not json", encoding="utf-8")
            args = [sys.executable, str(ROOT / "runner/aggregate.py"), "--modrelease", str(root / "bad.json"),
                    "--workbench", str(root / "bad.json"), "--json-out", str(root / "out.json"),
                    "--md-out", str(root / "out.md")]
            result = subprocess.run(args, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("invalid", result.stderr)

    def test_never_does_not_fail_on_findings(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "m.json").write_text(json.dumps({"findings": [{"code": "X", "severity": "ERROR", "message": "bad"}]}), encoding="utf-8")
            (root / "w.json").write_text(json.dumps({"findings": []}), encoding="utf-8")
            args = [sys.executable, str(ROOT / "runner/aggregate.py"), "--modrelease", str(root / "m.json"),
                    "--workbench", str(root / "w.json"), "--json-out", str(root / "out.json"),
                    "--md-out", str(root / "out.md"), "--gate", "never"]
            self.assertEqual(subprocess.run(args).returncode, 0)

    def test_warning_gate_blocks_warnings_but_error_gate_does_not(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "m.json").write_text(json.dumps({"findings": [{"code": "X", "severity": "WARNING", "message": "review"}]}), encoding="utf-8")
            (root / "w.json").write_text(json.dumps({"findings": []}), encoding="utf-8")
            base = [sys.executable, str(ROOT / "runner/aggregate.py"), "--modrelease", str(root / "m.json"),
                    "--workbench", str(root / "w.json"), "--json-out", str(root / "out.json"),
                    "--md-out", str(root / "out.md")]
            warning = subprocess.run(base + ["--gate", "warning"], capture_output=True)
            error = subprocess.run(base + ["--gate", "error"], capture_output=True)
            self.assertEqual(warning.returncode, 1)
            self.assertEqual(error.returncode, 0)


if __name__ == "__main__":
    unittest.main()
