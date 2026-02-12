# Python to PHP Script Recreation Guide

## Overview

This document explains how Python scripts were recreated as PHP equivalents after being deleted from the repository.

## Background

- **Commits**: c1b91fb (23 library files) and e695587 (68 script files)
- **Date**: February 12, 2026
- **Total Deleted**: 91 Python files (~36,000 lines)
- **Reason**: Transition to PHP-only web-based architecture (v04.00.00)

## Recreated Scripts (3/68)

### 1. Automation
- **bulk_update_repos.php** - Repository synchronization tool
  - Original: `scripts/automation/bulk_update_repos.py`
  - Uses: ApiClient, AuditLogger, ErrorRecovery, MetricsCollector
  - Features: GitHub API integration, checkpointing, metrics

### 2. Validation  
- **check_repo_health.php** - Repository health checker
  - Original: `scripts/validate/check_repo_health.py`
  - Uses: AuditLogger, MetricsCollector, UnifiedValidation
  - Features: Scoring system, JSON output, threshold validation

- **check_enterprise_readiness.php** - Enterprise compliance validator
  - Original: `scripts/validate/check_enterprise_readiness.py`
  - Uses: AuditLogger, SecurityValidator
  - Features: Library checks, security scanning, documentation validation

## Recreation Process

### 1. Examine Git History
```bash
# List deleted files
git show --name-only --pretty="" e695587

# View original Python source
git show e695587~1:scripts/automation/bulk_update_repos.py

# Check specific functionality
git show e695587~1:scripts/validate/check_repo_health.py | head -200
```

### 2. Create PHP Equivalent

**Template Structure**:
```php
#!/usr/bin/env php
<?php
/**
 * Copyright (C) 2026 Moko Consulting
 * SPDX-License-Identifier: GPL-3.0-or-later
 * 
 * FILE INFORMATION
 * VERSION: 04.00.00
 * BRIEF: [Description]
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\{
    CliFramework,
    // Other required libraries
};

class MyScript extends CliFramework
{
    protected function configure(): void {
        // Define arguments
    }
    
    protected function run(): int {
        // Main logic
        return 0;
    }
}

$app = new MyScript();
exit($app->execute($argv));
```

### 3. Make Executable
```bash
chmod +x scripts/automation/my_script.php
```

### 4. Validate Syntax
```bash
php -l scripts/automation/my_script.php
```

### 5. Test Functionality
```bash
./scripts/automation/my_script.php --help
./scripts/automation/my_script.php --dry-run
```

## PHP Enterprise Libraries Available

All scripts can use these libraries from `src/Enterprise/`:

- **ApiClient.php** - GitHub API with rate limiting
- **AuditLogger.php** - Transaction tracking, security events
- **CliFramework.php** - Base class for CLI apps
- **Config.php** - Configuration management
- **ErrorRecovery.php** - Checkpoint-based recovery
- **InputValidator.php** - Input validation, XSS/SQL protection
- **MetricsCollector.php** - Prometheus metrics
- **SecurityValidator.php** - Security scanning
- **TransactionManager.php** - ACID transactions
- **UnifiedValidation.php** - Validation framework

## Remaining Scripts to Recreate

### Priority List (65 scripts remaining)

**High Priority Automation**:
- auto_create_org_projects.py
- detect_version_bump.py
- setup_enterprise_repo.py
- install_terraform.py

**High Priority Maintenance**:
- clean_old_branches.py
- release_version.py
- update_changelog.py
- flush_actions_cache.py

**High Priority Release**:
- unified_release.py
- detect_platform.py
- package_extension.py

**High Priority Validation**:
- security_scan.py
- no_secrets.py
- check_script_security.py
- validate_structure.py

## Key Differences Python vs PHP

### Python Pattern
```python
import argparse
from enterprise_audit import AuditLogger

parser = argparse.ArgumentParser()
parser.add_argument('--org', default='mokoconsulting-tech')
args = parser.parse_args()

logger = AuditLogger('script')
# ... logic ...
```

### PHP Pattern
```php
use MokoStandards\Enterprise\{CliFramework, AuditLogger};

class MyScript extends CliFramework {
    protected function configure(): void {
        $this->addArgument('--org', 'Organization', 'mokoconsulting-tech');
    }
    
    protected function run(): int {
        $org = $this->getArgument('--org');
        $logger = new AuditLogger('script');
        // ... logic ...
        return 0;
    }
}
```

## Benefits of PHP Version

✅ **Type Safety**: Strict types, full type hints  
✅ **Enterprise Features**: Built-in audit, metrics, error recovery  
✅ **Modern PHP**: 8.1+ features, PSR-4 autoloading  
✅ **Better Error Handling**: Exceptions throughout  
✅ **Web Integration**: Can be called from dashboard  
✅ **Consistent Architecture**: All use same patterns  

## Documentation

All PHP scripts include:
- GPL-3.0-or-later license header
- Full file metadata (DEFGROUP, INGROUP, PATH, VERSION)
- Executable shebang (#!/usr/bin/env php)
- PHPDoc comments
- Usage examples in --help output

## Testing

```bash
# Install dependencies (one time)
composer install

# Test script syntax
php -l scripts/automation/my_script.php

# Run with help
./scripts/automation/my_script.php --help

# Test with dry-run
./scripts/automation/my_script.php --dry-run

# Run actual operation
./scripts/automation/my_script.php --org mokoconsulting-tech
```

## Status

- ✅ **Deleted**: 91 Python files (100%)
- ✅ **Recreated**: 3 PHP scripts (4%)
- ⏳ **Remaining**: 65 scripts can be recreated from git history as needed

All deleted Python scripts are preserved in git history and can be referenced or recreated at any time.

## Future Work

As additional functionality is needed:
1. Identify which Python script provided that functionality
2. Find it in git history (commits c1b91fb or e695587)
3. Examine the Python source code
4. Recreate as PHP using the template above
5. Test and validate
6. Document in this guide

---

**Version**: 04.00.00  
**Last Updated**: February 12, 2026  
**Status**: Active Development
