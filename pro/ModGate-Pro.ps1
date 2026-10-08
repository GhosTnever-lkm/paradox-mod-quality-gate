$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = Split-Path -Parent $root
$outRoot = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Paradox Mod Quality Gate Reports'
New-Item -ItemType Directory -Force -Path $outRoot | Out-Null

function ConvertTo-ProcessArgument([string]$Value) {
  '"' + $Value.Replace('"', '\"') + '"'
}
function Invoke-Tool([string]$Executable, [string[]]$Arguments) {
  $quoted = ($Arguments | ForEach-Object { ConvertTo-ProcessArgument ([string]$_) }) -join ' '
  Start-Process -FilePath $Executable -ArgumentList $quoted -Wait -PassThru -NoNewWindow
}

$form = New-Object Windows.Forms.Form
$form.Text = 'Paradox Mod Quality Gate Pro'
$form.Size = New-Object Drawing.Size(760, 560)
$form.StartPosition = 'CenterScreen'
$form.BackColor = [Drawing.Color]::FromArgb(20, 27, 38)
$form.ForeColor = [Drawing.Color]::White
$form.Font = New-Object Drawing.Font('Segoe UI', 10)

$title = New-Object Windows.Forms.Label
$title.Text = 'Paradox Mod Quality Gate Pro'
$title.Font = New-Object Drawing.Font('Segoe UI Semibold', 19)
$title.Location = New-Object Drawing.Point(24, 18); $title.Size = New-Object Drawing.Size(690, 38)
$form.Controls.Add($title)
$hint = New-Object Windows.Forms.Label
$hint.Text = 'Добавьте папки или ZIP модов. Исходники остаются на компьютере; экспортируются только отчёты.'
$hint.Location = New-Object Drawing.Point(26, 62); $hint.Size = New-Object Drawing.Size(690, 28)
$form.Controls.Add($hint)

$list = New-Object Windows.Forms.ListBox
$list.Location = New-Object Drawing.Point(26, 100); $list.Size = New-Object Drawing.Size(690, 250)
$list.BackColor = [Drawing.Color]::FromArgb(30, 39, 53); $list.ForeColor = [Drawing.Color]::White
$form.Controls.Add($list)

$addFolder = New-Object Windows.Forms.Button
$addFolder.Text = 'Добавить папки'; $addFolder.Location = New-Object Drawing.Point(26, 365); $addFolder.Size = New-Object Drawing.Size(160, 38)
$addZip = New-Object Windows.Forms.Button
$addZip.Text = 'Добавить ZIP'; $addZip.Location = New-Object Drawing.Point(196, 365); $addZip.Size = New-Object Drawing.Size(140, 38)
$remove = New-Object Windows.Forms.Button
$remove.Text = 'Убрать выбранное'; $remove.Location = New-Object Drawing.Point(346, 365); $remove.Size = New-Object Drawing.Size(170, 38)
$scan = New-Object Windows.Forms.Button
$scan.Text = 'Запустить проверку'; $scan.Location = New-Object Drawing.Point(526, 365); $scan.Size = New-Object Drawing.Size(190, 38)
foreach ($button in @($addFolder,$addZip,$remove,$scan)) {
  $button.FlatStyle = 'Flat'; $button.BackColor = [Drawing.Color]::FromArgb(44, 110, 190); $button.ForeColor = [Drawing.Color]::White
  $form.Controls.Add($button)
}
$status = New-Object Windows.Forms.Label
$status.Text = 'Готово'; $status.Location = New-Object Drawing.Point(28, 420); $status.Size = New-Object Drawing.Size(690, 54)
$form.Controls.Add($status)
$open = New-Object Windows.Forms.Button
$open.Text = 'Открыть папку отчётов'; $open.Location = New-Object Drawing.Point(26, 478); $open.Size = New-Object Drawing.Size(200, 34)
$form.Controls.Add($open)

$addFolder.Add_Click({
  $dialog = New-Object Windows.Forms.FolderBrowserDialog
  $dialog.Description = 'Выберите папку мода'
  if ($dialog.ShowDialog() -eq 'OK' -and -not $list.Items.Contains($dialog.SelectedPath)) { [void]$list.Items.Add($dialog.SelectedPath) }
})
$addZip.Add_Click({
  $dialog = New-Object Windows.Forms.OpenFileDialog
  $dialog.Filter = 'ZIP archives (*.zip)|*.zip'; $dialog.Multiselect = $true
  if ($dialog.ShowDialog() -eq 'OK') { foreach ($item in $dialog.FileNames) { if (-not $list.Items.Contains($item)) { [void]$list.Items.Add($item) } } }
})
$remove.Add_Click({ while ($list.SelectedItems.Count -gt 0) { $list.Items.Remove($list.SelectedItems[0]) } })
$open.Add_Click({ Invoke-Item -LiteralPath $outRoot })

$scan.Add_Click({
  if ($list.Items.Count -lt 1) { [Windows.Forms.MessageBox]::Show('Сначала добавьте папку или ZIP.', 'Нет модов') | Out-Null; return }
  $scan.Enabled = $false
  try {
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $target = Join-Path $outRoot $stamp
    New-Item -ItemType Directory -Force -Path $target | Out-Null
    $python = Get-Command py -ErrorAction SilentlyContinue
    if (-not $python) { $python = Get-Command python -ErrorAction Stop }
    $releaseReports = @()
    $index = 0
    foreach ($source in $list.Items) {
      $index++
      $json = Join-Path $target "modrelease-$index.json"
      $md = Join-Path $target "modrelease-$index.md"
      $proc = Invoke-Tool $python.Source @('-m','modrelease_studio','scan',[string]$source,'--json-out',$json,'--md-out',$md)
      if ($proc.ExitCode -notin @(0,1) -or -not (Test-Path $json)) { throw "ModRelease Studio failed on item $index (exit $($proc.ExitCode))." }
      $releaseReports += Get-Content -Raw -Encoding UTF8 $json | ConvertFrom-Json
    }
    $pmwJson = Join-Path $target 'workbench.json'
    $pmwArgs = @('-m','paradox_mod_workbench','scan') + @($list.Items | ForEach-Object { [string]$_ }) + @('--format','json','--output',$pmwJson,'--fail-on','never')
    $proc = Invoke-Tool $python.Source $pmwArgs
    if ($proc.ExitCode -ne 0 -or -not (Test-Path $pmwJson)) { throw "Paradox Mod Workbench failed (exit $($proc.ExitCode))." }

    # Merge per-mod release findings with the pack Workbench report without adding machine-specific source paths.
    $mr = [ordered]@{ version='0.2.1'; findings=@() }
    foreach ($item in $releaseReports) { $mr.findings += @($item.findings) }
    $mrPath = Join-Path $target 'combined-modrelease.json'
    $mr | ConvertTo-Json -Depth 30 | Set-Content -Encoding UTF8 $mrPath
    $aggregate = Join-Path $repo 'runner/aggregate.py'
    $unifiedJson = Join-Path $target 'report.json'; $unifiedMd = Join-Path $target 'report.md'
    $proc = Invoke-Tool $python.Source @($aggregate,'--modrelease',$mrPath,'--workbench',$pmwJson,'--json-out',$unifiedJson,'--md-out',$unifiedMd,'--gate','never')
    if ($proc.ExitCode -ne 0) { throw 'Unable to build unified report.' }
    $report = Get-Content -Raw -Encoding UTF8 $unifiedJson | ConvertFrom-Json
    $report.findings | Select-Object severity,source,code,path,line,message | ConvertTo-Html -Title 'Paradox Mod Quality Gate Pro' -PreContent "<h1>Paradox Mod Quality Gate Pro</h1><p>$($report.counts.error) errors · $($report.counts.warning) warnings · $($report.counts.notice) notices</p>" | Set-Content -Encoding UTF8 (Join-Path $target 'report.html')
    $status.Text = "Готово. HTML, Markdown и JSON отчёты сохранены: $target"
    [Windows.Forms.MessageBox]::Show("Проверка завершена. Отчёты сохранены в:`n$target", 'Готово') | Out-Null
  } catch {
    $status.Text = "Ошибка: $($_.Exception.Message)"
    [Windows.Forms.MessageBox]::Show($_.Exception.Message, 'Ошибка проверки') | Out-Null
  } finally { $scan.Enabled = $true }
})
[void]$form.ShowDialog()
