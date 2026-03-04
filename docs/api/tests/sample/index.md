# Sample Fixture Documentation

## Overview

`api/tests/sample/` is a minimal generic repository fixture used by MokoStandards API tests.

## Purpose

Test scripts pass `api/tests/sample/` as the `--path` argument to validation scripts so
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
$samplePath = __DIR__ . '/../tests/sample';

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
**Mirrors**: `/api/tests/sample/`
**Last Updated**: 2026-03-04
**Maintained By**: MokoStandards Team
