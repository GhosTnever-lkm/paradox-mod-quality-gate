import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runner"))
from aggregate import normalize  # noqa: E402


class AggregateTests(unittest.TestCase):
    def test_normalizes_findings_without_local_paths(self):
        report = normalize(
            {"version": "0.2.1", "target": "C:/Users/alice/mod", "findings": [
                {"code": "SECRET", "severity": "ERROR", "path": "common/x.txt", "message": "Potential token"}]},
            {"version": "0.2.1", "findings": [
                {"code": "PARSE", "severity": "warning", "mod": "A", "path": "events/a.txt", "line": 12, "message": "Unbalanced brace"}]},
        )
        self.assertEqual(report["counts"], {"error": 1, "warning": 1, "notice": 0})
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
