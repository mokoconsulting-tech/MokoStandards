/**
 * Default Repository Structure Definition
 * Default repository structure applicable to all repository types with minimal requirements
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0
 * Schema Version: 1.0
 */

locals {
  repository_structure = {
    metadata = {
      name             = "Default Repository Structure"
      description      = "Default repository structure applicable to all repository types with minimal requirements"
      repository_type  = "library"
      platform         = "multi-platform"
      last_updated     = "2026-01-16T00:00:00Z"
      maintainer       = "Moko Consulting"
      version          = "1.0"
      schema_version   = "1.0"
    }

    root_files = [
      {
        name                  = "README.md"
        extension             = "md"
        description           = "Project overview and documentation"
        requirement_status    = "required"
        audience              = "general"
        source_path           = "templates/docs/required"
        source_filename       = "template-README.md"
        source_type           = "template"
        destination_path      = "."
        destination_filename  = "README.md"
        create_path           = false
        template              = "templates/docs/required/template-README.md"
      },
      {
        name                  = "LICENSE"
        extension             = ""
        description           = "License file (GPL-3.0-or-later)"
        requirement_status    = "required"
        audience              = "general"
        source_path           = "templates/licenses"
        source_filename       = "GPL-3.0"
        source_type           = "template"
        destination_path      = "."
        destination_filename  = "LICENSE"
        create_path           = false
        template              = "templates/licenses/GPL-3.0"
      },
      {
        name                  = "CHANGELOG.md"
        extension             = "md"
        description           = "Version history and changes"
        requirement_status    = "required"
        audience              = "general"
        source_path           = "templates/docs/required"
        source_filename       = "template-CHANGELOG.md"
        source_type           = "template"
        destination_path      = "."
        destination_filename  = "CHANGELOG.md"
        create_path           = false
        template              = "templates/docs/required/template-CHANGELOG.md"
      },
      {
        name                  = "CONTRIBUTING.md"
        extension             = "md"
        description           = "Contribution guidelines"
        requirement_status    = "required"
        audience              = "contributor"
        source_path           = "templates/docs/required"
        source_filename       = "template-CONTRIBUTING.md"
        source_type           = "template"
        destination_path      = "."
        destination_filename  = "CONTRIBUTING.md"
        create_path           = false
        template              = "templates/docs/required/template-CONTRIBUTING.md"
      },
      {
        name                  = "SECURITY.md"
        extension             = "md"
        description           = "Security policy and vulnerability reporting"
        requirement_status    = "required"
        audience              = "general"
        source_path           = "templates/docs/required"
        source_filename       = "template-SECURITY.md"
        source_type           = "template"
        destination_path      = "."
        destination_filename  = "SECURITY.md"
        create_path           = false
        template              = "templates/docs/required/template-SECURITY.md"
      },
      {
        name                  = "CODE_OF_CONDUCT.md"
        extension             = "md"
        description           = "Community code of conduct"
        requirement_status    = "required"
        always_overwrite      = true
        audience              = "contributor"
        source_path           = "templates/docs/extra"
        source_filename       = "template-CODE_OF_CONDUCT.md"
        source_type           = "template"
        destination_path      = "."
        destination_filename  = "CODE_OF_CONDUCT.md"
        create_path           = false
        template              = "templates/docs/extra/template-CODE_OF_CONDUCT.md"
      },
      {
        name                  = "ROADMAP.md"
        extension             = "md"
        description           = "Project roadmap with version goals and milestones"
        requirement_status    = "suggested"
        audience              = "general"
        source_path           = "templates/docs/extra"
        source_filename       = "template-ROADMAP.md"
        source_type           = "template"
        destination_path      = "."
        destination_filename  = "ROADMAP.md"
        create_path           = false
        template              = "templates/docs/extra/template-ROADMAP.md"
      },
      {
        name                  = ".gitignore"
        extension             = "gitignore"
        description           = "Git ignore patterns"
        requirement_status    = "required"
        always_overwrite      = false
        audience              = "developer"
      },
      {
        name                  = ".gitattributes"
        extension             = "gitattributes"
        description           = "Git attributes configuration"
        requirement_status    = "required"
        audience              = "developer"
      },
      {
        name                  = ".editorconfig"
        extension             = "editorconfig"
        description           = "Editor configuration for consistent coding style"
        requirement_status    = "required"
        always_overwrite      = false
        audience              = "developer"
      },
      {
        name                  = "Makefile"
        description           = "Build automation"
        requirement_status    = "required"
        always_overwrite      = true
        audience              = "developer"
        source_path           = "templates/makefiles"
        source_filename       = "Makefile.generic.template"
        source_type           = "template"
        destination_path      = "."
        destination_filename  = "Makefile"
        create_path           = false
        template              = "templates/makefiles/Makefile.generic.template"
      }
    ]

    directories = [
      {
        name                = "docs"
        path                = "docs"
        description         = "Documentation directory"
        requirement_status  = "required"
        purpose             = "Contains comprehensive project documentation"
        files = [
          {
            name                = "index.md"
            extension           = "md"
            description         = "Documentation index"
            requirement_status  = "suggested"
            template            = "templates/docs/index.md"
          },
          {
            name                  = "INSTALLATION.md"
            extension             = "md"
            description           = "Installation and setup instructions"
            requirement_status    = "required"
            audience              = "general"
            source_path           = "templates/docs/required"
            source_filename       = "template-INSTALLATION.md"
            source_type           = "template"
            destination_path      = "docs"
            destination_filename  = "INSTALLATION.md"
            create_path           = true
            template              = "templates/docs/required/template-INSTALLATION.md"
          },
          {
            name                = "API.md"
            extension           = "md"
            description         = "API documentation"
            requirement_status  = "suggested"
          },
          {
            name                = "ARCHITECTURE.md"
            extension           = "md"
            description         = "Architecture documentation"
            requirement_status  = "suggested"
          }
        ]
      },
      {
        name                = "scripts"
        path                = "scripts"
        description         = "Build and automation scripts"
        requirement_status  = "required"
        purpose             = "Contains scripts for building, testing, and deploying"
        files = [
          {
            name                = "validate_structure.sh"
            extension           = "sh"
            description         = "Repository structure validation script"
            requirement_status  = "suggested"
            template            = "templates/scripts/validate/structure.sh"
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
        name                = "src"
        path                = "src"
        description         = "Source code directory"
        requirement_status  = "required"
        purpose             = "Contains application source code"
      },
      {
        name                = "tests"
        path                = "tests"
        description         = "Test files"
        requirement_status  = "suggested"
        purpose             = "Contains unit tests, integration tests, and test fixtures"
        subdirectories = [
          {
            name                = "unit"
            path                = "tests/unit"
            description         = "Unit tests"
            requirement_status  = "suggested"
          },
          {
            name                = "integration"
            path                = "tests/integration"
            description         = "Integration tests"
            requirement_status  = "optional"
          }
        ]
      },
      {
        name                = ".github"
        path                = ".github"
        description         = "GitHub-specific configuration"
        requirement_status  = "required"
        purpose             = "Contains GitHub Actions workflows, issue templates, etc."
        subdirectories = [
          {
            name                = "workflows"
            path                = ".github/workflows"
            description         = "GitHub Actions workflows"
            requirement_status  = "required"
            files = [
              {
                name                  = "ci.yml"
                extension             = "yml"
                description           = "Continuous integration workflow"
                requirement_status    = "required"
                always_overwrite      = true
                source_path           = "templates/workflows/generic"
                source_filename       = "ci.yml.template"
                source_type           = "template"
                destination_path      = ".github/workflows"
                destination_filename  = "ci.yml"
                create_path           = true
                template              = "templates/workflows/generic/ci.yml.template"
              },
              {
                name                  = "test.yml"
                extension             = "yml"
                description           = "Comprehensive testing workflow"
                requirement_status    = "optional"
                always_overwrite      = true
                source_path           = "templates/workflows/generic"
                source_filename       = "test.yml.template"
                source_type           = "template"
                destination_path      = ".github/workflows"
                destination_filename  = "test.yml"
                create_path           = true
                template              = "templates/workflows/generic/test.yml.template"
              },
              {
                name                  = "code-quality.yml"
                extension             = "yml"
                description           = "Code quality and linting workflow"
                requirement_status    = "required"
                always_overwrite      = true
                source_path           = "templates/workflows/generic"
                source_filename       = "code-quality.yml.template"
                source_type           = "template"
                destination_path      = ".github/workflows"
                destination_filename  = "code-quality.yml"
                create_path           = true
                template              = "templates/workflows/generic/code-quality.yml.template"
              },
              {
                name                  = "codeql-analysis.yml"
                extension             = "yml"
                description           = "CodeQL security analysis workflow"
                requirement_status    = "required"
                always_overwrite      = true
                source_path           = "templates/workflows/generic"
                source_filename       = "codeql-analysis.yml.template"
                source_type           = "template"
                destination_path      = ".github/workflows"
                destination_filename  = "codeql-analysis.yml"
                create_path           = true
                template              = "templates/workflows/generic/codeql-analysis.yml.template"
              },
              {
                name                  = "deploy.yml"
                extension             = "yml"
                description           = "Deployment workflow"
                requirement_status    = "optional"
                always_overwrite      = true
                source_path           = "templates/workflows/generic"
                source_filename       = "deploy.yml.template"
                source_type           = "template"
                destination_path      = ".github/workflows"
                destination_filename  = "deploy.yml"
                create_path           = true
                template              = "templates/workflows/generic/deploy.yml.template"
              },
              {
                name                  = "repo-health.yml"
                extension             = "yml"
                description           = "Repository health monitoring"
                requirement_status    = "required"
                always_overwrite      = true
                source_path           = "templates/workflows/generic"
                source_filename       = "repo_health.yml.template"
                source_type           = "template"
                destination_path      = ".github/workflows"
                destination_filename  = "repo-health.yml"
                create_path           = true
                template              = "templates/workflows/generic/repo_health.yml.template"
              },
              {
                name                  = "release-cycle.yml"
                extension             = "yml"
                description           = "Release management workflow with automated release flow"
                requirement_status    = "required"
                always_overwrite      = true
                source_path           = ".github/workflows"
                source_filename       = "release-cycle.yml"
                source_type           = "copy"
                destination_path      = ".github/workflows"
                destination_filename  = "release-cycle.yml"
                create_path           = true
                template              = ".github/workflows/release-cycle.yml"
              },
              {
                name                  = "standards-compliance.yml"
                extension             = "yml"
                description           = "MokoStandards compliance validation"
                requirement_status    = "required"
                always_overwrite      = true
                source_path           = ".github/workflows"
                source_filename       = "standards-compliance.yml"
                source_type           = "copy"
                destination_path      = ".github/workflows"
                destination_filename  = "standards-compliance.yml"
                create_path           = true
                template              = ".github/workflows/standards-compliance.yml"
              }
            ]
          }
        ]
      },
      {
        name                = "node_modules"
        path                = "node_modules"
        description         = "Node.js dependencies (generated)"
        requirement_status  = "not-allowed"
        purpose             = "Generated directory that should not be committed"
      },
      {
        name                = "vendor"
        path                = "vendor"
        description         = "PHP dependencies (generated)"
        requirement_status  = "not-allowed"
        purpose             = "Generated directory that should not be committed"
      },
      {
        name                = "build"
        path                = "build"
        description         = "Build artifacts (generated)"
        requirement_status  = "not-allowed"
        purpose             = "Generated directory that should not be committed"
      },
      {
        name                = "dist"
        path                = "dist"
        description         = "Distribution files (generated)"
        requirement_status  = "not-allowed"
        purpose             = "Generated directory that should not be committed"
      }
    ]

    repository_requirements = {
      secrets = [
        {
          name        = "GH_TOKEN"
          description = "Org-level GitHub PAT — configure in org Actions secrets"
          required    = true
          scope       = "organisation"
          used_in     = "GitHub Actions workflows"
        },
        {
          name        = "CODECOV_TOKEN"
          description = "Codecov upload token for code coverage reporting"
          required    = false
          scope       = "repository"
          used_in     = "CI workflow code coverage step"
        }
      ]

      variables = [
        {
          name          = "NODE_VERSION"
          description   = "Node.js version for CI/CD"
          default_value = "18"
          required      = false
          scope         = "repository"
        },
        {
          name          = "PYTHON_VERSION"
          description   = "Python version for CI/CD"
          default_value = "3.9"
          required      = false
          scope         = "repository"
        }
      ]

      branch_protections = [
        {
          branch_pattern          = "main"
          require_pull_request    = true
          required_approvals      = 1
          require_code_owner_review = false
          dismiss_stale_reviews   = true
          require_status_checks   = true
          required_status_checks  = ["ci", "code-quality"]
          enforce_admins          = false
          restrict_pushes         = true
        },
        {
          branch_pattern          = "master"
          require_pull_request    = true
          required_approvals      = 1
          require_code_owner_review = false
          dismiss_stale_reviews   = true
          require_status_checks   = true
          required_status_checks  = ["ci"]
          enforce_admins          = false
          restrict_pushes         = true
        }
      ]

      repository_settings = {
        has_issues            = true
        has_projects          = true
        has_wiki              = false
        has_discussions       = false
        allow_merge_commit    = true
        allow_squash_merge    = true
        allow_rebase_merge    = false
        delete_branch_on_merge = true
        allow_auto_merge      = false
      }

      labels = [
        {
          name        = "bug"
          color       = "d73a4a"
          description = "Something isn't working"
        },
        {
          name        = "enhancement"
          color       = "a2eeef"
          description = "New feature or request"
        },
        {
          name        = "documentation"
          color       = "0075ca"
          description = "Improvements or additions to documentation"
        },
        {
          name        = "security"
          color       = "ee0701"
          description = "Security vulnerability or concern"
        }
      ]
    }
  }
}
