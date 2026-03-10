# GitHub Copilot Instructions for MokoStandards

## Repository Overview

**MokoStandards** is the authoritative source of coding standards, architectural patterns, GitHub Actions workflow templates, governance policies, and PHP automation libraries for the Moko Consulting ecosystem. It is **Tier 2 (Public SOURCE OF TRUTH)** — do **not** clone or duplicate it to start new projects; use the template repositories instead.

- **Languages**: PHP (primary), Python, PowerShell, Bash, YAML, Terraform HCL
- **PHP requirement**: ≥ 8.1; Composer-managed dependencies
- **License**: GPL-3.0-or-later
- **Version**: 04.00.04 (semantic versioning `MM.mm.pp` style used throughout)

---

## Directory Layout

```
.github/            GitHub Actions workflows + config
api/                Main API directory (replaces legacy scripts/)
  automation/       Automation scripts (bulk_sync.php, etc.)
  build/            Build helpers
  definitions/      Repository structure definitions (.tf files, HCL format)
    default/        Platform base definitions (crm-module.tf, standards-repository.tf, …)
    sync/           Auto-generated per-repo definitions ({repo}.def.tf)
  fix/              Auto-fix scripts
  lib/              Shared libraries
    Enterprise/     PHP Enterprise classes (PluginFactory, RepositoryHealthChecker, …)
    plugins/        Project-type plugins (Joomla, Dolibarr)
  maintenance/      Maintenance scripts
  release/          Release automation
  src/              PSR-4 autoloaded source (namespace MokoStandards\)
  tests/            PHPUnit tests (namespace MokoStandards\Tests\)
  validate/         Validation scripts (auto_detect_platform.php, check_repo_health.php, …)
  wrappers/         Cross-platform wrapper scripts (PowerShell / Bash, 100+)
docs/               238 documentation files
  policy/           77 policy documents (file-header-standards.md, coding-style-guide.md, …)
  training/         7 training sessions
  guide/            Implementation guides
  reference/        Technical references
  enforcement-levels.md   45 KB six-tier enforcement guide (OPTIONAL→FORCED→NOT_ALLOWED)
templates/          Project templates and config templates
logs/               Runtime log output (gitignored)
```

---

## Build, Lint, Test Commands

Always run `composer install` before any PHP command when `vendor/` is absent.

```bash
# Install dependencies
composer install

# Run all checks (phpcs + phpstan + phpunit)
composer run check

# Code style (PSR-12, 120-char line limit, no var_dump/eval)
composer run phpcs          # or: ./vendor/bin/phpcs

# Static analysis (level 5, paths: api/src, api/tests)
composer run phpstan        # or: ./vendor/bin/phpstan analyse api/src/ api/tests/

# Type checking
./vendor/bin/psalm          # psalm.xml config at repo root

# Unit tests
composer run test           # or: ./vendor/bin/phpunit

# YAML lint
yamllint .

# Markdown lint
markdownlint "**/*.md"

# Python lint (pyproject.toml config)
pylint <file>
```

Key config files: `phpcs.xml`, `phpstan.neon`, `psalm.xml`, `pyproject.toml`, `.eslintrc.json`, `.markdownlint.json`, `.yamllint`, `.editorconfig`.

The CI workflows that must pass before merge are in `.github/workflows/`:
- `standards-compliance.yml` — 28 validation checks (structure, headers, code style, docs, license)
- `security-comprehensive.yml` / `security-scan.yml` — CodeQL + secret scanning
- `integration-tests.yml` — integration test suite
- `validate-script-integrity.yml` — script registry integrity

---

## Coding Standards (mandatory)

### File Headers

Every file that supports comments **must** start with a copyright block. Use the comment syntax for the file type:

```php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.<Group>
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /<relative-path-from-repo-root>
 * VERSION: 04.00.04
 * BRIEF: <one-line description>
 */
```

For YAML, Markdown, Bash/shell, Python — adapt the comment delimiter accordingly. JSON files do not support comments and are exempt. See `docs/policy/file-header-standards.md` for complete examples.

### Indentation

| File type | Style |
|-----------|-------|
| PHP, PowerShell, Bash, Terraform | **Tabs** |
| YAML, Python, JSON, RST | **Spaces** (YAML=2, Python=4, JSON=2) |
| Makefiles | **Tabs** (required by Make) |

See `.editorconfig` for authoritative per-extension rules.

### PHP Style

- PSR-12 + `declare(strict_types=1)` at top of every file
- Namespace prefix: `MokoStandards\` (autoloaded from `api/src/`)
- Enterprise classes live under `MokoStandards\Enterprise\` (source: `api/lib/Enterprise/`)
- Forbidden: `eval`, `create_function`, `var_dump`, `print_r`
- Max line length: 120 characters (hard limit 150)
- Use typed properties and return types

### Commit / Version discipline

- **Bump the patch version on every PR** — increment `MM.mm.pp` (e.g. `04.00.04` → `04.00.05`) in `README.md` before opening the PR; the `sync-version-on-merge` workflow propagates it to all file headers and badges on merge
- Update `VERSION` field in every modified file header
- Keep `CHANGELOG.md` current for every PR
- Semantic version format: `MM.mm.pp` (e.g., `04.00.03`)
- Conventional commits are expected (see `.gitmessage`)

---

## Key Architecture Points

- **Plugin system**: All validation/automation scripts use `PluginFactory` and `ProjectTypeDetector`. Call `PluginFactory::createForProject()` for auto-detection; do not instantiate plugins directly.
- **Circuit breaker**: `ApiClient` implements a circuit breaker. In bulk-sync loops, reset it before each repository to prevent state leakage.
- **Repository definitions**: Definition files are Terraform HCL (`.tf` extension) stored in `api/definitions/default/`. Auto-generated per-repo definitions go in `api/definitions/sync/` with the pattern `{repo}.def.tf`. Do **not** create `.github/override.tf` in remote repos manually — the bulk sync workflow handles this.
- **Documentation mirrors API**: `docs/api/` mirrors `api/` structure. Subdirectories use `index.md` files only, never `README.md`.
- **Dolibarr module IDs**: Sequential IDs reserved in `docs/development/crm/module-registry.md`. Always check this file for the current next available ID before reserving a new one.
- **Six-tier enforcement**: Files synced to repos follow OPTIONAL → SUGGESTED → REQUIRED → FORCED → NOT_SUGGESTED → NOT_ALLOWED. NOT_ALLOWED takes absolute priority. See `docs/enforcement-levels.md`.

---

## Keeping Documentation Current

Whenever you make code changes, update the corresponding documentation in the same commit or PR. Do not leave docs stale.

| Change type | Documentation to update |
|-------------|------------------------|
| New or renamed public PHP method | PHPDoc block on the method; `docs/api/` index for that class |
| New or changed CLI script argument | Script's own `--help` text; `docs/api/validate/` or equivalent |
| New or changed GitHub Actions workflow | `docs/workflows/<workflow-name>.md` |
| New or changed enforcement rule | `docs/enforcement-levels.md` |
| New or changed policy | Corresponding file under `docs/policy/` |
| New library class or major feature | `CHANGELOG.md` entry under `Added` |
| Bug fix | `CHANGELOG.md` entry under `Fixed` |
| Breaking change | `CHANGELOG.md` entry under `Changed`; update `CONTRIBUTING.md` if contributor steps change |
| Any modified file | Update the `VERSION` field in that file's `FILE INFORMATION` block |
| **Every PR** | **Bump the patch version** — increment `MM.mm.pp` in `README.md`; `sync-version-on-merge` propagates it to all headers and badges on merge |

If your code change makes any existing doc sentence false or incomplete, fix the doc before closing the PR.

---

## Validation Before Committing

Run these locally before pushing:

```bash
# Full quality check
composer run check

# YAML lint
yamllint .

# Standards compliance (mirrors the CI workflow)
php api/validate/auto_detect_platform.php --path .
php api/validate/check_repo_health.php --path .
```

Trust these instructions. Only search the codebase for additional context if the instructions above are incomplete or appear out-of-date for your specific task.
