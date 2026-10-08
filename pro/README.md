# Paradox Mod Quality Gate Pro Edition

## Included

- `Start-Pro.ps1` installs the pinned free scanner versions, then opens the Windows GUI.
- `ModGate-Pro.ps1` accepts multiple mod folders and ZIPs, runs both scanners, and exports unified JSON, Markdown, and HTML reports.
- A dated output folder is created under **Documents\Paradox Mod Quality Gate Reports** for each run.

## Requirements

- Windows 10/11, PowerShell 7, Python 3.11+, and internet access for the first scanner installation.
- No administrator access is needed. The scripts do not change the execution policy; launch them from PowerShell 7 with `-File`.
- For an offline run after installing both scanners, start with `-SkipInstall`.

## Start

Extract the archive, open PowerShell 7 in the extracted `pro` folder, then run:

```powershell
pwsh -NoProfile -File .\Start-Pro.ps1
```

The interface only launches the free scanner tools. A report with no findings is not proof that the game launches or that two mods are fully compatible.
