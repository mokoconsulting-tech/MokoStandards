[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoStandards Monitoring Setup

This directory contains monitoring and alerting configurations for the MokoStandards automation scripts and infrastructure.

## Overview

The monitoring infrastructure provides visibility into:
- Script execution metrics and performance
- Success/failure rates and trends
- API rate limit usage and availability
- Circuit breaker states for fault tolerance
- Security findings and vulnerabilities
- System health and operational status

## Files

### `grafana-dashboard.json`
Grafana dashboard configuration for visualizing MokoStandards metrics.

**Panels included:**
1. **Script Execution Rate** - Time series showing execution rates by script and status
2. **Success Rate Gauge** - Real-time success percentage with threshold indicators
3. **GitHub API Rate Limit Gauge** - Remaining API calls visualization
4. **API Rate Limit Usage Over Time** - Historical API usage trends
5. **Circuit Breaker States Table** - Current state of all circuit breakers
6. **Script Execution Duration** - Performance trends with p50/p95 percentiles
7. **Recent Script Operations Table** - Latest script execution status and timestamps
8. **Success vs Failure Rates** - Stacked bar chart comparing success/failure counts

### `alerts-config.yml`
Prometheus AlertManager rules for automated alerting.

**Alert rules:**
1. **HighScriptFailureRate** - Warning when failure rate >5%
2. **CriticalScriptFailureRate** - Critical alert when failure rate >20%
3. **HighAPIRateLimitUsage** - Warning when API usage >90%
4. **CriticalAPIRateLimitUsage** - Critical alert when API usage >95%
5. **CircuitBreakerOpen** - Notification when circuit breaker opens
6. **CircuitBreakerStuckOpen** - Critical alert when breaker stays open >10m
7. **SecurityFindingsDetected** - Warning on new security findings
8. **HighSeveritySecurityFinding** - Critical alert for high/critical severity findings
9. **SlowScriptExecution** - Warning when p95 execution time >300s
10. **NoScriptExecutions** - Info alert when no executions detected for 15m
11. **APIRateLimitResetSoon** - Info notification before rate limit reset

## Prerequisites

### Required Components
- **Prometheus** - Metrics collection and storage
- **Grafana** - Dashboard visualization
- **AlertManager** - Alert routing and notification

### Supported Prometheus Exporters
The monitoring configuration expects metrics from application instrumentation. Ensure your scripts export the following metrics:

#### Required Metrics
```
# Script execution counters
moko_script_executions_total{script_name, status}

# Script duration histograms
moko_script_duration_seconds_bucket{script_name, le}

# API rate limit gauges
moko_api_rate_limit_remaining{api}
moko_api_rate_limit_total{api}
moko_api_rate_limit_reset_timestamp_seconds{api}

# Circuit breaker state (0=CLOSED, 1=OPEN, 2=HALF_OPEN)
moko_circuit_breaker_state{service}

# Security findings counter
moko_security_findings_total{severity, finding_type}

# Last execution timestamp
moko_script_last_execution_timestamp_seconds{script_name, status}
```

## Setup Instructions

### 1. Install Prometheus

```bash
# Download and install Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-*.tar.gz
cd prometheus-*
```

Configure Prometheus to scrape your application metrics by editing `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'moko-standards'
    static_configs:
      - targets: ['localhost:9090']  # Adjust to your metrics endpoint
```

### 2. Configure AlertManager

```bash
# Copy the alerts configuration
cp docs/monitoring/alerts-config.yml /etc/prometheus/rules/

# Update prometheus.yml to include the alert rules
# Add under 'rule_files:' section:
rule_files:
  - "/etc/prometheus/rules/alerts-config.yml"

# Configure AlertManager for notifications (edit alertmanager.yml)
```

Example AlertManager notification configuration:

```yaml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'team-notifications'

receivers:
  - name: 'team-notifications'
    email_configs:
      - to: 'devops@example.com'
        from: 'alertmanager@example.com'
        smarthost: 'smtp.example.com:587'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        channel: '#moko-alerts'
```

### 3. Import Grafana Dashboard

**Option A: Via Grafana UI**
1. Log in to Grafana
2. Navigate to Dashboards → Import
3. Upload `grafana-dashboard.json` or paste its contents
4. Select your Prometheus datasource
5. Click Import

**Option B: Via API**
```bash
curl -X POST http://localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d @docs/monitoring/grafana-dashboard.json
```

**Option C: Provisioning**
Copy the dashboard to Grafana's provisioning directory:
```bash
cp docs/monitoring/grafana-dashboard.json /etc/grafana/provisioning/dashboards/
```

### 4. Verify Setup

1. **Check Prometheus targets:**
   - Open http://localhost:9090/targets
   - Verify your application target is UP

2. **Test AlertManager:**
   ```bash
   # Check alert rules
   curl http://localhost:9090/api/v1/rules | jq .
   
   # View active alerts
   curl http://localhost:9090/api/v1/alerts | jq .
   ```

3. **Access Grafana Dashboard:**
   - Open http://localhost:3000
   - Navigate to the "MokoStandards - Script Monitoring Dashboard"
   - Verify panels are displaying data

## Instrumentation Guide

To enable monitoring in your scripts, instrument them with Prometheus client libraries:

### Python Example
```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
script_executions = Counter('moko_script_executions_total', 
                           'Total script executions', 
                           ['script_name', 'status'])

script_duration = Histogram('moko_script_duration_seconds',
                           'Script execution duration',
                           ['script_name'])

api_rate_limit = Gauge('moko_api_rate_limit_remaining',
                      'API rate limit remaining',
                      ['api'])

# Start metrics server
start_http_server(9090)

# Instrument your code
@script_duration.labels(script_name='my_script').time()
def my_script():
    try:
        # Script logic here
        result = do_work()
        script_executions.labels(script_name='my_script', status='success').inc()
        return result
    except Exception as e:
        script_executions.labels(script_name='my_script', status='failure').inc()
        raise
```

### Bash Example
```bash
# Use curl to push metrics to Pushgateway
push_metric() {
    local metric_name=$1
    local metric_value=$2
    local labels=$3
    
    echo "${metric_name}{${labels}} ${metric_value}" | \
        curl --data-binary @- http://localhost:9091/metrics/job/moko_scripts
}

# Example usage
push_metric "moko_script_executions_total" 1 "script_name=\"backup.sh\",status=\"success\""
```

## Customization

### Adjusting Alert Thresholds

Edit `alerts-config.yml` to modify thresholds:
- Script failure rate: Change `> 5` to your desired percentage
- API rate limit: Adjust `> 90` for earlier/later warnings
- Execution duration: Modify `> 300` to match your performance SLOs

### Adding Custom Panels

Use Grafana's UI to:
1. Add new panels to the dashboard
2. Configure queries using PromQL
3. Export the updated dashboard JSON
4. Replace `grafana-dashboard.json` with the new version

### Notification Channels

Configure additional AlertManager receivers for:
- PagerDuty
- Microsoft Teams
- Webhooks
- OpsGenie
- Custom integrations

## Troubleshooting

### No Data Appearing in Grafana
1. Verify Prometheus is scraping metrics: Check `/targets` endpoint
2. Test metrics endpoint directly: `curl http://your-app:9090/metrics`
3. Check Prometheus logs for scrape errors
4. Verify datasource configuration in Grafana

### Alerts Not Firing
1. Check alert rule evaluation: http://localhost:9090/alerts
2. Verify AlertManager is configured in prometheus.yml
3. Check AlertManager logs for routing issues
4. Test with manual alert: `amtool alert add`

### High Memory Usage
1. Reduce metrics retention period in Prometheus
2. Adjust scrape intervals to reduce data volume
3. Use recording rules to pre-aggregate metrics
4. Consider using Prometheus federation for scale

## Best Practices

1. **Retention**: Configure appropriate data retention based on compliance requirements
2. **Backup**: Regularly backup Prometheus data and Grafana dashboards
3. **Testing**: Test alert rules regularly using `promtool` and alert simulators
4. **Documentation**: Keep runbooks updated for alert response procedures
5. **Tuning**: Review and adjust thresholds based on actual operational patterns
6. **Security**: Use authentication and TLS for Prometheus/Grafana endpoints
7. **High Availability**: Deploy Prometheus/AlertManager in HA mode for production

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [AlertManager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [PromQL Tutorial](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboard Best Practices](https://grafana.com/docs/grafana/latest/best-practices/)

## Support

For issues or questions:
1. Check existing documentation and runbooks
2. Review Prometheus/Grafana logs
3. Consult the troubleshooting section above
4. Open an issue in the MokoStandards repository

## License

This monitoring configuration is part of the MokoStandards project and follows the same license.
