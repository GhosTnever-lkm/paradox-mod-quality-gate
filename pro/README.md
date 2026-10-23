# Paradox Mod Quality Gate Pro Edition

Version: **1.0.11**. This Windows convenience bundle runs the current free scanners: ModRelease Studio v0.3.90 and Paradox Mod Workbench v0.2.13.

## Included

- `Start-Pro.ps1` installs the pinned free scanner versions, then opens the Windows GUI.
- `ModGate-Pro.ps1` accepts multiple mod folders and ZIPs, runs both scanners, and exports unified JSON, Markdown, and HTML reports.
- The unified report is also exported as SARIF 2.1.0 for optional GitHub Code Scanning upload.
- A dated output folder is created under **Documents\Paradox Mod Quality Gate Reports** for each run.

## Requirements

- Windows 10/11, PowerShell 7, Python 3.11+, and internet access for the first scanner installation.
- No administrator access is needed. The scripts do not change the execution policy; launch them from PowerShell 7 with `-File`.
- For an offline run after installing both scanners, start with `-SkipInstall`.

See `CHANGELOG.md` for Pro bundle changes. The report aggregator rejects malformed scanner reports without a findings list instead of labeling them clean. This is a convenience package; it does not add hidden scanner rules, validate game launch, or guarantee mod compatibility.

## Start

Extract the archive, open PowerShell 7 in the extracted `pro` folder, then run:

```powershell
pwsh -NoProfile -File .\Start-Pro.ps1
```

The interface only launches the free scanner tools. A report with no findings is not proof that the game launches or that two mods are fully compatible.


### Reusing an existing scanner installation

The first launch installs the pinned scanner packages and therefore needs an internet connection. After both packages are installed, run without reinstalling them:

```powershell
pwsh -NoProfile -File .\Start-Pro.ps1 -SkipInstall
```
