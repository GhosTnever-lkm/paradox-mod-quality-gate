#!/usr/bin/env python3
"""Combine ModRelease Studio and Paradox Mod Workbench reports safely."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

VERSION = (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()


def _text(item: dict[str, Any], key: str, default: str = "") -> str:
    value = item.get(key, default)
    return value if isinstance(value, str) else default


def _safe_path(raw: str) -> str:
    raw = raw.replace("\\", "/")
    if raw.startswith("/") or re.match(r"^[A-Za-z]:/", raw):
        return PurePosixPath(raw).name[:200]
    parts = [p for p in PurePosixPath(raw).parts if p not in ("/", "", ".", "..")]
    return "/".join(parts)[:300]


def _load(path: str, label: str) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} report is missing or invalid: {exc.__class__.__name__}") from None
    if not isinstance(data, dict) or not isinstance(data.get("findings", []), list):
        raise ValueError(f"{label} report has an unexpected format")
    return data


def normalize(modrelease: dict[str, Any], workbench: dict[str, Any]) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    for item in modrelease.get("findings", []):
        if not isinstance(item, dict):
            continue
        severity = _text(item, "severity").lower()
        severity = {"error": "error", "warning": "warning", "info": "notice"}.get(severity, "notice")
        findings.append({"source": "ModRelease Studio", "severity": severity,
                         "code": _text(item, "code", "MODRELEASE_FINDING"),
                         "path": _safe_path(_text(item, "path")), "line": None,
                         "message": _text(item, "message", "Finding without a message")[:1000]})
    for item in workbench.get("findings", []):
        if not isinstance(item, dict):
            continue
        severity = _text(item, "severity").lower()
        severity = {"error": "error", "warning": "warning", "info": "notice"}.get(severity, "notice")
        path = _safe_path(_text(item, "path"))
        mod = _text(item, "mod").replace("|", "\\|").replace("\n", " ").replace("\r", " ")[:120]
        line = item.get("line")
        findings.append({"source": "Paradox Mod Workbench", "severity": severity,
                         "code": _text(item, "code", "PMW_FINDING"), "path": path, "mod": mod,
                         "line": line if isinstance(line, int) and line > 0 else None,
                         "message": _text(item, "message", "Finding without a message")[:1000]})
    counts = {key: sum(f["severity"] == key for f in findings) for key in ("error", "warning", "notice")}
    return {"tool": "Paradox Mod Quality Gate", "version": VERSION, "scanners": {
        "modrelease": _text(modrelease, "version", "unknown"), "workbench": _text(workbench, "version", "unknown")},
        "counts": counts, "findings": findings}


def _escape_command(value: str) -> str:
    return value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A").replace(":", "%3A").replace(",", "%2C")


def _annotation(finding: dict[str, Any]) -> str:
    level = {"error": "error", "warning": "warning", "notice": "notice"}[finding["severity"]]
    properties = []
    if finding["path"]:
        properties.append("file=" + _escape_command(finding["path"]))
    if finding["line"]:
        properties.append(f"line={finding['line']}")
    props = " ".join(properties)
    message = _escape_command(f"[{finding['source']}/{finding['code']}] {finding['message']}")
    return f"::{level}{' ' + props if props else ''}::{message}"


def markdown(report: dict[str, Any]) -> str:
    c = report["counts"]
    lines = ["# Paradox Mod Quality Gate", "", f"**{c['error']} errors · {c['warning']} warnings · {c['notice']} notices**", "",
             "| Level | Tool / check | File | Finding |", "|---|---|---|---|"]
    for finding in report["findings"][:100]:
        msg = finding["message"].replace("|", "\\|").replace("\n", " ")
        if finding.get("mod"):
            msg = f"**{finding['mod']}** — {msg}"
        path = finding["path"] + (f":{finding['line']}" if finding["line"] else "")
        lines.append(f"| {finding['severity']} | {finding['source']} / `{finding['code']}` | `{path or '—'}` | {msg} |")
    if len(report["findings"]) > 100:
        lines.append(f"| — | — | — | Showing 100 of {len(report['findings'])} findings; see the JSON artifact. |")
    if not report["findings"]:
        lines.append("| — | — | — | No findings reported. |")
    lines += ["", "This report combines ModRelease Studio and Paradox Mod Workbench. A clean report is not a guarantee that the game will launch.", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modrelease", required=True)
    parser.add_argument("--workbench", required=True)
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--md-out", required=True)
    parser.add_argument("--gate", choices=("error", "warning", "never"), default="error")
    parser.add_argument("--github", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = normalize(_load(args.modrelease, "ModRelease"), _load(args.workbench, "Workbench"))
    except ValueError as exc:
        print(f"Paradox Mod Quality Gate: {exc}", file=sys.stderr)
        return 2
    Path(args.json_out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rendered = markdown(report)
    Path(args.md_out).write_text(rendered + "\n", encoding="utf-8")
    if args.github:
        summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as handle:
                handle.write(rendered + "\n")
        for finding in report["findings"][:50]:
            print(_annotation(finding))
        if len(report["findings"]) > 50:
            print(f"::warning::Only the first 50 of {len(report['findings'])} findings were annotated; see report artifact.")
    counts = report["counts"]
    if args.gate == "never":
        return 0
    if counts["error"]:
        return 1
    if args.gate == "warning" and counts["warning"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
