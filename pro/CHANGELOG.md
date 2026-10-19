# Pro bundle changelog

## 1.0.10 - 2026-10-20

- Update the bundled scanners to ModRelease Studio v0.3.82 and Paradox Mod Workbench v0.2.8.
- Include the latest secret-detection, traversal, and `replace_path` parsing fixes in the Windows package.

## 1.0.9 - 2026-10-13

- Update the bundled ModRelease Studio scanner to v0.3.78.

## 1.0.8 - 2026-10-13

- Document offline reuse of already-installed scanners via Start-Pro.ps1 -SkipInstall.
- Refresh package README and version metadata.

## 1.0.7 - 2026-10-13

- Pin Paradox Mod Workbench v0.2.7 for script diagnostics in all Clausewitz script roots.
- Rebuild the Windows Pro bundle with current scanner versions.

## 1.0.6 - 2026-10-13

- Pin ModRelease Studio v0.3.77 in the Windows launcher.
- Rebuild the paid bundle with the updated scanner.

## 1.0.5 - 2026-10-13

- Pin the cross-platform reproducible archive build and current scanner releases.

## 1.0.4 - 2026-10-13

- Pin ModRelease Studio v0.3.75 and Paradox Mod Workbench v0.2.6.
- Refresh the unified scanner launcher and product information for the current releases.

## 1.0.3 - 2026-10-13

- Reject malformed scanner reports without a findings list instead of treating them as clean.
- Include the fail-closed aggregator from the free release.

## 1.0.2 - 2026-10-12

- Pin ModRelease Studio v0.3.73.
- Refresh the launcher and product information for the matching scanner release.

## 1.0.1 - 2026-10-12

- Refresh the Windows launcher and report builder from Paradox Mod Quality Gate v1.0.57.
- Pin ModRelease Studio v0.3.72 and Paradox Mod Workbench v0.2.5.
- Include the current PowerShell GUI, unified SARIF export, usage notes, and MIT license in the reproducible archive.

## 1.0.0 - 2026-10-08

- Initial Windows GUI bundle for batch scanning mod folders and ZIP archives.
