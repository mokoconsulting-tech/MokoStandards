<?php

declare(strict_types=1);

/**
 * Input Validation Library - Security-focused input validation and sanitization.
 *
 * This class provides comprehensive validation to prevent:
 * - Path traversal attacks
 * - Shell injection
 * - SQL injection
 * - XSS attacks
 * - Invalid data types
 * - Out-of-range values
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

use InvalidArgumentException;
use RuntimeException;

/**
 * Exception raised when validation fails.
 */
class ValidationError extends RuntimeException
{
}

/**
 * Input validation and sanitization utilities.
 *
 * Features:
 * - Path validation (prevent path traversal)
 * - Version format validation (semver, Moko format)
 * - Email validation
 * - URL validation with scheme checking
 * - Shell injection prevention
 * - SQL injection prevention
 * - Integer validation with range checking
 * - String validation with length/pattern checking
 * - Choice validation (enum-like)
 *
 * Example:
 * ```php
 * use MokoStandards\Enterprise\InputValidator;
 *
 * $path = InputValidator::validatePath('/tmp/file.txt');
 * $email = InputValidator::validateEmail('user@example.com');
 * $version = InputValidator::validateVersion('04.00.01', 'moko');
 * $safe = InputValidator::sanitizeShellInput('user; rm -rf /');
 * ```
 */
class InputValidator
{
    public const VERSION = '04.00.01';

    /**
     * Validate and sanitize file paths to prevent path traversal.
     *
     * @param string $path Path to validate
     * @param bool $allowRelative Allow relative paths
     * @param bool $mustExist Path must exist
     * @param array<string>|null $allowedExtensions List of allowed file extensions
     * @return string Validated path
     * @throws ValidationError If path is invalid or dangerous
     */
    public static function validatePath(
        string $path,
        bool $allowRelative = false,
        bool $mustExist = false,
        ?array $allowedExtensions = null
    ): string {
        if (empty($path)) {
            throw new ValidationError("Path must be a non-empty string");
        }

        // Check for path traversal attempts
        if (strpos($path, '..') !== false) {
            throw new ValidationError("Path traversal detected (..)");
        }

        // Resolve to absolute path if not allowing relative
        if (!$allowRelative) {
            $realPath = realpath($path);
            if ($realPath === false && $mustExist) {
                throw new ValidationError("Path does not exist: {$path}");
            }
            if ($realPath !== false) {
                $path = $realPath;
            }
        }

        // Check if path must exist
        if ($mustExist && !file_exists($path)) {
            throw new ValidationError("Path does not exist: {$path}");
        }

        // Check file extension if specified
        if ($allowedExtensions !== null) {
            $extension = pathinfo($path, PATHINFO_EXTENSION);
            if ($extension !== '') {
                $allowedLower = array_map('strtolower', $allowedExtensions);
                if (!in_array(strtolower($extension), $allowedLower, true)) {
                    throw new ValidationError(
                        "Invalid file extension: .{$extension}. " .
                        "Allowed: " . implode(', ', $allowedExtensions)
                    );
                }
            }
        }

        return $path;
    }

    /**
     * Validate version strings.
     *
     * @param string $version Version string to validate
     * @param string $formatType Version format ('semver', 'simple', 'moko')
     * @return string Validated version string
     * @throws ValidationError If version format is invalid
     */
    public static function validateVersion(string $version, string $formatType = 'semver'): string
    {
        if (empty($version)) {
            throw new ValidationError("Version must be a non-empty string");
        }

        switch ($formatType) {
            case 'semver':
                // Semantic versioning: MAJOR.MINOR.PATCH
                $pattern = '/^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$/';
                if (!preg_match($pattern, $version)) {
                    throw new ValidationError(
                        "Invalid semver format: {$version}. Expected: MAJOR.MINOR.PATCH"
                    );
                }
                break;

            case 'moko':
                // MokoStandards format: XX.YY.ZZ
                $pattern = '/^\d{2}\.\d{2}\.\d{2}$/';
                if (!preg_match($pattern, $version)) {
                    throw new ValidationError(
                        "Invalid MokoStandards version format: {$version}. Expected: XX.YY.ZZ"
                    );
                }
                break;

            case 'simple':
                // Simple format: X.Y or X.Y.Z
                $pattern = '/^\d+\.\d+(\.\d+)?$/';
                if (!preg_match($pattern, $version)) {
                    throw new ValidationError("Invalid version format: {$version}");
                }
                break;

            default:
                throw new ValidationError("Unknown version format type: {$formatType}");
        }

        return $version;
    }

    /**
     * Validate email addresses.
     *
     * @param string $email Email address to validate
     * @return string Validated email address (lowercase)
     * @throws ValidationError If email is invalid
     */
    public static function validateEmail(string $email): string
    {
        if (empty($email)) {
            throw new ValidationError("Email must be a non-empty string");
        }

        // Simple but effective email regex
        $pattern = '/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/';
        if (!preg_match($pattern, $email)) {
            throw new ValidationError("Invalid email format: {$email}");
        }

        return strtolower($email);
    }

    /**
     * Validate URLs and check schemes.
     *
     * @param string $url URL to validate
     * @param array<string>|null $allowedSchemes List of allowed URL schemes (e.g., ['http', 'https'])
     * @return string Validated URL
     * @throws ValidationError If URL is invalid
     */
    public static function validateUrl(string $url, ?array $allowedSchemes = null): string
    {
        if (empty($url)) {
            throw new ValidationError("URL must be a non-empty string");
        }

        $parsed = parse_url($url);
        if ($parsed === false || !isset($parsed['scheme']) || !isset($parsed['host'])) {
            throw new ValidationError("Invalid URL format: {$url}");
        }

        if ($allowedSchemes !== null && !in_array($parsed['scheme'], $allowedSchemes, true)) {
            throw new ValidationError(
                "URL scheme '{$parsed['scheme']}' not allowed. " .
                "Allowed: " . implode(', ', $allowedSchemes)
            );
        }

        return $url;
    }

    /**
     * Sanitize input to prevent shell injection.
     *
     * @param string $input Input string to sanitize
     * @return string Sanitized string
     */
    public static function sanitizeShellInput(string $input): string
    {
        // Remove dangerous shell characters
        $dangerousChars = [';', '&', '|', '`', '$', '(', ')', '<', '>', "\n", "\r"];
        $sanitized = str_replace($dangerousChars, '', $input);
        
        return trim($sanitized);
    }

    /**
     * Sanitize input to prevent SQL injection.
     *
     * @param string $input Input string to sanitize
     * @return string Sanitized string
     */
    public static function sanitizeSqlInput(string $input): string
    {
        // Remove SQL injection patterns
        $dangerousPatterns = ["'", '"', '--', '/*', '*/', 'xp_', 'sp_'];
        $sanitized = str_replace($dangerousPatterns, '', $input);
        
        return trim($sanitized);
    }

    /**
     * Validate and convert to integer with range checking.
     *
     * @param mixed $value Value to validate
     * @param int|null $minValue Minimum allowed value
     * @param int|null $maxValue Maximum allowed value
     * @return int Validated integer
     * @throws ValidationError If value is invalid or out of range
     */
    public static function validateInteger(
        mixed $value,
        ?int $minValue = null,
        ?int $maxValue = null
    ): int {
        if (!is_numeric($value)) {
            throw new ValidationError("Cannot convert to integer: {$value}");
        }

        $intValue = (int) $value;

        if ($minValue !== null && $intValue < $minValue) {
            throw new ValidationError("Value {$intValue} is below minimum {$minValue}");
        }

        if ($maxValue !== null && $intValue > $maxValue) {
            throw new ValidationError("Value {$intValue} is above maximum {$maxValue}");
        }

        return $intValue;
    }

    /**
     * Validate string with length and pattern checking.
     *
     * @param string $value String to validate
     * @param int|null $minLength Minimum string length
     * @param int|null $maxLength Maximum string length
     * @param string|null $pattern Regex pattern to match
     * @return string Validated string
     * @throws ValidationError If string is invalid
     */
    public static function validateString(
        string $value,
        ?int $minLength = null,
        ?int $maxLength = null,
        ?string $pattern = null
    ): string {
        $length = strlen($value);

        if ($minLength !== null && $length < $minLength) {
            throw new ValidationError("String length {$length} is below minimum {$minLength}");
        }

        if ($maxLength !== null && $length > $maxLength) {
            throw new ValidationError("String length {$length} exceeds maximum {$maxLength}");
        }

        if ($pattern !== null && !preg_match($pattern, $value)) {
            throw new ValidationError("String does not match pattern: {$pattern}");
        }

        return $value;
    }

    /**
     * Validate that value is in a list of allowed choices.
     *
     * @param mixed $value Value to validate
     * @param array<mixed> $choices List of allowed values
     * @return mixed Validated value
     * @throws ValidationError If value not in choices
     */
    public static function validateChoice(mixed $value, array $choices): mixed
    {
        if (!in_array($value, $choices, true)) {
            $choicesStr = implode(', ', array_map('strval', $choices));
            throw new ValidationError("Invalid choice: {$value}. Allowed: {$choicesStr}");
        }

        return $value;
    }
}

/**
 * Chainable validator for complex validation scenarios.
 *
 * Features:
 * - Fluent interface for chaining validations
 * - Accumulates errors instead of throwing immediately
 * - Single validation call at the end
 *
 * Example:
 * ```php
 * $validator = new Validator('user@example.com', 'email');
 * $email = $validator
 *     ->isString(minLength: 5, maxLength: 100)
 *     ->isEmail()
 *     ->validate();
 * ```
 */
class Validator
{
    private mixed $value;
    private string $name;
    /** @var array<string> */
    private array $errors = [];

    /**
     * Initialize validator.
     *
     * @param mixed $value Value to validate
     * @param string $name Name of the value (for error messages)
     */
    public function __construct(mixed $value, string $name = 'value')
    {
        $this->value = $value;
        $this->name = $name;
    }

    /**
     * Check if value is a string.
     *
     * @param int|null $minLength Minimum length
     * @param int|null $maxLength Maximum length
     * @return self
     */
    public function isString(?int $minLength = null, ?int $maxLength = null): self
    {
        try {
            if (!is_string($this->value)) {
                throw new ValidationError("Value must be a string");
            }
            InputValidator::validateString($this->value, $minLength, $maxLength);
        } catch (ValidationError $e) {
            $this->errors[] = $e->getMessage();
        }
        return $this;
    }

    /**
     * Check if value is an integer.
     *
     * @param int|null $minValue Minimum value
     * @param int|null $maxValue Maximum value
     * @return self
     */
    public function isInteger(?int $minValue = null, ?int $maxValue = null): self
    {
        try {
            InputValidator::validateInteger($this->value, $minValue, $maxValue);
        } catch (ValidationError $e) {
            $this->errors[] = $e->getMessage();
        }
        return $this;
    }

    /**
     * Check if value is a valid email.
     *
     * @return self
     */
    public function isEmail(): self
    {
        try {
            if (!is_string($this->value)) {
                throw new ValidationError("Email must be a string");
            }
            InputValidator::validateEmail($this->value);
        } catch (ValidationError $e) {
            $this->errors[] = $e->getMessage();
        }
        return $this;
    }

    /**
     * Check if value is a valid URL.
     *
     * @param array<string>|null $allowedSchemes Allowed URL schemes
     * @return self
     */
    public function isUrl(?array $allowedSchemes = null): self
    {
        try {
            if (!is_string($this->value)) {
                throw new ValidationError("URL must be a string");
            }
            InputValidator::validateUrl($this->value, $allowedSchemes);
        } catch (ValidationError $e) {
            $this->errors[] = $e->getMessage();
        }
        return $this;
    }

    /**
     * Check if value matches regex pattern.
     *
     * @param string $pattern Regex pattern
     * @return self
     */
    public function matches(string $pattern): self
    {
        if (!preg_match($pattern, (string) $this->value)) {
            $this->errors[] = "{$this->name} does not match pattern: {$pattern}";
        }
        return $this;
    }

    /**
     * Perform validation and raise exception if errors found.
     *
     * @return mixed The validated value
     * @throws ValidationError If validation failed
     */
    public function validate(): mixed
    {
        if (!empty($this->errors)) {
            $errorMsg = "Validation failed for {$this->name}:\n";
            $errorMsg .= implode("\n", array_map(fn($e) => "  - {$e}", $this->errors));
            throw new ValidationError($errorMsg);
        }
        return $this->value;
    }

    /**
     * Get all validation errors.
     *
     * @return array<string>
     */
    public function getErrors(): array
    {
        return $this->errors;
    }

    /**
     * Check if validation has errors.
     *
     * @return bool
     */
    public function hasErrors(): bool
    {
        return !empty($this->errors);
    }
}
