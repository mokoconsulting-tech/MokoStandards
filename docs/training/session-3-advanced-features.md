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
PATH: docs/training/session-3-advanced-features.md
VERSION: 03.02.00
BRIEF: Session 3 - Advanced Features training materials
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Session 3: Advanced Features

**Duration**: 2 hours  
**Format**: Advanced Workshop  
**Prerequisite**: Complete Sessions 1 and 2

---

## Session Objectives

By the end of this session, you will:
- ✅ Implement robust error recovery patterns
- ✅ Design fault-tolerant automation workflows
- ✅ Optimize script performance and resource usage
- ✅ Apply enterprise security patterns
- ✅ Meet audit and compliance requirements
- ✅ Master advanced API client features

---

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 0:00-0:30 | Advanced Error Recovery Patterns | Demo + Practice |
| 0:30-1:00 | Transaction Management Deep Dive | Workshop |
| 1:00-1:30 | Performance Optimization | Demo + Practice |
| 1:30-1:50 | Security & Compliance Best Practices | Discussion + Practice |
| 1:50-2:00 | Certification & Next Steps | Wrap-up |

---

## Part 1: Advanced Error Recovery Patterns (30 minutes)

### Pattern 1: Multi-Level Retry Strategy

**Scenario**: Different operations require different retry strategies.

```python
from scripts.lib.error_recovery import retry_with_backoff, Checkpoint
from scripts.lib.api_client import GitHubClient
from scripts.lib.enterprise_audit import AuditLogger
import time

class AdvancedErrorRecovery:
    def __init__(self):
        self.api = GitHubClient()
        self.audit = AuditLogger(service='advanced_recovery')
        self.checkpoint = Checkpoint(name='multi_level_recovery')
    
    @retry_with_backoff(
        max_retries=5,
        base_delay=2.0,
        max_delay=60.0,
        exponential_base=2,
        jitter=True
    )
    def fetch_with_aggressive_retry(self, url):
        """Aggressive retry for critical operations"""
        return self.api.get(url)
    
    @retry_with_backoff(
        max_retries=2,
        base_delay=1.0,
        max_delay=10.0
    )
    def fetch_with_conservative_retry(self, url):
        """Conservative retry for less critical operations"""
        return self.api.get(url)
    
    def fetch_with_circuit_breaker(self, url, circuit_breaker):
        """Use circuit breaker to prevent cascade failures"""
        if circuit_breaker.is_open():
            raise Exception("Circuit breaker is open")
        
        try:
            response = self.api.get(url)
            circuit_breaker.record_success()
            return response
        except Exception as e:
            circuit_breaker.record_failure()
            raise
```

**Key Concepts**:
- **Exponential Backoff**: Progressively longer waits between retries
- **Jitter**: Random delay to prevent thundering herd
- **Max Delay**: Cap on retry delay to prevent infinite waits
- **Circuit Breaker**: Stop trying when system is failing

---

### Pattern 2: Checkpoint-Based State Recovery

**Scenario**: Long-running operations that need to resume after failures.

```python
from scripts.lib.error_recovery import Checkpoint
from scripts.lib.enterprise_audit import AuditLogger
import json
from datetime import datetime

class StateRecoveryManager:
    def __init__(self, operation_name):
        self.checkpoint = Checkpoint(
            name=operation_name,
            checkpoint_dir='/var/lib/myapp/checkpoints'
        )
        self.audit = AuditLogger(service='state_recovery')
    
    def save_state(self, item_id, state_data):
        """Save detailed state for recovery"""
        self.checkpoint.mark_completed(item_id, {
            'state': state_data,
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0'
        })
    
    def load_state(self, item_id):
        """Load saved state"""
        return self.checkpoint.get_state(item_id)
    
    def process_with_recovery(self, items):
        """Process items with state recovery"""
        
        for item in items:
            item_id = item['id']
            
            # Check if already completed
            if self.checkpoint.is_completed(item_id):
                print(f"Resuming from completed state: {item_id}")
                continue
            
            # Load previous state if exists
            previous_state = self.load_state(item_id)
            if previous_state:
                print(f"Resuming from checkpoint: {item_id}")
                current_step = previous_state.get('current_step', 0)
            else:
                current_step = 0
            
            # Multi-step processing with state saving
            try:
                # Step 1
                if current_step < 1:
                    self.process_step1(item)
                    self.save_state(item_id, {'current_step': 1, 'data': item})
                    current_step = 1
                
                # Step 2
                if current_step < 2:
                    self.process_step2(item)
                    self.save_state(item_id, {'current_step': 2, 'data': item})
                    current_step = 2
                
                # Step 3
                if current_step < 3:
                    self.process_step3(item)
                    self.save_state(item_id, {'current_step': 3, 'data': item})
                    current_step = 3
                
                # Mark as fully completed
                self.checkpoint.mark_completed(item_id, {
                    'status': 'complete',
                    'steps_completed': 3
                })
                
            except Exception as e:
                print(f"Failed at step {current_step}: {e}")
                self.checkpoint.mark_failed(item_id, str(e))
                # State is already saved, can resume later
```

**Exercise 3.1**: Implement multi-step processing with state recovery
```python
# TODO: Create a 5-step process with checkpoint after each step
# TODO: Simulate failures at different steps
# TODO: Verify recovery continues from last successful checkpoint
```

---

### Pattern 3: Dead Letter Queue for Failed Items

**Scenario**: Handle items that fail repeatedly without blocking the entire process.

```python
from scripts.lib.error_recovery import Checkpoint
from scripts.lib.metrics_collector import MetricsCollector
import json
from pathlib import Path

class DeadLetterQueue:
    def __init__(self, name, max_retries=3):
        self.name = name
        self.max_retries = max_retries
        self.checkpoint = Checkpoint(name=name)
        self.metrics = MetricsCollector(service=name)
        self.dlq_path = Path(f'/var/lib/myapp/dlq/{name}')
        self.dlq_path.mkdir(parents=True, exist_ok=True)
    
    def process_with_dlq(self, items):
        """Process items with dead letter queue"""
        
        for item in items:
            item_id = item['id']
            
            # Check retry count
            retry_count = self.checkpoint.get_retry_count(item_id)
            
            if retry_count >= self.max_retries:
                # Move to dead letter queue
                self.move_to_dlq(item, f"Max retries ({self.max_retries}) exceeded")
                self.metrics.increment('items_moved_to_dlq')
                continue
            
            try:
                self.process_item(item)
                self.checkpoint.mark_completed(item_id)
                self.metrics.increment('items_processed_success')
                
            except Exception as e:
                # Increment retry count
                self.checkpoint.increment_retry_count(item_id)
                self.checkpoint.mark_failed(item_id, str(e))
                self.metrics.increment('items_retried')
                
                print(f"Failed {item_id} (attempt {retry_count + 1}/{self.max_retries}): {e}")
    
    def move_to_dlq(self, item, reason):
        """Move failed item to dead letter queue"""
        dlq_file = self.dlq_path / f"{item['id']}.json"
        
        dlq_entry = {
            'item': item,
            'reason': reason,
            'timestamp': datetime.utcnow().isoformat(),
            'retry_count': self.checkpoint.get_retry_count(item['id'])
        }
        
        with open(dlq_file, 'w') as f:
            json.dump(dlq_entry, f, indent=2)
        
        print(f"Moved {item['id']} to dead letter queue: {reason}")
    
    def process_dlq(self):
        """Manually process items from dead letter queue"""
        dlq_items = list(self.dlq_path.glob('*.json'))
        
        print(f"Found {len(dlq_items)} items in dead letter queue")
        
        for dlq_file in dlq_items:
            with open(dlq_file) as f:
                dlq_entry = json.load(f)
            
            item = dlq_entry['item']
            print(f"Manual processing: {item['id']}")
            
            try:
                self.process_item(item)
                # Remove from DLQ
                dlq_file.unlink()
                self.checkpoint.mark_completed(item['id'])
                print(f"Successfully processed {item['id']} from DLQ")
                
            except Exception as e:
                print(f"Still failing: {item['id']}: {e}")
```

**Exercise 3.2**: Implement DLQ pattern
```python
# TODO: Process a batch where 10% of items fail
# TODO: Verify failed items move to DLQ after max retries
# TODO: Implement manual DLQ processing
```

---

## Part 2: Transaction Management Deep Dive (30 minutes)

### Pattern 4: Nested Transactions

**Scenario**: Complex operations with sub-operations that need independent rollback.

```python
from scripts.lib.transaction_manager import TransactionManager
from scripts.lib.enterprise_audit import AuditLogger

class NestedTransactionExample:
    def __init__(self):
        self.txn_manager = TransactionManager()
        self.audit = AuditLogger(service='nested_transactions')
    
    def update_organization(self, org):
        """Update organization with nested transactions"""
        
        with self.txn_manager.begin_transaction(f'update_org_{org}') as parent_txn:
            
            # Sub-transaction 1: Update organization settings
            with self.txn_manager.begin_transaction(f'org_settings_{org}') as txn1:
                txn1.add_operation(
                    'update_org_settings',
                    forward=lambda: self.update_org_settings(org),
                    rollback=lambda: self.restore_org_settings(org)
                )
                txn1.commit()
            
            # Sub-transaction 2: Update all repositories
            with self.txn_manager.begin_transaction(f'org_repos_{org}') as txn2:
                repos = self.get_repositories(org)
                
                for repo in repos:
                    # Independent transaction per repository
                    try:
                        with self.txn_manager.begin_transaction(f'repo_{repo}') as repo_txn:
                            repo_txn.add_operation(
                                'update_repo',
                                forward=lambda r=repo: self.update_repository(org, r),
                                rollback=lambda r=repo: self.restore_repository(org, r)
                            )
                            repo_txn.commit()
                    except Exception as e:
                        # Individual repo failure doesn't affect others
                        print(f"Failed to update {repo}: {e}")
                        continue
                
                txn2.commit()
            
            # Sub-transaction 3: Update team settings
            with self.txn_manager.begin_transaction(f'org_teams_{org}') as txn3:
                txn3.add_operation(
                    'update_teams',
                    forward=lambda: self.update_teams(org),
                    rollback=lambda: self.restore_teams(org)
                )
                txn3.commit()
            
            # Commit parent transaction
            parent_txn.commit()
            print(f"Successfully updated organization: {org}")
```

**Key Concepts**:
- **Nested Transactions**: Sub-transactions within parent transactions
- **Partial Rollback**: Failed sub-transaction rolls back without affecting parent
- **Isolation**: Each transaction has independent commit/rollback
- **Atomicity**: Each level maintains all-or-nothing guarantee

---

### Pattern 5: Compensating Transactions

**Scenario**: Handle operations that can't be rolled back directly.

```python
from scripts.lib.transaction_manager import TransactionManager
import json
from datetime import datetime

class CompensatingTransaction:
    def __init__(self):
        self.txn_manager = TransactionManager()
        self.state_log = []
    
    def create_repository(self, org, repo_name, settings):
        """Create repository with compensating transaction"""
        
        with self.txn_manager.begin_transaction(f'create_repo_{repo_name}') as txn:
            
            # Operation 1: Create repository
            # (Can't be rolled back, so we use compensating action)
            txn.add_operation(
                'create_repository',
                forward=lambda: self.api.create_repo(org, repo_name, settings),
                rollback=lambda: self.api.delete_repo(org, repo_name)  # Compensating action
            )
            
            # Operation 2: Set up branch protection
            txn.add_operation(
                'setup_protection',
                forward=lambda: self.api.update_branch_protection(org, repo_name, 'main', {...}),
                rollback=lambda: self.api.delete_branch_protection(org, repo_name, 'main')
            )
            
            # Operation 3: Add collaborators
            txn.add_operation(
                'add_collaborators',
                forward=lambda: self.add_team_access(org, repo_name),
                rollback=lambda: self.remove_team_access(org, repo_name)
            )
            
            # Operation 4: Create initial issues
            txn.add_operation(
                'create_issues',
                forward=lambda: self.create_initial_issues(org, repo_name),
                rollback=lambda: self.close_initial_issues(org, repo_name)
            )
            
            try:
                txn.commit()
                print(f"Repository {repo_name} created successfully")
                return True
                
            except Exception as e:
                print(f"Failed to create repository: {e}")
                print("Rolling back all operations...")
                # Compensating actions execute automatically
                return False
    
    def add_team_access(self, org, repo_name):
        """Add team access with state tracking"""
        teams = ['developers', 'maintainers', 'admins']
        added_teams = []
        
        try:
            for team in teams:
                self.api.add_team_to_repo(org, repo_name, team)
                added_teams.append(team)
            
            # Save state for rollback
            self.state_log.append({
                'operation': 'add_team_access',
                'repo': repo_name,
                'teams': added_teams
            })
            
        except Exception as e:
            # Partial rollback
            for team in added_teams:
                self.api.remove_team_from_repo(org, repo_name, team)
            raise
    
    def remove_team_access(self, org, repo_name):
        """Compensating action: remove team access"""
        # Find teams from state log
        for entry in self.state_log:
            if entry['operation'] == 'add_team_access' and entry['repo'] == repo_name:
                for team in entry['teams']:
                    self.api.remove_team_from_repo(org, repo_name, team)
```

**Exercise 3.3**: Implement compensating transactions
```python
# TODO: Create a multi-step workflow with compensating actions
# TODO: Trigger a failure in step 3 of 5
# TODO: Verify all previous steps are compensated correctly
```

---

### Pattern 6: Saga Pattern for Distributed Operations

**Scenario**: Coordinate operations across multiple systems.

```python
class SagaOrchestrator:
    def __init__(self):
        self.txn_manager = TransactionManager()
        self.audit = AuditLogger(service='saga_orchestrator')
    
    def execute_saga(self, saga_name, steps):
        """Execute a saga with compensation"""
        
        with self.audit.transaction(saga_name) as audit_txn:
            with self.txn_manager.begin_transaction(saga_name) as txn:
                
                for step in steps:
                    step_name = step['name']
                    forward_action = step['forward']
                    compensating_action = step['compensate']
                    
                    audit_txn.log_event(f'step_start', {'step': step_name})
                    
                    txn.add_operation(
                        step_name,
                        forward=forward_action,
                        rollback=compensating_action
                    )
                    
                    audit_txn.log_event(f'step_complete', {'step': step_name})
                
                try:
                    txn.commit()
                    audit_txn.log_event('saga_complete', {'status': 'success'})
                    return True
                    
                except Exception as e:
                    audit_txn.log_event('saga_failed', {
                        'status': 'failure',
                        'error': str(e),
                        'compensating': True
                    })
                    # Compensating actions execute in reverse order
                    return False

# Example usage
orchestrator = SagaOrchestrator()

saga_steps = [
    {
        'name': 'create_github_repo',
        'forward': lambda: github_api.create_repo('myrepo'),
        'compensate': lambda: github_api.delete_repo('myrepo')
    },
    {
        'name': 'create_ci_pipeline',
        'forward': lambda: ci_system.create_pipeline('myrepo'),
        'compensate': lambda: ci_system.delete_pipeline('myrepo')
    },
    {
        'name': 'setup_monitoring',
        'forward': lambda: monitoring.add_repo('myrepo'),
        'compensate': lambda: monitoring.remove_repo('myrepo')
    },
    {
        'name': 'notify_team',
        'forward': lambda: slack.notify('New repo: myrepo'),
        'compensate': lambda: slack.notify('Repo creation failed: myrepo')
    }
]

success = orchestrator.execute_saga('onboard_repository', saga_steps)
```

**Exercise 3.4**: Build a saga orchestrator
```python
# TODO: Create a saga with 4 distributed operations
# TODO: Implement proper compensation for each step
# TODO: Test failure at different points in the saga
```

---

## Part 3: Performance Optimization (30 minutes)

### Pattern 7: API Client Caching Strategy

**Scenario**: Optimize API calls with intelligent caching.

```python
from scripts.lib.api_client import GitHubClient, RateLimitConfig
from functools import lru_cache
import time

class OptimizedAPIClient:
    def __init__(self):
        # Configure aggressive caching
        rate_config = RateLimitConfig(
            max_requests_per_hour=5000,
            burst_size=100,
            enable_caching=True,
            cache_ttl=3600  # 1 hour cache
        )
        
        self.api = GitHubClient(
            token=os.getenv('GITHUB_TOKEN'),
            rate_limit_config=rate_config
        )
        
        self.local_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0
    
    @lru_cache(maxsize=1000)
    def get_repository_cached(self, org, repo):
        """Get repository with local LRU cache"""
        self.cache_misses += 1
        return self.api.get_repo(org, repo)
    
    def get_repository_with_etag(self, org, repo):
        """Get repository with ETag-based caching"""
        cache_key = f"{org}/{repo}"
        
        # Check local cache
        if cache_key in self.local_cache:
            cached_data, etag, timestamp = self.local_cache[cache_key]
            
            # Cache still valid?
            if time.time() - timestamp < 300:  # 5 minutes
                self.cache_hits += 1
                return cached_data
            
            # Conditional request with ETag
            response = self.api.get_repo(
                org, repo,
                headers={'If-None-Match': etag}
            )
            
            if response.status_code == 304:  # Not Modified
                self.cache_hits += 1
                # Update timestamp
                self.local_cache[cache_key] = (cached_data, etag, time.time())
                return cached_data
        
        # Fetch fresh data
        self.cache_misses += 1
        response = self.api.get_repo(org, repo)
        
        # Cache with ETag
        etag = response.headers.get('ETag')
        self.local_cache[cache_key] = (response.json(), etag, time.time())
        
        return response.json()
    
    def get_cache_stats(self):
        """Get cache performance statistics"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = self.cache_hits / total_requests if total_requests > 0 else 0
        
        return {
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'hit_rate': f"{hit_rate:.2%}",
            'cache_size': len(self.local_cache)
        }
```

**Exercise 3.5**: Optimize API performance
```python
# TODO: Fetch 100 repositories multiple times
# TODO: Compare performance with and without caching
# TODO: Measure cache hit rate
# TODO: Calculate API rate limit savings
```

---

### Pattern 8: Batch Processing Optimization

**Scenario**: Process large datasets efficiently.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from scripts.lib.metrics_collector import MetricsCollector
import time

class BatchOptimizer:
    def __init__(self, max_workers=10):
        self.max_workers = max_workers
        self.metrics = MetricsCollector(service='batch_optimizer')
    
    def process_sequential(self, items):
        """Sequential processing (baseline)"""
        start_time = time.time()
        results = []
        
        for item in items:
            result = self.process_item(item)
            results.append(result)
        
        elapsed = time.time() - start_time
        self.metrics.record_histogram('batch_duration_sequential', elapsed)
        
        return results
    
    def process_parallel(self, items):
        """Parallel processing with thread pool"""
        start_time = time.time()
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_item = {
                executor.submit(self.process_item, item): item
                for item in items
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_item):
                item = future_to_item[future]
                try:
                    result = future.result()
                    results.append(result)
                    self.metrics.increment('items_processed_success')
                except Exception as e:
                    print(f"Failed to process {item}: {e}")
                    self.metrics.increment('items_processed_failure')
        
        elapsed = time.time() - start_time
        self.metrics.record_histogram('batch_duration_parallel', elapsed)
        
        return results
    
    def process_batched(self, items, batch_size=50):
        """Process in batches for better throughput"""
        start_time = time.time()
        results = []
        
        # Split into batches
        batches = [items[i:i+batch_size] for i in range(0, len(items), batch_size)]
        
        for batch_num, batch in enumerate(batches, 1):
            print(f"Processing batch {batch_num}/{len(batches)}")
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                batch_results = list(executor.map(self.process_item, batch))
                results.extend(batch_results)
            
            # Brief pause between batches to avoid overwhelming systems
            time.sleep(0.5)
        
        elapsed = time.time() - start_time
        self.metrics.record_histogram('batch_duration_batched', elapsed)
        
        return results
    
    def compare_performance(self, items):
        """Compare different processing strategies"""
        print(f"Processing {len(items)} items...\n")
        
        # Sequential
        print("Sequential processing...")
        start = time.time()
        self.process_sequential(items[:100])  # Sample
        seq_time = time.time() - start
        seq_rate = 100 / seq_time
        
        # Parallel
        print("Parallel processing...")
        start = time.time()
        self.process_parallel(items[:100])  # Sample
        par_time = time.time() - start
        par_rate = 100 / par_time
        
        # Batched
        print("Batched processing...")
        start = time.time()
        self.process_batched(items[:100], batch_size=20)  # Sample
        batch_time = time.time() - start
        batch_rate = 100 / batch_time
        
        # Report
        print(f"\nPerformance Comparison:")
        print(f"Sequential: {seq_time:.2f}s ({seq_rate:.1f} items/sec)")
        print(f"Parallel:   {par_time:.2f}s ({par_rate:.1f} items/sec) - {par_time/seq_time:.1f}x faster")
        print(f"Batched:    {batch_time:.2f}s ({batch_rate:.1f} items/sec) - {batch_time/seq_time:.1f}x faster")
        
        return {
            'sequential': seq_rate,
            'parallel': par_rate,
            'batched': batch_rate
        }
```

**Exercise 3.6**: Optimize batch processing
```python
# TODO: Process 500 items using all three strategies
# TODO: Measure and compare performance
# TODO: Find optimal batch size and worker count
# TODO: Consider memory usage and API rate limits
```

---

### Pattern 9: Memory-Efficient Processing

**Scenario**: Process large datasets without loading everything into memory.

```python
from scripts.lib.api_client import GitHubClient
import itertools

class MemoryEfficientProcessor:
    def __init__(self):
        self.api = GitHubClient()
    
    def stream_repositories(self, org):
        """Stream repositories without loading all into memory"""
        page = 1
        per_page = 100
        
        while True:
            repos = self.api.list_repos(
                org=org,
                page=page,
                per_page=per_page
            )
            
            if not repos:
                break
            
            for repo in repos:
                yield repo
            
            page += 1
            
            if len(repos) < per_page:
                break
    
    def process_large_dataset(self, org):
        """Process repositories one at a time"""
        processed = 0
        
        for repo in self.stream_repositories(org):
            # Process individual repo
            self.process_repository(repo)
            processed += 1
            
            if processed % 100 == 0:
                print(f"Processed {processed} repositories...")
        
        print(f"Total processed: {processed}")
    
    def process_in_chunks(self, org, chunk_size=10):
        """Process repositories in small chunks"""
        repo_stream = self.stream_repositories(org)
        
        while True:
            # Get next chunk
            chunk = list(itertools.islice(repo_stream, chunk_size))
            
            if not chunk:
                break
            
            # Process chunk
            self.process_chunk(chunk)
            
            # Explicit memory cleanup
            del chunk
```

**Exercise 3.7**: Implement memory-efficient processing
```python
# TODO: Process 1000+ repositories without loading all into memory
# TODO: Monitor memory usage during processing
# TODO: Compare memory footprint with traditional approach
```

---

## Part 4: Security & Compliance (20 minutes)

### Pattern 10: Comprehensive Security Validation

**Scenario**: Implement defense-in-depth security.

```python
from scripts.lib.security_validator import SecurityValidator
from scripts.lib.enterprise_audit import AuditLogger
from scripts.lib.config_manager import Config

class SecureAutomation:
    def __init__(self):
        self.security = SecurityValidator()
        self.audit = AuditLogger(service='secure_automation')
        self.config = Config.load(env='production')
    
    def validate_all_inputs(self, user_inputs):
        """Multi-layer input validation"""
        
        with self.audit.transaction('input_validation') as txn:
            
            # Layer 1: Type validation
            for key, value in user_inputs.items():
                expected_type = self.config.get(f'validation.{key}.type')
                if not isinstance(value, eval(expected_type)):
                    raise ValueError(f"Invalid type for {key}")
            
            # Layer 2: Pattern validation
            for key, value in user_inputs.items():
                if isinstance(value, str):
                    if not self.security.validate_input(value, input_type='identifier'):
                        txn.log_security_event('validation_failure', {
                            'field': key,
                            'reason': 'invalid_pattern'
                        })
                        raise ValueError(f"Invalid pattern in {key}")
            
            # Layer 3: Credential detection
            for key, value in user_inputs.items():
                if self.security.detect_credentials(str(value)):
                    txn.log_security_event('credential_detected', {
                        'field': key,
                        'severity': 'HIGH'
                    })
                    raise ValueError(f"Credential detected in {key}")
            
            # Layer 4: SQL injection detection
            for key, value in user_inputs.items():
                if isinstance(value, str):
                    if self.security.detect_sql_injection(value):
                        txn.log_security_event('sql_injection_attempt', {
                            'field': key,
                            'severity': 'CRITICAL'
                        })
                        raise ValueError(f"SQL injection detected in {key}")
            
            # Layer 5: Path traversal prevention
            for key, value in user_inputs.items():
                if 'path' in key.lower() or 'file' in key.lower():
                    if not self.security.validate_path(value):
                        txn.log_security_event('path_traversal_attempt', {
                            'field': key,
                            'value': value,
                            'severity': 'HIGH'
                        })
                        raise ValueError(f"Path traversal detected in {key}")
            
            txn.log_event('validation_complete', {
                'fields_validated': len(user_inputs),
                'status': 'success'
            })
            
            return True
    
    def scan_before_execution(self, script_path):
        """Security scan before executing scripts"""
        
        with self.audit.transaction('security_scan') as txn:
            
            # Scan for security issues
            findings = self.security.scan_directory(script_path)
            
            # Categorize by severity
            critical = [f for f in findings if f['severity'] == 'CRITICAL']
            high = [f for f in findings if f['severity'] == 'HIGH']
            medium = [f for f in findings if f['severity'] == 'MEDIUM']
            
            # Log findings
            txn.log_event('scan_complete', {
                'critical': len(critical),
                'high': len(high),
                'medium': len(medium)
            })
            
            # Block on critical findings
            if critical:
                txn.log_security_event('execution_blocked', {
                    'reason': 'critical_security_findings',
                    'count': len(critical)
                })
                raise SecurityError(f"Found {len(critical)} critical security issues")
            
            # Warn on high findings
            if high:
                txn.log_security_event('execution_warning', {
                    'reason': 'high_security_findings',
                    'count': len(high)
                })
                print(f"WARNING: Found {len(high)} high-severity security issues")
            
            return findings
```

**Exercise 3.8**: Build comprehensive security validation
```python
# TODO: Implement all 5 validation layers
# TODO: Test with various malicious inputs
# TODO: Verify all attacks are detected and blocked
# TODO: Ensure audit trail captures all security events
```

---

### Pattern 11: Compliance and Audit Reporting

**Scenario**: Generate compliance reports for auditors.

```python
from scripts.lib.enterprise_audit import AuditLogger
from scripts.lib.metrics_collector import MetricsCollector
from datetime import datetime, timedelta
import json

class ComplianceReporter:
    def __init__(self):
        self.audit = AuditLogger(service='compliance_reporter')
        self.metrics = MetricsCollector(service='compliance_reporter')
    
    def generate_compliance_report(self, start_date, end_date):
        """Generate comprehensive compliance report"""
        
        report = {
            'report_metadata': {
                'generated_at': datetime.utcnow().isoformat(),
                'period_start': start_date,
                'period_end': end_date,
                'report_version': '1.0'
            },
            'audit_summary': self.get_audit_summary(start_date, end_date),
            'security_events': self.get_security_events(start_date, end_date),
            'access_log': self.get_access_log(start_date, end_date),
            'changes_made': self.get_change_log(start_date, end_date),
            'compliance_metrics': self.get_compliance_metrics(start_date, end_date)
        }
        
        return report
    
    def get_audit_summary(self, start_date, end_date):
        """Get audit trail summary"""
        events = self.audit.generate_report(
            start_date=start_date,
            end_date=end_date
        )
        
        return {
            'total_transactions': len(set(e['transaction_id'] for e in events)),
            'total_events': len(events),
            'services': list(set(e['service'] for e in events)),
            'users': list(set(e.get('user', 'system') for e in events))
        }
    
    def get_security_events(self, start_date, end_date):
        """Get security-related events"""
        events = self.audit.generate_report(
            start_date=start_date,
            end_date=end_date,
            filter_by={'event_type': 'security'}
        )
        
        # Group by severity
        by_severity = {}
        for event in events:
            severity = event.get('severity', 'UNKNOWN')
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(event)
        
        return {
            'total_security_events': len(events),
            'by_severity': {k: len(v) for k, v in by_severity.items()},
            'critical_events': by_severity.get('CRITICAL', []),
            'high_events': by_severity.get('HIGH', [])
        }
    
    def get_access_log(self, start_date, end_date):
        """Get access log for audit trail"""
        events = self.audit.generate_report(
            start_date=start_date,
            end_date=end_date,
            filter_by={'event_type': 'access'}
        )
        
        return {
            'total_access_events': len(events),
            'unique_users': len(set(e.get('user') for e in events)),
            'access_by_service': self.group_by_service(events)
        }
    
    def get_change_log(self, start_date, end_date):
        """Get all changes made during period"""
        events = self.audit.generate_report(
            start_date=start_date,
            end_date=end_date,
            filter_by={'event_type': 'change'}
        )
        
        return {
            'total_changes': len(events),
            'changes_by_type': self.group_by_type(events),
            'rollbacks': [e for e in events if e.get('rollback', False)]
        }
    
    def get_compliance_metrics(self, start_date, end_date):
        """Get compliance-specific metrics"""
        return {
            'audit_coverage': self.calculate_audit_coverage(),
            'security_scan_results': self.get_security_scan_stats(),
            'failed_operations': self.get_failed_operations_count(),
            'sla_compliance': self.calculate_sla_compliance()
        }
    
    def export_report(self, report, format='json'):
        """Export compliance report"""
        
        if format == 'json':
            return json.dumps(report, indent=2)
        
        elif format == 'html':
            return self.generate_html_report(report)
        
        elif format == 'pdf':
            return self.generate_pdf_report(report)
        
        else:
            raise ValueError(f"Unsupported format: {format}")
```

**Exercise 3.9**: Generate compliance report
```python
# TODO: Run various operations with audit logging
# TODO: Generate compliance report for the period
# TODO: Verify all required data is present
# TODO: Export in multiple formats
```

---

## Part 5: Advanced API Client Features (20 minutes)

### Pattern 12: Circuit Breaker Implementation

**Scenario**: Protect against cascading failures.

```python
from scripts.lib.api_client import GitHubClient
import time
from enum import Enum

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60, success_threshold=2):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        """Execute function through circuit breaker"""
        
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.timeout:
                # Try to recover
                self.state = CircuitState.HALF_OPEN
                print("Circuit breaker moving to HALF_OPEN state")
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
            
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        """Handle successful call"""
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            
            if self.success_count >= self.success_threshold:
                # Recovery successful
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
                print("Circuit breaker CLOSED - recovered")
        else:
            # Reset failure count on success
            self.failure_count = 0
    
    def on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            print(f"Circuit breaker OPEN after {self.failure_count} failures")
        
        if self.state == CircuitState.HALF_OPEN:
            # Failed during recovery
            self.state = CircuitState.OPEN
            self.success_count = 0
            print("Circuit breaker reopened - recovery failed")

# Usage with API client
class ResilientAPIClient:
    def __init__(self):
        self.api = GitHubClient()
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=3,
            timeout=30,
            success_threshold=2
        )
    
    def get_repository(self, org, repo):
        """Get repository with circuit breaker protection"""
        return self.circuit_breaker.call(
            self.api.get_repo,
            org, repo
        )
```

**Exercise 3.10**: Implement circuit breaker
```python
# TODO: Create API client with circuit breaker
# TODO: Simulate API failures
# TODO: Verify circuit breaker opens after threshold
# TODO: Test recovery after timeout
```

---

## Part 6: Certification & Next Steps (10 minutes)

### Final Assessment Project

**Project**: Create a production-ready automation script that demonstrates mastery of all advanced features.

**Requirements**:
1. ✅ Use CLI Framework for consistent interface
2. ✅ Implement comprehensive audit logging
3. ✅ Add multi-level error recovery with checkpointing
4. ✅ Use transaction management for atomic operations
5. ✅ Implement API caching and circuit breaker
6. ✅ Add comprehensive security validation
7. ✅ Track detailed metrics
8. ✅ Generate compliance reports
9. ✅ Optimize for performance (parallel processing)
10. ✅ Include complete documentation

**Evaluation Criteria**:
- Code quality and organization (20%)
- Proper library integration (20%)
- Error handling and resilience (20%)
- Security implementation (15%)
- Performance optimization (10%)
- Documentation (10%)
- Testing coverage (5%)

**Passing Score**: 80% (160/200 points)

---

### Certification

Upon successful completion of the assessment project:

**You will receive**:
- ✅ MokoStandards Enterprise Libraries Certified Developer certificate
- ✅ Digital badge for GitHub profile
- ✅ Listed in team developer registry
- ✅ Access to advanced workshops

**Next Steps**:
1. Complete final assessment project
2. Submit pull request for review
3. Present your solution to the team
4. Receive certification upon approval

---

### Advanced Topics for Further Learning

**1. Custom Library Extensions**
- Creating custom plugins
- Extending existing libraries
- Building domain-specific libraries

**2. Distributed Automation**
- Multi-organization management
- Distributed transaction coordination
- Cross-system saga patterns

**3. Advanced Monitoring**
- Custom Prometheus exporters
- Grafana dashboard creation
- Alert rule configuration

**4. Performance Tuning**
- Profiling automation scripts
- Database query optimization
- API call optimization

**5. Security Hardening**
- Security scanning automation
- Vulnerability management
- Secrets management integration

---

## Session Summary

### What We Covered

✅ **Advanced Error Recovery**
- Multi-level retry strategies
- Checkpoint-based state recovery
- Dead letter queue pattern

✅ **Transaction Management**
- Nested transactions
- Compensating transactions
- Saga pattern for distributed operations

✅ **Performance Optimization**
- API caching strategies
- Batch processing optimization
- Memory-efficient processing

✅ **Security & Compliance**
- Multi-layer security validation
- Comprehensive audit reporting
- Compliance metrics

✅ **Advanced API Features**
- Circuit breaker implementation
- Rate limiting strategies
- Resilient API patterns

---

### Key Takeaways

1. **Resilience is key** - Implement multiple layers of error recovery
2. **Think transactionally** - Use compensating actions for rollback
3. **Optimize strategically** - Profile first, optimize bottlenecks
4. **Security is non-negotiable** - Validate at every layer
5. **Audit everything** - Compliance requires comprehensive logging

---

## Additional Resources

- **Source Code**: Review advanced examples in `/scripts/lib/`
- **Tests**: Study test patterns in `/.github/workflows/`
- **Documentation**: Deep dive into `/docs/automation/`
- **Community**: Join #mokostds-advanced on Slack

---

## Feedback

Please complete the training feedback survey:
- What worked well?
- What could be improved?
- Topics for future sessions?
- Rate overall training experience

**Contact**: training@mokoconsulting.tech

---

**Congratulations on completing the MokoStandards Enterprise Libraries Training Program!**

You now have the skills to build production-grade, enterprise-ready automation scripts using the full MokoStandards library ecosystem.

**Ready to get certified?** → Submit your assessment project for review!
