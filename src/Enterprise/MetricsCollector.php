<?php

declare(strict_types=1);

/**
 * Metrics Collector for MokoStandards
 *
 * Provides observability and monitoring capabilities:
 * - Execution time tracking with timers
 * - Success/failure rate monitoring
 * - Counter and gauge metrics
 * - Histogram support for distributions
 * - Prometheus format export
 * - Time series data collection
 *
 * Example usage:
 * ```php
 * $metrics = new MetricsCollector('my_service');
 * $metrics->increment('requests_total');
 * $metrics->setGauge('cpu_usage', 45.5);
 * 
 * // Timing operations
 * $timer = $metrics->startTimer('operation');
 * // ... do work ...
 * $timer->stop();
 * 
 * // Export for monitoring
 * echo $metrics->exportPrometheus();
 * ```
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

use DateTime;
use DateTimeZone;

/**
 * Timer class for timing operations
 */
class MetricsTimer
{
    private MetricsCollector $collector;
    private string $metricName;
    private array $labels;
    private float $startTime;

    public function __construct(MetricsCollector $collector, string $metricName, array $labels = [])
    {
        $this->collector = $collector;
        $this->metricName = $metricName;
        $this->labels = $labels;
        $this->startTime = microtime(true);
    }

    public function stop(bool $success = true): float
    {
        $duration = microtime(true) - $this->startTime;
        $this->collector->observe($this->metricName . '_duration_seconds', $duration, $this->labels);
        
        if ($success) {
            $this->collector->increment($this->metricName . '_success_total', 1, $this->labels);
        } else {
            $this->collector->increment($this->metricName . '_failure_total', 1, $this->labels);
        }
        
        return $duration;
    }
}

/**
 * Metrics collector for monitoring and observability
 */
class MetricsCollector
{
    private const VERSION = '04.00.01';

    private string $serviceName;
    private array $counters = [];
    private array $gauges = [];
    private array $histograms = [];
    private float $startTime;

    public function __construct(string $serviceName = 'mokostandards')
    {
        $this->serviceName = $serviceName;
        $this->startTime = microtime(true);
    }

    /**
     * Increment a counter metric
     *
     * @param string $metricName Name of the metric
     * @param int $value Value to increment by
     * @param array<string, string> $labels Optional labels for the metric
     */
    public function increment(string $metricName, int $value = 1, array $labels = []): void
    {
        $key = $this->makeKey($metricName, $labels);
        if (!isset($this->counters[$key])) {
            $this->counters[$key] = 0;
        }
        $this->counters[$key] += $value;
    }

    /**
     * Set a gauge metric
     *
     * @param string $metricName Name of the metric
     * @param float $value Value to set
     * @param array<string, string> $labels Optional labels for the metric
     */
    public function setGauge(string $metricName, float $value, array $labels = []): void
    {
        $key = $this->makeKey($metricName, $labels);
        $this->gauges[$key] = $value;
    }

    /**
     * Observe a value for histogram
     *
     * @param string $metricName Name of the metric
     * @param float $value Value to observe
     * @param array<string, string> $labels Optional labels for the metric
     */
    public function observe(string $metricName, float $value, array $labels = []): void
    {
        $key = $this->makeKey($metricName, $labels);
        if (!isset($this->histograms[$key])) {
            $this->histograms[$key] = [];
        }
        $this->histograms[$key][] = $value;
    }

    /**
     * Start a timer for timing operations
     *
     * @param string $metricName Name of the metric
     * @param array<string, string> $labels Optional labels for the metric
     * @return MetricsTimer Timer instance
     */
    public function startTimer(string $metricName, array $labels = []): MetricsTimer
    {
        return new MetricsTimer($this, $metricName, $labels);
    }

    /**
     * Create a metric key with labels
     *
     * @param string $metricName Name of the metric
     * @param array<string, string> $labels Optional labels
     * @return string Metric key string
     */
    private function makeKey(string $metricName, array $labels = []): string
    {
        if (empty($labels)) {
            return $metricName;
        }
        
        ksort($labels);
        $labelPairs = [];
        foreach ($labels as $key => $value) {
            $labelPairs[] = sprintf('%s="%s"', $key, $value);
        }
        
        return sprintf('%s{%s}', $metricName, implode(',', $labelPairs));
    }

    /**
     * Get current counter value
     *
     * @param string $metricName Name of the metric
     * @return int Counter value
     */
    public function getCounter(string $metricName): int
    {
        return $this->counters[$metricName] ?? 0;
    }

    /**
     * Get current gauge value
     *
     * @param string $metricName Name of the metric
     * @return float|null Gauge value or null if not set
     */
    public function getGauge(string $metricName): ?float
    {
        return $this->gauges[$metricName] ?? null;
    }

    /**
     * Get statistics for a histogram
     *
     * @param string $metricName Name of the metric
     * @return array<string, float> Dictionary with min, max, avg, count, sum
     */
    public function getHistogramStats(string $metricName): array
    {
        $values = $this->histograms[$metricName] ?? [];
        
        if (empty($values)) {
            return ['count' => 0, 'min' => 0.0, 'max' => 0.0, 'avg' => 0.0, 'sum' => 0.0];
        }
        
        $sum = array_sum($values);
        return [
            'count' => count($values),
            'min' => min($values),
            'max' => max($values),
            'avg' => $sum / count($values),
            'sum' => $sum
        ];
    }

    /**
     * Export metrics in Prometheus format
     *
     * @return string Metrics in Prometheus text format
     */
    public function exportPrometheus(): string
    {
        $lines = [];
        $now = new DateTime('now', new DateTimeZone('UTC'));
        
        $lines[] = sprintf('# Metrics for %s', $this->serviceName);
        $lines[] = sprintf('# Generated at %s', $now->format('c'));
        $lines[] = '';
        
        // Export counters
        foreach ($this->counters as $key => $value) {
            $lines[] = sprintf('# TYPE %s counter', $this->stripLabels($key));
            $lines[] = sprintf('%s %d', $key, $value);
        }
        
        // Export gauges
        foreach ($this->gauges as $key => $value) {
            $lines[] = sprintf('# TYPE %s gauge', $this->stripLabels($key));
            $lines[] = sprintf('%s %s', $key, $value);
        }
        
        // Export histograms
        foreach ($this->histograms as $key => $values) {
            if (!empty($values)) {
                $stats = $this->getHistogramStats($key);
                $lines[] = sprintf('# TYPE %s histogram', $this->stripLabels($key));
                $lines[] = sprintf('%s_count %d', $key, $stats['count']);
                $lines[] = sprintf('%s_sum %s', $key, $stats['sum']);
                $lines[] = sprintf('%s_min %s', $key, $stats['min']);
                $lines[] = sprintf('%s_max %s', $key, $stats['max']);
                $lines[] = sprintf('%s_avg %s', $key, $stats['avg']);
            }
        }
        
        // Add uptime
        $uptime = microtime(true) - $this->startTime;
        $lines[] = '# TYPE process_uptime_seconds gauge';
        $lines[] = sprintf('process_uptime_seconds %.2f', $uptime);
        
        return implode("\n", $lines);
    }

    /**
     * Strip labels from metric key
     *
     * @param string $key Metric key
     * @return string Metric name without labels
     */
    private function stripLabels(string $key): string
    {
        $pos = strpos($key, '{');
        return $pos !== false ? substr($key, 0, $pos) : $key;
    }

    /**
     * Print a summary of all metrics
     */
    public function printSummary(): void
    {
        echo "\n" . str_repeat('=', 60) . "\n";
        echo "Metrics Summary for {$this->serviceName}\n";
        echo str_repeat('=', 60) . "\n";
        
        if (!empty($this->counters)) {
            echo "\nCounters:\n";
            ksort($this->counters);
            foreach ($this->counters as $key => $value) {
                echo "  {$key}: {$value}\n";
            }
        }
        
        if (!empty($this->gauges)) {
            echo "\nGauges:\n";
            ksort($this->gauges);
            foreach ($this->gauges as $key => $value) {
                echo "  {$key}: {$value}\n";
            }
        }
        
        if (!empty($this->histograms)) {
            echo "\nHistograms:\n";
            $keys = array_keys($this->histograms);
            sort($keys);
            foreach ($keys as $key) {
                $stats = $this->getHistogramStats($key);
                echo "  {$key}:\n";
                echo sprintf("    Count: %d\n", $stats['count']);
                echo sprintf("    Min:   %.4f\n", $stats['min']);
                echo sprintf("    Max:   %.4f\n", $stats['max']);
                echo sprintf("    Avg:   %.4f\n", $stats['avg']);
            }
        }
        
        $uptime = microtime(true) - $this->startTime;
        echo sprintf("\nUptime: %.2f seconds\n", $uptime);
        echo str_repeat('=', 60) . "\n\n";
    }

    public function getVersion(): string
    {
        return self::VERSION;
    }
}
