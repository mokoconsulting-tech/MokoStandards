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
VERSION: 04.00.00
BRIEF: Session 1 - Enterprise Libraries Overview training materials
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Session 1: Enterprise Libraries Overview

**Duration**: 2 hours  
**Format**: Presentation + Live Demos  
**Prerequisite**: Basic PHP 8.1+ and Git knowledge

---

## Session Objectives

By the end of this session, you will:
- ✅ Understand all 13 PHP enterprise libraries and their purposes
- ✅ Know when to use each library in your scripts
- ✅ See live demonstrations of each library in action
- ✅ Complete basic hands-on exercises
- ✅ Navigate library documentation effectively

---

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 0:00-0:15 | Introduction & Setup | Presentation |
| 0:15-0:45 | Core Libraries (1-7) | Demo + Discussion |
| 0:45-1:15 | Advanced Libraries (8-13) | Demo + Discussion |
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

### The 13 PHP Enterprise Libraries Overview

| # | Library | Purpose | Priority |
|---|---------|---------|----------|
| 1 | AuditLogger | Transaction tracking & compliance | CRITICAL |
| 2 | ApiClient | Rate-limited, resilient API calls | CRITICAL |
| 3 | CliFramework | Standardized command-line interface | HIGH |
| 4 | Config | Environment-aware configuration | HIGH |
| 5 | ErrorRecovery | Automatic retry & checkpointing | HIGH |
| 6 | InputValidator | Input sanitization & validation | HIGH |
| 7 | MetricsCollector | Observability & monitoring | MEDIUM |
| 8 | SecurityValidator | Security scanning & validation | HIGH |
| 9 | TransactionManager | Atomic operations & rollback | MEDIUM |
| 10 | UnifiedValidation | Multi-source validation framework | MEDIUM |
| 11 | RepositorySynchronizer | Repository sync operations | MEDIUM |
| 12 | RepositoryHealthChecker | Repository health monitoring | MEDIUM |
| 13 | EnterpriseReadinessValidator | Enterprise compliance validation | MEDIUM |

---

## Part 2: Core Libraries (30 minutes)

### 1. AuditLogger Library ⭐ CRITICAL

**File**: `src/Enterprise/AuditLogger.php` (470 lines)

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
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\AuditLogger;

// Initialize logger for your service
$logger = new AuditLogger(
    service: 'demo_script',
    retentionDays: 90
);

// Start a transaction
$transaction = $logger->startTransaction('user_provisioning');

try {
    // Log individual steps
    $transaction->logEvent('create_user', [
        'username' => 'john.doe',
        'email' => 'john@example.com',
        'status' => 'success'
    ]);
    
    $transaction->logEvent('assign_permissions', [
        'permissions' => ['read', 'write'],
        'status' => 'success'
    ]);
    
    // Transaction automatically completes
    $transaction->end();
    
} catch (Exception $e) {
    $transaction->fail($e->getMessage());
    throw $e;
}

// Log security events
$logger->logSecurityEvent(
    eventType: 'login_attempt',
    severity: 'INFO',
    details: ['user' => 'admin', 'ip' => '192.168.1.1']
);

// Generate audit report
$report = $logger->generateReport(
    startDate: '2026-01-01',
    endDate: '2026-02-01',
    filterBy: ['service' => 'demo_script']
);
echo "Found " . count($report) . " audit events\n";
```

**Exercise 1.1**: Create an audit trail
```php
<?php
// TODO: Create an audit logger and log a transaction with 3 steps
// Steps: validate_input -> process_data -> save_results
// Include relevant metadata for each step
```

---

### 2. ApiClient Library ⭐ CRITICAL

**File**: `src/Enterprise/ApiClient.php` (580 lines)

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
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\ApiClient;
use MokoStandards\Enterprise\RateLimitExceeded;
use MokoStandards\Enterprise\CircuitBreakerOpen;

// Initialize client with rate limiting
$client = new ApiClient(
    baseUrl: 'https://api.github.com',
    authToken: getenv('GITHUB_TOKEN'),
    maxRequestsPerHour: 5000,
    enableCaching: true,
    cacheTtl: 300  // 5 minutes
);

// Automatic rate limiting in action
try {
    // List repositories (cached for 5 minutes)
    $repos = $client->get('/orgs/mokoconsulting-tech/repos');
    echo "Found " . count($repos) . " repositories\n";
    
    // Get repository details (with retry and circuit breaker)
    foreach (array_slice($repos, 0, 5) as $repo) {
        $details = $client->get("/repos/mokoconsulting-tech/{$repo['name']}");
        echo "Repo: {$details['name']}, Stars: {$details['stargazers_count']}\n";
    }
    
} catch (RateLimitExceeded $e) {
    echo "Rate limit exceeded: {$e->getMessage()}\n";
} catch (CircuitBreakerOpen $e) {
    echo "Circuit breaker open: {$e->getMessage()}\n";
}

// Check rate limit status
$status = $client->getRateLimitStatus();
echo "Remaining requests: {$status['remaining']}/{$status['limit']}\n";
```

**Exercise 1.2**: Use API client with rate limiting
```php
<?php
// TODO: Create an ApiClient and list all issues in a repository
// Configure rate limiting to 1000 requests per hour
// Print the title of each issue
```

---

### 3. CliFramework Library

**File**: `src/Enterprise/CliFramework.php` (470 lines)

**Purpose**: Standardized command-line interface for all automation scripts.

**Key Features**:
- CliApp base class for consistent structure
- Common options (--verbose, --dry-run, --json, --config)
- Integrated logging setup
- Enterprise library integration
- Standard error handling and exit codes

**When to Use**:
- ✅ Every new automation script
- ✅ Scripts requiring command-line arguments
- ✅ Scripts needing consistent error handling
- ✅ User-facing automation tools

**Live Demo**:
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\CliFramework;
use Symfony\Component\Console\Input\InputOption;

class MyAutomationScript extends CliFramework
{
    protected function configure(): void
    {
        parent::configure();
        
        $this
            ->setName('my-automation')
            ->setDescription('My automation script')
            ->addOption('org', null, InputOption::VALUE_REQUIRED, 'GitHub organization')
            ->addOption('repo', null, InputOption::VALUE_OPTIONAL, 'Specific repository');
    }
    
    protected function execute($input, $output): int
    {
        $org = $input->getOption('org');
        $repo = $input->getOption('repo');
        
        $this->logger->info("Processing organization: {$org}");
        
        if ($input->getOption('dry-run')) {
            $this->logger->warning('DRY RUN: No changes will be made');
        }
        
        // Your automation logic here
        $results = $this->processOrganization($org, $repo);
        
        if ($input->getOption('json')) {
            $this->outputJson($results);
        } else {
            $this->outputText($results);
        }
        
        return 0;  // Success exit code
    }
    
    private function processOrganization(string $org, ?string $repo = null): array
    {
        return [
            'org' => $org,
            'processed' => 42,
            'errors' => 0
        ];
    }
}

// Run the application
$app = new MyAutomationScript();
exit($app->execute());
```

**Usage**:
```bash
# Standard usage
php my_script.php --org mokoconsulting-tech

# Dry run mode
php my_script.php --org mokoconsulting-tech --dry-run

# Verbose logging
php my_script.php --org mokoconsulting-tech --verbose

# JSON output
php my_script.php --org mokoconsulting-tech --json
```

**Exercise 1.3**: Create a CLI application
```php
<?php
// TODO: Create a CliFramework subclass that accepts --name option
// Print "Hello, {name}!" when run
// Add --uppercase flag to print in uppercase
```

---

### 4. Config Library

**File**: `src/Enterprise/Config.php` (320 lines)

**Purpose**: Environment-aware configuration management with validation.

**Key Features**:
- Environment-specific configs (dev, staging, production)
- Dot notation access (`$config->get('db.host')`)
- Type-safe getters
- Runtime overrides
- Configuration validation

**When to Use**:
- ✅ Scripts with environment-specific settings
- ✅ Complex configuration structures
- ✅ Multi-environment deployments
- ✅ Configuration validation needs

**Live Demo**:
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\Config;

// Load configuration for current environment
$config = Config::load('production');

// Access with dot notation
$dbHost = $config->get('database.host');
$dbPort = $config->get('database.port', 5432);

// Type-safe getters
$maxRetries = $config->getInt('api.max_retries', 3);
$enableCache = $config->getBool('api.cache.enabled', true);
$timeout = $config->getFloat('api.timeout', 30.0);

// Runtime overrides (for testing)
$config->set('api.max_retries', 5);

// Validate required keys
$config->require(['database.host', 'database.port', 'api.token']);

// Export configuration
$config->exportEnvVars();  // Sets environment variables
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

**Exercise 1.4**: Load and use configuration
```php
<?php
// TODO: Create a config file with your settings
// Load it and access values using dot notation
// Validate that required keys exist
```

---

### 5. ErrorRecovery Library ⭐ HIGH PRIORITY

**File**: `src/Enterprise/ErrorRecovery.php` (390 lines)

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
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\ErrorRecovery;
use MokoStandards\Enterprise\Checkpoint;

// Automatic retry with attribute
class ApiService
{
    #[RetryWithBackoff(maxRetries: 3, baseDelay: 1.0)]
    public function fetchDataFromApi(string $url): array
    {
        // Automatically retries on failure with exponential backoff
        // Uses the ApiClient internally which handles HTTP properly
        $client = new \GuzzleHttp\Client();
        $response = $client->get($url);
        
        if ($response->getStatusCode() !== 200) {
            throw new RuntimeException('Failed to fetch data');
        }
        
        return json_decode($response->getBody()->getContents(), true);
    }
}

// Checkpointing for batch operations
$checkpoint = new Checkpoint(
    name: 'process_repos',
    checkpointDir: '/tmp/checkpoints'
);

$repositories = ['repo1', 'repo2', 'repo3', 'repo4', 'repo5'];

foreach ($repositories as $repo) {
    if ($checkpoint->isCompleted($repo)) {
        echo "Skipping {$repo} (already processed)\n";
        continue;
    }
    
    try {
        // Process repository
        $result = processRepository($repo);
        
        // Mark as completed
        $checkpoint->markCompleted($repo, $result);
        
    } catch (Exception $e) {
        echo "Failed to process {$repo}: {$e->getMessage()}\n";
        $checkpoint->markFailed($repo, $e->getMessage());
    }
}

// Recovery after failure
if ($checkpoint->hasFailures()) {
    $failed = $checkpoint->getFailures();
    echo "Retry " . count($failed) . " failed items\n";
}
```

**Exercise 1.5**: Implement error recovery
```php
<?php
// TODO: Create a function that fails randomly (50% chance)
// Use #[RetryWithBackoff] to automatically retry
// Use checkpointing to track progress
```

---

## Part 3: Advanced Libraries (30 minutes)

### 6. InputValidator Library

**File**: `src/Enterprise/InputValidator.php` (450 lines)

**Purpose**: Comprehensive input sanitization and validation.

**Key Features**:
- Multi-format validation (email, URL, IP, etc.)
- XSS prevention and sanitization
- SQL injection detection
- Custom validation rules
- Type coercion with validation

**When to Use**:
- ✅ Validating user input
- ✅ API request validation
- ✅ Form data processing
- ✅ Security-critical input handling

**Live Demo**:
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\InputValidator;

$validator = new InputValidator();

// Email validation
$email = $validator->validateEmail('user@example.com');
if ($email === null) {
    echo "Invalid email\n";
}

// URL validation and sanitization
$url = $validator->validateUrl('https://example.com/path?query=value');

// Sanitize HTML input (XSS prevention)
$safeHtml = $validator->sanitizeHtml('<script>alert("XSS")</script><p>Safe content</p>');
// Result: '<p>Safe content</p>'

// Custom validation rules
$validator->addRule('username', function($value) {
    return preg_match('/^[a-z0-9_]{3,20}$/i', $value);
});

$username = $validator->validate('john_doe123', 'username');
```

**Exercise 1.6**: Input validation
```php
<?php
// TODO: Create a validator and validate multiple inputs
// Validate: email, URL, and a custom phone number format
// Handle validation errors appropriately
```

---

### 7. MetricsCollector Library

**File**: `src/Enterprise/MetricsCollector.php` (340 lines)

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
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\MetricsCollector;

// Initialize metrics collector
$metrics = new MetricsCollector(service: 'my_script');

// Counter: increment operations
$metrics->increment('repositories_processed', ['org' => 'mokoconsulting-tech']);
$metrics->increment('api_calls_total', ['method' => 'GET', 'endpoint' => '/repos']);

// Gauge: set current value
$metrics->setGauge('active_connections', 42);
$metrics->setGauge('queue_size', 128);

// Histogram: track distributions
$metrics->recordHistogram('request_duration_seconds', 0.234);
$metrics->recordHistogram('file_size_bytes', 1024000);

// Time tracking
$startTime = microtime(true);
processRepository();
$duration = microtime(true) - $startTime;
$metrics->recordHistogram('process_repository_duration', $duration);

// Export metrics
$prometheusData = $metrics->exportPrometheus();
echo $prometheusData;

// Get specific metric
$totalProcessed = $metrics->getCounter('repositories_processed');
echo "Total processed: {$totalProcessed}\n";
```

**Exercise 1.7**: Track metrics
```php
<?php
// TODO: Create a metrics collector
// Track: operations_total (counter), error_rate (gauge), duration (histogram)
// Export to Prometheus format
```

---

### 8. SecurityValidator Library ⭐ HIGH PRIORITY

**File**: `src/Enterprise/SecurityValidator.php` (430 lines)

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
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\SecurityValidator;

$validator = new SecurityValidator();

// Scan a directory for security issues
$findings = $validator->scanDirectory('/path/to/code');

foreach ($findings as $finding) {
    echo "{$finding['severity']}: {$finding['message']}\n";
    echo "  File: {$finding['file']}:{$finding['line']}\n";
}

// Validate file permissions
$isSafe = $validator->checkFilePermissions('/path/to/script.sh');

// Detect credentials in code
$hasSecrets = $validator->detectCredentials($codeContent);

// Validate user input for path traversal
$safePath = $validator->validatePath($userInput);
```

**Exercise 1.8**: Security scanning
```php
<?php
// TODO: Scan the src/Enterprise directory for security issues
// Print a summary of findings by severity
```

---

### 9. TransactionManager Library

**File**: `src/Enterprise/TransactionManager.php` (300 lines)

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
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\TransactionManager;

$manager = new TransactionManager();

try {
    $txn = $manager->beginTransaction('update_repos');
    
    // Step 1: Update repository settings
    $txn->addOperation(
        name: 'update_settings',
        operation: fn() => updateRepoSettings('repo1'),
        rollback: fn() => restoreRepoSettings('repo1')
    );
    
    // Step 2: Update branch protection
    $txn->addOperation(
        name: 'update_protection',
        operation: fn() => updateBranchProtection('repo1', 'main'),
        rollback: fn() => restoreBranchProtection('repo1', 'main')
    );
    
    // Step 3: Update webhooks
    $txn->addOperation(
        name: 'update_webhooks',
        operation: fn() => updateWebhooks('repo1'),
        rollback: fn() => restoreWebhooks('repo1')
    );
    
    // Commit transaction (executes all operations)
    $txn->commit();
    
} catch (Exception $e) {
    // Automatic rollback occurred
    echo "Transaction failed and rolled back: {$e->getMessage()}\n";
}

// View transaction history
$history = $manager->getHistory();
echo "Completed " . count($history) . " transactions\n";
```

**Exercise 1.9**: Use transaction management
```php
<?php
// TODO: Create a transaction with 3 operations
// Make one operation fail and verify rollback occurs
// Check transaction history
```

---

### 10. UnifiedValidation Library

**File**: `src/Enterprise/UnifiedValidation.php` (450 lines)

**Purpose**: Multi-source validation framework with pluggable validators.

**Key Features**:
- Unified validation API
- Support for multiple validation sources
- Composite validation rules
- Validation result aggregation
- Custom validator plugins

**When to Use**:
- ✅ Complex validation scenarios
- ✅ Multi-step validation pipelines
- ✅ Combining multiple validation sources
- ✅ Enterprise compliance checks

**Live Demo**:
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\UnifiedValidation;

$validator = new UnifiedValidation();

// Add multiple validators
$validator->addValidator('email', new EmailValidator());
$validator->addValidator('security', new SecurityValidator());
$validator->addValidator('business', new BusinessRuleValidator());

// Validate data through all validators
$data = [
    'email' => 'user@example.com',
    'password' => 'SecurePass123!',
    'role' => 'admin'
];

$result = $validator->validateAll($data);

if ($result->isValid()) {
    echo "All validations passed\n";
} else {
    foreach ($result->getErrors() as $error) {
        echo "Error: {$error['message']}\n";
    }
}
```

---

### 11. RepositorySynchronizer Library

**File**: `src/Enterprise/RepositorySynchronizer.php` (280 lines)

**Purpose**: Automated repository synchronization and configuration management.

**Key Features**:
- Repository settings sync
- Branch protection synchronization
- Webhook management
- Label synchronization
- Team permission sync

**When to Use**:
- ✅ Managing multiple repositories
- ✅ Standardizing repository configuration
- ✅ Bulk repository updates
- ✅ Repository compliance enforcement

**Live Demo**:
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\RepositorySynchronizer;

$synchronizer = new RepositorySynchronizer(
    apiClient: $apiClient,
    auditLogger: $logger
);

// Sync repository settings
$synchronizer->syncSettings(
    org: 'mokoconsulting-tech',
    repos: ['repo1', 'repo2'],
    settings: [
        'has_issues' => true,
        'has_wiki' => false,
        'allow_squash_merge' => true
    ]
);

// Sync branch protection
$synchronizer->syncBranchProtection(
    org: 'mokoconsulting-tech',
    repos: ['repo1', 'repo2'],
    branch: 'main',
    rules: [
        'required_reviews' => 2,
        'enforce_admins' => true
    ]
);
```

---

### 12. RepositoryHealthChecker Library

**File**: `src/Enterprise/RepositoryHealthChecker.php` (320 lines)

**Purpose**: Comprehensive repository health monitoring and reporting.

**Key Features**:
- Repository health scoring
- Security check validation
- Documentation completeness
- CI/CD status monitoring
- Dependency health checks

**When to Use**:
- ✅ Regular health audits
- ✅ Compliance reporting
- ✅ Quality gate enforcement
- ✅ Repository metrics tracking

**Live Demo**:
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\RepositoryHealthChecker;

$healthChecker = new RepositoryHealthChecker(
    apiClient: $apiClient,
    thresholds: [
        'min_health_score' => 75,
        'max_open_issues' => 50,
        'max_pr_age_days' => 30
    ]
);

// Check repository health
$health = $healthChecker->checkHealth(
    org: 'mokoconsulting-tech',
    repo: 'MokoStandards'
);

echo "Health Score: {$health['score']}/100\n";
echo "Status: {$health['status']}\n";

foreach ($health['checks'] as $check) {
    echo "  [{$check['status']}] {$check['name']}\n";
}
```

---

### 13. EnterpriseReadinessValidator Library

**File**: `src/Enterprise/EnterpriseReadinessValidator.php` (280 lines)

**Purpose**: Validate enterprise compliance and readiness standards.

**Key Features**:
- Security compliance validation
- Documentation requirement checks
- CI/CD pipeline validation
- License compliance verification
- Code quality standards

**When to Use**:
- ✅ Pre-production deployment checks
- ✅ Enterprise certification
- ✅ Compliance audits
- ✅ Quality gate validation

**Live Demo**:
```php
<?php

declare(strict_types=1);

use MokoStandards\Enterprise\EnterpriseReadinessValidator;

$validator = new EnterpriseReadinessValidator();

// Validate enterprise readiness
$result = $validator->validate(
    org: 'mokoconsulting-tech',
    repo: 'MokoStandards'
);

echo "Enterprise Ready: " . ($result['ready'] ? 'YES' : 'NO') . "\n";
echo "Compliance Score: {$result['score']}%\n";

foreach ($result['requirements'] as $req) {
    $status = $req['met'] ? '✅' : '❌';
    echo "{$status} {$req['name']}\n";
}
```

---

### Exercise Set 2: Quick Challenges

**Challenge 1**: Create an audit logger and log a 3-step transaction  
**Challenge 2**: Use the API client to fetch all issues from a repository  
**Challenge 3**: Create a CLI app with custom options  
**Challenge 4**: Implement checkpointing for a batch operation  
**Challenge 5**: Scan a directory for security issues and generate a report  

---

## Part 5: Q&A and Resources (20 minutes)

### Common Questions

**Q: Which libraries should I use in every script?**
A: At minimum, use CliFramework for consistency and AuditLogger for compliance.

**Q: Can I use these libraries together?**
A: Yes! They're designed to work together. See Session 2 for integration patterns.

**Q: What about performance overhead?**
A: Minimal. Most libraries add <50ms overhead. Session 3 covers optimization.

**Q: How do I handle library updates?**
A: Follow semantic versioning. Check CHANGELOG.md for breaking changes via `composer update`.

**Q: Can I extend these libraries?**
A: Yes! All libraries support extension via inheritance and composition. See source code for details.

### Quick Reference Guide

| Need | Use This Library | Key Class/Function |
|------|------------------|-------------------|
| Audit trail | AuditLogger.php | AuditLogger |
| API calls | ApiClient.php | ApiClient |
| CLI interface | CliFramework.php | CliFramework |
| Configuration | Config.php | Config |
| Error recovery | ErrorRecovery.php | #[RetryWithBackoff], Checkpoint |
| Input validation | InputValidator.php | InputValidator |
| Metrics | MetricsCollector.php | MetricsCollector |
| Security | SecurityValidator.php | SecurityValidator |
| Transactions | TransactionManager.php | TransactionManager |
| Unified validation | UnifiedValidation.php | UnifiedValidation |
| Repo sync | RepositorySynchronizer.php | RepositorySynchronizer |
| Health checks | RepositoryHealthChecker.php | RepositoryHealthChecker |
| Readiness | EnterpriseReadinessValidator.php | EnterpriseReadinessValidator |

### Resources for Further Learning

1. **Source Code**: `/src/Enterprise/` - Read the actual implementation
2. **Tests**: `/tests/` - See usage examples in unit tests
3. **Documentation**: `/docs/automation/README.md` - Complete automation guide
4. **Planning**: `/docs/planning/README.md` - Implementation roadmap
5. **Composer**: `composer.json` - Dependency management and autoloading

---

## Knowledge Check Quiz

**Question 1**: Which library should you use for tracking API rate limits?
- a) MetricsCollector.php
- b) ApiClient.php ✅
- c) ErrorRecovery.php
- d) AuditLogger.php

**Question 2**: What attribute provides automatic retry logic in PHP 8.1+?
- a) #[Transaction]
- b) #[Recoverable]
- c) #[RetryWithBackoff] ✅
- d) #[Resilient]

**Question 3**: Which library provides compliance audit trails?
- a) AuditLogger.php ✅
- b) TransactionManager.php
- c) SecurityValidator.php
- d) MetricsCollector.php

**Question 4**: What's the base class for CLI applications?
- a) CliBase
- b) CliFramework ✅
- c) Application
- d) BaseScript

**Question 5**: Which library detects security vulnerabilities?
- a) InputValidator.php
- b) SecurityScanner.php
- c) SecurityValidator.php ✅
- d) VulnerabilityDetector.php

---

## Session Summary

### What We Covered
✅ All 13 PHP enterprise libraries and their purposes  
✅ Live demonstrations of each library  
✅ Basic hands-on exercises  
✅ When to use each library  
✅ Integration basics  

### Key Takeaways
1. **Enterprise libraries provide consistency** across all automation
2. **Use multiple libraries together** for enterprise-grade scripts
3. **Start simple** - add libraries as needed
4. **Read the source code** - it's well-documented with full docblocks
5. **Practice with exercises** - hands-on learning is key
6. **Use PSR-4 autoloading** - follow PHP standards

### Next Steps
1. ✅ Complete all hands-on exercises
2. 📝 Review library source code in `src/Enterprise/`
3. 🔨 Migrate a simple script to use 2-3 libraries
4. 📚 Read Session 2 materials before next session
5. ❓ Prepare questions for Session 2

---

## Homework Assignment (Optional)

Create a simple automation script that:
1. Uses CliFramework for argument parsing
2. Uses AuditLogger to log operations
3. Uses ApiClient to fetch data from GitHub
4. Uses MetricsCollector to track performance
5. Prints a summary report

**Setup**:
```bash
# Install dependencies
composer install

# Set GitHub token
export GITHUB_TOKEN="your_token_here"

# Run your script
php my_script.php --org mokoconsulting-tech
```

**Due**: Before Session 2  
**Estimated Time**: 1-2 hours

---

**Ready for more?** → Continue to [Session 2: Practical Integration Workshop](session-2-integration-workshop.md)
