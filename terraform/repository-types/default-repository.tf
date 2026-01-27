# Default Repository Structure Definition
# Converted from scripts/definitions/default-repository.xml
# This defines the standard structure for generic repositories

locals {
  default_repo_metadata = {
    name            = "Default Repository Structure"
    description     = "Standard structure for generic repositories in MokoStandards"
    repository_type = "library"
    platform        = "multi-platform"
    last_updated    = "2026-01-16T00:00:00Z"
    maintainer      = "MokoStandards Team"
    schema_version  = "1.0"
  }

  # Root files expected at repository root
  default_root_files = {
    readme = {
      name                = "README.md"
      extension           = "md"
      description         = "Project documentation and overview"
      requirement_status  = "required"
      always_overwrite    = false
      audience            = "general"
      validation_rules    = []
    }

    license = {
      name                = "LICENSE"
      extension           = ""
      description         = "Repository license"
      requirement_status  = "required"
      always_overwrite    = false
      audience            = "general"
      validation_rules    = []
    }

    changelog = {
      name                = "CHANGELOG.md"
      extension           = "md"
      description         = "Version history and changes"
      requirement_status  = "suggested"
      always_overwrite    = false
      audience            = "developer"
      validation_rules    = []
    }

    contributing = {
      name                = "CONTRIBUTING.md"
      extension           = "md"
      description         = "Contribution guidelines"
      requirement_status  = "suggested"
      always_overwrite    = false
      audience            = "contributor"
      validation_rules    = []
    }

    code_of_conduct = {
      name                = "CODE_OF_CONDUCT.md"
      extension           = "md"
      description         = "Code of conduct for contributors"
      requirement_status  = "suggested"
      always_overwrite    = false
      audience            = "contributor"
      validation_rules    = []
    }

    security = {
      name                = "SECURITY.md"
      extension           = "md"
      description         = "Security policy and vulnerability reporting"
      requirement_status  = "required"
      always_overwrite    = false
      audience            = "general"
      validation_rules    = []
    }

    gitignore = {
      name                = ".gitignore"
      extension           = ""
      description         = "Git ignore patterns"
      requirement_status  = "required"
      always_overwrite    = false
      audience            = "developer"
      validation_rules    = []
    }

    gitattributes = {
      name                = ".gitattributes"
      extension           = ""
      description         = "Git attributes configuration"
      requirement_status  = "optional"
      always_overwrite    = false
      audience            = "developer"
      validation_rules    = []
    }

    editorconfig = {
      name                = ".editorconfig"
      extension           = ""
      description         = "Editor configuration"
      requirement_status  = "suggested"
      always_overwrite    = false
      audience            = "developer"
      validation_rules    = []
    }
  }

  # Directory structure
  default_directories = {
    github = {
      name                = ".github"
      path                = ".github"
      description         = "GitHub configuration and templates"
      requirement_status  = "required"
      purpose             = "GitHub-specific configuration files"
      subdirectories = {
        workflows = {
          name                = "workflows"
          path                = ".github/workflows"
          description         = "GitHub Actions workflows"
          requirement_status  = "required"
          purpose             = "CI/CD automation"
        }
        
        issue_templates = {
          name                = "ISSUE_TEMPLATE"
          path                = ".github/ISSUE_TEMPLATE"
          description         = "Issue templates"
          requirement_status  = "suggested"
          purpose             = "Standardized issue reporting"
        }

        pull_request_template = {
          name                = "PULL_REQUEST_TEMPLATE"
          path                = ".github/PULL_REQUEST_TEMPLATE"
          description         = "Pull request templates"
          requirement_status  = "suggested"
          purpose             = "Standardized PR descriptions"
        }
      }
    }

    docs = {
      name                = "docs"
      path                = "docs"
      description         = "Documentation files"
      requirement_status  = "suggested"
      purpose             = "Project documentation"
      subdirectories      = {}
    }

    tests = {
      name                = "tests"
      path                = "tests"
      description         = "Test files"
      requirement_status  = "suggested"
      purpose             = "Automated testing"
      subdirectories      = {}
    }

    scripts = {
      name                = "scripts"
      path                = "scripts"
      description         = "Utility scripts"
      requirement_status  = "optional"
      purpose             = "Automation and utility scripts"
      subdirectories      = {}
    }

    src = {
      name                = "src"
      path                = "src"
      description         = "Source code"
      requirement_status  = "optional"
      purpose             = "Main source code directory"
      subdirectories      = {}
    }
  }
}

# Output the repository structure configuration
output "default_repository_structure" {
  description = "Default repository structure definition"
  value = {
    metadata     = local.default_repo_metadata
    root_files   = local.default_root_files
    directories  = local.default_directories
  }
}
