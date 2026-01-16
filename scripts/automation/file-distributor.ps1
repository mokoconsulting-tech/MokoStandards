<#
.SYNOPSIS
  Enterprise utility to distribute a selected source file into folders under a selected root directory,
  with GUI selection, depth control, per-folder confirmation, dry run, overwrite control, and audit logging.

.DESCRIPTION
  Operating model:
    - GUI: pick Source File
    - GUI: pick Root Folder
    - GUI: pick Options (DryRun, Overwrite, Depth, ConfirmEach, LogPath)
    - Enumerate target folders by depth (0..N or -1 full recursive)
    - Optionally confirm each folder (Yes, No, Yes to All, Cancel)
    - Copy file into each folder in scope
    - Produce structured audit outputs:
        - CSV log (default)
        - JSON log (parallel)
    - Non-interactive safe defaults:
        - DryRun default = enabled
        - Overwrite default = disabled

  Depth modes:
    - 0  : root only
    - 1  : root + immediate subfolders
    - N  : root + N levels
    - -1 : full recursive

.NOTES
  - Requires WinForms (Windows PowerShell 5.1 or PowerShell 7+ on Windows with WindowsDesktop).
  - Designed for controlled execution and traceability.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Windows.Forms | Out-Null
Add-Type -AssemblyName System.Drawing | Out-Null

function Select-SourceFile {
  $dialog = New-Object System.Windows.Forms.OpenFileDialog
  $dialog.Title = "Select the source file to distribute"
  $dialog.Filter = "All files (*.*)|*.*"
  $dialog.Multiselect = $false

  $result = $dialog.ShowDialog()
  if ($result -ne [System.Windows.Forms.DialogResult]::OK -or [string]::IsNullOrWhiteSpace($dialog.FileName)) {
    throw "No source file selected."
  }
  return $dialog.FileName
}

function Select-RootFolder {
  $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
  $dialog.Description = "Select the root directory"
  $dialog.ShowNewFolderButton = $false

  $result = $dialog.ShowDialog()
  if ($result -ne [System.Windows.Forms.DialogResult]::OK -or [string]::IsNullOrWhiteSpace($dialog.SelectedPath)) {
    throw "No root directory selected."
  }
  return $dialog.SelectedPath
}

function Get-FoldersByDepth {
  param(
    [Parameter(Mandatory=$true)][string]$RootDir,
    [Parameter(Mandatory=$true)][int]$Depth,
    [Parameter(Mandatory=$false)][bool]$IncludeHidden = $true
  )

  if (-not (Test-Path -LiteralPath $RootDir -PathType Container)) {
    throw "Root directory not found: $RootDir"
  }

  $folders = New-Object System.Collections.Generic.List[string]
  $rootItem = Get-Item -LiteralPath $RootDir
  $folders.Add($rootItem.FullName)

  if ($Depth -eq 0) {
    return $folders
  }

  $getChildArgs = @{
    Directory = $true
    ErrorAction = 'SilentlyContinue'
  }
  if ($IncludeHidden) {
    $getChildArgs.Force = $true
  }

  if ($Depth -eq -1) {
    Get-ChildItem -LiteralPath $RootDir -Recurse @getChildArgs |
      ForEach-Object { $folders.Add($_.FullName) }
    return $folders
  }

  if ($Depth -lt -1) {
    throw "Invalid depth '$Depth'. Use -1 for full recursion, or 0..N for limited depth."
  }

  $currentLevel = New-Object System.Collections.Generic.List[string]
  $currentLevel.Add($rootItem.FullName)

  for ($level = 1; $level -le $Depth; $level++) {
    $nextLevel = New-Object System.Collections.Generic.List[string]

    foreach ($parent in $currentLevel) {
      Get-ChildItem -LiteralPath $parent @getChildArgs |
        ForEach-Object {
          $nextLevel.Add($_.FullName)
          $folders.Add($_.FullName)
        }
    }

    if ($nextLevel.Count -eq 0) { break }
    $currentLevel = $nextLevel
  }

  return $folders
}

function Ensure-Directory {
  param([Parameter(Mandatory=$true)][string]$Path)

  if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
  }
}

function Get-DefaultLogPaths {
  $base = Join-Path -Path $env:USERPROFILE -ChildPath "Documents\FileDistributorLogs"
  Ensure-Directory -Path $base

  $stamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
  return [pscustomobject]@{
    Folder = $base
    Csv    = Join-Path -Path $base -ChildPath ("file-distributor_{0}.csv" -f $stamp)
    Json   = Join-Path -Path $base -ChildPath ("file-distributor_{0}.json" -f $stamp)
  }
}

function Show-OptionsDialog {
  param(
    [Parameter(Mandatory=$true)][string]$SourceFile,
    [Parameter(Mandatory=$true)][string]$RootDir
  )

  $defaults = Get-DefaultLogPaths

  $form = New-Object System.Windows.Forms.Form
  $form.Text = "Distribution Options"
  $form.StartPosition = "CenterScreen"
  $form.FormBorderStyle = "FixedDialog"
  $form.MaximizeBox = $false
  $form.MinimizeBox = $false
  $form.ClientSize = New-Object System.Drawing.Size(760, 420)
  $form.Topmost = $true

  $font = New-Object System.Drawing.Font("Segoe UI", 9)

  $lblSource = New-Object System.Windows.Forms.Label
  $lblSource.AutoSize = $false
  $lblSource.Location = New-Object System.Drawing.Point(12, 12)
  $lblSource.Size = New-Object System.Drawing.Size(736, 40)
  $lblSource.Font = $font
  $lblSource.Text = "Source file:`r`n$SourceFile"

  $lblRoot = New-Object System.Windows.Forms.Label
  $lblRoot.AutoSize = $false
  $lblRoot.Location = New-Object System.Drawing.Point(12, 58)
  $lblRoot.Size = New-Object System.Drawing.Size(736, 40)
  $lblRoot.Font = $font
  $lblRoot.Text = "Root folder:`r`n$RootDir"

  $chkDryRun = New-Object System.Windows.Forms.CheckBox
  $chkDryRun.Location = New-Object System.Drawing.Point(12, 110)
  $chkDryRun.Size = New-Object System.Drawing.Size(320, 24)
  $chkDryRun.Font = $font
  $chkDryRun.Text = "Dry run (no files written)"
  $chkDryRun.Checked = $true

  $chkOverwrite = New-Object System.Windows.Forms.CheckBox
  $chkOverwrite.Location = New-Object System.Drawing.Point(12, 138)
  $chkOverwrite.Size = New-Object System.Drawing.Size(320, 24)
  $chkOverwrite.Font = $font
  $chkOverwrite.Text = "Overwrite if file exists"
  $chkOverwrite.Checked = $false

  $chkConfirmEach = New-Object System.Windows.Forms.CheckBox
  $chkConfirmEach.Location = New-Object System.Drawing.Point(12, 166)
  $chkConfirmEach.Size = New-Object System.Drawing.Size(420, 24)
  $chkConfirmEach.Font = $font
  $chkConfirmEach.Text = "Confirm each folder (Yes, No, Yes to All, Cancel)"
  $chkConfirmEach.Checked = $false

  $chkIncludeHidden = New-Object System.Windows.Forms.CheckBox
  $chkIncludeHidden.Location = New-Object System.Drawing.Point(12, 194)
  $chkIncludeHidden.Size = New-Object System.Drawing.Size(320, 24)
  $chkIncludeHidden.Font = $font
  $chkIncludeHidden.Text = "Include hidden folders"
  $chkIncludeHidden.Checked = $true

  $grpDepth = New-Object System.Windows.Forms.GroupBox
  $grpDepth.Text = "Child Folder Depth"
  $grpDepth.Font = $font
  $grpDepth.Location = New-Object System.Drawing.Point(12, 226)
  $grpDepth.Size = New-Object System.Drawing.Size(736, 80)

  $lblDepth = New-Object System.Windows.Forms.Label
  $lblDepth.Font = $font
  $lblDepth.Location = New-Object System.Drawing.Point(12, 30)
  $lblDepth.Size = New-Object System.Drawing.Size(220, 20)
  $lblDepth.Text = "Depth (0 = root, -1 = full):"

  $numDepth = New-Object System.Windows.Forms.NumericUpDown
  $numDepth.Font = $font
  $numDepth.Location = New-Object System.Drawing.Point(235, 28)
  $numDepth.Size = New-Object System.Drawing.Size(90, 24)
  $numDepth.Minimum = -1
  $numDepth.Maximum = 50
  $numDepth.Value = 1

  $lblDepthHelp = New-Object System.Windows.Forms.Label
  $lblDepthHelp.Font = $font
  $lblDepthHelp.Location = New-Object System.Drawing.Point(340, 26)
  $lblDepthHelp.Size = New-Object System.Drawing.Size(380, 44)
  $lblDepthHelp.Text = "0 = root only`r`n1 = root + 1 level`r`n-1 = full recursive"

  $grpDepth.Controls.AddRange(@($lblDepth, $numDepth, $lblDepthHelp))

  $grpLog = New-Object System.Windows.Forms.GroupBox
  $grpLog.Text = "Audit Logging"
  $grpLog.Font = $font
  $grpLog.Location = New-Object System.Drawing.Point(12, 314)
  $grpLog.Size = New-Object System.Drawing.Size(736, 56)

  $lblLog = New-Object System.Windows.Forms.Label
  $lblLog.Font = $font
  $lblLog.Location = New-Object System.Drawing.Point(12, 24)
  $lblLog.Size = New-Object System.Drawing.Size(90, 20)
  $lblLog.Text = "Log folder:"

  $txtLogFolder = New-Object System.Windows.Forms.TextBox
  $txtLogFolder.Font = $font
  $txtLogFolder.Location = New-Object System.Drawing.Point(105, 22)
  $txtLogFolder.Size = New-Object System.Drawing.Size(520, 24)
  $txtLogFolder.Text = $defaults.Folder

  $btnBrowseLog = New-Object System.Windows.Forms.Button
  $btnBrowseLog.Font = $font
  $btnBrowseLog.Text = "Browse"
  $btnBrowseLog.Location = New-Object System.Drawing.Point(635, 20)
  $btnBrowseLog.Size = New-Object System.Drawing.Size(88, 26)

  $btnBrowseLog.Add_Click({
    $fb = New-Object System.Windows.Forms.FolderBrowserDialog
    $fb.Description = "Select a folder for audit logs"
    $fb.ShowNewFolderButton = $true
    $res = $fb.ShowDialog()
    if ($res -eq [System.Windows.Forms.DialogResult]::OK -and -not [string]::IsNullOrWhiteSpace($fb.SelectedPath)) {
      if (Test-Path -LiteralPath $fb.SelectedPath -PathType Container) {
        $txtLogFolder.Text = $fb.SelectedPath
      } else {
        [System.Windows.Forms.MessageBox]::Show(
          "Selected path is not a valid directory.",
          "Invalid Path",
          [System.Windows.Forms.MessageBoxButtons]::OK,
          [System.Windows.Forms.MessageBoxIcon]::Warning
        ) | Out-Null
      }
    }
  })

  $grpLog.Controls.AddRange(@($lblLog, $txtLogFolder, $btnBrowseLog))

  $btnOk = New-Object System.Windows.Forms.Button
  $btnOk.Text = "Run"
  $btnOk.Font = $font
  $btnOk.Size = New-Object System.Drawing.Size(90, 30)
  $btnOk.Location = New-Object System.Drawing.Point(560, 378)
  $btnOk.DialogResult = [System.Windows.Forms.DialogResult]::OK

  $btnCancel = New-Object System.Windows.Forms.Button
  $btnCancel.Text = "Cancel"
  $btnCancel.Font = $font
  $btnCancel.Size = New-Object System.Drawing.Size(90, 30)
  $btnCancel.Location = New-Object System.Drawing.Point(658, 378)
  $btnCancel.DialogResult = [System.Windows.Forms.DialogResult]::Cancel

  $form.AcceptButton = $btnOk
  $form.CancelButton = $btnCancel

  $form.Controls.AddRange(@(
    $lblSource, $lblRoot,
    $chkDryRun, $chkOverwrite, $chkConfirmEach, $chkIncludeHidden,
    $grpDepth,
    $grpLog,
    $btnOk, $btnCancel
  ))

  $result = $form.ShowDialog()
  if ($result -ne [System.Windows.Forms.DialogResult]::OK) {
    throw "Operation cancelled."
  }

  $logFolder = $txtLogFolder.Text.Trim()
  if ([string]::IsNullOrWhiteSpace($logFolder)) {
    throw "Log folder is required for audit readiness."
  }
  Ensure-Directory -Path $logFolder

  $stamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
  $csvPath = Join-Path -Path $logFolder -ChildPath ("file-distributor_{0}.csv" -f $stamp)
  $jsonPath = Join-Path -Path $logFolder -ChildPath ("file-distributor_{0}.json" -f $stamp)

  return [pscustomobject]@{
    DryRun         = [bool]$chkDryRun.Checked
    Overwrite      = [bool]$chkOverwrite.Checked
    ConfirmEach    = [bool]$chkConfirmEach.Checked
    IncludeHidden  = [bool]$chkIncludeHidden.Checked
    Depth          = [int]$numDepth.Value
    LogFolder      = $logFolder
    LogCsvPath     = $csvPath
    LogJsonPath    = $jsonPath
  }
}

function Confirm-FolderAction {
  param(
    [Parameter(Mandatory=$true)][string]$FolderPath,
    [Parameter(Mandatory=$true)][string]$TargetPath,
    [Parameter(Mandatory=$true)][string]$SourceName,
    [Parameter(Mandatory=$true)][bool]$Overwrite,
    [Parameter(Mandatory=$true)][bool]$Exists
  )

  $action = if ($Exists -and $Overwrite) { "OVERWRITE" } elseif ($Exists) { "SKIP" } else { "COPY" }
  
  $form = New-Object System.Windows.Forms.Form
  $form.Text = "Confirm Folder"
  $form.StartPosition = "CenterScreen"
  $form.FormBorderStyle = "FixedDialog"
  $form.MaximizeBox = $false
  $form.MinimizeBox = $false
  $form.ClientSize = New-Object System.Drawing.Size(500, 280)
  $form.Topmost = $true

  $font = New-Object System.Drawing.Font("Segoe UI", 9)

  $lblMessage = New-Object System.Windows.Forms.Label
  $lblMessage.Font = $font
  $lblMessage.Location = New-Object System.Drawing.Point(12, 12)
  $lblMessage.Size = New-Object System.Drawing.Size(476, 200)
  $lblMessage.Text = @(
    "Target folder:",
    $FolderPath,
    "",
    "File:",
    $SourceName,
    "",
    "Target path:",
    $TargetPath,
    "",
    "Planned action: $action"
  ) -join "`r`n"

  $btnYes = New-Object System.Windows.Forms.Button
  $btnYes.Text = "Yes"
  $btnYes.Font = $font
  $btnYes.Size = New-Object System.Drawing.Size(100, 30)
  $btnYes.Location = New-Object System.Drawing.Point(12, 230)
  $btnYes.DialogResult = [System.Windows.Forms.DialogResult]::Yes

  $btnNo = New-Object System.Windows.Forms.Button
  $btnNo.Text = "No"
  $btnNo.Font = $font
  $btnNo.Size = New-Object System.Drawing.Size(100, 30)
  $btnNo.Location = New-Object System.Drawing.Point(118, 230)
  $btnNo.DialogResult = [System.Windows.Forms.DialogResult]::No

  $btnYesToAll = New-Object System.Windows.Forms.Button
  $btnYesToAll.Text = "Yes to All"
  $btnYesToAll.Font = $font
  $btnYesToAll.Size = New-Object System.Drawing.Size(100, 30)
  $btnYesToAll.Location = New-Object System.Drawing.Point(224, 230)
  $btnYesToAll.DialogResult = [System.Windows.Forms.DialogResult]::Retry

  $btnCancel = New-Object System.Windows.Forms.Button
  $btnCancel.Text = "Cancel"
  $btnCancel.Font = $font
  $btnCancel.Size = New-Object System.Drawing.Size(100, 30)
  $btnCancel.Location = New-Object System.Drawing.Point(330, 230)
  $btnCancel.DialogResult = [System.Windows.Forms.DialogResult]::Cancel

  $form.AcceptButton = $btnYes
  $form.CancelButton = $btnCancel

  $form.Controls.AddRange(@($lblMessage, $btnYes, $btnNo, $btnYesToAll, $btnCancel))

  return $form.ShowDialog()
}

function Write-AuditLogs {
  param(
    [Parameter(Mandatory=$true)][System.Collections.Generic.List[object]]$Records,
    [Parameter(Mandatory=$true)][string]$CsvPath,
    [Parameter(Mandatory=$true)][string]$JsonPath
  )

  $Records | Export-Csv -LiteralPath $CsvPath -NoTypeInformation -Encoding UTF8

  $json = $Records | ConvertTo-Json -Depth 6
  [System.IO.File]::WriteAllText($JsonPath, $json, (New-Object System.Text.UTF8Encoding($false)))
}

function Copy-FileToFolders {
  param(
    [Parameter(Mandatory=$true)][string]$SourceFile,
    [Parameter(Mandatory=$true)][string]$RootDir,
    [Parameter(Mandatory=$true)][bool]$DryRun,
    [Parameter(Mandatory=$true)][bool]$Overwrite,
    [Parameter(Mandatory=$true)][int]$Depth,
    [Parameter(Mandatory=$true)][bool]$ConfirmEach,
    [Parameter(Mandatory=$false)][bool]$IncludeHidden = $true,
    [Parameter(Mandatory=$true)][string]$LogCsvPath,
    [Parameter(Mandatory=$true)][string]$LogJsonPath
  )

  if (-not (Test-Path -LiteralPath $SourceFile -PathType Leaf)) {
    throw "Source file not found: $SourceFile"
  }
  if (-not (Test-Path -LiteralPath $RootDir -PathType Container)) {
    throw "Root directory not found: $RootDir"
  }

  $runId = [guid]::NewGuid().ToString()
  $start = Get-Date

  $sourceItem = Get-Item -LiteralPath $SourceFile
  $sourceName = $sourceItem.Name
  $sourceSize = $sourceItem.Length
  $sourceHash = (Get-FileHash -LiteralPath $SourceFile -Algorithm SHA256).Hash

  $folders = Get-FoldersByDepth -RootDir $RootDir -Depth $Depth -IncludeHidden $IncludeHidden

  $records = New-Object System.Collections.Generic.List[object]

  $stats = [ordered]@{
    RunId        = $runId
    StartedAt    = $start.ToString("o")
    TotalFolders = $folders.Count
    Skipped      = 0
    ConfirmSkip  = 0
    Copied       = 0
    Overwritten  = 0
    Errors       = 0
    Cancelled    = $false
  }

  $yesToAll = $false

  foreach ($folderPath in $folders) {
    $targetPath = Join-Path -Path $folderPath -ChildPath $sourceName
    $exists = Test-Path -LiteralPath $targetPath -PathType Leaf

    $plannedAction =
      if ($exists -and -not $Overwrite) { "SkipExists" }
      elseif ($exists -and $Overwrite)  { "Overwrite" }
      else                             { "Copy" }

    $decision = "Auto"
    $status = "Planned"

    try {
      if ($ConfirmEach -and -not $yesToAll) {
        $mb = Confirm-FolderAction -FolderPath $folderPath -TargetPath $targetPath -SourceName $sourceName -Overwrite $Overwrite -Exists $exists
        if ($mb -eq [System.Windows.Forms.DialogResult]::No) {
          $decision = "UserNo"
          $status = "SkippedByUser"
          $stats.ConfirmSkip++
          $records.Add([pscustomobject]@{
            RunId          = $runId
            Timestamp      = (Get-Date).ToString("o")
            Folder         = $folderPath
            TargetPath     = $targetPath
            ActionPlanned  = $plannedAction
            ActionTaken    = "Skip"
            Decision       = $decision
            DryRun         = $DryRun
            Overwrite      = $Overwrite
            Depth          = $Depth
            SourceFile     = $SourceFile
            SourceSize     = $sourceSize
            SourceSha256   = $sourceHash
            Result         = $status
            Error          = ""
          })
          Write-Host "[SKIP] User declined: $targetPath"
          continue
        }
        if ($mb -eq [System.Windows.Forms.DialogResult]::Cancel) {
          $decision = "UserCancel"
          $stats.Cancelled = $true
          $records.Add([pscustomobject]@{
            RunId          = $runId
            Timestamp      = (Get-Date).ToString("o")
            Folder         = $folderPath
            TargetPath     = $targetPath
            ActionPlanned  = $plannedAction
            ActionTaken    = "Abort"
            Decision       = $decision
            DryRun         = $DryRun
            Overwrite      = $Overwrite
            Depth          = $Depth
            SourceFile     = $SourceFile
            SourceSize     = $sourceSize
            SourceSha256   = $sourceHash
            Result         = "Cancelled"
            Error          = ""
          })
          Write-Host "[CANCEL] User cancelled at: $folderPath"
          break
        }
        if ($mb -eq [System.Windows.Forms.DialogResult]::Retry) {
          $yesToAll = $true
          $decision = "UserYesToAll"
          Write-Host "[INFO] Yes to All selected - remaining folders will proceed without confirmation"
        } else {
          $decision = "UserYes"
        }
      } elseif ($yesToAll) {
        $decision = "UserYesToAll"
      }

      if ($exists -and -not $Overwrite) {
        $stats.Skipped++
        $records.Add([pscustomobject]@{
          RunId          = $runId
          Timestamp      = (Get-Date).ToString("o")
          Folder         = $folderPath
          TargetPath     = $targetPath
          ActionPlanned  = "SkipExists"
          ActionTaken    = "Skip"
          Decision       = $decision
          DryRun         = $DryRun
          Overwrite      = $Overwrite
          Depth          = $Depth
          SourceFile     = $SourceFile
          SourceSize     = $sourceSize
          SourceSha256   = $sourceHash
          Result         = "SkippedExists"
          Error          = ""
        })
        Write-Host "[SKIP] Exists: $targetPath"
        continue
      }

      if ($DryRun) {
        if ($exists -and $Overwrite) {
          $stats.Overwritten++
          Write-Host "[DRYRUN] Would overwrite: $targetPath"
          $taken = "WouldOverwrite"
        } else {
          $stats.Copied++
          Write-Host "[DRYRUN] Would copy: $targetPath"
          $taken = "WouldCopy"
        }

        $records.Add([pscustomobject]@{
          RunId          = $runId
          Timestamp      = (Get-Date).ToString("o")
          Folder         = $folderPath
          TargetPath     = $targetPath
          ActionPlanned  = $plannedAction
          ActionTaken    = $taken
          Decision       = $decision
          DryRun         = $DryRun
          Overwrite      = $Overwrite
          Depth          = $Depth
          SourceFile     = $SourceFile
          SourceSize     = $sourceSize
          SourceSha256   = $sourceHash
          Result         = "DryRun"
          Error          = ""
        })
        continue
      }

      if ($exists -and $Overwrite) {
        Copy-Item -LiteralPath $SourceFile -Destination $targetPath -Force
        $stats.Overwritten++
        Write-Host "[OK] Overwrote: $targetPath"
        $taken = "Overwrite"
      } else {
        Copy-Item -LiteralPath $SourceFile -Destination $targetPath
        $stats.Copied++
        Write-Host "[OK] Copied: $targetPath"
        $taken = "Copy"
      }

      $records.Add([pscustomobject]@{
        RunId          = $runId
        Timestamp      = (Get-Date).ToString("o")
        Folder         = $folderPath
        TargetPath     = $targetPath
        ActionPlanned  = $plannedAction
        ActionTaken    = $taken
        Decision       = $decision
        DryRun         = $DryRun
        Overwrite      = $Overwrite
        Depth          = $Depth
        SourceFile     = $SourceFile
        SourceSize     = $sourceSize
        SourceSha256   = $sourceHash
        Result         = "Success"
        Error          = ""
      })
    }
    catch {
      $stats.Errors++
      $err = $_.Exception.Message
      Write-Warning "[ERROR] $folderPath -> $err"

      $records.Add([pscustomobject]@{
        RunId          = $runId
        Timestamp      = (Get-Date).ToString("o")
        Folder         = $folderPath
        TargetPath     = $targetPath
        ActionPlanned  = $plannedAction
        ActionTaken    = "Error"
        Decision       = $decision
        DryRun         = $DryRun
        Overwrite      = $Overwrite
        Depth          = $Depth
        SourceFile     = $SourceFile
        SourceSize     = $sourceSize
        SourceSha256   = $sourceHash
        Result         = "Error"
        Error          = $err
      })
    }
  }

  $end = Get-Date
  $stats.EndedAt = $end.ToString("o")

  Write-AuditLogs -Records $records -CsvPath $LogCsvPath -JsonPath $LogJsonPath

  $summary = @(
    "RunId:        $runId",
    "StartedAt:    $($stats.StartedAt)",
    "EndedAt:      $($stats.EndedAt)",
    "TotalFolders: $($stats.TotalFolders)",
    "Copied:       $($stats.Copied)",
    "Overwritten:  $($stats.Overwritten)",
    "Skipped:      $($stats.Skipped)",
    "UserSkipped:  $($stats.ConfirmSkip)",
    "Errors:       $($stats.Errors)",
    "Cancelled:    $($stats.Cancelled)",
    "",
    "Audit CSV:    $LogCsvPath",
    "Audit JSON:   $LogJsonPath"
  ) -join "`r`n"

  [System.Windows.Forms.MessageBox]::Show(
    $summary,
    "Distribution Complete",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Information
  ) | Out-Null

  Write-Host ""
  Write-Host "============================================================"
  Write-Host "Run Summary"
  Write-Host "============================================================"
  $stats.GetEnumerator() | ForEach-Object { "{0,-12}: {1}" -f $_.Key, $_.Value }
  Write-Host "============================================================"
  Write-Host "Audit CSV:  $LogCsvPath"
  Write-Host "Audit JSON: $LogJsonPath"
}

# Main execution
try {
  $source = Select-SourceFile
  $root   = Select-RootFolder
  $opts   = Show-OptionsDialog -SourceFile $source -RootDir $root

  Write-Host ""
  Write-Host "Source file   : $source"
  Write-Host "Root folder   : $root"
  Write-Host "Dry Run       : $($opts.DryRun)"
  Write-Host "Overwrite     : $($opts.Overwrite)"
  Write-Host "ConfirmEach   : $($opts.ConfirmEach)"
  Write-Host "IncludeHidden : $($opts.IncludeHidden)"
  Write-Host "Depth         : $($opts.Depth)  (0=root only, -1=full recursive)"
  Write-Host "Log CSV       : $($opts.LogCsvPath)"
  Write-Host "Log JSON      : $($opts.LogJsonPath)"
  Write-Host ""

  Copy-FileToFolders `
    -SourceFile $source `
    -RootDir $root `
    -DryRun $opts.DryRun `
    -Overwrite $opts.Overwrite `
    -Depth $opts.Depth `
    -ConfirmEach $opts.ConfirmEach `
    -IncludeHidden $opts.IncludeHidden `
    -LogCsvPath $opts.LogCsvPath `
    -LogJsonPath $opts.LogJsonPath
}
catch {
  [System.Windows.Forms.MessageBox]::Show(
    $_.Exception.Message,
    "Operation Result",
    [System.Windows.Forms.MessageBoxButtons]::OK,
    [System.Windows.Forms.MessageBoxIcon]::Error
  ) | Out-Null
  Write-Error $_.Exception.Message
  exit 1
}
