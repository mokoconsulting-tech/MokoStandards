<#
.SYNOPSIS
    GUI wrapper for demo data loading.

.DESCRIPTION
    Provides a Windows Forms GUI interface for loading SQL demo data into MySQL/MariaDB databases.
    Users can select SQL files, configure database connections, and load data with a graphical interface.

.NOTES
    File Name   : Invoke-DemoDataLoaderGUI.ps1
    Author      : Moko Consulting <hello@mokoconsulting.tech>
    Requires    : PowerShell 5.1 or later, Windows OS, MySQL .NET Connector
    Version     : 03.01.00
    License     : GPL-3.0-or-later

.EXAMPLE
    .\Invoke-DemoDataLoaderGUI.ps1
    Launches the GUI for demo data loading.
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

function Show-DemoDataLoaderForm {
    <#
    .SYNOPSIS
        Displays the main demo data loader GUI form.
    #>
    [CmdletBinding()]
    param()
    
    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
        Add-Type -AssemblyName System.Drawing -ErrorAction Stop
        
        # Create main form
        $form = New-Object System.Windows.Forms.Form -Property @{
            Text            = 'Demo Data Loader v03.01.00'
            Size            = New-Object System.Drawing.Size(600, 650)
            StartPosition   = 'CenterScreen'
            FormBorderStyle = 'FixedDialog'
            MaximizeBox     = $false
            MinimizeBox     = $false
        }
        
        # Title Label
        $titleLabel = New-Object System.Windows.Forms.Label -Property @{
            Text      = 'Load SQL Demo Data'
            Location  = New-Object System.Drawing.Point(20, 20)
            Size      = New-Object System.Drawing.Size(550, 30)
            Font      = New-Object System.Drawing.Font('Segoe UI', 14, [System.Drawing.FontStyle]::Bold)
        }
        $form.Controls.Add($titleLabel)
        
        # SQL File Selection
        $sqlFileLabel = New-Object System.Windows.Forms.Label -Property @{
            Text     = 'SQL File:'
            Location = New-Object System.Drawing.Point(20, 70)
            Size     = New-Object System.Drawing.Size(100, 20)
        }
        $form.Controls.Add($sqlFileLabel)
        
        $sqlFileTextBox = New-Object System.Windows.Forms.TextBox -Property @{
            Location = New-Object System.Drawing.Point(120, 70)
            Size     = New-Object System.Drawing.Size(350, 20)
        }
        $form.Controls.Add($sqlFileTextBox)
        
        $sqlFileBrowseButton = New-Object System.Windows.Forms.Button -Property @{
            Text     = 'Browse...'
            Location = New-Object System.Drawing.Point(480, 68)
            Size     = New-Object System.Drawing.Size(90, 25)
        }
        $sqlFileBrowseButton.Add_Click({
            $file = Select-FileGUI -Title 'Select SQL File' -Filter 'SQL Files (*.sql)|*.sql|All Files (*.*)|*.*'
            if ($file) {
                $sqlFileTextBox.Text = $file
            }
        })
        $form.Controls.Add($sqlFileBrowseButton)
        
        # Config File Selection
        $configFileLabel = New-Object System.Windows.Forms.Label -Property @{
            Text     = 'Config File (Optional):'
            Location = New-Object System.Drawing.Point(20, 110)
            Size     = New-Object System.Drawing.Size(150, 20)
        }
        $form.Controls.Add($configFileLabel)
        
        $configFileTextBox = New-Object System.Windows.Forms.TextBox -Property @{
            Location = New-Object System.Drawing.Point(170, 110)
            Size     = New-Object System.Drawing.Size(300, 20)
        }
        $form.Controls.Add($configFileTextBox)
        
        $configFileBrowseButton = New-Object System.Windows.Forms.Button -Property @{
            Text     = 'Browse...'
            Location = New-Object System.Drawing.Point(480, 108)
            Size     = New-Object System.Drawing.Size(90, 25)
        }
        $configFileBrowseButton.Add_Click({
            $file = Select-FileGUI -Title 'Select Config File' -Filter 'PHP Files (*.php)|*.php|All Files (*.*)|*.*'
            if ($file) {
                $configFileTextBox.Text = $file
            }
        })
        $form.Controls.Add($configFileBrowseButton)
        
        # Database Connection Group
        $dbGroupBox = New-Object System.Windows.Forms.GroupBox -Property @{
            Text     = 'Database Connection'
            Location = New-Object System.Drawing.Point(20, 150)
            Size     = New-Object System.Drawing.Size(550, 240)
        }
        $form.Controls.Add($dbGroupBox)
        
        # Host
        $hostLabel = New-Object System.Windows.Forms.Label -Property @{
            Text     = 'Host:'
            Location = New-Object System.Drawing.Point(10, 30)
            Size     = New-Object System.Drawing.Size(80, 20)
        }
        $dbGroupBox.Controls.Add($hostLabel)
        
        $hostTextBox = New-Object System.Windows.Forms.TextBox -Property @{
            Text     = 'localhost'
            Location = New-Object System.Drawing.Point(100, 30)
            Size     = New-Object System.Drawing.Size(200, 20)
        }
        $dbGroupBox.Controls.Add($hostTextBox)
        
        # Port
        $portLabel = New-Object System.Windows.Forms.Label -Property @{
            Text     = 'Port:'
            Location = New-Object System.Drawing.Point(320, 30)
            Size     = New-Object System.Drawing.Size(40, 20)
        }
        $dbGroupBox.Controls.Add($portLabel)
        
        $portTextBox = New-Object System.Windows.Forms.TextBox -Property @{
            Text     = '3306'
            Location = New-Object System.Drawing.Point(370, 30)
            Size     = New-Object System.Drawing.Size(100, 20)
        }
        $dbGroupBox.Controls.Add($portTextBox)
        
        # User
        $userLabel = New-Object System.Windows.Forms.Label -Property @{
            Text     = 'User:'
            Location = New-Object System.Drawing.Point(10, 70)
            Size     = New-Object System.Drawing.Size(80, 20)
        }
        $dbGroupBox.Controls.Add($userLabel)
        
        $userTextBox = New-Object System.Windows.Forms.TextBox -Property @{
            Text     = 'root'
            Location = New-Object System.Drawing.Point(100, 70)
            Size     = New-Object System.Drawing.Size(200, 20)
        }
        $dbGroupBox.Controls.Add($userTextBox)
        
        # Password
        $passwordLabel = New-Object System.Windows.Forms.Label -Property @{
            Text     = 'Password:'
            Location = New-Object System.Drawing.Point(10, 110)
            Size     = New-Object System.Drawing.Size(80, 20)
        }
        $dbGroupBox.Controls.Add($passwordLabel)
        
        $passwordTextBox = New-Object System.Windows.Forms.TextBox -Property @{
            Location     = New-Object System.Drawing.Point(100, 110)
            Size         = New-Object System.Drawing.Size(200, 20)
            PasswordChar = '*'
        }
        $dbGroupBox.Controls.Add($passwordTextBox)
        
        # Database
        $databaseLabel = New-Object System.Windows.Forms.Label -Property @{
            Text     = 'Database:'
            Location = New-Object System.Drawing.Point(10, 150)
            Size     = New-Object System.Drawing.Size(80, 20)
        }
        $dbGroupBox.Controls.Add($databaseLabel)
        
        $databaseTextBox = New-Object System.Windows.Forms.TextBox -Property @{
            Location = New-Object System.Drawing.Point(100, 150)
            Size     = New-Object System.Drawing.Size(200, 20)
        }
        $dbGroupBox.Controls.Add($databaseTextBox)
        
        # Table Prefix
        $prefixLabel = New-Object System.Windows.Forms.Label -Property @{
            Text     = 'Table Prefix:'
            Location = New-Object System.Drawing.Point(10, 190)
            Size     = New-Object System.Drawing.Size(80, 20)
        }
        $dbGroupBox.Controls.Add($prefixLabel)
        
        $prefixTextBox = New-Object System.Windows.Forms.TextBox -Property @{
            Location = New-Object System.Drawing.Point(100, 190)
            Size     = New-Object System.Drawing.Size(200, 20)
        }
        $dbGroupBox.Controls.Add($prefixTextBox)
        
        # Skip IP Check
        $skipIpCheckBox = New-Object System.Windows.Forms.CheckBox -Property @{
            Text     = 'Skip IP whitelist check (not recommended)'
            Location = New-Object System.Drawing.Point(20, 410)
            Size     = New-Object System.Drawing.Size(350, 20)
        }
        $form.Controls.Add($skipIpCheckBox)
        
        # Output TextBox
        $outputLabel = New-Object System.Windows.Forms.Label -Property @{
            Text     = 'Output:'
            Location = New-Object System.Drawing.Point(20, 450)
            Size     = New-Object System.Drawing.Size(100, 20)
        }
        $form.Controls.Add($outputLabel)
        
        $outputTextBox = New-Object System.Windows.Forms.TextBox -Property @{
            Location   = New-Object System.Drawing.Point(20, 475)
            Size       = New-Object System.Drawing.Size(550, 80)
            Multiline  = $true
            ScrollBars = 'Vertical'
            ReadOnly   = $true
        }
        $form.Controls.Add($outputTextBox)
        
        # Load Button
        $loadButton = New-Object System.Windows.Forms.Button -Property @{
            Text     = 'Load Data'
            Location = New-Object System.Drawing.Point(380, 570)
            Size     = New-Object System.Drawing.Size(100, 30)
            Font     = New-Object System.Drawing.Font('Segoe UI', 10, [System.Drawing.FontStyle]::Bold)
        }
        $loadButton.Add_Click({
            try {
                $outputTextBox.Clear()
                $outputTextBox.AppendText("Loading demo data...`r`n")
                
                # Build command
                $pythonScript = Join-Path $scriptRoot 'load_demo_data.py'
                $args = @('python3', $pythonScript, '--sql', $sqlFileTextBox.Text)
                
                if ($configFileTextBox.Text) {
                    $args += '--config', $configFileTextBox.Text
                }
                
                if ($hostTextBox.Text) { $args += '--host', $hostTextBox.Text }
                if ($portTextBox.Text) { $args += '--port', $portTextBox.Text }
                if ($userTextBox.Text) { $args += '--user', $userTextBox.Text }
                if ($passwordTextBox.Text) { $args += '--password', $passwordTextBox.Text }
                if ($databaseTextBox.Text) { $args += '--database', $databaseTextBox.Text }
                if ($prefixTextBox.Text) { $args += '--prefix', $prefixTextBox.Text }
                if ($skipIpCheckBox.Checked) { $args += '--no-ip-check' }
                
                # Execute
                $output = & $args[0] $args[1..($args.Count-1)] 2>&1
                $outputTextBox.AppendText($output -join "`r`n")
                $outputTextBox.AppendText("`r`n`r`nCompleted!")
                
                [System.Windows.Forms.MessageBox]::Show(
                    'Demo data loaded successfully!',
                    'Success',
                    'OK',
                    'Information'
                )
            }
            catch {
                $outputTextBox.AppendText("`r`nError: $($_.Exception.Message)")
                [System.Windows.Forms.MessageBox]::Show(
                    "Error loading data: $($_.Exception.Message)",
                    'Error',
                    'OK',
                    'Error'
                )
            }
        })
        $form.Controls.Add($loadButton)
        
        # Close Button
        $closeButton = New-Object System.Windows.Forms.Button -Property @{
            Text     = 'Close'
            Location = New-Object System.Drawing.Point(490, 570)
            Size     = New-Object System.Drawing.Size(80, 30)
        }
        $closeButton.Add_Click({ $form.Close() })
        $form.Controls.Add($closeButton)
        
        # Show form
        [void]$form.ShowDialog()
    }
    catch {
        Write-Error "Failed to create GUI: $_"
        throw
    }
}

#endregion

#region Main

try {
    Write-Verbose 'Starting Demo Data Loader GUI...'
    Show-DemoDataLoaderForm
}
catch {
    Write-Error "Failed to launch GUI: $_"
    exit 1
}

#endregion
