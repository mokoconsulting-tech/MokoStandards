# Tests Documentation

## Overview

Documentation for the test suite in `/api/tests/` of the `mokoconsulting/mokostandards` package.

## Test Files

### test_circuit_breaker_handling.php

Verifies that `CircuitBreakerOpen` and `RateLimitExceeded` exceptions are throwable and
catchable, and that `ApiClient` trips its circuit breaker after repeated failures.

**Run:**
```bash
php api/tests/test_circuit_breaker_handling.php
```

### test_enterprise_libraries.php

Smoke-tests all Enterprise library classes:
`MetricsCollector`, `SecurityValidator`, `TransactionManager`, `UnifiedValidator`,
`CLIApp` (`CliFramework`).

**Run:**
```bash
php api/tests/test_enterprise_libraries.php
```

## Sample Fixture

`tests/sample/` (at the repository root) is a minimal generic repository used to exercise
validators (`check_repo_health.php`, `auto_detect_platform.php`) against a local path without
requiring network access or a real GitHub repository.

This directory is excluded from version control via `.gitignore` (`/tests/`) and must be
created locally by each developer. It contains:

| Path | Purpose |
|---|---|
| `README.md` | Substantial README (satisfies health-check threshold) |
| `LICENSE` | GPL-3.0-or-later |
| `.gitignore` | Basic ignore rules |
| `CHANGELOG.md` | Keep-a-Changelog stub |
| `CODE_OF_CONDUCT.md` | Contributor Covenant stub |
| `SECURITY.md` | Vulnerability reporting policy |
| `composer.json` | PHP project manifest (`mokoconsulting/sample-repo`) |
| `docs/` | Minimal docs directory |
| `.github/workflows/ci.yml` | Sample CI workflow |
| `.github/dependabot.yml` | Dependabot configuration |

See [`docs/api/tests/sample/index.md`](./sample/index.md) for details.

## Related Documentation

- [API Overview](../index.md)

---

**Location**: `docs/api/tests/`
**Mirrors**: `/api/tests/`
**Last Updated**: 2026-03-04
**Maintained By**: MokoStandards Team
