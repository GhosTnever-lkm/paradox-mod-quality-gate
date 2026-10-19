import hashlib
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import package_pro as pro_builder  # noqa: E402
from package_pro import PACKAGE_FILES, package_pro  # noqa: E402


class ProPackageTests(unittest.TestCase):
    def test_builds_versioned_allowlisted_archive_and_checksum(self):
        with tempfile.TemporaryDirectory() as temp:
            archive_path, sidecar_path = package_pro(Path(temp))
            self.assertEqual(archive_path.name, "Paradox-Mod-Quality-Gate-Pro-v1.0.10.zip")
            with zipfile.ZipFile(archive_path) as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(set(archive.namelist()), set(PACKAGE_FILES))
                self.assertEqual(archive.read("VERSION").decode().strip(), (ROOT / "VERSION").read_text(encoding="utf-8").strip())
                self.assertEqual(archive.read("pro/VERSION").decode().strip(), "1.0.10")
                launcher = archive.read("pro/Start-Pro.ps1").decode()
                self.assertIn("modrelease-studio.git@v0.3.82", launcher)
                self.assertIn("paradox-mod-workbench.git@v0.2.8", launcher)
                self.assertIn("ModRelease Studio v0.3.82", archive.read("pro/README.md").decode())
                pro_readme = archive.read("pro/README.md").decode()
                self.assertIn("Start-Pro.ps1 -SkipInstall", pro_readme)
                self.assertIn("first launch", pro_readme.lower())
                self.assertIn("Version: **1.0.10**", pro_readme)
            digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
            self.assertEqual(sidecar_path.read_text(encoding="ascii"), f"{digest}  {archive_path.name}\n")

    def test_package_build_is_reproducible(self):
        with tempfile.TemporaryDirectory() as temp:
            first, _ = package_pro(Path(temp) / "one")
            second, _ = package_pro(Path(temp) / "two")
            self.assertEqual(first.read_bytes(), second.read_bytes())

    def test_archive_is_identical_for_lf_and_crlf_checkouts(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            archives = []
            for name, ending in (("lf", b"\n"), ("crlf", b"\r\n")):
                source_root = (base / name / "source").resolve()
                for relative in PACKAGE_FILES:
                    target = source_root / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    content = (ROOT / relative).read_bytes().replace(b"\r\n", b"\n").replace(b"\n", ending)
                    target.write_bytes(content)
                with patch.object(pro_builder, "ROOT", source_root):
                    archive, _ = package_pro(base / name / "dist")
                archives.append(archive.read_bytes())
            self.assertEqual(archives[0], archives[1])


if __name__ == "__main__":
    unittest.main()
