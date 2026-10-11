# Changelog

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
