# What This Repo Is

MokoStandards is the authoritative standards, policy, and automation repository for all Moko Consulting repositories (https://github.com/mokoconsulting-tech/MokoStandards). It publishes the six-tier file-enforcement system, copyright-header policies, coding-style rules, reusable GitHub Actions workflows, PHP enterprise libraries, and Terraform configuration templates that every governed repository must follow. It is **not** a project template to clone, not a runnable application, and not a monorepo root — it is the single source of truth that other repositories pull standards from via the bulk-sync workflow.

# Repo Structure

```
MokoStandards/
├── api/                  # All executable PHP scripts and enterprise libraries
│   ├── automation/       # Bulk-sync and other automation scripts (bulk_sync.php)
│   ├── build/            # Build-related helpers
│   ├── definitions/      # Repository structure definition files (.tf extension, HCL/XML content)
│   ├── fix/              # One-off fix scripts
│   ├── lib/              # PHP enterprise library source (13 classes under lib/Enterprise/)
│   ├── maintenance/      # Housekeeping scripts
│   ├── release/          # Release automation
│   ├── run/              # Runtime helpers
│   ├── src/              # Additional PHP source (autoload, bootstrap)
│   ├── tests/            # PHPUnit test suite
│   ├── validate/         # Validation scripts (check_repo_health.php, scan_drift.php, etc.)
│   └── wrappers/         # PHP wrapper scripts — one per CLI script; add logging and repo-root detection
├── docs/                 # All documentation (never executable code)
│   ├── guide/            # How-to guides for contributors and maintainers
│   ├── policy/           # Binding policy documents (enforcement, coding style, file headers, etc.)
│   ├── training/         # Seven-session training curriculum
│   ├── workflows/        # Documentation for each GitHub Actions workflow
│   └── …                 # adr/, checklist/, reference/, schemas/, terraform/, etc.
├── templates/            # Files synced out to governed repositories
│   ├── configs/          # Linter configs (.eslintrc.json, phpcs.xml, gitignore, etc.)
│   ├── docs/             # Required and optional document templates (README, CHANGELOG, etc.)
│   ├── github/           # Issue templates, PR template, settings.yml, dependabot.yml
│   ├── terraform/        # Terraform module stubs and repository-management helpers
│   └── workflows/        # GitHub Actions workflow templates (.yml.template files)
├── logs/                 # Runtime logs from bulk-sync and validation runs (not committed)
├── .github/              # Workflows that govern THIS repository (standards-compliance, bulk-repo-sync, etc.)
├── .editorconfig         # Indentation/encoding rules (authoritative for all languages)
├── .gitmessage           # Commit message template — configure with: git config commit.template .gitmessage
├── phpcs.xml             # PHP_CodeSniffer ruleset (PSR-12 + project rules)
├── phpstan.neon          # PHPStan static analysis config (level 5)
├── psalm.xml             # Psalm type-checker config
├── composer.json         # PHP dependency manifest
├── CONTRIBUTING.md       # Contributor workflow and code standards
├── CHANGELOG.md          # Full version history
└── ROADMAP.md            # Planned work
```

# Six-Tier Enforcement System

This repository defines and uses the MokoStandards six-tier enforcement system. Full details in `docs/enforcement-levels.md`.

| Level | Name | Behavior | Overridable? |
|-------|------|----------|-------------|
| 1 | **OPTIONAL** | Not synced by default; must explicitly opt-in | ✅ Yes |
| 2 | **SUGGESTED** | Synced by default; excluded with warnings only | ✅ Yes |
| 3 | **REQUIRED** | Mandatory; exclusion causes errors | ❌ No |
| 4 | **FORCED** | Always synced; six critical compliance files | ❌ No |
| 5 | **NOT_SUGGESTED** | Discouraged; presence triggers warnings | ✅ Yes (with warning) |
| 6 | **NOT_ALLOWED** | Absolutely prohibited; checked before all else | ❌ **Never** |

Processing order during bulk sync: Level 6 → 4 → 3 → 2 → 5 → 1.

# File Header Requirements

Every new file **must** have a copyright header as its very first content. JSON files, binary files, generated files, and third-party files are exempt.

## Minimal header (use for most files)

**Markdown:**
```markdown
<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/example.md
VERSION: XX.YY.ZZ
BRIEF: One-line description of file purpose
-->
```

**PHP:**
```php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts.Validate
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/validate/example.php
 * VERSION: XX.YY.ZZ
 * BRIEF: One-line description of file purpose
 */
```

**YAML / Shell / Python:** Same pattern using `#` comments; Python uses a module docstring.

## Full header (add GPL warranty disclaimer)

Use for: policy documents, public-facing APIs, security-sensitive code, README files (warranty must appear as **visible text** in README, not in a comment). Also required for `index.php` directory-protection files and Dolibarr module descriptor files.

## FILE INFORMATION block fields

| Field | Required | Description |
|-------|----------|-------------|
| `DEFGROUP` | ✅ | Logical group — e.g. `MokoStandards.Policy`, `MokoStandards.Scripts.Validate` |
| `INGROUP` | ✅ | Parent group — e.g. `MokoStandards.Documentation` |
| `REPO` | ✅ | Full repository URL |
| `PATH` | ✅ | Absolute path from repo root, starting with `/` |
| `VERSION` | ✅ | Zero-padded semver: `04.00.04` not `4.0.3` |
| `BRIEF` | ✅ | ≤ 80 chars; starts with noun or action verb |
| `NOTE` | optional | Additional warnings or context |

## Exempt file types

Binary files, JSON (no comment syntax), auto-generated files (mark with `// @generated`), third-party vendored files.

# Coding Standards

## Indentation (from `.editorconfig`)

| File type | Style | Width |
|-----------|-------|-------|
| Default (PHP, Markdown, etc.) | **Tabs** | 2 |
| YAML (`.yml`, `.yaml`) | Spaces | 2 |
| JSON | Spaces | 2 |

## Line length

- **PHP**: warn at 120 chars, hard limit 150 (from `phpcs.xml`)
- **Markdown**: no limit (`.editorconfig` sets `max_line_length = off`)

## Naming conventions

**PHP** (PSR-12):
- Classes: `PascalCase` — `RepositorySynchronizer`
- Methods / functions: `camelCase` — `getUserData()`
- Variables: `$snake_case` — `$user_id`
- Constants: `UPPER_SNAKE_CASE` — `DEFAULT_THRESHOLD`
- Files: `PascalCase.php` for classes, `snake_case.php` for scripts

**YAML workflow files:** `kebab-case.yml`

## Primary language for new code

**PHP 8.1+** is the exclusive language for all automation scripts, validators, wrappers, and library classes in `api/`. No Python or shell scripts exist in this repository.

# Language-Specific Requirements

## PHP

All scripts in `api/` use `declare(strict_types=1)` and extend `CliFramework` from `api/lib/Enterprise/CliFramework.php`.

**Script structure template:**
```php
#!/usr/bin/env php
<?php
/* … file header … */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\{AuditLogger, CliFramework, MetricsCollector};

class MyScript extends CliFramework
{
    protected function configure(): void
    {
        $this->setDescription('What this script does');
        $this->addArgument('--path', 'Repository path', '.');
    }

    protected function execute(): int
    {
        // implementation
        return 0;
    }
}

$script = new MyScript();
exit($script->run());
```

**PHPDoc (required for all public methods):**
```php
/**
 * Brief description.
 *
 * @param string $path  Repository path to inspect
 * @param bool   $dry   Dry-run mode; no changes written
 * @return int          Exit code (0 = success)
 * @throws RuntimeException  When path does not exist
 */
public function check(string $path, bool $dry = false): int
```

**Error handling:** throw typed exceptions; catch at the `CliFramework` boundary; exit codes follow POSIX (0 = success, 1 = general failure, 2 = misuse).

**Forbidden:** `eval()`, `create_function()`, `var_dump()`, `print_r()` (enforced by `phpcs.xml`).


# Commit Message Format

Configure once with: `git config commit.template .gitmessage`

```
<type>(<scope>): <subject>
# types: build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test
# subject: imperative, lower-case, no trailing period

# Body: what and why

# BREAKING CHANGE: <description>
# Closes: #123
# Signed-off-by: <Your Name> <you@example.com>
```

**Subject line rules:** imperative mood ("add" not "added"), lower-case, no period, ≤ 72 chars.

**Valid types:**

| Type | When to use |
|------|-------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `chore` | Maintenance, dependency bumps, tooling |
| `ci` | GitHub Actions / workflow changes |
| `refactor` | Code restructure with no behaviour change |
| `style` | Formatting, whitespace |
| `test` | Adding or fixing tests |
| `perf` | Performance improvement |
| `revert` | Reverts a previous commit |
| `build` | Build system or compilation changes |

# Running Validation

Run these before committing:

```bash
# PHP syntax check
find api -name "*.php" -exec php -l {} \;

# PHP CodeSniffer (PSR-12 + project rules)
./vendor/bin/phpcs --standard=phpcs.xml api/

# PHPStan static analysis (level 5)
./vendor/bin/phpstan analyse -c phpstan.neon api/

# Psalm type checker
./vendor/bin/psalm --config=psalm.xml

# PHPUnit tests
./vendor/bin/phpunit api/tests/

# Validate file headers across repo
php api/validate/auto_detect_platform.php --path .

# Repository health check
php api/validate/check_repo_health.php --path .

# Version consistency check
php api/validate/check_version_consistency.php --path .

```

# Contribution Workflow

1. **Fork** the repository on GitHub.
2. **Branch** — name must match `(prefix)/MAJOR.MINOR.PATCH[/description]`.
   - Approved prefixes: `dev/`, `rc/`, `version/`, `patch/`, `copilot/`, `dependabot/`
   - Examples: `dev/4.0.4/add-new-validator`, `patch/4.0.4/fix-header-check`
   - ❌ `feature/my-thing` is rejected by branch protection.
3. **Configure git:**
   ```bash
   git config commit.template .gitmessage
   ```
4. **Install dependencies:**
   ```bash
   composer install
   ```
5. **Make changes** following all standards above.
6. **Validate** — run the full validation suite (see above).
7. **Commit** using conventional commit format.
8. **Push** and open a PR against `main`.
9. **PR title** becomes the squash-commit subject line — write it carefully.
10. **PR description** becomes the squash-commit body.

**Merge strategy:** squash merge only (merge commits and rebase merges are disabled). Branches are auto-deleted after merge. Never commit directly to `main`.

# Keeping Documentation Current

Whenever you make code changes, update the corresponding documentation in the same commit or PR. Do not leave docs stale.

| Change type | Documentation to update |
|-------------|------------------------|
| New or renamed public PHP method | PHPDoc block on the method; `docs/api/` index for that class |
| New or changed CLI script argument | Script's own `--help` text (via `setDescription`/`addArgument`); `docs/api/validate/` or equivalent |
| New or changed GitHub Actions workflow | `docs/workflows/<workflow-name>.md` |
| New or changed enforcement rule | `docs/enforcement-levels.md` |
| New or changed policy | Corresponding file under `docs/policy/` |
| New library class or major feature | `CHANGELOG.md` entry under `Added` |
| Bug fix | `CHANGELOG.md` entry under `Fixed` |
| Breaking change | `CHANGELOG.md` entry under `Changed`; update `CONTRIBUTING.md` if contributor steps change |
| Any modified file | Update the `VERSION` field in that file's `FILE INFORMATION` block |
| **Every PR** | **Bump the patch version** — increment `MM.mm.pp` in `README.md`; `sync-version-on-merge` propagates it to all headers and badges on merge |

**Rule**: if your code change makes any existing doc sentence false or incomplete, fix the doc before closing the PR. The PR checklist item `docs/ updated if public-facing behaviour changed` is a reminder, not a suggestion.

# PR Checklist

- [ ] Patch version bumped in `README.md` (`MM.mm.pp` → next patch)
- [ ] Branch name follows `(prefix)/MAJOR.MINOR.PATCH[/description]` format
- [ ] All new files have a correct FILE INFORMATION header
- [ ] Version badge added to any new Markdown files
- [ ] No hardcoded version numbers in body text (use badge or file-info header)
- [ ] `declare(strict_types=1)` in all new PHP files
- [ ] PHPDoc on all public PHP methods
- [ ] `phpcs` passes with zero errors
- [ ] `phpstan` passes at level 5
- [ ] PHPUnit tests pass; new logic has test coverage
- [ ] CHANGELOG.md updated with a meaningful entry
- [ ] `docs/` updated if public-facing behaviour changed
- [ ] PR title is a valid conventional-commit subject line
- [ ] No secrets, tokens, or credentials in any file
- [ ] No `var_dump`, `print_r`, `eval`, or `create_function` in PHP
- [ ] All CI checks green before requesting review

# What NOT to Do

- **Never commit directly to `main`** — all changes go through a PR.
- **Never use `feature/` or `hotfix/` branch prefixes** — they are rejected; use `dev/` or `patch/`.
- **Never write Python or shell scripts** — the codebase is PHP-only; no `.py`, `.sh`, `.ps1` files.
- **Never hardcode `04.00.04`** (or any specific version) in document body text — use the version badge and FILE INFORMATION header only.
- **Never commit `.env`, secret keys, API tokens, or credentials** — the `templates/configs/gitignore` template covers common patterns but double-check before pushing.
- **Never modify files under `vendor/`** — managed by Composer.
- **Never skip the FILE INFORMATION block** on a new source file — it is required by policy and checked in CI.
- **Never catch `\Throwable` silently in PHP** without re-throwing or logging.
- **Never prefix a branch with `mokostandards`** — that namespace is reserved for automated workflows.
- **Never mix tabs and spaces within a file** — follow `.editorconfig` exactly.

# Key Policy Documents

| Document | Purpose |
|----------|---------|
| `docs/policy/file-header-standards.md` | Full copyright-header rules for every file type |
| `docs/enforcement-levels.md` | Six-tier enforcement system reference |
| `docs/policy/coding-style-guide.md` | Universal naming and formatting conventions |
| `docs/policy/scripting-standards.md` | PHP-only scripting requirements in detail |
| `docs/policy/branching-strategy.md` | Branch naming, hierarchy, and release workflow |
| `docs/policy/merge-strategy.md` | Squash-merge policy and PR title/body conventions |
| `docs/policy/changelog-standards.md` | How and when to update CHANGELOG.md |
| `docs/guide/php-only-architecture.md` | PHP-only rationale and enterprise library overview |
| `CONTRIBUTING.md` | Complete contributor setup and standards reference |
