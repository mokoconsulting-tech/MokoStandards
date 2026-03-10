/**
 * MokoCRM Module Structure Definition
 * Standard repository structure for MokoCRM (Dolibarr) modules
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0
 * Schema Version: 1.0
 */

locals {
  repository_structure = {
    metadata = {
      name             = "MokoCRM Module"
      description      = "Standard repository structure for MokoCRM (Dolibarr) modules"
      repository_type  = "crm-module"
      platform         = "dolibarr"
      last_updated     = "2026-01-07T00:00:00Z"
      maintainer       = "Moko Consulting"
      version          = "1.0"
      schema_version   = "1.0"
    }

    root_files = [
      {
        name              = "README.md"
        extension         = "md"
        description       = "Developer-focused documentation for contributors and maintainers"
        required          = true
        audience          = "developer"
        stub_content      = <<-EOT
# {MODULE_NAME}

## For Developers

This README is for developers contributing to this module.

### Development Setup

1. Clone this repository
2. Install dependencies: `make install-dev`
3. Run tests: `make test`

### Building

```bash
make build
```

### Testing

```bash
make test
make lint
```

### Contributing

See CONTRIBUTING.md for contribution guidelines.

## For End Users

End user documentation is available in `src/README.md` after installation.

## License

See LICENSE file for details.
EOT
      },
      {
        name              = "CONTRIBUTING.md"
        extension         = "md"
        description       = "Contribution guidelines"
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
        name              = "LICENSE"
        extension         = ""
        description       = "License file (GPL-3.0-or-later) - Default for Dolibarr/CRM modules"
        required          = true
        audience          = "general"
        template          = "templates/licenses/GPL-3.0"
        license_type      = "GPL-3.0-or-later"
      },
      {
        name              = "CHANGELOG.md"
        extension         = "md"
        description       = "Version history and changes"
        required          = true
        audience          = "general"
      },
      {
        name                = "Makefile"
        description         = "Build automation using MokoStandards templates"
        required            = true
        always_overwrite    = true
        audience            = "developer"
        source_path         = "templates/makefiles"
        source_filename     = "Makefile.dolibarr.template"
        source_type         = "template"
        destination_path    = "."
        destination_filename = "Makefile"
        create_path         = false
        template            = "templates/makefiles/Makefile.dolibarr.template"
      },
      {
        name              = ".editorconfig"
        extension         = "editorconfig"
        description       = "Editor configuration for consistent coding style"
        required          = true
        audience          = "developer"
      },
      {
        name              = ".gitignore"
        extension         = "gitignore"
        description       = "Git ignore patterns - preserved during sync operations"
        required          = true
        always_overwrite  = false
        audience          = "developer"
      },
      {
        name              = ".gitattributes"
        extension         = "gitattributes"
        description       = "Git attributes configuration"
        required          = true
        audience          = "developer"
      },
      {
        name              = ".moko-standards"
        extension         = "yml"
        description       = "MokoStandards governance attachment — links this repo back to the standards source"
        required          = true
        always_overwrite  = true
        audience          = "developer"
        template          = "templates/configs/moko-standards.yml.template"
      }
    ]

    directories = [
      {
        name                = "src"
        path                = "src"
        description         = "Module source code for deployment"
        required            = true
        purpose             = "Contains the actual module code that gets deployed to Dolibarr"
        files = [
          {
            name              = "README.md"
            extension         = "md"
            description       = "End-user documentation deployed with the module"
            required          = true
            audience          = "end-user"
            stub_content      = <<-EOT
# {MODULE_NAME}

## For End Users

This module provides {MODULE_DESCRIPTION}.

### Installation

1. Navigate to Home → Setup → Modules/Applications
2. Find "{MODULE_NAME}" in the list
3. Click "Activate"

### Configuration

After activation, configure the module:
1. Go to Home → Setup → Modules/Applications
2. Click on the module settings icon
3. Configure as needed

### Usage

{USAGE_INSTRUCTIONS}

### Support

For support, contact: {SUPPORT_EMAIL}

## Version

Current version: {VERSION}

See CHANGELOG.md for version history.
EOT
          },
          {
            name              = "core/modules/mod{ModuleName}.class.php"
            extension         = "php"
            description       = "Main module descriptor file"
            required          = true
            audience          = "developer"
          }
        ]
        subdirectories = [
          {
            name                = "core"
            path                = "src/core"
            description         = "Core module files"
            required            = true
          },
          {
            name                = "langs"
            path                = "src/langs"
            description         = "Language translation files"
            required            = true
          },
          {
            name                = "sql"
            path                = "src/sql"
            description         = "Database schema files"
            requirement_status  = "suggested"
          },
          {
            name                = "css"
            path                = "src/css"
            description         = "Stylesheets"
            requirement_status  = "suggested"
          },
          {
            name                = "js"
            path                = "src/js"
            description         = "JavaScript files"
            requirement_status  = "suggested"
          },
          {
            name                = "class"
            path                = "src/class"
            description         = "PHP class files"
            requirement_status  = "suggested"
          },
          {
            name                = "lib"
            path                = "src/lib"
            description         = "Library files"
            requirement_status  = "suggested"
          }
        ]
      },
      {
        name                = "docs"
        path                = "docs"
        description         = "Developer and technical documentation"
        required            = true
        purpose             = "Contains technical documentation, API docs, architecture diagrams"
        files = [
          {
            name              = "index.md"
            extension         = "md"
            description       = "Documentation index"
            required          = true
          }
        ]
      },
      {
        name                = "scripts"
        path                = "scripts"
        description         = "Build and maintenance scripts"
        required            = true
        purpose             = "Contains scripts for building, testing, and deploying"
        files = [
          {
            name                = "index.md"
            extension           = "md"
            description         = "Scripts documentation"
            requirement_status  = "required"
          },
          {
            name                = "build_package.sh"
            extension           = "sh"
            description         = "Package building script for Dolibarr module"
            requirement_status  = "suggested"
            template            = "templates/scripts/release/package_dolibarr.sh"
          },
          {
            name                = "validate_module.sh"
            extension           = "sh"
            description         = "Module validation script"
            requirement_status  = "suggested"
            template            = "templates/scripts/validate/dolibarr_module.sh"
          },
          {
            name                = "MokoStandards.override.xml"
            extension           = "xml"
            description         = "MokoStandards sync override configuration"
            requirement_status  = "optional"
            always_overwrite    = false
          }
        ]
      },
      {
        name                = "tests"
        path                = "tests"
        description         = "Test files"
        required            = true
        purpose             = "Contains unit tests, integration tests, and test fixtures"
        subdirectories = [
          {
            name                = "unit"
            path                = "tests/unit"
            description         = "Unit tests"
            required            = true
          },
          {
            name                = "integration"
            path                = "tests/integration"
            description         = "Integration tests"
            requirement_status  = "suggested"
          }
        ]
      },
      {
        name                = "templates"
        path                = "templates"
        description         = "Template files for code generation"
        requirement_status  = "suggested"
        purpose             = "Contains templates used by build scripts"
      },
      {
        name                = ".github"
        path                = ".github"
        description         = "GitHub-specific configuration"
        requirement_status  = "suggested"
        purpose             = "Contains GitHub Actions workflows, issue templates, etc."
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
            description         = "GitHub Copilot custom instructions enforcing MokoStandards — Dolibarr/CRM edition"
            requirement_status  = "required"
            always_overwrite    = false
            destination_path    = ".github"
            destination_filename = "copilot-instructions.md"
            template            = "templates/github/copilot-instructions.dolibarr.md.template"
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
				> | `{{MODULE_NAME}}` | The module name as used in Dolibarr (lowercase, e.g. `mymodule`) — from the `langs/en_US/*.lang` filename or `$this->rights_class` in the module descriptor |
				> | `{{MODULE_CLASS}}` | PascalCase module class name (e.g. `MyModule`) — from the `src/core/modules/mod*.class.php` filename |
				> | `{{MODULE_ID}}` | The `$this->numero` value in `src/core/modules/mod*.class.php`; check [module-registry.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/development/crm/module-registry.md) if creating a new module |
				> | `{{PRIMARY_LANGUAGE}}` | Primary programming language (usually `PHP`) |
				>
				> ---
				
				# {{REPO_NAME}} — GitHub Copilot Custom Instructions
				
				## What This Repo Is
				
				This is a **Moko Consulting MokoCRM** (Dolibarr) module repository governed by [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards). All coding standards, workflows, and policies are defined there and enforced here via bulk sync.
				
				Repository URL: {{REPO_URL}}
				Module name: **{{MODULE_NAME}}**
				Module class: **{{MODULE_CLASS}}**
				Module ID: **{{MODULE_ID}}**
				Platform: **Dolibarr / MokoCRM**
				
				---
				
				## Primary Language
				
				**PHP** (≥ 8.1) is the primary language for this Dolibarr module. YAML uses 2-space indentation. All other text files use tabs per `.editorconfig`.
				
				---
				
				## File Header — Always Required on New Files
				
				Every new file needs a copyright header as its first content.
				
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
				 * PATH: /src/path/to/file.php
				 * VERSION: XX.YY.ZZ
				 * BRIEF: One-line description of purpose
				 */
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
				- The `VERSION: XX.YY.ZZ` field in `README.md` governs all other version references.
				- Version format is zero-padded semver: `XX.YY.ZZ` (e.g. `01.02.03`).
				- Never hardcode a specific version in document body text — use the badge or FILE INFORMATION header only.
				
				### Dolibarr Module Version Alignment
				
				The version in `README.md` **must always match** the `$this->version` property in the main module descriptor class (`src/core/modules/mod{{MODULE_CLASS}}.class.php`).
				
				```php
				// In src/core/modules/mod{{MODULE_CLASS}}.class.php
				public $version = '01.02.04';  // Must match README.md version
				```
				
				---
				
				## Dolibarr Module Structure
				
				```
				{{REPO_NAME}}/
				├── src/                          # Module source code (deployed to Dolibarr)
				│   ├── README.md                 # End-user documentation
				│   ├── core/
				│   │   └── modules/
				│   │       └── mod{{MODULE_CLASS}}.class.php   # Main module descriptor
				│   ├── langs/
				│   │   └── en_US/
				│   │       └── {{MODULE_NAME}}.lang
				│   ├── sql/                      # Database schema
				│   │   ├── llx_{{MODULE_NAME}}.sql
				│   │   └── llx_{{MODULE_NAME}}.key.sql
				│   ├── class/                    # PHP class files
				│   └── lib/                      # Library files
				├── docs/                         # Technical documentation
				├── scripts/                      # Build and maintenance scripts
				├── tests/                        # Test suite
				├── .github/
				│   ├── workflows/
				│   ├── copilot-instructions.md   # This file
				│   └── CLAUDE.md
				├── README.md                     # Version source of truth
				├── CHANGELOG.md
				├── CONTRIBUTING.md
				├── LICENSE                       # GPL-3.0-or-later
				└── Makefile                      # Build automation
				```
				
				---
				
				## Module Descriptor Class Pattern
				
				The main module descriptor (`src/core/modules/mod{{MODULE_CLASS}}.class.php`) must follow this pattern:
				
				```php
				<?php
				/* … file header … */
				
				/**
				 * Description of module {{MODULE_NAME}}
				 */
				class mod{{MODULE_CLASS}} extends DolibarrModules
				{
				    /**
				     * Constructor
				     *
				     * @param DoliDB $db Database handler
				     */
				    public function __construct($db)
				    {
				        global $langs, $conf;
				
				        $this->db = $db;
				        $this->numero = {{MODULE_ID}};          // Unique module ID — do not change
				        $this->rights_class = '{{MODULE_NAME}}';
				        $this->family = 'crm';
				        $this->module_position = '50';
				        $this->name = preg_replace('/^mod/i', '', get_class($this));
				        $this->description = 'Description of {{MODULE_NAME}} module';
				        $this->version = 'XX.YY.ZZ';           // Must match README.md version
				        $this->const_name = 'MAIN_MODULE_' . strtoupper($this->name);
				        $this->picto = 'favicon.png@{{MODULE_NAME}}';
				    }
				}
				```
				
				**Key rules for the module descriptor:**
				- `$this->numero` is a globally unique ID registered in [module-registry.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/development/crm/module-registry.md) — **never change it**.
				- `$this->version` must exactly match the version in `README.md`.
				- Register new modules in the module registry before using any ID.
				
				---
				
				## GitHub Actions — Token Usage
				
				Every workflow must use **`secrets.GH_TOKEN`** (the org-level Personal Access Token).
				
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
				
				PHP scripts read the token with: `getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN')` — `GH_TOKEN` is always preferred; `GITHUB_TOKEN` is a local-dev fallback only.
				
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
				| [module-registry.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/development/crm/module-registry.md) | Dolibarr module ID registry — check before reserving a new ID |
				| [crm-development-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/crm/development-standards.md) | MokoCRM Dolibarr module development standards |
				
				---
				
				## Naming Conventions
				
				| Context | Convention | Example |
				|---------|-----------|---------|
				| PHP class | `PascalCase` | `MyService` |
				| PHP method / function | `camelCase` | `getUserData()` |
				| PHP variable | `$snake_case` | `$module_name` |
				| PHP constant | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
				| PHP class file | `PascalCase.php` | `ApiClient.php` |
				| PHP script file | `snake_case.php` | `check_health.php` |
				| YAML workflow | `kebab-case.yml` | `ci-dolibarr.yml` |
				| Markdown doc | `kebab-case.md` | `installation-guide.md` |
				
				---
				
				## Commit Messages
				
				Format: `<type>(<scope>): <subject>` — imperative, lower-case subject, no trailing period.
				
				Valid types: `feat` · `fix` · `docs` · `chore` · `ci` · `refactor` · `style` · `test` · `perf` · `revert` · `build`
				
				---
				
				## Branch Naming
				
				Format: `<prefix>/<MAJOR.MINOR.PATCH>[/description]`
				
				Approved prefixes: `dev/` · `rc/` · `version/` · `patch/` · `copilot/` · `dependabot/`
				
				---
				
				## Keeping Documentation Current
				
				| Change type | Documentation to update |
				|-------------|------------------------|
				| New or renamed public PHP method | PHPDoc block; `docs/api/` index for that class |
				| New or changed module version | Update `$this->version` in module descriptor; bump `README.md` |
				| New library class or major feature | `CHANGELOG.md` entry under `Added` |
				| Bug fix | `CHANGELOG.md` entry under `Fixed` |
				| Breaking change | `CHANGELOG.md` entry under `Changed` |
				| Any modified file | Update the `VERSION` field in that file's `FILE INFORMATION` block |
				| **Every PR** | **Bump the patch version** — increment `XX.YY.ZZ` in `README.md`; `sync-version-on-merge` propagates it |
				
				---
				
				## Key Constraints
				
				- Never commit directly to `main` — all changes go via PR, squash-merged
				- Never skip the FILE INFORMATION block on a new file
				- Never change `$this->numero` (module ID) — it is permanently registered in the module registry
				- Never hardcode version numbers in body text — update `README.md` and let automation propagate
				- Never use `github.token` or `secrets.GITHUB_TOKEN` in workflows — always use `secrets.GH_TOKEN`
				- Never let the module descriptor `$this->version` and `README.md` version go out of sync
				- Never register a new module ID without first checking module-registry.md for the next available ID
				MOKO_END
          },
          {
            name                = "CLAUDE.md"
            extension           = "md"
            description         = "Claude AI assistant context enforcing MokoStandards — Dolibarr/CRM edition"
            requirement_status  = "required"
            always_overwrite    = false
            destination_path    = ".github"
            destination_filename = "CLAUDE.md"
            template            = "templates/github/CLAUDE.dolibarr.md.template"
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
				> | `{{MODULE_NAME}}` | The module name as used in Dolibarr (lowercase, e.g. `mymodule`) — from the `langs/en_US/*.lang` filename or `$this->rights_class` in the module descriptor |
				> | `{{MODULE_CLASS}}` | PascalCase module class name (e.g. `MyModule`) — from the `src/core/modules/mod*.class.php` filename |
				> | `{{MODULE_ID}}` | The `$this->numero` value in `src/core/modules/mod*.class.php`; check [module-registry.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/development/crm/module-registry.md) if creating a new module |
				>
				> ---
				
				# What This Repo Is
				
				**{{REPO_NAME}}** is a Moko Consulting **MokoCRM** (Dolibarr) module repository.
				
				{{REPO_DESCRIPTION}}
				
				Module name: **{{MODULE_NAME}}**
				Module class: **{{MODULE_CLASS}}**
				Module ID: **{{MODULE_ID}}** *(unique, immutable — registered in [module-registry.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/development/crm/module-registry.md))*
				Repository URL: {{REPO_URL}}
				
				This repository is governed by [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) — the single source of truth for coding standards, file-header policies, GitHub Actions workflows, and Terraform configuration templates across all Moko Consulting repositories.
				
				---
				
				# Repo Structure
				
				```
				{{REPO_NAME}}/
				├── src/                              # Module source (deployed to Dolibarr)
				│   ├── README.md                     # End-user documentation
				│   ├── core/
				│   │   └── modules/
				│   │       └── mod{{MODULE_CLASS}}.class.php  # Main module descriptor
				│   ├── langs/
				│   │   └── en_US/{{MODULE_NAME}}.lang
				│   ├── sql/                          # Database schema
				│   ├── class/                        # PHP class files
				│   └── lib/                          # Library files
				├── docs/                             # Technical documentation
				├── scripts/                          # Build and maintenance scripts
				├── tests/                            # Test suite
				│   ├── unit/
				│   └── integration/
				├── .github/
				│   ├── workflows/                    # CI/CD workflows (synced from MokoStandards)
				│   ├── copilot-instructions.md
				│   └── CLAUDE.md                     # This file
				├── README.md                         # Version source of truth
				├── CHANGELOG.md
				├── CONTRIBUTING.md
				├── LICENSE                           # GPL-3.0-or-later
				└── Makefile                          # Build automation
				```
				
				---
				
				# Primary Language
				
				**PHP** (≥ 8.1) is the primary language for this Dolibarr module. YAML uses 2-space indentation. All other text files use tabs per `.editorconfig`.
				
				---
				
				# Version Management
				
				**`README.md` is the single source of truth for the repository version.**
				
				- **Bump the patch version on every PR** — increment `XX.YY.ZZ` (e.g. `01.02.03` → `01.02.04`) in `README.md` before opening the PR; the `sync-version-on-merge` workflow propagates it to all `FILE INFORMATION` headers automatically on merge.
				- Version format is zero-padded semver: `XX.YY.ZZ` (e.g. `01.02.03`).
				- Never hardcode a version number in body text — use the badge or FILE INFORMATION header only.
				
				### Dolibarr Version Alignment
				
				Two artefacts must always carry the same version:
				
				| Artefact | Location |
				|----------|----------|
				| `README.md` | `FILE INFORMATION VERSION` field + badge |
				| Module descriptor | `$this->version` in `src/core/modules/mod{{MODULE_CLASS}}.class.php` |
				
				---
				
				# Module Descriptor Class
				
				The file `src/core/modules/mod{{MODULE_CLASS}}.class.php` is the Dolibarr module descriptor. The key properties:
				
				```php
				public $numero  = {{MODULE_ID}};       // IMMUTABLE — never change; registered globally
				public $version = 'XX.YY.ZZ';         // Must match README.md version exactly
				```
				
				**`$numero` is permanent.** It was registered in [module-registry.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/development/crm/module-registry.md) when this module was created. Changing it would break all Dolibarr installations that have this module activated.
				
				Before creating a new module, always check the registry for the next available ID.
				
				---
				
				# File Header Requirements
				
				Every new file **must** have a copyright header as its first content. JSON files, binary files, generated files, and third-party files are exempt.
				
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
				 * PATH: /src/class/MyClass.php
				 * VERSION: XX.YY.ZZ
				 * BRIEF: One-line description of file purpose
				 */
				```
				
				**Markdown / YAML / Shell:** Use the appropriate comment syntax with the same fields.
				
				---
				
				# Coding Standards
				
				## Naming Conventions
				
				| Context | Convention | Example |
				|---------|-----------|---------|
				| PHP class | `PascalCase` | `MyService` |
				| PHP method / function | `camelCase` | `getUserData()` |
				| PHP variable | `$snake_case` | `$module_name` |
				| PHP constant | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
				| PHP class file | `PascalCase.php` | `ApiClient.php` |
				| PHP script file | `snake_case.php` | `check_health.php` |
				| YAML workflow | `kebab-case.yml` | `ci-dolibarr.yml` |
				| Markdown doc | `kebab-case.md` | `installation-guide.md` |
				
				## Commit Messages
				
				Format: `<type>(<scope>): <subject>` — imperative, lower-case subject, no trailing period.
				
				Valid types: `feat` · `fix` · `docs` · `chore` · `ci` · `refactor` · `style` · `test` · `perf` · `revert` · `build`
				
				## Branch Naming
				
				Format: `<prefix>/<MAJOR.MINOR.PATCH>[/description]`
				
				Approved prefixes: `dev/` · `rc/` · `version/` · `patch/` · `copilot/` · `dependabot/`
				
				---
				
				# GitHub Actions — Token Usage
				
				Every workflow must use **`secrets.GH_TOKEN`** (the org-level Personal Access Token).
				
				```yaml
				# ✅ Correct
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
				
				| Change type | Documentation to update |
				|-------------|------------------------|
				| New or renamed PHP class/method | PHPDoc block; `docs/api/` entry |
				| New or changed module version | Update `$this->version` in module descriptor; bump `README.md` |
				| New library class or major feature | `CHANGELOG.md` entry under `Added` |
				| Bug fix | `CHANGELOG.md` entry under `Fixed` |
				| Breaking change | `CHANGELOG.md` entry under `Changed` |
				| Any modified file | Update the `VERSION` field in that file's `FILE INFORMATION` block |
				| **Every PR** | **Bump the patch version** — increment `XX.YY.ZZ` in `README.md`; `sync-version-on-merge` propagates it |
				
				---
				
				# What NOT to Do
				
				- **Never commit directly to `main`** — all changes go through a PR.
				- **Never hardcode version numbers** in body text — update `README.md` and let automation propagate.
				- **Never change `$this->numero`** — the module ID is permanent and globally registered.
				- **Never skip the FILE INFORMATION block** on a new source file.
				- **Never use bare `catch (\Throwable $e) {}`** — always log or re-throw.
				- **Never mix tabs and spaces** within a file — follow `.editorconfig`.
				- **Never use `github.token` or `secrets.GITHUB_TOKEN` in workflows** — always use `secrets.GH_TOKEN`.
				- **Never register a new module ID** without first consulting module-registry.md.
				- **Never let `$this->version` and `README.md` version diverge.**
				
				---
				
				# PR Checklist
				
				Before opening a PR, verify:
				
				- [ ] Patch version bumped in `README.md` (e.g. `01.02.03` → `01.02.04`)
				- [ ] `$this->version` in module descriptor updated to match
				- [ ] FILE INFORMATION headers updated in modified files
				- [ ] CHANGELOG.md updated
				
				---
				
				# Key Policy Documents (MokoStandards)
				
				| Document | Purpose |
				|----------|---------|
				| [file-header-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/file-header-standards.md) | Copyright-header rules for every file type |
				| [coding-style-guide.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/coding-style-guide.md) | Naming and formatting conventions |
				| [branching-strategy.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/branching-strategy.md) | Branch naming, hierarchy, and release workflow |
				| [merge-strategy.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/merge-strategy.md) | Squash-merge policy and PR conventions |
				| [changelog-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/changelog-standards.md) | How and when to update CHANGELOG.md |
				| [module-registry.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/development/crm/module-registry.md) | Dolibarr module ID registry — check before reserving a new ID |
				| [crm/development-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/crm/development-standards.md) | MokoCRM Dolibarr module development standards |
				| [dolibarr-development-guide.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/guide/crm/dolibarr-development-guide.md) | MokoCRM full development guide |
				MOKO_END
          }
        ]
        subdirectories = [
          {
            name                = "workflows"
            path                = ".github/workflows"
            description         = "GitHub Actions workflows"
            requirement_status  = "required"
            files = [
              {
                name                = "ci-dolibarr.yml"
                extension           = "yml"
                description         = "Dolibarr-specific CI workflow"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/workflows/dolibarr/ci-dolibarr.yml.template"
              },
              {
                name                = "codeql-analysis.yml"
                extension           = "yml"
                description         = "CodeQL security analysis workflow"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/workflows/generic/codeql-analysis.yml.template"
              },
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
              }
            ]
          }
        ]
      },
      {
        name                = "img"
        path                = "img"
        description         = "Module image assets including Dolibarr picto"
        requirement_status  = "required"
        purpose             = "Contains the module picto displayed in the Dolibarr UI"
        files = [
          {
            name                = "favicon.png"
            extension           = "png"
            description         = "Moko Consulting picto shown in Dolibarr module list"
            requirement_status  = "required"
            always_overwrite    = true
            template            = "templates/build/dolibarr/img/favicon.png"
          }
        ]
      }
    ]
  }
}
