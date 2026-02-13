<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/guide/dual-language-architecture.md
VERSION: 04.00.00
BRIEF: Guide to MokoStandards dual-language architecture (Python + PHP)
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Dual-Language Architecture: Python + PHP

**Version**: 1.0.0  
**Status**: ⚠️ **HISTORICAL - OBSOLETE**  
**Last Updated**: 2026-02-13  
**Obsolete Date**: 2026-02-12

---

> **⚠️ HISTORICAL DOCUMENT - NO LONGER APPLICABLE**
>
> This document describes a dual-language architecture that existed only during the transition period.
> As of **February 12, 2026**, MokoStandards is **100% PHP-only**.
>
> **See**: [PHP-Only Architecture Guide](php-only-architecture.md) for current architecture.

---

## Overview

~~MokoStandards now operates as a **dual-language system**~~ **This architecture is obsolete** ❌

MokoStandards **previously operated** as a dual-language system during the migration period (Feb 11-12, 2026):
- **Python**: CLI automation, GitHub Actions workflows, scripting ❌ **REMOVED**
- **PHP**: Web-based management interface, API endpoints, browser UI ✅ **ACTIVE**

**Current Status**: All Python code has been removed. The system is now PHP-only.

### Migration Completed

~~Both languages coexist~~ **Python has been completely removed** ✅

Current state:
- **Automation & CI/CD** → Use PHP scripts or bash
- **Web Management & Dashboards** → Use PHP web interface
- **API Integration** → Use PHP only

### Historical Goals (Obsolete)

~~✅ **Python Strengths**: DevOps automation, CLI tools, GitHub Actions integration~~ ❌ **REMOVED**  
✅ **PHP Strengths**: Web applications, browser UIs, server-side rendering  
✅ **Unified System**: Shared audit logs, metrics, and configuration  
✅ **Gradual Migration**: PHP libraries added incrementally alongside Python

---

## Architecture Strategy

### Current State (v04.00.00)

```
MokoStandards Repository
│
├── Python Implementation (Complete)
│   ├── scripts/lib/          # 10 enterprise libraries
│   │   ├── enterprise_audit.py
│   │   ├── api_client.py
│   │   ├── config_manager.py
│   │   ├── error_recovery.py
│   │   ├── input_validator.py
│   │   ├── metrics_collector.py
│   │   ├── security_validator.py
│   │   ├── transaction_manager.py
│   │   ├── unified_validation.py
│   │   └── cli_framework.py
│   │
│   ├── scripts/automation/   # 90 automation scripts
│   ├── scripts/maintenance/  # Branch/release management
│   └── scripts/release/      # Release orchestration
│
├── PHP Implementation (In Progress - Web Focus)
│   ├── src/Enterprise/       # 2/10 libraries converted
│   │   ├── AuditLogger.php   ✅
│   │   ├── ApiClient.php     ✅
│   │   └── [8 more pending]
│   │
│   ├── src/Web/             # Web-specific components
│   │   ├── Controller/      # HTTP controllers
│   │   ├── Router/          # URL routing
│   │   └── View/            # Templates
│   │
│   └── public/              # Web entry point
│       └── index.php        # Main web application
│
└── Shared Resources
    ├── logs/audit/          # Shared by both languages
    ├── logs/metrics/        # Shared by both languages
    └── .env                 # Shared configuration
```

### Design Principles

1. **Coexistence**: Both languages remain fully functional
2. **Shared State**: Common audit logs, metrics, and configuration
3. **Language-Appropriate**: Use Python for CLI/automation, PHP for web
4. **Feature Parity**: PHP libraries match Python functionality
5. **Independent Evolution**: Languages can be updated separately

---

## Language Distribution

### When to Use Python

✅ **GitHub Actions Workflows**
```yaml
- name: Run automation
  run: python scripts/automation/bulk_update_repos.py
```

✅ **CLI Operations**
```bash
./scripts/maintenance/clean_old_branches.py --dry-run
./scripts/release/unified_release.py bump patch
```

✅ **CI/CD Pipelines**
- Version bump detection
- Branch cleanup
- Release automation
- Terraform deployment

✅ **Cron Jobs & Scheduled Tasks**
```bash
0 0 * * 0 python scripts/automation/weekly_audit.py
```

### When to Use PHP

✅ **Web Dashboard**
```
http://localhost:8000/dashboard
```

✅ **API Endpoints**
```
GET  /api/status
GET  /api/metrics
POST /api/repositories/sync
```

✅ **Browser-Based Management**
- Repository configuration
- Audit log viewing
- Metrics visualization
- User authentication

✅ **Web Hooks**
```php
// Handle GitHub webhooks
POST /webhooks/github
```

---

## Library Equivalence Matrix

### Enterprise Libraries Status

| Library | Python | PHP | Status | Notes |
|---------|--------|-----|--------|-------|
| **Audit Logging** | `enterprise_audit.py` | `AuditLogger.php` | ✅ Complete | Feature parity achieved |
| **API Client** | `api_client.py` | `ApiClient.php` | ✅ Complete | GitHub API, rate limiting, circuit breaker |
| **Config Manager** | `config_manager.py` | `ConfigManager.php` | ⏳ Pending | Next in conversion queue |
| **Error Recovery** | `error_recovery.py` | `ErrorRecovery.php` | ⏳ Pending | Retry logic, checkpointing |
| **Input Validator** | `input_validator.py` | `InputValidator.php` | ⏳ Pending | Sanitization, validation |
| **Metrics Collector** | `metrics_collector.py` | `MetricsCollector.php` | ⏳ Pending | Prometheus export |
| **Security Validator** | `security_validator.py` | `SecurityValidator.php` | ⏳ Pending | Vulnerability scanning |
| **Transaction Manager** | `transaction_manager.py` | `TransactionManager.php` | ⏳ Pending | Atomic operations |
| **Unified Validation** | `unified_validation.py` | `UnifiedValidation.php` | ⏳ Pending | Validation framework |
| **CLI Framework** | `cli_framework.py` | `CliFramework.php` | ⏳ Pending | Command-line interface |

### Automation Scripts

| Category | Python Scripts | PHP Equivalent | Notes |
|----------|----------------|----------------|-------|
| **Repository Sync** | `bulk_update_repos.py` | Web UI | PHP provides web interface |
| **Project Creation** | `auto_create_org_projects.py` | Web API | `/api/projects/create` |
| **Branch Cleanup** | `clean_old_branches.py` | Scheduled Task | PHP cron job |
| **Release Management** | `unified_release.py` | Web UI | Dashboard-based release |

---

## Usage Guidelines

### Calling Python from PHP

PHP can execute Python scripts when needed:

```php
use Symfony\Component\Process\Process;

$process = new Process([
    'python3',
    '/path/to/scripts/automation/bulk_update_repos.py',
    '--org', 'mokoconsulting-tech'
]);
$process->run();

if (!$process->isSuccessful()) {
    throw new RuntimeException($process->getErrorOutput());
}

$output = $process->getOutput();
```

### Calling PHP from Python

Python can invoke PHP web APIs:

```python
import requests

response = requests.post('http://localhost:8000/api/repositories/sync', json={
    'repository': 'MokoStandards',
    'branch': 'main'
})

if response.status_code == 200:
    result = response.json()
    print(f"Sync complete: {result}")
```

### Shared Audit Logging

Both languages write to the same audit log format:

**Python:**
```python
from enterprise_audit import AuditLogger

logger = AuditLogger('my_script')
with logger.transaction('operation') as txn:
    txn.log_event('step_complete', {'status': 'ok'})
```

**PHP:**
```php
use MokoStandards\Enterprise\AuditLogger;

$logger = new AuditLogger('my_script');
$txn = $logger->startTransaction('operation');
$txn->logEvent('step_complete', ['status' => 'ok']);
$txn->end('success');
```

Both produce identical JSONL audit logs in `logs/audit/`.

---

## Integration Patterns

### Pattern 1: CLI Automation with Web Monitoring

```
┌─────────────┐
│   Python    │  Runs automation
│   Script    │  Writes audit logs
└──────┬──────┘
       │
       ├────────► logs/audit/*.jsonl
       │
┌──────▼──────┐
│     PHP     │  Reads audit logs
│  Dashboard  │  Displays in browser
└─────────────┘
```

### Pattern 2: Web-Triggered Automation

```
┌─────────────┐
│   Browser   │  User clicks "Sync Repos"
└──────┬──────┘
       │
┌──────▼──────┐
│     PHP     │  Receives request
│  Controller │  Queues job
└──────┬──────┘
       │
┌──────▼──────┐
│   Python    │  Executes automation
│   Script    │  via Process or queue
└─────────────┘
```

### Pattern 3: Hybrid Operations

```
User Request → PHP Web UI
                 │
                 ├─► PHP ApiClient → GitHub API (fast queries)
                 │
                 └─► Python Script → Complex automation (background)
```

---

## Development Workflow

### Adding a New Feature

1. **Decide Language**:
   - CLI/Automation → Python
   - Web UI/Dashboard → PHP
   - Both needed → Implement in primary language, expose via API

2. **Implement in Primary Language**:
   ```bash
   # Python
   scripts/new_feature/my_script.py
   
   # PHP
   src/Web/Controller/MyController.php
   ```

3. **Add Tests**:
   ```bash
   # Python
   scripts/tests/test_my_script.py
   
   # PHP
   tests/Web/Controller/MyControllerTest.php
   ```

4. **Update Documentation**:
   - Add to appropriate language section
   - Update equivalence matrix if applicable
   - Document API endpoints for cross-language access

5. **Verify Integration**:
   - Test audit logging from both languages
   - Verify metrics collection
   - Check shared configuration

---

## Best Practices

### DO ✅

- **Use Python** for GitHub Actions, CLI tools, automation scripts
- **Use PHP** for web dashboards, browser UIs, HTTP APIs
- **Share** audit logs, metrics, and configuration between languages
- **Document** which language implements each feature
- **Test** cross-language integration points
- **Maintain** feature parity where needed

### DON'T ❌

- Don't duplicate entire codebases unnecessarily
- Don't mix languages in single script files
- Don't create language-specific silos for shared data
- Don't skip documentation when adding new features
- Don't break existing Python automation when adding PHP

---

## Future Roadmap

### Short Term (Month 1)
- Complete PHP library conversions (8 remaining)
- Build web dashboard with repository overview
- Add authentication system (PHP)
- Implement job queue for background tasks

### Medium Term (Quarter 1)
- Real-time metrics dashboard
- Web-based configuration editor
- Audit log viewer with search/filter
- API documentation (Swagger/OpenAPI)

### Long Term (Year 1)
- Full-featured web management portal
- Mobile-responsive design
- Role-based access control
- SSO integration
- Webhook management UI

---

## Support & Resources

### Documentation
- [Python Scripts Documentation](../scripts/)
- [PHP API Reference](../../src/)
- [Web Application Guide](./web-application.md)
- [API Documentation](./api-reference.md)

### Examples
- [Python → PHP Integration Examples](../examples/python-php/)
- [Shared Audit Logging Examples](../examples/audit-logging/)
- [Cross-Language API Calls](../examples/api-integration/)

---

**Last Updated**: 2026-02-11  
**Document Owner**: MokoStandards Team  
**Status**: Active  
**Review Schedule**: Monthly
