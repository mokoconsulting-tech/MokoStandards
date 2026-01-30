<#
.SYNOPSIS
    Visual output utilities for PowerShell scripts.

.DESCRIPTION
    Provides rich console output including colored messages, progress indicators,
    boxes, tables, and status messages for MokoStandards PowerShell scripts.

.NOTES
    File Name   : VisualUtils.psm1
    Author      : Moko Consulting <hello@mokoconsulting.tech>
    Requires    : PowerShell 5.1 or later
    Version     : 03.01.00
    License     : GPL-3.0-or-later
#>

#Requires -Version 5.1

Set-StrictMode -Version Latest

#region Color Utilities

function Write-ColorText {
    <#
    .SYNOPSIS
        Write colored text to console.
    
    .PARAMETER Text
        Text to display
    
    .PARAMETER ForegroundColor
        Text color
    
    .PARAMETER BackgroundColor
        Background color
    
    .PARAMETER NoNewline
        Don't add newline at end
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory, ValueFromPipeline)]
        [string]$Text,
        
        [Parameter()]
        [ConsoleColor]$ForegroundColor = [ConsoleColor]::White,
        
        [Parameter()]
        [ConsoleColor]$BackgroundColor,
        
        [Parameter()]
        [switch]$NoNewline
    )
    
    $params = @{
        Object          = $Text
        ForegroundColor = $ForegroundColor
    }
    
    if ($PSBoundParameters.ContainsKey('BackgroundColor')) {
        $params.BackgroundColor = $BackgroundColor
    }
    
    if ($NoNewline) {
        $params.NoNewline = $true
    }
    
    Write-Host @params
}

#endregion

#region Status Messages

function Write-SuccessMessage {
    <#
    .SYNOPSIS
        Write a success message with checkmark.
    
    .PARAMETER Message
        Success message to display
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Message
    )
    
    Write-ColorText " ✓ $Message" -ForegroundColor Green
}

function Write-ErrorMessage {
    <#
    .SYNOPSIS
        Write an error message with X.
    
    .PARAMETER Message
        Error message to display
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Message
    )
    
    Write-ColorText " ✗ $Message" -ForegroundColor Red
}

function Write-WarningMessage {
    <#
    .SYNOPSIS
        Write a warning message.
    
    .PARAMETER Message
        Warning message to display
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Message
    )
    
    Write-ColorText " ⚠ $Message" -ForegroundColor Yellow
}

function Write-InfoMessage {
    <#
    .SYNOPSIS
        Write an info message.
    
    .PARAMETER Message
        Info message to display
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Message
    )
    
    Write-ColorText " ℹ $Message" -ForegroundColor Cyan
}

#endregion

#region Visual Components

function Write-Header {
    <#
    .SYNOPSIS
        Write a formatted header with box.
    
    .PARAMETER Title
        Main title
    
    .PARAMETER Subtitle
        Optional subtitle
    
    .PARAMETER Width
        Box width
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Title,
        
        [Parameter()]
        [string]$Subtitle,
        
        [Parameter()]
        [int]$Width = 70
    )
    
    $topBorder = '╔' + ('═' * ($Width - 2)) + '╗'
    $bottomBorder = '╚' + ('═' * ($Width - 2)) + '╝'
    
    Write-Host ''
    Write-ColorText $topBorder -ForegroundColor Cyan
    
    $titleLine = $Title.PadLeft(($Width - 2 + $Title.Length) / 2).PadRight($Width - 2)
    Write-ColorText "║$titleLine║" -ForegroundColor White
    
    if ($Subtitle) {
        $subtitleLine = $Subtitle.PadLeft(($Width - 2 + $Subtitle.Length) / 2).PadRight($Width - 2)
        Write-ColorText "║$subtitleLine║" -ForegroundColor DarkGray
    }
    
    Write-ColorText $bottomBorder -ForegroundColor Cyan
    Write-Host ''
}

function Write-Box {
    <#
    .SYNOPSIS
        Write a message in a colored box.
    
    .PARAMETER Message
        Message to display
    
    .PARAMETER Type
        Box type (Info, Success, Warning, Error)
    
    .PARAMETER Width
        Box width
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Message,
        
        [Parameter()]
        [ValidateSet('Info', 'Success', 'Warning', 'Error')]
        [string]$Type = 'Info',
        
        [Parameter()]
        [int]$Width = 70
    )
    
    $colorMap = @{
        'Info'    = [ConsoleColor]::Cyan
        'Success' = [ConsoleColor]::Green
        'Warning' = [ConsoleColor]::Yellow
        'Error'   = [ConsoleColor]::Red
    }
    
    $color = $colorMap[$Type]
    
    # Split message into lines
    $words = $Message -split '\s+'
    $lines = @()
    $currentLine = ''
    
    foreach ($word in $words) {
        if (($currentLine.Length + $word.Length + 1) -le ($Width - 6)) {
            $currentLine += " $word"
        }
        else {
            if ($currentLine) {
                $lines += $currentLine.Trim()
            }
            $currentLine = $word
        }
    }
    
    if ($currentLine) {
        $lines += $currentLine.Trim()
    }
    
    # Print box
    Write-Host ''
    Write-ColorText ('┌' + ('─' * ($Width - 2)) + '┐') -ForegroundColor $color
    
    foreach ($line in $lines) {
        $paddedLine = $line.PadRight($Width - 4)
        Write-ColorText "│ $paddedLine │" -ForegroundColor $color
    }
    
    Write-ColorText ('└' + ('─' * ($Width - 2)) + '┘') -ForegroundColor $color
    Write-Host ''
}

function Write-ProgressBar {
    <#
    .SYNOPSIS
        Write a visual progress bar.
    
    .PARAMETER Current
        Current progress value
    
    .PARAMETER Total
        Total value
    
    .PARAMETER Activity
        Activity description
    
    .PARAMETER Width
        Bar width in characters
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [int]$Current,
        
        [Parameter(Mandatory)]
        [int]$Total,
        
        [Parameter()]
        [string]$Activity = 'Progress',
        
        [Parameter()]
        [int]$Width = 50
    )
    
    $percent = if ($Total -gt 0) { ($Current / $Total) * 100 } else { 0 }
    $filled = if ($Total -gt 0) { [int]($Width * $Current / $Total) } else { 0 }
    $empty = $Width - $filled
    
    $bar = ('█' * $filled) + ('░' * $empty)
    
    Write-Host -NoNewline "`r$Activity`: $Current/$Total "
    Write-ColorText -Text "[$bar]" -ForegroundColor Green -NoNewline
    Write-Host -NoNewline " $($percent.ToString('F1'))%"
}

function Write-Table {
    <#
    .SYNOPSIS
        Write a formatted table.
    
    .PARAMETER Headers
        Column headers
    
    .PARAMETER Rows
        Table rows (array of hashtables or objects)
    
    .PARAMETER Title
        Optional table title
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string[]]$Headers,
        
        [Parameter(Mandatory)]
        [array]$Rows,
        
        [Parameter()]
        [string]$Title
    )
    
    if ($Title) {
        Write-Host ''
        Write-ColorText $Title -ForegroundColor White
    }
    
    # Calculate column widths
    $colWidths = $Headers | ForEach-Object { $_.Length }
    
    for ($i = 0; $i < $Headers.Count; $i++) {
        $maxWidth = $Rows | ForEach-Object {
            if ($_ -is [hashtable]) {
                $_.Values[$i].ToString().Length
            }
            else {
                $_.PSObject.Properties[$i].Value.ToString().Length
            }
        } | Measure-Object -Maximum | Select-Object -ExpandProperty Maximum
        
        if ($maxWidth -gt $colWidths[$i]) {
            $colWidths[$i] = $maxWidth
        }
    }
    
    # Print table
    $topBorder = '┌─' + (($colWidths | ForEach-Object { '─' * $_ }) -join '─┬─') + '─┐'
    $separator = '├─' + (($colWidths | ForEach-Object { '─' * $_ }) -join '─┼─') + '─┤'
    $bottomBorder = '└─' + (($colWidths | ForEach-Object { '─' * $_ }) -join '─┴─') + '─┘'
    
    Write-Host $topBorder
    
    # Headers
    $headerLine = '│ ' + (
        (0..($Headers.Count - 1) | ForEach-Object {
            $Headers[$_].PadRight($colWidths[$_])
        }) -join ' │ '
    ) + ' │'
    Write-ColorText $headerLine -ForegroundColor Cyan
    
    Write-Host $separator
    
    # Rows
    foreach ($row in $Rows) {
        $values = if ($row -is [hashtable]) {
            $row.Values
        }
        else {
            $row.PSObject.Properties.Value
        }
        
        $rowLine = '│ ' + (
            (0..($Headers.Count - 1) | ForEach-Object {
                $values[$_].ToString().PadRight($colWidths[$_])
            }) -join ' │ '
        ) + ' │'
        Write-Host $rowLine
    }
    
    Write-Host $bottomBorder
    Write-Host ''
}

function Write-Summary {
    <#
    .SYNOPSIS
        Write a summary box with key-value pairs.
    
    .PARAMETER Items
        Hashtable of key-value pairs
    
    .PARAMETER Title
        Summary title
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [hashtable]$Items,
        
        [Parameter()]
        [string]$Title = 'Summary'
    )
    
    $maxKeyLen = ($Items.Keys | Measure-Object -Maximum -Property Length).Maximum
    
    Write-Host ''
    Write-ColorText ('═' * 60) -ForegroundColor Blue
    Write-ColorText "  $Title" -ForegroundColor White
    Write-ColorText ('═' * 60) -ForegroundColor Blue
    
    foreach ($key in $Items.Keys) {
        $keyStr = "$($key):".PadRight($maxKeyLen + 2)
        Write-Host -NoNewline '  '
        Write-ColorText -Text $keyStr -ForegroundColor Cyan -NoNewline
        Write-Host " $($Items[$key])"
    }
    
    Write-ColorText ('═' * 60) -ForegroundColor Blue
    Write-Host ''
}

function Read-Confirmation {
    <#
    .SYNOPSIS
        Ask for user confirmation with colored prompt.
    
    .PARAMETER Message
        Confirmation message
    
    .PARAMETER Default
        Default response (Y or N)
    
    .RETURNS
        Boolean indicating user's choice
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Message,
        
        [Parameter()]
        [ValidateSet('Y', 'N')]
        [string]$Default = 'Y'
    )
    
    $suffix = if ($Default -eq 'Y') { '[Y/n]' } else { '[y/N]' }
    
    Write-ColorText " ? $Message $suffix`: " -ForegroundColor Magenta -NoNewline
    $response = Read-Host
    
    if ([string]::IsNullOrWhiteSpace($response)) {
        return ($Default -eq 'Y')
    }
    
    return $response -match '^[Yy]'
}

#endregion

#region Export Members

Export-ModuleMember -Function @(
    'Write-ColorText',
    'Write-SuccessMessage',
    'Write-ErrorMessage',
    'Write-WarningMessage',
    'Write-InfoMessage',
    'Write-Header',
    'Write-Box',
    'Write-ProgressBar',
    'Write-Table',
    'Write-Summary',
    'Read-Confirmation'
)

#endregion
