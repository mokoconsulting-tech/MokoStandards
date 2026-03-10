<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Enterprise.Plugins
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/lib/Enterprise/Plugins/ApiPlugin.php
 * VERSION: 04.00.04
 * BRIEF: Enterprise plugin for API/Microservices projects
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise\Plugins;

use MokoStandards\Enterprise\AbstractProjectPlugin;

/**
 * API/Microservices Project Plugin
 * 
 * Provides validation, metrics, and management capabilities for
 * API and microservices projects (REST, GraphQL, gRPC).
 */
class ApiPlugin extends AbstractProjectPlugin
{
    /**
     * {@inheritdoc}
     */
    public function getProjectType(): string
    {
        return 'api';
    }

    /**
     * {@inheritdoc}
     */
    public function getPluginName(): string
    {
        return 'API/Microservices Enterprise Plugin';
    }

    /**
     * {@inheritdoc}
     */
    public function validateProject(array $config, string $projectPath): array
    {
        $errors = [];
        $warnings = [];

        $apiType = $this->detectAPIType($projectPath);

        // Check for API documentation
        if (!$this->hasAPIDocumentation($projectPath, $apiType)) {
            $warnings[] = 'No API documentation found (OpenAPI, GraphQL schema, etc.)';
        }

        // Check for proper error handling
        if (!$this->hasErrorHandling($projectPath)) {
            $warnings[] = 'Consider implementing standardized error handling';
        }

        // Check for authentication
        if (!$this->hasAuthentication($projectPath)) {
            $warnings[] = 'No authentication mechanism detected';
        }

        // Check for rate limiting
        if (!$this->hasRateLimiting($projectPath)) {
            $warnings[] = 'Consider implementing rate limiting';
        }

        // Check for logging
        if (!$this->hasLogging($projectPath)) {
            $warnings[] = 'No logging configuration found';
        }

        // Check for input validation
        if (!$this->hasInputValidation($projectPath)) {
            $warnings[] = 'Ensure proper input validation is implemented';
        }

        // Check for CORS configuration
        if (!$this->hasCORSConfig($projectPath)) {
            $warnings[] = 'No CORS configuration found';
        }

        // Check for tests
        if (!$this->hasTests($projectPath)) {
            $warnings[] = 'No API tests found';
        }

        $this->log(
            'API project validation completed',
            'info',
            ['errors' => count($errors), 'warnings' => count($warnings), 'type' => $apiType]
        );

        return [
            'valid' => empty($errors),
            'errors' => $errors,
            'warnings' => $warnings,
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function collectMetrics(string $projectPath, array $config): array
    {
        $apiType = $this->detectAPIType($projectPath);
        $language = $this->detectLanguage($projectPath);

        $metrics = [
            'api_type' => $apiType,
            'language' => $language,
            'has_documentation' => $this->hasAPIDocumentation($projectPath, $apiType),
            'has_authentication' => $this->hasAuthentication($projectPath),
            'has_authorization' => $this->hasAuthorization($projectPath),
            'has_rate_limiting' => $this->hasRateLimiting($projectPath),
            'has_logging' => $this->hasLogging($projectPath),
            'has_monitoring' => $this->hasMonitoring($projectPath),
            'has_caching' => $this->hasCaching($projectPath),
            'has_tests' => $this->hasTests($projectPath),
            'has_docker' => $this->fileExists($projectPath, 'Dockerfile'),
            'has_ci' => $this->hasCICD($projectPath),
            'has_kubernetes' => $this->hasKubernetes($projectPath),
        ];

        // Count endpoints
        $metrics['endpoints_count'] = $this->countEndpoints($projectPath, $apiType, $language);

        // Count routes/controllers
        $metrics['routes_count'] = $this->countRoutes($projectPath, $language);

        // Count middleware
        $metrics['middleware_count'] = $this->countMiddleware($projectPath, $language);

        // Count lines of code
        $metrics['total_lines'] = $this->countTotalLines($projectPath, $language);

        // Detect framework
        $metrics['framework'] = $this->detectFramework($projectPath, $language);

        // Record metrics
        $this->recordMetric('api', 'endpoints', $metrics['endpoints_count']);
        $this->recordMetric('api', 'total_lines', $metrics['total_lines']);

        $this->log('Collected API metrics', 'info', $metrics);

        return $metrics;
    }

    /**
     * {@inheritdoc}
     */
    public function healthCheck(string $projectPath, array $config): array
    {
        $issues = [];
        $score = 100;

        $apiType = $this->detectAPIType($projectPath);

        // Check for API documentation
        if (!$this->hasAPIDocumentation($projectPath, $apiType)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing API documentation',
            ];
            $score -= 15;
        }

        // Check for authentication
        if (!$this->hasAuthentication($projectPath)) {
            $issues[] = [
                'severity' => 'critical',
                'message' => 'No authentication mechanism detected',
            ];
            $score -= 20;
        }

        // Check for authorization
        if (!$this->hasAuthorization($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No authorization/access control detected',
            ];
            $score -= 10;
        }

        // Check for input validation
        if (!$this->hasInputValidation($projectPath)) {
            $issues[] = [
                'severity' => 'critical',
                'message' => 'Input validation may be missing',
            ];
            $score -= 20;
        }

        // Check for rate limiting
        if (!$this->hasRateLimiting($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No rate limiting configured',
            ];
            $score -= 10;
        }

        // Check for logging
        if (!$this->hasLogging($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No logging configuration found',
            ];
            $score -= 10;
        }

        // Check for tests
        if (!$this->hasTests($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No API tests found',
            ];
            $score -= 15;
        }

        // Check for README
        if (!$this->fileExists($projectPath, 'README.md')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing README.md',
            ];
            $score -= 5;
        }

        // Check for environment configuration
        if (!$this->fileExists($projectPath, '.env.example')) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'Missing .env.example for configuration',
            ];
            $score -= 5;
        }

        $score = max(0, $score);

        $this->log('API health check completed', 'info', [
            'score' => $score,
            'issues_count' => count($issues),
            'api_type' => $apiType,
        ]);

        return [
            'healthy' => $score >= 70,
            'score' => $score,
            'issues' => $issues,
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRequiredFiles(): array
    {
        return [
            'API documentation (openapi.yaml, swagger.json, schema.graphql)',
            'Authentication configuration',
            'Error handling middleware',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRecommendedFiles(): array
    {
        return [
            'README.md',
            '.env.example',
            'openapi.yaml or swagger.json (REST)',
            'schema.graphql (GraphQL)',
            'Dockerfile',
            'docker-compose.yml',
            'kubernetes/*.yaml',
            'tests/ or test/',
            '.github/workflows/* or .gitlab-ci.yml',
            'middleware/ or middlewares/',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getConfigSchema(): array
    {
        return [
            'type' => 'object',
            'properties' => [
                'api_type' => [
                    'type' => 'string',
                    'enum' => ['rest', 'graphql', 'grpc', 'soap', 'websocket'],
                    'description' => 'API type',
                ],
                'authentication' => [
                    'type' => 'string',
                    'enum' => ['jwt', 'oauth2', 'api-key', 'basic', 'none'],
                    'description' => 'Authentication method',
                ],
                'framework' => [
                    'type' => 'string',
                    'description' => 'Framework used (Express, FastAPI, Spring Boot, etc.)',
                ],
                'enable_rate_limiting' => [
                    'type' => 'boolean',
                    'description' => 'Enable rate limiting',
                ],
                'enable_caching' => [
                    'type' => 'boolean',
                    'description' => 'Enable response caching',
                ],
                'port' => [
                    'type' => 'integer',
                    'description' => 'API server port',
                ],
            ],
            'required' => ['api_type'],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getBestPractices(): array
    {
        return [
            'Document API with OpenAPI/Swagger or GraphQL schema',
            'Implement proper authentication (JWT, OAuth2)',
            'Use authorization for access control',
            'Validate all input data',
            'Implement rate limiting to prevent abuse',
            'Use standardized error responses',
            'Implement comprehensive logging',
            'Add monitoring and metrics collection',
            'Use HTTPS/TLS for all endpoints',
            'Implement CORS properly',
            'Version your API endpoints',
            'Use pagination for list endpoints',
            'Implement caching where appropriate',
            'Write comprehensive API tests',
            'Use Docker for consistent deployments',
        ];
    }

    /**
     * Detect API type
     */
    private function detectAPIType(string $projectPath): string
    {
        // GraphQL
        if ($this->fileExists($projectPath, 'schema.graphql') ||
            $this->fileExists($projectPath, '*.graphql')) {
            return 'graphql';
        }

        // gRPC
        if ($this->fileExists($projectPath, '*.proto')) {
            return 'grpc';
        }

        // REST (OpenAPI/Swagger)
        if ($this->fileExists($projectPath, 'openapi.yaml') ||
            $this->fileExists($projectPath, 'openapi.json') ||
            $this->fileExists($projectPath, 'swagger.yaml') ||
            $this->fileExists($projectPath, 'swagger.json')) {
            return 'rest';
        }

        // Check code for REST patterns
        $files = $this->findFiles($projectPath, '**/*.{js,ts,py,java,go,php}');
        foreach (array_slice($files, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    if (preg_match('/@(Get|Post|Put|Delete|Patch)\(/', $content) ||
                        preg_match('/(get|post|put|delete|patch)\s*\([\'"]/', $content)) {
                        return 'rest';
                    }
                }
            }
        }

        return 'rest';
    }

    /**
     * Detect language
     */
    private function detectLanguage(string $projectPath): string
    {
        $counts = [
            'js' => $this->countFiles($projectPath, '**/*.js'),
            'ts' => $this->countFiles($projectPath, '**/*.ts'),
            'py' => $this->countFiles($projectPath, '**/*.py'),
            'java' => $this->countFiles($projectPath, '**/*.java'),
            'go' => $this->countFiles($projectPath, '**/*.go'),
            'php' => $this->countFiles($projectPath, '**/*.php'),
        ];

        arsort($counts);
        $topLang = array_key_first($counts);

        $langMap = [
            'js' => 'JavaScript',
            'ts' => 'TypeScript',
            'py' => 'Python',
            'java' => 'Java',
            'go' => 'Go',
            'php' => 'PHP',
        ];

        return $langMap[$topLang] ?? 'Unknown';
    }

    /**
     * Check for API documentation
     */
    private function hasAPIDocumentation(string $projectPath, string $apiType): bool
    {
        if ($apiType === 'graphql') {
            return $this->fileExists($projectPath, 'schema.graphql') ||
                   $this->countFiles($projectPath, '**/*.graphql') > 0;
        }

        if ($apiType === 'grpc') {
            return $this->countFiles($projectPath, '**/*.proto') > 0;
        }

        // REST
        return $this->fileExists($projectPath, 'openapi.yaml') ||
               $this->fileExists($projectPath, 'openapi.json') ||
               $this->fileExists($projectPath, 'swagger.yaml') ||
               $this->fileExists($projectPath, 'swagger.json');
    }

    /**
     * Check for error handling
     */
    private function hasErrorHandling(string $projectPath): bool
    {
        $files = $this->findFiles($projectPath, '**/*.{js,ts,py}');
        
        foreach (array_slice($files, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && (
                    strpos($content, 'errorHandler') !== false ||
                    strpos($content, 'error_handler') !== false ||
                    preg_match('/class\s+\w*Error/', $content)
                )) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for authentication
     */
    private function hasAuthentication(string $projectPath): bool
    {
        $files = $this->findFiles($projectPath, '**/*.{js,ts,py,java,go,php}');
        
        foreach (array_slice($files, 0, 15) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && (
                    stripos($content, 'jwt') !== false ||
                    stripos($content, 'oauth') !== false ||
                    stripos($content, 'passport') !== false ||
                    stripos($content, 'authenticate') !== false ||
                    stripos($content, 'api_key') !== false ||
                    stripos($content, 'bearer') !== false
                )) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for authorization
     */
    private function hasAuthorization(string $projectPath): bool
    {
        $files = $this->findFiles($projectPath, '**/*.{js,ts,py,java,go,php}');
        
        foreach (array_slice($files, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && (
                    stripos($content, 'authorize') !== false ||
                    stripos($content, 'permission') !== false ||
                    stripos($content, 'role') !== false ||
                    stripos($content, 'acl') !== false
                )) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for rate limiting
     */
    private function hasRateLimiting(string $projectPath): bool
    {
        $files = $this->findFiles($projectPath, '**/*.{js,ts,py,java,go,php}');
        
        foreach (array_slice($files, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && (
                    stripos($content, 'rate_limit') !== false ||
                    stripos($content, 'rateLimit') !== false ||
                    stripos($content, 'throttle') !== false
                )) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for logging
     */
    private function hasLogging(string $projectPath): bool
    {
        $files = $this->findFiles($projectPath, '**/*.{js,ts,py,java,go,php}');
        
        foreach (array_slice($files, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && (
                    stripos($content, 'logger') !== false ||
                    stripos($content, 'winston') !== false ||
                    stripos($content, 'logging') !== false ||
                    stripos($content, 'log.') !== false
                )) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for monitoring
     */
    private function hasMonitoring(string $projectPath): bool
    {
        $files = $this->findFiles($projectPath, '**/*.{js,ts,py,java,go,php}');
        
        foreach (array_slice($files, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && (
                    stripos($content, 'prometheus') !== false ||
                    stripos($content, 'metrics') !== false ||
                    stripos($content, 'monitoring') !== false ||
                    stripos($content, 'newrelic') !== false
                )) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for caching
     */
    private function hasCaching(string $projectPath): bool
    {
        $files = $this->findFiles($projectPath, '**/*.{js,ts,py,java,go,php}');
        
        foreach (array_slice($files, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && (
                    stripos($content, 'redis') !== false ||
                    stripos($content, 'cache') !== false ||
                    stripos($content, 'memcached') !== false
                )) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for input validation
     */
    private function hasInputValidation(string $projectPath): bool
    {
        $files = $this->findFiles($projectPath, '**/*.{js,ts,py,java,go,php}');
        
        foreach (array_slice($files, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && (
                    stripos($content, 'validate') !== false ||
                    stripos($content, 'validator') !== false ||
                    stripos($content, 'joi') !== false ||
                    stripos($content, 'yup') !== false
                )) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for CORS configuration
     */
    private function hasCORSConfig(string $projectPath): bool
    {
        $files = $this->findFiles($projectPath, '**/*.{js,ts,py,java,go,php}');
        
        foreach (array_slice($files, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && stripos($content, 'cors') !== false) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for tests
     */
    private function hasTests(string $projectPath): bool
    {
        return $this->fileExists($projectPath, 'tests') ||
               $this->fileExists($projectPath, 'test') ||
               $this->fileExists($projectPath, '__tests__') ||
               $this->countFiles($projectPath, '**/*.test.*') > 0 ||
               $this->countFiles($projectPath, '**/*.spec.*') > 0;
    }

    /**
     * Check for CI/CD
     */
    private function hasCICD(string $projectPath): bool
    {
        return $this->fileExists($projectPath, '.github/workflows') ||
               $this->fileExists($projectPath, '.gitlab-ci.yml') ||
               $this->fileExists($projectPath, 'Jenkinsfile') ||
               $this->fileExists($projectPath, '.circleci');
    }

    /**
     * Check for Kubernetes
     */
    private function hasKubernetes(string $projectPath): bool
    {
        return $this->fileExists($projectPath, 'k8s') ||
               $this->fileExists($projectPath, 'kubernetes') ||
               $this->countFiles($projectPath, '**/*.yaml') > 0;
    }

    /**
     * Count endpoints
     */
    private function countEndpoints(string $projectPath, string $apiType, string $language): int
    {
        $count = 0;
        $pattern = $language === 'Python' ? '**/*.py' : '**/*.{js,ts}';
        $files = $this->findFiles($projectPath, $pattern);

        foreach ($files as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    $count += preg_match_all('/@(app\.)?(get|post|put|delete|patch)\s*\(/', $content);
                    $count += preg_match_all('/\.(get|post|put|delete|patch)\s*\([\'"]/', $content);
                }
            }
        }

        return $count;
    }

    /**
     * Count routes
     */
    private function countRoutes(string $projectPath, string $language): int
    {
        $routeFiles = array_merge(
            $this->findFiles($projectPath, '**/routes/**/*.{js,ts,py}'),
            $this->findFiles($projectPath, '**/route*.{js,ts,py}')
        );

        return count($routeFiles);
    }

    /**
     * Count middleware
     */
    private function countMiddleware(string $projectPath, string $language): int
    {
        $middlewareFiles = array_merge(
            $this->findFiles($projectPath, '**/middleware/**/*.{js,ts,py}'),
            $this->findFiles($projectPath, '**/middlewares/**/*.{js,ts,py}')
        );

        return count($middlewareFiles);
    }

    /**
     * Count total lines
     */
    private function countTotalLines(string $projectPath, string $language): int
    {
        $extMap = [
            'JavaScript' => ['js'],
            'TypeScript' => ['ts'],
            'Python' => ['py'],
            'Java' => ['java'],
            'Go' => ['go'],
            'PHP' => ['php'],
        ];

        $extensions = $extMap[$language] ?? ['js', 'ts', 'py'];
        $totalLines = 0;

        foreach ($extensions as $ext) {
            $files = $this->findFiles($projectPath, "**/*.{$ext}");
            foreach ($files as $file) {
                if (is_file($file)) {
                    $totalLines += count(file($file));
                }
            }
        }

        return $totalLines;
    }

    /**
     * Detect framework
     */
    private function detectFramework(string $projectPath, string $language): string
    {
        if ($language === 'JavaScript' || $language === 'TypeScript') {
            $packageData = $this->parseJsonFile($projectPath, 'package.json');
            if ($packageData) {
                $deps = array_merge(
                    $packageData['dependencies'] ?? [],
                    $packageData['devDependencies'] ?? []
                );
                
                if (isset($deps['express'])) return 'Express';
                if (isset($deps['fastify'])) return 'Fastify';
                if (isset($deps['@nestjs/core'])) return 'NestJS';
                if (isset($deps['koa'])) return 'Koa';
            }
        }

        if ($language === 'Python') {
            $requirements = $this->readFile($projectPath, 'requirements.txt');
            if ($requirements) {
                if (stripos($requirements, 'fastapi') !== false) return 'FastAPI';
                if (stripos($requirements, 'flask') !== false) return 'Flask';
                if (stripos($requirements, 'django') !== false) return 'Django';
            }
        }

        return 'Unknown';
    }
}
