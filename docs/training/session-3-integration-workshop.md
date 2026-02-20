<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Training
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/training/session-2-integration-workshop.md
VERSION: 04.00.01
BRIEF: Session 2 - Practical Integration Workshop training materials
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Session 2: Practical Integration Workshop

**Duration**: 3 hours  
**Format**: Hands-on Workshop  
**Prerequisite**: Complete Session 1

---

## Session Objectives

By the end of this session, you will:
- ✅ Migrate an existing script to use enterprise libraries
- ✅ Implement common integration patterns
- ✅ Debug and troubleshoot integration issues
- ✅ Follow best practices for library usage
- ✅ Build a production-ready automation script from scratch

---

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 0:00-0:20 | Integration Patterns Overview | Presentation |
| 0:20-1:20 | Hands-on: Migrate Sample Script | Workshop |
| 1:20-2:00 | Common Integration Patterns | Demo + Practice |
| 2:00-2:40 | Troubleshooting Workshop | Interactive |
| 2:40-3:00 | Q&A and Next Steps | Discussion |

---

## Part 1: Integration Patterns Overview (20 minutes)

### Common Integration Patterns

#### Pattern 1: The Essential Stack
**Use Case**: Every production script  
**Libraries**: CLI Framework + Enterprise Audit + Metrics

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\CliFramework;
use MokoStandards\Enterprise\AuditLogger;
use MokoStandards\Enterprise\MetricsCollector;

class MyScript extends CliFramework
{
    private AuditLogger $audit;
    private MetricsCollector $metrics;
    
    protected function initialize(): void
    {
        $this->audit = new AuditLogger(service: self::class);
        $this->metrics = new MetricsCollector(service: self::class);
    }
    
    protected function run(): int
    {
        try {
            $txn = $this->audit->transaction('main_operation');
            try {
                $timer = $this->metrics->timeOperation('execution');
                try {
                    // Your logic here
                    $txn->logEvent('complete', ['status' => 'success']);
                } finally {
                    $timer->stop();
                }
            } finally {
                $txn->commit();
            }
        } finally {
            // Transaction cleanup
        }
        return 0;
    }
}
```

#### Pattern 2: The API Integration Stack
**Use Case**: Scripts making API calls  
**Libraries**: Essential Stack + API Client + Error Recovery

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\CliFramework;
use MokoStandards\Enterprise\AuditLogger;
use MokoStandards\Enterprise\GitHubClient;
use MokoStandards\Enterprise\RetryWithBackoff;
use MokoStandards\Enterprise\MetricsCollector;

class APIScript extends CliFramework
{
    private AuditLogger $audit;
    private MetricsCollector $metrics;
    private GitHubClient $api;
    
    protected function initialize(): void
    {
        $this->audit = new AuditLogger(service: self::class);
        $this->metrics = new MetricsCollector(service: self::class);
        $this->api = new GitHubClient(token: $this->getToken());
    }
    
    #[RetryWithBackoff(maxRetries: 3)]
    protected function fetchData(): array
    {
        $this->metrics->increment('api_calls_total');
        return $this->api->listRepos(org: 'mokoconsulting-tech');
    }
}
```

#### Pattern 3: The Batch Processing Stack
**Use Case**: Long-running batch operations  
**Libraries**: API Stack + Checkpointing + Transaction Manager

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\Checkpoint;
use MokoStandards\Enterprise\Transaction;

class BatchProcessor extends CliFramework
{
    protected function processBatch(array $items): void
    {
        $checkpoint = new Checkpoint('batch_process');
        
        foreach ($items as $item) {
            if ($checkpoint->isCompleted($item)) {
                continue;
            }
            
            try {
                $txn = new Transaction();
                try {
                    $this->processItem($item, $txn);
                    $txn->commit();
                    $checkpoint->markCompleted($item);
                } finally {
                    // Transaction cleanup
                }
            } catch (\Exception $e) {
                $checkpoint->markFailed($item, $e->getMessage());
            }
        }
    }
}
```

#### Pattern 4: The Security-First Stack
**Use Case**: Scripts handling sensitive data  
**Libraries**: Essential Stack + Security Validator + Config Manager

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\SecurityValidator;
use MokoStandards\Enterprise\Config;

class SecureScript extends CliFramework
{
    private SecurityValidator $security;
    private Config $config;
    
    protected function initialize(): void
    {
        parent::initialize();
        $this->security = new SecurityValidator();
        $this->config = Config::load(env: $this->args->env);
    }
    
    protected function validateInput(string $userInput): string
    {
        // Security validation
        if ($this->security->detectCredentials($userInput)) {
            throw new \ValueError("Input contains credentials!");
        }
        return $this->security->validateInput($userInput);
    }
}
```

### Integration Best Practices

✅ **DO**:
- Initialize libraries in `initialize()` method
- Use context managers for transactions and metrics
- Handle errors gracefully with try/except
- Log all major operations to audit trail
- Track metrics for observability
- Use checkpointing for long operations

❌ **DON'T**:
- Initialize libraries in global scope
- Ignore error recovery for flaky operations
- Skip audit logging for critical operations
- Mix business logic with library initialization
- Forget to export metrics
- Hardcode configuration values

---

## Part 2: Hands-On Migration (60 minutes)

### Exercise 2.1: Migrate Legacy Script

**Scenario**: We have a legacy script that needs enterprise library integration.

#### Original Script (Legacy)

```php
<?php
declare(strict_types=1);

/**
 * Legacy script: manage_repositories.php
 * Fetches repositories and updates their settings
 */

function main(): void
{
    $options = getopt('', ['org:', 'dry-run']);
    
    if (!isset($options['org'])) {
        fwrite(STDERR, "Error: --org is required\n");
        exit(1);
    }
    
    $org = $options['org'];
    $dryRun = isset($options['dry-run']);
    
    // Get token from environment
    $token = getenv('GITHUB_TOKEN');
    if (!$token) {
        fwrite(STDERR, "Error: GITHUB_TOKEN not set\n");
        exit(1);
    }
    
    // Fetch repositories
    echo "Fetching repositories for {$org}...\n";
    $headers = ["Authorization: token {$token}"];
    
    $url = "https://api.github.com/orgs/{$org}/repos";
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($statusCode !== 200) {
        fwrite(STDERR, "Error: API returned {$statusCode}\n");
        exit(1);
    }
    
    $repos = json_decode($response, true);
    $repoCount = count($repos);
    echo "Found {$repoCount} repositories\n";
    
    // Update each repository
    $updatedCount = 0;
    $failedCount = 0;
    
    foreach ($repos as $repo) {
        $repoName = $repo['name'];
        echo "Processing {$repoName}...\n";
        
        if ($dryRun) {
            echo "  [DRY RUN] Would update {$repoName}\n";
            $updatedCount++;
            continue;
        }
        
        // Update repository settings
        $updateUrl = "https://api.github.com/repos/{$org}/{$repoName}";
        $data = json_encode([
            'has_issues' => true,
            'has_wiki' => false,
            'has_projects' => false
        ]);
        
        $ch = curl_init($updateUrl);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array_merge($headers, ['Content-Type: application/json']));
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PATCH');
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_exec($ch);
        $statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($statusCode === 200) {
            echo "  ✓ Updated {$repoName}\n";
            $updatedCount++;
        } else {
            echo "  ✗ Failed to update {$repoName}: {$statusCode}\n";
            $failedCount++;
        }
        
        // Rate limiting (simple sleep)
        sleep(1);
    }
    
    // Print summary
    echo "\nSummary:\n";
    echo "  Total repositories: {$repoCount}\n";
    echo "  Updated: {$updatedCount}\n";
    echo "  Failed: {$failedCount}\n";
}

main();
```

#### Your Task: Migrate to Enterprise Libraries

**Requirements**:
1. ✅ Use CLI Framework for argument parsing
2. ✅ Add Enterprise Audit logging for all operations
3. ✅ Use API Client for rate-limited API calls
4. ✅ Add error recovery with checkpointing
5. ✅ Track metrics (repos_processed, update_success, update_failure)
6. ✅ Use Security Validator to validate inputs
7. ✅ Add proper error handling

#### Step-by-Step Migration Guide

**Step 1: Set up the CLI Framework structure**

```php
<?php
declare(strict_types=1);

/**
 * Enterprise script: manage_repositories.php
 * Manages repository settings with enterprise libraries
 */

use MokoStandards\Enterprise\CliFramework;

class RepositoryManager extends CliFramework
{
    /**
     * Configure command-line arguments
     */
    protected function setupArguments(): array
    {
        return [
            'org' => [
                'required' => true,
                'help' => 'GitHub organization name'
            ],
            // TODO: Add any additional arguments
        ];
    }
    
    /**
     * Initialize enterprise libraries
     */
    protected function initialize(): void
    {
        // TODO: Initialize libraries here
    }
    
    /**
     * Main execution logic
     */
    protected function run(): int
    {
        $org = $this->args->org;
        
        // TODO: Implement main logic
        
        return 0; // Success
    }
}

$app = new RepositoryManager();
exit($app->execute());
```

**Step 2: Add Enterprise Audit**

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\AuditLogger;

protected function initialize(): void
{
    parent::initialize();
    $this->audit = new AuditLogger(
        service: 'repository_manager',
        retentionDays: 90
    );
}

protected function run(): int
{
    $org = $this->args->org;
    
    try {
        $txn = $this->audit->transaction('manage_repositories');
        try {
            $txn->logEvent('start', [
                'organization' => $org,
                'dry_run' => $this->args->dryRun
            ]);
            
            // TODO: Add main logic
            
            $txn->logEvent('complete', [
                'organization' => $org,
                'status' => 'success'
            ]);
        } finally {
            $txn->commit();
        }
    } finally {
        // Transaction cleanup
    }
    
    return 0;
}
```

**Step 3: Add API Client**

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\GitHubClient;
use MokoStandards\Enterprise\RateLimitConfig;

protected function initialize(): void
{
    parent::initialize();
    $this->audit = new AuditLogger(service: 'repository_manager');
    
    // Initialize API client with rate limiting
    $rateConfig = new RateLimitConfig(
        maxRequestsPerHour: 5000,
        enableCaching: true,
        cacheTtl: 300
    );
    
    $this->api = new GitHubClient(
        token: getenv('GITHUB_TOKEN') ?: '',
        rateLimitConfig: $rateConfig
    );
}

protected function fetchRepositories(string $org): array
{
    try {
        $repos = $this->api->listRepos(org: $org);
        $count = count($repos);
        $this->logger->info("Fetched {$count} repositories");
        return $repos;
    } catch (\Exception $e) {
        $this->logger->error("Failed to fetch repositories: {$e->getMessage()}");
        throw $e;
    }
}
```

**Step 4: Add Metrics Collection**

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\MetricsCollector;

protected function initialize(): void
{
    parent::initialize();
    $this->audit = new AuditLogger(service: 'repository_manager');
    $this->metrics = new MetricsCollector(service: 'repository_manager');
    $this->api = new GitHubClient(token: getenv('GITHUB_TOKEN') ?: '');
}

protected function updateRepository(string $org, string $repoName, object $txn): bool
{
    try {
        $timer = $this->metrics->timeOperation('repository_update');
        try {
            // Update repository settings
            $this->api->updateRepo(
                org: $org,
                repo: $repoName,
                data: [
                    'has_issues' => true,
                    'has_wiki' => false,
                    'has_projects' => false
                ]
            );
        } finally {
            $timer->stop();
        }
        
        // Track success
        $this->metrics->increment('repos_updated_success', 
                                  labels: ['org' => $org]);
        $txn->logEvent('repository_updated', [
            'repo' => $repoName,
            'status' => 'success'
        ]);
        
        return true;
        
    } catch (\Exception $e) {
        // Track failure
        $this->metrics->increment('repos_updated_failure',
                                  labels: ['org' => $org]);
        $txn->logEvent('repository_failed', [
            'repo' => $repoName,
            'error' => $e->getMessage()
        ]);
        
        return false;
    }
}
```

**Step 5: Add Error Recovery with Checkpointing**

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\Checkpoint;
use MokoStandards\Enterprise\RetryWithBackoff;

protected function initialize(): void
{
    parent::initialize();
    $this->audit = new AuditLogger(service: 'repository_manager');
    $this->metrics = new MetricsCollector(service: 'repository_manager');
    $this->api = new GitHubClient(token: getenv('GITHUB_TOKEN') ?: '');
    
    // Initialize checkpoint
    $this->checkpoint = new Checkpoint(
        name: 'repository_updates',
        checkpointDir: '/tmp/checkpoints'
    );
}

#[RetryWithBackoff(maxRetries: 3, baseDelay: 1.0)]
protected function updateRepository(string $org, string $repoName, object $txn): bool
{
    // Check if already processed
    if ($this->checkpoint->isCompleted($repoName)) {
        $this->logger->info("Skipping {$repoName} (already processed)");
        return true;
    }
    
    try {
        $timer = $this->metrics->timeOperation('repository_update');
        try {
            $this->api->updateRepo(
                org: $org,
                repo: $repoName,
                data: [
                    'has_issues' => true,
                    'has_wiki' => false,
                    'has_projects' => false
                ]
            );
        } finally {
            $timer->stop();
        }
        
        // Mark as completed
        $this->checkpoint->markCompleted($repoName, ['status' => 'success']);
        $this->metrics->increment('repos_updated_success', labels: ['org' => $org]);
        $txn->logEvent('repository_updated', ['repo' => $repoName]);
        
        return true;
        
    } catch (\Exception $e) {
        // Mark as failed
        $this->checkpoint->markFailed($repoName, $e->getMessage());
        $this->metrics->increment('repos_updated_failure', labels: ['org' => $org]);
        $txn->logEvent('repository_failed', ['repo' => $repoName, 'error' => $e->getMessage()]);
        
        throw $e; // Re-raise for retry logic
    }
}
```

**Step 6: Add Security Validation**

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\SecurityValidator;

protected function initialize(): void
{
    parent::initialize();
    $this->audit = new AuditLogger(service: 'repository_manager');
    $this->metrics = new MetricsCollector(service: 'repository_manager');
    $this->api = new GitHubClient(token: getenv('GITHUB_TOKEN') ?: '');
    $this->checkpoint = new Checkpoint(name: 'repository_updates');
    $this->security = new SecurityValidator();
}

protected function validateInputs(): void
{
    $org = $this->args->org;
    
    // Validate organization name
    if (!$this->security->validateInput($org, inputType: 'identifier')) {
        throw new \ValueError("Invalid organization name: {$org}");
    }
    
    // Check for dangerous patterns
    if ($this->security->detectDangerousPatterns($org)) {
        throw new \ValueError("Organization name contains dangerous patterns");
    }
    
    $this->logger->info("Input validation passed for org: {$org}");
}
```

**Step 7: Complete Integration**

```php
<?php
declare(strict_types=1);

/**
 * Enterprise script: manage_repositories.php
 * Manages repository settings with enterprise libraries
 *
 * Copyright (C) 2026 Moko Consulting
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

use MokoStandards\Enterprise\CliFramework;
use MokoStandards\Enterprise\AuditLogger;
use MokoStandards\Enterprise\GitHubClient;
use MokoStandards\Enterprise\RateLimitConfig;
use MokoStandards\Enterprise\MetricsCollector;
use MokoStandards\Enterprise\Checkpoint;
use MokoStandards\Enterprise\RetryWithBackoff;
use MokoStandards\Enterprise\SecurityValidator;

class RepositoryManager extends CliFramework
{
    private AuditLogger $audit;
    private MetricsCollector $metrics;
    private SecurityValidator $security;
    private GitHubClient $api;
    private Checkpoint $checkpoint;
    
    protected function setupArguments(): array
    {
        return [
            'org' => [
                'required' => true,
                'help' => 'GitHub organization'
            ]
        ];
    }
    
    protected function initialize(): void
    {
        parent::initialize();
        
        // Initialize all enterprise libraries
        $this->audit = new AuditLogger(service: 'repository_manager', retentionDays: 90);
        $this->metrics = new MetricsCollector(service: 'repository_manager');
        $this->security = new SecurityValidator();
        
        // API client with rate limiting
        $rateConfig = new RateLimitConfig(
            maxRequestsPerHour: 5000,
            enableCaching: true
        );
        $this->api = new GitHubClient(
            token: getenv('GITHUB_TOKEN') ?: '',
            rateLimitConfig: $rateConfig
        );
        
        // Checkpoint for recovery
        $this->checkpoint = new Checkpoint(
            name: 'repository_updates',
            checkpointDir: '/tmp/checkpoints'
        );
    }
    
    protected function validateInputs(): void
    {
        $org = $this->args->org;
        if (!$this->security->validateInput($org, inputType: 'identifier')) {
            throw new \ValueError("Invalid organization name: {$org}");
        }
    }
    
    #[RetryWithBackoff(maxRetries: 3, baseDelay: 1.0)]
    protected function updateRepository(string $org, string $repoName, object $txn): bool
    {
        if ($this->checkpoint->isCompleted($repoName)) {
            $this->logger->debug("Skipping {$repoName} (completed)");
            return true;
        }
        
        try {
            if ($this->args->dryRun) {
                $this->logger->info("[DRY RUN] Would update {$repoName}");
            } else {
                $timer = $this->metrics->timeOperation('repository_update');
                try {
                    $this->api->updateRepo(
                        org: $org,
                        repo: $repoName,
                        data: [
                            'has_issues' => true,
                            'has_wiki' => false,
                            'has_projects' => false
                        ]
                    );
                } finally {
                    $timer->stop();
                }
            }
            
            $this->checkpoint->markCompleted($repoName, ['status' => 'success']);
            $this->metrics->increment('repos_updated_success', labels: ['org' => $org]);
            $txn->logEvent('repository_updated', ['repo' => $repoName]);
            
            return true;
            
        } catch (\Exception $e) {
            $this->checkpoint->markFailed($repoName, $e->getMessage());
            $this->metrics->increment('repos_updated_failure', labels: ['org' => $org]);
            $txn->logEvent('repository_failed', ['repo' => $repoName, 'error' => $e->getMessage()]);
            throw $e;
        }
    }
    
    protected function run(): int
    {
        $org = $this->args->org;
        
        // Validate inputs
        $this->validateInputs();
        
        // Main transaction
        try {
            $txn = $this->audit->transaction('manage_repositories');
            try {
                $txn->logEvent('start', ['organization' => $org, 'dry_run' => $this->args->dryRun]);
                
                // Fetch repositories
                $repos = $this->api->listRepos(org: $org);
                $repoCount = count($repos);
                $this->logger->info("Found {$repoCount} repositories");
                $this->metrics->setGauge('repositories_total', $repoCount);
                
                // Process each repository
                $successCount = 0;
                $failureCount = 0;
                
                foreach ($repos as $repo) {
                    $repoName = $repo['name'];
                    $this->logger->info("Processing {$repoName}...");
                    
                    try {
                        if ($this->updateRepository($org, $repoName, $txn)) {
                            $successCount++;
                        }
                    } catch (\Exception $e) {
                        $this->logger->error("Failed to update {$repoName}: {$e->getMessage()}");
                        $failureCount++;
                    }
                }
                
                // Log final results
                $txn->logEvent('complete', [
                    'organization' => $org,
                    'total' => $repoCount,
                    'success' => $successCount,
                    'failure' => $failureCount
                ]);
                
                // Print summary
                $this->logger->info("\nSummary:");
                $this->logger->info("  Total: {$repoCount}");
                $this->logger->info("  Success: {$successCount}");
                $this->logger->info("  Failed: {$failureCount}");
                
                // Export metrics
                if ($this->args->verbose) {
                    echo "\nMetrics:\n";
                    echo $this->metrics->exportPrometheus();
                }
                
                return $failureCount === 0 ? 0 : 1;
            } finally {
                $txn->commit();
            }
        } finally {
            // Transaction cleanup
        }
    }
}

$app = new RepositoryManager();
exit($app->execute());
```

#### Your Turn: Complete the Migration

**Task**: Take the legacy script and migrate it following the steps above.

**Verification Checklist**:
- [ ] Script uses CLIApp base class
- [ ] Audit logging tracks all operations
- [ ] API calls use GitHubClient with rate limiting
- [ ] Checkpointing enables recovery
- [ ] Metrics track success/failure
- [ ] Security validation on inputs
- [ ] Proper error handling throughout
- [ ] Dry-run mode works correctly

---

## Part 3: Common Integration Patterns (40 minutes)

### Pattern Exercise 2.2: Configuration-Driven Script

Build a script that loads configuration from YAML files.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\CliFramework;
use MokoStandards\Enterprise\Config;

class ConfigDrivenScript extends CliFramework
{
    private Config $config;
    
    protected function setupArguments(): array
    {
        return [
            'env' => [
                'default' => 'development',
                'choices' => ['development', 'staging', 'production'],
                'help' => 'Environment'
            ],
            'config' => [
                'help' => 'Config file override'
            ]
        ];
    }
    
    protected function initialize(): void
    {
        parent::initialize();
        
        // Load environment-specific config
        $this->config = Config::load(
            env: $this->args->env,
            configFile: $this->args->config
        );
        
        // Validate required configuration
        $this->config->require([
            'github.organization',
            'github.token',
            'settings.max_retries'
        ]);
    }
    
    protected function run(): int
    {
        $org = $this->config->get('github.organization');
        $maxRetries = $this->config->getInt('settings.max_retries', default: 3);
        $enableCache = $this->config->getBool('cache.enabled', default: true);
        
        $this->logger->info("Organization: {$org}");
        $this->logger->info("Max retries: {$maxRetries}");
        $this->logger->info("Cache enabled: " . ($enableCache ? 'true' : 'false'));
        
        // Your logic here
        
        return 0;
    }
}
```

**Configuration File** (`config/development.yaml`):
```yaml
github:
  organization: mokoconsulting-tech
  token: ${GITHUB_TOKEN}

settings:
  max_retries: 3
  timeout: 30
  
cache:
  enabled: true
  ttl: 300

logging:
  level: DEBUG
```

**Exercise**: Create a config-driven script that:
1. Loads environment-specific configuration
2. Validates required keys exist
3. Uses config values throughout the script
4. Supports runtime overrides via CLI args

---

### Pattern Exercise 2.3: Transaction-Based Updates

Implement atomic operations that rollback on failure.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\TransactionManager;

class AtomicUpdater extends CliFramework
{
    private TransactionManager $txnManager;
    private array $stateCache = [];
    
    protected function initialize(): void
    {
        parent::initialize();
        $this->txnManager = new TransactionManager();
    }
    
    protected function updateRepositoryAtomically(string $org, string $repo): bool
    {
        try {
            $txn = $this->txnManager->beginTransaction("update_{$repo}");
            try {
                // Operation 1: Update settings
                $txn->addOperation(
                    name: 'update_settings',
                    forward: fn() => $this->updateSettings($org, $repo),
                    rollback: fn() => $this->restoreSettings($org, $repo)
                );
                
                // Operation 2: Update branch protection
                $txn->addOperation(
                    name: 'update_protection',
                    forward: fn() => $this->updateProtection($org, $repo, 'main'),
                    rollback: fn() => $this->restoreProtection($org, $repo, 'main')
                );
                
                // Operation 3: Update webhooks
                $txn->addOperation(
                    name: 'update_webhooks',
                    forward: fn() => $this->updateWebhooks($org, $repo),
                    rollback: fn() => $this->restoreWebhooks($org, $repo)
                );
                
                // Commit all operations atomically
                $txn->commit();
                
                $this->logger->info("Successfully updated {$repo}");
                return true;
                
            } catch (\Exception $e) {
                $txn->rollback();
                throw $e;
            }
        } catch (\Exception $e) {
            $this->logger->error("Failed to update {$repo}: {$e->getMessage()}");
            $this->logger->info("All changes rolled back");
            return false;
        }
    }
    
    protected function updateSettings(string $org, string $repo): void
    {
        // Save current state for rollback
        $current = $this->api->getRepo($org, $repo);
        $this->stateCache["{$repo}_settings"] = $current;
        
        // Apply new settings
        $this->api->updateRepo($org, $repo, [
            'has_issues' => true,
            'has_wiki' => false
        ]);
    }
    
    protected function restoreSettings(string $org, string $repo): void
    {
        $previous = $this->stateCache["{$repo}_settings"] ?? null;
        if ($previous) {
            $this->api->updateRepo($org, $repo, $previous);
        }
    }
}
```

**Exercise**: Implement a transaction-based script that:
1. Updates multiple settings atomically
2. Provides rollback functions for each operation
3. Logs transaction history
4. Handles nested transactions

---

### Pattern Exercise 2.4: Batch Processing with Checkpoints

Process large datasets with recovery capabilities.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\Checkpoint;
use MokoStandards\Enterprise\MetricsCollector;

class BatchProcessor extends CliFramework
{
    private Checkpoint $checkpoint;
    private MetricsCollector $metrics;
    
    protected function initialize(): void
    {
        parent::initialize();
        $this->checkpoint = new Checkpoint(name: 'batch_process');
        $this->metrics = new MetricsCollector(service: 'batch_processor');
    }
    
    protected function processBatch(array $items): bool
    {
        $total = count($items);
        $processed = 0;
        $failed = 0;
        
        $this->logger->info("Processing {$total} items");
        
        foreach ($items as $idx => $item) {
            $itemId = $item['id'];
            $current = $idx + 1;
            
            // Skip if already processed
            if ($this->checkpoint->isCompleted($itemId)) {
                $this->logger->debug("Skipping {$itemId} (completed)");
                $processed++;
                continue;
            }
            
            // Skip if previously failed and not retrying
            if ($this->checkpoint->isFailed($itemId) && !$this->args->retryFailed) {
                $this->logger->debug("Skipping {$itemId} (failed)");
                $failed++;
                continue;
            }
            
            // Process item
            try {
                $this->logger->info("[{$current}/{$total}] Processing {$itemId}...");
                $result = $this->processItem($item);
                
                // Mark as completed
                $this->checkpoint->markCompleted($itemId, $result);
                $this->metrics->increment('items_processed_success');
                $processed++;
                
            } catch (\Exception $e) {
                $this->logger->error("Failed to process {$itemId}: {$e->getMessage()}");
                $this->checkpoint->markFailed($itemId, $e->getMessage());
                $this->metrics->increment('items_processed_failure');
                $failed++;
            }
        }
        
        // Print summary
        $this->logger->info("\nBatch Summary:");
        $this->logger->info("  Total: {$total}");
        $this->logger->info("  Processed: {$processed}");
        $this->logger->info("  Failed: {$failed}");
        
        // Check for failed items
        if ($this->checkpoint->hasFailures()) {
            $failedItems = $this->checkpoint->getFailures();
            $failedCount = count($failedItems);
            $this->logger->warning("\n{$failedCount} items failed:");
            foreach ($failedItems as $itemId => $error) {
                $this->logger->warning("  - {$itemId}: {$error}");
            }
            $this->logger->info("\nRun with --retry-failed to retry failed items");
        }
        
        return $failed === 0;
    }
}
```

**Exercise**: Create a batch processing script that:
1. Processes 100+ items with checkpointing
2. Recovers from failures gracefully
3. Provides retry capability for failed items
4. Tracks progress metrics
5. Generates a summary report

---

## Part 4: Troubleshooting Workshop (40 minutes)

### Common Issues and Solutions

#### Issue 1: Import Errors

**Problem**:
```php
<?php
// Fatal error: Class 'MokoStandards\Enterprise\AuditLogger' not found
```

**Solution**:
```php
<?php
declare(strict_types=1);

// Option 1: Ensure autoloader is configured properly
require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\AuditLogger;

// Option 2: Use relative namespace imports (if in scripts directory)
use Enterprise\AuditLogger;

// Option 3: Install via Composer
// composer install
```

---

#### Issue 2: Rate Limiting Not Working

**Problem**: Script still hits rate limits despite using API Client.

**Diagnosis**:
```php
<?php
declare(strict_types=1);

// Check rate limit status
$status = $client->getRateLimitStatus();
echo sprintf("Rate limit: %d/%d\n", $status['remaining'], $status['limit']);
echo sprintf("Reset time: %s\n", $status['reset_time']);
```

**Solution**:
```php
<?php
declare(strict_types=1);

// Ensure proper configuration
$rateConfig = new RateLimitConfig(
    maxRequestsPerHour: 5000,  // Match GitHub limits
    burstSize: 100,  // Allow bursts
    enableCaching: true,  // Cache responses
    cacheTtl: 300  // 5-minute cache
);

$client = new GitHubClient(
    token: $token,
    rateLimitConfig: $rateConfig
);

// Enable request logging
use Monolog\Logger;
use Monolog\Handler\StreamHandler;
$logger = new Logger('api_client');
$logger->pushHandler(new StreamHandler('php://stderr', Logger::DEBUG));
```

---

#### Issue 3: Checkpoints Not Persisting

**Problem**: Checkpoints reset after script restart.

**Solution**:
```php
<?php
declare(strict_types=1);

// Use persistent checkpoint directory
$checkpoint = new Checkpoint(
    name: 'my_operation',
    checkpointDir: '/var/lib/myapp/checkpoints'  // Persistent location
);

// Ensure directory exists and has correct permissions
if (!is_dir('/var/lib/myapp/checkpoints')) {
    mkdir('/var/lib/myapp/checkpoints', 0755, true);
}
```

---

#### Issue 4: Metrics Not Exporting

**Problem**: Prometheus export returns empty results.

**Diagnosis**:
```php
<?php
declare(strict_types=1);

// Check if metrics are being recorded
echo sprintf("Counter value: %d\n", $metrics->getCounter('my_counter'));
echo sprintf("All metrics: %s\n", json_encode($metrics->getAllMetrics()));
```

**Solution**:
```php
<?php
declare(strict_types=1);

// Ensure metrics are incremented with correct labels
$metrics->increment('operations_total', labels: ['type' => 'update']);

// Export with proper formatting
$prometheusText = $metrics->exportPrometheus();
echo $prometheusText;

// Write to file for Prometheus scraping
file_put_contents('/var/lib/prometheus/metrics.prom', $prometheusText);
```

---

#### Issue 5: Audit Logs Missing

**Problem**: Audit transactions not appearing in logs.

**Solution**:
```php
<?php
declare(strict_types=1);

// Ensure transaction is completed
try {
    $txn = $logger->transaction('operation');
    try {
        $txn->logEvent('step1', ['status' => 'complete']);
        $txn->logEvent('step2', ['status' => 'complete']);
        // Transaction auto-completes on finally block
    } finally {
        $txn->commit();
    }
} finally {
    // Transaction cleanup
}

// Check log file location
echo sprintf("Log file: %s\n", $logger->getLogFile());

// Verify log rotation settings
$logger = new AuditLogger(
    service: 'my_script',
    logDir: '/var/log/myapp',
    retentionDays: 90
);
```

---

### Troubleshooting Exercise 2.5

**Scenario**: A script is failing intermittently with the following symptoms:
- Rate limit errors despite using API Client
- Some operations not in audit log
- Metrics show incorrect counts
- Checkpoints not preventing re-processing

**Your Task**: Debug and fix the script.

```php
<?php
declare(strict_types=1);

// Buggy script
class BuggyScript extends CliFramework
{
    protected function run(): int
    {
        // BUG: Libraries not initialized
        $repos = $this->api->listRepos(org: 'mokoconsulting-tech');
        
        foreach ($repos as $repo) {
            // BUG: No audit logging
            // BUG: No checkpoint check
            $this->processRepo($repo);
            
            // BUG: Metrics incremented incorrectly
            $this->metrics->increment('repos');
        }
        
        // BUG: Transaction never started
        return 0;
    }
}
```

**Solution**: <details><summary>Click to reveal</summary>

```php
<?php
declare(strict_types=1);

class FixedScript extends CliFramework
{
    private AuditLogger $audit;
    private MetricsCollector $metrics;
    private GitHubClient $api;
    private Checkpoint $checkpoint;
    
    /**
     * Initialize all libraries
     */
    protected function initialize(): void
    {
        parent::initialize();
        $this->audit = new AuditLogger(service: 'fixed_script');
        $this->metrics = new MetricsCollector(service: 'fixed_script');
        $this->api = new GitHubClient(token: getenv('GITHUB_TOKEN') ?: '');
        $this->checkpoint = new Checkpoint(name: 'process_repos');
    }
    
    protected function run(): int
    {
        try {
            $txn = $this->audit->transaction('process_repositories');
            try {
                $repos = $this->api->listRepos(org: 'mokoconsulting-tech');
                $repoCount = count($repos);
                $txn->logEvent('repos_fetched', ['count' => $repoCount]);
                
                foreach ($repos as $repo) {
                    $repoName = $repo['name'];
                    
                    // Check checkpoint
                    if ($this->checkpoint->isCompleted($repoName)) {
                        continue;
                    }
                    
                    try {
                        $this->processRepo($repo);
                        $this->checkpoint->markCompleted($repoName);
                        $this->metrics->increment('repos_processed_success');
                        $txn->logEvent('repo_processed', ['repo' => $repoName]);
                    } catch (\Exception $e) {
                        $this->checkpoint->markFailed($repoName, $e->getMessage());
                        $this->metrics->increment('repos_processed_failure');
                        $txn->logEvent('repo_failed', ['repo' => $repoName, 'error' => $e->getMessage()]);
                    }
                }
                
                $txn->logEvent('complete', ['total' => $repoCount]);
            } finally {
                $txn->commit();
            }
        } finally {
            // Transaction cleanup
        }
        
        return 0;
    }
}
```
</details>

---

## Part 5: Real-World Examples (20 minutes)

### Example 1: Bulk Repository Updater

Reference: Production script from the repository.

**Key Integration Points**:
- CLI Framework for argument parsing
- Enterprise Audit for compliance trail
- API Client for rate-limited GitHub API calls
- Error Recovery for checkpointing batch updates
- Metrics for tracking update statistics

**Code Walkthrough**: See `scripts/automation/bulk_update_repos.php`

---

### Example 2: Organization Project Creator

Reference: Production script from the repository.

**Key Integration Points**:
- CLI Framework with extended arguments
- Enterprise Audit for project creation tracking
- API Client for GitHub Projects API
- Transaction Manager for atomic project creation
- Security Validator for input validation

**Code Walkthrough**: See PHP web interface at `public/index.php` (Organization Management section)

---

### Example 3: Branch Cleanup Script

Reference: Production script from the repository.

**Key Integration Points**:
- CLI Framework with date-based arguments
- Enterprise Audit for deletion tracking
- API Client for branch operations
- Error Recovery with checkpoint-based recovery
- Metrics for cleanup statistics

**Code Walkthrough**: See PHP web interface at `public/index.php` (Branch Management section)

---

### Example 4: Unified Release Manager

Reference: Production script from the repository.

**Key Integration Points**:
- CLI Framework with release arguments
- Enterprise Audit for release audit trail
- API Client for release operations
- Transaction Manager for atomic multi-repo releases
- Error Recovery for release rollback

**Code Walkthrough**: See PHP web interface at `public/index.php` (Release Management section)

---

## Part 6: Q&A and Next Steps (20 minutes)

### Key Takeaways

✅ **Always start with CLI Framework** - Provides consistent structure  
✅ **Add audit logging early** - Track operations from the start  
✅ **Use checkpointing for batch operations** - Enable recovery  
✅ **Track metrics for observability** - Monitor script performance  
✅ **Validate inputs with security validator** - Prevent vulnerabilities  

### Common Pitfalls to Avoid

❌ Forgetting to initialize libraries in `initialize()`  
❌ Not using context managers for transactions  
❌ Ignoring checkpoint status in loops  
❌ Hardcoding values instead of using configuration  
❌ Skipping error handling in critical sections  

### Homework Assignment

**Task**: Migrate one of your existing automation scripts to use enterprise libraries.

**Requirements**:
1. Use at least 5 enterprise libraries
2. Add comprehensive audit logging
3. Implement error recovery with checkpointing
4. Track relevant metrics
5. Add security validation
6. Write tests for critical functions

**Deliverable**: Pull request with migrated script

**Due**: Before Session 3

---

## Knowledge Check Quiz

1. **What method should you override to initialize enterprise libraries?**
   - a) `__init__`
   - b) `setup`
   - c) `initialize` ✅
   - d) `configure`

2. **How do you mark a checkpoint as completed?**
   - a) `checkpoint.complete(item_id)`
   - b) `checkpoint.mark_completed(item_id)` ✅
   - c) `checkpoint.finish(item_id)`
   - d) `checkpoint.done(item_id)`

3. **What happens when a transaction context exits normally?**
   - a) Transaction is rolled back
   - b) Transaction is committed automatically ✅
   - c) Transaction is suspended
   - d) Transaction requires manual commit

4. **Which library handles automatic retry with exponential backoff?**
   - a) ApiClient.php
   - b) TransactionManager.php
   - c) ErrorRecovery.php ✅
   - d) CliFramework.php

5. **What's the recommended pattern for batch processing?**
   - a) Essential Stack only
   - b) API Stack + Checkpointing ✅
   - c) Security Stack + Metrics
   - d) CLI Framework only

---

## Additional Resources

- **Source Code**: Review migrated production scripts in `/scripts/`
- **Tests**: Check integration tests in `/.github/workflows/`
- **Documentation**: Read automation guide in `/docs/automation/`
- **Examples**: Explore templates in `/templates/`

---

**Ready for advanced topics?** → Continue to [Session 3: Advanced Features](session-3-advanced-features.md)
