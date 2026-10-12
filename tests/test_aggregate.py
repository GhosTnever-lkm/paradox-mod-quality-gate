import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runner"))
from aggregate import VERSION, _annotation, json_report, markdown, normalize, sarif_report  # noqa: E402
from workspace import resolve_workspace_path  # noqa: E402


class WorkspacePathTests(unittest.TestCase):
    def test_resolves_existing_workspace_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            config = root / "modrelease.toml"
            config.write_text("[scan]\n", encoding="utf-8")
            self.assertEqual(
                resolve_workspace_path(root, "modrelease.toml", label="config-file", require_file=True),
                config.resolve(),
            )

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
            try:
                link.symlink_to(target)
            except OSError as exc:
                if getattr(exc, "winerror", None) == 1314:
                    self.skipTest("symbolic-link creation is not permitted for this Windows account")
                raise
            with self.assertRaisesRegex(ValueError, "must stay inside"):
                resolve_workspace_path(root, "escape.toml", label="config-file", require_file=True)


class AggregateTests(unittest.TestCase):
    def test_sarif_maps_findings_and_keeps_only_relative_locations(self):
        report = normalize(
            {"version": "0.3.58", "findings": [
                {"code": "SHARED", "severity": "ERROR", "path": r"C:\Users\alice\mod\events\bad.txt", "message": "bad\u202eexe"},
                {"code": "SHARED", "severity": "WARNING", "path": "common/other file.txt", "message": "review"},
            ]},
            {"version": "0.2.2", "findings": [
                {"code": "SHARED", "severity": "INFO", "path": "events/test.txt", "line": 7, "message": "note"},
                {"code": "NO_LINE", "severity": "ERROR", "path": "events/no-line.txt", "line": 0, "message": "no line"},
            ]},
        )
        sarif = sarif_report(report)
        self.assertEqual(sarif["version"], "2.1.0")
        self.assertEqual(sarif["$schema"], "https://json.schemastore.org/sarif-2.1.0.json")
        run = sarif["runs"][0]
        self.assertEqual(run["tool"]["driver"]["name"], "Paradox Mod Quality Gate")
        self.assertEqual(run["tool"]["driver"]["version"], VERSION)
        self.assertEqual(len(run["tool"]["driver"]["rules"]), 3)
        self.assertEqual([item["level"] for item in run["results"]], ["error", "warning", "note", "error"])
        scanner_rule_ids = [item["ruleId"] for item in run["results"][:3]]
        self.assertNotEqual(scanner_rule_ids[0], scanner_rule_ids[2])
        self.assertIn("MRS-SHARED-", scanner_rule_ids[0])
        self.assertIn("PMW-SHARED-", scanner_rule_ids[2])
        first_location = run["results"][0]["locations"][0]["physicalLocation"]
        self.assertEqual(first_location["artifactLocation"]["uri"], "bad.txt")
        self.assertNotIn("region", first_location)
        line_location = run["results"][2]["locations"][0]["physicalLocation"]
        self.assertEqual(line_location["region"], {"startLine": 7})
        no_line_location = run["results"][3]["locations"][0]["physicalLocation"]
        self.assertNotIn("region", no_line_location)
        self.assertIn(r"\u202E", run["results"][0]["message"]["text"])
        serialized = json.dumps(sarif, ensure_ascii=True)
        self.assertNotIn("C:\\\\Users", serialized)
        self.assertNotIn("/home/", serialized)
        self.assertNotIn("uriBaseId", serialized)
        self.assertNotIn("originalUriBaseIds", serialized)
        for item in run["results"]:
            for location in item.get("locations", []):
                uri = location["physicalLocation"]["artifactLocation"]["uri"]
                self.assertFalse(uri.startswith(("/", "\\\\")))
                self.assertNotRegex(uri, r"^[A-Za-z]:")
                self.assertNotIn("file:", uri.lower())

    def test_sarif_with_no_findings_has_an_empty_results_list(self):
        sarif = sarif_report(normalize({"findings": []}, {"findings": []}))
        self.assertEqual(sarif["runs"][0]["tool"]["driver"]["rules"], [])
        self.assertEqual(sarif["runs"][0]["results"], [])

    def test_cli_writes_sarif_before_returning_a_blocking_gate_status(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            modrelease = root / "modrelease.json"
            workbench = root / "workbench.json"
            sarif_path = root / "report.sarif"
            modrelease.write_text(json.dumps({"findings": [{
                "code": "BLOCK", "severity": "ERROR", "path": "common/blocked.txt", "message": "blocked",
            }]}), encoding="utf-8")
            workbench.write_text(json.dumps({"findings": []}), encoding="utf-8")
            result = subprocess.run([
                sys.executable, str(ROOT / "runner/aggregate.py"),
                "--modrelease", str(modrelease), "--workbench", str(workbench),
                "--json-out", str(root / "report.json"), "--md-out", str(root / "report.md"),
                "--sarif-out", str(sarif_path), "--gate", "error",
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertTrue(sarif_path.is_file())
            self.assertEqual(json.loads(sarif_path.read_text(encoding="utf-8"))["runs"][0]["results"][0]["level"], "error")

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

    def test_absolute_finding_paths_are_reduced_to_basename(self):
        report = normalize(
            {"findings": [
                {"code": "POSIX", "severity": "ERROR", "path": "/home/alice/private/mod/events/suspect.txt"},
                {"code": "WINDOWS", "severity": "WARNING", "path": r"C:\Users\Alice\Documents\mod\secret.cfg"},
            ]},
            {"findings": []},
        )
        rendered = json.dumps(report)
        self.assertEqual([item["path"] for item in report["findings"]], ["suspect.txt", "secret.cfg"])
        for private_segment in ("/home/alice", "C:\\Users", "Documents", "private"):
            self.assertNotIn(private_segment, rendered)

    def test_untrusted_path_markup_cannot_break_markdown_table(self):
        report = normalize(
            {"findings": [{"code": "PATH", "severity": "ERROR", "path": "events/evil|`row\nnext.txt"}]},
            {"findings": []},
        )
        path = report["findings"][0]["path"]
        self.assertEqual(path, r"events/evil\x7c\x60row\x0anext.txt")
        rendered = __import__("aggregate").markdown(report)
        self.assertEqual(rendered.count("| error |"), 1)
        self.assertNotIn("evil|`row\n", rendered)

    def test_invisible_unicode_is_visible_in_json_markdown_and_annotations(self):
        raw = {
            "findings": [{
                "code": "RULE\u202eTXT", "severity": "ERROR",
                "path": "events/evil\u202eexe.txt\u2028line\u2029end\u0085file",
                "message": "bad\u202evalue <img src=x>| [click](javascript:alert(1))",
                "mod": "Mod\u202e**spoof**",
            }]
        }
        report = normalize(raw, {"findings": []})
        json_text = json_report(report)
        markdown_text = markdown(report)
        annotation = _annotation(report["findings"][0])
        for output in (json_text, markdown_text, annotation):
            for invisible in ("\u202e", "\u2028", "\u2029", "\u0085"):
                self.assertNotIn(invisible, output.casefold())
        self.assertIn(r"\u202e", json_text.casefold())
        self.assertIn("202e", markdown_text.casefold())
        self.assertIn("2028", markdown_text.casefold())
        self.assertIn("2029", annotation.casefold())
        self.assertIn("&lt;img", markdown_text)
        self.assertNotIn("<img", markdown_text)
        self.assertEqual(json.loads(json_text), report)
        self.assertEqual(len(annotation.splitlines()), 1)

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


class DocumentationConsistencyTests(unittest.TestCase):
    def test_readme_examples_use_current_gate_and_checkout_versions(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        current_gate = f"GhosTnever-lkm/paradox-mod-quality-gate@v{VERSION}"
        self.assertNotIn("GhosTnever-lkm/paradox-mod-quality-gate@v1.0.43", readme)
        self.assertGreaterEqual(readme.count(current_gate), 3)
        self.assertNotIn("actions/checkout@v6", readme)
        self.assertGreaterEqual(readme.count("actions/checkout@v7"), 2)

    def test_workbench_pins_match_the_current_release(self):
        pin = "paradox-mod-workbench.git@v0.2.4"
        self.assertIn(pin, (ROOT / "action.yml").read_text(encoding="utf-8"))
        self.assertIn(pin, (ROOT / "pro/Start-Pro.ps1").read_text(encoding="utf-8"))
        self.assertIn(pin, (ROOT / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
