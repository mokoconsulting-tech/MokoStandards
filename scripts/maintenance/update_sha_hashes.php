#!/usr/bin/env php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts.Maintenance
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /scripts/maintenance/update_sha_hashes.php
 * VERSION: 04.00.00
 * BRIEF: Update SHA-256 hashes in script registry
 */

declare(strict_types=1);

/**
 * Script Registry Hash Updater
 * 
 * Updates SHA-256 hashes for all scripts in the registry
 */
class ScriptRegistryUpdater
{
    private const REGISTRY_PATH = 'scripts/.script-registry.json';
    
    private bool $dryRun = false;
    private bool $verbose = false;
    private array $changes = [];
    
    public function __construct(array $args)
    {
        $this->parseArguments($args);
    }
    
    private function parseArguments(array $args): void
    {
        foreach ($args as $arg) {
            if ($arg === '--dry-run') {
                $this->dryRun = true;
            } elseif ($arg === '--verbose' || $arg === '-v') {
                $this->verbose = true;
            } elseif ($arg === '--help' || $arg === '-h') {
                $this->showHelp();
                exit(0);
            }
        }
    }
    
    private function showHelp(): void
    {
        echo "Usage: php update_sha_hashes.php [OPTIONS]\n\n";
        echo "Options:\n";
        echo "  --dry-run     Check for changes without updating the registry\n";
        echo "  --verbose     Show detailed output\n";
        echo "  --help        Show this help message\n";
        echo "\n";
    }
    
    public function run(): int
    {
        try {
            $this->log("🔐 SHA-256 Hash Update Tool", true);
            $this->log(str_repeat("=", 50), true);
            
            if ($this->dryRun) {
                $this->log("Mode: DRY RUN (no changes will be made)", true);
            }
            
            // Load registry
            $registry = $this->loadRegistry();
            
            // Update hashes
            $updatedRegistry = $this->updateHashes($registry);
            
            // Save if not dry run and there are changes
            if (!$this->dryRun && !empty($this->changes)) {
                $this->saveRegistry($updatedRegistry);
                $this->log("\n✅ Registry updated successfully", true);
            } elseif (empty($this->changes)) {
                $this->log("\nℹ️  No changes needed - all hashes are current", true);
            } else {
                $this->log("\n✅ Dry run complete - changes detected but not applied", true);
            }
            
            return 0;
            
        } catch (Exception $e) {
            fwrite(STDERR, "❌ Error: " . $e->getMessage() . "\n");
            return 1;
        }
    }
    
    private function loadRegistry(): array
    {
        if (!file_exists(self::REGISTRY_PATH)) {
            throw new Exception("Registry file not found: " . self::REGISTRY_PATH);
        }
        
        $content = file_get_contents(self::REGISTRY_PATH);
        $registry = json_decode($content, true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            throw new Exception("Failed to parse registry JSON: " . json_last_error_msg());
        }
        
        $this->log("Registry loaded: " . count($registry['scripts']) . " scripts tracked");
        
        return $registry;
    }
    
    private function updateHashes(array $registry): array
    {
        $this->log("\nChecking scripts for changes...\n");
        
        foreach ($registry['scripts'] as $index => &$script) {
            $path = $script['path'];
            
            if (!file_exists($path)) {
                $this->log("⚠️  Skipping missing file: {$path}");
                continue;
            }
            
            // Calculate current hash
            $currentHash = hash_file('sha256', $path);
            $currentSize = filesize($path);
            
            // Check if changed
            if ($currentHash !== $script['sha256']) {
                $this->changes[] = [
                    'path' => $path,
                    'old_hash' => $script['sha256'],
                    'new_hash' => $currentHash,
                ];
                
                $this->log("🔄 Hash updated: {$path}", true);
                
                if ($this->verbose) {
                    $this->log("   Old: {$script['sha256']}");
                    $this->log("   New: {$currentHash}");
                }
                
                // Update in registry
                $script['sha256'] = $currentHash;
                $script['size_bytes'] = $currentSize;
            } else {
                $this->log("✓ No change: {$path}");
            }
        }
        
        // Update metadata timestamp if there are changes
        if (!empty($this->changes)) {
            $microtime = microtime(true);
            $dt = DateTime::createFromFormat('U.u', sprintf('%.6f', $microtime), new DateTimeZone('UTC'));
            $registry['metadata']['generated_at'] = $dt->format('Y-m-d\TH:i:s.u\Z');
        }
        
        $this->log("\nSummary:");
        $this->log("  Total scripts: " . count($registry['scripts']), true);
        $this->log("  Changed: " . count($this->changes), true);
        
        return $registry;
    }
    
    private function saveRegistry(array $registry): void
    {
        $json = json_encode($registry, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
        
        if ($json === false) {
            throw new Exception("Failed to encode registry JSON: " . json_last_error_msg());
        }
        
        if (file_put_contents(self::REGISTRY_PATH, $json) === false) {
            throw new Exception("Failed to write registry file");
        }
        
        $this->log("Registry saved: " . self::REGISTRY_PATH);
    }
    
    private function log(string $message, bool $force = false): void
    {
        if ($this->verbose || $force) {
            echo $message . "\n";
        }
    }
}

// Run the updater
$updater = new ScriptRegistryUpdater(array_slice($argv, 1));
exit($updater->run());
