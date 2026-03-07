<?php

declare(strict_types=1);

namespace MokoStandards\Enterprise;

/**
 * Plugin Factory - Factory for creating and managing plugin instances
 * 
 * Provides convenient methods for plugin instantiation with dependency injection
 *
 * @package MokoStandards\Enterprise
 * @version 1.0.0
 */
class PluginFactory
{
    /** @var AuditLogger */
    private $logger;

    /** @var MetricsCollector */
    private $metricsCollector;

    /** @var array Default configuration for plugins */
    private $defaultConfig;

    /**
     * Constructor
     *
     * @param AuditLogger|null $logger Optional audit logger
     * @param MetricsCollector|null $metricsCollector Optional metrics collector
     * @param array $defaultConfig Default configuration for all plugins
     */
    public function __construct(
        ?AuditLogger $logger = null,
        ?MetricsCollector $metricsCollector = null,
        array $defaultConfig = []
    ) {
        $this->logger = $logger ?? new AuditLogger('plugin_factory');
        $this->metricsCollector = $metricsCollector ?? new MetricsCollector();
        $this->defaultConfig = $defaultConfig;

        // Set shared instances in registry
        PluginRegistry::setLogger($this->logger);
        PluginRegistry::setMetricsCollector($this->metricsCollector);
    }

    /**
     * Create plugin for a project type
     *
     * @param string $projectType Project type identifier
     * @param array $config Optional plugin-specific configuration
     * @return ProjectPluginInterface|null Plugin instance or null if not found
     */
    public function create(string $projectType, array $config = []): ?ProjectPluginInterface
    {
        $config = array_merge($this->defaultConfig, $config);
        return PluginRegistry::getPlugin($projectType, $config);
    }

    /**
     * Create plugin for a project by auto-detecting type
     *
     * @param string $projectPath Path to project directory
     * @param array $config Optional plugin-specific configuration
     * @return ProjectPluginInterface|null Plugin instance or null if type can't be detected
     */
    public function createForProject(string $projectPath, array $config = []): ?ProjectPluginInterface
    {
        $detector = new ProjectTypeDetector($this->logger);
        $detection = $detector->detectProjectType($projectPath);

        if (empty($detection['type'])) {
            $this->logger->logWarning('Could not detect project type', [
                'project_path' => $projectPath,
                'detection_result' => $detection,
            ]);
            return null;
        }

        $projectType = $detection['type'];
        $this->logger->logInfo("Detected project type: {$projectType}", [
            'project_path' => $projectPath,
            'confidence' => $detection['confidence'] ?? 0,
        ]);

        return $this->create($projectType, $config);
    }

    /**
     * Create all available plugins
     *
     * @param array $config Optional configuration for all plugins
     * @return array<string, ProjectPluginInterface> Map of project types to plugin instances
     */
    public function createAll(array $config = []): array
    {
        $config = array_merge($this->defaultConfig, $config);
        return PluginRegistry::getAllPlugins($config);
    }

    /**
     * Create multiple plugins
     *
     * @param array $projectTypes List of project type identifiers
     * @param array $config Optional configuration for plugins
     * @return array<string, ProjectPluginInterface> Map of project types to plugin instances
     */
    public function createMultiple(array $projectTypes, array $config = []): array
    {
        $config = array_merge($this->defaultConfig, $config);
        $plugins = [];

        foreach ($projectTypes as $projectType) {
            $plugin = $this->create($projectType, $config);
            if ($plugin !== null) {
                $plugins[$projectType] = $plugin;
            }
        }

        return $plugins;
    }

    /**
     * Validate and create plugin
     *
     * @param string $projectType Project type identifier
     * @param string $projectPath Path to project directory
     * @param array $projectConfig Project configuration
     * @return array Result with 'plugin' (ProjectPluginInterface|null) and 'validation' (array)
     */
    public function createAndValidate(
        string $projectType,
        string $projectPath,
        array $projectConfig = []
    ): array {
        $plugin = $this->create($projectType);

        if ($plugin === null) {
            return [
                'plugin' => null,
                'validation' => [
                    'valid' => false,
                    'errors' => ["Plugin not found for project type: {$projectType}"],
                    'warnings' => [],
                ],
            ];
        }

        $validation = $plugin->validateProject($projectConfig, $projectPath);

        return [
            'plugin' => $plugin,
            'validation' => $validation,
        ];
    }

    /**
     * Get factory statistics
     *
     * @return array Factory and registry statistics
     */
    public function getStatistics(): array
    {
        return [
            'factory' => [
                'has_logger' => $this->logger !== null,
                'has_metrics_collector' => $this->metricsCollector !== null,
                'default_config_keys' => array_keys($this->defaultConfig),
            ],
            'registry' => PluginRegistry::getStatistics(),
        ];
    }

    /**
     * Get all available plugin information
     *
     * @return array Map of project types to plugin information
     */
    public function getAvailablePlugins(): array
    {
        return PluginRegistry::getAllPluginsInfo();
    }

    /**
     * Check if a plugin is available for a project type
     *
     * @param string $projectType Project type identifier
     * @return bool True if plugin is available
     */
    public function hasPlugin(string $projectType): bool
    {
        return PluginRegistry::hasPlugin($projectType);
    }

    /**
     * Get the logger instance
     *
     * @return AuditLogger
     */
    public function getLogger(): AuditLogger
    {
        return $this->logger;
    }

    /**
     * Get the metrics collector instance
     *
     * @return MetricsCollector
     */
    public function getMetricsCollector(): MetricsCollector
    {
        return $this->metricsCollector;
    }

    /**
     * Set default configuration for all plugins
     *
     * @param array $config Default configuration
     * @return void
     */
    public function setDefaultConfig(array $config): void
    {
        $this->defaultConfig = $config;
    }

    /**
     * Get default configuration
     *
     * @return array Default configuration
     */
    public function getDefaultConfig(): array
    {
        return $this->defaultConfig;
    }

    /**
     * Run health check using appropriate plugin
     *
     * @param string $projectType Project type identifier
     * @param string $projectPath Path to project directory
     * @param array $projectConfig Project configuration
     * @return array Health check result
     */
    public function runHealthCheck(
        string $projectType,
        string $projectPath,
        array $projectConfig = []
    ): array {
        $plugin = $this->create($projectType);

        if ($plugin === null) {
            return [
                'healthy' => false,
                'score' => 0,
                'issues' => [
                    [
                        'severity' => 'critical',
                        'message' => "Plugin not found for project type: {$projectType}",
                        'category' => 'plugin',
                    ],
                ],
            ];
        }

        return $plugin->healthCheck($projectPath, $projectConfig);
    }

    /**
     * Collect metrics using appropriate plugin
     *
     * @param string $projectType Project type identifier
     * @param string $projectPath Path to project directory
     * @param array $projectConfig Project configuration
     * @return array Metrics data
     */
    public function collectMetrics(
        string $projectType,
        string $projectPath,
        array $projectConfig = []
    ): array {
        $plugin = $this->create($projectType);

        if ($plugin === null) {
            return [
                'error' => "Plugin not found for project type: {$projectType}",
                'metrics' => [],
            ];
        }

        return $plugin->collectMetrics($projectPath, $projectConfig);
    }

    /**
     * Check project readiness using appropriate plugin
     *
     * @param string $projectType Project type identifier
     * @param string $projectPath Path to project directory
     * @param array $projectConfig Project configuration
     * @return array Readiness result
     */
    public function checkReadiness(
        string $projectType,
        string $projectPath,
        array $projectConfig = []
    ): array {
        $plugin = $this->create($projectType);

        if ($plugin === null) {
            return [
                'ready' => false,
                'blockers' => ["Plugin not found for project type: {$projectType}"],
                'warnings' => [],
                'score' => 0,
            ];
        }

        return $plugin->checkReadiness($projectPath, $projectConfig);
    }
}
