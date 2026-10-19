# Changelog

## Unreleased

- Refresh the Windows Pro bundle to v1.0.10 and pin its launcher to ModRelease Studio v0.3.82 and Paradox Mod Workbench v0.2.8.
- Add regressions that keep Pro package metadata and scanner pins aligned.

## 1.0.68 - 2026-10-20

- Pin the free GitHub Action and CLI installation example to Paradox Mod Workbench v0.2.8, which retains `replace_path` declarations.
- Keep the separately versioned Pro v1.0.9 package and its scanner pins unchanged; this Action release does not publish a Pro update.

## 1.0.67 - 2026-10-17

- Pin the free GitHub Action and CLI installation example to ModRelease Studio v0.3.82, which detects secrets in environment files and quoted AWS secret-key fields.
- Keep the separately versioned Pro v1.0.9 bundle pinned to ModRelease Studio v0.3.78; this Action release does not refresh its archive.

## 1.0.66 - 2026-10-15

- Pin the free GitHub Action and CLI installation example to ModRelease Studio v0.3.81, which fixes absolute path disclosure in filesystem error reports.
- Keep the separately versioned Pro v1.0.9 bundle pinned to ModRelease Studio v0.3.78; the Pro archive itself is not refreshed by this Action release.

## 1.0.65 - 2026-10-13

- Pin ModRelease Studio v0.3.78 across the GitHub Action and bundled Windows Pro launcher.
- Refresh the Pro package to v1.0.9 and update integration/package regressions.

## 1.0.64 - 2026-10-13

- Document the no-reinstall -SkipInstall launch path for the Windows Pro bundle after the pinned scanners are installed.
- Refresh the bundled Pro package to v1.0.8.

## 1.0.63 - 2026-10-13

- Pin Paradox Mod Workbench v0.2.7 across the Action, docs, CI, and Pro launcher.
- Refresh the Windows Pro bundle to v1.0.7.

## 1.0.62 - 2026-10-13

- Pin ModRelease Studio v0.3.77 across the GitHub Action, Pro launcher, install guide, and CI.
- Refresh the Windows Pro bundle to v1.0.6 and update its package regression checks.

## 1.0.61 - 2026-10-13

- Normalize text line endings in the Pro ZIP builder so Windows and Linux produce identical archives.
- Add a regression test that builds the paid package from LF and CRLF source trees.
- Refresh the Windows Pro bundle to v1.0.5 and align the README and package checks.

## 1.0.60 - 2026-10-13

- Pin ModRelease Studio v0.3.75 and Paradox Mod Workbench v0.2.6 across the Action and Pro launcher.
- Refresh the Windows Pro bundle to v1.0.4 and align the install guide and CI version checks.

## 1.0.59 - 2026-10-13

- Reject scanner reports without a `findings` array instead of treating malformed data as a clean scan.
- Refresh the Windows Pro bundle to v1.0.3 with the fail-closed report aggregator.
- Update examples and package regression checks for the current Action release.

## 1.0.58 - 2026-10-12

- Pin ModRelease Studio v0.3.73 across the Action, Pro launcher, install guide, and CI.
- Refresh the paid Windows bundle to Pro v1.0.2 and regenerate its versioned ZIP.
- Update examples and tests to assert the scanner and bundle pins.

## 1.0.57 - 2026-10-12

- Add a reproducible Windows Pro package builder and refresh the paid bundle to Pro v1.0.1 with current scanner pins.
- Update README examples to the current GitHub Action release.

## 1.0.56 - 2026-10-12

- Pin ModRelease Studio v0.3.72 across the GitHub Action, Pro launcher, install guide, and CI.

## 1.0.55 - 2026-10-12

- Pin ModRelease Studio v0.3.71 across the Action, Pro launcher, install guide, and CI.

## 1.0.54 - 2026-10-12

- Pin ModRelease Studio v0.3.70 across the GitHub Action, Pro launcher, install guide, and CI.

## 1.0.53 - 2026-10-12

- Pin Paradox Mod Workbench v0.2.5 across the Action, Windows Pro launcher, install guide, and CI.

## 1.0.52 - 2026-10-12

- Pin ModRelease Studio v0.3.69 across the GitHub Action, Pro launcher, install guide, and CI; update release examples and add a pin-consistency regression check.

## 1.0.51 - 2026-10-12

- Pin ModRelease Studio v0.3.68 across the GitHub Action, Pro launcher, install guide, and CI.

## 1.0.49 - 2026-10-12

- Pin ModRelease Studio v0.3.68 across the GitHub Action, Pro launcher, install guide, and CI.

## 1.0.46 - 2026-10-12

- Pin ModRelease Studio v0.3.63 in the Action, Windows Pro launcher, install guide, and CI so all users receive the corrected release guidance and current product page.
- Refresh README examples to Paradox Mod Quality Gate v1.0.46.

## 1.0.45 - 2026-10-12

- Pin ModRelease Studio v0.3.62 in the GitHub Action, Pro launcher, and install guide so consumers receive fine-grained GitHub token detection.
- Refresh release examples and scanner integration checks for v0.3.62.

## 1.0.44 - 2026-10-12

- Pin Paradox Mod Workbench v0.2.4 in the GitHub Action, Windows Pro launcher, and install guide.
- Verify the installed Workbench version and prevent stale release examples in README from returning.

## 1.0.43 - 2026-10-12

- Refresh all README examples to Gate v1.0.43 and use checkout v7 consistently.

## 1.0.42 - 2026-10-12

- Pin ModRelease Studio v0.3.61 in the GitHub Action, Pro launcher, and install guide; refresh README examples to this release and assert the exact scanner version in CI.

## 1.0.41 - 2026-10-12

- Pin ModRelease Studio v0.3.60 in the GitHub Action, Pro launcher, and install guide; assert the exact scanner version in CI.

## 1.0.40 - 2026-10-12

- Pin ModRelease Studio v0.3.59 and Paradox Mod Workbench v0.2.3 in the Action, Windows Pro launcher, and install guide; verify exact scanner versions in CI.

## 1.0.38 - 2026-10-12

- Export the unified findings as relative-path SARIF 2.1.0, expose the file from the Action, and include it in GitHub artifacts and Pro reports.
- Add an opt-in Code Scanning upload example; the Action itself does not request extra token permissions.

## 1.0.37 - 2026-10-12

- Pin ModRelease Studio v0.3.58 and Paradox Mod Workbench v0.2.2 in the GitHub Action, Pro launcher, and install guide; align the CI version assertion.

## 1.0.36 - 2026-10-11

- Pin ModRelease Studio v0.3.57 in the GitHub Action, manual install guide, and Pro launcher.
- The scanner now prunes paths and reports `READ_METADATA` if directory junction metadata cannot be checked; CI verifies the combined gate thresholds end to end.

## 1.0.35 - 2026-10-11

- Verify that an emitted `JUNCTION` warning passes `gate: error` but blocks `gate: warning`.
- Keep the scanner pinned to ModRelease Studio v0.3.56.

## 1.0.34 - 2026-10-11

- Pin ModRelease Studio v0.3.56 so folder scans do not traverse Windows directory junctions.
- Keep the combined gate and Pro launcher aligned with the released scanner.
- Assert the exact scanner version in CI.

# Changelog

## 1.0.55 - 2026-10-12

- Pin ModRelease Studio v0.3.71 across the Action, Pro launcher, install guide, and CI.

## 1.0.49 - 2026-10-12

- Pin ModRelease Studio v0.3.68 across the GitHub Action, Pro launcher, install guide, and CI.

## 1.0.33 - 2026-10-11

- Pin ModRelease Studio v0.3.53 so ZIP release scans still inspect `.git` and other normally ignored directory names for secrets.
- Verify a synthetic archived `.git` secret is reported in CI.


## 1.0.32 - 2026-10-11

- Correct the traversal integration fixture boundary: account for the OS-junk file in the indexed-entry limit.
- Retain the pre-index pruning regression for ignored folders.



## 1.0.30 - 2026-10-11

- Pin ModRelease Studio v0.3.50, including generated-folder exclusions and OS-junk warnings.
- Verify scanner traversal policy in CI.


## 1.0.29 - 2026-10-11

- Verify `LARGE_TEXT_FILE` reaches the combined report; `gate: error` allows the warning and `gate: warning` blocks.


## 1.0.28 - 2026-10-11

- Pin ModRelease Studio v0.3.46 and cover the new `LARGE_TEXT_FILE` growth warning in CI.

## 1.0.27 - 2026-10-11

- Select the intended synthetic finding by rule code in CI, avoiding an order-dependent assertion.
- Keep the scanner pinned to ModRelease Studio v0.3.44.

## 1.0.26 - 2026-10-11

- Advance the pinned ModRelease Studio scanner to v0.3.44 for safe Unicode report serialization.
- Add an end-to-end Action fixture proving unified artifacts contain visible escapes for bidi and line separators.

## 1.0.25 - 2026-10-11

- Make control, bidi, C1, and Unicode line/paragraph separators visible in JSON, Markdown, and GitHub annotations without changing parsed JSON values.
- Escape untrusted Markdown text/HTML in findings and repair the lagging report VERSION metadata.
- Add hostile Unicode regression coverage across all three output formats; keep scanner pins at v0.3.25.

## 1.0.24 - 2026-10-11

- Assert in CI that the composite Action installs the exact pinned ModRelease Studio v0.3.25.
- Scanner pins and runtime behavior are unchanged; this release strengthens integration verification only.

## 1.0.23 - 2026-10-11

- Pin the composite Action, local install example, and Windows Pro launcher to ModRelease Studio v0.3.25, including the symlink-safe directory read fix.
- Refresh the Quick Start Action tag to v1.0.23.


## 1.0.22 - 2026-10-11

- Escape control characters, pipes, and backticks in untrusted finding paths so Markdown reports remain structurally safe.


## 1.0.21 - 2026-10-11

- Add regression coverage proving absolute POSIX and Windows finding paths are reduced to basenames in shared reports.


## 1.0.20 - 2026-10-11

- Pin ModRelease Studio v0.3.16, which omits local parent paths from shareable reports.
- Refresh the Quick Start Action tag.

## 1.0.19 - 2026-10-11

- Pin the Action and local scanner installs to ModRelease Studio v0.3.15.
- Refresh the Quality Gate quick-start to v1.0.19.

## 1.0.18 - 2026-10-11

- Pin the Action and local scanner installs to ModRelease Studio v0.3.14.
- Refresh the Quality Gate quick-start to v1.0.18.

## 1.0.17 - 2026-10-11

- Pin the Action and local scanner installs to ModRelease Studio v0.3.13.
- Refresh the Quality Gate quick-start to v1.0.17.

## 1.0.16 - 2026-10-11

- Pin the Action and local scanner installs to ModRelease Studio v0.3.12.
- Refresh the Quality Gate quick-start to v1.0.16.

## 1.0.15 - 2026-10-11

- Pin the Action and local scanner installs to ModRelease Studio v0.3.11.
- Refresh the Quality Gate quick-start to v1.0.15.

## 1.0.14 - 2026-10-11

- Pin the Action and local scanner installs to ModRelease Studio v0.3.10.
- Refresh the Quality Gate quick-start to v1.0.14.

## 1.0.13 - 2026-10-11

- Pin the Action and local scanner installs to ModRelease Studio v0.3.9.
- Refresh the Quality Gate quick-start to v1.0.13.

## 1.0.12 - 2026-10-11

- Pin scanner installs to ModRelease Studio v0.3.8 with cross-platform path collision checks.
- Refresh the Quality Gate quick-start to v1.0.12.

## 1.0.11 - 2026-10-11

- Pin scanner installs and examples to ModRelease Studio v0.3.7.
- Refresh the Quality Gate quick-start to v1.0.11.

## 1.0.10 - 2026-10-11

- Pin scanner installs and policy examples to ModRelease Studio v0.3.6.
- Refresh the Quality Gate quick-start to v1.0.10.

## 1.0.9 - 2026-10-11

- Pin the ModRelease Studio Action install to v0.3.5.
- Refresh the Quality Gate quick-start to v1.0.9.

## 1.0.8 - 2026-10-11

- Centralize workspace path validation and cover parent traversal, outside symlinks, missing files, and directories with unit tests.
- Keep the aggregate report version synchronized with the release.
- Refresh the quick-start pin to v1.0.8.

## 1.0.7 - 2026-10-11

- Add a workspace-contained `config-file` input for ModRelease Studio policies.
- Prove an ERROR-level required-path finding blocks the default gate in CI.
- Document project-specific policy setup.

## 1.0.6 - 2026-10-11

- Pin Action and Pro scanner installs to ModRelease Studio v0.3.4.
- Refresh the quick-start to Paradox Mod Quality Gate v1.0.6.

## 1.0.5 - 2026-10-11

- Pin the scanner install examples to ModRelease Studio v0.3.2 so the combined gate can use required-path policies.
- Refresh the quick-start to Paradox Mod Quality Gate v1.0.5.

## 1.0.4 — 2026-10-11

- Add GitHub Funding metadata with verified Buy Me a Coffee and Gumroad links.
- Refresh the quick-start action tag.

## 1.0.3 — 2026-10-11

- Refresh the GitHub Action and local install examples to use ModRelease Studio v0.3.1.
- Update the workflow example to the current Paradox Mod Quality Gate tag.

## 1.0.2 — 2026-10-10

- Add CI, version and license badges to the README.

## 1.0.1 — 2026-10-08

- Added direct links to the published Boosty Pro package and public announcement.

## 1.0.0 — 2026-10-08

- First public release of the combined GitHub Action and unified JSON/Markdown report.
- Added bounded GitHub annotations and `error` / `warning` / `never` gates.
- Added Windows Pro Edition batch launcher and report export pack.
