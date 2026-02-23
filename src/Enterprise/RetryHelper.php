<?php

declare(strict_types=1);

/**
 * Retry Helper - Retry execution with exponential backoff
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

use Exception;
use Throwable;

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
