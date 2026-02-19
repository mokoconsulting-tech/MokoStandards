<?php

declare(strict_types=1);

/**
 * Error Recovery Framework - Retry logic with exponential backoff and checkpointing.
 *
 * This class provides enterprise-grade error recovery capabilities including:
 * - Automatic retry with exponential backoff
 * - Checkpointing for long-running operations
 * - Transaction rollback on failure
 * - State recovery from checkpoints
 * - Resume capability after failures
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

use DateTime;
use DateTimeZone;
use Exception;
use RuntimeException;
use Throwable;

/**
 * Exception raised when recovery operations fail.
 */
class RecoveryError extends RuntimeException
{
}

/**
 * Manages checkpoints for recovery operations.
 *
 * Features:
 * - Save/load checkpoint state
 * - Automatic timestamp tracking
 * - Checkpoint listing and cleanup
 * - JSON-based state persistence
 *
 * Example:
 * ```php
 * $manager = new CheckpointManager('.checkpoints');
 * $manager->saveCheckpoint('operation', ['step' => 1, 'data' => 'value']);
 * $state = $manager->loadCheckpoint('operation');
 * ```
 */
class CheckpointManager
{
    private string $checkpointDir;

    public const VERSION = '04.00.01';

    /**
     * Initialize checkpoint manager.
     *
     * @param string $checkpointDir Directory to store checkpoints
     */
    public function __construct(string $checkpointDir = '.checkpoints')
    {
        $this->checkpointDir = $checkpointDir;
        
        // Create checkpoint directory if it doesn't exist
        if (!is_dir($this->checkpointDir)) {
            if (!mkdir($this->checkpointDir, 0755, true) && !is_dir($this->checkpointDir)) {
                throw new RecoveryError("Failed to create checkpoint directory: {$this->checkpointDir}");
            }
        }
    }

    /**
     * Save a checkpoint.
     *
     * @param string $name Checkpoint name
     * @param array<string, mixed> $state State to save
     * @return string Path to checkpoint file
     * @throws RecoveryError
     */
    public function saveCheckpoint(string $name, array $state): string
    {
        $timestamp = (new DateTime('now', new DateTimeZone('UTC')))->format('Ymd_His');
        $checkpointFile = "{$this->checkpointDir}/{$name}_{$timestamp}.json";

        try {
            $json = json_encode($state, JSON_PRETTY_PRINT | JSON_THROW_ON_ERROR);
            file_put_contents($checkpointFile, $json, LOCK_EX);
            error_log("Checkpoint saved: {$checkpointFile}");
            return $checkpointFile;
        } catch (Throwable $e) {
            error_log("Failed to save checkpoint: {$e->getMessage()}");
            throw new RecoveryError("Checkpoint save failed: {$e->getMessage()}");
        }
    }

    /**
     * Load the most recent checkpoint for a name.
     *
     * @param string $name Checkpoint name
     * @return array<string, mixed>|null Checkpoint state or null if not found
     */
    public function loadCheckpoint(string $name): ?array
    {
        $checkpoints = glob("{$this->checkpointDir}/{$name}_*.json");
        if ($checkpoints === false || empty($checkpoints)) {
            return null;
        }

        // Sort by filename (which includes timestamp) to get latest
        sort($checkpoints);
        $latest = end($checkpoints);

        try {
            $json = file_get_contents($latest);
            if ($json === false) {
                error_log("Failed to read checkpoint: {$latest}");
                return null;
            }

            $state = json_decode($json, true, 512, JSON_THROW_ON_ERROR);
            error_log("Checkpoint loaded: {$latest}");
            return $state;
        } catch (Throwable $e) {
            error_log("Failed to load checkpoint: {$e->getMessage()}");
            return null;
        }
    }

    /**
     * List available checkpoints.
     *
     * @param string|null $name Filter by checkpoint name (optional)
     * @return array<string> List of checkpoint file paths
     */
    public function listCheckpoints(?string $name = null): array
    {
        $pattern = $name ? "{$this->checkpointDir}/{$name}_*.json" : "{$this->checkpointDir}/*.json";
        $checkpoints = glob($pattern);
        return $checkpoints !== false ? $checkpoints : [];
    }

    /**
     * Clean up old checkpoints.
     *
     * @param string|null $name Filter by checkpoint name (optional)
     * @param int $keepLatest Number of latest checkpoints to keep
     */
    public function cleanupCheckpoints(?string $name = null, int $keepLatest = 5): void
    {
        $checkpoints = $this->listCheckpoints($name);
        sort($checkpoints);

        if (count($checkpoints) > $keepLatest) {
            $toRemove = array_slice($checkpoints, 0, -$keepLatest);
            foreach ($toRemove as $checkpoint) {
                unlink($checkpoint);
                error_log("Removed old checkpoint: {$checkpoint}");
            }
        }
    }
}

/**
 * Retry execution helper with exponential backoff.
 *
 * Features:
 * - Configurable retry attempts
 * - Exponential backoff strategy
 * - Exception filtering
 * - Retry and failure callbacks
 *
 * Example:
 * ```php
 * $retry = new RetryHelper(maxRetries: 3, backoffBase: 2.0);
 * $result = $retry->execute(function() {
 *     // Your code that might fail
 *     return $api->call();
 * });
 * ```
 */
class RetryHelper
{
    private int $maxRetries;
    private float $backoffBase;
    /** @var array<class-string<Throwable>> */
    private array $retryableExceptions;
    /** @var callable|null */
    private $onRetry;
    /** @var callable|null */
    private $onFailure;

    /**
     * Initialize retry helper.
     *
     * @param int $maxRetries Maximum number of retry attempts
     * @param float $backoffBase Base for exponential backoff (seconds)
     * @param array<class-string<Throwable>> $retryableExceptions Exceptions to catch and retry
     * @param callable|null $onRetry Callback function called on each retry
     * @param callable|null $onFailure Callback function called on final failure
     */
    public function __construct(
        int $maxRetries = 3,
        float $backoffBase = 2.0,
        array $retryableExceptions = [Exception::class],
        ?callable $onRetry = null,
        ?callable $onFailure = null
    ) {
        $this->maxRetries = $maxRetries;
        $this->backoffBase = $backoffBase;
        $this->retryableExceptions = $retryableExceptions;
        $this->onRetry = $onRetry;
        $this->onFailure = $onFailure;
    }

    /**
     * Execute callable with retry logic.
     *
     * @param callable $callable Function to execute
     * @return mixed Result of callable
     * @throws Throwable If all retries exhausted
     */
    public function execute(callable $callable): mixed
    {
        $lastException = null;

        for ($attempt = 0; $attempt < $this->maxRetries; $attempt++) {
            try {
                $result = $callable();
                
                if ($attempt > 0) {
                    error_log("Function succeeded on attempt " . ($attempt + 1));
                }
                
                return $result;
            } catch (Throwable $e) {
                // Check if this exception is retryable
                $shouldRetry = false;
                foreach ($this->retryableExceptions as $exceptionClass) {
                    if ($e instanceof $exceptionClass) {
                        $shouldRetry = true;
                        break;
                    }
                }

                if (!$shouldRetry) {
                    throw $e;
                }

                $lastException = $e;

                if ($attempt < $this->maxRetries - 1) {
                    // Calculate backoff time
                    $backoffTime = $this->backoffBase ** $attempt;
                    error_log(
                        "Function failed on attempt " . ($attempt + 1) . "/{$this->maxRetries}: {$e->getMessage()}. " .
                        "Retrying in {$backoffTime}s..."
                    );

                    // Call retry callback if provided
                    if ($this->onRetry !== null) {
                        ($this->onRetry)($attempt, $e, $backoffTime);
                    }

                    // Sleep for backoff time (convert to microseconds)
                    usleep((int) ($backoffTime * 1000000));
                } else {
                    error_log("Function failed after {$this->maxRetries} attempts: {$e->getMessage()}");

                    // Call failure callback if provided
                    if ($this->onFailure !== null) {
                        ($this->onFailure)($this->maxRetries, $e);
                    }
                }
            }
        }

        // All retries exhausted
        throw $lastException ?? new RecoveryError('All retries exhausted');
    }
}

/**
 * High-level manager for recovery operations.
 *
 * Features:
 * - Check recovery availability
 * - Recover operations from checkpoints
 * - Track recovery history
 * - Cleanup old checkpoints
 *
 * Example:
 * ```php
 * $manager = new RecoveryManager();
 * 
 * if ($manager->canRecover('my_operation')) {
 *     $state = $manager->recoverOperation('my_operation');
 *     // Resume from saved state
 * }
 * ```
 */
class RecoveryManager
{
    private CheckpointManager $checkpointManager;
    /** @var array<array<string, mixed>> */
    private array $recoveryLog = [];

    /**
     * Initialize recovery manager.
     *
     * @param string $checkpointDir Directory for checkpoints
     */
    public function __construct(string $checkpointDir = '.checkpoints')
    {
        $this->checkpointManager = new CheckpointManager($checkpointDir);
    }

    /**
     * Check if an operation can be recovered.
     *
     * @param string $operationName Name of the operation
     * @return bool True if recovery checkpoint exists
     */
    public function canRecover(string $operationName): bool
    {
        $checkpoints = $this->checkpointManager->listCheckpoints($operationName);
        return count($checkpoints) > 0;
    }

    /**
     * Recover an operation from checkpoint.
     *
     * @param string $operationName Name of the operation to recover
     * @return array<string, mixed>|null Recovered state or null
     */
    public function recoverOperation(string $operationName): ?array
    {
        error_log("Attempting to recover operation: {$operationName}");
        $state = $this->checkpointManager->loadCheckpoint($operationName);

        if ($state !== null) {
            $this->recoveryLog[] = [
                'operation' => $operationName,
                'recovered_at' => (new DateTime('now', new DateTimeZone('UTC')))->format('c'),
                'state' => $state,
            ];
            error_log("Successfully recovered operation: {$operationName}");
        } else {
            error_log("No checkpoint found for operation: {$operationName}");
        }

        return $state;
    }

    /**
     * Get recovery log.
     *
     * @return array<array<string, mixed>> List of recovery operations
     */
    public function getRecoveryLog(): array
    {
        return $this->recoveryLog;
    }

    /**
     * Clean up old checkpoints.
     *
     * @param int $keepLatest Number of latest checkpoints to keep per operation
     */
    public function cleanupOldCheckpoints(int $keepLatest = 5): void
    {
        $this->checkpointManager->cleanupCheckpoints(null, $keepLatest);
    }

    /**
     * Get checkpoint manager instance.
     *
     * @return CheckpointManager
     */
    public function getCheckpointManager(): CheckpointManager
    {
        return $this->checkpointManager;
    }
}

/**
 * Execute a callable with automatic rollback on failure.
 *
 * @param callable $operation Operation to execute
 * @param callable $rollback Rollback function to call on failure
 * @return mixed Result of operation
 * @throws Throwable Re-throws the original exception after rollback
 */
function withRollback(callable $operation, callable $rollback): mixed
{
    try {
        return $operation();
    } catch (Throwable $e) {
        error_log("Operation failed, executing rollback: {$e->getMessage()}");
        try {
            $rollback();
            error_log("Rollback completed successfully");
        } catch (Throwable $rollbackError) {
            error_log("Rollback failed: {$rollbackError->getMessage()}");
        }
        throw $e;
    }
}
