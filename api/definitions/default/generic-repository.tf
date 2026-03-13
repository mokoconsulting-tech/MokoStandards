/**
 * Generic Repository Structure Definition
 * Standard repository structure for generic projects and libraries
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0
 * Schema Version: 1.0
 */

locals {
  repository_structure = {
    metadata = {
      name             = "Generic Repository"
      description      = "Standard repository structure for generic projects and libraries"
      repository_type  = "library"
      platform         = "multi-platform"
      last_updated     = "2026-01-15T00:00:00Z"
      maintainer       = "Moko Consulting"
      version          = "1.0"
      schema_version   = "1.0"
    }

    root_files = [
      {
        name              = "README.md"
        extension         = "md"
        description       = "Project overview and documentation"
        required          = true
        audience          = "general"
      },
      {
        name              = "LICENSE"
        extension         = ""
        description       = "License file (GPL-3.0-or-later)"
        required          = true
        audience          = "general"
      },
      {
        name              = "CHANGELOG.md"
        extension         = "md"
        description       = "Version history and changes"
        required          = true
        audience          = "general"
      },
      {
        name              = "SECURITY.md"
        extension         = "md"
        description       = "Security policy and vulnerability reporting"
        required          = true
        audience          = "general"
      },
      {
        name              = "CODE_OF_CONDUCT.md"
        extension         = "md"
        description       = "Community code of conduct"
        required          = true
        audience          = "contributor"
      },
      {
        name              = "ROADMAP.md"
        extension         = "md"
        description       = "Project roadmap with version goals and milestones"
        required          = false
        audience          = "general"
      },
      {
        name              = "CONTRIBUTING.md"
        extension         = "md"
        description       = "Contribution guidelines"
        required          = true
        audience          = "contributor"
      },
      {
        name              = ".gitignore"
        extension         = "gitignore"
        description       = "Git ignore patterns - preserved during sync operations"
        required          = true
        always_overwrite  = false
        audience          = "developer"
        template          = "templates/configs/.gitignore.generic"
      },
      {
        name              = ".gitattributes"
        extension         = "gitattributes"
        description       = "Git attributes configuration"
        required          = true
        audience          = "developer"
      },
      {
        name              = ".editorconfig"
        extension         = "editorconfig"
        description       = "Editor configuration for consistent coding style - preserved during sync"
        required          = true
        always_overwrite  = false
        audience          = "developer"
      },
      {
        name                = "Makefile"
        description         = "Build automation"
        requirement_status  = "suggested"
        audience            = "developer"
      },
      {
        name              = ".moko-standards"
        extension         = "yml"
        description       = "MokoStandards governance attachment — links this repo back to the standards source"
        required          = true
        always_overwrite  = true
        audience          = "developer"
        template          = "templates/configs/moko-standards.yml.template"
      },
      {
        name              = "GOVERNANCE.md"
        extension         = "md"
        description       = "Project governance rules, roles, and decision process — auto-maintained by MokoStandards"
        required          = true
        always_overwrite  = true
        audience          = "all"
        template          = "templates/docs/required/GOVERNANCE.md"
      }
    ]

    directories = [
      {
        name                = "src"
        path                = "src"
        description         = "Source code"
        requirement_status  = "suggested"
        purpose             = "Contains application/library source code"
      },
      {
        name                = "docs"
        path                = "docs"
        description         = "Documentation"
        required            = true
        purpose             = "Contains comprehensive documentation"
        files = [
          {
            name                = "index.md"
            extension           = "md"
            description         = "Documentation index"
            requirement_status  = "suggested"
          }
        ]
      },
      {
        name                = "scripts"
        path                = "scripts"
        description         = "Build and automation scripts"
        required            = true
        purpose             = "Contains scripts for building, testing, and deploying"
        files = [
          {
            name                = "index.md"
            extension           = "md"
            description         = "Scripts documentation"
            requirement_status  = "suggested"
          },
          {
            name                = "MokoStandards.override.xml"
            extension           = "xml"
            description         = "MokoStandards sync override configuration - preserved during sync"
            requirement_status  = "optional"
            always_overwrite    = false
            audience            = "developer"
          }
        ]
      },
      {
        name                = "tests"
        path                = "tests"
        description         = "Test files"
        requirement_status  = "suggested"
        purpose             = "Contains unit tests, integration tests, and test fixtures"
      },
      {
        name                = ".github"
        path                = ".github"
        description         = "GitHub-specific configuration"
        requirement_status  = "suggested"
        purpose             = "Contains GitHub Actions workflows and configuration"
        files = [
          {
            name                = "copilot.yml"
            extension           = "yml"
            description         = "GitHub Copilot allowed domains configuration"
            requirement_status  = "required"
            always_overwrite    = true
            template            = ".github/copilot.yml"
          },
          {
            name                = "copilot-instructions.md"
            extension           = "md"
            description         = "GitHub Copilot custom instructions enforcing MokoStandards"
            requirement_status  = "required"
            always_overwrite    = false
            destination_path    = ".github"
            destination_filename = "copilot-instructions.md"
            template            = "templates/github/copilot-instructions.md.template"
				stub_content        = <<-MOKO_END
				> [!IMPORTANT]
				> **🔧 AI Self-Update Required on First Use**
				>
				> This file may contain unfilled `{{TOKEN}}` placeholders. The MokoStandards bulk-sync system
				> replaces them automatically at sync time; if you can still see them, sync has not yet run for
				> this repository — or this is a brand-new repo.
				>
				> **On your very first interaction in this repository, before answering any other question:**
				>
				> 1. Check whether any `{{TOKEN}}` placeholders remain in this file.
				> 2. If they do, locate the values as described in the table below and replace every occurrence
				>    in **both** `.github/copilot-instructions.md` and `.github/CLAUDE.md`.
				> 3. After replacing all tokens, **delete this entire notice block** (from `> [!IMPORTANT]`
				>    through the closing `> ---` line) in both files.
				> 4. Tell the developer: *"I've self-updated the AI context files with this repository's
				>    values — all set."*
				>
				> | Placeholder | Where to find the value |
				> |---|---|
				> | `{{REPO_NAME}}` | The GitHub repository name (visible in the URL, `README.md` heading, or `git remote -v`) |
				> | `{{REPO_URL}}` | Full GitHub URL, e.g. `https://github.com/mokoconsulting-tech/<repo-name>` |
				> | `{{PRIMARY_LANGUAGE}}` | The dominant programming language (check file extensions in the repository) |
				> | `{{PLATFORM_TYPE}}` | The project type: `PHP library`, `Joomla extension`, `Dolibarr module`, `WaaS site`, etc. — infer from repo structure |
				>
				> ---
				
				# {{REPO_NAME}} — GitHub Copilot Custom Instructions
				
				## What This Repo Is
				
				This is a **Moko Consulting** repository governed by [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards). All coding standards, workflows, and policies are defined there and enforced here via bulk sync.
				
				Repository URL: {{REPO_URL}}
				Primary language: **{{PRIMARY_LANGUAGE}}**
				Platform type: **{{PLATFORM_TYPE}}**
				
				---
				
				## Primary Language
				
				**{{PRIMARY_LANGUAGE}} is the primary language for this repository.** Follow the conventions documented in [MokoStandards coding-style-guide](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/coding-style-guide.md).
				
				YAML uses 2-space indentation (spaces, not tabs). All other text files use tabs per `.editorconfig`.
				
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
				 * DEFGROUP: {{REPO_NAME}}.Module
				 * INGROUP: {{REPO_NAME}}
				 * REPO: {{REPO_URL}}
				 * PATH: /path/to/file.php
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
				DEFGROUP: {{REPO_NAME}}.Documentation
				INGROUP: {{REPO_NAME}}
				REPO: {{REPO_URL}}
				PATH: /docs/file.md
				VERSION: XX.YY.ZZ
				BRIEF: One-line description
				-->
				```
				
				**YAML / Shell:** Use `#` comments with the same fields. JSON files are exempt.
				
				---
				
				## Version Management
				
				**`README.md` is the single source of truth for the repository version.**
				
				- **Bump the patch version on every PR** — increment `XX.YY.ZZ` (e.g. `01.02.03` → `01.02.04`) in `README.md` before opening the PR; the `sync-version-on-merge` workflow propagates it automatically to all badges and `FILE INFORMATION` headers on merge to `main`.
				- The `VERSION: XX.YY.ZZ` field in the README.md `FILE INFORMATION` block governs all other version references.
				- Update the version in `README.md` only — the `sync-version-on-merge` workflow propagates it automatically to all badges and `FILE INFORMATION` headers on merge to `main`.
				- Version format is zero-padded semver: `XX.YY.ZZ` (e.g. `04.00.04`).
				- Never hardcode a specific version in document body text — use the badge or FILE INFORMATION header only.
				
				---
				
				## GitHub Actions — Token Usage
				
				Every workflow must use **`secrets.GH_TOKEN`** (the org-level Personal Access Token). This applies to all `actions/checkout`, `gh` CLI calls, and any step that talks to the GitHub API.
				
				```yaml
				# ✅ Correct
				- uses: actions/checkout@v4
				  with:
				    token: ${{ secrets.GH_TOKEN }}
				
				env:
				  GH_TOKEN: ${{ secrets.GH_TOKEN }}
				```
				
				```yaml
				# ❌ Wrong — never use these in workflows
				token: ${{ github.token }}
				token: ${{ secrets.GITHUB_TOKEN }}
				```
				
				PHP scripts read the token with: `getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN')` — `GH_TOKEN` is always preferred; `GITHUB_TOKEN` is accepted only as a local-dev fallback.
				
				---
				
				## Composer Package (PHP repositories)
				
				This repository requires the MokoStandards enterprise library. The `composer.json` must include:
				
				```json
				{
				  "repositories": [
				    {
				      "type": "vcs",
				      "url": "https://github.com/mokoconsulting-tech/MokoStandards"
				    }
				  ],
				  "require": {
				    "mokoconsulting/mokostandards": "^4.0"
				  }
				}
				```
				
				Run `composer install` after adding the dependency. See [package-installation.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/guide/package-installation.md) for full instructions.
				
				---
				
				## PHP Script Pattern
				
				All PHP scripts **must** extend `MokoStandards\Enterprise\CliFramework`. Never write standalone classes or extend the legacy `CliBase`.
				
				```php
				#!/usr/bin/env php
				<?php
				/* … file header … */
				
				declare(strict_types=1);
				
				require_once __DIR__ . '/vendor/autoload.php';
				
				use MokoStandards\Enterprise\CliFramework;
				
				class MyScript extends CliFramework
				{
				    protected function configure(): void
				    {
				        $this->setDescription('One-line description');
				        $this->addArgument('--path',    'Repository root',          '.');
				        $this->addArgument('--dry-run', 'Preview without writing',  false);
				    }
				
				    protected function run(): int
				    {
				        $path   = $this->getArgument('--path');
				        $dryRun = (bool) $this->getArgument('--dry-run');
				
				        $this->log('INFO', "Processing: {$path}");
				        return 0;
				    }
				}
				
				$script = new MyScript('my_script', 'One-line description');
				exit($script->execute());
				```
				
				**Key rules:**
				- Abstract methods to implement: `configure()` and `run()` — **not** `execute()`
				- `execute()` is the **public entry point** that orchestrates setup (arg parsing, `initialize()`) and then calls your `run()` implementation; call it at the bottom with `exit($script->execute())`
				- Entry point at the bottom: `$script->execute()` — **not** `$script->run()`
				- Constructor always takes `(string $name, string $description = '')`; pass the description here — `setDescription()` inside `configure()` is only needed to override it
				- `log(string $level, string $message)` — level is the **first** argument (INFO / SUCCESS / WARNING / ERROR)
				- `$this->dryRun` and `$this->verbose` are set automatically from `--dry-run` / `--verbose`
				
				---
				
				## Naming Conventions
				
				| Context | Convention | Example |
				|---------|-----------|---------|
				| PHP class | `PascalCase` | `MyService` |
				| PHP method / function | `camelCase` | `getUserData()` |
				| PHP variable | `$snake_case` | `$repo_path` |
				| PHP constant | `UPPER_SNAKE_CASE` | `DEFAULT_THRESHOLD` |
				| PHP class file | `PascalCase.php` | `ApiClient.php` |
				| PHP script file | `snake_case.php` | `check_health.php` |
				| YAML workflow | `kebab-case.yml` | `bulk-repo-sync.yml` |
				| Markdown doc | `kebab-case.md` | `coding-style-guide.md` |
				
				---
				
				## Commit Messages
				
				Format: `<type>(<scope>): <subject>` — imperative, lower-case subject, no trailing period.
				
				Valid types: `feat` · `fix` · `docs` · `chore` · `ci` · `refactor` · `style` · `test` · `perf` · `revert` · `build`
				
				Examples:
				- `feat(module): add user preference caching`
				- `fix(api): handle null response from external service`
				- `docs(readme): update installation instructions`
				- `chore(deps): bump phpunit to 11.x`
				
				---
				
				## Branch Naming
				
				Format: `<prefix>/<MAJOR.MINOR.PATCH>[/description]`
				
				Approved prefixes: `dev/` · `rc/` · `version/` · `patch/` · `copilot/` · `dependabot/`
				
				- ✅ `dev/1.2.0/add-feature`
				- ✅ `patch/1.2.1/fix-bug`
				- ❌ `feature/my-thing` — rejected by branch protection
				
				---
				
				## Keeping Documentation Current
				
				Whenever you make code changes, update the corresponding documentation in the same commit or PR. Do not leave docs stale.
				
				| Change type | Documentation to update |
				|-------------|------------------------|
				| New or renamed public PHP method | PHPDoc block on the method; `docs/api/` index for that class |
				| New or changed CLI script argument | Script's own `--help` text; `docs/api/` or equivalent |
				| New or changed GitHub Actions workflow | `docs/workflows/<workflow-name>.md` |
				| New or changed policy | Corresponding file under `docs/policy/` |
				| New library class or major feature | `CHANGELOG.md` entry under `Added` |
				| Bug fix | `CHANGELOG.md` entry under `Fixed` |
				| Breaking change | `CHANGELOG.md` entry under `Changed`; update `CONTRIBUTING.md` if contributor steps change |
				| Any modified file | Update the `VERSION` field in that file's `FILE INFORMATION` block |
				| **Every PR** | **Bump the patch version** — increment `XX.YY.ZZ` in `README.md`; `sync-version-on-merge` propagates it to all headers and badges on merge |
				
				If your code change makes any existing doc sentence false or incomplete, fix the doc before closing the PR.
				
				---
				
				## Key Constraints
				
				- Never commit directly to `main` — all changes go via PR, squash-merged
				- Never skip the FILE INFORMATION block on a new file
				- Never use bare `catch (\Throwable $e) {}` without logging or re-throwing
				- Never hardcode version numbers in body text — update `README.md` and let automation propagate
				- Never use `github.token` or `secrets.GITHUB_TOKEN` in workflows — always use `secrets.GH_TOKEN`
				- Never extend `CliBase` in PHP scripts — extend `MokoStandards\Enterprise\CliFramework`
				- Never call `$script->run()` as the entry point — call `$script->execute()`
				- Policy documents and guides must not be mixed
				
				---
				
				## MokoStandards Reference
				
				This repository is governed by [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards). Authoritative policies:
				
				| Document | Purpose |
				|----------|---------|
				| [file-header-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/file-header-standards.md) | Copyright-header rules for every file type |
				| [coding-style-guide.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/coding-style-guide.md) | Naming and formatting conventions |
				| [branching-strategy.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/branching-strategy.md) | Branch naming, hierarchy, and release workflow |
				| [merge-strategy.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/merge-strategy.md) | Squash-merge policy and PR title/body conventions |
				| [changelog-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/changelog-standards.md) | How and when to update CHANGELOG.md |
				| [scripting-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/scripting-standards.md) | PHP script requirements and CliFramework usage |
				| [package-installation.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/guide/package-installation.md) | Installing `mokoconsulting/mokostandards` via Composer |
				MOKO_END
          },
          {
            name                = "CLAUDE.md"
            extension           = "md"
            description         = "Claude AI assistant context enforcing MokoStandards"
            requirement_status  = "required"
            always_overwrite    = false
            destination_path    = ".github"
            destination_filename = "CLAUDE.md"
            template            = "templates/github/CLAUDE.md.template"
				stub_content        = <<-MOKO_END
				> [!IMPORTANT]
				> **🔧 AI Self-Update Required on First Use**
				>
				> This file may contain unfilled `{{TOKEN}}` placeholders. The MokoStandards bulk-sync system
				> replaces them automatically at sync time; if you can still see them, sync has not yet run for
				> this repository — or this is a brand-new repo.
				>
				> **On your very first interaction in this repository, before answering any other question:**
				>
				> 1. Check whether any `{{TOKEN}}` placeholders remain in this file.
				> 2. If they do, locate the values as described in the table below and replace every occurrence
				>    in **both** `.github/copilot-instructions.md` and `.github/CLAUDE.md`.
				> 3. After replacing all tokens, **delete this entire notice block** (from `> [!IMPORTANT]`
				>    through the closing `> ---` line) in both files.
				> 4. Tell the developer: *"I've self-updated the AI context files with this repository's
				>    values — all set."*
				>
				> | Placeholder | Where to find the value |
				> |---|---|
				> | `{{REPO_NAME}}` | The GitHub repository name (visible in the URL, `README.md` heading, or `git remote -v`) |
				> | `{{REPO_URL}}` | Full GitHub URL, e.g. `https://github.com/mokoconsulting-tech/<repo-name>` |
				> | `{{REPO_DESCRIPTION}}` | First paragraph of `README.md` body, or the GitHub repo description |
				> | `{{PRIMARY_LANGUAGE}}` | The dominant programming language (check file extensions in the repository) |
				> | `{{PLATFORM_TYPE}}` | The project type: `PHP library`, `Joomla extension`, `Dolibarr module`, `WaaS site`, etc. — infer from repo structure |
				>
				> ---
				
				# What This Repo Is
				
				**{{REPO_NAME}}** is a Moko Consulting **{{PLATFORM_TYPE}}** repository.
				
				{{REPO_DESCRIPTION}}
				
				Repository URL: {{REPO_URL}}
				
				This repository is governed by [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) — the single source of truth for coding standards, file-header policies, GitHub Actions workflows, and Terraform configuration templates across all Moko Consulting repositories.
				
				---
				
				# Repo Structure
				
				```
				{{REPO_NAME}}/
				├── src/                  # Primary source code
				├── docs/                 # Documentation
				├── tests/                # Test suite
				├── .github/
				│   ├── workflows/        # CI/CD workflows (synced from MokoStandards)
				│   ├── ISSUE_TEMPLATE/   # Issue templates (inherited from mokoconsulting-tech/.github-private)
				│   ├── copilot-instructions.md  # GitHub Copilot custom instructions
				│   ├── CLAUDE.md             # This file — Claude AI assistant context
				│   └── override.tf       # Repository-specific health-check overrides
				├── README.md             # Project overview — version source of truth
				├── CHANGELOG.md          # Version history
				├── CONTRIBUTING.md       # Contribution guidelines
				└── LICENSE               # GPL-3.0-or-later
				```
				
				---
				
				# Primary Language
				
				**{{PRIMARY_LANGUAGE}}** is the primary language for this repository.
				
				YAML uses 2-space indentation (spaces, not tabs). All other text files use tabs per `.editorconfig`.
				
				---
				
				# Composer Package (PHP repositories)
				
				This repository requires the MokoStandards enterprise library. The package is installed from the private GitHub VCS source.
				
				`composer.json` must contain:
				
				```json
				{
				  "repositories": [
				    {
				      "type": "vcs",
				      "url": "https://github.com/mokoconsulting-tech/MokoStandards"
				    }
				  ],
				  "require": {
				    "mokoconsulting/mokostandards": "^4.0"
				  }
				}
				```
				
				Install or update with:
				
				```bash
				composer install          # first time
				composer update mokoconsulting/mokostandards   # upgrade
				```
				
				---
				
				# PHP Script Pattern
				
				All PHP scripts must extend `MokoStandards\Enterprise\CliFramework` — **never** use a standalone class or the legacy `CliBase`.
				
				```php
				#!/usr/bin/env php
				<?php
				/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
				 *
				 * This file is part of a Moko Consulting project.
				 *
				 * SPDX-License-Identifier: GPL-3.0-or-later
				 *
				 * FILE INFORMATION
				 * DEFGROUP: {{REPO_NAME}}.Scripts
				 * INGROUP: {{REPO_NAME}}
				 * REPO: {{REPO_URL}}
				 * PATH: /api/my_script.php
				 * VERSION: XX.YY.ZZ
				 * BRIEF: One-line description of what this script does
				 */
				
				declare(strict_types=1);
				
				require_once __DIR__ . '/vendor/autoload.php';
				
				use MokoStandards\Enterprise\CliFramework;
				
				class MyScript extends CliFramework
				{
				    protected function configure(): void
				    {
				        $this->setDescription('One-line description of what this script does');
				        $this->addArgument('--path',    'Repository root path',             '.');
				        $this->addArgument('--dry-run', 'Preview changes without writing',  false);
				    }
				
				    protected function run(): int
				    {
				        $path   = $this->getArgument('--path');
				        $dryRun = (bool) $this->getArgument('--dry-run');
				
				        // implementation …
				        $this->log('INFO', "Processing: {$path}");
				
				        return 0;
				    }
				}
				
				$script = new MyScript('my_script', 'One-line description of what this script does');
				exit($script->execute());
				```
				
				**CliFramework interface summary:**
				
				| Member | Purpose |
				|--------|---------|
				| `configure(): void` | Abstract — register arguments with `addArgument()` |
				| `run(): int` | Abstract — main script logic; return the exit code |
				| `initialize(): void` | Optional hook — runs after arg-parse, before `run()` |
				| `execute(array $argv = []): int` | **Public entry point** — call this at the bottom; it calls `configure()`, parses argv, then calls `run()` |
				| `addArgument(string $name, string $desc, mixed $default)` | Register a CLI argument |
				| `getArgument(string $name): mixed` | Read a parsed or default argument value |
				| `log(string $level, string $message)` | Structured log — levels: INFO SUCCESS WARNING ERROR DEBUG |
				| `error(string $message, int $code = 1): never` | Log error and exit |
				| `$this->dryRun` | `true` when `--dry-run` is passed |
				| `$this->verbose` | `true` when `--verbose` / `-v` is passed |
				
				**Forbidden patterns in PHP:**
				
				```php
				// ❌ Wrong — legacy base class, not namespaced
				class MyScript extends CliBase { … }
				
				// ❌ Wrong — standalone class with no framework
				class MyScript { public function run() { … } }
				
				// ❌ Wrong — method names and entry-point transposed
				protected function execute(): int { … }   // should be run()
				exit($script->run());                      // should be execute()
				
				// ✅ Correct
				class MyScript extends CliFramework {
				    protected function configure(): void { … }
				    protected function run(): int { … }
				}
				$script = new MyScript('name', 'description');
				exit($script->execute());
				```
				
				---
				
				# Version Management
				
				**`README.md` is the single source of truth for the repository version.**
				
				- **Bump the patch version on every PR** — increment `XX.YY.ZZ` (e.g. `01.02.03` → `01.02.04`) in `README.md` before opening the PR; the `sync-version-on-merge` workflow propagates it to all badges and `FILE INFORMATION` headers automatically on merge to `main`.
				- The `VERSION: XX.YY.ZZ` field in the `README.md` `FILE INFORMATION` block governs all other version references.
				- Update `README.md` only — the `sync-version-on-merge` workflow propagates it to all badges and `FILE INFORMATION` headers automatically on merge to `main`.
				- Version format is zero-padded semver: `XX.YY.ZZ` (e.g. `01.02.03`).
				- Never hardcode a version number in body text — use the badge or FILE INFORMATION header only.
				
				---
				
				# File Header Requirements
				
				Every new file **must** have a copyright header as its first content. JSON files, binary files, generated files, and third-party files are exempt.
				
				## Minimal header
				
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
				 * DEFGROUP: {{REPO_NAME}}.Module
				 * INGROUP: {{REPO_NAME}}
				 * REPO: {{REPO_URL}}
				 * PATH: /src/MyClass.php
				 * VERSION: XX.YY.ZZ
				 * BRIEF: One-line description of file purpose
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
				DEFGROUP: {{REPO_NAME}}.Documentation
				INGROUP: {{REPO_NAME}}
				REPO: {{REPO_URL}}
				PATH: /docs/guide/example.md
				VERSION: XX.YY.ZZ
				BRIEF: One-line description of file purpose
				-->
				```
				
				**YAML / Shell:** Use `#` comments with the same fields. JSON files are exempt.
				
				---
				
				# Coding Standards
				
				## Naming Conventions
				
				| Context | Convention | Example |
				|---------|-----------|---------|
				| PHP class | `PascalCase` | `MyService` |
				| PHP method / function | `camelCase` | `getUserData()` |
				| PHP variable | `$snake_case` | `$user_id` |
				| PHP constant | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
				| PHP class file | `PascalCase.php` | `UserService.php` |
				| PHP script file | `snake_case.php` | `check_health.php` |
				| YAML workflow | `kebab-case.yml` | `code-quality.yml` |
				| Markdown doc | `kebab-case.md` | `coding-style-guide.md` |
				
				## Commit Messages
				
				Format: `<type>(<scope>): <subject>` — imperative, lower-case subject, no trailing period.
				
				Valid types: `feat` · `fix` · `docs` · `chore` · `ci` · `refactor` · `style` · `test` · `perf` · `revert` · `build`
				
				## Branch Naming
				
				Format: `<prefix>/<MAJOR.MINOR.PATCH>[/description]`
				
				Approved prefixes: `dev/` · `rc/` · `version/` · `patch/` · `copilot/` · `dependabot/`
				
				---
				
				# GitHub Actions — Token Usage
				
				Every workflow in this repository must use **`secrets.GH_TOKEN`** (the org-level Personal Access Token).
				
				```yaml
				# ✅ Correct — always use GH_TOKEN
				- uses: actions/checkout@v4
				  with:
				    token: ${{ secrets.GH_TOKEN }}
				
				env:
				  GH_TOKEN: ${{ secrets.GH_TOKEN }}
				```
				
				```yaml
				# ❌ Wrong — never use these
				token: ${{ github.token }}
				token: ${{ secrets.GITHUB_TOKEN }}
				```
				
				PHP scripts read the token with: `getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN')` — `GH_TOKEN` is always preferred; `GITHUB_TOKEN` is a local-dev fallback only.
				
				---
				
				# Keeping Documentation Current
				
				Whenever you make code changes, update the corresponding documentation in the same commit or PR. Do not leave docs stale.
				
				| Change type | Documentation to update |
				|-------------|------------------------|
				| New or renamed public PHP method | PHPDoc block on the method; `docs/api/` index for that class |
				| New or changed CLI script argument | Script's own `--help` text; `docs/api/` or equivalent |
				| New or changed GitHub Actions workflow | `docs/workflows/<workflow-name>.md` |
				| New or changed policy | Corresponding file under `docs/policy/` |
				| New library class or major feature | `CHANGELOG.md` entry under `Added` |
				| Bug fix | `CHANGELOG.md` entry under `Fixed` |
				| Breaking change | `CHANGELOG.md` entry under `Changed`; update `CONTRIBUTING.md` if contributor steps change |
				| Any modified file | Update the `VERSION` field in that file's `FILE INFORMATION` block |
				| **Every PR** | **Bump the patch version** — increment `XX.YY.ZZ` in `README.md`; `sync-version-on-merge` propagates it to all headers and badges on merge |
				
				If your code change makes any existing doc sentence false or incomplete, fix the doc before closing the PR.
				
				---
				
				# What NOT to Do
				
				- **Never commit directly to `main`** — all changes go through a PR.
				- **Never hardcode version numbers** in body text — update `README.md` and let automation propagate.
				- **Never skip the FILE INFORMATION block** on a new source file.
				- **Never use bare `catch (\Throwable $e) {}`** — always log or re-throw.
				- **Never mix tabs and spaces** within a file — follow `.editorconfig`.
				- **Never use `github.token` or `secrets.GITHUB_TOKEN` in workflows** — always use `secrets.GH_TOKEN`.
				- **Never extend `CliBase` in PHP scripts** — extend `MokoStandards\Enterprise\CliFramework` instead.
				- **Never use `exit($script->run())`** — the correct entry point is `exit($script->execute())`.
				
				---
				
				# Key Policy Documents (MokoStandards)
				
				| Document | Purpose |
				|----------|---------|
				| [file-header-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/file-header-standards.md) | Copyright-header rules for every file type |
				| [coding-style-guide.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/coding-style-guide.md) | Naming and formatting conventions |
				| [branching-strategy.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/branching-strategy.md) | Branch naming, hierarchy, and release workflow |
				| [merge-strategy.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/merge-strategy.md) | Squash-merge policy and PR conventions |
				| [changelog-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/changelog-standards.md) | How and when to update CHANGELOG.md |
				| [scripting-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/scripting-standards.md) | PHP script requirements and CliFramework usage |
				| [package-installation.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/guide/package-installation.md) | Installing `mokoconsulting/mokostandards` via Composer |
				MOKO_END
          }
        ]
        subdirectories = [
          {
            name                = "workflows"
            path                = ".github/workflows"
            description         = "GitHub Actions workflows"
            requirement_status  = "suggested"
            files = [
              {
                name                = "standards-compliance.yml"
                extension           = "yml"
                description         = "MokoStandards compliance validation"
                requirement_status  = "required"
                always_overwrite    = true
                template            = ".github/workflows/standards-compliance.yml"
              },
              {
                name                = "enterprise-firewall-setup.yml"
                extension           = "yml"
                description         = "Enterprise firewall configuration for trusted domain access"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/workflows/shared/enterprise-firewall-setup.yml.template"
              },
              {
                name                = "deploy-dev.yml"
                extension           = "yml"
                description         = "SFTP deployment of src/ to the development server"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/workflows/shared/deploy-dev.yml.template"
              }
            ]
          }
        ]
      }
    ]

    repository_requirements = {
      secrets = [
        {
          name        = "GH_TOKEN"
          description = "Org-level GitHub PAT for automation"
          required    = true
          scope       = "org"
        },
        {
          name        = "DEV_FTP_KEY"
          description = "SSH private key for SFTP dev deployment (preferred); if DEV_FTP_PASSWORD is also set it is used as the key passphrase, with password-only as fallback"
          required    = false
          scope       = "org"
        },
        {
          name        = "DEV_FTP_PASSWORD"
          description = "SFTP password for dev deployment; used as SSH key passphrase when DEV_FTP_KEY is also set, and as standalone fallback if key auth fails"
          required    = false
          scope       = "org"
          note        = "At least one of DEV_FTP_KEY or DEV_FTP_PASSWORD must be configured"
        }
      ]

      variables = [
        {
          name        = "DEV_FTP_HOST"
          description = "Dev server hostname; may include port suffix (e.g. dev.example.com or dev.example.com:2222)"
          required    = true
          scope       = "org"
        },
        {
          name        = "DEV_FTP_PATH"
          description = "Base remote path for SFTP deployment (e.g. /var/www/html)"
          required    = true
          scope       = "org"
        },
        {
          name        = "DEV_FTP_USERNAME"
          description = "SFTP username for dev server authentication"
          required    = true
          scope       = "org"
        },
        {
          name        = "DEV_FTP_PORT"
          description = "Explicit SFTP port override; if omitted the port is parsed from DEV_FTP_HOST or defaults to 22"
          required    = false
          scope       = "org"
        },
        {
          name        = "DEV_FTP_PATH_SUFFIX"
          description = "Per-repo path suffix appended to DEV_FTP_PATH (e.g. /my-project)"
          required    = false
          scope       = "repo"
        }
      ]
    }
  }
}
