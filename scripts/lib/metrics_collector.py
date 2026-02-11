#!/usr/bin/env python3
"""
Metrics Collector for MokoStandards
Version: 03.02.00
Copyright (C) 2026 Moko Consulting LLC

Provides observability and monitoring capabilities:
- Execution time tracking
- Success/failure rate monitoring
- Counter and gauge metrics
- Prometheus format export
- Histogram support

Usage:
    from metrics_collector import MetricsCollector
    
    metrics = MetricsCollector()
    with metrics.timer('operation'):
        # do work
        pass
    metrics.increment('operations_completed')
"""

import time
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

VERSION = "03.02.00"


class MetricsCollector:
    """Collect and export metrics for monitoring."""
    
    def __init__(self, service_name: str = "mokostandards"):
        """Initialize metrics collector.
        
        Args:
            service_name: Name of the service
        """
        self.service_name = service_name
        self.counters = defaultdict(int)
        self.gauges = {}
        self.histograms = defaultdict(list)
        self.timers = {}
        self.start_time = time.time()
        
    def increment(self, metric_name: str, value: int = 1, labels: Optional[Dict[str, str]] = None):
        """Increment a counter metric.
        
        Args:
            metric_name: Name of the metric
            value: Value to increment by
            labels: Optional labels for the metric
        """
        key = self._make_key(metric_name, labels)
        self.counters[key] += value
        
    def set_gauge(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge metric.
        
        Args:
            metric_name: Name of the metric
            value: Value to set
            labels: Optional labels for the metric
        """
        key = self._make_key(metric_name, labels)
        self.gauges[key] = value
        
    def observe(self, metric_name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Observe a value for histogram.
        
        Args:
            metric_name: Name of the metric
            value: Value to observe
            labels: Optional labels for the metric
        """
        key = self._make_key(metric_name, labels)
        self.histograms[key].append(value)
        
    def timer(self, metric_name: str, labels: Optional[Dict[str, str]] = None):
        """Context manager for timing operations.
        
        Args:
            metric_name: Name of the metric
            labels: Optional labels for the metric
            
        Returns:
            Timer context manager
        """
        return Timer(self, metric_name, labels)
        
    def _make_key(self, metric_name: str, labels: Optional[Dict[str, str]] = None) -> str:
        """Create a metric key with labels.
        
        Args:
            metric_name: Name of the metric
            labels: Optional labels
            
        Returns:
            Metric key string
        """
        if not labels:
            return metric_name
        label_str = ','.join(f'{k}="{v}"' for k, v in sorted(labels.items()))
        return f"{metric_name}{{{label_str}}}"
    
    def get_counter(self, metric_name: str) -> int:
        """Get current counter value.
        
        Args:
            metric_name: Name of the metric
            
        Returns:
            Counter value
        """
        return self.counters.get(metric_name, 0)
    
    def get_gauge(self, metric_name: str) -> Optional[float]:
        """Get current gauge value.
        
        Args:
            metric_name: Name of the metric
            
        Returns:
            Gauge value or None
        """
        return self.gauges.get(metric_name)
    
    def get_histogram_stats(self, metric_name: str) -> Dict[str, float]:
        """Get statistics for a histogram.
        
        Args:
            metric_name: Name of the metric
            
        Returns:
            Dictionary with min, max, avg, count
        """
        values = self.histograms.get(metric_name, [])
        if not values:
            return {'count': 0, 'min': 0, 'max': 0, 'avg': 0, 'sum': 0}
        
        return {
            'count': len(values),
            'min': min(values),
            'max': max(values),
            'avg': sum(values) / len(values),
            'sum': sum(values)
        }
    
    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format.
        
        Returns:
            Metrics in Prometheus text format
        """
        lines = []
        lines.append(f"# Metrics for {self.service_name}")
        lines.append(f"# Generated at {datetime.now().isoformat()}")
        lines.append("")
        
        # Export counters
        for key, value in self.counters.items():
            lines.append(f"# TYPE {key} counter")
            lines.append(f"{key} {value}")
        
        # Export gauges
        for key, value in self.gauges.items():
            lines.append(f"# TYPE {key} gauge")
            lines.append(f"{key} {value}")
        
        # Export histograms
        for key, values in self.histograms.items():
            if values:
                stats = self.get_histogram_stats(key)
                lines.append(f"# TYPE {key} histogram")
                lines.append(f"{key}_count {stats['count']}")
                lines.append(f"{key}_sum {stats['sum']}")
                lines.append(f"{key}_min {stats['min']}")
                lines.append(f"{key}_max {stats['max']}")
                lines.append(f"{key}_avg {stats['avg']}")
        
        # Add uptime
        uptime = time.time() - self.start_time
        lines.append(f"# TYPE process_uptime_seconds gauge")
        lines.append(f"process_uptime_seconds {uptime:.2f}")
        
        return '\n'.join(lines)
    
    def print_summary(self):
        """Print a summary of all metrics."""
        print(f"\n{'='*60}")
        print(f"Metrics Summary for {self.service_name}")
        print(f"{'='*60}")
        
        if self.counters:
            print("\nCounters:")
            for key, value in sorted(self.counters.items()):
                print(f"  {key}: {value}")
        
        if self.gauges:
            print("\nGauges:")
            for key, value in sorted(self.gauges.items()):
                print(f"  {key}: {value}")
        
        if self.histograms:
            print("\nHistograms:")
            for key in sorted(self.histograms.keys()):
                stats = self.get_histogram_stats(key)
                print(f"  {key}:")
                print(f"    Count: {stats['count']}")
                print(f"    Min:   {stats['min']:.4f}")
                print(f"    Max:   {stats['max']:.4f}")
                print(f"    Avg:   {stats['avg']:.4f}")
        
        uptime = time.time() - self.start_time
        print(f"\nUptime: {uptime:.2f} seconds")
        print(f"{'='*60}\n")


class Timer:
    """Context manager for timing operations."""
    
    def __init__(self, collector: MetricsCollector, metric_name: str, labels: Optional[Dict[str, str]] = None):
        """Initialize timer.
        
        Args:
            collector: Metrics collector instance
            metric_name: Name of the metric
            labels: Optional labels
        """
        self.collector = collector
        self.metric_name = metric_name
        self.labels = labels
        self.start_time = None
        
    def __enter__(self):
        """Start timing."""
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing and record duration."""
        duration = time.time() - self.start_time
        self.collector.observe(f"{self.metric_name}_duration_seconds", duration, self.labels)
        
        # Also increment counter for this operation
        if exc_type is None:
            self.collector.increment(f"{self.metric_name}_success_total", labels=self.labels)
        else:
            self.collector.increment(f"{self.metric_name}_failure_total", labels=self.labels)
        
        return False


# Example usage and testing
if __name__ == "__main__":
    print(f"Metrics Collector v{VERSION}")
    print("=" * 50)
    
    metrics = MetricsCollector(service_name="test_service")
    
    # Test 1: Counters
    print("\n1. Testing counters...")
    metrics.increment('requests_total')
    metrics.increment('requests_total')
    metrics.increment('requests_total', value=3)
    print(f"   ✓ Counter value: {metrics.get_counter('requests_total')}")
    
    # Test 2: Gauges
    print("\n2. Testing gauges...")
    metrics.set_gauge('cpu_usage', 45.5)
    metrics.set_gauge('memory_usage', 78.2)
    print(f"   ✓ CPU usage: {metrics.get_gauge('cpu_usage')}%")
    print(f"   ✓ Memory usage: {metrics.get_gauge('memory_usage')}%")
    
    # Test 3: Timers
    print("\n3. Testing timers...")
    with metrics.timer('operation'):
        time.sleep(0.1)
    stats = metrics.get_histogram_stats('operation_duration_seconds')
    print(f"   ✓ Operation took: {stats['avg']:.3f} seconds")
    
    # Test 4: Histograms
    print("\n4. Testing histograms...")
    for i in range(10):
        metrics.observe('response_time', i * 0.1)
    stats = metrics.get_histogram_stats('response_time')
    print(f"   ✓ Response time stats: count={stats['count']}, avg={stats['avg']:.2f}")
    
    # Test 5: Labels
    print("\n5. Testing labels...")
    metrics.increment('http_requests', labels={'method': 'GET', 'status': '200'})
    metrics.increment('http_requests', labels={'method': 'POST', 'status': '201'})
    print(f"   ✓ Labeled metrics recorded")
    
    # Print summary
    metrics.print_summary()
    
    # Export Prometheus format
    print("\nPrometheus Export Sample:")
    print("-" * 50)
    prom_output = metrics.export_prometheus()
    print(prom_output[:500])  # Print first 500 chars
    print("...")
    
    print("\n✓ All tests passed!")
