<#
.SYNOPSIS
    Enterprise file distribution utility with GUI, depth control, and comprehensive audit logging.

.DESCRIPTION
    Distributes a source file to multiple directories based on configurable depth criteria.
    Features include:
    - GUI-based file and directory selection
    - Configurable recursion depth (0 to N levels, or -1 for full recursion)
    - Per-folder confirmation dialogs with Yes to All
    - Dry run mode for safe testing
    - Overwrite control
    - Structured audit logging (CSV and JSON)
    - Progress reporting with visual feedback
    - Configuration file support (.json)
    - SHA256 hash tracking for file integrity
    - Hidden folder inclusion control
    - Comprehensive error handling with try-catch blocks
    - Verbose and Debug output support

.PARAMETER SourceFile
    Path to the file to distribute. If not specified, a GUI dialog will prompt for selection.

.PARAMETER RootDirectory
    Root directory where files will be distributed. If not specified, a GUI dialog will prompt for selection.

.PARAMETER Depth
    Recursion depth for folder enumeration:
    - 0  : Root directory only
    - 1  : Root + immediate subdirectories
    - N  : Root + N levels deep
    - -1 : Full recursive (all subdirectories)

.PARAMETER DryRun
    If specified, simulates the operation without actually copying files.

.PARAMETER Overwrite
    If specified, overwrites existing files at target locations.

.PARAMETER ConfirmEach
    If specified, prompts for confirmation before each folder operation.

.PARAMETER IncludeHidden
    If specified, includes hidden folders in the distribution.

.PARAMETER LogDirectory
    Directory where audit logs will be saved. Defaults to ~/Documents/FileDistributorLogs.

.PARAMETER ConfigFile
    Path to a JSON configuration file containing default settings.

.PARAMETER UseGUI
    Forces GUI mode even when parameters are provided.

.PARAMETER WhatIf
    Shows what would happen if the command runs without actually executing.

.PARAMETER Verbose
    Displays detailed progress and diagnostic information.

.EXAMPLE
    .\file-distributor.ps1
    Launches the GUI for interactive file distribution.

.EXAMPLE
    .\file-distributor.ps1 -SourceFile "C:\template.txt" -RootDirectory "C:\Projects" -Depth 1 -DryRun
    Distributes template.txt to C:\Projects and immediate subdirectories in dry run mode.

.EXAMPLE
    .\file-distributor.ps1 -ConfigFile ".\config.json" -Verbose
    Uses settings from config.json with verbose output.

.EXAMPLE
    .\file-distributor.ps1 -SourceFile ".\LICENSE" -RootDirectory "C:\Repos" -Depth -1 -Overwrite -WhatIf
    Shows what would happen when distributing LICENSE to all subdirectories with overwrite.

.NOTES
    File Name      : file-distributor.ps1
    Version        : v02.00.00
    Author         : MokoStandards
    Prerequisite   : PowerShell 5.1 or later, Windows (for WinForms GUI)
    Requires       : -Modules (none)
    Requires       : -Version 5.1

.LINK
    https://github.com/MokoStandards
#>

#Requires -Version 5.1

[CmdletBinding(SupportsShouldProcess, DefaultParameterSetName = 'Interactive')]
param(
    [Parameter(ParameterSetName = 'CLI', HelpMessage = 'Path to the source file to distribute')]
    [ValidateNotNullOrEmpty()]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf }, ErrorMessage = 'Source file must exist')]
    [string]$SourceFile,

    [Parameter(ParameterSetName = 'CLI', HelpMessage = 'Root directory for distribution')]
    [ValidateNotNullOrEmpty()]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Container }, ErrorMessage = 'Root directory must exist')]
    [string]$RootDirectory,

    [Parameter(ParameterSetName = 'CLI', HelpMessage = 'Folder depth: 0=root only, 1=root+1 level, -1=full recursive')]
    [ValidateRange(-1, 100)]
    [int]$Depth = 1,

    [Parameter(ParameterSetName = 'CLI', HelpMessage = 'Simulate without making changes')]
    [switch]$DryRun,

    [Parameter(ParameterSetName = 'CLI', HelpMessage = 'Overwrite existing files')]
    [switch]$Overwrite,

    [Parameter(ParameterSetName = 'CLI', HelpMessage = 'Confirm each folder operation')]
    [switch]$ConfirmEach,

    [Parameter(ParameterSetName = 'CLI', HelpMessage = 'Include hidden folders')]
    [switch]$IncludeHidden = $true,

    [Parameter(HelpMessage = 'Directory for audit logs')]
    [ValidateNotNullOrEmpty()]
    [string]$LogDirectory,

    [Parameter(HelpMessage = 'Path to JSON configuration file')]
    [ValidateNotNullOrEmpty()]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf }, ErrorMessage = 'Config file must exist')]
    [string]$ConfigFile,

    [Parameter(ParameterSetName = 'Interactive', HelpMessage = 'Force GUI mode')]
    [switch]$UseGUI
)

#region Script Initialization
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'Continue'

$script:Version = 'v02.00.00'
$script:StartTime = Get-Date

Write-Verbose "File Distributor $script:Version starting at $($script:StartTime.ToString('o'))"
Write-Debug "Parameter Set: $($PSCmdlet.ParameterSetName)"
#endregion

#region Configuration Management
function Get-DistributorConfig {
    <#
    .SYNOPSIS
        Loads configuration from a JSON file.
    #>
    [CmdletBinding()]
    [OutputType([PSCustomObject])]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$Path
    )

    try {
        Write-Verbose "Loading configuration from: $Path"
        $configContent = Get-Content -LiteralPath $Path -Raw -Encoding UTF8
        $config = $configContent | ConvertFrom-Json
        Write-Debug "Configuration loaded successfully"
        return $config
    }
    catch {
        Write-Error "Failed to load configuration file '$Path': $_"
        throw
    }
}

function Merge-Configuration {
    <#
    .SYNOPSIS
        Merges command-line parameters with configuration file settings.
    #>
    [CmdletBinding()]
    [OutputType([PSCustomObject])]
    param(
        [Parameter(Mandatory)]
        [PSCustomObject]$Config,

        [Parameter(Mandatory)]
        [hashtable]$Parameters
    )

    Write-Verbose "Merging configuration with command-line parameters"

    foreach ($key in $Parameters.Keys) {
        if ($null -ne $Parameters[$key] -and $Config.PSObject.Properties.Name -contains $key) {
            Write-Debug "Overriding config.$key with parameter value"
            $Config.$key = $Parameters[$key]
        }
    }

    return $Config
}
#endregion

#region GUI Components
function Select-SourceFileGUI {
    <#
    .SYNOPSIS
        Displays a file selection dialog.
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param()

    try {
        Write-Verbose "Launching source file selection dialog"
        
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
        
        $dialog = New-Object System.Windows.Forms.OpenFileDialog -Property @{
            Title            = 'Select Source File to Distribute'
            Filter           = 'All Files (*.*)|*.*|Text Files (*.txt)|*.txt|Config Files (*.json;*.xml;*.yml)|*.json;*.xml;*.yml'
            FilterIndex      = 1
            Multiselect      = $false
            CheckFileExists  = $true
            CheckPathExists  = $true
            RestoreDirectory = $true
        }

        $result = $dialog.ShowDialog()
        
        if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
            if ([string]::IsNullOrWhiteSpace($dialog.FileName)) {
                throw 'No file was selected'
            }
            Write-Verbose "Selected source file: $($dialog.FileName)"
            return $dialog.FileName
        }
        else {
            throw 'File selection cancelled by user'
        }
    }
    catch {
        Write-Error "Failed to select source file: $_"
        throw
    }
    finally {
        if ($dialog) { $dialog.Dispose() }
    }
}

function Select-RootDirectoryGUI {
    <#
    .SYNOPSIS
        Displays a folder selection dialog.
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param()

    try {
        Write-Verbose "Launching root directory selection dialog"
        
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
        
        $dialog = New-Object System.Windows.Forms.FolderBrowserDialog -Property @{
            Description         = 'Select Root Directory for File Distribution'
            ShowNewFolderButton = $false
            RootFolder          = [System.Environment+SpecialFolder]::MyComputer
        }

        $result = $dialog.ShowDialog()
        
        if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
            if ([string]::IsNullOrWhiteSpace($dialog.SelectedPath)) {
                throw 'No directory was selected'
            }
            Write-Verbose "Selected root directory: $($dialog.SelectedPath)"
            return $dialog.SelectedPath
        }
        else {
            throw 'Directory selection cancelled by user'
        }
    }
    catch {
        Write-Error "Failed to select root directory: $_"
        throw
    }
    finally {
        if ($dialog) { $dialog.Dispose() }
    }
}

function Show-OptionsDialogGUI {
    <#
    .SYNOPSIS
        Displays the main options configuration dialog.
    #>
    [CmdletBinding()]
    [OutputType([PSCustomObject])]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$SourceFile,

        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$RootDirectory
    )

    try {
        Write-Verbose "Launching options configuration dialog"
        
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
        Add-Type -AssemblyName System.Drawing -ErrorAction Stop

        $defaultLogDir = Get-DefaultLogDirectory
        $form = New-Object System.Windows.Forms.Form -Property @{
            Text              = "File Distributor $script:Version - Configuration"
            StartPosition     = 'CenterScreen'
            FormBorderStyle   = 'FixedDialog'
            MaximizeBox       = $false
            MinimizeBox       = $false
            ClientSize        = New-Object System.Drawing.Size(780, 480)
            Topmost           = $true
            Font              = New-Object System.Drawing.Font('Segoe UI', 9)
            BackColor         = [System.Drawing.Color]::White
        }

        $lblSource = New-Object System.Windows.Forms.Label -Property @{
            Location  = New-Object System.Drawing.Point(15, 15)
            Size      = New-Object System.Drawing.Size(750, 45)
            Text      = "Source File:`n$SourceFile"
            Font      = New-Object System.Drawing.Font('Segoe UI', 9)
            ForeColor = [System.Drawing.Color]::FromArgb(0, 0, 139)
        }

        $lblRoot = New-Object System.Windows.Forms.Label -Property @{
            Location  = New-Object System.Drawing.Point(15, 65)
            Size      = New-Object System.Drawing.Size(750, 45)
            Text      = "Root Directory:`n$RootDirectory"
            Font      = New-Object System.Drawing.Font('Segoe UI', 9)
            ForeColor = [System.Drawing.Color]::FromArgb(0, 100, 0)
        }

        $grpOptions = New-Object System.Windows.Forms.GroupBox -Property @{
            Text     = 'Distribution Options'
            Location = New-Object System.Drawing.Point(15, 120)
            Size     = New-Object System.Drawing.Size(750, 140)
            Font     = New-Object System.Drawing.Font('Segoe UI', 9, [System.Drawing.FontStyle]::Bold)
        }

        $chkDryRun = New-Object System.Windows.Forms.CheckBox -Property @{
            Location = New-Object System.Drawing.Point(15, 25)
            Size     = New-Object System.Drawing.Size(350, 24)
            Text     = 'Dry Run (simulate without making changes)'
            Checked  = $true
            Font     = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $chkOverwrite = New-Object System.Windows.Forms.CheckBox -Property @{
            Location = New-Object System.Drawing.Point(15, 52)
            Size     = New-Object System.Drawing.Size(350, 24)
            Text     = 'Overwrite existing files'
            Checked  = $false
            Font     = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $chkConfirmEach = New-Object System.Windows.Forms.CheckBox -Property @{
            Location = New-Object System.Drawing.Point(15, 79)
            Size     = New-Object System.Drawing.Size(450, 24)
            Text     = 'Confirm each folder (Yes, No, Yes to All, Cancel)'
            Checked  = $false
            Font     = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $chkIncludeHidden = New-Object System.Windows.Forms.CheckBox -Property @{
            Location = New-Object System.Drawing.Point(15, 106)
            Size     = New-Object System.Drawing.Size(350, 24)
            Text     = 'Include hidden folders'
            Checked  = $true
            Font     = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $grpOptions.Controls.AddRange(@($chkDryRun, $chkOverwrite, $chkConfirmEach, $chkIncludeHidden))

        $grpDepth = New-Object System.Windows.Forms.GroupBox -Property @{
            Text     = 'Recursion Depth'
            Location = New-Object System.Drawing.Point(15, 270)
            Size     = New-Object System.Drawing.Size(750, 90)
            Font     = New-Object System.Drawing.Font('Segoe UI', 9, [System.Drawing.FontStyle]::Bold)
        }

        $lblDepth = New-Object System.Windows.Forms.Label -Property @{
            Location = New-Object System.Drawing.Point(15, 28)
            Size     = New-Object System.Drawing.Size(160, 22)
            Text     = 'Depth (-1 = full recursive):'
            Font     = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $numDepth = New-Object System.Windows.Forms.NumericUpDown -Property @{
            Location = New-Object System.Drawing.Point(180, 26)
            Size     = New-Object System.Drawing.Size(100, 24)
            Minimum  = -1
            Maximum  = 100
            Value    = 1
            Font     = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $lblDepthHelp = New-Object System.Windows.Forms.Label -Property @{
            Location  = New-Object System.Drawing.Point(290, 22)
            Size      = New-Object System.Drawing.Size(440, 55)
            Text      = "0  = Root directory only`n1  = Root + immediate subdirectories`nN  = Root + N levels deep`n-1 = Full recursive (all subdirectories)"
            Font      = New-Object System.Drawing.Font('Segoe UI', 8)
            ForeColor = [System.Drawing.Color]::Gray
        }

        $grpDepth.Controls.AddRange(@($lblDepth, $numDepth, $lblDepthHelp))

        $grpLog = New-Object System.Windows.Forms.GroupBox -Property @{
            Text     = 'Audit Logging'
            Location = New-Object System.Drawing.Point(15, 370)
            Size     = New-Object System.Drawing.Size(750, 62)
            Font     = New-Object System.Drawing.Font('Segoe UI', 9, [System.Drawing.FontStyle]::Bold)
        }

        $lblLog = New-Object System.Windows.Forms.Label -Property @{
            Location = New-Object System.Drawing.Point(15, 28)
            Size     = New-Object System.Drawing.Size(90, 22)
            Text     = 'Log Directory:'
            Font     = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $txtLogDir = New-Object System.Windows.Forms.TextBox -Property @{
            Location = New-Object System.Drawing.Point(110, 26)
            Size     = New-Object System.Drawing.Size(520, 24)
            Text     = $defaultLogDir
            Font     = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $btnBrowseLog = New-Object System.Windows.Forms.Button -Property @{
            Text     = 'Browse...'
            Location = New-Object System.Drawing.Point(640, 24)
            Size     = New-Object System.Drawing.Size(95, 28)
            Font     = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $btnBrowseLog.Add_Click({
            try {
                $folderDialog = New-Object System.Windows.Forms.FolderBrowserDialog -Property @{
                    Description         = 'Select Log Directory'
                    ShowNewFolderButton = $true
                    SelectedPath        = $txtLogDir.Text
                }

                $result = $folderDialog.ShowDialog()
                if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
                    $txtLogDir.Text = $folderDialog.SelectedPath
                }
            }
            catch {
                [System.Windows.Forms.MessageBox]::Show(
                    "Error selecting log directory: $_",
                    'Error',
                    [System.Windows.Forms.MessageBoxButtons]::OK,
                    [System.Windows.Forms.MessageBoxIcon]::Error
                ) | Out-Null
            }
            finally {
                if ($folderDialog) { $folderDialog.Dispose() }
            }
        })

        $grpLog.Controls.AddRange(@($lblLog, $txtLogDir, $btnBrowseLog))

        $btnRun = New-Object System.Windows.Forms.Button -Property @{
            Text         = 'Run Distribution'
            Location     = New-Object System.Drawing.Point(555, 442)
            Size         = New-Object System.Drawing.Size(100, 32)
            Font         = New-Object System.Drawing.Font('Segoe UI', 9, [System.Drawing.FontStyle]::Bold)
            DialogResult = [System.Windows.Forms.DialogResult]::OK
            BackColor    = [System.Drawing.Color]::FromArgb(0, 120, 215)
            ForeColor    = [System.Drawing.Color]::White
            FlatStyle    = [System.Windows.Forms.FlatStyle]::Flat
        }

        $btnCancel = New-Object System.Windows.Forms.Button -Property @{
            Text         = 'Cancel'
            Location     = New-Object System.Drawing.Point(665, 442)
            Size         = New-Object System.Drawing.Size(100, 32)
            Font         = New-Object System.Drawing.Font('Segoe UI', 9)
            DialogResult = [System.Windows.Forms.DialogResult]::Cancel
        }

        $form.AcceptButton = $btnRun
        $form.CancelButton = $btnCancel

        $form.Controls.AddRange(@(
            $lblSource, $lblRoot,
            $grpOptions, $grpDepth, $grpLog,
            $btnRun, $btnCancel
        ))

        $dialogResult = $form.ShowDialog()

        if ($dialogResult -ne [System.Windows.Forms.DialogResult]::OK) {
            throw 'Operation cancelled by user'
        }

        $logDir = $txtLogDir.Text.Trim()
        if ([string]::IsNullOrWhiteSpace($logDir)) {
            throw 'Log directory is required for audit compliance'
        }

        Write-Verbose "Options configured - DryRun: $($chkDryRun.Checked), Overwrite: $($chkOverwrite.Checked), Depth: $($numDepth.Value)"

        return [PSCustomObject]@{
            DryRun        = [bool]$chkDryRun.Checked
            Overwrite     = [bool]$chkOverwrite.Checked
            ConfirmEach   = [bool]$chkConfirmEach.Checked
            IncludeHidden = [bool]$chkIncludeHidden.Checked
            Depth         = [int]$numDepth.Value
            LogDirectory  = $logDir
        }
    }
    catch {
        Write-Error "Failed to show options dialog: $_"
        throw
    }
    finally {
        if ($form) { $form.Dispose() }
    }
}

function Show-FolderConfirmationGUI {
    <#
    .SYNOPSIS
        Displays a per-folder confirmation dialog.
    #>
    [CmdletBinding()]
    [OutputType([System.Windows.Forms.DialogResult])]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$FolderPath,

        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$TargetFilePath,

        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$FileName,

        [Parameter(Mandatory)]
        [bool]$WillOverwrite,

        [Parameter(Mandatory)]
        [bool]$FileExists
    )

    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
        Add-Type -AssemblyName System.Drawing -ErrorAction Stop

        $action = if ($FileExists -and $WillOverwrite) { 'OVERWRITE' }
                  elseif ($FileExists) { 'SKIP (file exists)' }
                  else { 'COPY' }

        $form = New-Object System.Windows.Forms.Form -Property @{
            Text            = 'Confirm Folder Operation'
            StartPosition   = 'CenterScreen'
            FormBorderStyle = 'FixedDialog'
            MaximizeBox     = $false
            MinimizeBox     = $false
            ClientSize      = New-Object System.Drawing.Size(550, 320)
            Topmost         = $true
            Font            = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $lblMessage = New-Object System.Windows.Forms.Label -Property @{
            Location = New-Object System.Drawing.Point(15, 15)
            Size     = New-Object System.Drawing.Size(520, 240)
            Font     = New-Object System.Drawing.Font('Segoe UI', 9)
            Text     = @(
                'Target Folder:',
                $FolderPath,
                '',
                'File Name:',
                $FileName,
                '',
                'Target Path:',
                $TargetFilePath,
                '',
                "Action: $action",
                '',
                'Do you want to proceed with this folder?'
            ) -join "`n"
        }

        $btnYes = New-Object System.Windows.Forms.Button -Property @{
            Text         = 'Yes'
            Location     = New-Object System.Drawing.Point(15, 270)
            Size         = New-Object System.Drawing.Size(120, 35)
            DialogResult = [System.Windows.Forms.DialogResult]::Yes
            Font         = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $btnNo = New-Object System.Windows.Forms.Button -Property @{
            Text         = 'No'
            Location     = New-Object System.Drawing.Point(145, 270)
            Size         = New-Object System.Drawing.Size(120, 35)
            DialogResult = [System.Windows.Forms.DialogResult]::No
            Font         = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $btnYesToAll = New-Object System.Windows.Forms.Button -Property @{
            Text         = 'Yes to All'
            Location     = New-Object System.Drawing.Point(275, 270)
            Size         = New-Object System.Drawing.Size(120, 35)
            DialogResult = [System.Windows.Forms.DialogResult]::Retry
            Font         = New-Object System.Drawing.Font('Segoe UI', 9, [System.Drawing.FontStyle]::Bold)
        }

        $btnCancel = New-Object System.Windows.Forms.Button -Property @{
            Text         = 'Cancel All'
            Location     = New-Object System.Drawing.Point(405, 270)
            Size         = New-Object System.Drawing.Size(120, 35)
            DialogResult = [System.Windows.Forms.DialogResult]::Cancel
            Font         = New-Object System.Drawing.Font('Segoe UI', 9)
        }

        $form.AcceptButton = $btnYes
        $form.CancelButton = $btnCancel

        $form.Controls.AddRange(@($lblMessage, $btnYes, $btnNo, $btnYesToAll, $btnCancel))

        return $form.ShowDialog()
    }
    catch {
        Write-Error "Failed to show folder confirmation dialog: $_"
        throw
    }
    finally {
        if ($form) { $form.Dispose() }
    }
}

function Show-SummaryDialogGUI {
    <#
    .SYNOPSIS
        Displays a summary dialog with operation results.
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNull()]
        [PSCustomObject]$Summary
    )

    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop

        $summaryText = @(
            "Run ID: $($Summary.RunId)",
            "Started: $($Summary.StartedAt)",
            "Ended: $($Summary.EndedAt)",
            "Duration: $($Summary.Duration)",
            '',
            "Total Folders: $($Summary.TotalFolders)",
            "Copied: $($Summary.Copied)",
            "Overwritten: $($Summary.Overwritten)",
            "Skipped (exists): $($Summary.Skipped)",
            "Skipped (user): $($Summary.UserSkipped)",
            "Errors: $($Summary.Errors)",
            "Cancelled: $($Summary.Cancelled)",
            '',
            'Audit Logs:',
            "CSV: $($Summary.CsvLog)",
            "JSON: $($Summary.JsonLog)"
        ) -join "`n"

        $icon = if ($Summary.Errors -gt 0) {
            [System.Windows.Forms.MessageBoxIcon]::Warning
        } elseif ($Summary.Cancelled) {
            [System.Windows.Forms.MessageBoxIcon]::Information
        } else {
            [System.Windows.Forms.MessageBoxIcon]::Information
        }

        [System.Windows.Forms.MessageBox]::Show(
            $summaryText,
            'Distribution Complete',
            [System.Windows.Forms.MessageBoxButtons]::OK,
            $icon
        ) | Out-Null
    }
    catch {
        Write-Warning "Failed to show summary dialog: $_"
    }
}
#endregion

#region Core Functions
function Get-DefaultLogDirectory {
    <#
    .SYNOPSIS
        Gets the default log directory path.
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param()

    $logDir = Join-Path -Path ([Environment]::GetFolderPath('MyDocuments')) -ChildPath 'FileDistributorLogs'
    
    if (-not (Test-Path -LiteralPath $logDir -PathType Container)) {
        try {
            Write-Verbose "Creating default log directory: $logDir"
            New-Item -ItemType Directory -Path $logDir -Force | Out-Null
        }
        catch {
            Write-Error "Failed to create log directory: $_"
            throw
        }
    }

    return $logDir
}

function Get-FoldersByDepth {
    <#
    .SYNOPSIS
        Enumerates folders based on depth criteria.
    #>
    [CmdletBinding()]
    [OutputType([string[]])]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({ Test-Path -LiteralPath $_ -PathType Container }, ErrorMessage = 'Root path must be a valid directory')]
        [string]$RootPath,

        [Parameter(Mandatory)]
        [ValidateRange(-1, 100)]
        [int]$Depth,

        [Parameter()]
        [bool]$IncludeHidden = $true
    )

    try {
        Write-Verbose "Enumerating folders from '$RootPath' with depth $Depth"
        
        $folders = [System.Collections.Generic.List[string]]::new()
        $rootItem = Get-Item -LiteralPath $RootPath -Force

        $folders.Add($rootItem.FullName)
        Write-Debug "Added root folder: $($rootItem.FullName)"

        if ($Depth -eq 0) {
            Write-Verbose "Depth is 0, returning root only"
            return $folders.ToArray()
        }

        $childItemParams = @{
            Directory   = $true
            ErrorAction = 'SilentlyContinue'
        }

        if ($IncludeHidden) {
            $childItemParams.Force = $true
        }

        if ($Depth -eq -1) {
            Write-Verbose "Full recursive enumeration"
            $allFolders = Get-ChildItem -LiteralPath $RootPath -Recurse @childItemParams
            foreach ($folder in $allFolders) {
                $folders.Add($folder.FullName)
            }
            Write-Verbose "Found $($folders.Count) folders (including root)"
            return $folders.ToArray()
        }

        $currentLevel = [System.Collections.Generic.List[string]]::new()
        $currentLevel.Add($rootItem.FullName)

        for ($level = 1; $level -le $Depth; $level++) {
            Write-Debug "Processing depth level $level"
            $nextLevel = [System.Collections.Generic.List[string]]::new()

            foreach ($parentPath in $currentLevel) {
                $children = Get-ChildItem -LiteralPath $parentPath @childItemParams
                
                foreach ($child in $children) {
                    $nextLevel.Add($child.FullName)
                    $folders.Add($child.FullName)
                }
            }

            if ($nextLevel.Count -eq 0) {
                Write-Debug "No more folders at level $level, stopping enumeration"
                break
            }

            $currentLevel = $nextLevel
        }

        Write-Verbose "Found $($folders.Count) folders at depth $Depth"
        return $folders.ToArray()
    }
    catch {
        Write-Error "Failed to enumerate folders: $_"
        throw
    }
}

function Write-AuditLogs {
    <#
    .SYNOPSIS
        Creates audit log files from operation records.
    #>
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNull()]
        [System.Collections.Generic.List[PSCustomObject]]$Records,

        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$CsvPath,

        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [string]$JsonPath
    )

    try {
        if ($PSCmdlet.ShouldProcess("Audit logs", "Write to '$CsvPath' and '$JsonPath'")) {
            Write-Verbose "Writing $($Records.Count) records to audit logs"

            Write-Debug "Writing CSV log: $CsvPath"
            $Records | Export-Csv -LiteralPath $CsvPath -NoTypeInformation -Encoding UTF8 -Force

            Write-Debug "Writing JSON log: $JsonPath"
            $json = $Records | ConvertTo-Json -Depth 10 -Compress:$false
            $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
            [System.IO.File]::WriteAllText($JsonPath, $json, $utf8NoBom)

            Write-Verbose "Audit logs written successfully"
        }
    }
    catch {
        Write-Error "Failed to write audit logs: $_"
        throw
    }
}

function Invoke-FileDistribution {
    <#
    .SYNOPSIS
        Distributes a file to multiple folders.
    #>
    [CmdletBinding(SupportsShouldProcess)]
    [OutputType([PSCustomObject])]
    param(
        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf }, ErrorMessage = 'Source file must exist')]
        [string]$SourceFile,

        [Parameter(Mandatory)]
        [ValidateNotNullOrEmpty()]
        [ValidateScript({ Test-Path -LiteralPath $_ -PathType Container }, ErrorMessage = 'Root directory must exist')]
        [string]$RootDirectory,

        [Parameter(Mandatory)]
        [ValidateNotNull()]
        [PSCustomObject]$Options
    )

    try {
        $runId = [guid]::NewGuid().ToString()
        $startTime = Get-Date

        Write-Verbose "Starting distribution - Run ID: $runId"

        $sourceItem = Get-Item -LiteralPath $SourceFile -Force
        $sourceName = $sourceItem.Name
        $sourceSize = $sourceItem.Length

        Write-Progress -Activity 'File Distribution' -Status 'Computing file hash...' -PercentComplete 0
        $sourceHash = (Get-FileHash -LiteralPath $SourceFile -Algorithm SHA256).Hash
        Write-Debug "Source file hash: $sourceHash"

        Write-Progress -Activity 'File Distribution' -Status 'Enumerating folders...' -PercentComplete 5
        $folders = Get-FoldersByDepth -RootPath $RootDirectory -Depth $Options.Depth -IncludeHidden $Options.IncludeHidden

        Write-Verbose "Processing $($folders.Count) folders"

        $timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
        $csvPath = Join-Path -Path $Options.LogDirectory -ChildPath "file-distributor_$timestamp.csv"
        $jsonPath = Join-Path -Path $Options.LogDirectory -ChildPath "file-distributor_$timestamp.json"

        $records = [System.Collections.Generic.List[PSCustomObject]]::new()
        
        $stats = @{
            RunId        = $runId
            StartedAt    = $startTime.ToString('o')
            TotalFolders = $folders.Count
            Copied       = 0
            Overwritten  = 0
            Skipped      = 0
            UserSkipped  = 0
            Errors       = 0
            Cancelled    = $false
        }

        $yesToAll = $false
        $folderIndex = 0

        foreach ($folderPath in $folders) {
            $folderIndex++
            $percentComplete = [Math]::Min(100, 10 + (($folderIndex / $folders.Count) * 85))
            
            $targetPath = Join-Path -Path $folderPath -ChildPath $sourceName
            $fileExists = Test-Path -LiteralPath $targetPath -PathType Leaf

            Write-Progress -Activity 'File Distribution' -Status "Processing folder $folderIndex of $($folders.Count)" -CurrentOperation $folderPath -PercentComplete $percentComplete

            $plannedAction = if ($fileExists -and -not $Options.Overwrite) { 'SkipExists' }
                            elseif ($fileExists -and $Options.Overwrite) { 'Overwrite' }
                            else { 'Copy' }

            $decision = 'Auto'
            $record = [PSCustomObject]@{
                RunId         = $runId
                Timestamp     = (Get-Date).ToString('o')
                Folder        = $folderPath
                TargetPath    = $targetPath
                ActionPlanned = $plannedAction
                ActionTaken   = ''
                Decision      = $decision
                DryRun        = $Options.DryRun
                Overwrite     = $Options.Overwrite
                Depth         = $Options.Depth
                SourceFile    = $SourceFile
                SourceName    = $sourceName
                SourceSize    = $sourceSize
                SourceSHA256  = $sourceHash
                Result        = ''
                ErrorMessage  = ''
            }

            try {
                if ($Options.ConfirmEach -and -not $yesToAll) {
                    $confirmation = Show-FolderConfirmationGUI -FolderPath $folderPath -TargetFilePath $targetPath -FileName $sourceName -WillOverwrite $Options.Overwrite -FileExists $fileExists

                    if ($confirmation -eq [System.Windows.Forms.DialogResult]::No) {
                        $decision = 'UserNo'
                        $record.Decision = $decision
                        $record.ActionTaken = 'Skip'
                        $record.Result = 'SkippedByUser'
                        $stats.UserSkipped++
                        $records.Add($record)
                        Write-Host "[SKIP] User declined: $targetPath" -ForegroundColor Yellow
                        continue
                    }

                    if ($confirmation -eq [System.Windows.Forms.DialogResult]::Cancel) {
                        $decision = 'UserCancel'
                        $record.Decision = $decision
                        $record.ActionTaken = 'Abort'
                        $record.Result = 'Cancelled'
                        $stats.Cancelled = $true
                        $records.Add($record)
                        Write-Host "[CANCEL] User cancelled operation at: $folderPath" -ForegroundColor Red
                        break
                    }

                    if ($confirmation -eq [System.Windows.Forms.DialogResult]::Retry) {
                        $yesToAll = $true
                        $decision = 'UserYesToAll'
                        Write-Host "[INFO] 'Yes to All' selected - remaining folders will proceed without confirmation" -ForegroundColor Cyan
                    }
                    else {
                        $decision = 'UserYes'
                    }
                }
                elseif ($yesToAll) {
                    $decision = 'UserYesToAll'
                }

                $record.Decision = $decision

                if ($fileExists -and -not $Options.Overwrite) {
                    $record.ActionTaken = 'Skip'
                    $record.Result = 'SkippedExists'
                    $stats.Skipped++
                    $records.Add($record)
                    Write-Verbose "[SKIP] File exists and overwrite disabled: $targetPath"
                    continue
                }

                if ($Options.DryRun) {
                    if ($fileExists -and $Options.Overwrite) {
                        $record.ActionTaken = 'WouldOverwrite'
                        $record.Result = 'DryRun'
                        $stats.Overwritten++
                        Write-Host "[DRYRUN] Would overwrite: $targetPath" -ForegroundColor Magenta
                    }
                    else {
                        $record.ActionTaken = 'WouldCopy'
                        $record.Result = 'DryRun'
                        $stats.Copied++
                        Write-Host "[DRYRUN] Would copy: $targetPath" -ForegroundColor Magenta
                    }
                    $records.Add($record)
                    continue
                }

                if ($PSCmdlet.ShouldProcess($targetPath, "Copy file from '$SourceFile'")) {
                    if ($fileExists -and $Options.Overwrite) {
                        Copy-Item -LiteralPath $SourceFile -Destination $targetPath -Force -ErrorAction Stop
                        $record.ActionTaken = 'Overwrite'
                        $record.Result = 'Success'
                        $stats.Overwritten++
                        Write-Host "[OK] Overwrote: $targetPath" -ForegroundColor Green
                    }
                    else {
                        Copy-Item -LiteralPath $SourceFile -Destination $targetPath -ErrorAction Stop
                        $record.ActionTaken = 'Copy'
                        $record.Result = 'Success'
                        $stats.Copied++
                        Write-Host "[OK] Copied: $targetPath" -ForegroundColor Green
                    }
                }

                $records.Add($record)
            }
            catch {
                $stats.Errors++
                $errorMsg = $_.Exception.Message
                
                $record.ActionTaken = 'Error'
                $record.Result = 'Error'
                $record.ErrorMessage = $errorMsg
                $records.Add($record)

                Write-Warning "[ERROR] Failed to process '$folderPath': $errorMsg"
            }
        }

        Write-Progress -Activity 'File Distribution' -Status 'Writing audit logs...' -PercentComplete 95

        $endTime = Get-Date
        $duration = $endTime - $startTime
        $stats.EndedAt = $endTime.ToString('o')

        Write-AuditLogs -Records $records -CsvPath $csvPath -JsonPath $jsonPath

        Write-Progress -Activity 'File Distribution' -Completed

        $summary = [PSCustomObject]@{
            RunId        = $stats.RunId
            StartedAt    = $stats.StartedAt
            EndedAt      = $stats.EndedAt
            Duration     = $duration.ToString('hh\:mm\:ss')
            TotalFolders = $stats.TotalFolders
            Copied       = $stats.Copied
            Overwritten  = $stats.Overwritten
            Skipped      = $stats.Skipped
            UserSkipped  = $stats.UserSkipped
            Errors       = $stats.Errors
            Cancelled    = $stats.Cancelled
            CsvLog       = $csvPath
            JsonLog      = $jsonPath
        }

        Write-Verbose "Distribution complete - Copied: $($stats.Copied), Errors: $($stats.Errors)"

        return $summary
    }
    catch {
        Write-Error "Distribution failed: $_"
        throw
    }
}
#endregion

#region Main Execution
try {
    Write-Verbose "Initializing File Distributor $script:Version"

    $config = $null
    if ($ConfigFile) {
        $config = Get-DistributorConfig -Path $ConfigFile
        Write-Verbose "Configuration loaded from file"
    }

    $useInteractiveMode = ($PSCmdlet.ParameterSetName -eq 'Interactive') -or $UseGUI.IsPresent -or (-not $SourceFile -or -not $RootDirectory)

    if ($useInteractiveMode) {
        Write-Verbose "Running in GUI mode"

        try {
            Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
            Add-Type -AssemblyName System.Drawing -ErrorAction Stop
        }
        catch {
            Write-Error "Failed to load Windows Forms. This script requires Windows with GUI support."
            throw
        }

        $selectedSource = Select-SourceFileGUI
        $selectedRoot = Select-RootDirectoryGUI
        $options = Show-OptionsDialogGUI -SourceFile $selectedSource -RootDirectory $selectedRoot

        $summary = Invoke-FileDistribution -SourceFile $selectedSource -RootDirectory $selectedRoot -Options $options

        Show-SummaryDialogGUI -Summary $summary
    }
    else {
        Write-Verbose "Running in CLI mode"

        $logDir = if ($LogDirectory) { $LogDirectory } else { Get-DefaultLogDirectory }

        $options = [PSCustomObject]@{
            DryRun        = $DryRun.IsPresent
            Overwrite     = $Overwrite.IsPresent
            ConfirmEach   = $ConfirmEach.IsPresent
            IncludeHidden = $IncludeHidden.IsPresent
            Depth         = $Depth
            LogDirectory  = $logDir
        }

        Write-Host ''
        Write-Host "File Distributor $script:Version - CLI Mode" -ForegroundColor Cyan
        Write-Host ('=' * 60) -ForegroundColor Cyan
        Write-Host "Source File    : $SourceFile"
        Write-Host "Root Directory : $RootDirectory"
        Write-Host "Depth          : $Depth $(if ($Depth -eq -1) {'(full recursive)'} elseif ($Depth -eq 0) {'(root only)'} else {"($Depth levels)"})"
        Write-Host "Dry Run        : $($options.DryRun)"
        Write-Host "Overwrite      : $($options.Overwrite)"
        Write-Host "Confirm Each   : $($options.ConfirmEach)"
        Write-Host "Include Hidden : $($options.IncludeHidden)"
        Write-Host "Log Directory  : $($options.LogDirectory)"
        Write-Host ('=' * 60) -ForegroundColor Cyan
        Write-Host ''

        $summary = Invoke-FileDistribution -SourceFile $SourceFile -RootDirectory $RootDirectory -Options $options

        Write-Host ''
        Write-Host ('=' * 60) -ForegroundColor Green
        Write-Host 'Distribution Summary' -ForegroundColor Green
        Write-Host ('=' * 60) -ForegroundColor Green
        Write-Host "Run ID         : $($summary.RunId)"
        Write-Host "Started        : $($summary.StartedAt)"
        Write-Host "Ended          : $($summary.EndedAt)"
        Write-Host "Duration       : $($summary.Duration)"
        Write-Host "Total Folders  : $($summary.TotalFolders)"
        Write-Host "Copied         : $($summary.Copied)" -ForegroundColor Green
        Write-Host "Overwritten    : $($summary.Overwritten)" -ForegroundColor Yellow
        Write-Host "Skipped        : $($summary.Skipped)" -ForegroundColor Gray
        Write-Host "User Skipped   : $($summary.UserSkipped)" -ForegroundColor Gray
        Write-Host "Errors         : $($summary.Errors)" -ForegroundColor $(if ($summary.Errors -gt 0) { 'Red' } else { 'Gray' })
        Write-Host "Cancelled      : $($summary.Cancelled)" -ForegroundColor $(if ($summary.Cancelled) { 'Red' } else { 'Gray' })
        Write-Host ''
        Write-Host 'Audit Logs:' -ForegroundColor Cyan
        Write-Host "  CSV  : $($summary.CsvLog)"
        Write-Host "  JSON : $($summary.JsonLog)"
        Write-Host ('=' * 60) -ForegroundColor Green
        Write-Host ''
    }

    $endTime = Get-Date
    $totalDuration = $endTime - $script:StartTime
    Write-Verbose "File Distributor completed in $($totalDuration.TotalSeconds) seconds"

    exit 0
}
catch {
    $errorMessage = $_.Exception.Message
    Write-Error "File Distributor failed: $errorMessage"

    if (-not $useInteractiveMode -or $null -eq $useInteractiveMode) {
        try {
            Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue
            [System.Windows.Forms.MessageBox]::Show(
                $errorMessage,
                'File Distributor Error',
                [System.Windows.Forms.MessageBoxButtons]::OK,
                [System.Windows.Forms.MessageBoxIcon]::Error
            ) | Out-Null
        }
        catch {
        }
    }

    exit 1
}
#endregion
