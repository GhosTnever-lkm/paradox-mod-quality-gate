import hashlib
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from package_pro import PACKAGE_FILES, package_pro  # noqa: E402


class ProPackageTests(unittest.TestCase):
    def test_builds_versioned_allowlisted_archive_and_checksum(self):
        with tempfile.TemporaryDirectory() as temp:
            archive_path, sidecar_path = package_pro(Path(temp))
            self.assertEqual(archive_path.name, "Paradox-Mod-Quality-Gate-Pro-v1.0.1.zip")
            with zipfile.ZipFile(archive_path) as archive:
                self.assertIsNone(archive.testzip())
                self.assertEqual(set(archive.namelist()), set(PACKAGE_FILES))
                self.assertEqual(archive.read("VERSION").decode().strip(), "1.0.57")
                self.assertEqual(archive.read("pro/VERSION").decode().strip(), "1.0.1")
                launcher = archive.read("pro/Start-Pro.ps1").decode()
                self.assertIn("modrelease-studio.git@v0.3.72", launcher)
                self.assertIn("paradox-mod-workbench.git@v0.2.5", launcher)
                self.assertIn("ModRelease Studio v0.3.72", archive.read("pro/README.md").decode())
            digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
            self.assertEqual(sidecar_path.read_text(encoding="ascii"), f"{digest}  {archive_path.name}\n")

    def test_package_build_is_reproducible(self):
        with tempfile.TemporaryDirectory() as temp:
            first, _ = package_pro(Path(temp) / "one")
            second, _ = package_pro(Path(temp) / "two")
            self.assertEqual(first.read_bytes(), second.read_bytes())


if __name__ == "__main__":
    unittest.main()
