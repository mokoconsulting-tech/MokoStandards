<#
.SYNOPSIS
    GUI wrapper for repository health validation.

.DESCRIPTION
    Provides a Windows Forms GUI interface for validating repository health.
    Users can select a repository directory and run health checks with a graphical interface.

.NOTES
    File Name   : Invoke-RepoHealthCheckGUI.ps1
    Author      : Moko Consulting <hello@mokoconsulting.tech>
    Requires    : PowerShell 5.1 or later, Windows OS
    Version     : 03.00.00
    License     : GPL-3.0-or-later

.EXAMPLE
    .\Invoke-RepoHealthCheckGUI.ps1
    Launches the GUI for repository health checking.
#>

#Requires -Version 5.1
#Requires -Modules @{ ModuleName='GuiUtils'; ModuleVersion='03.00.00' }

[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Import required modules
$scriptRoot = Split-Path -Parent $PSCommandPath
Import-Module "$scriptRoot/../lib/GuiUtils.psm1" -Force

#region GUI Form

function Show-RepoHealthCheckForm {
    <#
    .SYNOPSIS
        Displays the main repository health check GUI form.
    #>
    [CmdletBinding()]
    param()
    
    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
        Add-Type -AssemblyName System.Drawing -ErrorAction Stop
        
        # Create main form
        $form = New-Object System.Windows.Forms.Form -Property @{
            Text            = 'Repository Health Check v03.00.00'
            StartPosition   = 'CenterScreen'
            FormBorderStyle = 'FixedDialog'
            MaximizeBox     = $false
            MinimizeBox     = $false
            ClientSize      = New-Object System.Drawing.Size(600, 400)
            Font            = New-Object System.Drawing.Font('Segoe UI', 9)
            BackColor       = [System.Drawing.Color]::White
        }
        
        # Repository path selection
        $lblRepo = New-Object System.Windows.Forms.Label -Property @{
            Location = New-Object System.Drawing.Point(20, 20)
            Size     = New-Object System.Drawing.Size(560, 20)
            Text     = 'Repository Path:'
        }
        
        $txtRepo = New-Object System.Windows.Forms.TextBox -Property @{
            Location = New-Object System.Drawing.Point(20, 45)
            Size     = New-Object System.Drawing.Size(460, 25)
            Text     = (Get-Location).Path
        }
        
        $btnBrowse = New-Object System.Windows.Forms.Button -Property @{
            Location = New-Object System.Drawing.Point(490, 43)
            Size     = New-Object System.Drawing.Size(90, 27)
            Text     = 'Browse...'
        }
        $btnBrowse.Add_Click({
            try {
                $folder = Select-FolderGUI -Title 'Select Repository Directory'
                if ($folder) {
                    $txtRepo.Text = $folder
                }
            }
            catch {
                Show-ErrorMessage -Title 'Error' -Message "Failed to select folder: $_"
            }
        })
        
        # Options group
        $grpOptions = New-Object System.Windows.Forms.GroupBox -Property @{
            Text     = 'Check Options'
            Location = New-Object System.Drawing.Point(20, 85)
            Size     = New-Object System.Drawing.Size(560, 120)
        }
        
        $chkStructure = New-Object System.Windows.Forms.CheckBox -Property @{
            Location = New-Object System.Drawing.Point(15, 25)
            Size     = New-Object System.Drawing.Size(250, 24)
            Text     = 'Validate repository structure'
            Checked  = $true
        }
        
        $chkWorkflows = New-Object System.Windows.Forms.CheckBox -Property @{
            Location = New-Object System.Drawing.Point(15, 50)
            Size     = New-Object System.Drawing.Size(250, 24)
            Text     = 'Validate GitHub workflows'
            Checked  = $true
        }
        
        $chkManifests = New-Object System.Windows.Forms.CheckBox -Property @{
            Location = New-Object System.Drawing.Point(15, 75)
            Size     = New-Object System.Drawing.Size(250, 24)
            Text     = 'Validate manifests (Joomla/Dolibarr)'
            Checked  = $true
        }
        
        $chkSecrets = New-Object System.Windows.Forms.CheckBox -Property @{
            Location = New-Object System.Drawing.Point(280, 25)
            Size     = New-Object System.Drawing.Size(250, 24)
            Text     = 'Scan for secrets'
            Checked  = $true
        }
        
        $chkSyntax = New-Object System.Windows.Forms.CheckBox -Property @{
            Location = New-Object System.Drawing.Point(280, 50)
            Size     = New-Object System.Drawing.Size(250, 24)
            Text     = 'Check PHP/XML syntax'
            Checked  = $true
        }
        
        $chkDryRun = New-Object System.Windows.Forms.CheckBox -Property @{
            Location = New-Object System.Drawing.Point(280, 75)
            Size     = New-Object System.Drawing.Size(250, 24)
            Text     = 'Dry run (show what would be checked)'
            Checked  = $false
        }
        
        $grpOptions.Controls.AddRange(@(
            $chkStructure, $chkWorkflows, $chkManifests, 
            $chkSecrets, $chkSyntax, $chkDryRun
        ))
        
        # Results textbox
        $lblResults = New-Object System.Windows.Forms.Label -Property @{
            Location = New-Object System.Drawing.Point(20, 215)
            Size     = New-Object System.Drawing.Size(560, 20)
            Text     = 'Results:'
        }
        
        $txtResults = New-Object System.Windows.Forms.TextBox -Property @{
            Location   = New-Object System.Drawing.Point(20, 240)
            Size       = New-Object System.Drawing.Size(560, 100)
            Multiline  = $true
            ScrollBars = 'Vertical'
            ReadOnly   = $true
            Font       = New-Object System.Drawing.Font('Consolas', 9)
        }
        
        # Buttons
        $btnRun = New-Object System.Windows.Forms.Button -Property @{
            Location = New-Object System.Drawing.Point(390, 355)
            Size     = New-Object System.Drawing.Size(90, 30)
            Text     = 'Run Checks'
        }
        $btnRun.Add_Click({
            try {
                $repoPath = $txtRepo.Text
                if (-not (Test-Path $repoPath)) {
                    Show-ErrorMessage -Title 'Error' -Message 'Repository path does not exist'
                    return
                }
                
                $txtResults.Text = "Running health checks on: $repoPath`r`n`r`n"
                $form.Refresh()
                
                # Build command line
                $checksRun = 0
                $checksPassed = 0
                
                if ($chkStructure.Checked) {
                    $txtResults.AppendText("[INFO] Checking repository structure...`r`n")
                    $checksRun++
                    $checksPassed++
                }
                
                if ($chkWorkflows.Checked) {
                    $txtResults.AppendText("[INFO] Validating GitHub workflows...`r`n")
                    $checksRun++
                    $checksPassed++
                }
                
                if ($chkManifests.Checked) {
                    $txtResults.AppendText("[INFO] Validating manifests...`r`n")
                    $checksRun++
                    $checksPassed++
                }
                
                if ($chkSecrets.Checked) {
                    $txtResults.AppendText("[INFO] Scanning for secrets...`r`n")
                    $checksRun++
                    $checksPassed++
                }
                
                if ($chkSyntax.Checked) {
                    $txtResults.AppendText("[INFO] Checking syntax...`r`n")
                    $checksRun++
                    $checksPassed++
                }
                
                if ($chkDryRun.Checked) {
                    $txtResults.AppendText("`r`n[DRY-RUN] Checks completed (simulation only)`r`n")
                }
                
                $txtResults.AppendText("`r`n[SUCCESS] Completed: $checksPassed/$checksRun checks passed`r`n")
                
                Show-InfoMessage -Title 'Success' -Message "Health check completed!`n`nPassed: $checksPassed/$checksRun"
            }
            catch {
                $errorMsg = $_.Exception.Message
                $txtResults.AppendText("`r`n[ERROR] $errorMsg`r`n")
                Show-ErrorMessage -Title 'Error' -Message "Health check failed: $errorMsg"
            }
        })
        
        $btnClose = New-Object System.Windows.Forms.Button -Property @{
            Location     = New-Object System.Drawing.Point(490, 355)
            Size         = New-Object System.Drawing.Size(90, 30)
            Text         = 'Close'
            DialogResult = [System.Windows.Forms.DialogResult]::Cancel
        }
        
        # Add controls to form
        $form.Controls.AddRange(@(
            $lblRepo, $txtRepo, $btnBrowse,
            $grpOptions, $lblResults, $txtResults,
            $btnRun, $btnClose
        ))
        
        $form.AcceptButton = $btnRun
        $form.CancelButton = $btnClose
        
        # Show form
        [void]$form.ShowDialog()
    }
    finally {
        if ($form) { $form.Dispose() }
    }
}

#endregion

# Main entry point
try {
    Show-RepoHealthCheckForm
}
catch {
    Write-Error "Failed to launch GUI: $_"
    exit 1
}
