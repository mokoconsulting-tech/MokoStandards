<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/guide/php-only-architecture.md
VERSION: 04.00.01
BRIEF: Guide to MokoStandards PHP-only architecture
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# PHP-Only Architecture

**Version**: 1.0.0  
**Status**: Active  
**Last Updated**: 2026-02-14

## Table of Contents

- [Overview](#overview)
- [Architecture Benefits](#architecture-benefits)
- [PHP Enterprise Libraries](#php-enterprise-libraries)
- [Development Environment](#development-environment)
- [Best Practices](#best-practices)

---

## Overview

MokoStandards is a **100% PHP-only system** providing enterprise-grade libraries and automation tools. Built with modern PHP 8.1+ features, the system emphasizes web-native capabilities and professional development standards.

### Key Facts

✅ **13 PHP Enterprise Libraries** - All operational  
✅ **PHP 8.1+** - Modern PHP with strict types  
✅ **Web-Based** - Full browser management interface  
✅ **Composer** - Professional dependency management  
✅ **PSR Standards** - Following PHP-FIG recommendations  

---

## Architecture Benefits

### Why PHP-Only?

1. **Single Language Stack** 
   - Reduced complexity and maintenance overhead
   - Consistent coding standards across all components
   - Easier onboarding for new developers

2. **Web-Native Capabilities**
   - Built-in web server support
   - Native HTTP handling and routing
   - Session management and authentication

3. **Enterprise Features**
   - Robust type system (PHP 8.1+)
   - Comprehensive error handling
   - Professional OOP patterns

4. **Modern Tooling**
   - Composer for dependency management
   - PHPUnit for testing
   - CodeQL for security scanning (JavaScript mode)

5. **Performance**
   - PHP 8.1+ JIT compilation
   - Optimized for web workloads
   - Efficient memory management

---

## PHP Enterprise Libraries

MokoStandards includes **13 production-ready enterprise libraries** located in `src/Enterprise/`:

### Core Libraries (4)

1. **ApiClient.php** - GitHub API integration
   - Rate limiting and retry logic
   - OAuth token management
   - Circuit breaker pattern

2. **AuditLogger.php** - Transaction tracking
   - Structured logging
   - Audit trail generation
   - Compliance reporting

3. **CliFramework.php** - CLI application base
   - Argument parsing
   - Help generation
   - Exit code management

4. **Config.php** - Configuration management
   - Environment variable handling
   - YAML/JSON configuration
   - Default value management

### Validation Libraries (4)

5. **InputValidator.php** - Input sanitization
   - XSS prevention
   - SQL injection protection
   - Data type validation

6. **SecurityValidator.php** - Security scanning
   - Credential detection
   - Vulnerability scanning
   - Security policy enforcement

7. **UnifiedValidation.php** - Validation framework
   - Rule-based validation
   - Custom validators
   - Error message formatting

8. **EnterpriseReadinessValidator.php** - Compliance checking
   - Enterprise library verification
   - Documentation requirements
   - Security compliance

### Operations Libraries (3)

9. **ErrorRecovery.php** - Retry and checkpointing
   - Exponential backoff
   - State persistence
   - Transaction rollback

10. **TransactionManager.php** - ACID transactions
    - Atomic operations
    - Rollback support
    - Transaction logging

11. **RepositorySynchronizer.php** - Repository sync
    - Bulk operations
    - Checkpoint recovery
    - Progress tracking

### Monitoring Libraries (2)

12. **MetricsCollector.php** - Prometheus metrics
    - Counter, gauge, histogram
    - Label management
    - Export formatting

13. **RepositoryHealthChecker.php** - Health validation
    - 100-point scoring system
    - Category-based checks
    - Threshold comparison

---

## Development Environment

### Requirements

- **PHP**: 8.1 or higher
- **Composer**: Latest stable version
- **Extensions**: mbstring, curl, json, yaml

### Installation

```bash
# Install Composer dependencies
composer install --no-dev --optimize-autoloader

# For development
composer install

# Run tests
composer test

# Run linters
composer lint
```

### Project Structure

```
MokoStandards/
├── src/
│   └── Enterprise/          # 13 PHP libraries
├── scripts/
│   ├── automation/          # PHP CLI scripts
│   └── validate/            # PHP validation scripts
├── public/
│   └── index.php            # Web dashboard entry point
├── .github/
│   ├── workflows/           # 17 PHP/bash workflows
│   └── codeql/              # CodeQL configuration (JavaScript)
├── composer.json            # PHP dependencies
└── docs/                    # Documentation
```

---

## Best Practices

### PHP Development

1. **Use Strict Types**
   ```php
   <?php declare(strict_types=1);
   ```

2. **Follow PSR Standards**
   - PSR-4: Autoloading
   - PSR-12: Coding style
   - PSR-3: Logger interface

3. **Type Hints Everything**
   ```php
   public function process(string $input): array
   {
       // Implementation
   }
   ```

4. **Use Composer Autoloading**
   ```php
   require_once __DIR__ . '/vendor/autoload.php';
   
   use MokoStandards\Enterprise\ApiClient;
   ```

5. **Error Handling**
   ```php
   try {
       $result = $api->call();
   } catch (ApiException $e) {
       $logger->error($e->getMessage());
       throw $e;
   }
   ```

### CLI Development

Use the `CliFramework` base class for all CLI tools:

```php
<?php declare(strict_types=1);

namespace MokoStandards\Scripts;

use MokoStandards\Enterprise\CliFramework;

class MyScript extends CliFramework
{
    protected function run(): int
    {
        $this->log('Starting script...');
        
        // Your logic here
        
        return 0; // Exit code
    }
}

// Execute
$script = new MyScript();
exit($script->execute());
```

### Security

1. **Never Commit Secrets**
   - Use environment variables
   - Use `.env` files (git-ignored)
   - Use secure vaults for production

2. **Validate All Input**
   ```php
   use MokoStandards\Enterprise\InputValidator;
   
   $validator = new InputValidator();
   $clean = $validator->sanitize($_POST['input']);
   ```

3. **Use SecurityValidator**
   ```php
   use MokoStandards\Enterprise\SecurityValidator;
   
   $security = new SecurityValidator($logger);
   $results = $security->scanCredentials('/path/to/repo');
   ```

---

## See Also

- [Enterprise Libraries Overview](../training/session-1-libraries-overview.md)
- [Training Program](../training/README.md)
- [Contributing Guide](../../CONTRIBUTING.md)

---

**Last Updated**: 2026-02-14  
**Status**: Operational and Production-Ready
