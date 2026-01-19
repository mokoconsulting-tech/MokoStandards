<#
.SYNOPSIS
    Auto-Detect Repository Platform v02.00.00 - Critical Validator Infrastructure.

.DESCRIPTION
    This script automatically detects repository platform types with confidence scoring
    and provides JSON/CLI output for automation workflows.
    
    Platform detection capabilities:
        - Joomla/WaaS components (manifest patterns, version detection)
        - Dolibarr/CRM modules (module.php, core/ structure)
        - Generic repositories (fallback with confidence scoring)

.PARAMETER Path
    Path to repository to analyze. Defaults to current directory.

.PARAMETER OutputFormat
    Output format: Text or JSON. Defaults to Text.

.PARAMETER UseCache
    Enable caching for performance (stores results in cache directory).

.PARAMETER ClearCache
    Clear detection cache and exit.

.PARAMETER Verbose
    Enable verbose output with detailed indicators.

.EXAMPLE
    .\Invoke-PlatformDetection.ps1
    Auto-detect current repository with text output.

.EXAMPLE
    .\Invoke-PlatformDetection.ps1 -Path "C:\Projects\MyRepo" -OutputFormat JSON
    Detect specific repository with JSON output.

.EXAMPLE
    .\Invoke-PlatformDetection.ps1 -UseCache -Verbose
    Detect with caching enabled and verbose output.

.EXAMPLE
    .\Invoke-PlatformDetection.ps1 -ClearCache
    Clear detection cache.

.NOTES
    Version: 02.00.00
    Exit Codes:
        0: Success (platform detected successfully)
        1: Detection failed (no platform could be determined)
        2: Configuration error (invalid arguments or paths)
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Path = ".",
    
    [Parameter()]
    [ValidateSet("Text", "JSON")]
    [string]$OutputFormat = "Text",
    
    [Parameter()]
    [switch]$UseCache,
    
    [Parameter()]
    [switch]$ClearCache
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Version
$Script:Version = "02.00.00"

# Platform types enumeration
enum PlatformType {
    Joomla
    Dolibarr
    Generic
}

# Detection result class
class DetectionResult {
    [PlatformType]$Platform
    [int]$Confidence
    [string[]]$Indicators
    [hashtable]$Metadata
    
    DetectionResult([PlatformType]$platform, [int]$confidence, [string[]]$indicators, [hashtable]$metadata) {
        $this.Platform = $platform
        $this.Confidence = $confidence
        $this.Indicators = $indicators
        $this.Metadata = $metadata
    }
    
    [hashtable] ToHashtable() {
        return @{
            platform_type = $this.Platform.ToString().ToLower()
            confidence = $this.Confidence
            indicators = $this.Indicators
            metadata = $this.Metadata
        }
    }
}

# Detection cache class
class DetectionCache {
    [string]$CacheDir
    
    DetectionCache() {
        if ($IsWindows -or $PSVersionTable.PSVersion.Major -lt 6 -or -not $IsLinux) {
            $this.CacheDir = Join-Path $env:LOCALAPPDATA "MokoStudios\PlatformDetection"
        } else {
            $homeDir = [Environment]::GetFolderPath("UserProfile")
            $this.CacheDir = Join-Path $homeDir ".cache/mokostudios/platform_detection"
        }
        
        if (-not (Test-Path $this.CacheDir)) {
            New-Item -ItemType Directory -Path $this.CacheDir -Force | Out-Null
        }
    }
    
    [string] GetCacheKey([string]$repoPath) {
        $sha256 = [System.Security.Cryptography.SHA256]::Create()
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($repoPath)
        $hash = $sha256.ComputeHash($bytes)
        return [BitConverter]::ToString($hash).Replace("-", "").ToLower()
    }
    
    [DetectionResult] Get([string]$repoPath) {
        $cacheKey = $this.GetCacheKey($repoPath)
        $cacheFile = Join-Path $this.CacheDir "$cacheKey.json"
        
        if (-not (Test-Path $cacheFile)) {
            return $null
        }
        
        try {
            $data = Get-Content $cacheFile -Raw | ConvertFrom-Json
            
            $platform = [PlatformType]::($data.platform_type.Substring(0,1).ToUpper() + $data.platform_type.Substring(1))
            $metadata = @{}
            foreach ($prop in $data.metadata.PSObject.Properties) {
                $metadata[$prop.Name] = $prop.Value
            }
            
            return [DetectionResult]::new(
                $platform,
                $data.confidence,
                $data.indicators,
                $metadata
            )
        } catch {
            return $null
        }
    }
    
    [void] Set([string]$repoPath, [DetectionResult]$result) {
        $cacheKey = $this.GetCacheKey($repoPath)
        $cacheFile = Join-Path $this.CacheDir "$cacheKey.json"
        
        try {
            $result.ToHashtable() | ConvertTo-Json -Depth 10 | Set-Content $cacheFile -Force
        } catch {
            # Silently ignore cache write failures
        }
    }
    
    [void] Clear() {
        if (Test-Path $this.CacheDir) {
            Get-ChildItem -Path $this.CacheDir -Filter "*.json" | Remove-Item -Force -ErrorAction SilentlyContinue
        }
    }
}

# Platform detector class
class PlatformDetector {
    [string]$RepoPath
    [bool]$UseCache
    [DetectionCache]$Cache
    
    PlatformDetector([string]$repoPath, [bool]$useCache) {
        $this.RepoPath = (Resolve-Path $repoPath).Path
        $this.UseCache = $useCache
        
        if ($useCache) {
            $this.Cache = [DetectionCache]::new()
        }
        
        if (-not (Test-Path $this.RepoPath)) {
            throw "Repository path does not exist: $($this.RepoPath)"
        }
    }
    
    [DetectionResult] Detect() {
        if ($this.UseCache -and $this.Cache) {
            $cachedResult = $this.Cache.Get($this.RepoPath)
            if ($cachedResult) {
                return $cachedResult
            }
        }
        
        $joomlaResult = $this.DetectJoomla()
        if ($joomlaResult.Confidence -ge 50) {
            if ($this.UseCache -and $this.Cache) {
                $this.Cache.Set($this.RepoPath, $joomlaResult)
            }
            return $joomlaResult
        }
        
        $dolibarrResult = $this.DetectDolibarr()
        if ($dolibarrResult.Confidence -ge 50) {
            if ($this.UseCache -and $this.Cache) {
                $this.Cache.Set($this.RepoPath, $dolibarrResult)
            }
            return $dolibarrResult
        }
        
        $genericResult = $this.DetectGeneric()
        if ($this.UseCache -and $this.Cache) {
            $this.Cache.Set($this.RepoPath, $genericResult)
        }
        return $genericResult
    }
    
    [DetectionResult] DetectJoomla() {
        $confidence = 0
        $indicators = @()
        $metadata = @{}
        
        $skipDirs = @('.git', 'vendor', 'node_modules', '.github')
        
        $xmlFiles = Get-ChildItem -Path $this.RepoPath -Filter "*.xml" -Recurse -ErrorAction SilentlyContinue | 
            Where-Object {
                $skip = $false
                foreach ($skipDir in $skipDirs) {
                    if ($_.FullName -like "*\$skipDir\*" -or $_.FullName -like "*/$skipDir/*") {
                        $skip = $true
                        break
                    }
                }
                -not $skip
            }
        
        foreach ($xmlFile in $xmlFiles) {
            try {
                [xml]$xmlContent = Get-Content $xmlFile.FullName -ErrorAction Stop
                $root = $xmlContent.DocumentElement
                
                if ($root.LocalName -in @('extension', 'install')) {
                    $extType = $root.GetAttribute('type')
                    
                    if ($extType -in @('component', 'module', 'plugin', 'library', 'template', 'file')) {
                        $confidence += 50
                        $relPath = $xmlFile.FullName.Substring($this.RepoPath.Length).TrimStart('\', '/')
                        $indicators += "Joomla manifest: $relPath (type=$extType)"
                        $metadata['manifest_file'] = $relPath
                        $metadata['extension_type'] = $extType
                        
                        $versionNode = $root.SelectSingleNode('version')
                        if ($versionNode -and $versionNode.InnerText) {
                            $confidence += 10
                            $version = $versionNode.InnerText.Trim()
                            $metadata['version'] = $version
                            $indicators += "Joomla version tag: $version"
                        }
                        
                        $nameNode = $root.SelectSingleNode('name')
                        if ($nameNode -and $nameNode.InnerText) {
                            $metadata['extension_name'] = $nameNode.InnerText.Trim()
                        }
                        
                        break
                    }
                }
            } catch {
                continue
            }
        }
        
        $joomlaDirs = @('site', 'admin', 'administrator')
        foreach ($dirName in $joomlaDirs) {
            $dirPath = Join-Path $this.RepoPath $dirName
            if (Test-Path $dirPath -PathType Container) {
                $confidence += 15
                $indicators += "Joomla directory structure: $dirName/"
            }
        }
        
        $langPath = Join-Path $this.RepoPath "language\en-GB"
        if (-not (Test-Path $langPath)) {
            $langPath = Join-Path $this.RepoPath "language/en-GB"
        }
        if (Test-Path $langPath -PathType Container) {
            $confidence += 10
            $indicators += "Joomla language directory: language/en-GB/"
        }
        
        $mediaDir = Join-Path $this.RepoPath "media"
        if (Test-Path $mediaDir -PathType Container) {
            $cssFiles = Get-ChildItem -Path $mediaDir -Filter "*.css" -Recurse -ErrorAction SilentlyContinue
            if ($cssFiles) {
                $confidence += 5
                $indicators += "Joomla media directory with assets"
            }
        }
        
        $confidence = [Math]::Min($confidence, 100)
        
        return [DetectionResult]::new(
            [PlatformType]::Joomla,
            $confidence,
            $indicators,
            $metadata
        )
    }
    
    [DetectionResult] DetectDolibarr() {
        $confidence = 0
        $indicators = @()
        $metadata = @{}
        
        $skipDirs = @('.git', 'vendor', 'node_modules')
        
        $descriptorPatterns = @('mod*.class.php')
        $phpFiles = @()
        
        foreach ($pattern in $descriptorPatterns) {
            $phpFiles += Get-ChildItem -Path $this.RepoPath -Filter $pattern -Recurse -ErrorAction SilentlyContinue
        }
        
        $coreModulesPath = Join-Path $this.RepoPath "core\modules"
        if (-not (Test-Path $coreModulesPath)) {
            $coreModulesPath = Join-Path $this.RepoPath "core/modules"
        }
        if (Test-Path $coreModulesPath) {
            $phpFiles += Get-ChildItem -Path $coreModulesPath -Filter "*.php" -Recurse -ErrorAction SilentlyContinue
        }
        
        foreach ($phpFile in $phpFiles) {
            $skip = $false
            foreach ($skipDir in $skipDirs) {
                if ($phpFile.FullName -like "*\$skipDir\*" -or $phpFile.FullName -like "*/$skipDir/*") {
                    $skip = $true
                    break
                }
            }
            if ($skip) { continue }
            
            try {
                $content = Get-Content $phpFile.FullName -Raw -ErrorAction Stop
                
                $dolibarrPatterns = @(
                    'extends DolibarrModules',
                    'class mod',
                    '$this->numero',
                    '$this->rights_class',
                    'DolibarrModules',
                    'dol_include_once'
                )
                
                $patternMatches = 0
                foreach ($pattern in $dolibarrPatterns) {
                    if ($content -like "*$pattern*") {
                        $patternMatches++
                    }
                }
                
                if ($patternMatches -ge 3) {
                    $confidence += 60
                    $relPath = $phpFile.FullName.Substring($this.RepoPath.Length).TrimStart('\', '/')
                    $indicators += "Dolibarr module descriptor: $relPath"
                    $metadata['descriptor_file'] = $relPath
                    
                    if ($content -match 'class\s+(mod\w+)') {
                        $metadata['module_class'] = $matches[1]
                    }
                    
                    break
                }
            } catch {
                continue
            }
        }
        
        $dolibarrDirs = @('core/modules', 'core\modules', 'sql', 'class', 'lib', 'langs')
        $checkedDirs = @{}
        
        foreach ($dirName in $dolibarrDirs) {
            $normalizedDir = $dirName -replace '[/\\]', [System.IO.Path]::DirectorySeparatorChar
            $displayDir = $dirName -replace '\\', '/'
            
            if ($checkedDirs.ContainsKey($displayDir)) {
                continue
            }
            $checkedDirs[$displayDir] = $true
            
            $dirPath = Join-Path $this.RepoPath $normalizedDir
            if (Test-Path $dirPath -PathType Container) {
                $confidence += 8
                $indicators += "Dolibarr directory structure: $displayDir/"
            }
        }
        
        $sqlDir = Join-Path $this.RepoPath "sql"
        if (Test-Path $sqlDir -PathType Container) {
            $sqlFiles = Get-ChildItem -Path $sqlDir -Filter "*.sql" -ErrorAction SilentlyContinue
            if ($sqlFiles) {
                $confidence += 10
                $indicators += "Dolibarr SQL files: $($sqlFiles.Count) migration scripts"
                $metadata['sql_files_count'] = $sqlFiles.Count.ToString()
            }
        }
        
        $confidence = [Math]::Min($confidence, 100)
        
        return [DetectionResult]::new(
            [PlatformType]::Dolibarr,
            $confidence,
            $indicators,
            $metadata
        )
    }
    
    [DetectionResult] DetectGeneric() {
        $confidence = 50
        $indicators = @("No platform-specific markers found")
        $metadata = @{
            'checked_platforms' = 'Joomla, Dolibarr'
            'detection_reason' = 'Generic repository fallback'
        }
        
        $standardFiles = @('README.md', 'LICENSE', '.gitignore', 'composer.json', 'package.json')
        $foundFiles = @()
        
        foreach ($fileName in $standardFiles) {
            $filePath = Join-Path $this.RepoPath $fileName
            if (Test-Path $filePath) {
                $foundFiles += $fileName
                $confidence += 5
            }
        }
        
        if ($foundFiles.Count -gt 0) {
            $indicators += "Standard repository files: $($foundFiles -join ', ')"
        }
        
        $standardDirs = @('src', 'tests', 'docs', '.github')
        $foundDirs = @()
        
        foreach ($dirName in $standardDirs) {
            $dirPath = Join-Path $this.RepoPath $dirName
            if (Test-Path $dirPath -PathType Container) {
                $foundDirs += $dirName
                $confidence += 3
            }
        }
        
        if ($foundDirs.Count -gt 0) {
            $indicators += "Standard directory structure: $($foundDirs -join ', ')"
        }
        
        $confidence = [Math]::Min($confidence, 100)
        
        return [DetectionResult]::new(
            [PlatformType]::Generic,
            $confidence,
            $indicators,
            $metadata
        )
    }
}

# Main execution
function Main {
    try {
        if ($ClearCache) {
            $cache = [DetectionCache]::new()
            $cache.Clear()
            if ($OutputFormat -eq "Text") {
                Write-Host "✓ Detection cache cleared"
            }
            return 0
        }
        
        $repoPath = Resolve-Path $Path -ErrorAction Stop
        
        if (-not (Test-Path $repoPath)) {
            if ($OutputFormat -eq "JSON") {
                $errorObj = @{
                    error = "Repository path does not exist"
                    path = $repoPath.Path
                }
                Write-Output ($errorObj | ConvertTo-Json)
            } else {
                Write-Error "✗ Error: Repository path does not exist: $repoPath"
            }
            return 2
        }
        
        $detector = [PlatformDetector]::new($repoPath.Path, $UseCache.IsPresent)
        $result = $detector.Detect()
        
        if ($OutputFormat -eq "JSON") {
            $output = $result.ToHashtable()
            $output['repo_path'] = $repoPath.Path
            $output['version'] = $Script:Version
            Write-Output ($output | ConvertTo-Json -Depth 10)
        } else {
            Write-Host "=" * 70
            Write-Host "Platform Auto-Detection v$Script:Version"
            Write-Host "=" * 70
            Write-Host ""
            Write-Host "📁 Repository: $($repoPath.Path)"
            Write-Host "🔍 Platform: $($result.Platform.ToString().ToUpper())"
            Write-Host "📊 Confidence: $($result.Confidence)%"
            Write-Host ""
            
            if ($VerbosePreference -eq 'Continue' -and $result.Indicators.Count -gt 0) {
                Write-Host "Detection Indicators:"
                foreach ($indicator in $result.Indicators) {
                    Write-Host "   • $indicator"
                }
                Write-Host ""
            }
            
            if ($VerbosePreference -eq 'Continue' -and $result.Metadata.Count -gt 0) {
                Write-Host "Metadata:"
                foreach ($key in $result.Metadata.Keys) {
                    Write-Host "   $key`: $($result.Metadata[$key])"
                }
                Write-Host ""
            }
            
            if ($UseCache) {
                Write-Host "💾 Result cached for future runs"
                Write-Host ""
            }
            
            Write-Host "=" * 70
        }
        
        return 0
        
    } catch {
        if ($OutputFormat -eq "JSON") {
            $errorObj = @{
                error = $_.Exception.Message
            }
            Write-Output ($errorObj | ConvertTo-Json)
        } else {
            Write-Error "✗ Error: $($_.Exception.Message)"
        }
        return 2
    }
}

# Execute main function
$exitCode = Main
exit $exitCode
