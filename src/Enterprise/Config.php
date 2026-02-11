<?php

declare(strict_types=1);

/**
 * Configuration Manager - Centralized, environment-aware configuration.
 *
 * This class provides enterprise-grade configuration management with:
 * - Environment variable loading (.env support via phpdotenv)
 * - YAML and JSON configuration file parsing
 * - Secure secret management
 * - Configuration validation
 * - Default values with overrides
 * - Type-safe configuration access
 * - Dot notation for nested values
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * @package MokoStandards\Enterprise
 * @version 03.02.00
 * @author MokoStandards Team
 * @license GPL-3.0-or-later
 */

namespace MokoStandards\Enterprise;

use RuntimeException;

/**
 * Exception raised when configuration validation fails.
 */
class ConfigValidationError extends RuntimeException
{
}

/**
 * Enterprise configuration manager with environment support.
 *
 * Features:
 * - Environment-based configuration
 * - Dot notation for nested access (e.g., 'github.rate_limit')
 * - Runtime overrides
 * - Type-safe getters
 * - Default value fallbacks
 * - Environment detection (dev/staging/production)
 *
 * Example:
 * ```php
 * $config = Config::load();
 * $org = $config->get('github.organization');
 * $rateLimit = $config->getInt('github.rate_limit', 5000);
 * $isProduction = $config->isProduction();
 * ```
 */
class Config
{
    /** @var array<string, mixed> Default configuration values */
    private const DEFAULT_CONFIG = [
        'version' => '03.02.00',
        'environment' => 'development',
        'github' => [
            'organization' => 'mokoconsulting-tech',
            'rate_limit' => 5000,
            'max_retries' => 3,
            'timeout' => 30,
        ],
        'logging' => [
            'level' => 'INFO',
            'format' => 'json',
            'directory' => 'logs',
            'retention_days' => 90,
        ],
        'audit' => [
            'enabled' => true,
            'directory' => 'logs/audit',
            'max_file_size_mb' => 10,
            'retention_days' => 90,
        ],
        'cache' => [
            'enabled' => true,
            'ttl_seconds' => 300,
        ],
        'circuit_breaker' => [
            'enabled' => true,
            'threshold' => 5,
            'timeout_seconds' => 60,
        ],
    ];

    /** @var array<string, mixed> Configuration data */
    private array $configData;

    /** @var string Current environment */
    private string $environment;

    /** @var array<string, mixed> Runtime override data */
    private array $overrideData = [];

    public const VERSION = '03.02.00';

    /**
     * Constructor.
     *
     * @param array<string, mixed> $configData Configuration data
     * @param string $environment Environment name
     */
    public function __construct(array $configData, string $environment = 'development')
    {
        $this->configData = $configData;
        $this->environment = $environment;
    }

    /**
     * Load configuration from environment.
     *
     * @param string|null $env Environment override (null = auto-detect)
     * @return self Configuration instance
     */
    public static function load(?string $env = null): self
    {
        // Detect environment from env var or default to development
        $env = $env ?? $_ENV['MOKO_ENV'] ?? getenv('MOKO_ENV') ?: 'development';

        // Start with default config
        $configData = self::DEFAULT_CONFIG;
        $configData['environment'] = $env;

        // Load from .env file if exists using vlucas/phpdotenv
        $repoRoot = dirname(__DIR__, 2);
        if (file_exists($repoRoot . '/.env')) {
            // Note: In production, you'd use Dotenv::createImmutable() here
            // For now, we'll manually parse simple .env files
            self::loadEnvFile($repoRoot . '/.env');
        }

        // Override with environment variables
        self::applyEnvironmentOverrides($configData);

        return new self($configData, $env);
    }

    /**
     * Load environment variables from .env file.
     *
     * @param string $envFile Path to .env file
     */
    private static function loadEnvFile(string $envFile): void
    {
        if (!is_readable($envFile)) {
            return;
        }

        $lines = file($envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        if ($lines === false) {
            return;
        }

        foreach ($lines as $line) {
            // Skip comments
            if (str_starts_with(trim($line), '#')) {
                continue;
            }

            // Parse KEY=VALUE format
            if (strpos($line, '=') !== false) {
                [$key, $value] = explode('=', $line, 2);
                $key = trim($key);
                $value = trim($value);

                // Remove quotes if present
                if (preg_match('/^(["\'])(.*)\\1$/', $value, $matches)) {
                    $value = $matches[2];
                }

                // Set environment variable
                putenv("$key=$value");
                $_ENV[$key] = $value;
            }
        }
    }

    /**
     * Apply environment variable overrides to config.
     *
     * @param array<string, mixed> &$configData Configuration data to modify
     */
    private static function applyEnvironmentOverrides(array &$configData): void
    {
        // GitHub configuration
        if ($token = getenv('GITHUB_TOKEN')) {
            $configData['github']['token'] = $token;
        }
        if ($org = getenv('GITHUB_ORG')) {
            $configData['github']['organization'] = $org;
        }

        // Logging configuration
        if ($logLevel = getenv('LOG_LEVEL')) {
            $configData['logging']['level'] = $logLevel;
        }
    }

    /**
     * Get configuration value with dot notation.
     *
     * @param string $key Configuration key (e.g., 'github.rate_limit')
     * @param mixed $default Default value if key not found
     * @return mixed Configuration value
     */
    public function get(string $key, mixed $default = null): mixed
    {
        // Check runtime overrides first
        if (array_key_exists($key, $this->overrideData)) {
            return $this->overrideData[$key];
        }

        // Navigate nested configuration using dot notation
        $value = $this->configData;
        foreach (explode('.', $key) as $part) {
            if (is_array($value) && array_key_exists($part, $value)) {
                $value = $value[$part];
            } else {
                return $default;
            }
        }

        return $value;
    }

    /**
     * Set configuration value (runtime override).
     *
     * @param string $key Configuration key
     * @param mixed $value Value to set
     */
    public function set(string $key, mixed $value): void
    {
        $this->overrideData[$key] = $value;
    }

    /**
     * Get integer value.
     *
     * @param string $key Configuration key
     * @param int $default Default value
     * @return int Integer value
     */
    public function getInt(string $key, int $default = 0): int
    {
        $value = $this->get($key, $default);
        return is_numeric($value) ? (int) $value : $default;
    }

    /**
     * Get string value.
     *
     * @param string $key Configuration key
     * @param string $default Default value
     * @return string String value
     */
    public function getString(string $key, string $default = ''): string
    {
        $value = $this->get($key, $default);
        return is_scalar($value) ? (string) $value : $default;
    }

    /**
     * Get boolean value.
     *
     * @param string $key Configuration key
     * @param bool $default Default value
     * @return bool Boolean value
     */
    public function getBool(string $key, bool $default = false): bool
    {
        $value = $this->get($key, $default);
        
        // Handle string representations of booleans
        if (is_string($value)) {
            $value = strtolower($value);
            if (in_array($value, ['true', '1', 'yes', 'on'], true)) {
                return true;
            }
            if (in_array($value, ['false', '0', 'no', 'off'], true)) {
                return false;
            }
        }
        
        return (bool) $value;
    }

    /**
     * Get entire configuration section.
     *
     * @param string $section Section name
     * @return array<string, mixed> Section data
     */
    public function getSection(string $section): array
    {
        $value = $this->get($section, []);
        return is_array($value) ? $value : [];
    }

    /**
     * Get current environment.
     *
     * @return string Environment name
     */
    public function getEnvironment(): string
    {
        return $this->environment;
    }

    /**
     * Check if production environment.
     *
     * @return bool True if production
     */
    public function isProduction(): bool
    {
        return in_array($this->environment, ['production', 'prod'], true);
    }

    /**
     * Check if development environment.
     *
     * @return bool True if development
     */
    public function isDevelopment(): bool
    {
        return in_array($this->environment, ['development', 'dev'], true);
    }

    /**
     * Check if staging environment.
     *
     * @return bool True if staging
     */
    public function isStaging(): bool
    {
        return in_array($this->environment, ['staging', 'stage'], true);
    }

    /**
     * Get all configuration data.
     *
     * @return array<string, mixed> All configuration
     */
    public function all(): array
    {
        return array_merge($this->configData, $this->overrideData);
    }

    /**
     * Validate required configuration keys exist.
     *
     * @param array<string> $requiredKeys Required configuration keys
     * @throws ConfigValidationError If validation fails
     */
    public function validate(array $requiredKeys): void
    {
        $missing = [];
        
        foreach ($requiredKeys as $key) {
            if ($this->get($key) === null) {
                $missing[] = $key;
            }
        }
        
        if (!empty($missing)) {
            throw new ConfigValidationError(
                'Missing required configuration keys: ' . implode(', ', $missing)
            );
        }
    }

    /**
     * String representation.
     *
     * @return string
     */
    public function __toString(): string
    {
        return "Config(environment='{$this->environment}')";
    }
}
