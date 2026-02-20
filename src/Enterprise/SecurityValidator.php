<?php

declare(strict_types=1);

/**
 * Security Validator for MokoStandards
 *
 * Provides security scanning and validation:
 * - Credential detection in code/config files
 * - Vulnerability pattern checking
 * - Security best practices validation
 * - Dangerous function detection
 * - File permission validation
 * - Secret management guidance
 *
 * Example usage:
 * ```php
 * $validator = new SecurityValidator();
 * $findings = $validator->scanFile('config.php');
 * 
 * if ($validator->hasCriticalFindings()) {
 *     $validator->printReport();
 *     exit(1);
 * }
 * 
 * // Scan entire directory
 * $validator->scanDirectory('src/', ['.php', '.js']);
 * ```
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * @package MokoStandards\Enterprise
 * @version 04.00.01
 * @author MokoStandards Team
 * @license GPL-3.0-or-later
 */

namespace MokoStandards\Enterprise;

use Exception;
use RecursiveDirectoryIterator;
use RecursiveIteratorIterator;

/**
 * Exception raised when security violations are detected
 */
class SecurityViolation extends Exception
{
}

/**
 * Security validator for detecting vulnerabilities
 */
class SecurityValidator
{
    private const VERSION = '04.00.01';

    /**
     * Common patterns for credentials and secrets
     */
    private const CREDENTIAL_PATTERNS = [
        ['/password\s*=\s*["\']([^"\']+)["\']/i', 'hardcoded password'],
        ['/api[_-]?key\s*=\s*["\']([^"\']+)["\']/i', 'hardcoded API key'],
        ['/secret[_-]?key\s*=\s*["\']([^"\']+)["\']/i', 'hardcoded secret key'],
        ['/token\s*=\s*["\']([^"\']+)["\']/i', 'hardcoded token'],
        ['/aws[_-]?access[_-]?key[_-]?id\s*=\s*["\']([^"\']+)["\']/i', 'AWS access key'],
        ['/private[_-]?key\s*=\s*["\']([^"\']+)["\']/i', 'private key'],
        ['/["\'][A-Za-z0-9\/+]{40,}["\']/i', 'potential secret (base64)'],
    ];

    /**
     * Dangerous function calls
     */
    private const DANGEROUS_FUNCTIONS = [
        'eval',
        'exec',
        'system',
        'passthru',
        'shell_exec',
        'assert',
        'create_function',
        'unserialize',
        'extract',
        '$$',
    ];

    /**
     * File permissions that are too permissive
     */
    private const DANGEROUS_PERMISSIONS = [
        0777, // rwxrwxrwx
        0666, // rw-rw-rw-
    ];

    private array $findings = [];

    /**
     * Scan a file for security issues
     *
     * @param string $filePath Path to file to scan
     * @param bool $checkCredentials Check for hardcoded credentials
     * @param bool $checkDangerousFunctions Check for dangerous function usage
     * @return array<int, array<string, mixed>> List of security findings
     */
    public function scanFile(
        string $filePath,
        bool $checkCredentials = true,
        bool $checkDangerousFunctions = true
    ): array {
        $findings = [];

        if (!file_exists($filePath)) {
            return $findings;
        }

        try {
            $content = file_get_contents($filePath);

            if ($checkCredentials) {
                $credFindings = $this->checkCredentialsInText($content, $filePath);
                $findings = array_merge($findings, $credFindings);
            }

            if ($checkDangerousFunctions) {
                $funcFindings = $this->checkDangerousFunctions($content, $filePath);
                $findings = array_merge($findings, $funcFindings);
            }
        } catch (Exception $e) {
            $findings[] = [
                'severity' => 'warning',
                'type' => 'scan_error',
                'file' => $filePath,
                'message' => 'Failed to scan file: ' . $e->getMessage()
            ];
        }

        $this->findings = array_merge($this->findings, $findings);
        return $findings;
    }

    /**
     * Check for hardcoded credentials in text
     *
     * @param string $text Text to scan
     * @param string $source Source file/location
     * @return array<int, array<string, mixed>> List of findings
     */
    private function checkCredentialsInText(string $text, string $source): array
    {
        $findings = [];

        foreach (self::CREDENTIAL_PATTERNS as [$pattern, $description]) {
            if (preg_match_all($pattern, $text, $matches, PREG_OFFSET_CAPTURE)) {
                foreach ($matches[0] as $match) {
                    $matchedValue = isset($matches[1]) && !empty($matches[1]) ? $matches[1][0][0] : $match[0];
                    
                    if ($this->isPlaceholder($matchedValue)) {
                        continue;
                    }

                    $line = substr_count(substr($text, 0, $match[1]), "\n") + 1;
                    $snippet = substr($match[0], 0, 50);

                    $findings[] = [
                        'severity' => 'high',
                        'type' => 'credential',
                        'file' => $source,
                        'description' => $description,
                        'line' => $line,
                        'snippet' => $snippet
                    ];
                }
            }
        }

        return $findings;
    }

    /**
     * Check for dangerous function usage
     *
     * @param string $text Text to scan
     * @param string $source Source file/location
     * @return array<int, array<string, mixed>> List of findings
     */
    private function checkDangerousFunctions(string $text, string $source): array
    {
        $findings = [];

        foreach (self::DANGEROUS_FUNCTIONS as $funcName) {
            $pattern = '/\b' . preg_quote($funcName, '/') . '\s*\(/';
            if (preg_match_all($pattern, $text, $matches, PREG_OFFSET_CAPTURE)) {
                foreach ($matches[0] as $match) {
                    $line = substr_count(substr($text, 0, $match[1]), "\n") + 1;

                    $findings[] = [
                        'severity' => 'medium',
                        'type' => 'dangerous_function',
                        'file' => $source,
                        'function' => $funcName,
                        'line' => $line,
                        'message' => "Potentially dangerous function: {$funcName}"
                    ];
                }
            }
        }

        return $findings;
    }

    /**
     * Check if a value looks like a placeholder
     *
     * @param string $value Value to check
     * @return bool True if looks like placeholder
     */
    private function isPlaceholder(string $value): bool
    {
        $placeholders = [
            'your_', 'example', 'placeholder', 'xxx', 'test',
            'dummy', 'sample', 'replace', 'changeme', 'todo'
        ];
        
        $valueLower = strtolower($value);
        foreach ($placeholders as $placeholder) {
            if (strpos($valueLower, $placeholder) !== false) {
                return true;
            }
        }
        
        return false;
    }

    /**
     * Check file permissions for security issues
     *
     * @param string $filePath Path to file
     * @return array<string, mixed>|null Finding if permissions are too permissive, null otherwise
     */
    public function checkFilePermissions(string $filePath): ?array
    {
        if (!file_exists($filePath)) {
            return null;
        }

        $perms = fileperms($filePath) & 0777;

        if (in_array($perms, self::DANGEROUS_PERMISSIONS, true)) {
            $finding = [
                'severity' => 'medium',
                'type' => 'file_permissions',
                'file' => $filePath,
                'permissions' => decoct($perms),
                'message' => sprintf('File has overly permissive permissions: %o', $perms)
            ];
            $this->findings[] = $finding;
            return $finding;
        }

        return null;
    }

    /**
     * Validate that sensitive data comes from environment variables
     *
     * @param string $varName Environment variable name
     * @return bool True if variable exists
     */
    public function validateEnvironmentVar(string $varName): bool
    {
        return getenv($varName) !== false;
    }

    /**
     * Get all security findings
     *
     * @param string|null $severity Filter by severity (high, medium, low, warning)
     * @return array<int, array<string, mixed>> List of findings
     */
    public function getFindings(?string $severity = null): array
    {
        if ($severity !== null) {
            return array_filter($this->findings, function ($finding) use ($severity) {
                return ($finding['severity'] ?? '') === $severity;
            });
        }
        return $this->findings;
    }

    /**
     * Check if there are any critical/high severity findings
     *
     * @return bool True if critical findings exist
     */
    public function hasCriticalFindings(): bool
    {
        foreach ($this->findings as $finding) {
            if (in_array($finding['severity'] ?? '', ['critical', 'high'], true)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Print a security report
     */
    public function printReport(): void
    {
        echo "\n" . str_repeat('=', 60) . "\n";
        echo "Security Validation Report\n";
        echo str_repeat('=', 60) . "\n";

        if (empty($this->findings)) {
            echo "\n✓ No security issues found!\n";
            echo str_repeat('=', 60) . "\n\n";
            return;
        }

        // Group by severity
        $bySeverity = [];
        foreach ($this->findings as $finding) {
            $sev = $finding['severity'] ?? 'unknown';
            if (!isset($bySeverity[$sev])) {
                $bySeverity[$sev] = [];
            }
            $bySeverity[$sev][] = $finding;
        }

        // Print findings by severity
        foreach (['critical', 'high', 'medium', 'low', 'warning'] as $sev) {
            if (isset($bySeverity[$sev])) {
                echo sprintf("\n%s Severity (%d findings):\n", strtoupper($sev), count($bySeverity[$sev]));
                foreach ($bySeverity[$sev] as $finding) {
                    $message = $finding['message'] ?? $finding['description'] ?? 'No description';
                    echo "  - {$finding['type']}: {$message}\n";
                    if (isset($finding['file'])) {
                        echo "    File: {$finding['file']}\n";
                    }
                    if (isset($finding['line'])) {
                        echo "    Line: {$finding['line']}\n";
                    }
                }
            }
        }

        $total = count($this->findings);
        $critical = count($bySeverity['critical'] ?? []) + count($bySeverity['high'] ?? []);

        echo "\nTotal findings: {$total}\n";
        echo "Critical/High: {$critical}\n";
        echo str_repeat('=', 60) . "\n\n";
    }

    /**
     * Clear all findings
     */
    public function clearFindings(): void
    {
        $this->findings = [];
    }

    /**
     * Scan a directory for security issues
     *
     * @param string $directory Directory to scan
     * @param array<int, string>|null $extensions File extensions to scan
     */
    public function scanDirectory(string $directory, ?array $extensions = null): void
    {
        if ($extensions === null) {
            $extensions = ['.php', '.sh', '.yaml', '.yml', '.json', '.conf', '.cfg'];
        }

        if (!is_dir($directory)) {
            return;
        }

        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($directory)
        );

        foreach ($iterator as $file) {
            if ($file->isFile()) {
                $filePath = $file->getPathname();
                foreach ($extensions as $ext) {
                    if (substr($filePath, -strlen($ext)) === $ext) {
                        $this->scanFile($filePath);
                        break;
                    }
                }
            }
        }
    }

    public function getVersion(): string
    {
        return self::VERSION;
    }
}
