param([switch]$SkipInstall)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Get-Command py -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command python -ErrorAction SilentlyContinue }
if (-not $python) { throw 'Python 3.11 or newer is required. Install Python from python.org and retry.' }
$versionText = & $python.Source -c 'import sys; print("%s.%s.%s" % sys.version_info[:3])'
if ($LASTEXITCODE -ne 0 -or $versionText -notmatch '^(\d+)\.(\d+)\.(\d+)$') { throw 'Python could not be started.' }
if ([version]$versionText -lt [version]'3.11') { throw 'Python 3.11 or newer is required.' }
if (-not $SkipInstall) {
    & $python.Source -m pip install --disable-pip-version-check `
      'modrelease-studio @ git+https://github.com/GhosTnever-lkm/modrelease-studio.git@v0.3.4' `
      'paradox-mod-workbench @ git+https://github.com/GhosTnever-lkm/paradox-mod-workbench.git@v0.2.1'
    if ($LASTEXITCODE -ne 0) { throw 'Scanner installation failed.' }
}
& (Join-Path $root 'ModGate-Pro.ps1')
