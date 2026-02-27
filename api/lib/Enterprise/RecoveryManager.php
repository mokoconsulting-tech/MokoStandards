<?php

declare(strict_types=1);

/**
 * Recovery Manager - High-level manager for recovery operations
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * @package MokoStandards\Enterprise
 * @version 04.00.03
 * @author MokoStandards Team
 * @license GPL-3.0-or-later
 */

namespace MokoStandards\Enterprise;

use DateTime;
use DateTimeZone;

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
