<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Training
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/training/session-1-libraries-overview.md
VERSION: 03.02.00
BRIEF: Session 1 - Enterprise Libraries Overview training materials
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Session 1: Enterprise Libraries Overview

**Duration**: 2 hours  
**Format**: Presentation + Live Demos  
**Prerequisite**: Basic Python and Git knowledge

---

## Session Objectives

By the end of this session, you will:
- ✅ Understand all 10 enterprise libraries and their purposes
- ✅ Know when to use each library in your scripts
- ✅ See live demonstrations of each library in action
- ✅ Complete basic hands-on exercises
- ✅ Navigate library documentation effectively

---

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 0:00-0:15 | Introduction & Setup | Presentation |
| 0:15-0:45 | Core Libraries (1-5) | Demo + Discussion |
| 0:45-1:15 | Advanced Libraries (6-10) | Demo + Discussion |
| 1:15-1:40 | Hands-on Exercises | Interactive |
| 1:40-2:00 | Q&A and Wrap-up | Discussion |

---

## Part 1: Introduction (15 minutes)

### What Are Enterprise Libraries?

Enterprise libraries are production-ready, reusable code modules that provide:
- ✅ **Consistency**: Standard patterns across all automation
- ✅ **Reliability**: Battle-tested error handling and resilience
- ✅ **Security**: Built-in security validation and compliance
- ✅ **Observability**: Audit logging and metrics collection
- ✅ **Maintainability**: Well-documented, tested code

### The 10 Libraries Overview

| # | Library | Purpose | Priority |
|---|---------|---------|----------|
| 1 | Enterprise Audit | Transaction tracking & compliance | CRITICAL |
| 2 | API Client | Rate-limited, resilient API calls | CRITICAL |
| 3 | CLI Framework | Standardized command-line interface | HIGH |
| 4 | Common Utilities | Shared helper functions | HIGH |
| 5 | Config Manager | Environment-aware configuration | HIGH |
| 6 | Doc Helper | Documentation generation | MEDIUM |
| 7 | Error Recovery | Automatic retry & checkpointing | HIGH |
| 8 | Metrics Collector | Observability & monitoring | MEDIUM |
| 9 | Security Validator | Security scanning & validation | HIGH |
| 10 | Transaction Manager | Atomic operations & rollback | MEDIUM |

---

## Part 2: Core Libraries (30 minutes)

### 1. Enterprise Audit Library ⭐ CRITICAL

**File**: `scripts/lib/enterprise_audit.py` (470 lines)

**Purpose**: Structured audit logging with transaction tracking for compliance and debugging.

**Key Features**:
- UUID-based transaction tracking
- Security event logging
- JSON structured logs
- Automatic log rotation
- SIEM integration ready

**When to Use**:
- ✅ Any script that modifies resources
- ✅ Scripts handling sensitive data
- ✅ Operations requiring compliance trails
- ✅ Multi-step workflows

**Live Demo**:
```python
from scripts.lib.enterprise_audit import AuditLogger

# Initialize logger for your service
logger = AuditLogger(service='demo_script', retention_days=90)

# Start a transaction
with logger.transaction('user_provisioning') as txn:
    # Log individual steps
    txn.log_event('create_user', {
        'username': 'john.doe',
        'email': 'john@example.com',
        'status': 'success'
    })
    
    txn.log_event('assign_permissions', {
        'permissions': ['read', 'write'],
        'status': 'success'
    })
    
    # Transaction automatically completes

# Log security events
logger.log_security_event(
    event_type='login_attempt',
    severity='INFO',
    details={'user': 'admin', 'ip': '192.168.1.1'}
)

# Generate audit report
report = logger.generate_report(
    start_date='2026-01-01',
    end_date='2026-02-01',
    filter_by={'service': 'demo_script'}
)
print(f"Found {len(report)} audit events")
```

**Exercise 1.1**: Create an audit trail
```python
# TODO: Create an audit logger and log a transaction with 3 steps
# Steps: validate_input -> process_data -> save_results
# Include relevant metadata for each step
```

---

### 2. API Client Library ⭐ CRITICAL

**File**: `scripts/lib/api_client.py` (580 lines)

**Purpose**: Rate-limited, resilient API interactions with automatic retry and circuit breaker.

**Key Features**:
- Configurable rate limiting (requests per hour)
- Exponential backoff retry logic
- Circuit breaker pattern for failing endpoints
- Response caching with TTL
- Request metrics tracking

**When to Use**:
- ✅ Any GitHub API interactions
- ✅ External API calls
- ✅ High-volume API operations
- ✅ Rate-limited APIs

**Live Demo**:
```python
from scripts.lib.api_client import GitHubClient, RateLimitConfig
import os

# Configure rate limiting
rate_config = RateLimitConfig(
    max_requests_per_hour=5000,
    burst_size=100,
    enable_caching=True,
    cache_ttl=300  # 5 minutes
)

# Initialize client
client = GitHubClient(
    token=os.getenv('GITHUB_TOKEN'),
    rate_limit_config=rate_config
)

# Automatic rate limiting in action
try:
    # List repositories (cached for 5 minutes)
    repos = client.list_repos(org='mokoconsulting-tech')
    print(f"Found {len(repos)} repositories")
    
    # Get repository details (with retry and circuit breaker)
    for repo in repos[:5]:
        details = client.get_repo(org='mokoconsulting-tech', repo=repo['name'])
        print(f"Repo: {details['name']}, Stars: {details['stargazers_count']}")
        
except Exception as e:
    # Circuit breaker tripped or rate limit exceeded
    print(f"API error: {e}")
    
# Check rate limit status
status = client.get_rate_limit_status()
print(f"Remaining requests: {status['remaining']}/{status['limit']}")
```

**Exercise 1.2**: Use API client with rate limiting
```python
# TODO: Create a GitHubClient and list all issues in a repository
# Configure rate limiting to 1000 requests per hour
# Print the title of each issue
```

---

### 3. CLI Framework Library

**File**: `scripts/lib/cli_framework.py` (470 lines)

**Purpose**: Standardized command-line interface for all automation scripts.

**Key Features**:
- CLIApp base class for consistent structure
- Common arguments (--verbose, --dry-run, --json, --config)
- Integrated logging setup
- Enterprise library integration
- Standard error handling and exit codes

**When to Use**:
- ✅ Every new automation script
- ✅ Scripts requiring command-line arguments
- ✅ Scripts needing consistent error handling
- ✅ User-facing automation tools

**Live Demo**:
```python
from scripts.lib.cli_framework import CLIApp
import argparse

class MyAutomationScript(CLIApp):
    def setup_arguments(self, parser: argparse.ArgumentParser):
        """Add script-specific arguments"""
        parser.add_argument('--org', required=True, help='GitHub organization')
        parser.add_argument('--repo', help='Specific repository (optional)')
        
    def run(self):
        """Main script logic"""
        org = self.args.org
        repo = self.args.repo
        
        self.logger.info(f"Processing organization: {org}")
        
        if self.args.dry_run:
            self.logger.warning("DRY RUN: No changes will be made")
            
        # Your automation logic here
        results = self.process_organization(org, repo)
        
        if self.args.json:
            self.output_json(results)
        else:
            self.output_text(results)
            
        return 0  # Success exit code
        
    def process_organization(self, org, repo=None):
        """Business logic"""
        return {
            'org': org,
            'processed': 42,
            'errors': 0
        }

if __name__ == '__main__':
    app = MyAutomationScript()
    exit(app.execute())
```

**Usage**:
```bash
# Standard usage
python my_script.py --org mokoconsulting-tech

# Dry run mode
python my_script.py --org mokoconsulting-tech --dry-run

# Verbose logging
python my_script.py --org mokoconsulting-tech --verbose

# JSON output
python my_script.py --org mokoconsulting-tech --json
```

**Exercise 1.3**: Create a CLI application
```python
# TODO: Create a CLIApp subclass that accepts --name argument
# Print "Hello, {name}!" when run
# Add --uppercase flag to print in uppercase
```

---

### 4. Common Utilities Library

**File**: `scripts/lib/common.py` (820 lines)

**Purpose**: Shared utility functions used across all scripts.

**Key Features**:
- File system operations (safe read/write)
- String manipulation utilities
- Date/time helpers
- Data structure utilities
- Environment detection

**When to Use**:
- ✅ Common operations across scripts
- ✅ File handling with error checking
- ✅ Data transformations
- ✅ Cross-platform compatibility

**Live Demo**:
```python
from scripts.lib.common import (
    safe_read_file,
    safe_write_file,
    ensure_directory,
    format_timestamp,
    parse_yaml_safe,
    deep_merge_dict
)

# Safe file operations
content = safe_read_file('/path/to/config.yaml')
parsed = parse_yaml_safe(content)

# Ensure directory exists
ensure_directory('/path/to/output')

# Write file safely
safe_write_file('/path/to/output/result.txt', 'Results here')

# Timestamp formatting
timestamp = format_timestamp(format='iso')
print(f"Current time: {timestamp}")

# Deep merge dictionaries
base_config = {'db': {'host': 'localhost', 'port': 5432}}
override = {'db': {'port': 3306}, 'cache': {'enabled': True}}
merged = deep_merge_dict(base_config, override)
print(merged)  # {'db': {'host': 'localhost', 'port': 3306}, 'cache': {'enabled': True}}
```

**Exercise 1.4**: Use common utilities
```python
# TODO: Read a YAML file, modify a value, and write it back
# Use safe_read_file, parse_yaml_safe, and safe_write_file
```

---

### 5. Config Manager Library

**File**: `scripts/lib/config_manager.py` (120 lines)

**Purpose**: Environment-aware configuration management with validation.

**Key Features**:
- Environment-specific configs (dev, staging, production)
- Dot notation access (`config.get('db.host')`)
- Type-safe getters
- Runtime overrides
- Configuration validation

**When to Use**:
- ✅ Scripts with environment-specific settings
- ✅ Complex configuration structures
- ✅ Multi-environment deployments
- ✅ Configuration validation needs

**Live Demo**:
```python
from scripts.lib.config_manager import Config

# Load configuration for current environment
config = Config.load(env='production')

# Access with dot notation
db_host = config.get('database.host')
db_port = config.get('database.port', default=5432)

# Type-safe getters
max_retries = config.get_int('api.max_retries', default=3)
enable_cache = config.get_bool('api.cache.enabled', default=True)
timeout = config.get_float('api.timeout', default=30.0)

# Runtime overrides (for testing)
config.set('api.max_retries', 5)

# Validate required keys
config.require(['database.host', 'database.port', 'api.token'])

# Export configuration
config.export_env_vars()  # Sets environment variables
```

**Configuration File Example** (`config/production.yaml`):
```yaml
database:
  host: db.production.example.com
  port: 5432
  name: mokostds_prod
  
api:
  base_url: https://api.github.com
  max_retries: 3
  timeout: 30.0
  cache:
    enabled: true
    ttl: 300
    
logging:
  level: INFO
  format: json
```

**Exercise 1.5**: Load and use configuration
```python
# TODO: Create a config file with your settings
# Load it and access values using dot notation
# Validate that required keys exist
```

---

## Part 3: Advanced Libraries (30 minutes)

### 6. Doc Helper Library

**File**: `scripts/lib/doc_helper.py` (220 lines)

**Purpose**: Automated documentation generation and validation.

**Key Features**:
- Extract docstrings and metadata
- Generate markdown documentation
- Validate documentation completeness
- Auto-generate API docs

**When to Use**:
- ✅ Documenting new scripts
- ✅ Generating API documentation
- ✅ Validating doc completeness
- ✅ Automated doc updates

**Live Demo**:
```python
from scripts.lib.doc_helper import DocGenerator

# Generate documentation for a module
doc_gen = DocGenerator()
docs = doc_gen.generate_module_docs('scripts.lib.api_client')

# Save to markdown
doc_gen.save_markdown(docs, 'docs/api/api_client.md')

# Validate documentation
issues = doc_gen.validate_docs('scripts/')
print(f"Found {len(issues)} documentation issues")
```

---

### 7. Error Recovery Library ⭐ HIGH PRIORITY

**File**: `scripts/lib/error_recovery.py` (390 lines)

**Purpose**: Automatic error recovery with retry logic and checkpointing.

**Key Features**:
- Automatic retry with exponential backoff
- Checkpoint system for long-running operations
- Transaction rollback capabilities
- State recovery after failures
- Dead letter queue for failed items

**When to Use**:
- ✅ Long-running batch operations
- ✅ Operations prone to transient failures
- ✅ Multi-step workflows
- ✅ Critical operations requiring reliability

**Live Demo**:
```python
from scripts.lib.error_recovery import Recoverable, Checkpoint, retry_with_backoff

# Automatic retry with decorator
@retry_with_backoff(max_retries=3, base_delay=1.0)
def fetch_data_from_api(url):
    """Automatically retries on failure with exponential backoff"""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Checkpointing for batch operations
checkpoint = Checkpoint(name='process_repos', checkpoint_dir='/tmp/checkpoints')

repositories = ['repo1', 'repo2', 'repo3', 'repo4', 'repo5']

for repo in repositories:
    if checkpoint.is_completed(repo):
        print(f"Skipping {repo} (already processed)")
        continue
        
    try:
        # Process repository
        result = process_repository(repo)
        
        # Mark as completed
        checkpoint.mark_completed(repo, result)
        
    except Exception as e:
        print(f"Failed to process {repo}: {e}")
        checkpoint.mark_failed(repo, str(e))
        
# Recovery after failure
if checkpoint.has_failures():
    failed = checkpoint.get_failures()
    print(f"Retry {len(failed)} failed items")
```

**Exercise 1.6**: Implement error recovery
```python
# TODO: Create a function that fails randomly (50% chance)
# Use @retry_with_backoff to automatically retry
# Use checkpointing to track progress
```

---

### 8. Metrics Collector Library

**File**: `scripts/lib/metrics_collector.py` (340 lines)

**Purpose**: Collect, track, and export metrics for observability.

**Key Features**:
- Counter, gauge, and histogram metrics
- Execution time tracking
- Prometheus export format
- Label support for dimensions
- In-memory and persistent storage

**When to Use**:
- ✅ Production automation scripts
- ✅ Performance monitoring
- ✅ SLA tracking
- ✅ Capacity planning

**Live Demo**:
```python
from scripts.lib.metrics_collector import MetricsCollector

# Initialize metrics collector
metrics = MetricsCollector(service='my_script')

# Counter: increment operations
metrics.increment('repositories_processed', labels={'org': 'mokoconsulting-tech'})
metrics.increment('api_calls_total', labels={'method': 'GET', 'endpoint': '/repos'})

# Gauge: set current value
metrics.set_gauge('active_connections', 42)
metrics.set_gauge('queue_size', 128)

# Histogram: track distributions
metrics.record_histogram('request_duration_seconds', 0.234)
metrics.record_histogram('file_size_bytes', 1024000)

# Time tracking with context manager
with metrics.time_operation('process_repository'):
    # Your operation here
    process_repository()

# Export metrics
prometheus_data = metrics.export_prometheus()
print(prometheus_data)

# Get specific metric
total_processed = metrics.get_counter('repositories_processed')
print(f"Total processed: {total_processed}")
```

**Exercise 1.7**: Track metrics
```python
# TODO: Create a metrics collector
# Track: operations_total (counter), error_rate (gauge), duration (histogram)
# Export to Prometheus format
```

---

### 9. Security Validator Library ⭐ HIGH PRIORITY

**File**: `scripts/lib/security_validator.py` (430 lines)

**Purpose**: Security scanning and validation for scripts and code.

**Key Features**:
- Credential and secret detection
- Dangerous function detection
- File permission checking
- Path traversal prevention
- SQL injection detection

**When to Use**:
- ✅ Before committing code
- ✅ Validating user input
- ✅ Scanning repositories
- ✅ Pre-deployment checks

**Live Demo**:
```python
from scripts.lib.security_validator import SecurityValidator

validator = SecurityValidator()

# Scan a directory for security issues
findings = validator.scan_directory('/path/to/code')

for finding in findings:
    print(f"{finding['severity']}: {finding['message']}")
    print(f"  File: {finding['file']}:{finding['line']}")
    
# Validate file permissions
is_safe = validator.check_file_permissions('/path/to/script.sh')

# Detect credentials in code
has_secrets = validator.detect_credentials(code_content)

# Validate user input
safe_input = validator.validate_input(user_input, input_type='email')
```

**Exercise 1.8**: Security scanning
```python
# TODO: Scan the scripts/lib directory for security issues
# Print a summary of findings by severity
```

---

### 10. Transaction Manager Library

**File**: `scripts.lib/transaction_manager.py` (300 lines)

**Purpose**: Atomic operations with automatic rollback on failure.

**Key Features**:
- Atomic operations (all-or-nothing)
- Automatic rollback on errors
- State consistency guarantees
- Transaction history and audit
- Nested transaction support

**When to Use**:
- ✅ Multi-step operations requiring atomicity
- ✅ Critical updates that must succeed or rollback
- ✅ State-changing operations
- ✅ Operations with dependencies

**Live Demo**:
```python
from scripts.lib.transaction_manager import Transaction, TransactionManager

manager = TransactionManager()

try:
    with manager.begin_transaction('update_repos') as txn:
        # Step 1: Update repository settings
        txn.add_operation(
            'update_settings',
            lambda: update_repo_settings('repo1'),
            rollback=lambda: restore_repo_settings('repo1')
        )
        
        # Step 2: Update branch protection
        txn.add_operation(
            'update_protection',
            lambda: update_branch_protection('repo1', 'main'),
            rollback=lambda: restore_branch_protection('repo1', 'main')
        )
        
        # Step 3: Update webhooks
        txn.add_operation(
            'update_webhooks',
            lambda: update_webhooks('repo1'),
            rollback=lambda: restore_webhooks('repo1')
        )
        
        # Commit transaction (executes all operations)
        txn.commit()
        
except Exception as e:
    # Automatic rollback occurred
    print(f"Transaction failed and rolled back: {e}")
    
# View transaction history
history = manager.get_history()
print(f"Completed {len(history)} transactions")
```

**Exercise 1.9**: Use transaction management
```python
# TODO: Create a transaction with 3 operations
# Make one operation fail and verify rollback occurs
# Check transaction history
```

---

## Part 4: Hands-On Exercises (25 minutes)

### Exercise Set 1: Basic Integration

**Task**: Create a simple script that uses 5 libraries together.

```python
#!/usr/bin/env python3
"""
Exercise: Integrated Script
Combines multiple enterprise libraries in one script
"""

from scripts.lib.cli_framework import CLIApp
from scripts.lib.enterprise_audit import AuditLogger
from scripts.lib.api_client import GitHubClient
from scripts.lib.metrics_collector import MetricsCollector
from scripts.lib.error_recovery import retry_with_backoff
import argparse
import os

class IntegratedScript(CLIApp):
    def setup_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--org', required=True, help='GitHub organization')
        
    def initialize(self):
        """Initialize all enterprise libraries"""
        # TODO: Initialize audit logger
        self.audit = None
        
        # TODO: Initialize metrics collector
        self.metrics = None
        
        # TODO: Initialize API client
        self.api_client = None
        
    @retry_with_backoff(max_retries=3)
    def fetch_repositories(self, org):
        """Fetch repositories with automatic retry"""
        # TODO: Use API client to fetch repositories
        # TODO: Track metrics
        # TODO: Log audit events
        pass
        
    def run(self):
        org = self.args.org
        
        # TODO: Start audit transaction
        # TODO: Fetch repositories
        # TODO: Track metrics
        # TODO: Generate report
        
        return 0

if __name__ == '__main__':
    app = IntegratedScript()
    exit(app.execute())
```

**Requirements**:
1. Initialize all 5 libraries correctly
2. Create an audit transaction for the operation
3. Track metrics (repositories_found, api_calls_total)
4. Use retry logic for API calls
5. Print a summary report

**Solution** (revealed after exercise):
<details>
<summary>Click to show solution</summary>

```python
def initialize(self):
    self.audit = AuditLogger(service='integrated_script')
    self.metrics = MetricsCollector(service='integrated_script')
    self.api_client = GitHubClient(token=os.getenv('GITHUB_TOKEN'))
    
@retry_with_backoff(max_retries=3)
def fetch_repositories(self, org):
    repos = self.api_client.list_repos(org=org)
    self.metrics.increment('api_calls_total')
    self.metrics.set_gauge('repositories_found', len(repos))
    return repos
    
def run(self):
    org = self.args.org
    
    with self.audit.transaction('fetch_repositories') as txn:
        txn.log_event('start', {'org': org})
        
        repos = self.fetch_repositories(org)
        
        txn.log_event('complete', {
            'org': org,
            'count': len(repos)
        })
        
    print(f"Found {len(repos)} repositories in {org}")
    print(f"Metrics: {self.metrics.export_prometheus()}")
    
    return 0
```
</details>

---

### Exercise Set 2: Quick Challenges

**Challenge 1**: Create an audit logger and log a 3-step transaction  
**Challenge 2**: Use the API client to fetch all issues from a repository  
**Challenge 3**: Create a CLI app with custom arguments  
**Challenge 4**: Implement checkpointing for a batch operation  
**Challenge 5**: Scan a directory for security issues and generate a report  

---

## Part 5: Q&A and Resources (20 minutes)

### Common Questions

**Q: Which libraries should I use in every script?**
A: At minimum, use CLI Framework for consistency and Enterprise Audit for compliance.

**Q: Can I use these libraries together?**
A: Yes! They're designed to work together. See Session 2 for integration patterns.

**Q: What about performance overhead?**
A: Minimal. Most libraries add <50ms overhead. Session 3 covers optimization.

**Q: How do I handle library updates?**
A: Follow semantic versioning. Check CHANGELOG.md for breaking changes.

**Q: Can I extend these libraries?**
A: Yes! All libraries support extension. See source code for details.

### Quick Reference Guide

| Need | Use This Library | Key Class/Function |
|------|------------------|-------------------|
| Audit trail | enterprise_audit.py | AuditLogger |
| API calls | api_client.py | GitHubClient |
| CLI interface | cli_framework.py | CLIApp |
| Configuration | config_manager.py | Config |
| Error recovery | error_recovery.py | @retry_with_backoff, Checkpoint |
| Metrics | metrics_collector.py | MetricsCollector |
| Security | security_validator.py | SecurityValidator |
| Transactions | transaction_manager.py | Transaction |
| Utilities | common.py | Various helpers |
| Documentation | doc_helper.py | DocGenerator |

### Resources for Further Learning

1. **Source Code**: `/scripts/lib/` - Read the actual implementation
2. **Tests**: `/.github/workflows/integration-tests.yml` - See usage examples
3. **Documentation**: `/docs/automation/README.md` - Complete automation guide
4. **Planning**: `/docs/planning/README.md` - Implementation roadmap

---

## Knowledge Check Quiz

**Question 1**: Which library should you use for tracking API rate limits?
- a) metrics_collector.py
- b) api_client.py ✅
- c) error_recovery.py
- d) audit_logger.py

**Question 2**: What decorator provides automatic retry logic?
- a) @transaction
- b) @recoverable
- c) @retry_with_backoff ✅
- d) @resilient

**Question 3**: Which library provides compliance audit trails?
- a) enterprise_audit.py ✅
- b) audit_logger.py
- c) transaction_manager.py
- d) metrics_collector.py

**Question 4**: What's the base class for CLI applications?
- a) CLIBase
- b) CLIApp ✅
- c) Application
- d) BaseScript

**Question 5**: Which library detects security vulnerabilities?
- a) input_validator.py
- b) security_scanner.py
- c) security_validator.py ✅
- d) vulnerability_detector.py

---

## Session Summary

### What We Covered
✅ All 10 enterprise libraries and their purposes  
✅ Live demonstrations of each library  
✅ Basic hands-on exercises  
✅ When to use each library  
✅ Integration basics  

### Key Takeaways
1. **Enterprise libraries provide consistency** across all automation
2. **Use multiple libraries together** for enterprise-grade scripts
3. **Start simple** - add libraries as needed
4. **Read the source code** - it's well-documented
5. **Practice with exercises** - hands-on learning is key

### Next Steps
1. ✅ Complete all hands-on exercises
2. 📝 Review library source code
3. 🔨 Migrate a simple script to use 2-3 libraries
4. 📚 Read Session 2 materials before next session
5. ❓ Prepare questions for Session 2

---

## Homework Assignment (Optional)

Create a simple automation script that:
1. Uses CLI Framework for argument parsing
2. Uses Enterprise Audit to log operations
3. Uses API Client to fetch data from GitHub
4. Uses Metrics Collector to track performance
5. Prints a summary report

**Due**: Before Session 2  
**Estimated Time**: 1-2 hours

---

**Ready for more?** → Continue to [Session 2: Practical Integration Workshop](session-2-integration-workshop.md)
