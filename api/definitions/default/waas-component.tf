/**
 * MokoWaaS Component Structure Definition
 * Standard repository structure for MokoWaaS (Joomla) components
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0
 * Schema Version: 1.0
 */

locals {
  repository_structure = {
    metadata = {
      name             = "MokoWaaS Component"
      description      = "Standard repository structure for MokoWaaS (Joomla) components"
      repository_type  = "waas-component"
      platform         = "mokowaas"
      last_updated     = "2026-01-15T00:00:00Z"
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
      },
      {
        name              = "LICENSE"
        extension         = ""
        description       = "License file (GPL-3.0-or-later) - Default for Joomla/WaaS components"
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
        always_overwrite  = true
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
        name              = "update.xml"
        extension         = "xml"
        description       = "Joomla extension update server manifest — lists releases for Joomla auto-update; must be kept in sync with manifest.xml version"
        required          = true
        always_overwrite  = false
        audience          = "developer"
        template          = "templates/joomla/update.xml.template"
        stub_content      = <<-MOKO_END
        <!--
          Joomla Extension Update Server XML
          See: https://docs.joomla.org/Deploying_an_Update_Server
        
          This file is the update server manifest for {{EXTENSION_NAME}}.
          The Joomla installer polls this URL to check for new versions.
        
          The manifest.xml in this repository must reference this file:
            <updateservers>
              <server type="extension" priority="1" name="{{EXTENSION_NAME}}">
                {{REPO_URL}}/raw/main/update.xml
              </server>
            </updateservers>
        
          When a new release is made, run `make release` or the release workflow to
          prepend a new <update> entry to this file automatically.
        -->
        <updates>
        	<update>
        		<name>{{EXTENSION_NAME}}</name>
        		<description>{{REPO_NAME}} — Moko Consulting Joomla extension</description>
        		<element>{{EXTENSION_ELEMENT}}</element>
        		<type>{{EXTENSION_TYPE}}</type>
        		<version>{{VERSION}}</version>
        		<infourl title="Release Information">{{REPO_URL}}/releases/tag/{{VERSION}}</infourl>
        		<downloads>
        			<downloadurl type="full" format="zip">{{DOWNLOAD_URL}}</downloadurl>
        		</downloads>
        		<targetplatform name="joomla" version="4\.[0-9]+" />
        		<php_minimum>7.4</php_minimum>
        		<maintainer>Moko Consulting</maintainer>
        		<maintainerurl>{{MAINTAINER_URL}}</maintainerurl>
        	</update>
        </updates>
        MOKO_END
      },
      {
        name                = "Makefile"
        description         = "Build automation using MokoStandards templates"
        required            = true
        always_overwrite    = true
        audience            = "developer"
        source_path         = "templates/makefiles"
        source_filename     = "Makefile.joomla.template"
        source_type         = "template"
        destination_path    = "."
        destination_filename = "Makefile"
        create_path         = false
        template            = "templates/makefiles/Makefile.joomla.template"
      },
      {
        name              = ".gitignore"
        extension         = "gitignore"
        description       = "Git ignore patterns for Joomla development - preserved during sync operations"
        required          = true
        always_overwrite  = false
        audience          = "developer"
        template          = "templates/configs/.gitignore.joomla"
        validation_rules = [
          {
            type        = "content-pattern"
            description = "Must contain sftp-config pattern to ignore SFTP sync configuration files"
            pattern     = "sftp-config"
            severity    = "error"
          },
          {
            type        = "content-pattern"
            description = "Must contain user.css pattern to ignore custom user CSS overrides"
            pattern     = "user\\.css"
            severity    = "error"
          },
          {
            type        = "content-pattern"
            description = "Must contain user.js pattern to ignore custom user JavaScript overrides"
            pattern     = "user\\.js"
            severity    = "error"
          },
          {
            type        = "content-pattern"
            description = "Must contain modulebuilder.txt pattern to ignore Joomla Module Builder artifacts"
            pattern     = "modulebuilder\\.txt"
            severity    = "error"
          },
          {
            type        = "content-pattern"
            description = "Must contain colors_custom.css pattern to ignore custom color scheme overrides"
            pattern     = "colors_custom\\.css"
            severity    = "error"
          }
        ]
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
        name                = "site"
        path                = "site"
        description         = "Component frontend (site) code"
        required            = true
        purpose             = "Contains frontend component code deployed to site"
        files = [
          {
            name              = "controller.php"
            extension         = "php"
            description       = "Main site controller"
            required          = true
            audience          = "developer"
          },
          {
            name              = "manifest.xml"
            extension         = "xml"
            description       = "Component manifest for site"
            required          = true
            audience          = "developer"
          }
        ]
        subdirectories = [
          {
            name                = "controllers"
            path                = "site/controllers"
            description         = "Site controllers"
            requirement_status  = "suggested"
          },
          {
            name                = "models"
            path                = "site/models"
            description         = "Site models"
            requirement_status  = "suggested"
          },
          {
            name                = "views"
            path                = "site/views"
            description         = "Site views"
            required            = true
          }
        ]
      },
      {
        name                = "admin"
        path                = "admin"
        description         = "Component backend (admin) code"
        required            = true
        purpose             = "Contains backend component code for administrator"
        files = [
          {
            name              = "controller.php"
            extension         = "php"
            description       = "Main admin controller"
            required          = true
            audience          = "developer"
          }
        ]
        subdirectories = [
          {
            name                = "controllers"
            path                = "admin/controllers"
            description         = "Admin controllers"
            requirement_status  = "suggested"
          },
          {
            name                = "models"
            path                = "admin/models"
            description         = "Admin models"
            requirement_status  = "suggested"
          },
          {
            name                = "views"
            path                = "admin/views"
            description         = "Admin views"
            required            = true
          },
          {
            name                = "sql"
            path                = "admin/sql"
            description         = "Database schema files"
            requirement_status  = "suggested"
          }
        ]
      },
      {
        name                = "media"
        path                = "media"
        description         = "Media files (CSS, JS, images)"
        requirement_status  = "suggested"
        purpose             = "Contains static assets"
        subdirectories = [
          {
            name                = "css"
            path                = "media/css"
            description         = "Stylesheets"
            requirement_status  = "suggested"
          },
          {
            name                = "js"
            path                = "media/js"
            description         = "JavaScript files"
            requirement_status  = "suggested"
          },
          {
            name                = "images"
            path                = "media/images"
            description         = "Image files"
            requirement_status  = "suggested"
          }
        ]
      },
      {
        name                = "language"
        path                = "language"
        description         = "Language translation files"
        required            = true
        purpose             = "Contains language INI files"
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
            description         = "Package building script for Joomla component"
            requirement_status  = "suggested"
            template            = "templates/scripts/release/package_joomla.sh"
          },
          {
            name                = "validate_manifest.sh"
            extension           = "sh"
            description         = "Manifest validation script"
            requirement_status  = "suggested"
            template            = "templates/scripts/validate/manifest.sh"
          },
          {
            name                = "MokoStandards.override.xml"
            extension           = "xml"
            description         = "MokoStandards sync override configuration - preserved during sync"
            requirement_status  = "suggested"
            always_overwrite    = false
            audience            = "developer"
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
            description         = "GitHub Copilot custom instructions enforcing MokoStandards — Joomla/WaaS edition"
            requirement_status  = "required"
            always_overwrite    = false
            destination_path    = ".github"
            destination_filename = "copilot-instructions.md"
            template            = "templates/github/copilot-instructions.joomla.md.template"
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
				> | `{{EXTENSION_NAME}}` | The `<name>` element in `manifest.xml` at the repository root |
				> | `{{EXTENSION_TYPE}}` | The `type` attribute of the `<extension>` tag in `manifest.xml` (`component`, `module`, `plugin`, or `template`) |
				> | `{{EXTENSION_ELEMENT}}` | The `<element>` tag in `manifest.xml`, or the filename prefix (e.g. `com_myextension`, `mod_mymodule`) |
				>
				> ---
				
				# {{REPO_NAME}} — GitHub Copilot Custom Instructions
				
				## What This Repo Is
				
				This is a **Moko Consulting MokoWaaS** (Joomla) repository governed by [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards). All coding standards, workflows, and policies are defined there and enforced here via bulk sync.
				
				Repository URL: {{REPO_URL}}
				Extension name: **{{EXTENSION_NAME}}**
				Extension type: **{{EXTENSION_TYPE}}** (`{{EXTENSION_ELEMENT}}`)
				Platform: **Joomla 4.x / MokoWaaS**
				
				---
				
				## Primary Language
				
				**PHP** (≥ 7.4) is the primary language for this Joomla extension. JavaScript may be used for frontend enhancements. YAML uses 2-space indentation. All other text files use tabs per `.editorconfig`.
				
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
				 * DEFGROUP: {{REPO_NAME}}.{{EXTENSION_TYPE}}
				 * INGROUP: {{REPO_NAME}}
				 * REPO: {{REPO_URL}}
				 * PATH: /path/to/file.php
				 * VERSION: XX.YY.ZZ
				 * BRIEF: One-line description of purpose
				 */
				
				defined('_JEXEC') or die;
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
				
				**YAML / Shell / XML:** Use the appropriate comment syntax with the same fields. JSON files are exempt.
				
				---
				
				## Version Management
				
				**`README.md` is the single source of truth for the repository version.**
				
				- **Bump the patch version on every PR** — increment `XX.YY.ZZ` (e.g. `01.02.03` → `01.02.04`) in `README.md` before opening the PR; the `sync-version-on-merge` workflow propagates it automatically to all badges and `FILE INFORMATION` headers on merge to `main`.
				- The `VERSION: XX.YY.ZZ` field in `README.md` governs all other version references.
				- Version format is zero-padded semver: `XX.YY.ZZ` (e.g. `01.02.03`).
				- Never hardcode a specific version in document body text — use the badge or FILE INFORMATION header only.
				
				### Joomla Version Alignment
				
				The version in `README.md` **must always match** the `<version>` tag in `manifest.xml` and the latest entry in `update.xml`. The `make release` command / release workflow updates all three automatically.
				
				```xml
				<!-- In manifest.xml — must match README.md version -->
				<version>01.02.04</version>
				
				<!-- In update.xml — prepend a new <update> block for every release.
				     Note: the backslash in version="4\.[0-9]+" is a literal backslash character
				     in the XML attribute value. Joomla's update server treats the value as a
				     regular expression, so \. matches a literal dot. -->
				<updates>
					<update>
						<name>{{EXTENSION_NAME}}</name>
						<version>01.02.04</version>
						<downloads>
							<downloadurl type="full" format="zip">
								{{REPO_URL}}/releases/download/01.02.04/{{EXTENSION_ELEMENT}}-01.02.04.zip
							</downloadurl>
						</downloads>
						<targetplatform name="joomla" version="4\.[0-9]+" />
					</update>
					<!-- … older entries preserved below … -->
				</updates>
				```
				
				---
				
				## Joomla Extension Structure
				
				```
				{{REPO_NAME}}/
				├── manifest.xml          # Joomla installer manifest (root — required)
				├── update.xml            # Update server manifest (root — required, see below)
				├── site/                 # Frontend (site) code
				│   ├── controller.php
				│   ├── controllers/
				│   ├── models/
				│   └── views/
				├── admin/                # Backend (admin) code
				│   ├── controller.php
				│   ├── controllers/
				│   ├── models/
				│   ├── views/
				│   └── sql/
				├── language/             # Language INI files
				├── media/                # CSS, JS, images (deployed to /media/{{EXTENSION_ELEMENT}}/)
				├── docs/                 # Technical documentation
				├── tests/                # Test suite
				├── .github/
				│   ├── workflows/
				│   ├── copilot-instructions.md  # This file
				│   └── CLAUDE.md
				├── README.md             # Version source of truth
				├── CHANGELOG.md
				├── CONTRIBUTING.md
				├── LICENSE               # GPL-3.0-or-later
				└── Makefile              # Build automation
				```
				
				---
				
				## update.xml — Required in Repo Root
				
				`update.xml` **must exist at the repository root**. It is the Joomla update server manifest that allows Joomla installations to check for new versions of this extension.
				
				The `manifest.xml` must reference it via:
				```xml
				<updateservers>
					<server type="extension" priority="1" name="{{EXTENSION_NAME}}">
						{{REPO_URL}}/raw/main/update.xml
					</server>
				</updateservers>
				```
				
				**Rules:**
				- Every release must prepend a new `<update>` block at the top of `update.xml` — old entries must be preserved below.
				- The `<version>` in `update.xml` must exactly match `<version>` in `manifest.xml` and the version in `README.md`.
				- The `<downloadurl>` must be a publicly accessible direct download link (GitHub Releases asset URL).
				- `<targetplatform name="joomla" version="4\.[0-9]+">` — the backslash is a **literal backslash character** in the XML attribute value; Joomla's update-server parser treats the value as a regular expression, so `\.` matches a literal dot and `[0-9]+` matches one or more digits. Do not double-escape it.
				
				---
				
				## manifest.xml Rules
				
				- Lives at the repo root as `manifest.xml` (not inside `site/` or `admin/`).
				- `<version>` tag must be kept in sync with `README.md` version and `update.xml`.
				- Must include `<updateservers>` block pointing to this repo's `update.xml`.
				- Must include `<files folder="site">` and `<administration>` sections.
				- Joomla 4.x requires `<namespace path="src">Moko\{{EXTENSION_NAME}}</namespace>` for namespaced extensions.
				
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
				| [joomla-development-guide.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/guide/waas/joomla-development-guide.md) | MokoWaaS Joomla extension development guide |
				
				---
				
				## Naming Conventions
				
				| Context | Convention | Example |
				|---------|-----------|---------|
				| PHP class | `PascalCase` | `MyController` |
				| PHP method / function | `camelCase` | `getItems()` |
				| PHP variable | `$snake_case` | `$item_id` |
				| PHP constant | `UPPER_SNAKE_CASE` | `MAX_ITEMS` |
				| PHP class file | `PascalCase.php` | `ItemModel.php` |
				| YAML workflow | `kebab-case.yml` | `ci-joomla.yml` |
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
				| New or renamed PHP class/method | PHPDoc block; `docs/api/` entry |
				| New or changed manifest.xml | Update `update.xml` version; bump README.md version |
				| New release | Prepend `<update>` block to `update.xml`; update CHANGELOG.md; bump README.md version |
				| New or changed workflow | `docs/workflows/<workflow-name>.md` |
				| Any modified file | Update the `VERSION` field in that file's `FILE INFORMATION` block |
				| **Every PR** | **Bump the patch version** — increment `XX.YY.ZZ` in `README.md`; `sync-version-on-merge` propagates it |
				
				---
				
				## Key Constraints
				
				- Never commit directly to `main` — all changes go via PR, squash-merged
				- Never skip the FILE INFORMATION block on a new file
				- Never add `defined('_JEXEC') or die;` to CLI scripts or model tests — only to web-accessible PHP files
				- Never hardcode version numbers in body text — update `README.md` and let automation propagate
				- Never use `github.token` or `secrets.GITHUB_TOKEN` in workflows — always use `secrets.GH_TOKEN`
				- Never let `manifest.xml` version, `update.xml` version, and `README.md` version go out of sync
				MOKO_END
          },
          {
            name                = "CLAUDE.md"
            extension           = "md"
            description         = "Claude AI assistant context enforcing MokoStandards — Joomla/WaaS edition"
            requirement_status  = "required"
            always_overwrite    = false
            destination_path    = ".github"
            destination_filename = "CLAUDE.md"
            template            = "templates/github/CLAUDE.joomla.md.template"
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
				> | `{{EXTENSION_NAME}}` | The `<name>` element in `manifest.xml` at the repository root |
				> | `{{EXTENSION_TYPE}}` | The `type` attribute of the `<extension>` tag in `manifest.xml` (`component`, `module`, `plugin`, or `template`) |
				> | `{{EXTENSION_ELEMENT}}` | The `<element>` tag in `manifest.xml`, or the filename prefix (e.g. `com_myextension`, `mod_mymodule`) |
				>
				> ---
				
				# What This Repo Is
				
				**{{REPO_NAME}}** is a Moko Consulting **MokoWaaS** (Joomla) extension repository.
				
				{{REPO_DESCRIPTION}}
				
				Extension name: **{{EXTENSION_NAME}}**
				Extension type: **{{EXTENSION_TYPE}}** (`{{EXTENSION_ELEMENT}}`)
				Repository URL: {{REPO_URL}}
				
				This repository is governed by [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) — the single source of truth for coding standards, file-header policies, GitHub Actions workflows, and Terraform configuration templates across all Moko Consulting repositories.
				
				---
				
				# Repo Structure
				
				```
				{{REPO_NAME}}/
				├── manifest.xml          # Joomla installer manifest (root — required)
				├── update.xml            # Update server manifest (root — required)
				├── site/                 # Frontend (site) code
				│   ├── controller.php
				│   ├── controllers/
				│   ├── models/
				│   └── views/
				├── admin/                # Backend (admin) code
				│   ├── controller.php
				│   ├── controllers/
				│   ├── models/
				│   ├── views/
				│   └── sql/
				├── language/             # Language INI files
				├── media/                # CSS, JS, images
				├── docs/                 # Technical documentation
				├── tests/                # Test suite
				├── .github/
				│   ├── workflows/        # CI/CD workflows (synced from MokoStandards)
				│   ├── copilot-instructions.md
				│   └── CLAUDE.md         # This file
				├── README.md             # Version source of truth
				├── CHANGELOG.md
				├── CONTRIBUTING.md
				└── LICENSE               # GPL-3.0-or-later
				```
				
				---
				
				# Primary Language
				
				**PHP** (≥ 7.4) is the primary language for this Joomla extension. YAML uses 2-space indentation. All other text files use tabs per `.editorconfig`.
				
				---
				
				# Version Management
				
				**`README.md` is the single source of truth for the repository version.**
				
				- **Bump the patch version on every PR** — increment `XX.YY.ZZ` (e.g. `01.02.03` → `01.02.04`) in `README.md` before opening the PR; the `sync-version-on-merge` workflow propagates it to all `FILE INFORMATION` headers automatically on merge.
				- Version format is zero-padded semver: `XX.YY.ZZ` (e.g. `01.02.03`).
				- Never hardcode a version number in body text — use the badge or FILE INFORMATION header only.
				
				### Joomla Version Alignment
				
				Three files must **always have the same version**:
				
				| File | Where the version lives |
				|------|------------------------|
				| `README.md` | `FILE INFORMATION` block + badge |
				| `manifest.xml` | `<version>` tag |
				| `update.xml` | `<version>` in the most recent `<update>` block |
				
				The `make release` command / release workflow syncs all three automatically.
				
				---
				
				# update.xml — Required in Repo Root
				
				`update.xml` is the Joomla update server manifest. It allows Joomla installations to check for new versions of this extension via:
				
				```xml
				<!-- In manifest.xml -->
				<updateservers>
					<server type="extension" priority="1" name="{{EXTENSION_NAME}}">
						{{REPO_URL}}/raw/main/update.xml
					</server>
				</updateservers>
				```
				
				**Rules:**
				- Every release prepends a new `<update>` block at the top — older entries are preserved.
				- `<version>` in `update.xml` must exactly match `<version>` in `manifest.xml` and `README.md`.
				- `<downloadurl>` must be a publicly accessible GitHub Releases asset URL.
				- `<targetplatform version="4\.[0-9]+">` — backslash is literal (Joomla regex syntax).
				
				Example `update.xml` entry for a new release:
				```xml
				<updates>
					<update>
						<name>{{EXTENSION_NAME}}</name>
						<description>{{REPO_NAME}}</description>
						<element>{{EXTENSION_ELEMENT}}</element>
						<type>{{EXTENSION_TYPE}}</type>
						<version>01.02.04</version>
						<infourl title="Release Information">{{REPO_URL}}/releases/tag/01.02.04</infourl>
						<downloads>
							<downloadurl type="full" format="zip">
								{{REPO_URL}}/releases/download/01.02.04/{{EXTENSION_ELEMENT}}-01.02.04.zip
							</downloadurl>
						</downloads>
						<targetplatform name="joomla" version="4\.[0-9]+" />
						<php_minimum>7.4</php_minimum>
						<maintainer>Moko Consulting</maintainer>
						<maintainerurl>https://mokoconsulting.tech</maintainerurl>
					</update>
				</updates>
				```
				
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
				 * DEFGROUP: {{REPO_NAME}}.{{EXTENSION_TYPE}}
				 * INGROUP: {{REPO_NAME}}
				 * REPO: {{REPO_URL}}
				 * PATH: /site/controllers/item.php
				 * VERSION: XX.YY.ZZ
				 * BRIEF: One-line description of file purpose
				 */
				
				defined('_JEXEC') or die;
				```
				
				**Markdown / YAML / Shell / XML:** Use the appropriate comment syntax with the same fields.
				
				---
				
				# Coding Standards
				
				## Naming Conventions
				
				| Context | Convention | Example |
				|---------|-----------|---------|
				| PHP class | `PascalCase` | `ItemModel` |
				| PHP method / function | `camelCase` | `getItems()` |
				| PHP variable | `$snake_case` | `$item_id` |
				| PHP constant | `UPPER_SNAKE_CASE` | `MAX_ITEMS` |
				| PHP class file | `PascalCase.php` | `ItemModel.php` |
				| YAML workflow | `kebab-case.yml` | `ci-joomla.yml` |
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
				
				---
				
				# Keeping Documentation Current
				
				| Change type | Documentation to update |
				|-------------|------------------------|
				| New or renamed PHP class/method | PHPDoc block; `docs/api/` entry |
				| New or changed `manifest.xml` | Sync version to `update.xml` and `README.md` |
				| New release | Prepend `<update>` to `update.xml`; update `CHANGELOG.md`; bump `README.md` |
				| New or changed workflow | `docs/workflows/<workflow-name>.md` |
				| Any modified file | Update the `VERSION` field in that file's `FILE INFORMATION` block |
				| **Every PR** | **Bump the patch version** — increment `XX.YY.ZZ` in `README.md`; `sync-version-on-merge` propagates it |
				
				---
				
				# What NOT to Do
				
				- **Never commit directly to `main`** — all changes go through a PR.
				- **Never hardcode version numbers** in body text — update `README.md` and let automation propagate.
				- **Never let `manifest.xml`, `update.xml`, and `README.md` versions diverge.**
				- **Never skip the FILE INFORMATION block** on a new source file.
				- **Never use bare `catch (\Throwable $e) {}`** — always log or re-throw.
				- **Never mix tabs and spaces** within a file — follow `.editorconfig`.
				- **Never use `github.token` or `secrets.GITHUB_TOKEN` in workflows** — always use `secrets.GH_TOKEN`.
				- **Never remove `defined('_JEXEC') or die;`** from web-accessible PHP files.
				
				---
				
				# PR Checklist
				
				Before opening a PR, verify:
				
				- [ ] Patch version bumped in `README.md` (e.g. `01.02.03` → `01.02.04`)
				- [ ] If this is a release: `manifest.xml` version updated; `update.xml` updated with new entry
				- [ ] FILE INFORMATION headers updated in modified files
				- [ ] CHANGELOG.md updated
				- [ ] Tests pass
				
				---
				
				# Key Policy Documents (MokoStandards)
				
				| Document | Purpose |
				|----------|---------|
				| [file-header-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/file-header-standards.md) | Copyright-header rules for every file type |
				| [coding-style-guide.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/coding-style-guide.md) | Naming and formatting conventions |
				| [branching-strategy.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/branching-strategy.md) | Branch naming, hierarchy, and release workflow |
				| [merge-strategy.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/merge-strategy.md) | Squash-merge policy and PR conventions |
				| [changelog-standards.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/changelog-standards.md) | How and when to update CHANGELOG.md |
				| [joomla-development-guide.md](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/guide/waas/joomla-development-guide.md) | MokoWaaS Joomla extension development guide |
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
                name                = "ci-joomla.yml"
                extension           = "yml"
                description         = "Joomla-specific CI workflow"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/workflows/joomla/ci-joomla.yml.template"
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
      }
    ]
  }
}
