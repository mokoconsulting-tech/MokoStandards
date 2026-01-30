# Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# (./LICENSE).
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.PowerShell
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/powershell/lib/Common.psm1
# VERSION: 02.00.00
# BRIEF: Common PowerShell utilities for MokoStandards scripts
# PATH: /scripts/powershell/lib/Common.psm1
# NOTE: PowerShell equivalent of Python common.py v05.00.00

<#
.SYNOPSIS
    Common PowerShell Library for MokoStandards Scripts

.DESCRIPTION
    This module provides reusable utilities for MokoStandards scripts including:
    - Logging and output formatting
    - Process execution with timeout support
    - Path and file operations with atomic writes
    - Human-readable formatting utilities
    - Repository introspection

.NOTES
    Version: 02.00.00
    PowerShell equivalent of Python common.py v05.00.00
#>

#Requires -Version 5.1

# ============================================================
# Module Variables
# ============================================================

$script:ModuleVersion = "02.00.00"
$script:RepoUrl = "https://github.com/mokoconsulting-tech/MokoStandards"
$script:Copyright = "Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>"
$script:License = "GPL-3.0-or-later"

# Exit codes
$script:ExitSuccess = 0
$script:ExitError = 1
$script:ExitInvalidArgs = 2
$script:ExitNotFound = 3
$script:ExitPermission = 4
$script:ExitTimeout = 5


# ============================================================
# Repository Utilities
# ============================================================

function Get-RepositoryRoot {
    <#
    .SYNOPSIS
        Find the repository root by looking for .git directory.

    .DESCRIPTION
        Searches upward from the current directory to find the git repository
        root. Stops at filesystem root if no .git directory is found.

    .OUTPUTS
        System.IO.DirectoryInfo - Repository root directory

    .EXAMPLE
        $root = Get-RepositoryRoot
        Write-Host "Repository root: $root"

    .NOTES
        Throws an error if not in a git repository.
    #>
    [CmdletBinding()]
    [OutputType([System.IO.DirectoryInfo])]
    param()

    $current = Get-Location
    $currentPath = $current.Path

    while ($true) {
        $gitPath = Join-Path -Path $currentPath -ChildPath ".git"
        
        if (Test-Path -Path $gitPath) {
            Write-Verbose "Found repository root: $currentPath"
            return [System.IO.DirectoryInfo]::new($currentPath)
        }

        $parent = Split-Path -Path $currentPath -Parent
        
        if (-not $parent -or $parent -eq $currentPath) {
            throw "Not in a git repository"
        }

        $currentPath = $parent
    }
}


function Get-RelativePath {
    <#
    .SYNOPSIS
        Get relative path from repository root or current directory.

    .DESCRIPTION
        Converts an absolute path to a relative path, either from the repository
        root or from the current working directory.

    .PARAMETER Path
        Path to convert (accepts pipeline input)

    .PARAMETER FromRoot
        If true, relative to repo root; if false, relative to current directory

    .OUTPUTS
        System.String - Relative path (with leading / if FromRoot is $true)

    .EXAMPLE
        Get-RelativePath -Path "C:\repo\scripts\test.ps1" -FromRoot
        Returns: /scripts/test.ps1

    .EXAMPLE
        "C:\repo\scripts\test.ps1" | Get-RelativePath
        Returns: /scripts/test.ps1
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 0)]
        [ValidateNotNullOrEmpty()]
        [string]$Path,

        [Parameter(Position = 1)]
        [switch]$FromRoot = $true
    )

    process {
        $resolvedPath = Resolve-Path -Path $Path -ErrorAction SilentlyContinue
        if (-not $resolvedPath) {
            $resolvedPath = $Path
        } else {
            $resolvedPath = $resolvedPath.Path
        }

        if ($FromRoot) {
            try {
                $root = Get-RepositoryRoot
                $relativePath = $resolvedPath.Replace($root.FullName, "")
                $relativePath = $relativePath.Replace("\", "/")
                
                if (-not $relativePath.StartsWith("/")) {
                    $relativePath = "/" + $relativePath
                }
                
                Write-Verbose "Relative path from root: $relativePath"
                return $relativePath
            }
            catch {
                Write-Verbose "Could not resolve relative to root: $_"
                return $resolvedPath
            }
        }
        else {
            try {
                $currentDir = Get-Location
                $relativePath = $resolvedPath.Replace($currentDir.Path, "")
                $relativePath = $relativePath.TrimStart("\", "/")
                Write-Verbose "Relative path from current: $relativePath"
                return $relativePath
            }
            catch {
                return $resolvedPath
            }
        }
    }
}


# ============================================================
# Process Execution
# ============================================================

function Invoke-Command {
    <#
    .SYNOPSIS
        Execute a command with timeout support and error handling.

    .DESCRIPTION
        Runs a process with configurable timeout, output capture, and error handling.
        Provides a clean interface for command execution with proper exception handling.

    .PARAMETER Command
        Command to execute (string or array)

    .PARAMETER Arguments
        Command arguments as array

    .PARAMETER TimeoutSeconds
        Timeout in seconds (default: no timeout)

    .PARAMETER NoThrow
        If specified, do not throw on non-zero exit code

    .PARAMETER WorkingDirectory
        Working directory for command (default: current directory)

    .PARAMETER Environment
        Additional environment variables as hashtable

    .OUTPUTS
        PSCustomObject with properties: ExitCode, StandardOutput, StandardError

    .EXAMPLE
        $result = Invoke-Command -Command "git" -Arguments "status"
        Write-Host $result.StandardOutput

    .EXAMPLE
        $result = Invoke-Command -Command "npm" -Arguments "test" -TimeoutSeconds 300

    .NOTES
        Throws an error if command fails (unless -NoThrow is specified) or times out.
    #>
    [CmdletBinding()]
    [OutputType([PSCustomObject])]
    param(
        [Parameter(Mandatory = $true, Position = 0)]
        [ValidateNotNullOrEmpty()]
        [string]$Command,

        [Parameter(Position = 1)]
        [string[]]$Arguments = @(),

        [Parameter()]
        [ValidateRange(1, [int]::MaxValue)]
        [int]$TimeoutSeconds,

        [Parameter()]
        [switch]$NoThrow,

        [Parameter()]
        [string]$WorkingDirectory,

        [Parameter()]
        [hashtable]$Environment
    )

    $processInfo = New-Object System.Diagnostics.ProcessStartInfo
    $processInfo.FileName = $Command
    $processInfo.RedirectStandardError = $true
    $processInfo.RedirectStandardOutput = $true
    $processInfo.UseShellExecute = $false
    $processInfo.CreateNoWindow = $true
    
    if ($Arguments.Count -gt 0) {
        $processInfo.Arguments = $Arguments -join " "
    }

    if ($WorkingDirectory) {
        $processInfo.WorkingDirectory = $WorkingDirectory
    }

    if ($Environment) {
        foreach ($key in $Environment.Keys) {
            $processInfo.Environment[$key] = $Environment[$key]
        }
    }

    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $processInfo

    $stdoutBuilder = New-Object System.Text.StringBuilder
    $stderrBuilder = New-Object System.Text.StringBuilder

    $stdoutEvent = Register-ObjectEvent -InputObject $process -EventName OutputDataReceived -Action {
        if ($EventArgs.Data) {
            $Event.MessageData.AppendLine($EventArgs.Data) | Out-Null
        }
    } -MessageData $stdoutBuilder

    $stderrEvent = Register-ObjectEvent -InputObject $process -EventName ErrorDataReceived -Action {
        if ($EventArgs.Data) {
            $Event.MessageData.AppendLine($EventArgs.Data) | Out-Null
        }
    } -MessageData $stderrBuilder

    try {
        Write-Verbose "Executing: $Command $($Arguments -join ' ')"
        $process.Start() | Out-Null
        $process.BeginOutputReadLine()
        $process.BeginErrorReadLine()

        if ($TimeoutSeconds) {
            $completed = $process.WaitForExit($TimeoutSeconds * 1000)
            if (-not $completed) {
                $process.Kill()
                throw "Command timed out after $TimeoutSeconds seconds: $Command"
            }
        }
        else {
            $process.WaitForExit()
        }

        # Wait for output to be fully read
        Start-Sleep -Milliseconds 100

        $exitCode = $process.ExitCode
        $stdout = $stdoutBuilder.ToString()
        $stderr = $stderrBuilder.ToString()

        if (-not $NoThrow -and $exitCode -ne 0) {
            throw "Command failed with exit code ${exitCode}: $Command"
        }

        return [PSCustomObject]@{
            ExitCode = $exitCode
            StandardOutput = $stdout
            StandardError = $stderr
        }
    }
    finally {
        Unregister-Event -SourceIdentifier $stdoutEvent.Name -ErrorAction SilentlyContinue
        Unregister-Event -SourceIdentifier $stderrEvent.Name -ErrorAction SilentlyContinue
        $process.Dispose()
    }
}


# ============================================================
# Path and File Operations
# ============================================================

function New-Directory {
    <#
    .SYNOPSIS
        Create directory and all parent directories safely.

    .DESCRIPTION
        Creates the specified directory with all necessary parent directories.
        If the directory already exists, no error is raised.

    .PARAMETER Path
        Path to directory to create (accepts pipeline input)

    .OUTPUTS
        System.IO.DirectoryInfo - Created or existing directory

    .EXAMPLE
        $dir = New-Directory -Path "C:\temp\my\nested\dir"

    .EXAMPLE
        "C:\temp\test" | New-Directory
    #>
    [CmdletBinding(SupportsShouldProcess = $true)]
    [OutputType([System.IO.DirectoryInfo])]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 0)]
        [ValidateNotNullOrEmpty()]
        [string]$Path
    )

    process {
        if ($PSCmdlet.ShouldProcess($Path, "Create directory")) {
            if (-not (Test-Path -Path $Path)) {
                Write-Verbose "Creating directory: $Path"
                $dir = New-Item -Path $Path -ItemType Directory -Force
            }
            else {
                Write-Verbose "Directory already exists: $Path"
                $dir = Get-Item -Path $Path
            }

            return $dir
        }
    }
}


function Set-FileAtomic {
    <#
    .SYNOPSIS
        Write content to a file atomically using a temporary file.

    .DESCRIPTION
        Writes content to a temporary file first, then moves it to the target
        location. This ensures that the target file is never partially written
        or corrupted if the process is interrupted.

    .PARAMETER Path
        Destination file path

    .PARAMETER Content
        Content to write to file

    .PARAMETER Encoding
        Text encoding (default: UTF8)

    .OUTPUTS
        System.IO.FileInfo - The created file

    .EXAMPLE
        Set-FileAtomic -Path "C:\temp\config.json" -Content '{"key": "value"}'

    .EXAMPLE
        '{"key": "value"}' | Set-FileAtomic -Path "config.json"
    #>
    [CmdletBinding(SupportsShouldProcess = $true)]
    [OutputType([System.IO.FileInfo])]
    param(
        [Parameter(Mandatory = $true, Position = 0)]
        [ValidateNotNullOrEmpty()]
        [string]$Path,

        [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 1)]
        [AllowEmptyString()]
        [string]$Content,

        [Parameter()]
        [ValidateSet('UTF8', 'UTF7', 'UTF32', 'Unicode', 'ASCII', 'Default')]
        [string]$Encoding = 'UTF8'
    )

    process {
        $targetPath = Resolve-Path -Path $Path -ErrorAction SilentlyContinue
        if (-not $targetPath) {
            $targetPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
        }

        $parentDir = Split-Path -Path $targetPath -Parent
        if ($parentDir -and -not (Test-Path -Path $parentDir)) {
            New-Directory -Path $parentDir | Out-Null
        }

        $fileName = Split-Path -Path $targetPath -Leaf
        $tempFile = Join-Path -Path $parentDir -ChildPath ".$fileName.tmp.$([Guid]::NewGuid())"

        if ($PSCmdlet.ShouldProcess($targetPath, "Write file atomically")) {
            try {
                Write-Verbose "Writing to temporary file: $tempFile"
                [System.IO.File]::WriteAllText($tempFile, $Content, [System.Text.Encoding]::$Encoding)

                Write-Verbose "Moving to target: $targetPath"
                Move-Item -Path $tempFile -Destination $targetPath -Force

                return Get-Item -Path $targetPath
            }
            catch {
                if (Test-Path -Path $tempFile) {
                    Remove-Item -Path $tempFile -Force -ErrorAction SilentlyContinue
                }
                throw
            }
        }
    }
}


# ============================================================
# Human-Readable Formatting
# ============================================================

function Format-ByteSize {
    <#
    .SYNOPSIS
        Format byte count as human-readable string.

    .DESCRIPTION
        Converts a byte count into a human-readable string using appropriate
        units (B, KB, MB, GB, TB, PB).

    .PARAMETER Bytes
        Number of bytes to format (accepts pipeline input)

    .PARAMETER Precision
        Number of decimal places (default: 2)

    .OUTPUTS
        System.String - Formatted string with appropriate unit

    .EXAMPLE
        Format-ByteSize -Bytes 1024
        Returns: 1.00 KB

    .EXAMPLE
        1536 | Format-ByteSize -Precision 1
        Returns: 1.5 KB

    .EXAMPLE
        Format-ByteSize 1048576
        Returns: 1.00 MB
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 0)]
        [ValidateRange(0, [long]::MaxValue)]
        [long]$Bytes,

        [Parameter(Position = 1)]
        [ValidateRange(0, 10)]
        [int]$Precision = 2
    )

    process {
        $units = @('B', 'KB', 'MB', 'GB', 'TB', 'PB')
        $unitIndex = 0
        $size = [double]$Bytes

        while ($size -ge 1024.0 -and $unitIndex -lt ($units.Count - 1)) {
            $size /= 1024.0
            $unitIndex++
        }

        if ($unitIndex -eq 0) {
            return "{0:N0} {1}" -f $size, $units[$unitIndex]
        }
        else {
            return "{0:N$Precision} {1}" -f $size, $units[$unitIndex]
        }
    }
}


function Format-TimeSpan {
    <#
    .SYNOPSIS
        Format duration in seconds as human-readable string.

    .DESCRIPTION
        Converts a duration in seconds into a human-readable string using
        appropriate units (s, ms, μs, ns for small durations; s, m, h, d for
        large durations).

    .PARAMETER Seconds
        Duration in seconds (accepts pipeline input)

    .PARAMETER Precision
        Number of decimal places (default: 2)

    .OUTPUTS
        System.String - Formatted string with appropriate unit

    .EXAMPLE
        Format-TimeSpan -Seconds 0.001
        Returns: 1.00 ms

    .EXAMPLE
        65 | Format-TimeSpan
        Returns: 1.08 m

    .EXAMPLE
        Format-TimeSpan 3661
        Returns: 1.02 h
    #>
    [CmdletBinding()]
    [OutputType([string])]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 0)]
        [ValidateRange(0, [double]::MaxValue)]
        [double]$Seconds,

        [Parameter(Position = 1)]
        [ValidateRange(0, 10)]
        [int]$Precision = 2
    )

    process {
        # Handle sub-second durations
        if ($Seconds -lt 1.0) {
            if ($Seconds -lt 0.000001) {
                # nanoseconds
                return "{0:N$Precision} ns" -f ($Seconds * 1000000000)
            }
            elseif ($Seconds -lt 0.001) {
                # microseconds
                return "{0:N$Precision} μs" -f ($Seconds * 1000000)
            }
            else {
                # milliseconds
                return "{0:N$Precision} ms" -f ($Seconds * 1000)
            }
        }

        # Handle larger durations
        if ($Seconds -lt 60) {
            # seconds
            return "{0:N$Precision} s" -f $Seconds
        }
        elseif ($Seconds -lt 3600) {
            # minutes
            return "{0:N$Precision} m" -f ($Seconds / 60)
        }
        elseif ($Seconds -lt 86400) {
            # hours
            return "{0:N$Precision} h" -f ($Seconds / 3600)
        }
        else {
            # days
            return "{0:N$Precision} d" -f ($Seconds / 86400)
        }
    }
}


# ============================================================
# Logging and Output
# ============================================================

function Write-InfoLog {
    <#
    .SYNOPSIS
        Print an informational message.

    .DESCRIPTION
        Writes an informational message to the information stream with an icon.

    .PARAMETER Message
        Information message to display (accepts pipeline input)

    .EXAMPLE
        Write-InfoLog "Processing files..."

    .EXAMPLE
        "Starting operation" | Write-InfoLog
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 0)]
        [string]$Message
    )

    process {
        Write-Information "ℹ️  $Message" -InformationAction Continue
    }
}


function Write-SuccessLog {
    <#
    .SYNOPSIS
        Print a success message.

    .DESCRIPTION
        Writes a success message to the information stream with a checkmark icon.

    .PARAMETER Message
        Success message to display (accepts pipeline input)

    .EXAMPLE
        Write-SuccessLog "Operation completed successfully"

    .EXAMPLE
        "Tests passed" | Write-SuccessLog
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 0)]
        [string]$Message
    )

    process {
        Write-Information "✅ $Message" -InformationAction Continue
    }
}


function Write-WarningLog {
    <#
    .SYNOPSIS
        Print a warning message.

    .DESCRIPTION
        Writes a warning message to the warning stream with a warning icon.

    .PARAMETER Message
        Warning message to display (accepts pipeline input)

    .EXAMPLE
        Write-WarningLog "Configuration file not found, using defaults"

    .EXAMPLE
        "Deprecated feature" | Write-WarningLog
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 0)]
        [string]$Message
    )

    process {
        Write-Warning "⚠️  $Message"
    }
}


function Write-ErrorLog {
    <#
    .SYNOPSIS
        Print an error message.

    .DESCRIPTION
        Writes an error message to the error stream with an error icon.

    .PARAMETER Message
        Error message to display (accepts pipeline input)

    .PARAMETER ErrorRecord
        Optional ErrorRecord to include additional error details

    .EXAMPLE
        Write-ErrorLog "Failed to connect to server"

    .EXAMPLE
        try { Get-Item "nonexistent" } catch { Write-ErrorLog "File operation failed" -ErrorRecord $_ }
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 0)]
        [string]$Message,

        [Parameter()]
        [System.Management.Automation.ErrorRecord]$ErrorRecord
    )

    process {
        if ($ErrorRecord) {
            Write-Error "❌ $Message - $($ErrorRecord.Exception.Message)"
        }
        else {
            Write-Error "❌ $Message"
        }
    }
}


# ============================================================
# Module Exports
# ============================================================

Export-ModuleMember -Function @(
    'Get-RepositoryRoot',
    'Get-RelativePath',
    'Invoke-Command',
    'New-Directory',
    'Set-FileAtomic',
    'Format-ByteSize',
    'Format-TimeSpan',
    'Write-InfoLog',
    'Write-SuccessLog',
    'Write-WarningLog',
    'Write-ErrorLog'
)

Export-ModuleMember -Variable @(
    'ModuleVersion',
    'RepoUrl',
    'Copyright',
    'License',
    'ExitSuccess',
    'ExitError',
    'ExitInvalidArgs',
    'ExitNotFound',
    'ExitPermission',
    'ExitTimeout'
)
