<?php

declare(strict_types=1);

/**
 * Enterprise Audit Library - Structured audit logging for all operations.
 *
 * This class provides enterprise-grade audit logging capabilities with:
 * - Structured JSON logging to audit database
 * - Transaction ID tracking across operations
 * - Security event logging (who, what, when, where)
 * - Audit log rotation and archival
 * - Compliance reporting capabilities
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * @package MokoStandards\Enterprise
 * @version 03.02.00
 * @author MokoStandards Team
 * @license GPL-3.0-or-later
 */

namespace MokoStandards\Enterprise;

use DateTime;
use DateTimeZone;
use RuntimeException;

/**
 * Enterprise audit logger with transaction tracking and structured logging.
 *
 * Features:
 * - Transaction ID tracking
 * - Security event logging
 * - Structured JSON output
 * - Automatic log rotation
 * - Context manager support
 *
 * Example:
 * ```php
 * $logger = new AuditLogger('version_bump');
 * $transaction = $logger->startTransaction('bump_version');
 * $transaction->logEvent('version_change', ['old' => '1.0.0', 'new' => '1.1.0']);
 * $transaction->logSecurityEvent('file_modified', ['file' => 'README.md']);
 * $transaction->end();
 * ```
 */
class AuditLogger
{
    /** @var string Service name */
    private string $service;

    /** @var string User performing actions */
    private string $user;

    /** @var string Directory for audit logs */
    private string $logDir;

    /** @var bool Enable console output */
    private bool $enableConsole;

    /** @var bool Enable file logging */
    private bool $enableFile;

    /** @var int Maximum log file size in MB */
    private int $maxLogSizeMb;

    /** @var int Days to retain audit logs */
    private int $retentionDays;

    /** @var string Session ID */
    private string $sessionId;

    /** @var array Transaction stack */
    private array $transactionStack = [];

    /** @var string Version constant */
    public const VERSION = '03.02.00';

    /**
     * Initialize audit logger.
     *
     * @param string $service Service name (e.g., 'version_bump', 'branch_cleanup')
     * @param string|null $logDir Directory for audit logs (default: logs/audit/)
     * @param string|null $user Username for audit trail (default: from environment)
     * @param bool $enableConsole Output to console (default: true)
     * @param bool $enableFile Write to file (default: true)
     * @param int $maxLogSizeMb Maximum log file size before rotation
     * @param int $retentionDays Days to retain audit logs
     */
    public function __construct(
        string $service,
        ?string $logDir = null,
        ?string $user = null,
        bool $enableConsole = true,
        bool $enableFile = true,
        int $maxLogSizeMb = 10,
        int $retentionDays = 90
    ) {
        $this->service = $service;
        $this->enableConsole = $enableConsole;
        $this->enableFile = $enableFile;
        $this->maxLogSizeMb = $maxLogSizeMb;
        $this->retentionDays = $retentionDays;

        // Determine user
        $this->user = $user ?? $_SERVER['USER'] ?? $_SERVER['USERNAME'] ?? posix_getpwuid(posix_geteuid())['name'] ?? 'unknown';

        // Set up log directory
        if ($logDir === null) {
            // Default to logs/audit/ in repository root
            $repoRoot = dirname(__DIR__, 3);
            $this->logDir = $repoRoot . '/logs/audit';
        } else {
            $this->logDir = $logDir;
        }

        // Create log directory if it doesn't exist
        if ($this->enableFile && !is_dir($this->logDir)) {
            if (!mkdir($this->logDir, 0755, true) && !is_dir($this->logDir)) {
                throw new RuntimeException("Failed to create log directory: {$this->logDir}");
            }
        }

        // Session ID for this logger instance
        $this->sessionId = $this->generateSessionId();

        // Log session start
        $this->logSystemEvent('session_start', [
            'service' => $this->service,
            'user' => $this->user,
            'session_id' => $this->sessionId,
        ]);
    }

    /**
     * Generate unique session ID.
     *
     * @return string Session ID
     */
    private function generateSessionId(): string
    {
        $timestamp = (new DateTime('now', new DateTimeZone('UTC')))->format('Ymd_His');
        $uniqueId = substr(bin2hex(random_bytes(4)), 0, 8);
        return "{$timestamp}_{$uniqueId}";
    }

    /**
     * Generate unique transaction ID.
     *
     * @return string Transaction ID (UUID v4)
     */
    private function generateTransactionId(): string
    {
        return sprintf(
            '%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
            mt_rand(0, 0xffff),
            mt_rand(0, 0xffff),
            mt_rand(0, 0xffff),
            mt_rand(0, 0x0fff) | 0x4000,
            mt_rand(0, 0x3fff) | 0x8000,
            mt_rand(0, 0xffff),
            mt_rand(0, 0xffff),
            mt_rand(0, 0xffff)
        );
    }

    /**
     * Get current log file path with rotation support.
     *
     * @return string Log file path
     */
    private function getLogFilePath(): string
    {
        $dateStr = (new DateTime('now', new DateTimeZone('UTC')))->format('Ymd');
        return "{$this->logDir}/audit_{$this->service}_{$dateStr}.jsonl";
    }

    /**
     * Check if log file should be rotated based on size.
     *
     * @param string $logFile Log file path
     * @return bool True if should rotate
     */
    private function shouldRotateLog(string $logFile): bool
    {
        if (!file_exists($logFile)) {
            return false;
        }

        $sizeMb = filesize($logFile) / (1024 * 1024);
        return $sizeMb >= $this->maxLogSizeMb;
    }

    /**
     * Rotate log file if it exceeds size limit.
     *
     * @param string $logFile Log file path
     */
    private function rotateLogIfNeeded(string $logFile): void
    {
        if ($this->shouldRotateLog($logFile)) {
            $timestamp = (new DateTime('now', new DateTimeZone('UTC')))->format('His');
            $rotatedFile = preg_replace('/\.jsonl$/', ".{$timestamp}.jsonl", $logFile);
            rename($logFile, $rotatedFile);
        }
    }

    /**
     * Write log entry to file and/or console.
     *
     * @param array $entry Log entry data
     */
    private function writeLogEntry(array $entry): void
    {
        // Add timestamp and session info
        $entry['timestamp'] = (new DateTime('now', new DateTimeZone('UTC')))->format('c');
        $entry['session_id'] = $this->sessionId;
        $entry['service'] = $this->service;
        $entry['user'] = $this->user;

        // Console output
        if ($this->enableConsole) {
            $jsonOutput = json_encode($entry, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
            echo "[AUDIT] {$jsonOutput}\n";
        }

        // File output
        if ($this->enableFile) {
            $logFile = $this->getLogFilePath();
            $this->rotateLogIfNeeded($logFile);

            $jsonLine = json_encode($entry, JSON_UNESCAPED_SLASHES) . "\n";
            file_put_contents($logFile, $jsonLine, FILE_APPEND | LOCK_EX);
        }
    }

    /**
     * Log a system event.
     *
     * @param string $eventType Type of system event
     * @param array $data Event data
     */
    private function logSystemEvent(string $eventType, array $data = []): void
    {
        $entry = [
            'event_type' => 'system',
            'event_subtype' => $eventType,
            'data' => $data,
        ];
        $this->writeLogEntry($entry);
    }

    /**
     * Start a new transaction.
     *
     * @param string $operation Operation name
     * @param array $context Additional context data
     * @return AuditTransaction Transaction object
     */
    public function startTransaction(string $operation, array $context = []): AuditTransaction
    {
        $transactionId = $this->generateTransactionId();
        $transaction = new AuditTransaction($this, $transactionId, $operation, $context);
        $this->transactionStack[] = $transactionId;
        return $transaction;
    }

    /**
     * End a transaction.
     *
     * @param string $transactionId Transaction ID to end
     */
    public function endTransaction(string $transactionId): void
    {
        $key = array_search($transactionId, $this->transactionStack, true);
        if ($key !== false) {
            unset($this->transactionStack[$key]);
        }
    }

    /**
     * Log an event within a transaction.
     *
     * @param string $transactionId Transaction ID
     * @param string $eventType Event type
     * @param array $data Event data
     */
    public function logEvent(string $transactionId, string $eventType, array $data = []): void
    {
        $entry = [
            'event_type' => 'audit',
            'transaction_id' => $transactionId,
            'event_subtype' => $eventType,
            'data' => $data,
        ];
        $this->writeLogEntry($entry);
    }

    /**
     * Log a security event.
     *
     * @param string $transactionId Transaction ID
     * @param string $eventType Security event type
     * @param array $data Event data
     */
    public function logSecurityEvent(string $transactionId, string $eventType, array $data = []): void
    {
        $entry = [
            'event_type' => 'security',
            'transaction_id' => $transactionId,
            'event_subtype' => $eventType,
            'severity' => $data['severity'] ?? 'medium',
            'data' => $data,
        ];
        $this->writeLogEntry($entry);
    }
}

/**
 * Audit transaction context manager.
 */
class AuditTransaction
{
    private AuditLogger $logger;
    private string $transactionId;
    private string $operation;
    private array $context;
    private float $startTime;

    public function __construct(
        AuditLogger $logger,
        string $transactionId,
        string $operation,
        array $context = []
    ) {
        $this->logger = $logger;
        $this->transactionId = $transactionId;
        $this->operation = $operation;
        $this->context = $context;
        $this->startTime = microtime(true);

        // Log transaction start
        $this->logger->logEvent($this->transactionId, 'transaction_start', [
            'operation' => $this->operation,
            'context' => $this->context,
        ]);
    }

    /**
     * Get the transaction ID.
     *
     * @return string Transaction ID
     */
    public function getTransactionId(): string
    {
        return $this->transactionId;
    }

    /**
     * Log an event within this transaction.
     *
     * @param string $eventType Event type
     * @param array $data Event data
     */
    public function logEvent(string $eventType, array $data = []): void
    {
        $this->logger->logEvent($this->transactionId, $eventType, $data);
    }

    /**
     * Log a security event within this transaction.
     *
     * @param string $eventType Security event type
     * @param array $data Event data
     */
    public function logSecurityEvent(string $eventType, array $data = []): void
    {
        $this->logger->logSecurityEvent($this->transactionId, $eventType, $data);
    }

    /**
     * End the transaction.
     *
     * @param string|null $status Transaction status (success|failure)
     * @param array $result Transaction result data
     */
    public function end(?string $status = 'success', array $result = []): void
    {
        $duration = microtime(true) - $this->startTime;

        $this->logger->logEvent($this->transactionId, 'transaction_end', [
            'operation' => $this->operation,
            'status' => $status,
            'duration_seconds' => round($duration, 3),
            'result' => $result,
        ]);

        $this->logger->endTransaction($this->transactionId);
    }
}
