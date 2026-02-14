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
PATH: docs/training/session-3-advanced-features.md
VERSION: 04.00.00
BRIEF: Session 3 - Advanced Features training materials
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Session 3: Advanced Features

**Duration**: 2 hours  
**Format**: Advanced Workshop  
**Prerequisite**: Complete Sessions 1 and 2

---

## Session Objectives

By the end of this session, you will:
- ✅ Implement robust error recovery patterns
- ✅ Design fault-tolerant automation workflows
- ✅ Optimize script performance and resource usage
- ✅ Apply enterprise security patterns
- ✅ Meet audit and compliance requirements
- ✅ Master advanced API client features

---

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 0:00-0:30 | Advanced Error Recovery Patterns | Demo + Practice |
| 0:30-1:00 | Transaction Management Deep Dive | Workshop |
| 1:00-1:30 | Performance Optimization | Demo + Practice |
| 1:30-1:50 | Security & Compliance Best Practices | Discussion + Practice |
| 1:50-2:00 | Certification & Next Steps | Wrap-up |

---

## Part 1: Advanced Error Recovery Patterns (30 minutes)

### Pattern 1: Multi-Level Retry Strategy

**Scenario**: Different operations require different retry strategies.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\RetryWithBackoff;
use MokoStandards\Enterprise\Checkpoint;
use MokoStandards\Enterprise\GitHubClient;
use MokoStandards\Enterprise\AuditLogger;

class AdvancedErrorRecovery
{
    public function __construct()
    {
        $this->api = new GitHubClient();
        $this->audit = new AuditLogger(service: 'advanced_recovery');
        $this->checkpoint = new Checkpoint(name: 'multi_level_recovery');
    }
    
    #[RetryWithBackoff(
        maxRetries: 5,
        baseDelay: 2.0,
        maxDelay: 60.0,
        exponentialBase: 2,
        jitter: true
    )]
    protected function fetchWithAggressiveRetry(string $url): mixed
    {
        // Aggressive retry for critical operations
        return $this->api->get($url);
    }
    
    #[RetryWithBackoff(
        maxRetries: 2,
        baseDelay: 1.0,
        maxDelay: 10.0
    )]
    protected function fetchWithConservativeRetry(string $url): mixed
    {
        // Conservative retry for less critical operations
        return $this->api->get($url);
    }
    
    protected function fetchWithCircuitBreaker(string $url, $circuitBreaker): mixed
    {
        // Use circuit breaker to prevent cascade failures
        if ($circuitBreaker->isOpen()) {
            throw new \Exception("Circuit breaker is open");
        }
        
        try {
            $response = $this->api->get($url);
            $circuitBreaker->recordSuccess();
            return $response;
        } catch (\Exception $e) {
            $circuitBreaker->recordFailure();
            throw $e;
        }
    }
}
```

**Key Concepts**:
- **Exponential Backoff**: Progressively longer waits between retries
- **Jitter**: Random delay to prevent thundering herd
- **Max Delay**: Cap on retry delay to prevent infinite waits
- **Circuit Breaker**: Stop trying when system is failing

---

### Pattern 2: Checkpoint-Based State Recovery

**Scenario**: Long-running operations that need to resume after failures.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\Checkpoint;
use MokoStandards\Enterprise\AuditLogger;

class StateRecoveryManager
{
    public function __construct(string $operationName)
    {
        $this->checkpoint = new Checkpoint(
            name: $operationName,
            checkpointDir: '/var/lib/myapp/checkpoints'
        );
        $this->audit = new AuditLogger(service: 'state_recovery');
    }
    
    protected function saveState(string $itemId, array $stateData): mixed
    {
        // Save detailed state for recovery
        $this->checkpoint->markCompleted($itemId, [
            'state' => $stateData,
            'timestamp' => (new \DateTime('now', new \DateTimeZone('UTC')))->format(\DateTime::ATOM),
            'version' => '1.0'
        ]);
    }
    
    protected function loadState(string $itemId): mixed
    {
        // Load saved state
        return $this->checkpoint->getState($itemId);
    }
    
    protected function processWithRecovery(array $items): mixed
    {
        // Process items with state recovery
        
        foreach ($items as $item) {
            $itemId = $item['id'];
            
            // Check if already completed
            if ($this->checkpoint->isCompleted($itemId)) {
                echo "Resuming from completed state: {$itemId}";
                continue;
            }
            
            // Load previous state if exists
            $previousState = $this->loadState($itemId);
            if ($previousState) {
                echo "Resuming from checkpoint: {$itemId}";
                $currentStep = $previousState['current_step'] ?? 0;
            } else {
                $currentStep = 0;
            }
            
            // Multi-step processing with state saving
            try {
                // Step 1
                if ($currentStep < 1) {
                    $this->processStep1($item);
                    $this->saveState($itemId, ['current_step' => 1, 'data' => $item]);
                    $currentStep = 1;
                }
                
                // Step 2
                if ($currentStep < 2) {
                    $this->processStep2($item);
                    $this->saveState($itemId, ['current_step' => 2, 'data' => $item]);
                    $currentStep = 2;
                }
                
                // Step 3
                if ($currentStep < 3) {
                    $this->processStep3($item);
                    $this->saveState($itemId, ['current_step' => 3, 'data' => $item]);
                    $currentStep = 3;
                }
                
                // Mark as fully completed
                $this->checkpoint->markCompleted($itemId, [
                    'status' => 'complete',
                    'steps_completed' => 3
                ]);
                
            } catch (\Exception $e) {
                echo "Failed at step {$currentStep}: {$e}";
                $this->checkpoint->markFailed($itemId, (string)$e);
                // State is already saved, can resume later
            }
        }
    }
}
```

**Exercise 3.1**: Implement multi-step processing with state recovery
```php
<?php
declare(strict_types=1);

// TODO: Create a 5-step process with checkpoint after each step
// TODO: Simulate failures at different steps
// TODO: Verify recovery continues from last successful checkpoint
```

---

### Pattern 3: Dead Letter Queue for Failed Items

**Scenario**: Handle items that fail repeatedly without blocking the entire process.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\Checkpoint;
use MokoStandards\Enterprise\MetricsCollector;

class DeadLetterQueue
{
    public function __construct(string $name, int $maxRetries = 3)
    {
        $this->name = $name;
        $this->maxRetries = $maxRetries;
        $this->checkpoint = new Checkpoint(name: $name);
        $this->metrics = new MetricsCollector(service: $name);
        $this->dlqPath = new \SplFileInfo("/var/lib/myapp/dlq/{$name}");
        if (!is_dir($this->dlqPath->getPathname())) {
            mkdir($this->dlqPath->getPathname(), 0755, true);
        }
    }
    
    protected function processWithDlq(array $items): mixed
    {
        // Process items with dead letter queue
        
        foreach ($items as $item) {
            $itemId = $item['id'];
            
            // Check retry count
            $retryCount = $this->checkpoint->getRetryCount($itemId);
            
            if ($retryCount >= $this->maxRetries) {
                // Move to dead letter queue
                $this->moveToDlq($item, "Max retries ({$this->maxRetries}) exceeded");
                $this->metrics->increment('items_moved_to_dlq');
                continue;
            }
            
            try {
                $this->processItem($item);
                $this->checkpoint->markCompleted($itemId);
                $this->metrics->increment('items_processed_success');
                
            } catch (\Exception $e) {
                // Increment retry count
                $this->checkpoint->incrementRetryCount($itemId);
                $this->checkpoint->markFailed($itemId, (string)$e);
                $this->metrics->increment('items_retried');
                
                echo "Failed {$itemId} (attempt " . ($retryCount + 1) . "/{$this->maxRetries}): {$e}";
            }
        }
    }
    
    protected function moveToDlq(array $item, string $reason): mixed
    {
        // Move failed item to dead letter queue
        $dlqFile = $this->dlqPath->getPathname() . "/{$item['id']}.json";
        
        $dlqEntry = [
            'item' => $item,
            'reason' => $reason,
            'timestamp' => (new \DateTime('now', new \DateTimeZone('UTC')))->format(\DateTime::ATOM),
            'retry_count' => $this->checkpoint->getRetryCount($item['id'])
        ];
        
        file_put_contents($dlqFile, json_encode($dlqEntry, JSON_PRETTY_PRINT));
        
        echo "Moved {$item['id']} to dead letter queue: {$reason}";
    }
    
    protected function processDlq(): mixed
    {
        // Manually process items from dead letter queue
        $dlqItems = glob($this->dlqPath->getPathname() . '/*.json');
        
        echo "Found " . count($dlqItems) . " items in dead letter queue";
        
        foreach ($dlqItems as $dlqFile) {
            $dlqEntry = json_decode(file_get_contents($dlqFile), true);
            
            $item = $dlqEntry['item'];
            echo "Manual processing: {$item['id']}";
            
            try {
                $this->processItem($item);
                // Remove from DLQ
                unlink($dlqFile);
                $this->checkpoint->markCompleted($item['id']);
                echo "Successfully processed {$item['id']} from DLQ";
                
            } catch (\Exception $e) {
                echo "Still failing: {$item['id']}: {$e}";
            }
        }
    }
}
```

**Exercise 3.2**: Implement DLQ pattern
```php
<?php
declare(strict_types=1);

// TODO: Process a batch where 10% of items fail
// TODO: Verify failed items move to DLQ after max retries
// TODO: Implement manual DLQ processing
```

---

## Part 2: Transaction Management Deep Dive (30 minutes)

### Pattern 4: Nested Transactions

**Scenario**: Complex operations with sub-operations that need independent rollback.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\TransactionManager;
use MokoStandards\Enterprise\AuditLogger;

class NestedTransactionExample
{
    public function __construct()
    {
        $this->txnManager = new TransactionManager();
        $this->audit = new AuditLogger(service: 'nested_transactions');
    }
    
    protected function updateOrganization(string $org): mixed
    {
        // Update organization with nested transactions
        
        try {
            $parentTxn = $this->txnManager->beginTransaction("update_org_{$org}");
            
            // Sub-transaction 1: Update organization settings
            try {
                $txn1 = $this->txnManager->beginTransaction("org_settings_{$org}");
                $txn1->addOperation(
                    'update_org_settings',
                    forward: fn() => $this->updateOrgSettings($org),
                    rollback: fn() => $this->restoreOrgSettings($org)
                );
                $txn1->commit();
            } finally {
            }
            
            // Sub-transaction 2: Update all repositories
            try {
                $txn2 = $this->txnManager->beginTransaction("org_repos_{$org}");
                $repos = $this->getRepositories($org);
                
                foreach ($repos as $repo) {
                    // Independent transaction per repository
                    try {
                        $repoTxn = $this->txnManager->beginTransaction("repo_{$repo}");
                        $repoTxn->addOperation(
                            'update_repo',
                            forward: fn() => $this->updateRepository($org, $repo),
                            rollback: fn() => $this->restoreRepository($org, $repo)
                        );
                        $repoTxn->commit();
                    } catch (\Exception $e) {
                        // Individual repo failure doesn't affect others
                        echo "Failed to update {$repo}: {$e}";
                        continue;
                    } finally {
                    }
                }
                
                $txn2->commit();
            } finally {
            }
            
            // Sub-transaction 3: Update team settings
            try {
                $txn3 = $this->txnManager->beginTransaction("org_teams_{$org}");
                $txn3->addOperation(
                    'update_teams',
                    forward: fn() => $this->updateTeams($org),
                    rollback: fn() => $this->restoreTeams($org)
                );
                $txn3->commit();
            } finally {
            }
            
            // Commit parent transaction
            $parentTxn->commit();
            echo "Successfully updated organization: {$org}";
        } finally {
        }
    }
}
```

**Key Concepts**:
- **Nested Transactions**: Sub-transactions within parent transactions
- **Partial Rollback**: Failed sub-transaction rolls back without affecting parent
- **Isolation**: Each transaction has independent commit/rollback
- **Atomicity**: Each level maintains all-or-nothing guarantee

---

### Pattern 5: Compensating Transactions

**Scenario**: Handle operations that can't be rolled back directly.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\TransactionManager;

class CompensatingTransaction
{
    public function __construct()
    {
        $this->txnManager = new TransactionManager();
        $this->stateLog = [];
    }
    
    protected function createRepository(string $org, string $repoName, array $settings): mixed
    {
        // Create repository with compensating transaction
        
        try {
            $txn = $this->txnManager->beginTransaction("create_repo_{$repoName}");
            
            
            // Operation 1: Create repository
            // (Can't be rolled back, so we use compensating action)
            $txn->addOperation(
                'create_repository',
                forward: fn() => $this->api->createRepo($org, $repoName, $settings),
                rollback: fn() => $this->api->deleteRepo($org, $repoName)  // Compensating action
            );
            
            // Operation 2: Set up branch protection
            $txn->addOperation(
                'setup_protection',
                forward: fn() => $this->api->updateBranchProtection($org, $repoName, 'main', []),
                rollback: fn() => $this->api->deleteBranchProtection($org, $repoName, 'main')
            );
            
            // Operation 3: Add collaborators
            $txn->addOperation(
                'add_collaborators',
                forward: fn() => $this->addTeamAccess($org, $repoName),
                rollback: fn() => $this->removeTeamAccess($org, $repoName)
            );
            
            // Operation 4: Create initial issues
            $txn->addOperation(
                'create_issues',
                forward: fn() => $this->createInitialIssues($org, $repoName),
                rollback: fn() => $this->closeInitialIssues($org, $repoName)
            );
            
            try {
                $txn->commit();
                echo "Repository {$repoName} created successfully";
                return true;
                
            } catch (\Exception $e) {
                echo "Failed to create repository: {$e}";
                echo "Rolling back all operations...";
                // Compensating actions execute automatically
                return false;
            }
        } finally {
        }
    }
    
    protected function addTeamAccess(string $org, string $repoName): mixed
    {
        // Add team access with state tracking
        $teams = ['developers', 'maintainers', 'admins'];
        $addedTeams = [];
        
        try {
            foreach ($teams as $team) {
                $this->api->addTeamToRepo($org, $repoName, $team);
                $addedTeams[] = $team;
            }
            
            // Save state for rollback
            $this->stateLog[] = [
                'operation' => 'add_team_access',
                'repo' => $repoName,
                'teams' => $addedTeams
            ];
            
        } catch (\Exception $e) {
            // Partial rollback
            foreach ($addedTeams as $team) {
                $this->api->removeTeamFromRepo($org, $repoName, $team);
            }
            throw $e;
        }
    }
    
    protected function removeTeamAccess(string $org, string $repoName): mixed
    {
        // Compensating action: remove team access
        // Find teams from state log
        foreach ($this->stateLog as $entry) {
            if ($entry['operation'] === 'add_team_access' && $entry['repo'] === $repoName) {
                foreach ($entry['teams'] as $team) {
                    $this->api->removeTeamFromRepo($org, $repoName, $team);
                }
            }
        }
    }
}
```

**Exercise 3.3**: Implement compensating transactions
```php
<?php
declare(strict_types=1);

// TODO: Create a multi-step workflow with compensating actions
// TODO: Trigger a failure in step 3 of 5
// TODO: Verify all previous steps are compensated correctly
```

---

### Pattern 6: Saga Pattern for Distributed Operations

**Scenario**: Coordinate operations across multiple systems.

```php
<?php
declare(strict_types=1);

class SagaOrchestrator
{
    public function __construct()
    {
        $this->txnManager = new TransactionManager();
        $this->audit = new AuditLogger(service: 'saga_orchestrator');
    }
    
    protected function executeSaga(string $sagaName, array $steps): mixed
    {
        // Execute a saga with compensation
        
        try {
            $auditTxn = $this->audit->transaction($sagaName);
            try {
                $txn = $this->txnManager->beginTransaction($sagaName);
                
                foreach ($steps as $step) {
                    $stepName = $step['name'];
                    $forwardAction = $step['forward'];
                    $compensatingAction = $step['compensate'];
                    
                    $auditTxn->logEvent('step_start', ['step' => $stepName]);
                    
                    $txn->addOperation(
                        $stepName,
                        forward: $forwardAction,
                        rollback: $compensatingAction
                    );
                    
                    $auditTxn->logEvent('step_complete', ['step' => $stepName]);
                }
                
                try {
                    $txn->commit();
                    $auditTxn->logEvent('saga_complete', ['status' => 'success']);
                    return true;
                    
                } catch (\Exception $e) {
                    $auditTxn->logEvent('saga_failed', [
                        'status' => 'failure',
                        'error' => (string)$e,
                        'compensating' => true
                    ]);
                    // Compensating actions execute in reverse order
                    return false;
                }
            } finally {
            }
        } finally {
        }
    }
}

// Example usage
$orchestrator = new SagaOrchestrator();

$sagaSteps = [
    [
        'name' => 'create_github_repo',
        'forward' => fn() => $githubApi->createRepo('myrepo'),
        'compensate' => fn() => $githubApi->deleteRepo('myrepo')
    ],
    [
        'name' => 'create_ci_pipeline',
        'forward' => fn() => $ciSystem->createPipeline('myrepo'),
        'compensate' => fn() => $ciSystem->deletePipeline('myrepo')
    ],
    [
        'name' => 'setup_monitoring',
        'forward' => fn() => $monitoring->addRepo('myrepo'),
        'compensate' => fn() => $monitoring->removeRepo('myrepo')
    ],
    [
        'name' => 'notify_team',
        'forward' => fn() => $slack->notify('New repo: myrepo'),
        'compensate' => fn() => $slack->notify('Repo creation failed: myrepo')
    ]
];

$success = $orchestrator->executeSaga('onboard_repository', $sagaSteps);
```

**Exercise 3.4**: Build a saga orchestrator
```php
<?php
declare(strict_types=1);

// TODO: Create a saga with 4 distributed operations
// TODO: Implement proper compensation for each step
// TODO: Test failure at different points in the saga
```

---

## Part 3: Performance Optimization (30 minutes)

### Pattern 7: API Client Caching Strategy

**Scenario**: Optimize API calls with intelligent caching.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\GitHubClient;
use MokoStandards\Enterprise\RateLimitConfig;

class OptimizedAPIClient
{
    public function __construct()
    {
        // Configure aggressive caching
        $rateConfig = new RateLimitConfig(
            maxRequestsPerHour: 5000,
            burstSize: 100,
            enableCaching: true,
            cacheTtl: 3600  // 1 hour cache
        );
        
        $this->api = new GitHubClient(
            token: getenv('GITHUB_TOKEN'),
            rateLimitConfig: $rateConfig
        );
        
        $this->localCache = [];
        $this->cacheHits = 0;
        $this->cacheMisses = 0;
    }
    
    protected function getRepositoryCached(string $org, string $repo): mixed
    {
        // Get repository with local LRU cache
        static $cache = [];
        $key = "{$org}/{$repo}";
        
        if (isset($cache[$key])) {
            $this->cacheHits++;
            return $cache[$key];
        }
        
        $this->cacheMisses++;
        $result = $this->api->getRepo($org, $repo);
        $cache[$key] = $result;
        
        if (count($cache) > 1000) {
            array_shift($cache);
        }
        
        return $result;
    }
    
    protected function getRepositoryWithEtag(string $org, string $repo): mixed
    {
        // Get repository with ETag-based caching
        $cacheKey = "{$org}/{$repo}";
        
        // Check local cache
        if (isset($this->localCache[$cacheKey])) {
            [$cachedData, $etag, $timestamp] = $this->localCache[$cacheKey];
            
            // Cache still valid?
            if (time() - $timestamp < 300) {  // 5 minutes
                $this->cacheHits++;
                return $cachedData;
            }
            
            // Conditional request with ETag
            $response = $this->api->getRepo(
                $org, $repo,
                headers: ['If-None-Match' => $etag]
            );
            
            if ($response->statusCode === 304) {  // Not Modified
                $this->cacheHits++;
                // Update timestamp
                $this->localCache[$cacheKey] = [$cachedData, $etag, time()];
                return $cachedData;
            }
        }
        
        // Fetch fresh data
        $this->cacheMisses++;
        $response = $this->api->getRepo($org, $repo);
        
        // Cache with ETag
        $etag = $response->headers['ETag'] ?? null;
        $this->localCache[$cacheKey] = [$response->json(), $etag, time()];
        
        return $response->json();
    }
    
    protected function getCacheStats(): mixed
    {
        // Get cache performance statistics
        $totalRequests = $this->cacheHits + $this->cacheMisses;
        $hitRate = $totalRequests > 0 ? $this->cacheHits / $totalRequests : 0;
        
        return [
            'cache_hits' => $this->cacheHits,
            'cache_misses' => $this->cacheMisses,
            'hit_rate' => sprintf("%.2f%%", $hitRate * 100),
            'cache_size' => count($this->localCache)
        ];
    }
}
```

**Exercise 3.5**: Optimize API performance
```php
<?php
declare(strict_types=1);

// TODO: Fetch 100 repositories multiple times
// TODO: Compare performance with and without caching
// TODO: Measure cache hit rate
// TODO: Calculate API rate limit savings
```

---

### Pattern 8: Batch Processing Optimization

**Scenario**: Process large datasets efficiently.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\MetricsCollector;

class BatchOptimizer
{
    public function __construct(int $maxWorkers = 10)
    {
        $this->maxWorkers = $maxWorkers;
        $this->metrics = new MetricsCollector(service: 'batch_optimizer');
    }
    
    protected function processSequential(array $items): mixed
    {
        // Sequential processing (baseline)
        $startTime = microtime(true);
        $results = [];
        
        foreach ($items as $item) {
            $result = $this->processItem($item);
            $results[] = $result;
        }
        
        $elapsed = microtime(true) - $startTime;
        $this->metrics->recordHistogram('batch_duration_sequential', $elapsed);
        
        return $results;
    }
    
    protected function processParallel(array $items): mixed
    {
        // Parallel processing with thread pool
        $startTime = microtime(true);
        $results = [];
        
        $pool = new \Pool($this->maxWorkers);
        $futures = [];
        
        foreach ($items as $item) {
            $futures[] = $pool->submit(fn() => $this->processItem($item));
        }
        
        foreach ($futures as $i => $future) {
            try {
                $result = $future->get();
                $results[] = $result;
                $this->metrics->increment('items_processed_success');
            } catch (\Exception $e) {
                echo "Failed to process {$items[$i]}: {$e}";
                $this->metrics->increment('items_processed_failure');
            }
        }
        
        $elapsed = microtime(true) - $startTime;
        $this->metrics->recordHistogram('batch_duration_parallel', $elapsed);
        
        return $results;
    }
    
    protected function processBatched(array $items, int $batchSize = 50): mixed
    {
        // Process in batches for better throughput
        $startTime = microtime(true);
        $results = [];
        
        // Split into batches
        $batches = array_chunk($items, $batchSize);
        
        foreach ($batches as $batchNum => $batch) {
            echo "Processing batch " . ($batchNum + 1) . "/" . count($batches);
            
            $pool = new \Pool($this->maxWorkers);
            $batchResults = array_map(fn($item) => $this->processItem($item), $batch);
            $results = array_merge($results, $batchResults);
            
            // Brief pause between batches to avoid overwhelming systems
            usleep(500000);
        }
        
        $elapsed = microtime(true) - $startTime;
        $this->metrics->recordHistogram('batch_duration_batched', $elapsed);
        
        return $results;
    }
    
    protected function comparePerformance(array $items): mixed
    {
        // Compare different processing strategies
        echo "Processing " . count($items) . " items...\n";
        
        // Sequential
        echo "Sequential processing...";
        $start = microtime(true);
        $this->processSequential(array_slice($items, 0, 100));  // Sample
        $seqTime = microtime(true) - $start;
        $seqRate = 100 / $seqTime;
        
        // Parallel
        echo "Parallel processing...";
        $start = microtime(true);
        $this->processParallel(array_slice($items, 0, 100));  // Sample
        $parTime = microtime(true) - $start;
        $parRate = 100 / $parTime;
        
        // Batched
        echo "Batched processing...";
        $start = microtime(true);
        $this->processBatched(array_slice($items, 0, 100), batchSize: 20);  // Sample
        $batchTime = microtime(true) - $start;
        $batchRate = 100 / $batchTime;
        
        // Report
        echo "\nPerformance Comparison:";
        echo sprintf("Sequential: %.2fs (%.1f items/sec)", $seqTime, $seqRate);
        echo sprintf("Parallel:   %.2fs (%.1f items/sec) - %.1fx faster", $parTime, $parRate, $seqTime / $parTime);
        echo sprintf("Batched:    %.2fs (%.1f items/sec) - %.1fx faster", $batchTime, $batchRate, $seqTime / $batchTime);
        
        return [
            'sequential' => $seqRate,
            'parallel' => $parRate,
            'batched' => $batchRate
        ];
    }
}
```

**Exercise 3.6**: Optimize batch processing
```php
<?php
declare(strict_types=1);

// TODO: Process 500 items using all three strategies
// TODO: Measure and compare performance
// TODO: Find optimal batch size and worker count
// TODO: Consider memory usage and API rate limits
```

---

### Pattern 9: Memory-Efficient Processing

**Scenario**: Process large datasets without loading everything into memory.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\GitHubClient;

class MemoryEfficientProcessor
{
    public function __construct()
    {
        $this->api = new GitHubClient();
    }
    
    protected function streamRepositories(string $org): mixed
    {
        // Stream repositories without loading all into memory
        $page = 1;
        $perPage = 100;
        
        while (true) {
            $repos = $this->api->listRepos(
                org: $org,
                page: $page,
                perPage: $perPage
            );
            
            if (!$repos) {
                break;
            }
            
            foreach ($repos as $repo) {
                yield $repo;
            }
            
            $page++;
            
            if (count($repos) < $perPage) {
                break;
            }
        }
    }
    
    protected function processLargeDataset(string $org): mixed
    {
        // Process repositories one at a time
        $processed = 0;
        
        foreach ($this->streamRepositories($org) as $repo) {
            // Process individual repo
            $this->processRepository($repo);
            $processed++;
            
            if ($processed % 100 === 0) {
                echo "Processed {$processed} repositories...";
            }
        }
        
        echo "Total processed: {$processed}";
    }
    
    protected function processInChunks(string $org, int $chunkSize = 10): mixed
    {
        // Process repositories in small chunks
        $repoStream = $this->streamRepositories($org);
        
        while (true) {
            // Get next chunk
            $chunk = [];
            $count = 0;
            foreach ($repoStream as $repo) {
                $chunk[] = $repo;
                $count++;
                if ($count >= $chunkSize) {
                    break;
                }
            }
            
            if (empty($chunk)) {
                break;
            }
            
            // Process chunk
            $this->processChunk($chunk);
            
            // Explicit memory cleanup
            unset($chunk);
        }
    }
}
```

**Exercise 3.7**: Implement memory-efficient processing
```php
<?php
declare(strict_types=1);

// TODO: Process 1000+ repositories without loading all into memory
// TODO: Monitor memory usage during processing
// TODO: Compare memory footprint with traditional approach
```

---

## Part 4: Security & Compliance (20 minutes)

### Pattern 10: Comprehensive Security Validation

**Scenario**: Implement defense-in-depth security.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\SecurityValidator;
use MokoStandards\Enterprise\AuditLogger;
use MokoStandards\Enterprise\ConfigManager;

class SecureAutomation
{
    public function __construct()
    {
        $this->security = new SecurityValidator();
        $this->audit = new AuditLogger(service: 'secure_automation');
        $this->config = ConfigManager::load(env: 'production');
    }
    
    protected function validateAllInputs(array $userInputs): mixed
    {
        // Multi-layer input validation
        
        try {
            $txn = $this->audit->transaction('input_validation');
            
            // Layer 1: Type validation
            foreach ($userInputs as $key => $value) {
                $expectedType = $this->config->get("validation.{$key}.type");
                if (!($value instanceof $expectedType)) {
                    throw new \ValueError("Invalid type for {$key}");
                }
            }
            
            // Layer 2: Pattern validation
            foreach ($userInputs as $key => $value) {
                if (is_string($value)) {
                    if (!$this->security->validateInput($value, inputType: 'identifier')) {
                        $txn->logSecurityEvent('validation_failure', [
                            'field' => $key,
                            'reason' => 'invalid_pattern'
                        ]);
                        throw new \ValueError("Invalid pattern in {$key}");
                    }
                }
            }
            
            // Layer 3: Credential detection
            foreach ($userInputs as $key => $value) {
                if ($this->security->detectCredentials((string)$value)) {
                    $txn->logSecurityEvent('credential_detected', [
                        'field' => $key,
                        'severity' => 'HIGH'
                    ]);
                    throw new \ValueError("Credential detected in {$key}");
                }
            }
            
            // Layer 4: SQL injection detection
            foreach ($userInputs as $key => $value) {
                if (is_string($value)) {
                    if ($this->security->detectSqlInjection($value)) {
                        $txn->logSecurityEvent('sql_injection_attempt', [
                            'field' => $key,
                            'severity' => 'CRITICAL'
                        ]);
                        throw new \ValueError("SQL injection detected in {$key}");
                    }
                }
            }
            
            // Layer 5: Path traversal prevention
            foreach ($userInputs as $key => $value) {
                if (stripos($key, 'path') !== false || stripos($key, 'file') !== false) {
                    if (!$this->security->validatePath($value)) {
                        $txn->logSecurityEvent('path_traversal_attempt', [
                            'field' => $key,
                            'value' => $value,
                            'severity' => 'HIGH'
                        ]);
                        throw new \ValueError("Path traversal detected in {$key}");
                    }
                }
            }
            
            $txn->logEvent('validation_complete', [
                'fields_validated' => count($userInputs),
                'status' => 'success'
            ]);
            
            return true;
        } finally {
        }
    }
    
    protected function scanBeforeExecution(string $scriptPath): mixed
    {
        // Security scan before executing scripts
        
        try {
            $txn = $this->audit->transaction('security_scan');
            
            // Scan for security issues
            $findings = $this->security->scanDirectory($scriptPath);
            
            // Categorize by severity
            $critical = array_filter($findings, fn($f) => $f['severity'] === 'CRITICAL');
            $high = array_filter($findings, fn($f) => $f['severity'] === 'HIGH');
            $medium = array_filter($findings, fn($f) => $f['severity'] === 'MEDIUM');
            
            // Log findings
            $txn->logEvent('scan_complete', [
                'critical' => count($critical),
                'high' => count($high),
                'medium' => count($medium)
            ]);
            
            // Block on critical findings
            if (!empty($critical)) {
                $txn->logSecurityEvent('execution_blocked', [
                    'reason' => 'critical_security_findings',
                    'count' => count($critical)
                ]);
                throw new \SecurityError("Found " . count($critical) . " critical security issues");
            }
            
            // Warn on high findings
            if (!empty($high)) {
                $txn->logSecurityEvent('execution_warning', [
                    'reason' => 'high_security_findings',
                    'count' => count($high)
                ]);
                echo "WARNING: Found " . count($high) . " high-severity security issues";
            }
            
            return $findings;
        } finally {
        }
    }
}
```

**Exercise 3.8**: Build comprehensive security validation
```php
<?php
declare(strict_types=1);

// TODO: Implement all 5 validation layers
// TODO: Test with various malicious inputs
// TODO: Verify all attacks are detected and blocked
// TODO: Ensure audit trail captures all security events
```

---

### Pattern 11: Compliance and Audit Reporting

**Scenario**: Generate compliance reports for auditors.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\AuditLogger;
use MokoStandards\Enterprise\MetricsCollector;

class ComplianceReporter
{
    public function __construct()
    {
        $this->audit = new AuditLogger(service: 'compliance_reporter');
        $this->metrics = new MetricsCollector(service: 'compliance_reporter');
    }
    
    protected function generateComplianceReport(string $startDate, string $endDate): mixed
    {
        // Generate comprehensive compliance report
        
        $report = [
            'report_metadata' => [
                'generated_at' => (new \DateTime('now', new \DateTimeZone('UTC')))->format(\DateTime::ATOM),
                'period_start' => $startDate,
                'period_end' => $endDate,
                'report_version' => '1.0'
            ],
            'audit_summary' => $this->getAuditSummary($startDate, $endDate),
            'security_events' => $this->getSecurityEvents($startDate, $endDate),
            'access_log' => $this->getAccessLog($startDate, $endDate),
            'changes_made' => $this->getChangeLog($startDate, $endDate),
            'compliance_metrics' => $this->getComplianceMetrics($startDate, $endDate)
        ];
        
        return $report;
    }
    
    protected function getAuditSummary(string $startDate, string $endDate): mixed
    {
        // Get audit trail summary
        $events = $this->audit->generateReport(
            startDate: $startDate,
            endDate: $endDate
        );
        
        return [
            'total_transactions' => count(array_unique(array_column($events, 'transaction_id'))),
            'total_events' => count($events),
            'services' => array_values(array_unique(array_column($events, 'service'))),
            'users' => array_values(array_unique(array_map(fn($e) => $e['user'] ?? 'system', $events)))
        ];
    }
    
    protected function getSecurityEvents(string $startDate, string $endDate): mixed
    {
        // Get security-related events
        $events = $this->audit->generateReport(
            startDate: $startDate,
            endDate: $endDate,
            filterBy: ['event_type' => 'security']
        );
        
        // Group by severity
        $bySeverity = [];
        foreach ($events as $event) {
            $severity = $event['severity'] ?? 'UNKNOWN';
            if (!isset($bySeverity[$severity])) {
                $bySeverity[$severity] = [];
            }
            $bySeverity[$severity][] = $event;
        }
        
        return [
            'total_security_events' => count($events),
            'by_severity' => array_map('count', $bySeverity),
            'critical_events' => $bySeverity['CRITICAL'] ?? [],
            'high_events' => $bySeverity['HIGH'] ?? []
        ];
    }
    
    protected function getAccessLog(string $startDate, string $endDate): mixed
    {
        // Get access log for audit trail
        $events = $this->audit->generateReport(
            startDate: $startDate,
            endDate: $endDate,
            filterBy: ['event_type' => 'access']
        );
        
        return [
            'total_access_events' => count($events),
            'unique_users' => count(array_unique(array_filter(array_column($events, 'user')))),
            'access_by_service' => $this->groupByService($events)
        ];
    }
    
    protected function getChangeLog(string $startDate, string $endDate): mixed
    {
        // Get all changes made during period
        $events = $this->audit->generateReport(
            startDate: $startDate,
            endDate: $endDate,
            filterBy: ['event_type' => 'change']
        );
        
        return [
            'total_changes' => count($events),
            'changes_by_type' => $this->groupByType($events),
            'rollbacks' => array_filter($events, fn($e) => $e['rollback'] ?? false)
        ];
    }
    
    protected function getComplianceMetrics(string $startDate, string $endDate): mixed
    {
        // Get compliance-specific metrics
        return [
            'audit_coverage' => $this->calculateAuditCoverage(),
            'security_scan_results' => $this->getSecurityScanStats(),
            'failed_operations' => $this->getFailedOperationsCount(),
            'sla_compliance' => $this->calculateSlaCompliance()
        ];
    }
    
    protected function exportReport(array $report, string $format = 'json'): mixed
    {
        // Export compliance report
        
        if ($format === 'json') {
            return json_encode($report, JSON_PRETTY_PRINT);
        }
        
        if ($format === 'html') {
            return $this->generateHtmlReport($report);
        }
        
        if ($format === 'pdf') {
            return $this->generatePdfReport($report);
        }
        
        throw new \ValueError("Unsupported format: {$format}");
    }
}
```

**Exercise 3.9**: Generate compliance report
```php
<?php
declare(strict_types=1);

// TODO: Run various operations with audit logging
// TODO: Generate compliance report for the period
// TODO: Verify all required data is present
// TODO: Export in multiple formats
```

---

## Part 5: Advanced API Client Features (20 minutes)

### Pattern 12: Circuit Breaker Implementation

**Scenario**: Protect against cascading failures.

```php
<?php
declare(strict_types=1);

use MokoStandards\Enterprise\GitHubClient;

enum CircuitState: string
{
    case CLOSED = "closed";  // Normal operation
    case OPEN = "open";  // Failing, reject requests
    case HALF_OPEN = "half_open";  // Testing recovery
}

class CircuitBreaker
{
    public function __construct(int $failureThreshold = 5, int $timeout = 60, int $successThreshold = 2)
    {
        $this->failureThreshold = $failureThreshold;
        $this->timeout = $timeout;
        $this->successThreshold = $successThreshold;
        
        $this->failureCount = 0;
        $this->successCount = 0;
        $this->lastFailureTime = null;
        $this->state = CircuitState::CLOSED;
    }
    
    protected function call(callable $func, ...$args): mixed
    {
        // Execute function through circuit breaker
        
        if ($this->state === CircuitState::OPEN) {
            if (time() - $this->lastFailureTime >= $this->timeout) {
                // Try to recover
                $this->state = CircuitState::HALF_OPEN;
                echo "Circuit breaker moving to HALF_OPEN state";
            } else {
                throw new \Exception("Circuit breaker is OPEN");
            }
        }
        
        try {
            $result = $func(...$args);
            $this->onSuccess();
            return $result;
            
        } catch (\Exception $e) {
            $this->onFailure();
            throw $e;
        }
    }
    
    protected function onSuccess(): mixed
    {
        // Handle successful call
        if ($this->state === CircuitState::HALF_OPEN) {
            $this->successCount++;
            
            if ($this->successCount >= $this->successThreshold) {
                // Recovery successful
                $this->state = CircuitState::CLOSED;
                $this->failureCount = 0;
                $this->successCount = 0;
                echo "Circuit breaker CLOSED - recovered";
            }
        } else {
            // Reset failure count on success
            $this->failureCount = 0;
        }
    }
    
    protected function onFailure(): mixed
    {
        // Handle failed call
        $this->failureCount++;
        $this->lastFailureTime = time();
        
        if ($this->failureCount >= $this->failureThreshold) {
            $this->state = CircuitState::OPEN;
            echo "Circuit breaker OPEN after {$this->failureCount} failures";
        }
        
        if ($this->state === CircuitState::HALF_OPEN) {
            // Failed during recovery
            $this->state = CircuitState::OPEN;
            $this->successCount = 0;
            echo "Circuit breaker reopened - recovery failed";
        }
    }
}

// Usage with API client
class ResilientAPIClient
{
    public function __construct()
    {
        $this->api = new GitHubClient();
        $this->circuitBreaker = new CircuitBreaker(
            failureThreshold: 3,
            timeout: 30,
            successThreshold: 2
        );
    }
    
    protected function getRepository(string $org, string $repo): mixed
    {
        // Get repository with circuit breaker protection
        return $this->circuitBreaker->call(
            fn() => $this->api->getRepo($org, $repo)
        );
    }
}
```

**Exercise 3.10**: Implement circuit breaker
```php
<?php
declare(strict_types=1);

// TODO: Create API client with circuit breaker
// TODO: Simulate API failures
// TODO: Verify circuit breaker opens after threshold
// TODO: Test recovery after timeout
```

---

## Part 6: Certification & Next Steps (10 minutes)

### Final Assessment Project

**Project**: Create a production-ready automation script that demonstrates mastery of all advanced features.

**Requirements**:
1. ✅ Use CLI Framework for consistent interface
2. ✅ Implement comprehensive audit logging
3. ✅ Add multi-level error recovery with checkpointing
4. ✅ Use transaction management for atomic operations
5. ✅ Implement API caching and circuit breaker
6. ✅ Add comprehensive security validation
7. ✅ Track detailed metrics
8. ✅ Generate compliance reports
9. ✅ Optimize for performance (parallel processing)
10. ✅ Include complete documentation

**Evaluation Criteria**:
- Code quality and organization (20%)
- Proper library integration (20%)
- Error handling and resilience (20%)
- Security implementation (15%)
- Performance optimization (10%)
- Documentation (10%)
- Testing coverage (5%)

**Passing Score**: 80% (160/200 points)

---

### Certification

Upon successful completion of the assessment project:

**You will receive**:
- ✅ MokoStandards Enterprise Libraries Certified Developer certificate
- ✅ Digital badge for GitHub profile
- ✅ Listed in team developer registry
- ✅ Access to advanced workshops

**Next Steps**:
1. Complete final assessment project
2. Submit pull request for review
3. Present your solution to the team
4. Receive certification upon approval

---

### Advanced Topics for Further Learning

**1. Custom Library Extensions**
- Creating custom plugins
- Extending existing libraries
- Building domain-specific libraries

**2. Distributed Automation**
- Multi-organization management
- Distributed transaction coordination
- Cross-system saga patterns

**3. Advanced Monitoring**
- Custom Prometheus exporters
- Grafana dashboard creation
- Alert rule configuration

**4. Performance Tuning**
- Profiling automation scripts
- Database query optimization
- API call optimization

**5. Security Hardening**
- Security scanning automation
- Vulnerability management
- Secrets management integration

---

## Session Summary

### What We Covered

✅ **Advanced Error Recovery**
- Multi-level retry strategies
- Checkpoint-based state recovery
- Dead letter queue pattern

✅ **Transaction Management**
- Nested transactions
- Compensating transactions
- Saga pattern for distributed operations

✅ **Performance Optimization**
- API caching strategies
- Batch processing optimization
- Memory-efficient processing

✅ **Security & Compliance**
- Multi-layer security validation
- Comprehensive audit reporting
- Compliance metrics

✅ **Advanced API Features**
- Circuit breaker implementation
- Rate limiting strategies
- Resilient API patterns

---

### Key Takeaways

1. **Resilience is key** - Implement multiple layers of error recovery
2. **Think transactionally** - Use compensating actions for rollback
3. **Optimize strategically** - Profile first, optimize bottlenecks
4. **Security is non-negotiable** - Validate at every layer
5. **Audit everything** - Compliance requires comprehensive logging

---

## Additional Resources

- **Source Code**: Review advanced examples in `/scripts/lib/`
- **Tests**: Study test patterns in `/.github/workflows/`
- **Documentation**: Deep dive into `/docs/automation/`
- **Community**: Join #mokostds-advanced on Slack

---

## Feedback

Please complete the training feedback survey:
- What worked well?
- What could be improved?
- Topics for future sessions?
- Rate overall training experience

**Contact**: training@mokoconsulting.tech

---

**Congratulations on completing the MokoStandards Enterprise Libraries Training Program!**

You now have the skills to build production-grade, enterprise-ready automation scripts using the full MokoStandards library ecosystem.

**Ready to get certified?** → Submit your assessment project for review!
