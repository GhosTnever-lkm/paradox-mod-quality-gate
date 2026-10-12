#!/usr/bin/env python3
"""Combine ModRelease Studio and Paradox Mod Workbench reports safely."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import unicodedata
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import quote

VERSION = (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8").strip()


def _text(item: dict[str, Any], key: str, default: str = "") -> str:
    value = item.get(key, default)
    return value if isinstance(value, str) else default


def _visible_text(raw: str, *, preserve_line_breaks: bool = False) -> str:
    """Escape invisible Unicode code points before showing untrusted text."""
    safe = []
    for char in raw:
        category = unicodedata.category(char)
        if preserve_line_breaks and char in "\r\n":
            safe.append(char)
        elif category.startswith("C") or category in {"Zl", "Zp"}:
            codepoint = ord(char)
            if codepoint < 0x20 or codepoint == 0x7F:
                safe.append(f"\\x{codepoint:02x}")
            else:
                safe.append(f"\\u{{{codepoint:04x}}}")
        else:
            safe.append(char)
    return "".join(safe)


def _display_path(raw: str) -> str:
    # Paths originate in user-controlled mod archives. Keep report tables single-line
    # and prevent pipes/backticks from changing Markdown table/code-span structure.
    safe = []
    for char in raw:
        codepoint = ord(char)
        if char in {"|", "`"} or codepoint < 0x20 or codepoint == 0x7F:
            safe.append(f"\\x{codepoint:02x}")
        else:
            safe.append(_visible_text(char))
    return "".join(safe)


def _markdown_text(raw: str) -> str:
    text = _visible_text(raw)
    text = html.escape(text, quote=False)
    return re.sub(r"([\\`*_{}\[\]()#+.!|><:~-])", r"\\\1", text)


def json_report(report: dict[str, Any]) -> str:
    """Use JSON escapes for non-ASCII text while retaining parsed data exactly."""
    return json.dumps(report, ensure_ascii=True, indent=2)


def _safe_path(raw: str) -> str:
    raw = raw.replace("\\", "/")
    if raw.startswith("/") or re.match(r"^[A-Za-z]:/", raw):
        return _display_path(PurePosixPath(raw).name[:200])
    parts = [p for p in PurePosixPath(raw).parts if p not in ("/", "", ".", "..")]
    return _display_path("/".join(parts)[:300])


def _load(path: str, label: str) -> dict[str, Any]:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} report is missing or invalid: {exc.__class__.__name__}") from None
    if not isinstance(data, dict) or "findings" not in data or not isinstance(data["findings"], list):
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
    value = _visible_text(value, preserve_line_breaks=True)
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
        msg = _markdown_text(finding["message"])
        if finding.get("mod"):
            msg = f"**{_markdown_text(finding['mod'])}** — {msg}"
        path = finding["path"] + (f":{finding['line']}" if finding["line"] else "")
        code = _display_path(finding["code"])
        lines.append(f"| {finding['severity']} | {finding['source']} / `{code}` | `{path or '—'}` | {msg} |")
    if len(report["findings"]) > 100:
        lines.append(f"| — | — | — | Showing 100 of {len(report['findings'])} findings; see the JSON artifact. |")
    if not report["findings"]:
        lines.append("| — | — | — | No findings reported. |")
    lines += ["", "This report combines ModRelease Studio and Paradox Mod Workbench. A clean report is not a guarantee that the game will launch.", ""]
    return "\n".join(lines)


def _sarif_rule_id(finding: dict[str, Any]) -> str:
    source = _text(finding, "source")
    prefix = {"ModRelease Studio": "MRS", "Paradox Mod Workbench": "PMW"}.get(source)
    if not prefix:
        prefix = re.sub(r"[^A-Za-z0-9]+", "-", source).strip("-").upper()[:16] or "SCANNER"
    code = _text(finding, "code", "UNKNOWN")
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", code).strip("-._")[:64] or "UNKNOWN"
    digest = hashlib.sha256(code.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{slug}-{digest}"


def _sarif_level(severity: str) -> str:
    return {"error": "error", "warning": "warning", "notice": "note"}.get(severity.lower(), "note")


def _sarif_message(value: str) -> str:
    bidi_controls = {
        "\u061c", "\u200e", "\u200f", "\u202a", "\u202b", "\u202c", "\u202d", "\u202e",
        "\u2066", "\u2067", "\u2068", "\u2069",
    }
    visible = []
    for char in value[:1000]:
        if char in bidi_controls:
            visible.append(f"\\u{ord(char):04X}")
        else:
            visible.append(_visible_text(char, preserve_line_breaks=True))
    return "".join(visible)


def _sarif_uri(path: str) -> str:
    """Return a checkout-relative URI and never serialize a machine-local path."""
    normalized = path.replace("\\", "/").strip()
    absolute = normalized.startswith("/") or bool(re.match(r"^[A-Za-z]:/", normalized)) or normalized.lower().startswith("file:")
    if absolute:
        normalized = normalized.rstrip("/").rsplit("/", 1)[-1]
    parts: list[str] = []
    for part in normalized.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    return quote("/".join(parts), safe="/-._~")


def sarif_report(report: dict[str, Any]) -> dict[str, Any]:
    """Render the unified report as SARIF 2.1.0 with checkout-relative paths."""
    findings = [item for item in report.get("findings", []) if isinstance(item, dict)]
    rules: dict[str, dict[str, Any]] = {}
    results = []
    for finding in findings:
        rule_id = _sarif_rule_id(finding)
        source = _text(finding, "source", "Unknown scanner")
        code = _text(finding, "code", "UNKNOWN")
        rules.setdefault(rule_id, {
            "id": rule_id,
            "name": _visible_text(code),
            "shortDescription": {"text": _visible_text(f"{source}: {code}")[:256]},
        })
        result: dict[str, Any] = {
            "ruleId": rule_id,
            "level": _sarif_level(_text(finding, "severity", "notice")),
            "message": {"text": _sarif_message(_text(finding, "message", "Finding without a message"))},
        }
        path = _text(finding, "path")
        if path:
            physical_location: dict[str, Any] = {"artifactLocation": {"uri": _sarif_uri(path)}}
            line = finding.get("line")
            if isinstance(line, int) and not isinstance(line, bool) and line > 0:
                physical_location["region"] = {"startLine": line}
            result["locations"] = [{"physicalLocation": physical_location}]
        results.append(result)

    tool = _text(report, "tool", "Paradox Mod Quality Gate")
    version = _text(report, "version", VERSION)
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {
                "name": tool,
                "version": version,
                "rules": list(rules.values()),
            }},
            "results": results,
        }],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modrelease", required=True)
    parser.add_argument("--workbench", required=True)
    parser.add_argument("--json-out", required=True)
    parser.add_argument("--md-out", required=True)
    parser.add_argument("--sarif-out")
    parser.add_argument("--gate", choices=("error", "warning", "never"), default="error")
    parser.add_argument("--github", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = normalize(_load(args.modrelease, "ModRelease"), _load(args.workbench, "Workbench"))
    except ValueError as exc:
        print(f"Paradox Mod Quality Gate: {exc}", file=sys.stderr)
        return 2
    Path(args.json_out).write_text(json_report(report) + "\n", encoding="utf-8")
    rendered = markdown(report)
    Path(args.md_out).write_text(rendered + "\n", encoding="utf-8")
    if args.sarif_out:
        Path(args.sarif_out).write_text(json.dumps(sarif_report(report), ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
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
