<?php

declare(strict_types=1);

/**
 * API Client Library - Rate-limited, resilient API interactions.
 *
 * This class provides enterprise-grade API client capabilities with:
 * - Automatic rate limiting with backoff
 * - Retry logic with exponential backoff
 * - Request tracking and throttling
 * - Response caching
 * - Circuit breaker pattern
 * - Health monitoring
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
use GuzzleHttp\Client;
use GuzzleHttp\Exception\GuzzleException;
use GuzzleHttp\Exception\RequestException;
use Psr\Cache\CacheItemPoolInterface;
use Psr\Log\LoggerInterface;
use RuntimeException;
use Symfony\Component\Cache\Adapter\FilesystemAdapter;

/**
 * Circuit breaker states.
 */
enum CircuitState: string
{
    case CLOSED = 'closed';        // Normal operation
    case OPEN = 'open';            // Failures exceeded threshold, blocking requests
    case HALF_OPEN = 'half_open';  // Testing if service recovered
}

/**
 * Exception raised when rate limit is exceeded.
 */
class RateLimitExceeded extends RuntimeException
{
}

/**
 * Exception raised when circuit breaker is open.
 */
class CircuitBreakerOpen extends RuntimeException
{
}

/**
 * Enterprise API client with rate limiting, retry logic, and circuit breaker.
 *
 * Features:
 * - Rate limiting with configurable limits
 * - Exponential backoff retry
 * - Response caching with TTL
 * - Circuit breaker pattern
 * - Request tracking and metrics
 *
 * Example:
 * ```php
 * $client = new ApiClient(
 *     baseUrl: 'https://api.github.com',
 *     authToken: $token,
 *     maxRequestsPerHour: 5000
 * );
 * $response = $client->get('/repos/owner/repo');
 * ```
 */
class ApiClient
{
    private Client $httpClient;
    private string $baseUrl;
    private ?string $authToken;
    private int $maxRequestsPerHour;
    private int $maxRetries;
    private float $retryBackoffFactor;
    private int $cacheTtlSeconds;
    private int $circuitBreakerThreshold;
    private int $circuitBreakerTimeout;
    private bool $enableCaching;
    private string $userAgent;

    /** @var array<int> Request timestamps for rate limiting */
    private array $requestTimestamps = [];

    /** @var CacheItemPoolInterface Response cache */
    private CacheItemPoolInterface $cache;

    /** Circuit breaker state */
    private CircuitState $circuitState = CircuitState::CLOSED;

    /** Circuit breaker failure count */
    private int $circuitFailureCount = 0;

    /** Circuit breaker last failure time */
    private ?DateTime $circuitLastFailure = null;

    /** @var array<string, mixed> Request metrics */
    private array $metrics = [
        'total_requests' => 0,
        'successful_requests' => 0,
        'failed_requests' => 0,
        'cache_hits' => 0,
        'cache_misses' => 0,
        'rate_limit_waits' => 0,
        'circuit_breaker_trips' => 0,
    ];

    public const VERSION = '04.00.00';

    /**
     * Initialize API client.
     *
     * @param string $baseUrl Base URL for API (e.g., 'https://api.github.com')
     * @param string|null $authToken Authentication token (optional)
     * @param int $maxRequestsPerHour Maximum requests per hour
     * @param int $maxRetries Maximum retry attempts for failed requests
     * @param float $retryBackoffFactor Exponential backoff factor
     * @param int $cacheTtlSeconds Cache time-to-live in seconds
     * @param int $circuitBreakerThreshold Failures before opening circuit
     * @param int $circuitBreakerTimeout Seconds before attempting recovery
     * @param bool $enableCaching Enable response caching
     * @param string $userAgent User agent string
     * @param LoggerInterface|null $logger Optional logger
     */
    public function __construct(
        string $baseUrl,
        ?string $authToken = null,
        int $maxRequestsPerHour = 5000,
        int $maxRetries = 3,
        float $retryBackoffFactor = 2.0,
        int $cacheTtlSeconds = 300,
        int $circuitBreakerThreshold = 5,
        int $circuitBreakerTimeout = 60,
        bool $enableCaching = true,
        string $userAgent = 'MokoStandards-APIClient/1.0',
        ?LoggerInterface $logger = null
    ) {
        $this->baseUrl = rtrim($baseUrl, '/');
        $this->authToken = $authToken;
        $this->maxRequestsPerHour = $maxRequestsPerHour;
        $this->maxRetries = $maxRetries;
        $this->retryBackoffFactor = $retryBackoffFactor;
        $this->cacheTtlSeconds = $cacheTtlSeconds;
        $this->circuitBreakerThreshold = $circuitBreakerThreshold;
        $this->circuitBreakerTimeout = $circuitBreakerTimeout;
        $this->enableCaching = $enableCaching;
        $this->userAgent = $userAgent;

        // Initialize HTTP client
        $this->httpClient = new Client([
            'base_uri' => $this->baseUrl,
            'timeout' => 30,
            'headers' => [
                'User-Agent' => $this->userAgent,
                'Accept' => 'application/json',
            ],
        ]);

        // Initialize cache
        $cacheDir = sys_get_temp_dir() . '/mokostandards/api_cache';
        $this->cache = new FilesystemAdapter('api_client', $this->cacheTtlSeconds, $cacheDir);
    }

    /**
     * Perform GET request.
     *
     * @param string $endpoint API endpoint
     * @param array<string, mixed> $params Query parameters
     * @return array<string, mixed> Response data
     * @throws RateLimitExceeded
     * @throws CircuitBreakerOpen
     */
    public function get(string $endpoint, array $params = []): array
    {
        return $this->request('GET', $endpoint, ['query' => $params]);
    }

    /**
     * Perform POST request.
     *
     * @param string $endpoint API endpoint
     * @param array<string, mixed> $data Request body data
     * @return array<string, mixed> Response data
     * @throws RateLimitExceeded
     * @throws CircuitBreakerOpen
     */
    public function post(string $endpoint, array $data = []): array
    {
        return $this->request('POST', $endpoint, ['json' => $data]);
    }

    /**
     * Perform PUT request.
     *
     * @param string $endpoint API endpoint
     * @param array<string, mixed> $data Request body data
     * @return array<string, mixed> Response data
     * @throws RateLimitExceeded
     * @throws CircuitBreakerOpen
     */
    public function put(string $endpoint, array $data = []): array
    {
        return $this->request('PUT', $endpoint, ['json' => $data]);
    }

    /**
     * Perform DELETE request.
     *
     * @param string $endpoint API endpoint
     * @return array<string, mixed> Response data
     * @throws RateLimitExceeded
     * @throws CircuitBreakerOpen
     */
    public function delete(string $endpoint): array
    {
        return $this->request('DELETE', $endpoint);
    }

    /**
     * Perform HTTP request with rate limiting, caching, and resilience.
     *
     * @param string $method HTTP method
     * @param string $endpoint API endpoint
     * @param array<string, mixed> $options Request options
     * @return array<string, mixed> Response data
     * @throws RateLimitExceeded
     * @throws CircuitBreakerOpen
     */
    private function request(string $method, string $endpoint, array $options = []): array
    {
        $this->metrics['total_requests']++;

        // Check circuit breaker
        $this->checkCircuitBreaker();

        // Generate cache key
        $cacheKey = $this->getCacheKey($method, $endpoint, $options);

        // Check cache for GET requests
        if ($method === 'GET' && $this->enableCaching) {
            $cachedItem = $this->cache->getItem($cacheKey);
            if ($cachedItem->isHit()) {
                $this->metrics['cache_hits']++;
                return $cachedItem->get();
            }
            $this->metrics['cache_misses']++;
        }

        // Check rate limit
        $this->checkRateLimit();

        // Add authentication
        if ($this->authToken) {
            $options['headers']['Authorization'] = 'Bearer ' . $this->authToken;
        }

        // Perform request with retry logic
        $response = $this->requestWithRetry($method, $endpoint, $options);

        // Cache successful GET responses
        if ($method === 'GET' && $this->enableCaching) {
            $cachedItem = $this->cache->getItem($cacheKey);
            $cachedItem->set($response);
            $cachedItem->expiresAfter($this->cacheTtlSeconds);
            $this->cache->save($cachedItem);
        }

        return $response;
    }

    /**
     * Perform request with exponential backoff retry.
     *
     * @param string $method HTTP method
     * @param string $endpoint API endpoint
     * @param array<string, mixed> $options Request options
     * @return array<string, mixed> Response data
     * @throws RuntimeException
     */
    private function requestWithRetry(string $method, string $endpoint, array $options): array
    {
        $attempt = 0;
        $lastException = null;

        while ($attempt < $this->maxRetries) {
            try {
                $response = $this->httpClient->request($method, $endpoint, $options);
                $body = (string) $response->getBody();
                $data = json_decode($body, true, 512, JSON_THROW_ON_ERROR);

                $this->metrics['successful_requests']++;
                $this->recordSuccess();

                return $data;
            } catch (GuzzleException $e) {
                $lastException = $e;
                $attempt++;

                if ($attempt < $this->maxRetries) {
                    $waitTime = $this->retryBackoffFactor ** $attempt;
                    usleep((int) ($waitTime * 1000000));
                }

                $this->recordFailure();
            }
        }

        $this->metrics['failed_requests']++;
        throw new RuntimeException(
            "Request failed after {$this->maxRetries} attempts: " . ($lastException?->getMessage() ?? 'Unknown error')
        );
    }

    /**
     * Check and enforce rate limit.
     *
     * @throws RateLimitExceeded
     */
    private function checkRateLimit(): void
    {
        $now = time();
        $oneHourAgo = $now - 3600;

        // Remove old timestamps
        $this->requestTimestamps = array_filter(
            $this->requestTimestamps,
            fn($ts) => $ts > $oneHourAgo
        );

        // Check if limit exceeded
        if (count($this->requestTimestamps) >= $this->maxRequestsPerHour) {
            $oldestTimestamp = min($this->requestTimestamps);
            $waitTime = 3600 - ($now - $oldestTimestamp);

            $this->metrics['rate_limit_waits']++;
            
            throw new RateLimitExceeded(
                "Rate limit of {$this->maxRequestsPerHour} requests/hour exceeded. Wait {$waitTime} seconds."
            );
        }

        // Record this request
        $this->requestTimestamps[] = $now;
    }

    /**
     * Check circuit breaker state.
     *
     * @throws CircuitBreakerOpen
     */
    public function checkCircuitBreaker(): void
    {
        if ($this->circuitState === CircuitState::CLOSED) {
            return;
        }

        if ($this->circuitState === CircuitState::OPEN) {
            $now = new DateTime('now', new DateTimeZone('UTC'));
            $timeSinceFailure = $now->getTimestamp() - $this->circuitLastFailure?->getTimestamp();

            if ($timeSinceFailure >= $this->circuitBreakerTimeout) {
                // Try half-open state
                $this->circuitState = CircuitState::HALF_OPEN;
                $this->circuitFailureCount = 0;
            } else {
                throw new CircuitBreakerOpen(
                    "Circuit breaker is open. Service unavailable. Retry in " .
                    ($this->circuitBreakerTimeout - $timeSinceFailure) . " seconds."
                );
            }
        }
    }

    /**
     * Record successful request for circuit breaker.
     */
    private function recordSuccess(): void
    {
        if ($this->circuitState === CircuitState::HALF_OPEN) {
            // Service recovered, close circuit
            $this->circuitState = CircuitState::CLOSED;
            $this->circuitFailureCount = 0;
        }
    }

    /**
     * Record failed request for circuit breaker.
     */
    private function recordFailure(): void
    {
        $this->circuitFailureCount++;
        $this->circuitLastFailure = new DateTime('now', new DateTimeZone('UTC'));

        if ($this->circuitFailureCount >= $this->circuitBreakerThreshold) {
            $this->circuitState = CircuitState::OPEN;
            $this->metrics['circuit_breaker_trips']++;
        }
    }

    /**
     * Generate cache key for request.
     *
     * @param string $method HTTP method
     * @param string $endpoint API endpoint
     * @param array<string, mixed> $options Request options
     * @return string Cache key
     */
    private function getCacheKey(string $method, string $endpoint, array $options): string
    {
        $key = $method . '_' . $endpoint;
        if (isset($options['query'])) {
            $key .= '_' . http_build_query($options['query']);
        }
        return md5($key);
    }

    /**
     * Get current metrics.
     *
     * @return array<string, mixed> Metrics data
     */
    public function getMetrics(): array
    {
        return array_merge($this->metrics, [
            'circuit_state' => $this->circuitState->value,
            'circuit_failure_count' => $this->circuitFailureCount,
            'rate_limit_remaining' => max(0, $this->maxRequestsPerHour - count($this->requestTimestamps)),
        ]);
    }

    /**
     * Get current circuit breaker state.
     *
     * @return string Circuit state ('CLOSED', 'OPEN', or 'HALF_OPEN')
     */
    public function getCircuitState(): string
    {
        return strtoupper($this->circuitState->value);
    }

    /**
     * Simulate a failure for testing circuit breaker functionality.
     * This method is intended for testing only.
     *
     * @throws RuntimeException Always throws to simulate failure
     */
    public function simulateFailure(): void
    {
        $this->recordFailure();
        throw new RuntimeException('Simulated failure for circuit breaker testing');
    }

    /**
     * Reset circuit breaker to closed state.
     */
    public function resetCircuitBreaker(): void
    {
        $this->circuitState = CircuitState::CLOSED;
        $this->circuitFailureCount = 0;
        $this->circuitLastFailure = null;
    }

    /**
     * Clear response cache.
     */
    public function clearCache(): void
    {
        $this->cache->clear();
    }
}
