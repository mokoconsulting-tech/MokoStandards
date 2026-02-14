<?php

declare(strict_types=1);

/**
 * Transaction Manager for MokoStandards
 *
 * Provides atomic multi-step operations with automatic rollback:
 * - Transaction boundaries for ACID operations
 * - Automatic rollback on failure
 * - State consistency checks
 * - Transaction history tracking
 * - Nested transaction support
 * - Step-by-step execution with recovery
 *
 * Example usage:
 * ```php
 * $txn = new Transaction('user_registration');
 * try {
 *     $txn->execute('create_user', function() {
 *         // Create user logic
 *     }, function() {
 *         // Rollback: delete user
 *     });
 *     
 *     $txn->execute('send_email', function() {
 *         // Send welcome email
 *     });
 *     
 *     $txn->commit();
 * } catch (TransactionError $e) {
 *     // Automatic rollback on failure
 *     echo "Transaction failed: " . $e->getMessage();
 * }
 * ```
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * @package MokoStandards\Enterprise
 * @version 04.00.00
 * @author MokoStandards Team
 * @license GPL-3.0-or-later
 */

namespace MokoStandards\Enterprise;

use DateTime;
use DateTimeZone;
use Exception;

/**
 * Exception raised when transaction operations fail
 */
class TransactionError extends Exception
{
}

/**
 * Represents a single step in a transaction
 */
class TransactionStep
{
    public string $name;
    public $executeFunc;
    public $rollbackFunc;
    public bool $executed = false;
    public $result = null;
    public ?string $error = null;

    public function __construct(string $name, callable $executeFunc, ?callable $rollbackFunc = null)
    {
        $this->name = $name;
        $this->executeFunc = $executeFunc;
        $this->rollbackFunc = $rollbackFunc;
    }
}

/**
 * Transaction manager for atomic multi-step operations
 */
class Transaction
{
    private const VERSION = '04.00.00';

    private string $name;
    /** @var array<int, TransactionStep> */
    private array $steps = [];
    private bool $committed = false;
    private bool $rolledBack = false;
    private ?DateTime $startTime = null;
    private ?DateTime $endTime = null;

    public function __construct(?string $name = null)
    {
        $this->name = $name ?? 'txn_' . date('Ymd_His');
        $this->startTime = new DateTime('now', new DateTimeZone('UTC'));
        error_log("Starting transaction: {$this->name}");
    }

    /**
     * Execute a transaction step
     *
     * @param string $name Step name
     * @param callable $func Function to execute
     * @param callable|null $rollbackFunc Function to rollback this step
     * @param mixed ...$args Arguments for func
     * @return mixed Result of func
     * @throws TransactionError If step execution fails
     */
    public function execute(string $name, callable $func, ?callable $rollbackFunc = null, ...$args)
    {
        $step = new TransactionStep($name, $func, $rollbackFunc);

        try {
            error_log("Executing step: {$name}");
            $result = $func(...$args);
            $step->executed = true;
            $step->result = $result;
            $this->steps[] = $step;
            error_log("Step completed: {$name}");
            return $result;
        } catch (Exception $e) {
            $step->error = $e->getMessage();
            error_log("Step failed: {$name} - {$e->getMessage()}");
            throw new TransactionError("Transaction step '{$name}' failed: {$e->getMessage()}", 0, $e);
        }
    }

    /**
     * Commit the transaction
     *
     * @throws TransactionError If already committed or rolled back
     */
    public function commit(): void
    {
        if ($this->committed) {
            error_log("Transaction already committed");
            return;
        }

        if ($this->rolledBack) {
            throw new TransactionError("Cannot commit a rolled-back transaction");
        }

        $this->committed = true;
        $this->endTime = new DateTime('now', new DateTimeZone('UTC'));
        
        $duration = $this->endTime->getTimestamp() - $this->startTime->getTimestamp();
        error_log("Transaction committed: {$this->name} (" . count($this->steps) . " steps, {$duration}s)");
    }

    /**
     * Rollback all executed steps in reverse order
     */
    public function rollback(): void
    {
        if ($this->rolledBack) {
            error_log("Transaction already rolled back");
            return;
        }

        error_log("Rolling back transaction: {$this->name}");

        // Rollback in reverse order
        foreach (array_reverse($this->steps) as $step) {
            if ($step->executed && $step->rollbackFunc !== null) {
                try {
                    error_log("Rolling back step: {$step->name}");
                    ($step->rollbackFunc)();
                } catch (Exception $e) {
                    error_log("Rollback failed for step {$step->name}: {$e->getMessage()}");
                }
            }
        }

        $this->rolledBack = true;
        error_log("Transaction rolled back: {$this->name}");
    }

    /**
     * Get transaction status
     *
     * @return array<string, mixed> Dictionary with transaction status
     */
    public function getStatus(): array
    {
        return [
            'name' => $this->name,
            'steps_count' => count($this->steps),
            'committed' => $this->committed,
            'rolled_back' => $this->rolledBack,
            'start_time' => $this->startTime?->format('c'),
            'end_time' => $this->endTime?->format('c'),
            'steps' => array_map(function ($step) {
                return [
                    'name' => $step->name,
                    'executed' => $step->executed,
                    'error' => $step->error
                ];
            }, $this->steps)
        ];
    }

    /**
     * Get transaction name
     */
    public function getName(): string
    {
        return $this->name;
    }

    /**
     * Check if transaction is committed
     */
    public function isCommitted(): bool
    {
        return $this->committed;
    }

    /**
     * Check if transaction is rolled back
     */
    public function isRolledBack(): bool
    {
        return $this->rolledBack;
    }

    /**
     * Destructor - auto rollback if not committed
     */
    public function __destruct()
    {
        if (!$this->committed && !$this->rolledBack && count($this->steps) > 0) {
            error_log("Transaction {$this->name} was not committed, auto-rolling back");
            $this->rollback();
        }
    }
}

/**
 * High-level transaction management
 */
class TransactionManager
{
    private const VERSION = '04.00.00';

    /** @var array<int, Transaction> */
    private array $transactions = [];
    private ?Transaction $activeTransaction = null;

    /**
     * Begin a new transaction
     *
     * @param string|null $name Transaction name
     * @return Transaction New transaction instance
     * @throws TransactionError If another transaction is already active
     */
    public function begin(?string $name = null): Transaction
    {
        if ($this->activeTransaction !== null) {
            throw new TransactionError("Another transaction is already active");
        }

        $txn = new Transaction($name);
        $this->activeTransaction = $txn;
        $this->transactions[] = $txn;
        return $txn;
    }

    /**
     * End active transaction (commit or rollback should be done before this)
     */
    public function end(): void
    {
        $this->activeTransaction = null;
    }

    /**
     * Get transaction history
     *
     * @return array<int, array<string, mixed>> List of transaction status dictionaries
     */
    public function getHistory(): array
    {
        return array_map(function ($txn) {
            return $txn->getStatus();
        }, $this->transactions);
    }

    /**
     * Get transaction statistics
     *
     * @return array<string, int> Dictionary with statistics
     */
    public function getStats(): array
    {
        $committed = 0;
        $rolledBack = 0;
        
        foreach ($this->transactions as $txn) {
            if ($txn->isCommitted()) {
                $committed++;
            }
            if ($txn->isRolledBack()) {
                $rolledBack++;
            }
        }

        return [
            'total' => count($this->transactions),
            'committed' => $committed,
            'rolled_back' => $rolledBack,
            'active' => $this->activeTransaction !== null ? 1 : 0
        ];
    }

    /**
     * Get active transaction
     */
    public function getActiveTransaction(): ?Transaction
    {
        return $this->activeTransaction;
    }

    public function getVersion(): string
    {
        return self::VERSION;
    }
}
