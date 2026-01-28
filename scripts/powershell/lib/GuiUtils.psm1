<#
.SYNOPSIS
    GUI utilities module for MokoStandards PowerShell scripts.

.DESCRIPTION
    Provides reusable GUI components for Windows-based scripts using Windows.Forms.
    Includes file/folder selection dialogs, option forms, progress windows, and more.

.NOTES
    File Name   : GuiUtils.psm1
    Author      : Moko Consulting <hello@mokoconsulting.tech>
    Requires    : PowerShell 5.1 or later, Windows OS
    Version     : 03.00.00
    License     : GPL-3.0-or-later
#>

#Requires -Version 5.1

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

#region File and Folder Selection

function Select-FileGUI {
    <#
    .SYNOPSIS
        Displays a file selection dialog.
    
    .PARAMETER Title
        Title of the dialog window.
    
    .PARAMETER Filter
        File type filter (e.g., 'All Files (*.*)|*.*|Python Files (*.py)|*.py').
    
    .PARAMETER Multiselect
        Allow selecting multiple files.
    
    .EXAMPLE
        $file = Select-FileGUI -Title 'Select Python Script' -Filter 'Python Files (*.py)|*.py'
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param(
        [Parameter()]
        [string]$Title = 'Select File',
        
        [Parameter()]
        [string]$Filter = 'All Files (*.*)|*.*',
        
        [Parameter()]
        [switch]$Multiselect
    )
    
    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
        
        $dialog = New-Object System.Windows.Forms.OpenFileDialog -Property @{
            Title            = $Title
            Filter           = $Filter
            FilterIndex      = 1
            Multiselect      = $Multiselect.IsPresent
            CheckFileExists  = $true
            CheckPathExists  = $true
            RestoreDirectory = $true
        }
        
        $result = $dialog.ShowDialog()
        
        if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
            if ($Multiselect.IsPresent) {
                return $dialog.FileNames
            }
            else {
                return $dialog.FileName
            }
        }
        else {
            throw 'File selection cancelled by user'
        }
    }
    finally {
        if ($dialog) { $dialog.Dispose() }
    }
}

function Select-FolderGUI {
    <#
    .SYNOPSIS
        Displays a folder selection dialog.
    
    .PARAMETER Title
        Description text for the dialog.
    
    .PARAMETER ShowNewFolderButton
        Show button to create new folders.
    
    .EXAMPLE
        $folder = Select-FolderGUI -Title 'Select Repository Root'
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param(
        [Parameter()]
        [string]$Title = 'Select Folder',
        
        [Parameter()]
        [switch]$ShowNewFolderButton
    )
    
    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
        
        $dialog = New-Object System.Windows.Forms.FolderBrowserDialog -Property @{
            Description         = $Title
            ShowNewFolderButton = $ShowNewFolderButton.IsPresent
            RootFolder          = [System.Environment+SpecialFolder]::MyComputer
        }
        
        $result = $dialog.ShowDialog()
        
        if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
            return $dialog.SelectedPath
        }
        else {
            throw 'Folder selection cancelled by user'
        }
    }
    finally {
        if ($dialog) { $dialog.Dispose() }
    }
}

#endregion

#region Message Boxes

function Show-InfoMessage {
    <#
    .SYNOPSIS
        Displays an informational message box.
    
    .EXAMPLE
        Show-InfoMessage -Title 'Success' -Message 'Operation completed successfully'
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Title,
        
        [Parameter(Mandatory)]
        [string]$Message
    )
    
    Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
    [System.Windows.Forms.MessageBox]::Show(
        $Message,
        $Title,
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    ) | Out-Null
}

function Show-WarningMessage {
    <#
    .SYNOPSIS
        Displays a warning message box.
    
    .EXAMPLE
        Show-WarningMessage -Title 'Warning' -Message 'This operation cannot be undone'
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Title,
        
        [Parameter(Mandatory)]
        [string]$Message
    )
    
    Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
    [System.Windows.Forms.MessageBox]::Show(
        $Message,
        $Title,
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Warning
    ) | Out-Null
}

function Show-ErrorMessage {
    <#
    .SYNOPSIS
        Displays an error message box.
    
    .EXAMPLE
        Show-ErrorMessage -Title 'Error' -Message 'Operation failed'
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Title,
        
        [Parameter(Mandatory)]
        [string]$Message
    )
    
    Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
    [System.Windows.Forms.MessageBox]::Show(
        $Message,
        $Title,
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    ) | Out-Null
}

function Show-ConfirmDialog {
    <#
    .SYNOPSIS
        Displays a confirmation dialog with Yes/No buttons.
    
    .EXAMPLE
        if (Show-ConfirmDialog -Title 'Confirm' -Message 'Proceed?') { ... }
    #>
    [CmdletBinding()]
    [OutputType([bool])]
    param(
        [Parameter(Mandatory)]
        [string]$Title,
        
        [Parameter(Mandatory)]
        [string]$Message
    )
    
    Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
    $result = [System.Windows.Forms.MessageBox]::Show(
        $Message,
        $Title,
        [System.Windows.Forms.MessageBoxButtons]::YesNo,
        [System.Windows.Forms.MessageBoxIcon]::Question
    )
    
    return ($result -eq [System.Windows.Forms.DialogResult]::Yes)
}

#endregion

#region Input Dialogs

function Show-InputDialog {
    <#
    .SYNOPSIS
        Displays a simple input dialog for text entry.
    
    .EXAMPLE
        $name = Show-InputDialog -Title 'Enter Name' -Prompt 'Your name:'
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param(
        [Parameter(Mandatory)]
        [string]$Title,
        
        [Parameter(Mandatory)]
        [string]$Prompt,
        
        [Parameter()]
        [string]$DefaultValue = ''
    )
    
    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
        Add-Type -AssemblyName System.Drawing -ErrorAction Stop
        
        $form = New-Object System.Windows.Forms.Form -Property @{
            Text            = $Title
            StartPosition   = 'CenterScreen'
            FormBorderStyle = 'FixedDialog'
            MaximizeBox     = $false
            MinimizeBox     = $false
            ClientSize      = New-Object System.Drawing.Size(400, 150)
            Topmost         = $true
        }
        
        $label = New-Object System.Windows.Forms.Label -Property @{
            Location = New-Object System.Drawing.Point(10, 20)
            Size     = New-Object System.Drawing.Size(380, 20)
            Text     = $Prompt
        }
        
        $textbox = New-Object System.Windows.Forms.TextBox -Property @{
            Location = New-Object System.Drawing.Point(10, 50)
            Size     = New-Object System.Drawing.Size(380, 20)
            Text     = $DefaultValue
        }
        
        $okButton = New-Object System.Windows.Forms.Button -Property @{
            Location     = New-Object System.Drawing.Point(220, 90)
            Size         = New-Object System.Drawing.Size(80, 30)
            Text         = 'OK'
            DialogResult = [System.Windows.Forms.DialogResult]::OK
        }
        
        $cancelButton = New-Object System.Windows.Forms.Button -Property @{
            Location     = New-Object System.Drawing.Point(310, 90)
            Size         = New-Object System.Drawing.Size(80, 30)
            Text         = 'Cancel'
            DialogResult = [System.Windows.Forms.DialogResult]::Cancel
        }
        
        $form.Controls.AddRange(@($label, $textbox, $okButton, $cancelButton))
        $form.AcceptButton = $okButton
        $form.CancelButton = $cancelButton
        
        $result = $form.ShowDialog()
        
        if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
            return $textbox.Text
        }
        else {
            throw 'Input cancelled by user'
        }
    }
    finally {
        if ($form) { $form.Dispose() }
    }
}

#endregion

#region Progress Windows

function New-ProgressWindow {
    <#
    .SYNOPSIS
        Creates a progress window for long-running operations.
    
    .EXAMPLE
        $progress = New-ProgressWindow -Title 'Processing' -Message 'Please wait...'
        # ... do work ...
        $progress.Close()
    #>
    [CmdletBinding()]
    [OutputType([System.Windows.Forms.Form])]
    param(
        [Parameter(Mandatory)]
        [string]$Title,
        
        [Parameter(Mandatory)]
        [string]$Message
    )
    
    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction Stop
        Add-Type -AssemblyName System.Drawing -ErrorAction Stop
        
        $form = New-Object System.Windows.Forms.Form -Property @{
            Text            = $Title
            StartPosition   = 'CenterScreen'
            FormBorderStyle = 'FixedDialog'
            MaximizeBox     = $false
            MinimizeBox     = $false
            ControlBox      = $false
            ClientSize      = New-Object System.Drawing.Size(400, 120)
            Topmost         = $true
        }
        
        $label = New-Object System.Windows.Forms.Label -Property @{
            Location  = New-Object System.Drawing.Point(10, 20)
            Size      = New-Object System.Drawing.Size(380, 40)
            Text      = $Message
            TextAlign = [System.Drawing.ContentAlignment]::MiddleCenter
        }
        
        $progressBar = New-Object System.Windows.Forms.ProgressBar -Property @{
            Location = New-Object System.Drawing.Point(10, 70)
            Size     = New-Object System.Drawing.Size(380, 30)
            Style    = 'Marquee'
        }
        
        $form.Controls.AddRange(@($label, $progressBar))
        $form.Show()
        $form.Refresh()
        
        return $form
    }
    catch {
        if ($form) { $form.Dispose() }
        throw
    }
}

#endregion

# Export module members
Export-ModuleMember -Function @(
    'Select-FileGUI',
    'Select-FolderGUI',
    'Show-InfoMessage',
    'Show-WarningMessage',
    'Show-ErrorMessage',
    'Show-ConfirmDialog',
    'Show-InputDialog',
    'New-ProgressWindow'
)
