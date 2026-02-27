<?php

declare(strict_types=1);

/**
 * Checkpoint Manager - Manages checkpoints for recovery operations
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
use Throwable;

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

    public const VERSION = '04.00.03';

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
