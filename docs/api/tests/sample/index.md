# Sample Fixture Documentation

## Overview

`tests/sample/` (at the repository root) is a minimal generic repository fixture used by
MokoStandards API tests. This directory is gitignored (`/tests/`) and lives only on the
developer's local machine.

## Purpose

Test scripts pass `tests/sample/` as the `--path` argument to validation scripts so
that validators can be exercised locally without network access or a real GitHub repository.

## Fixture Contents

| Path | Health-check satisfied |
|---|---|
| `README.md` | README.md exists + substantial content |
| `LICENSE` | LICENSE file exists |
| `.gitignore` | .gitignore exists |
| `CHANGELOG.md` | CHANGELOG.md exists |
| `CODE_OF_CONDUCT.md` | CODE_OF_CONDUCT.md exists |
| `SECURITY.md` | SECURITY.md exists |
| `composer.json` | PHP project manifest |
| `docs/` | docs/ directory exists |
| `.github/workflows/ci.yml` | Workflows directory exists |
| `.github/dependabot.yml` | dependabot configured |

## Example Usage

```php
// From a test script at api/tests/test_*.php, __DIR__ = api/tests/
// Two levels up from api/tests/ reaches the repo root
$samplePath = __DIR__ . '/../../tests/sample';

// Platform detection
$detector = new AutoDetectPlatform();
$platform = $detector->detect($samplePath); // returns 'generic'

// Health check
$checker = new RepositoryHealthChecker($samplePath);
$score   = $checker->run(); // should reach passing threshold
```

## Related Documentation

- [Tests Documentation](../index.md)
- [Validation Scripts](../../validate/index.md)
- [API Overview](../../index.md)

---

**Location**: `docs/api/tests/sample/`
**Mirrors**: `/tests/sample/` (gitignored — local only)
**Last Updated**: 2026-03-04
**Maintained By**: MokoStandards Team
