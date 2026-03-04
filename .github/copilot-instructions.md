# MokoStandards — GitHub Copilot Custom Instructions

## What This Repo Is

MokoStandards is the **authoritative standards and automation repository** for all Moko Consulting repositories (https://github.com/mokoconsulting-tech/MokoStandards). It is not a project template, not a runnable application, and not a library. It is the single source of truth for policies, PHP enterprise libraries, GitHub Actions workflows, and Terraform configuration templates that governed repositories pull via bulk sync.

---

## Primary Language

**PHP 8.1+ is the only language for new automation scripts and library code in `api/`.** Do not suggest Python scripts inside `api/`. Python tooling config (`pyproject.toml`) exists but the runtime is PHP-only. YAML uses 2-space indentation (spaces, not tabs). All other files use tabs.

---

## File Header — Always Required on New Files

Every new file needs a copyright header as its first content. Use the minimal form unless the file is a policy doc, README, or public API.

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
 * PATH: /api/validate/my_script.php
 * VERSION: XX.YY.ZZ
 * BRIEF: One-line description of purpose
 */

declare(strict_types=1);
```

**Markdown:**
```markdown
<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/my-doc.md
VERSION: XX.YY.ZZ
BRIEF: One-line description
-->
```

**YAML / Shell:** Use `#` comments with the same fields. JSON files are exempt.

---

## PHP Script Structure

All scripts in `api/` extend `CliFramework` from `api/lib/Enterprise/CliFramework.php`. Use `configure()` to declare arguments and `run()` to execute.

```php
#!/usr/bin/env php
<?php
/* … header … */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\{AuditLogger, CliFramework, MetricsCollector, PluginFactory};

class MyScript extends CliFramework
{
    private AuditLogger $logger;

    protected function configure(): void
    {
        $this->setDescription('What this script does');
        $this->addArgument('--path', 'Repository path', '.');
        $this->addArgument('--dry-run', 'Preview without changes', false);
    }

    protected function initialize(): void
    {
        parent::initialize();
        $this->logger = new AuditLogger('my_script');
    }

    protected function run(): int
    {
        $path = $this->getArgument('--path');
        $this->log("Processing: {$path}");
        return 0;
    }
}

$script = new MyScript();
exit($script->run());
```

PHPDoc is required on all public methods. `declare(strict_types=1)` is required in every PHP file. Never use `var_dump`, `print_r`, `eval`, or `create_function`.

---

## Naming Conventions

| Context | Convention | Example |
|---------|-----------|---------|
| PHP class | `PascalCase` | `RepositorySynchronizer` |
| PHP method / function | `camelCase` | `getUserData()` |
| PHP variable | `$snake_case` | `$repo_path` |
| PHP constant | `UPPER_SNAKE_CASE` | `DEFAULT_THRESHOLD` |
| PHP class file | `PascalCase.php` | `ApiClient.php` |
| PHP script file | `snake_case.php` | `check_repo_health.php` |
| YAML workflow | `kebab-case.yml` | `bulk-repo-sync.yml` |
| Markdown doc | `kebab-case.md` | `php-only-architecture.md` |

---

## Commit Messages

Format: `<type>(<scope>): <subject>` — imperative, lower-case subject, no trailing period.

Valid types: `feat` · `fix` · `docs` · `chore` · `ci` · `refactor` · `style` · `test` · `perf` · `revert` · `build`

Examples:
- `feat(validate): add version drift detection to scan_drift.php`
- `fix(api): correct circuit breaker reset in RepositorySynchronizer`
- `docs(policy): update file-header-standards for YAML files`
- `chore(deps): bump phpstan to level 6`

---

## Branch Naming

Format: `<prefix>/<MAJOR.MINOR.PATCH>[/description]`

Approved prefixes: `dev/` · `rc/` · `version/` · `patch/` · `copilot/` · `dependabot/`

- ✅ `dev/4.0.4/add-validator`
- ✅ `patch/4.0.4/fix-header`
- ❌ `feature/my-thing` — rejected by branch protection

---

## Validation Commands

```bash
find api -name "*.php" -exec php -l {} \;          # syntax check
./vendor/bin/phpcs --standard=phpcs.xml api/        # PSR-12 style
./vendor/bin/phpstan analyse -c phpstan.neon api/   # static analysis
./vendor/bin/psalm --config=psalm.xml               # type checking
./vendor/bin/phpunit api/tests/                     # tests
```

---

## Key Constraints

- Never commit directly to `main` — all changes go via PR, squash-merged
- Never add Python to `api/` — PHP only
- Never hardcode a specific version like `04.00.03` in document body text — use the version badge and FILE INFORMATION header
- Never skip the FILE INFORMATION block on a new file
- Never use bare `catch (\Throwable $e) {}` without logging or re-throwing
- Policy documents live in `docs/policy/` — never mix policy and guide content
- Templates synced to other repos live in `templates/` — never modify them inline without understanding sync impact

---

## Where Things Live

| What | Where |
|------|-------|
| Executable PHP scripts | `api/validate/`, `api/automation/`, `api/maintenance/` |
| PHP enterprise library classes | `api/lib/Enterprise/` |
| GitHub Actions workflows for THIS repo | `.github/workflows/` |
| Workflow templates synced to other repos | `templates/workflows/` |
| Policy documents | `docs/policy/` |
| How-to guides | `docs/guide/` |
| Repository structure definitions (.tf HCL) | `api/definitions/` |
| Linter/config templates | `templates/configs/` |
