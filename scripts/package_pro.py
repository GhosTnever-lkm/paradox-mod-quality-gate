#!/usr/bin/env python3
"""Build the versioned Windows Pro convenience bundle reproducibly."""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_FILES = (
    "CHANGELOG.md",
    "LICENSE",
    "README.md",
    "VERSION",
    "pro/CHANGELOG.md",
    "pro/LICENSE",
    "pro/README.md",
    "pro/Start-Pro.ps1",
    "pro/ModGate-Pro.ps1",
    "pro/VERSION",
    "runner/aggregate.py",
)
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def package_pro(output_dir: Path) -> tuple[Path, Path]:
    """Build the allowlisted ZIP and its SHA-256 sidecar."""
    output_dir = output_dir.resolve()
    version = (ROOT / "pro/VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise ValueError(f"Invalid Pro bundle version: {version!r}")
    for relative in PACKAGE_FILES:
        path = ROOT / relative
        if not path.is_file() or not path.resolve().is_relative_to(ROOT):
            raise FileNotFoundError(f"Required package file is missing or outside the repository: {relative}")

    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"Paradox-Mod-Quality-Gate-Pro-v{version}.zip"
    output = output_dir / filename
    fd, temporary_name = tempfile.mkstemp(prefix=f".{filename}.", suffix=".tmp", dir=output_dir)
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for relative in sorted(PACKAGE_FILES):
                info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, (ROOT / relative).read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        os.replace(temporary, output)
    finally:
        temporary.unlink(missing_ok=True)

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    sidecar = output.with_suffix(output.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {filename}\n", encoding="ascii", newline="\n")
    return output, sidecar


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    output, sidecar = package_pro(args.output_dir)
    print(f"Package: {output}")
    print(f"SHA-256: {sidecar}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
