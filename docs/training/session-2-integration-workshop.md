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
PATH: docs/training/session-2-integration-workshop.md
VERSION: 03.02.00
BRIEF: Session 2 - Practical Integration Workshop training materials
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Session 2: Practical Integration Workshop

**Duration**: 3 hours  
**Format**: Hands-on Workshop  
**Prerequisite**: Complete Session 1

---

## Session Objectives

By the end of this session, you will:
- ✅ Migrate an existing script to use enterprise libraries
- ✅ Implement common integration patterns
- ✅ Debug and troubleshoot integration issues
- ✅ Follow best practices for library usage
- ✅ Build a production-ready automation script from scratch

---

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 0:00-0:20 | Integration Patterns Overview | Presentation |
| 0:20-1:20 | Hands-on: Migrate Sample Script | Workshop |
| 1:20-2:00 | Common Integration Patterns | Demo + Practice |
| 2:00-2:40 | Troubleshooting Workshop | Interactive |
| 2:40-3:00 | Q&A and Next Steps | Discussion |

---

## Part 1: Integration Patterns Overview (20 minutes)

### Common Integration Patterns

#### Pattern 1: The Essential Stack
**Use Case**: Every production script  
**Libraries**: CLI Framework + Enterprise Audit + Metrics

```python
from scripts.lib.cli_framework import CLIApp
from scripts.lib.enterprise_audit import AuditLogger
from scripts.lib.metrics_collector import MetricsCollector

class MyScript(CLIApp):
    def initialize(self):
        self.audit = AuditLogger(service=self.__class__.__name__)
        self.metrics = MetricsCollector(service=self.__class__.__name__)
    
    def run(self):
        with self.audit.transaction('main_operation') as txn:
            with self.metrics.time_operation('execution'):
                # Your logic here
                txn.log_event('complete', {'status': 'success'})
        return 0
```

#### Pattern 2: The API Integration Stack
**Use Case**: Scripts making API calls  
**Libraries**: Essential Stack + API Client + Error Recovery

```python
from scripts.lib.cli_framework import CLIApp
from scripts.lib.enterprise_audit import AuditLogger
from scripts.lib.api_client import GitHubClient
from scripts.lib.error_recovery import retry_with_backoff
from scripts.lib.metrics_collector import MetricsCollector

class APIScript(CLIApp):
    def initialize(self):
        self.audit = AuditLogger(service=self.__class__.__name__)
        self.metrics = MetricsCollector(service=self.__class__.__name__)
        self.api = GitHubClient(token=self.get_token())
    
    @retry_with_backoff(max_retries=3)
    def fetch_data(self):
        self.metrics.increment('api_calls_total')
        return self.api.list_repos(org='mokoconsulting-tech')
```

#### Pattern 3: The Batch Processing Stack
**Use Case**: Long-running batch operations  
**Libraries**: API Stack + Checkpointing + Transaction Manager

```python
from scripts.lib.error_recovery import Checkpoint
from scripts.lib.transaction_manager import Transaction

class BatchProcessor(CLIApp):
    def process_batch(self, items):
        checkpoint = Checkpoint('batch_process')
        
        for item in items:
            if checkpoint.is_completed(item):
                continue
                
            try:
                with Transaction() as txn:
                    self.process_item(item, txn)
                    txn.commit()
                checkpoint.mark_completed(item)
            except Exception as e:
                checkpoint.mark_failed(item, str(e))
```

#### Pattern 4: The Security-First Stack
**Use Case**: Scripts handling sensitive data  
**Libraries**: Essential Stack + Security Validator + Config Manager

```python
from scripts.lib.security_validator import SecurityValidator
from scripts.lib.config_manager import Config

class SecureScript(CLIApp):
    def initialize(self):
        super().initialize()
        self.security = SecurityValidator()
        self.config = Config.load(env=self.args.env)
        
    def validate_input(self, user_input):
        # Security validation
        if self.security.detect_credentials(user_input):
            raise ValueError("Input contains credentials!")
        return self.security.validate_input(user_input)
```

### Integration Best Practices

✅ **DO**:
- Initialize libraries in `initialize()` method
- Use context managers for transactions and metrics
- Handle errors gracefully with try/except
- Log all major operations to audit trail
- Track metrics for observability
- Use checkpointing for long operations

❌ **DON'T**:
- Initialize libraries in global scope
- Ignore error recovery for flaky operations
- Skip audit logging for critical operations
- Mix business logic with library initialization
- Forget to export metrics
- Hardcode configuration values

---

## Part 2: Hands-On Migration (60 minutes)

### Exercise 2.1: Migrate Legacy Script

**Scenario**: We have a legacy script that needs enterprise library integration.

#### Original Script (Legacy)

```python
#!/usr/bin/env python3
"""
Legacy script: manage_repositories.py
Fetches repositories and updates their settings
"""

import os
import sys
import requests
import time
import argparse

def main():
    parser = argparse.ArgumentParser(description='Manage repositories')
    parser.add_argument('--org', required=True, help='Organization')
    parser.add_argument('--dry-run', action='store_true', help='Dry run')
    args = parser.parse_args()
    
    # Get token from environment
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN not set")
        sys.exit(1)
    
    # Fetch repositories
    print(f"Fetching repositories for {args.org}...")
    headers = {'Authorization': f'token {token}'}
    
    url = f'https://api.github.com/orgs/{args.org}/repos'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: API returned {response.status_code}")
        sys.exit(1)
    
    repos = response.json()
    print(f"Found {len(repos)} repositories")
    
    # Update each repository
    updated_count = 0
    failed_count = 0
    
    for repo in repos:
        repo_name = repo['name']
        print(f"Processing {repo_name}...")
        
        if args.dry_run:
            print(f"  [DRY RUN] Would update {repo_name}")
            updated_count += 1
            continue
        
        # Update repository settings
        update_url = f'https://api.github.com/repos/{args.org}/{repo_name}'
        data = {
            'has_issues': True,
            'has_wiki': False,
            'has_projects': False
        }
        
        response = requests.patch(update_url, headers=headers, json=data)
        
        if response.status_code == 200:
            print(f"  ✓ Updated {repo_name}")
            updated_count += 1
        else:
            print(f"  ✗ Failed to update {repo_name}: {response.status_code}")
            failed_count += 1
        
        # Rate limiting (simple sleep)
        time.sleep(1)
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Total repositories: {len(repos)}")
    print(f"  Updated: {updated_count}")
    print(f"  Failed: {failed_count}")

if __name__ == '__main__':
    main()
```

#### Your Task: Migrate to Enterprise Libraries

**Requirements**:
1. ✅ Use CLI Framework for argument parsing
2. ✅ Add Enterprise Audit logging for all operations
3. ✅ Use API Client for rate-limited API calls
4. ✅ Add error recovery with checkpointing
5. ✅ Track metrics (repos_processed, update_success, update_failure)
6. ✅ Use Security Validator to validate inputs
7. ✅ Add proper error handling

#### Step-by-Step Migration Guide

**Step 1: Set up the CLI Framework structure**

```python
#!/usr/bin/env python3
"""
Enterprise script: manage_repositories.py
Manages repository settings with enterprise libraries
"""

from scripts.lib.cli_framework import CLIApp
import argparse

class RepositoryManager(CLIApp):
    """Manages repository settings for a GitHub organization"""
    
    def setup_arguments(self, parser: argparse.ArgumentParser):
        """Configure command-line arguments"""
        parser.add_argument('--org', required=True, 
                          help='GitHub organization name')
        # TODO: Add any additional arguments
    
    def initialize(self):
        """Initialize enterprise libraries"""
        # TODO: Initialize libraries here
        pass
    
    def run(self):
        """Main execution logic"""
        org = self.args.org
        
        # TODO: Implement main logic
        
        return 0  # Success

if __name__ == '__main__':
    app = RepositoryManager()
    exit(app.execute())
```

**Step 2: Add Enterprise Audit**

```python
from scripts.lib.enterprise_audit import AuditLogger

def initialize(self):
    """Initialize enterprise libraries"""
    super().initialize()
    self.audit = AuditLogger(
        service='repository_manager',
        retention_days=90
    )

def run(self):
    org = self.args.org
    
    with self.audit.transaction('manage_repositories') as txn:
        txn.log_event('start', {
            'organization': org,
            'dry_run': self.args.dry_run
        })
        
        # TODO: Add main logic
        
        txn.log_event('complete', {
            'organization': org,
            'status': 'success'
        })
    
    return 0
```

**Step 3: Add API Client**

```python
from scripts.lib.api_client import GitHubClient, RateLimitConfig
import os

def initialize(self):
    super().initialize()
    self.audit = AuditLogger(service='repository_manager')
    
    # Initialize API client with rate limiting
    rate_config = RateLimitConfig(
        max_requests_per_hour=5000,
        enable_caching=True,
        cache_ttl=300
    )
    
    self.api = GitHubClient(
        token=os.getenv('GITHUB_TOKEN'),
        rate_limit_config=rate_config
    )

def fetch_repositories(self, org):
    """Fetch repositories using API client"""
    try:
        repos = self.api.list_repos(org=org)
        self.logger.info(f"Fetched {len(repos)} repositories")
        return repos
    except Exception as e:
        self.logger.error(f"Failed to fetch repositories: {e}")
        raise
```

**Step 4: Add Metrics Collection**

```python
from scripts.lib.metrics_collector import MetricsCollector

def initialize(self):
    super().initialize()
    self.audit = AuditLogger(service='repository_manager')
    self.metrics = MetricsCollector(service='repository_manager')
    self.api = GitHubClient(token=os.getenv('GITHUB_TOKEN'))

def update_repository(self, org, repo_name, txn):
    """Update a single repository"""
    try:
        with self.metrics.time_operation('repository_update'):
            # Update repository settings
            self.api.update_repo(
                org=org,
                repo=repo_name,
                data={
                    'has_issues': True,
                    'has_wiki': False,
                    'has_projects': False
                }
            )
        
        # Track success
        self.metrics.increment('repos_updated_success', 
                              labels={'org': org})
        txn.log_event('repository_updated', {
            'repo': repo_name,
            'status': 'success'
        })
        
        return True
        
    except Exception as e:
        # Track failure
        self.metrics.increment('repos_updated_failure',
                              labels={'org': org})
        txn.log_event('repository_failed', {
            'repo': repo_name,
            'error': str(e)
        })
        
        return False
```

**Step 5: Add Error Recovery with Checkpointing**

```python
from scripts.lib.error_recovery import Checkpoint, retry_with_backoff

def initialize(self):
    super().initialize()
    self.audit = AuditLogger(service='repository_manager')
    self.metrics = MetricsCollector(service='repository_manager')
    self.api = GitHubClient(token=os.getenv('GITHUB_TOKEN'))
    
    # Initialize checkpoint
    self.checkpoint = Checkpoint(
        name='repository_updates',
        checkpoint_dir='/tmp/checkpoints'
    )

@retry_with_backoff(max_retries=3, base_delay=1.0)
def update_repository(self, org, repo_name, txn):
    """Update a single repository with retry logic"""
    # Check if already processed
    if self.checkpoint.is_completed(repo_name):
        self.logger.info(f"Skipping {repo_name} (already processed)")
        return True
    
    try:
        with self.metrics.time_operation('repository_update'):
            self.api.update_repo(
                org=org,
                repo=repo_name,
                data={
                    'has_issues': True,
                    'has_wiki': False,
                    'has_projects': False
                }
            )
        
        # Mark as completed
        self.checkpoint.mark_completed(repo_name, {'status': 'success'})
        self.metrics.increment('repos_updated_success', labels={'org': org})
        txn.log_event('repository_updated', {'repo': repo_name})
        
        return True
        
    except Exception as e:
        # Mark as failed
        self.checkpoint.mark_failed(repo_name, str(e))
        self.metrics.increment('repos_updated_failure', labels={'org': org})
        txn.log_event('repository_failed', {'repo': repo_name, 'error': str(e)})
        
        raise  # Re-raise for retry logic
```

**Step 6: Add Security Validation**

```python
from scripts.lib.security_validator import SecurityValidator

def initialize(self):
    super().initialize()
    self.audit = AuditLogger(service='repository_manager')
    self.metrics = MetricsCollector(service='repository_manager')
    self.api = GitHubClient(token=os.getenv('GITHUB_TOKEN'))
    self.checkpoint = Checkpoint(name='repository_updates')
    self.security = SecurityValidator()

def validate_inputs(self):
    """Validate all user inputs"""
    org = self.args.org
    
    # Validate organization name
    if not self.security.validate_input(org, input_type='identifier'):
        raise ValueError(f"Invalid organization name: {org}")
    
    # Check for dangerous patterns
    if self.security.detect_dangerous_patterns(org):
        raise ValueError(f"Organization name contains dangerous patterns")
    
    self.logger.info(f"Input validation passed for org: {org}")
```

**Step 7: Complete Integration**

```python
#!/usr/bin/env python3
"""
Enterprise script: manage_repositories.py
Manages repository settings with enterprise libraries

Copyright (C) 2026 Moko Consulting
SPDX-License-Identifier: GPL-3.0-or-later
"""

from scripts.lib.cli_framework import CLIApp
from scripts.lib.enterprise_audit import AuditLogger
from scripts.lib.api_client import GitHubClient, RateLimitConfig
from scripts.lib.metrics_collector import MetricsCollector
from scripts.lib.error_recovery import Checkpoint, retry_with_backoff
from scripts.lib.security_validator import SecurityValidator
import argparse
import os

class RepositoryManager(CLIApp):
    """Manages repository settings for a GitHub organization"""
    
    def setup_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--org', required=True, help='GitHub organization')
    
    def initialize(self):
        super().initialize()
        
        # Initialize all enterprise libraries
        self.audit = AuditLogger(service='repository_manager', retention_days=90)
        self.metrics = MetricsCollector(service='repository_manager')
        self.security = SecurityValidator()
        
        # API client with rate limiting
        rate_config = RateLimitConfig(
            max_requests_per_hour=5000,
            enable_caching=True
        )
        self.api = GitHubClient(
            token=os.getenv('GITHUB_TOKEN'),
            rate_limit_config=rate_config
        )
        
        # Checkpoint for recovery
        self.checkpoint = Checkpoint(
            name='repository_updates',
            checkpoint_dir='/tmp/checkpoints'
        )
    
    def validate_inputs(self):
        """Validate all inputs"""
        org = self.args.org
        if not self.security.validate_input(org, input_type='identifier'):
            raise ValueError(f"Invalid organization name: {org}")
    
    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def update_repository(self, org, repo_name, txn):
        """Update a single repository"""
        if self.checkpoint.is_completed(repo_name):
            self.logger.debug(f"Skipping {repo_name} (completed)")
            return True
        
        try:
            if self.args.dry_run:
                self.logger.info(f"[DRY RUN] Would update {repo_name}")
            else:
                with self.metrics.time_operation('repository_update'):
                    self.api.update_repo(
                        org=org,
                        repo=repo_name,
                        data={
                            'has_issues': True,
                            'has_wiki': False,
                            'has_projects': False
                        }
                    )
            
            self.checkpoint.mark_completed(repo_name, {'status': 'success'})
            self.metrics.increment('repos_updated_success', labels={'org': org})
            txn.log_event('repository_updated', {'repo': repo_name})
            
            return True
            
        except Exception as e:
            self.checkpoint.mark_failed(repo_name, str(e))
            self.metrics.increment('repos_updated_failure', labels={'org': org})
            txn.log_event('repository_failed', {'repo': repo_name, 'error': str(e)})
            raise
    
    def run(self):
        org = self.args.org
        
        # Validate inputs
        self.validate_inputs()
        
        # Main transaction
        with self.audit.transaction('manage_repositories') as txn:
            txn.log_event('start', {'organization': org, 'dry_run': self.args.dry_run})
            
            # Fetch repositories
            repos = self.api.list_repos(org=org)
            self.logger.info(f"Found {len(repos)} repositories")
            self.metrics.set_gauge('repositories_total', len(repos))
            
            # Process each repository
            success_count = 0
            failure_count = 0
            
            for repo in repos:
                repo_name = repo['name']
                self.logger.info(f"Processing {repo_name}...")
                
                try:
                    if self.update_repository(org, repo_name, txn):
                        success_count += 1
                except Exception as e:
                    self.logger.error(f"Failed to update {repo_name}: {e}")
                    failure_count += 1
            
            # Log final results
            txn.log_event('complete', {
                'organization': org,
                'total': len(repos),
                'success': success_count,
                'failure': failure_count
            })
            
            # Print summary
            self.logger.info(f"\nSummary:")
            self.logger.info(f"  Total: {len(repos)}")
            self.logger.info(f"  Success: {success_count}")
            self.logger.info(f"  Failed: {failure_count}")
            
            # Export metrics
            if self.args.verbose:
                print("\nMetrics:")
                print(self.metrics.export_prometheus())
        
        return 0 if failure_count == 0 else 1

if __name__ == '__main__':
    app = RepositoryManager()
    exit(app.execute())
```

#### Your Turn: Complete the Migration

**Task**: Take the legacy script and migrate it following the steps above.

**Verification Checklist**:
- [ ] Script uses CLIApp base class
- [ ] Audit logging tracks all operations
- [ ] API calls use GitHubClient with rate limiting
- [ ] Checkpointing enables recovery
- [ ] Metrics track success/failure
- [ ] Security validation on inputs
- [ ] Proper error handling throughout
- [ ] Dry-run mode works correctly

---

## Part 3: Common Integration Patterns (40 minutes)

### Pattern Exercise 2.2: Configuration-Driven Script

Build a script that loads configuration from YAML files.

```python
from scripts.lib.cli_framework import CLIApp
from scripts.lib.config_manager import Config
import argparse

class ConfigDrivenScript(CLIApp):
    def setup_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument('--env', default='development',
                          choices=['development', 'staging', 'production'],
                          help='Environment')
        parser.add_argument('--config', help='Config file override')
    
    def initialize(self):
        super().initialize()
        
        # Load environment-specific config
        self.config = Config.load(
            env=self.args.env,
            config_file=self.args.config
        )
        
        # Validate required configuration
        self.config.require([
            'github.organization',
            'github.token',
            'settings.max_retries'
        ])
    
    def run(self):
        org = self.config.get('github.organization')
        max_retries = self.config.get_int('settings.max_retries', default=3)
        enable_cache = self.config.get_bool('cache.enabled', default=True)
        
        self.logger.info(f"Organization: {org}")
        self.logger.info(f"Max retries: {max_retries}")
        self.logger.info(f"Cache enabled: {enable_cache}")
        
        # Your logic here
        
        return 0
```

**Configuration File** (`config/development.yaml`):
```yaml
github:
  organization: mokoconsulting-tech
  token: ${GITHUB_TOKEN}

settings:
  max_retries: 3
  timeout: 30
  
cache:
  enabled: true
  ttl: 300

logging:
  level: DEBUG
```

**Exercise**: Create a config-driven script that:
1. Loads environment-specific configuration
2. Validates required keys exist
3. Uses config values throughout the script
4. Supports runtime overrides via CLI args

---

### Pattern Exercise 2.3: Transaction-Based Updates

Implement atomic operations that rollback on failure.

```python
from scripts.lib.transaction_manager import TransactionManager

class AtomicUpdater(CLIApp):
    def initialize(self):
        super().initialize()
        self.txn_manager = TransactionManager()
    
    def update_repository_atomically(self, org, repo):
        """Perform atomic repository updates"""
        
        try:
            with self.txn_manager.begin_transaction(f'update_{repo}') as txn:
                # Operation 1: Update settings
                txn.add_operation(
                    name='update_settings',
                    forward=lambda: self.update_settings(org, repo),
                    rollback=lambda: self.restore_settings(org, repo)
                )
                
                # Operation 2: Update branch protection
                txn.add_operation(
                    name='update_protection',
                    forward=lambda: self.update_protection(org, repo, 'main'),
                    rollback=lambda: self.restore_protection(org, repo, 'main')
                )
                
                # Operation 3: Update webhooks
                txn.add_operation(
                    name='update_webhooks',
                    forward=lambda: self.update_webhooks(org, repo),
                    rollback=lambda: self.restore_webhooks(org, repo)
                )
                
                # Commit all operations atomically
                txn.commit()
                
                self.logger.info(f"Successfully updated {repo}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to update {repo}: {e}")
            self.logger.info(f"All changes rolled back")
            return False
    
    def update_settings(self, org, repo):
        """Update repository settings"""
        # Save current state for rollback
        current = self.api.get_repo(org, repo)
        self.state_cache[f'{repo}_settings'] = current
        
        # Apply new settings
        self.api.update_repo(org, repo, {
            'has_issues': True,
            'has_wiki': False
        })
    
    def restore_settings(self, org, repo):
        """Rollback settings"""
        previous = self.state_cache.get(f'{repo}_settings')
        if previous:
            self.api.update_repo(org, repo, previous)
```

**Exercise**: Implement a transaction-based script that:
1. Updates multiple settings atomically
2. Provides rollback functions for each operation
3. Logs transaction history
4. Handles nested transactions

---

### Pattern Exercise 2.4: Batch Processing with Checkpoints

Process large datasets with recovery capabilities.

```python
from scripts.lib.error_recovery import Checkpoint
from scripts.lib.metrics_collector import MetricsCollector

class BatchProcessor(CLIApp):
    def initialize(self):
        super().initialize()
        self.checkpoint = Checkpoint(name='batch_process')
        self.metrics = MetricsCollector(service='batch_processor')
    
    def process_batch(self, items):
        """Process items with checkpointing"""
        
        total = len(items)
        processed = 0
        failed = 0
        
        self.logger.info(f"Processing {total} items")
        
        for idx, item in enumerate(items, 1):
            item_id = item['id']
            
            # Skip if already processed
            if self.checkpoint.is_completed(item_id):
                self.logger.debug(f"Skipping {item_id} (completed)")
                processed += 1
                continue
            
            # Skip if previously failed and not retrying
            if self.checkpoint.is_failed(item_id) and not self.args.retry_failed:
                self.logger.debug(f"Skipping {item_id} (failed)")
                failed += 1
                continue
            
            # Process item
            try:
                self.logger.info(f"[{idx}/{total}] Processing {item_id}...")
                result = self.process_item(item)
                
                # Mark as completed
                self.checkpoint.mark_completed(item_id, result)
                self.metrics.increment('items_processed_success')
                processed += 1
                
            except Exception as e:
                self.logger.error(f"Failed to process {item_id}: {e}")
                self.checkpoint.mark_failed(item_id, str(e))
                self.metrics.increment('items_processed_failure')
                failed += 1
        
        # Print summary
        self.logger.info(f"\nBatch Summary:")
        self.logger.info(f"  Total: {total}")
        self.logger.info(f"  Processed: {processed}")
        self.logger.info(f"  Failed: {failed}")
        
        # Check for failed items
        if self.checkpoint.has_failures():
            failed_items = self.checkpoint.get_failures()
            self.logger.warning(f"\n{len(failed_items)} items failed:")
            for item_id, error in failed_items.items():
                self.logger.warning(f"  - {item_id}: {error}")
            self.logger.info("\nRun with --retry-failed to retry failed items")
        
        return failed == 0
```

**Exercise**: Create a batch processing script that:
1. Processes 100+ items with checkpointing
2. Recovers from failures gracefully
3. Provides retry capability for failed items
4. Tracks progress metrics
5. Generates a summary report

---

## Part 4: Troubleshooting Workshop (40 minutes)

### Common Issues and Solutions

#### Issue 1: Import Errors

**Problem**:
```python
ModuleNotFoundError: No module named 'scripts.lib.enterprise_audit'
```

**Solution**:
```python
# Option 1: Add parent directory to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.lib.enterprise_audit import AuditLogger

# Option 2: Use relative imports (if in scripts directory)
from lib.enterprise_audit import AuditLogger

# Option 3: Install as package
# pip install -e .
```

---

#### Issue 2: Rate Limiting Not Working

**Problem**: Script still hits rate limits despite using API Client.

**Diagnosis**:
```python
# Check rate limit status
status = client.get_rate_limit_status()
print(f"Rate limit: {status['remaining']}/{status['limit']}")
print(f"Reset time: {status['reset_time']}")
```

**Solution**:
```python
# Ensure proper configuration
rate_config = RateLimitConfig(
    max_requests_per_hour=5000,  # Match GitHub limits
    burst_size=100,  # Allow bursts
    enable_caching=True,  # Cache responses
    cache_ttl=300  # 5-minute cache
)

client = GitHubClient(
    token=token,
    rate_limit_config=rate_config
)

# Enable request logging
import logging
logging.getLogger('api_client').setLevel(logging.DEBUG)
```

---

#### Issue 3: Checkpoints Not Persisting

**Problem**: Checkpoints reset after script restart.

**Solution**:
```python
# Use persistent checkpoint directory
checkpoint = Checkpoint(
    name='my_operation',
    checkpoint_dir='/var/lib/myapp/checkpoints'  # Persistent location
)

# Ensure directory exists and has correct permissions
import os
os.makedirs('/var/lib/myapp/checkpoints', exist_ok=True)
```

---

#### Issue 4: Metrics Not Exporting

**Problem**: Prometheus export returns empty results.

**Diagnosis**:
```python
# Check if metrics are being recorded
print(f"Counter value: {metrics.get_counter('my_counter')}")
print(f"All metrics: {metrics.get_all_metrics()}")
```

**Solution**:
```python
# Ensure metrics are incremented with correct labels
metrics.increment('operations_total', labels={'type': 'update'})

# Export with proper formatting
prometheus_text = metrics.export_prometheus()
print(prometheus_text)

# Write to file for Prometheus scraping
with open('/var/lib/prometheus/metrics.prom', 'w') as f:
    f.write(prometheus_text)
```

---

#### Issue 5: Audit Logs Missing

**Problem**: Audit transactions not appearing in logs.

**Solution**:
```python
# Ensure transaction is completed
with logger.transaction('operation') as txn:
    txn.log_event('step1', {'status': 'complete'})
    txn.log_event('step2', {'status': 'complete'})
    # Transaction auto-completes on context exit

# Check log file location
print(f"Log file: {logger.log_file}")

# Verify log rotation settings
logger = AuditLogger(
    service='my_script',
    log_dir='/var/log/myapp',
    retention_days=90
)
```

---

### Troubleshooting Exercise 2.5

**Scenario**: A script is failing intermittently with the following symptoms:
- Rate limit errors despite using API Client
- Some operations not in audit log
- Metrics show incorrect counts
- Checkpoints not preventing re-processing

**Your Task**: Debug and fix the script.

```python
# Buggy script
class BuggyScript(CLIApp):
    def run(self):
        # BUG: Libraries not initialized
        repos = self.api.list_repos(org='mokoconsulting-tech')
        
        for repo in repos:
            # BUG: No audit logging
            # BUG: No checkpoint check
            self.process_repo(repo)
            
            # BUG: Metrics incremented incorrectly
            self.metrics.increment('repos')
        
        # BUG: Transaction never started
        return 0
```

**Solution**: <details><summary>Click to reveal</summary>

```python
class FixedScript(CLIApp):
    def initialize(self):
        """Initialize all libraries"""
        super().initialize()
        self.audit = AuditLogger(service='fixed_script')
        self.metrics = MetricsCollector(service='fixed_script')
        self.api = GitHubClient(token=os.getenv('GITHUB_TOKEN'))
        self.checkpoint = Checkpoint(name='process_repos')
    
    def run(self):
        with self.audit.transaction('process_repositories') as txn:
            repos = self.api.list_repos(org='mokoconsulting-tech')
            txn.log_event('repos_fetched', {'count': len(repos)})
            
            for repo in repos:
                repo_name = repo['name']
                
                # Check checkpoint
                if self.checkpoint.is_completed(repo_name):
                    continue
                
                try:
                    self.process_repo(repo)
                    self.checkpoint.mark_completed(repo_name)
                    self.metrics.increment('repos_processed_success')
                    txn.log_event('repo_processed', {'repo': repo_name})
                except Exception as e:
                    self.checkpoint.mark_failed(repo_name, str(e))
                    self.metrics.increment('repos_processed_failure')
                    txn.log_event('repo_failed', {'repo': repo_name, 'error': str(e)})
            
            txn.log_event('complete', {'total': len(repos)})
        
        return 0
```
</details>

---

## Part 5: Real-World Examples (20 minutes)

### Example 1: Bulk Repository Updater

Reference: Production script from the repository.

**Key Integration Points**:
- CLI Framework for argument parsing
- Enterprise Audit for compliance trail
- API Client for rate-limited GitHub API calls
- Error Recovery for checkpointing batch updates
- Metrics for tracking update statistics

**Code Walkthrough**: See `scripts/bulk_update_repos.py`

---

### Example 2: Organization Project Creator

Reference: Production script from the repository.

**Key Integration Points**:
- CLI Framework with extended arguments
- Enterprise Audit for project creation tracking
- API Client for GitHub Projects API
- Transaction Manager for atomic project creation
- Security Validator for input validation

**Code Walkthrough**: See `scripts/auto_create_org_projects.py`

---

### Example 3: Branch Cleanup Script

Reference: Production script from the repository.

**Key Integration Points**:
- CLI Framework with date-based arguments
- Enterprise Audit for deletion tracking
- API Client for branch operations
- Error Recovery with checkpoint-based recovery
- Metrics for cleanup statistics

**Code Walkthrough**: See `scripts/clean_old_branches.py`

---

### Example 4: Unified Release Manager

Reference: Production script from the repository.

**Key Integration Points**:
- CLI Framework with release arguments
- Enterprise Audit for release audit trail
- API Client for release operations
- Transaction Manager for atomic multi-repo releases
- Error Recovery for release rollback

**Code Walkthrough**: See `scripts/unified_release.py`

---

## Part 6: Q&A and Next Steps (20 minutes)

### Key Takeaways

✅ **Always start with CLI Framework** - Provides consistent structure  
✅ **Add audit logging early** - Track operations from the start  
✅ **Use checkpointing for batch operations** - Enable recovery  
✅ **Track metrics for observability** - Monitor script performance  
✅ **Validate inputs with security validator** - Prevent vulnerabilities  

### Common Pitfalls to Avoid

❌ Forgetting to initialize libraries in `initialize()`  
❌ Not using context managers for transactions  
❌ Ignoring checkpoint status in loops  
❌ Hardcoding values instead of using configuration  
❌ Skipping error handling in critical sections  

### Homework Assignment

**Task**: Migrate one of your existing automation scripts to use enterprise libraries.

**Requirements**:
1. Use at least 5 enterprise libraries
2. Add comprehensive audit logging
3. Implement error recovery with checkpointing
4. Track relevant metrics
5. Add security validation
6. Write tests for critical functions

**Deliverable**: Pull request with migrated script

**Due**: Before Session 3

---

## Knowledge Check Quiz

1. **What method should you override to initialize enterprise libraries?**
   - a) `__init__`
   - b) `setup`
   - c) `initialize` ✅
   - d) `configure`

2. **How do you mark a checkpoint as completed?**
   - a) `checkpoint.complete(item_id)`
   - b) `checkpoint.mark_completed(item_id)` ✅
   - c) `checkpoint.finish(item_id)`
   - d) `checkpoint.done(item_id)`

3. **What happens when a transaction context exits normally?**
   - a) Transaction is rolled back
   - b) Transaction is committed automatically ✅
   - c) Transaction is suspended
   - d) Transaction requires manual commit

4. **Which library handles automatic retry with exponential backoff?**
   - a) api_client.py
   - b) transaction_manager.py
   - c) error_recovery.py ✅
   - d) cli_framework.py

5. **What's the recommended pattern for batch processing?**
   - a) Essential Stack only
   - b) API Stack + Checkpointing ✅
   - c) Security Stack + Metrics
   - d) CLI Framework only

---

## Additional Resources

- **Source Code**: Review migrated production scripts in `/scripts/`
- **Tests**: Check integration tests in `/.github/workflows/`
- **Documentation**: Read automation guide in `/docs/automation/`
- **Examples**: Explore templates in `/templates/`

---

**Ready for advanced topics?** → Continue to [Session 3: Advanced Features](session-3-advanced-features.md)
