/**
 * MokoStandards Repository Structure Definition
 * Repository structure definition for the MokoStandards standards and templates repository
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0
 * Schema Version: 1.0
 */

locals {
  repository_structure = {
    metadata = {
      name             = "MokoStandards Repository"
      description      = "Repository structure definition for MokoStandards - organizational standards, templates, and automation"
      repository_type  = "standards"
      platform         = "standards"
      last_updated     = "2026-03-03T00:00:00Z"
      maintainer       = "Moko Consulting"
      version          = "1.0"
      schema_version   = "1.0"
    }

    root_files = [
      {
        name              = "README.md"
        extension         = "md"
        description       = "Repository overview and documentation"
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
        required          = true
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
        name              = "CITATION.cff"
        extension         = "cff"
        description       = "Citation file format for academic references"
        required          = true
        audience          = "general"
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
        name              = ".gitmessage"
        extension         = "gitmessage"
        description       = "Git commit message template"
        required          = true
        audience          = "developer"
      },
      {
        name              = ".git-blame-ignore-revs"
        extension         = "git-blame-ignore-revs"
        description       = "Git blame ignore revisions"
        requirement_status = "suggested"
        audience          = "developer"
      },
      {
        name              = ".mailmap"
        extension         = "mailmap"
        description       = "Git mailmap for contributor attribution"
        requirement_status = "suggested"
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
        name              = ".eslintrc.json"
        extension         = "json"
        description       = "ESLint configuration for JavaScript"
        requirement_status = "suggested"
        audience          = "developer"
      },
      {
        name              = ".prettierrc.json"
        extension         = "json"
        description       = "Prettier configuration for code formatting"
        requirement_status = "suggested"
        audience          = "developer"
      },
      {
        name              = ".markdownlint.json"
        extension         = "json"
        description       = "Markdown linting configuration"
        requirement_status = "suggested"
        audience          = "developer"
      },
      {
        name              = ".yamllint"
        extension         = "yamllint"
        description       = "YAML linting configuration"
        requirement_status = "suggested"
        audience          = "developer"
      },
      {
        name              = ".pylintrc"
        extension         = "pylintrc"
        description       = "Python linting configuration"
        requirement_status = "suggested"
        audience          = "developer"
      },
      {
        name              = ".htmlhintrc"
        extension         = "htmlhintrc"
        description       = "HTML linting configuration"
        requirement_status = "suggested"
        audience          = "developer"
      },
      {
        name              = "composer.json"
        extension         = "json"
        description       = "PHP dependency management"
        requirement_status = "suggested"
        audience          = "developer"
      }
    ]

    directories = [
      {
        name                = "api"
        path                = "api"
        description         = "API scripts and automation"
        required            = true
        purpose             = "Contains all operational scripts - validation, automation, build, release, etc."
        subdirectories = [
          {
            name                = "validate"
            path                = "api/validate"
            description         = "Validation scripts"
            required            = true
            purpose             = "Scripts for validating repository structure, health, and compliance"
          },
          {
            name                = "automation"
            path                = "api/automation"
            description         = "Automation scripts"
            required            = true
            purpose             = "Scripts for bulk operations and repository synchronization"
          },
          {
            name                = "build"
            path                = "api/build"
            description         = "Build scripts"
            requirement_status  = "suggested"
            purpose             = "Scripts for building and packaging"
          },
          {
            name                = "release"
            path                = "api/release"
            description         = "Release scripts"
            requirement_status  = "suggested"
            purpose             = "Scripts for release management"
          },
          {
            name                = "tests"
            path                = "api/tests"
            description         = "Test scripts"
            requirement_status  = "suggested"
            purpose             = "Test scripts and test data"
          },
          {
            name                = "maintenance"
            path                = "api/maintenance"
            description         = "Maintenance scripts"
            requirement_status  = "suggested"
            purpose             = "Scripts for repository maintenance tasks"
          },
          {
            name                = "definitions"
            path                = "api/definitions"
            description         = "Repository structure definitions"
            required            = true
            purpose             = "HCL/Terraform definition files for different repository types"
          },
          {
            name                = "lib"
            path                = "api/lib"
            description         = "Shared libraries"
            requirement_status  = "suggested"
            purpose             = "Shared code libraries and utilities"
          }
        ]
      },
      {
        name                = "docs"
        path                = "docs"
        description         = "Documentation"
        required            = true
        purpose             = "Comprehensive documentation for standards, guides, policies, and references"
        subdirectories = [
          {
            name                = "guide"
            path                = "docs/guide"
            description         = "User guides"
            requirement_status  = "suggested"
          },
          {
            name                = "reference"
            path                = "docs/reference"
            description         = "Reference documentation"
            requirement_status  = "suggested"
          },
          {
            name                = "policy"
            path                = "docs/policy"
            description         = "Policies and standards"
            requirement_status  = "suggested"
          },
          {
            name                = "workflows"
            path                = "docs/workflows"
            description         = "Workflow documentation"
            requirement_status  = "suggested"
          },
          {
            name                = "security"
            path                = "docs/security"
            description         = "Security documentation"
            requirement_status  = "suggested"
          },
          {
            name                = "development"
            path                = "docs/development"
            description         = "Development documentation"
            requirement_status  = "suggested"
          }
        ]
      },
      {
        name                = "templates"
        path                = "templates"
        description         = "Template files"
        required            = true
        purpose             = "Template files for workflows, configs, documentation, and projects"
        subdirectories = [
          {
            name                = "workflows"
            path                = "templates/workflows"
            description         = "GitHub Actions workflow templates"
            required            = true
          },
          {
            name                = "github"
            path                = "templates/github"
            description         = "GitHub configuration templates"
            required            = true
          },
          {
            name                = "docs"
            path                = "templates/docs"
            description         = "Documentation templates"
            requirement_status  = "suggested"
          },
          {
            name                = "configs"
            path                = "templates/configs"
            description         = "Configuration file templates"
            requirement_status  = "suggested"
          },
          {
            name                = "licenses"
            path                = "templates/licenses"
            description         = "License templates"
            requirement_status  = "suggested"
          },
          {
            name                = "projects"
            path                = "templates/projects"
            description         = "Project definition templates"
            requirement_status  = "suggested"
          },
          {
            name                = "terraform"
            path                = "templates/terraform"
            description         = "Terraform configuration templates"
            requirement_status  = "suggested"
          },
          {
            name                = "scripts"
            path                = "templates/scripts"
            description         = "Script templates"
            requirement_status  = "suggested"
          }
        ]
      },
      {
        name                = "logs"
        path                = "logs"
        description         = "Log files"
        requirement_status  = "suggested"
        purpose             = "Storage for operation logs, audit trails, and metrics"
        subdirectories = [
          {
            name                = "audit"
            path                = "logs/audit"
            description         = "Audit logs"
            requirement_status  = "suggested"
          },
          {
            name                = "automation"
            path                = "logs/automation"
            description         = "Automation logs"
            requirement_status  = "suggested"
          },
          {
            name                = "validation"
            path                = "logs/validation"
            description         = "Validation logs"
            requirement_status  = "suggested"
          }
        ]
      },
      {
        name                = ".github"
        path                = ".github"
        description         = "GitHub-specific configuration"
        required            = true
        purpose             = "GitHub Actions workflows, issue templates, and configuration"
        subdirectories = [
          {
            name                = "workflows"
            path                = ".github/workflows"
            description         = "GitHub Actions workflows"
            required            = true
          },
          {
            name                = "ISSUE_TEMPLATE"
            path                = ".github/ISSUE_TEMPLATE"
            description         = "GitHub issue templates"
            required            = true
          }
        ]
        files = [
          {
            name                = "config.tf"
            extension           = "tf"
            description         = "Repository override configuration for bulk sync"
            requirement_status  = "suggested"
            always_overwrite    = false
            audience            = "developer"
          },
          {
            name                = "copilot.yml"
            extension           = "yml"
            description         = "GitHub Copilot configuration"
            requirement_status  = "suggested"
            audience            = "developer"
          }
        ]
      },
      {
        name                = ".checkpoints"
        path                = ".checkpoints"
        description         = "Checkpoint files for long-running operations"
        requirement_status  = "optional"
        purpose             = "Stores checkpoint data for resumable operations"
      }
    ]

    repository_requirements = {
      secrets = [
        {
          name        = "GH_TOKEN"
          description = "Org-level GitHub PAT for automation — configure in org Actions secrets"
          required    = true
        }
      ]

      variables = [
        {
          name        = "STANDARDS_VERSION"
          description = "Current MokoStandards version"
          required    = false
        }
      ]

      branch_protections = {
        main = {
          required_status_checks = {
            strict   = true
            contexts = ["standards-compliance", "code-quality"]
          }
          enforce_admins                = false
          required_pull_request_reviews = {
            dismiss_stale_reviews           = true
            require_code_owner_reviews      = true
            required_approving_review_count = 1
          }
        }
      }

      repository_settings = {
        has_issues      = true
        has_projects    = true
        has_wiki        = false
        has_discussions = true
        allow_squash_merge = true
        allow_merge_commit = false
        allow_rebase_merge = true
        delete_branch_on_merge = true
      }

      labels = [
        { name = "bulk-sync-success", color = "0e8a16", description = "Bulk sync completed successfully" },
        { name = "bulk-sync-failure", color = "d73a4a", description = "Bulk sync failed" },
        { name = "standards-update", color = "fbca04", description = "Standards update" },
        { name = "template-update", color = "d4c5f9", description = "Template file update" },
        { name = "documentation", color = "0075ca", description = "Documentation changes" },
        { name = "automation", color = "5319e7", description = "Automation scripts" }
      ]
    }
  }
}
