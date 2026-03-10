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
 * PATH: /api/lib/Enterprise/Plugins/MobilePlugin.php
 * VERSION: 04.00.04
 * BRIEF: Enterprise plugin for mobile app projects
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise\Plugins;

use MokoStandards\Enterprise\AbstractProjectPlugin;

/**
 * Mobile App Project Plugin
 * 
 * Provides validation, metrics, and management capabilities for
 * mobile applications (React Native, Flutter, native iOS/Android).
 */
class MobilePlugin extends AbstractProjectPlugin
{
    /**
     * {@inheritdoc}
     */
    public function getProjectType(): string
    {
        return 'mobile';
    }

    /**
     * {@inheritdoc}
     */
    public function getPluginName(): string
    {
        return 'Mobile App Enterprise Plugin';
    }

    /**
     * {@inheritdoc}
     */
    public function validateProject(array $config, string $projectPath): array
    {
        $errors = [];
        $warnings = [];

        $platform = $this->detectPlatform($projectPath);

        switch ($platform) {
            case 'react-native':
                if (!$this->fileExists($projectPath, 'package.json')) {
                    $errors[] = 'React Native project missing package.json';
                }
                if (!$this->fileExists($projectPath, 'app.json') &&
                    !$this->fileExists($projectPath, 'app.config.js')) {
                    $warnings[] = 'Missing app.json or app.config.js';
                }
                if (!$this->fileExists($projectPath, 'ios') &&
                    !$this->fileExists($projectPath, 'android')) {
                    $warnings[] = 'No native platform directories found';
                }
                break;

            case 'flutter':
                if (!$this->fileExists($projectPath, 'pubspec.yaml')) {
                    $errors[] = 'Flutter project missing pubspec.yaml';
                }
                if (!$this->fileExists($projectPath, 'lib')) {
                    $errors[] = 'Flutter project missing lib directory';
                }
                break;

            case 'ios':
                if (!$this->fileExists($projectPath, '*.xcodeproj') &&
                    !$this->fileExists($projectPath, '*.xcworkspace')) {
                    $errors[] = 'iOS project missing Xcode project file';
                }
                if (!$this->fileExists($projectPath, 'Podfile')) {
                    $warnings[] = 'No Podfile found (CocoaPods not used)';
                }
                break;

            case 'android':
                if (!$this->fileExists($projectPath, 'build.gradle')) {
                    $errors[] = 'Android project missing build.gradle';
                }
                if (!$this->fileExists($projectPath, 'app/src/main')) {
                    $errors[] = 'Android project missing standard structure';
                }
                break;
        }

        // Check for app icons
        if (!$this->hasAppIcons($projectPath, $platform)) {
            $warnings[] = 'App icons not found';
        }

        // Check for splash screen
        if (!$this->hasSplashScreen($projectPath, $platform)) {
            $warnings[] = 'Splash screen not found';
        }

        // Check for tests
        if (!$this->hasTests($projectPath, $platform)) {
            $warnings[] = 'No tests found';
        }

        $this->log(
            'Mobile project validation completed',
            'info',
            ['errors' => count($errors), 'warnings' => count($warnings), 'platform' => $platform]
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
        $platform = $this->detectPlatform($projectPath);

        $metrics = [
            'platform' => $platform,
            'supports_ios' => $this->supportsIOS($projectPath, $platform),
            'supports_android' => $this->supportsAndroid($projectPath, $platform),
            'has_app_icons' => $this->hasAppIcons($projectPath, $platform),
            'has_splash_screen' => $this->hasSplashScreen($projectPath, $platform),
            'has_tests' => $this->hasTests($projectPath, $platform),
            'has_ci' => $this->hasCICD($projectPath),
        ];

        // Platform-specific metrics
        switch ($platform) {
            case 'react-native':
                $packageData = $this->parseJsonFile($projectPath, 'package.json');
                $metrics['js_files'] = $this->countFiles($projectPath, '**/*.js');
                $metrics['jsx_files'] = $this->countFiles($projectPath, '**/*.jsx');
                $metrics['ts_files'] = $this->countFiles($projectPath, '**/*.ts');
                $metrics['tsx_files'] = $this->countFiles($projectPath, '**/*.tsx');
                $metrics['dependencies'] = $packageData ? count($packageData['dependencies'] ?? []) : 0;
                $metrics['uses_typescript'] = $this->fileExists($projectPath, 'tsconfig.json');
                $metrics['uses_expo'] = $this->usesExpo($projectPath);
                break;

            case 'flutter':
                $metrics['dart_files'] = $this->countFiles($projectPath, '**/*.dart');
                $metrics['dependencies'] = $this->countFlutterDependencies($projectPath);
                break;

            case 'ios':
                $metrics['swift_files'] = $this->countFiles($projectPath, '**/*.swift');
                $metrics['objc_files'] = $this->countFiles($projectPath, '**/*.m');
                break;

            case 'android':
                $metrics['kotlin_files'] = $this->countFiles($projectPath, '**/*.kt');
                $metrics['java_files'] = $this->countFiles($projectPath, '**/*.java');
                break;
        }

        // Count total lines
        $metrics['total_lines'] = $this->countTotalLines($projectPath, $platform);

        // Record metrics
        $this->recordMetric('mobile', 'platform', $platform);
        $this->recordMetric('mobile', 'total_lines', $metrics['total_lines']);

        $this->log('Collected mobile metrics', 'info', $metrics);

        return $metrics;
    }

    /**
     * {@inheritdoc}
     */
    public function healthCheck(string $projectPath, array $config): array
    {
        $issues = [];
        $score = 100;

        $platform = $this->detectPlatform($projectPath);

        // Platform-specific checks
        switch ($platform) {
            case 'react-native':
                if (!$this->fileExists($projectPath, 'package.json')) {
                    $issues[] = [
                        'severity' => 'critical',
                        'message' => 'Missing package.json',
                    ];
                    $score -= 30;
                }
                if (!$this->fileExists($projectPath, '.watchmanconfig')) {
                    $issues[] = [
                        'severity' => 'info',
                        'message' => 'Missing .watchmanconfig',
                    ];
                    $score -= 5;
                }
                break;

            case 'flutter':
                if (!$this->fileExists($projectPath, 'pubspec.yaml')) {
                    $issues[] = [
                        'severity' => 'critical',
                        'message' => 'Missing pubspec.yaml',
                    ];
                    $score -= 30;
                }
                break;

            case 'ios':
                if (!$this->hasIOSProject($projectPath)) {
                    $issues[] = [
                        'severity' => 'critical',
                        'message' => 'No Xcode project found',
                    ];
                    $score -= 30;
                }
                break;

            case 'android':
                if (!$this->fileExists($projectPath, 'build.gradle')) {
                    $issues[] = [
                        'severity' => 'critical',
                        'message' => 'Missing build.gradle',
                    ];
                    $score -= 30;
                }
                break;
        }

        // Check for app icons
        if (!$this->hasAppIcons($projectPath, $platform)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'App icons missing',
            ];
            $score -= 10;
        }

        // Check for tests
        if (!$this->hasTests($projectPath, $platform)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No tests found',
            ];
            $score -= 15;
        }

        // Check for CI/CD
        if (!$this->hasCICD($projectPath)) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'No CI/CD configuration',
            ];
            $score -= 10;
        }

        // Check for README
        if (!$this->fileExists($projectPath, 'README.md')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing README.md',
            ];
            $score -= 5;
        }

        // Check for .gitignore
        if (!$this->fileExists($projectPath, '.gitignore')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing .gitignore',
            ];
            $score -= 5;
        }

        // Check for security best practices
        if ($this->hasInsecureStorage($projectPath, $platform)) {
            $issues[] = [
                'severity' => 'critical',
                'message' => 'Potential insecure data storage detected',
            ];
            $score -= 20;
        }

        $score = max(0, $score);

        $this->log('Mobile health check completed', 'info', [
            'score' => $score,
            'issues_count' => count($issues),
            'platform' => $platform,
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
            'React Native: package.json, app.json',
            'Flutter: pubspec.yaml, lib/',
            'iOS: *.xcodeproj or *.xcworkspace',
            'Android: build.gradle, app/src/main/',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRecommendedFiles(): array
    {
        return [
            'README.md',
            '.gitignore',
            'App icons for all required sizes',
            'Splash screen assets',
            'tests/ or __tests__/',
            '.github/workflows/* or fastlane/',
            'React Native: metro.config.js',
            'Flutter: analysis_options.yaml',
            'iOS: Podfile',
            'Android: proguard-rules.pro',
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
                'platform' => [
                    'type' => 'string',
                    'enum' => ['react-native', 'flutter', 'ios', 'android', 'xamarin'],
                    'description' => 'Mobile platform/framework',
                ],
                'supports_ios' => [
                    'type' => 'boolean',
                    'description' => 'Project supports iOS',
                ],
                'supports_android' => [
                    'type' => 'boolean',
                    'description' => 'Project supports Android',
                ],
                'min_ios_version' => [
                    'type' => 'string',
                    'description' => 'Minimum iOS version',
                ],
                'min_android_api' => [
                    'type' => 'integer',
                    'description' => 'Minimum Android API level',
                ],
            ],
            'required' => ['platform'],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getBestPractices(): array
    {
        return [
            'Support both iOS and Android for wider reach',
            'Implement proper error handling and crash reporting',
            'Use secure storage for sensitive data',
            'Implement proper app permissions handling',
            'Optimize app size and performance',
            'Provide app icons for all required sizes',
            'Include splash screen with proper sizing',
            'Implement comprehensive unit and integration tests',
            'Use CI/CD for automated builds and deployments',
            'Follow platform-specific design guidelines',
            'Implement proper deep linking',
            'Add analytics and monitoring',
            'Handle offline scenarios gracefully',
            'Optimize images and assets',
            'Keep dependencies up to date',
        ];
    }

    /**
     * Detect mobile platform
     */
    private function detectPlatform(string $projectPath): string
    {
        // React Native
        if ($this->fileExists($projectPath, 'package.json')) {
            $packageData = $this->parseJsonFile($projectPath, 'package.json');
            if ($packageData && isset($packageData['dependencies']['react-native'])) {
                return 'react-native';
            }
        }

        // Flutter
        if ($this->fileExists($projectPath, 'pubspec.yaml')) {
            return 'flutter';
        }

        // iOS
        if ($this->hasIOSProject($projectPath)) {
            return 'ios';
        }

        // Android
        if ($this->fileExists($projectPath, 'build.gradle') &&
            $this->fileExists($projectPath, 'app/src/main')) {
            return 'android';
        }

        return 'unknown';
    }

    /**
     * Check if supports iOS
     */
    private function supportsIOS(string $projectPath, string $platform): bool
    {
        if ($platform === 'ios') {
            return true;
        }

        return $this->fileExists($projectPath, 'ios');
    }

    /**
     * Check if supports Android
     */
    private function supportsAndroid(string $projectPath, string $platform): bool
    {
        if ($platform === 'android') {
            return true;
        }

        return $this->fileExists($projectPath, 'android');
    }

    /**
     * Check for app icons
     */
    private function hasAppIcons(string $projectPath, string $platform): bool
    {
        switch ($platform) {
            case 'react-native':
                return $this->fileExists($projectPath, 'android/app/src/main/res/mipmap-*') ||
                       $this->fileExists($projectPath, 'ios/*/Images.xcassets/AppIcon.appiconset');

            case 'flutter':
                return $this->fileExists($projectPath, 'android/app/src/main/res/mipmap-*') ||
                       $this->fileExists($projectPath, 'ios/Runner/Assets.xcassets/AppIcon.appiconset');

            case 'ios':
                return $this->countFiles($projectPath, '**/AppIcon.appiconset') > 0;

            case 'android':
                return $this->fileExists($projectPath, 'app/src/main/res/mipmap-*');

            default:
                return false;
        }
    }

    /**
     * Check for splash screen
     */
    private function hasSplashScreen(string $projectPath, string $platform): bool
    {
        switch ($platform) {
            case 'react-native':
                return $this->fileExists($projectPath, 'android/app/src/main/res/drawable/launch_screen*') ||
                       $this->fileExists($projectPath, 'ios/*/LaunchScreen*');

            case 'flutter':
                return $this->fileExists($projectPath, 'android/app/src/main/res/drawable/launch_background*') ||
                       $this->fileExists($projectPath, 'ios/Runner/Assets.xcassets/LaunchImage*');

            case 'ios':
                return $this->countFiles($projectPath, '**/LaunchScreen*') > 0;

            case 'android':
                return $this->fileExists($projectPath, 'app/src/main/res/drawable/launch_*');

            default:
                return false;
        }
    }

    /**
     * Check for tests
     */
    private function hasTests(string $projectPath, string $platform): bool
    {
        switch ($platform) {
            case 'react-native':
                return $this->fileExists($projectPath, '__tests__') ||
                       $this->fileExists($projectPath, 'e2e') ||
                       $this->countFiles($projectPath, '**/*.test.js') > 0;

            case 'flutter':
                return $this->fileExists($projectPath, 'test') ||
                       $this->countFiles($projectPath, '**/*_test.dart') > 0;

            case 'ios':
                return $this->fileExists($projectPath, '*Tests') ||
                       $this->countFiles($projectPath, '**/*Tests.swift') > 0;

            case 'android':
                return $this->fileExists($projectPath, 'app/src/test') ||
                       $this->fileExists($projectPath, 'app/src/androidTest');

            default:
                return false;
        }
    }

    /**
     * Check for CI/CD
     */
    private function hasCICD(string $projectPath): bool
    {
        return $this->fileExists($projectPath, '.github/workflows') ||
               $this->fileExists($projectPath, '.gitlab-ci.yml') ||
               $this->fileExists($projectPath, 'fastlane') ||
               $this->fileExists($projectPath, '.circleci');
    }

    /**
     * Check if uses Expo
     */
    private function usesExpo(string $projectPath): bool
    {
        $packageData = $this->parseJsonFile($projectPath, 'package.json');
        return $packageData && isset($packageData['dependencies']['expo']);
    }

    /**
     * Count Flutter dependencies
     */
    private function countFlutterDependencies(string $projectPath): int
    {
        $pubspec = $this->readFile($projectPath, 'pubspec.yaml');
        if (!$pubspec) {
            return 0;
        }

        $lines = explode("\n", $pubspec);
        $inDeps = false;
        $count = 0;

        foreach ($lines as $line) {
            if (strpos($line, 'dependencies:') !== false) {
                $inDeps = true;
                continue;
            }
            if ($inDeps && preg_match('/^\s{2}\w+:/', $line)) {
                $count++;
            } elseif ($inDeps && preg_match('/^\w+:/', $line)) {
                break;
            }
        }

        return $count;
    }

    /**
     * Count total lines
     */
    private function countTotalLines(string $projectPath, string $platform): int
    {
        $extensions = [];
        
        switch ($platform) {
            case 'react-native':
                $extensions = ['js', 'jsx', 'ts', 'tsx'];
                break;
            case 'flutter':
                $extensions = ['dart'];
                break;
            case 'ios':
                $extensions = ['swift', 'm', 'h'];
                break;
            case 'android':
                $extensions = ['kt', 'java'];
                break;
        }

        $totalLines = 0;
        foreach ($extensions as $ext) {
            $files = $this->findFiles($projectPath, "**/*.{$ext}");
            foreach ($files as $file) {
                if (is_file($file) && 
                    strpos($file, 'node_modules') === false &&
                    strpos($file, 'build') === false) {
                    $totalLines += count(file($file));
                }
            }
        }

        return $totalLines;
    }

    /**
     * Check for iOS project
     */
    private function hasIOSProject(string $projectPath): bool
    {
        return $this->countFiles($projectPath, '*.xcodeproj') > 0 ||
               $this->countFiles($projectPath, '*.xcworkspace') > 0;
    }

    /**
     * Check for insecure storage
     */
    private function hasInsecureStorage(string $projectPath, string $platform): bool
    {
        // Simple heuristic check - would be more comprehensive in production
        switch ($platform) {
            case 'react-native':
                $files = $this->findFiles($projectPath, '**/*.js');
                foreach (array_slice($files, 0, 10) as $file) {
                    if (is_file($file)) {
                        $content = @file_get_contents($file);
                        if ($content && strpos($content, 'AsyncStorage.setItem') !== false) {
                            // Should check if sensitive data without encryption
                            return true;
                        }
                    }
                }
                break;
        }

        return false;
    }
}
