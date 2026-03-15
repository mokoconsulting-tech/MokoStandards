<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/guide/php-only-architecture.md
VERSION: 04.00.15
BRIEF: Guide to MokoStandards PHP-only architecture
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.15-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# PHP-Only Architecture

**Version**: 04.00.15
**Status**: Active
**Last Updated**: 2026-03-15

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

✅ **28+ PHP Enterprise Library Classes** — All operational
✅ **PHP 8.1+** — Modern PHP with strict types
✅ **CLI-first** — All scripts extend `CliFramework` for consistent argument parsing and exit codes
✅ **Composer** — Professional dependency management
✅ **PSR Standards** — PSR-4 autoloading, PSR-12 coding style  

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

MokoStandards includes **28+ production-ready enterprise library classes** located in `api/lib/Enterprise/`:

### Core Classes

| Class | Purpose |
|-------|---------|
| `CliFramework.php` | Base class for all CLI scripts — argument parsing, help, exit codes |
| `ApiClient.php` | GitHub API integration with rate limiting and circuit breaker |
| `AuditLogger.php` | Structured logging and audit trail generation |
| `Config.php` | Environment variable and YAML/JSON configuration management |

### Validation Classes

| Class | Purpose |
|-------|---------|
| `InputValidator.php` | Input sanitization; XSS and injection prevention |
| `SecurityValidator.php` | Credential scanning and security policy enforcement |
| `UnifiedValidation.php` | Rule-based validation framework with custom validators |
| `EnterpriseReadinessValidator.php` | Repository enterprise-readiness compliance scoring |
| `ProjectConfigValidator.php` | Validates project configuration against schema |

### Operations Classes

| Class | Purpose |
|-------|---------|
| `RepositorySynchronizer.php` | Bulk repository sync with checkpoint recovery |
| `CheckpointManager.php` | Persistent checkpoint storage for long-running operations |
| `TransactionManager.php` | Atomic operations with rollback support |
| `ErrorRecovery.php` | Retry logic with exponential backoff |
| `RecoveryManager.php` | High-level recovery orchestration |
| `RetryHelper.php` | Configurable retry helper for transient failures |
| `PackageBuilder.php` | Extension package (ZIP) assembly |

### Monitoring and Metrics Classes

| Class | Purpose |
|-------|---------|
| `MetricsCollector.php` | Prometheus-format metrics (counters, gauges, histograms) |
| `RepositoryHealthChecker.php` | 100-point repository health scoring |
| `ProjectMetricsCollector.php` | GitHub Project-level metrics aggregation |

### Plugin System Classes

| Class | Purpose |
|-------|---------|
| `AbstractProjectPlugin.php` | Base class for all project-type plugins |
| `ProjectPluginInterface.php` | Interface contract for project plugins |
| `PluginFactory.php` | Instantiates the correct plugin for a repository type |
| `PluginRegistry.php` | Registry of all available project plugins |
| `ProjectTypeDetector.php` | Detects repository type (Joomla / Dolibarr / generic / etc.) |
| `DefinitionParser.php` | Parses `.tf`-format repository definition files |

### Plugin Implementations (`api/lib/Enterprise/Plugins/`)

| Class | Platform |
|-------|---------|
| `JoomlaPlugin.php` | Joomla extensions |
| `DolibarrPlugin.php` | Dolibarr modules |
| `WordPressPlugin.php` | WordPress plugins |
| `ApiPlugin.php` | REST API projects |
| `NodeJsPlugin.php` | Node.js projects |
| `PythonPlugin.php` | Python projects |
| `TerraformPlugin.php` | Terraform modules |
| `MobilePlugin.php` | Mobile applications |
| `DocumentationPlugin.php` | Documentation-only repositories |
| `GenericPlugin.php` | Fallback for unrecognized types |

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
│   └── Enterprise/          # 28+ PHP enterprise library classes
│       └── Plugins/         # Project-type plugin implementations
├── api/
│   ├── automation/          # Bulk-sync and automation scripts
│   ├── deploy/              # SFTP deployment scripts
│   ├── fix/                 # Automated fix scripts
│   ├── maintenance/         # Repository housekeeping scripts
│   ├── validate/            # Validation and quality-check scripts
│   └── wrappers/            # Wrapper scripts (one per CLI script)
├── templates/               # Files synced to governed repositories
├── .github/
│   └── workflows/           # Workflows governing THIS repository
├── composer.json            # PHP dependencies
└── docs/                    # Documentation (never executable code)
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

   use MokoEnterprise\ApiClient;
   use MokoEnterprise\CliFramework;
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
<?php
declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CliFramework;

class MyScript extends CliFramework
{
	protected function configure(): void
	{
		$this->setDescription('What this script does');
		$this->addArgument('--path', 'Repository path', '.');
	}

	protected function execute(): int
	{
		// Your logic here
		return 0;
	}
}

$script = new MyScript();
exit($script->run());
```

### Security

1. **Never Commit Secrets**
   - Use environment variables
   - Use `.env` files (git-ignored)
   - Use secure vaults for production

2. **Validate All Input**
   ```php
   use MokoEnterprise\InputValidator;
   
   $validator = new InputValidator();
   $clean = $validator->sanitize($_POST['input']);
   ```

3. **Use SecurityValidator**
   ```php
   use MokoEnterprise\SecurityValidator;
   
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
