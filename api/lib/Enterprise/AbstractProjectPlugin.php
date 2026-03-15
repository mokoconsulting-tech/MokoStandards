<?php

declare(strict_types=1);

namespace MokoEnterprise;

/**
 * Abstract base class for project type plugins
 * 
 * Provides common functionality for all project type plugins
 *
 * @package MokoStandards\Enterprise
 * @version 1.0.0
 */
abstract class AbstractProjectPlugin implements ProjectPluginInterface
{
    /** @var AuditLogger */
    protected $logger;

    /** @var MetricsCollector */
    protected $metricsCollector;

    /** @var array Plugin configuration */
    protected $config;

    /**
     * Constructor
     *
     * @param AuditLogger|null $logger Optional audit logger
     * @param MetricsCollector|null $metricsCollector Optional metrics collector
     * @param array $config Plugin configuration
     */
    public function __construct(
        ?AuditLogger $logger = null,
        ?MetricsCollector $metricsCollector = null,
        array $config = []
    ) {
        $this->logger = $logger ?? new AuditLogger('project_plugin');
        $this->metricsCollector = $metricsCollector ?? new MetricsCollector();
        $this->config = $config;
    }

    /**
     * {@inheritdoc}
     */
    abstract public function getProjectType(): string;

    /**
     * {@inheritdoc}
     */
    abstract public function getPluginName(): string;

    /**
     * {@inheritdoc}
     */
    public function getPluginVersion(): string
    {
        return '1.0.0';
    }

    /**
     * {@inheritdoc}
     */
    abstract public function validateProject(array $config, string $projectPath): array;

    /**
     * {@inheritdoc}
     */
    abstract public function collectMetrics(string $projectPath, array $config): array;

    /**
     * {@inheritdoc}
     */
    abstract public function healthCheck(string $projectPath, array $config): array;

    /**
     * {@inheritdoc}
     */
    abstract public function getRequiredFiles(): array;

    /**
     * {@inheritdoc}
     */
    abstract public function getRecommendedFiles(): array;

    /**
     * {@inheritdoc}
     */
    abstract public function getConfigSchema(): array;

    /**
     * {@inheritdoc}
     */
    abstract public function getBestPractices(): array;

    /**
     * {@inheritdoc}
     */
    public function checkReadiness(string $projectPath, array $config): array
    {
        $validation = $this->validateProject($config, $projectPath);
        $health = $this->healthCheck($projectPath, $config);

        $blockers = array_merge(
            $validation['errors'] ?? [],
            array_filter($health['issues'] ?? [], function ($issue) {
                return ($issue['severity'] ?? '') === 'critical';
            })
        );

        $warnings = array_merge(
            $validation['warnings'] ?? [],
            array_filter($health['issues'] ?? [], function ($issue) {
                return ($issue['severity'] ?? '') === 'warning';
            })
        );

        return [
            'ready' => empty($blockers),
            'blockers' => $blockers,
            'warnings' => $warnings,
            'score' => $health['score'] ?? 0,
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getCommands(): array
    {
        // Default: no custom commands
        return [];
    }

    /**
     * {@inheritdoc}
     */
    public function initializeProject(string $projectPath, array $options = []): array
    {
        // Default: no initialization
        return [
            'success' => true,
            'message' => 'No initialization required for ' . $this->getProjectType(),
            'files_created' => [],
        ];
    }

    /**
     * Check if a file exists in the project
     *
     * @param string $projectPath Project directory path
     * @param string $filePath Relative file path
     * @return bool True if file exists
     */
    protected function fileExists(string $projectPath, string $filePath): bool
    {
        return file_exists(rtrim($projectPath, '/') . '/' . ltrim($filePath, '/'));
    }

    /**
     * Read a file from the project
     *
     * @param string $projectPath Project directory path
     * @param string $filePath Relative file path
     * @return string|null File contents or null if not found
     */
    protected function readFile(string $projectPath, string $filePath): ?string
    {
        $fullPath = rtrim($projectPath, '/') . '/' . ltrim($filePath, '/');
        return file_exists($fullPath) ? file_get_contents($fullPath) : null;
    }

    /**
     * Check if files match a pattern in the project
     *
     * @param string $projectPath Project directory path
     * @param string $pattern Glob pattern
     * @return array Matching file paths
     */
    protected function findFiles(string $projectPath, string $pattern): array
    {
        $fullPattern = rtrim($projectPath, '/') . '/' . ltrim($pattern, '/');
        $matches = glob($fullPattern);
        return is_array($matches) ? $matches : [];
    }

    /**
     * Count files matching a pattern
     *
     * @param string $projectPath Project directory path
     * @param string $pattern Glob pattern
     * @return int Number of matching files
     */
    protected function countFiles(string $projectPath, string $pattern): int
    {
        return count($this->findFiles($projectPath, $pattern));
    }

    /**
     * Parse JSON file
     *
     * @param string $projectPath Project directory path
     * @param string $filePath Relative file path
     * @return array|null Parsed JSON data or null on error
     */
    protected function parseJsonFile(string $projectPath, string $filePath): ?array
    {
        $content = $this->readFile($projectPath, $filePath);
        if ($content === null) {
            return null;
        }

        $data = json_decode($content, true);
        return json_last_error() === JSON_ERROR_NONE ? $data : null;
    }

    /**
     * Log plugin activity
     *
     * @param string $message Log message
     * @param string $level Log level (info, warning, error)
     * @param array $context Additional context
     * @return void
     */
    protected function log(string $message, string $level = 'info', array $context = []): void
    {
        $context['plugin'] = $this->getPluginName();
        $context['project_type'] = $this->getProjectType();

        switch ($level) {
            case 'error':
                $this->logger->logError($message, $context);
                break;
            case 'warning':
                $this->logger->logWarning($message, $context);
                break;
            default:
                $this->logger->logInfo($message, $context);
                break;
        }
    }

    /**
     * Record metrics
     *
     * @param string $category Metric category
     * @param string $name Metric name
     * @param mixed $value Metric value
     * @param array $tags Optional tags
     * @return void
     */
    protected function recordMetric(string $category, string $name, $value, array $tags = []): void
    {
        $tags['plugin'] = $this->getPluginName();
        $tags['project_type'] = $this->getProjectType();

        $this->metricsCollector->record($category, $name, $value, $tags);
    }
}
