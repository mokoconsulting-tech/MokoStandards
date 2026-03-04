# Docs Index: /api/tests/sample

## Purpose

Minimal generic repository fixture used by MokoStandards API tests.
Test scripts pass `api/tests/sample/` as the `--path` argument to validators
such as `check_repo_health.php` and `auto_detect_platform.php`.

## Contents

| File / Directory | Description |
|---|---|
| `README.md` | Repository overview with substantial content |
| `LICENSE` | GPL-3.0-or-later licence text |
| `.gitignore` | Minimal ignore rules |
| `CHANGELOG.md` | Keep-a-Changelog format history |
| `CODE_OF_CONDUCT.md` | Contributor Covenant pledge |
| `SECURITY.md` | Vulnerability reporting policy |
| `composer.json` | PHP project manifest (`mokoconsulting/sample-repo`) |
| `docs/` | Minimal documentation directory |
| `.github/workflows/ci.yml` | Sample CI workflow |
| `.github/dependabot.yml` | Dependabot configuration |

## Usage in Tests

```php
$samplePath = __DIR__ . '/sample';
$result = $healthChecker->check($samplePath);
```

## Related Documentation

- [Tests Documentation](../index.md)
- [API Overview](../../index.md)
