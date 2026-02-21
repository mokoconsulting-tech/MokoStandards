<?php

declare(strict_types=1);

/**
 * Error Recovery Framework - Backward compatibility file
 *
 * This file now serves as a backward compatibility layer.
 * Classes have been split into separate files following PSR-4 standards:
 * - RecoveryError.php
 * - CheckpointManager.php
 * - RetryHelper.php
 * - RecoveryManager.php
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * @package MokoStandards\Enterprise
 * @version 04.00.03
 * @author MokoStandards Team
 * @license GPL-3.0-or-later
 * @deprecated Individual class files should be used instead
 */

namespace MokoStandards\Enterprise;

use Throwable;

// For backward compatibility, ensure classes are loaded
require_once __DIR__ . '/RecoveryError.php';
require_once __DIR__ . '/CheckpointManager.php';
require_once __DIR__ . '/RetryHelper.php';
require_once __DIR__ . '/RecoveryManager.php';

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
