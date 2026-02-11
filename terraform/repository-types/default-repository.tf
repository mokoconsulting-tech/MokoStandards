# Default Repository Structure Definition
# Converted from scripts/definitions/default-repository.xml
# This defines the standard structure for generic repositories


locals {
  # Metadata for this configuration
  config_metadata = {
    name            = "Repository Type Default Repository"
    description     = "Default repository structure and configuration schema definitions"
    version         = "2.0.0"
    last_updated    = "2026-01-28"
    maintainer      = "MokoStandards Team"
    schema_version  = "2.0"
    repository_url  = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type = "standards"
    format          = "terraform"
  }
}

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
      name               = "README.md"
      extension          = "md"
      description        = "Project documentation and overview"
      requirement_status = "required"
      always_overwrite   = false
      audience           = "general"
      validation_rules   = []
    }

    license = {
      name               = "LICENSE"
      extension          = ""
      description        = "Repository license"
      requirement_status = "required"
      always_overwrite   = false
      audience           = "general"
      validation_rules   = []
    }

    changelog = {
      name               = "CHANGELOG.md"
      extension          = "md"
      description        = "Version history and changes"
      requirement_status = "suggested"
      always_overwrite   = false
      audience           = "developer"
      validation_rules   = []
    }

    contributing = {
      name               = "CONTRIBUTING.md"
      extension          = "md"
      description        = "Contribution guidelines"
      requirement_status = "suggested"
      always_overwrite   = false
      audience           = "contributor"
      validation_rules   = []
    }

    code_of_conduct = {
      name               = "CODE_OF_CONDUCT.md"
      extension          = "md"
      description        = "Code of conduct for contributors"
      requirement_status = "suggested"
      always_overwrite   = false
      audience           = "contributor"
      validation_rules   = []
    }

    security = {
      name               = "SECURITY.md"
      extension          = "md"
      description        = "Security policy and vulnerability reporting"
      requirement_status = "required"
      always_overwrite   = false
      audience           = "general"
      validation_rules   = []
    }

    gitignore = {
      name               = ".gitignore"
      extension          = ""
      description        = "Git ignore patterns"
      requirement_status = "required"
      always_overwrite   = false
      audience           = "developer"
      validation_rules   = []
    }

    gitattributes = {
      name               = ".gitattributes"
      extension          = ""
      description        = "Git attributes configuration"
      requirement_status = "optional"
      always_overwrite   = false
      audience           = "developer"
      validation_rules   = []
    }

    editorconfig = {
      name               = ".editorconfig"
      extension          = ""
      description        = "Editor configuration"
      requirement_status = "suggested"
      always_overwrite   = false
      audience           = "developer"
      validation_rules   = []
    }
  }

  # Directory structure
  default_directories = {
    github = {
      name               = ".github"
      path               = ".github"
      description        = "GitHub configuration and templates"
      requirement_status = "required"
      purpose            = "GitHub-specific configuration files"
      subdirectories = {
        workflows = {
          name               = "workflows"
          path               = ".github/workflows"
          description        = "GitHub Actions workflows"
          requirement_status = "required"
          purpose            = "CI/CD automation"
        }

        issue_templates = {
          name               = "ISSUE_TEMPLATE"
          path               = ".github/ISSUE_TEMPLATE"
          description        = "Issue templates"
          requirement_status = "suggested"
          purpose            = "Standardized issue reporting"
        }

        pull_request_template = {
          name               = "PULL_REQUEST_TEMPLATE"
          path               = ".github/PULL_REQUEST_TEMPLATE"
          description        = "Pull request templates"
          requirement_status = "suggested"
          purpose            = "Standardized PR descriptions"
        }
      }
    }

    logs = {
      name               = "logs"
      path               = "logs"
      description        = "Application and workflow logs"
      requirement_status = "required"
      purpose            = "Centralized logging for scripts, automation, and copilot runs"
      subdirectories = {
        automation = {
          name               = "automation"
          path               = "logs/automation"
          description        = "Logs from automation scripts"
          requirement_status = "required"
          purpose            = "Automation script execution logs"
        }

        validation = {
          name               = "validation"
          path               = "logs/validation"
          description        = "Logs from validation scripts"
          requirement_status = "required"
          purpose            = "Validation script execution logs"
        }

        release = {
          name               = "release"
          path               = "logs/release"
          description        = "Logs from release processes"
          requirement_status = "required"
          purpose            = "Release script execution logs"
        }

        copilot = {
          name               = "copilot"
          path               = "logs/copilot"
          description        = "Logs from GitHub Copilot agent runs"
          requirement_status = "required"
          purpose            = "Copilot agent session logs"
        }

        maintenance = {
          name               = "maintenance"
          path               = "logs/maintenance"
          description        = "Logs from maintenance scripts"
          requirement_status = "required"
          purpose            = "Maintenance script execution logs"
        }
      }
    }

    docs = {
      name               = "docs"
      path               = "docs"
      description        = "Documentation files"
      requirement_status = "suggested"
      purpose            = "Project documentation"
      subdirectories     = {}
    }

    tests = {
      name               = "tests"
      path               = "tests"
      description        = "Test files"
      requirement_status = "suggested"
      purpose            = "Automated testing"
      subdirectories     = {}
    }

    scripts = {
      name               = "scripts"
      path               = "scripts"
      description        = "Utility scripts"
      requirement_status = "required"
      purpose            = "Automation and utility scripts including version management"
      subdirectories     = {
        lib = {
          name               = "lib"
          path               = "scripts/lib"
          description        = "Shared library modules"
          requirement_status = "required"
          purpose            = "Common utilities and version detection logic"
        }
        automation = {
          name               = "automation"
          path               = "scripts/automation"
          description        = "Automation scripts"
          requirement_status = "required"
          purpose            = "Repository automation including version bump detection"
        }
        tests = {
          name               = "tests"
          path               = "scripts/tests"
          description        = "Script test suites"
          requirement_status = "suggested"
          purpose            = "Unit and integration tests for scripts"
        }
        maintenance = {
          name               = "maintenance"
          path               = "scripts/maintenance"
          description        = "Maintenance and cleanup scripts"
          requirement_status = "required"
          purpose            = "Branch cleanup and repository maintenance automation"
        }
        release = {
          name               = "release"
          path               = "scripts/release"
          description        = "Release management scripts"
          requirement_status = "required"
          purpose            = "Version release and packaging automation"
        }
      }
      required_files = {
        version_bump_detector = {
          name               = "version_bump_detector.py"
          path               = "scripts/lib/version_bump_detector.py"
          description        = "Semantic version bump detection library"
          requirement_status = "required"
          source_template    = "scripts/lib/version_bump_detector.py"
          always_overwrite   = true
          purpose            = "Detect version bump type from PR/issue templates"
        }
        detect_version_bump = {
          name               = "detect_version_bump.py"
          path               = "scripts/automation/detect_version_bump.py"
          description        = "Version bump detection and application CLI"
          requirement_status = "required"
          source_template    = "scripts/automation/detect_version_bump.py"
          always_overwrite   = true
          purpose            = "Enterprise-grade version bump automation"
        }
        common_py = {
          name               = "common.py"
          path               = "scripts/lib/common.py"
          description        = "Common Python utilities"
          requirement_status = "required"
          source_template    = "scripts/lib/common.py"
          always_overwrite   = false
          purpose            = "Shared utilities for Python scripts"
        }
        clean_old_branches = {
          name               = "clean_old_branches.py"
          path               = "scripts/maintenance/clean_old_branches.py"
          description        = "Branch cleanup and archival automation"
          requirement_status = "required"
          source_template    = "scripts/maintenance/clean_old_branches.py"
          always_overwrite   = true
          purpose            = "Identifies and cleans old Git branches"
        }
        release_version = {
          name               = "release_version.py"
          path               = "scripts/maintenance/release_version.py"
          description        = "Version release and CHANGELOG management"
          requirement_status = "required"
          source_template    = "scripts/maintenance/release_version.py"
          always_overwrite   = true
          purpose            = "Manages version releases in CHANGELOG.md"
        }
        unified_release = {
          name               = "unified_release.py"
          path               = "scripts/release/unified_release.py"
          description        = "Unified release orchestration tool"
          requirement_status = "required"
          source_template    = "scripts/release/unified_release.py"
          always_overwrite   = true
          purpose            = "Consolidates all release functionality"
        }
        detect_platform = {
          name               = "detect_platform.py"
          path               = "scripts/release/detect_platform.py"
          description        = "Platform and project type detection"
          requirement_status = "required"
          source_template    = "scripts/release/detect_platform.py"
          always_overwrite   = true
          purpose            = "Detects project platform for release automation"
        }
        package_extension = {
          name               = "package_extension.py"
          path               = "scripts/release/package_extension.py"
          description        = "Extension packaging automation"
          requirement_status = "required"
          source_template    = "scripts/release/package_extension.py"
          always_overwrite   = true
          purpose            = "Packages extensions for distribution"
        }
      }
    }

    src = {
      name               = "src"
      path               = "src"
      description        = "Source code"
      requirement_status = "optional"
      purpose            = "Main source code directory"
      subdirectories     = {}
    }
  }
}

# Output the repository structure configuration
output "default_repository_structure" {
  description = "Default repository structure definition"
  value = {
    metadata    = local.default_repo_metadata
    root_files  = local.default_root_files
    directories = local.default_directories
  }
}
