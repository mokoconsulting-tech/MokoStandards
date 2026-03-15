<?php

declare(strict_types=1);

namespace MokoEnterprise;

use MokoEnterprise\Plugins\JoomlaPlugin;
use MokoEnterprise\Plugins\DolibarrPlugin;
use MokoEnterprise\Plugins\GenericPlugin;
use MokoEnterprise\Plugins\DocumentationPlugin;
use MokoEnterprise\Plugins\NodeJsPlugin;
use MokoEnterprise\Plugins\PythonPlugin;
use MokoEnterprise\Plugins\TerraformPlugin;
use MokoEnterprise\Plugins\WordPressPlugin;
use MokoEnterprise\Plugins\MobilePlugin;
use MokoEnterprise\Plugins\ApiPlugin;

/**
 * Plugin Registry - Central registry for all project type plugins
 * 
 * Manages plugin discovery, registration, and lifecycle
 *
 * @package MokoStandards\Enterprise
 * @version 1.0.0
 */
class PluginRegistry
{
    /** @var array<string, string> Map of project types to plugin class names */
    private static $pluginClasses = [
        'joomla' => JoomlaPlugin::class,
        'dolibarr' => DolibarrPlugin::class,
        'generic' => GenericPlugin::class,
        'documentation' => DocumentationPlugin::class,
        'nodejs' => NodeJsPlugin::class,
        'python' => PythonPlugin::class,
        'terraform' => TerraformPlugin::class,
        'wordpress' => WordPressPlugin::class,
        'mobile' => MobilePlugin::class,
        'api' => ApiPlugin::class,
    ];

    /** @var array<string, ProjectPluginInterface> Instantiated plugins */
    private static $plugins = [];

    /** @var AuditLogger|null Shared audit logger */
    private static $logger = null;

    /** @var MetricsCollector|null Shared metrics collector */
    private static $metricsCollector = null;

    /**
     * Set shared logger for all plugins
     *
     * @param AuditLogger $logger Audit logger instance
     * @return void
     */
    public static function setLogger(AuditLogger $logger): void
    {
        self::$logger = $logger;
    }

    /**
     * Set shared metrics collector for all plugins
     *
     * @param MetricsCollector $metricsCollector Metrics collector instance
     * @return void
     */
    public static function setMetricsCollector(MetricsCollector $metricsCollector): void
    {
        self::$metricsCollector = $metricsCollector;
    }

    /**
     * Register a custom plugin for a project type
     *
     * @param string $projectType Project type identifier
     * @param string $pluginClass Fully qualified plugin class name
     * @return void
     * @throws \InvalidArgumentException If plugin class doesn't implement ProjectPluginInterface
     */
    public static function registerPlugin(string $projectType, string $pluginClass): void
    {
        if (!class_exists($pluginClass)) {
            throw new \InvalidArgumentException("Plugin class does not exist: {$pluginClass}");
        }

        if (!is_subclass_of($pluginClass, ProjectPluginInterface::class)) {
            throw new \InvalidArgumentException(
                "Plugin class must implement ProjectPluginInterface: {$pluginClass}"
            );
        }

        self::$pluginClasses[$projectType] = $pluginClass;
        
        // Clear cached instance if exists
        if (isset(self::$plugins[$projectType])) {
            unset(self::$plugins[$projectType]);
        }
    }

    /**
     * Get plugin instance for a project type
     *
     * @param string $projectType Project type identifier
     * @param array $config Optional plugin configuration
     * @return ProjectPluginInterface|null Plugin instance or null if not found
     */
    public static function getPlugin(string $projectType, array $config = []): ?ProjectPluginInterface
    {
        // Check if plugin is already instantiated
        if (isset(self::$plugins[$projectType])) {
            return self::$plugins[$projectType];
        }

        // Check if plugin class is registered
        if (!isset(self::$pluginClasses[$projectType])) {
            return null;
        }

        // Instantiate plugin
        $pluginClass = self::$pluginClasses[$projectType];
        $plugin = new $pluginClass(self::$logger, self::$metricsCollector, $config);

        // Cache plugin instance
        self::$plugins[$projectType] = $plugin;

        return $plugin;
    }

    /**
     * Get all registered project types
     *
     * @return array List of project type identifiers
     */
    public static function getRegisteredTypes(): array
    {
        return array_keys(self::$pluginClasses);
    }

    /**
     * Get all registered plugins
     *
     * @param array $config Optional plugin configuration
     * @return array<string, ProjectPluginInterface> Map of project types to plugin instances
     */
    public static function getAllPlugins(array $config = []): array
    {
        $plugins = [];
        foreach (self::$pluginClasses as $projectType => $pluginClass) {
            $plugins[$projectType] = self::getPlugin($projectType, $config);
        }
        return $plugins;
    }

    /**
     * Check if a plugin is registered for a project type
     *
     * @param string $projectType Project type identifier
     * @return bool True if plugin is registered
     */
    public static function hasPlugin(string $projectType): bool
    {
        return isset(self::$pluginClasses[$projectType]);
    }

    /**
     * Unregister a plugin
     *
     * @param string $projectType Project type identifier
     * @return void
     */
    public static function unregisterPlugin(string $projectType): void
    {
        unset(self::$pluginClasses[$projectType]);
        unset(self::$plugins[$projectType]);
    }

    /**
     * Clear all plugin instances (forces re-instantiation)
     *
     * @return void
     */
    public static function clearCache(): void
    {
        self::$plugins = [];
    }

    /**
     * Get plugin information
     *
     * @param string $projectType Project type identifier
     * @return array|null Plugin info or null if not found
     */
    public static function getPluginInfo(string $projectType): ?array
    {
        $plugin = self::getPlugin($projectType);
        if ($plugin === null) {
            return null;
        }

        return [
            'project_type' => $plugin->getProjectType(),
            'plugin_name' => $plugin->getPluginName(),
            'plugin_version' => $plugin->getPluginVersion(),
            'required_files' => $plugin->getRequiredFiles(),
            'recommended_files' => $plugin->getRecommendedFiles(),
            'best_practices_count' => count($plugin->getBestPractices()),
            'commands_count' => count($plugin->getCommands()),
        ];
    }

    /**
     * Get all plugins information
     *
     * @return array Map of project types to plugin information
     */
    public static function getAllPluginsInfo(): array
    {
        $info = [];
        foreach (self::getRegisteredTypes() as $projectType) {
            $info[$projectType] = self::getPluginInfo($projectType);
        }
        return $info;
    }

    /**
     * Find plugin by feature/capability
     *
     * @param string $feature Feature name (e.g., 'package_manager', 'type_checking')
     * @return array List of project types supporting the feature
     */
    public static function findPluginsByFeature(string $feature): array
    {
        $matches = [];
        foreach (self::getRegisteredTypes() as $projectType) {
            $plugin = self::getPlugin($projectType);
            if ($plugin !== null) {
                $bestPractices = $plugin->getBestPractices();
                foreach ($bestPractices as $practice) {
                    if (stripos($practice['title'] ?? '', $feature) !== false ||
                        stripos($practice['description'] ?? '', $feature) !== false) {
                        $matches[] = $projectType;
                        break;
                    }
                }
            }
        }
        return $matches;
    }

    /**
     * Get plugin registry statistics
     *
     * @return array Registry statistics
     */
    public static function getStatistics(): array
    {
        return [
            'total_plugins' => count(self::$pluginClasses),
            'instantiated_plugins' => count(self::$plugins),
            'registered_types' => self::getRegisteredTypes(),
            'has_logger' => self::$logger !== null,
            'has_metrics_collector' => self::$metricsCollector !== null,
        ];
    }
}
