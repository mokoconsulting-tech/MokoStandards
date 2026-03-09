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
