/**
 * .github-private Repository Structure Definition
 * Org-level private repository containing universal GitHub Actions workflows,
 * helper scripts, and default issue templates for all governed repositories.
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 04.00.04
 * Schema Version: 1.0
 *
 * NOTES
 * ─────
 * • GitHub reads ISSUE_TEMPLATE/ from this repo as org-wide defaults for any
 *   governed repo that does not supply its own templates.
 * • Workflows in .github/workflows/ support both standalone execution and
 *   workflow_call so governed repos can invoke them as reusable workflows via
 *   `uses: mokoconsulting-tech/.github-private/.github/workflows/<name>.yml@main`.
 * • This repo is ALWAYS synced first by bulk-repo-sync to ensure universal
 *   workflows and issue templates are current before any other repo is updated.
 */

locals {
  github_private_repository_structure = {
    metadata = {
      name             = ".github-private"
      description      = "Private GitHub org defaults — universal workflows, issue templates, and helper scripts"
      repository_type  = "github-private"
      platform         = "github-private"
      last_updated     = "2026-03-12T00:00:00Z"
      maintainer       = "Moko Consulting"
      version          = "1.0"
      schema_version   = "1.0"
      visibility       = "private"
      sync_priority    = 0
    }

    root_files = [
      {
        name              = "README.md"
        extension         = "md"
        description       = "Repository overview — purpose, contents, and how governed repos use this repo"
        required          = true
        audience          = "general"
      },
      {
        name              = "LICENSE"
        extension         = ""
        description       = "License file (GPL-3.0-or-later)"
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
        description       = "Security policy and private vulnerability reporting"
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
        name              = "CONTRIBUTING.md"
        extension         = "md"
        description       = "Contribution guidelines"
        required          = true
        audience          = "contributor"
      },
      {
        name              = "GOVERNANCE.md"
        extension         = "md"
        description       = "Governance policy and decision-making process"
        required          = true
        always_overwrite  = true
        audience          = "general"
        template          = "templates/docs/required/GOVERNANCE.md"
      },
      {
        name              = ".gitignore"
        extension         = "gitignore"
        description       = "Git ignore patterns"
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
        name              = ".editorconfig"
        extension         = "editorconfig"
        description       = "Editor configuration for consistent coding style"
        required          = true
        always_overwrite  = false
        audience          = "developer"
      },
      {
        name              = ".moko-standards.yml"
        extension         = "yml"
        description       = "MokoStandards governance marker — identifies this repo as platform=github-private"
        required          = true
        always_overwrite  = true
        template          = "templates/configs/moko-standards.yml.template"
      }
    ]

    directories = [
      {
        name                = "ISSUE_TEMPLATE"
        path                = "ISSUE_TEMPLATE"
        description         = "Org-default issue templates — applied to all governed repos without their own templates"
        requirement_status  = "required"
        purpose             = "GitHub reads ISSUE_TEMPLATE/ from this repo as org-wide defaults"
        files = [
          {
            name                = "config.yml"
            extension           = "yml"
            description         = "Issue template chooser — disables blank issues and lists contact links"
            requirement_status  = "required"
            always_overwrite    = true
            template            = "templates/github-private/ISSUE_TEMPLATE/config.yml.template"
          },
          {
            name                = "bug_report.md"
            extension           = "md"
            description         = "Bug report issue template"
            requirement_status  = "required"
            always_overwrite    = false
            template            = "templates/github-private/ISSUE_TEMPLATE/bug_report.md.template"
          },
          {
            name                = "feature_request.md"
            extension           = "md"
            description         = "Feature request issue template"
            requirement_status  = "required"
            always_overwrite    = false
            template            = "templates/github-private/ISSUE_TEMPLATE/feature_request.md.template"
          }
        ]
      },
      {
        name                = "scripts"
        path                = "scripts"
        description         = "Helper scripts used by universal workflows and available as git hooks"
        requirement_status  = "required"
        purpose             = "Reusable Bash utilities for commit-message and PR-title validation"
        files = [
          {
            name                = "check-pr-title.sh"
            extension           = "sh"
            description         = "Validates PR title follows conventional-commit format"
            requirement_status  = "required"
            always_overwrite    = true
            template            = "templates/github-private/scripts/check-pr-title.sh.template"
          },
          {
            name                = "check-commit-msg.sh"
            extension           = "sh"
            description         = "Validates individual commit messages follow conventional-commit format; usable as a git commit-msg hook"
            requirement_status  = "required"
            always_overwrite    = true
            template            = "templates/github-private/scripts/check-commit-msg.sh.template"
          }
        ]
      },
      {
        name                = ".github"
        path                = ".github"
        description         = "GitHub-specific configuration for .github-private itself"
        requirement_status  = "required"
        purpose             = "Contains CI workflows for this repo and reusable workflows callable org-wide"
        subdirectories = [
          {
            name                = "workflows"
            path                = ".github/workflows"
            description         = "CI + universal reusable workflows; callable via uses: mokoconsulting-tech/.github-private/.github/workflows/<name>.yml@main"
            requirement_status  = "required"
            files = [
              {
                name                = "stale.yml"
                extension           = "yml"
                description         = "Marks stale issues and pull requests; standalone (schedule) and reusable (workflow_call)"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/github-private/workflows/stale.yml.template"
              },
              {
                name                = "auto-assign.yml"
                extension           = "yml"
                description         = "Auto-assigns PR author and logs CODEOWNERS status; standalone and reusable"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/github-private/workflows/auto-assign.yml.template"
              },
              {
                name                = "pr-labeler.yml"
                extension           = "yml"
                description         = "Labels PRs from branch name and validates PR title format; standalone and reusable"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/github-private/workflows/pr-labeler.yml.template"
              },
              {
                name                = "welcome.yml"
                extension           = "yml"
                description         = "Posts welcome message on first-time contributor PRs and issues; standalone and reusable"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/github-private/workflows/welcome.yml.template"
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
          description = "Org-level GitHub PAT for automation — required for bulk sync and workflow execution"
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
          description = "Per-repo path suffix appended to DEV_FTP_PATH (e.g. /.github-private)"
          required    = false
          scope       = "repo"
        }
      ]

      repository_settings = {
        visibility              = "private"
        has_issues              = true
        has_projects            = false
        has_wiki                = false
        has_discussions         = false
        allow_squash_merge      = true
        allow_merge_commit      = false
        allow_rebase_merge      = true
        delete_branch_on_merge  = true
      }
    }
  }
}
