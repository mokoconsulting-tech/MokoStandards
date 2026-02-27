<?php

declare(strict_types=1);

namespace MokoStandards\Enterprise;

/**
 * Interface for project type-specific enterprise plugins
 * 
 * Each project type (Joomla, Node.js, Python, etc.) implements this interface
 * to provide type-specific validation, metrics, and management capabilities.
 *
 * @package MokoStandards\Enterprise
 * @version 1.0.0
 */
interface ProjectPluginInterface
{
    /**
     * Get the project type this plugin handles
     *
     * @return string Project type (e.g., 'joomla', 'nodejs', 'python')
     */
    public function getProjectType(): string;

    /**
     * Get the plugin name
     *
     * @return string Plugin name
     */
    public function getPluginName(): string;

    /**
     * Get the plugin version
     *
     * @return string Plugin version
     */
    public function getPluginVersion(): string;

    /**
     * Validate project configuration for this type
     *
     * @param array $config Project configuration
     * @param string $projectPath Path to project directory
     * @return array Validation result with 'valid' (bool), 'errors' (array), 'warnings' (array)
     */
    public function validateProject(array $config, string $projectPath): array;

    /**
     * Collect project-specific metrics
     *
     * @param string $projectPath Path to project directory
     * @param array $config Project configuration
     * @return array Metrics data
     */
    public function collectMetrics(string $projectPath, array $config): array;

    /**
     * Perform project health check
     *
     * @param string $projectPath Path to project directory
     * @param array $config Project configuration
     * @return array Health check result with 'healthy' (bool), 'score' (int), 'issues' (array)
     */
    public function healthCheck(string $projectPath, array $config): array;

    /**
     * Get required files for this project type
     *
     * @return array List of required file patterns
     */
    public function getRequiredFiles(): array;

    /**
     * Get recommended files for this project type
     *
     * @return array List of recommended file patterns
     */
    public function getRecommendedFiles(): array;

    /**
     * Get configuration schema for this project type
     *
     * @return array JSON schema for project configuration
     */
    public function getConfigSchema(): array;

    /**
     * Get best practices checklist
     *
     * @return array List of best practices with descriptions
     */
    public function getBestPractices(): array;

    /**
     * Check if project is ready for release/deployment
     *
     * @param string $projectPath Path to project directory
     * @param array $config Project configuration
     * @return array Readiness result with 'ready' (bool), 'blockers' (array), 'warnings' (array)
     */
    public function checkReadiness(string $projectPath, array $config): array;

    /**
     * Get plugin-specific commands
     *
     * @return array Array of command definitions
     */
    public function getCommands(): array;

    /**
     * Initialize project with type-specific scaffolding
     *
     * @param string $projectPath Path to project directory
     * @param array $options Initialization options
     * @return array Result with 'success' (bool), 'message' (string), 'files_created' (array)
     */
    public function initializeProject(string $projectPath, array $options = []): array;
}
