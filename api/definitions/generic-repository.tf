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
            description         = "GitHub Copilot custom instructions enforcing MokoStandards"
            requirement_status  = "required"
            always_overwrite    = true
            destination_path    = ".github"
            destination_filename = "copilot-instructions.md"
            template            = "templates/github/copilot-instructions.md.template"
          },
          {
            name                = "CLAUDE.md"
            extension           = "md"
            description         = "Claude AI assistant context enforcing MokoStandards"
            requirement_status  = "required"
            always_overwrite    = true
            destination_path    = ".github"
            destination_filename = "CLAUDE.md"
            template            = "templates/github/CLAUDE.md.template"
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
              }
            ]
          },
          {
            name                = "ISSUE_TEMPLATE"
            path                = ".github/ISSUE_TEMPLATE"
            description         = "GitHub issue templates"
            requirement_status  = "suggested"
          }
        ]
      }
    ]
  }
}
