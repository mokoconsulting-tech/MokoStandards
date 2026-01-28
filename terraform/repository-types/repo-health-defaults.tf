# Repository Health Default Configuration
# Converted from schemas/repo-health-default.xml
# This defines the default repository health scoring and validation configuration


locals {
  # Metadata for this configuration
  config_metadata = {
    name            = "Repository Type Repo Health Defaults"
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
  repo_health_metadata = {
    name           = "MokoStandards Repository Health Default Configuration"
    description    = "Default repository health scoring and validation configuration for Moko Consulting projects"
    effective_date = "2026-01-08T00:00:00Z"
    maintainer     = "Moko Consulting"
    repository_url = "https://github.com/mokoconsulting-tech/MokoStandards"
    version        = "1.0.0"
    schema_version = "1.0"
  }

  scoring = {
    # TODO: Calculate total_points dynamically from sum of all check points
    # Currently hardcoded to match original XML schema value
    total_points = 103
  }

  categories = {
    ci_cd_status = {
      id          = "ci-cd-status"
      name        = "CI/CD Status"
      description = "Continuous integration and deployment health"
      max_points  = 15
      enabled     = true
    }

    required_documentation = {
      id          = "required-documentation"
      name        = "Required Documentation"
      description = "Core documentation files presence and quality"
      max_points  = 16
      enabled     = true
    }

    required_folders = {
      id          = "required-folders"
      name        = "Required Folders"
      description = "Standard directory structure compliance"
      max_points  = 10
      enabled     = true
    }

    workflows = {
      id          = "workflows"
      name        = "Workflows"
      description = "GitHub Actions workflow completeness"
      max_points  = 12
      enabled     = true
    }

    issue_templates = {
      id          = "issue-templates"
      name        = "Issue Templates"
      description = "Issue and PR template availability"
      max_points  = 5
      enabled     = true
    }

    security = {
      id          = "security"
      name        = "Security"
      description = "Security scanning and vulnerability management"
      max_points  = 15
      enabled     = true
    }

    repository_settings = {
      id          = "repository-settings"
      name        = "Repository Settings"
      description = "GitHub repository configuration compliance"
      max_points  = 10
      enabled     = true
    }

    deployment_secrets = {
      id          = "deployment-secrets"
      name        = "Deployment Secrets"
      description = "Deployment configuration and secrets management"
      max_points  = 20
      enabled     = true
    }
  }

  thresholds = {
    excellent = {
      level          = "excellent"
      min_percentage = 90
      max_percentage = 100
      indicator      = "✅"
      description    = "Production-ready, fully compliant"
    }

    good = {
      level          = "good"
      min_percentage = 70
      max_percentage = 89
      indicator      = "⚠️"
      description    = "Minor improvements needed"
    }

    fair = {
      level          = "fair"
      min_percentage = 50
      max_percentage = 69
      indicator      = "🟡"
      description    = "Significant improvements required"
    }

    poor = {
      level          = "poor"
      min_percentage = 0
      max_percentage = 49
      indicator      = "❌"
      description    = "Critical issues, requires immediate attention"
    }
  }

  # CI/CD Status Checks (15 points)
  ci_cd_checks = {
    ci_workflow_present = {
      id          = "ci-workflow-present"
      name        = "CI workflow present and enabled"
      description = "Check if .github/workflows/ci.yml exists and is properly configured"
      points      = 5
      check_type  = "workflow-exists"
      category    = "ci-cd-status"
      required    = true
      remediation = "Add CI workflow from MokoStandards templates"
      parameters = {
        workflow_path = ".github/workflows/ci.yml"
        type          = "path"
      }
    }

    ci_workflow_passing = {
      id          = "ci-workflow-passing"
      name        = "CI workflow passing on main branch"
      description = "Verify latest CI run was successful"
      points      = 5
      check_type  = "workflow-passing"
      category    = "ci-cd-status"
      required    = true
      remediation = "Fix CI workflow failures"
      parameters = {
        workflow_name = "ci.yml"
        branch        = "main"
      }
    }

    build_status_badge = {
      id          = "build-status-badge"
      name        = "Build status badge in README"
      description = "README.md contains CI status badge"
      points      = 5
      check_type  = "content-pattern"
      category    = "ci-cd-status"
      required    = false
      remediation = "Add build status badge to README.md"
      parameters = {
        file_path = "README.md"
        pattern   = "\\[!\\[.*\\]\\(.*\\)\\]\\(.*\\)"
      }
    }
  }

  # Required Documentation Checks (16 points)
  documentation_checks = {
    readme_present = {
      id          = "readme-present"
      name        = "README.md present"
      description = "Repository has a README.md file"
      points      = 3
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create README.md from template"
      parameters = {
        file_path = "README.md"
      }
    }

    license_present = {
      id          = "license-present"
      name        = "LICENSE file present"
      description = "Repository has a LICENSE file"
      points      = 2
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Add LICENSE file"
      parameters = {
        file_path = "LICENSE"
      }
    }

    contributing_present = {
      id          = "contributing-present"
      name        = "CONTRIBUTING.md present"
      description = "Repository has contribution guidelines"
      points      = 2
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = false
      remediation = "Create CONTRIBUTING.md from template"
      parameters = {
        file_path = "CONTRIBUTING.md"
      }
    }

    changelog_present = {
      id          = "changelog-present"
      name        = "CHANGELOG.md present"
      description = "Repository maintains a changelog"
      points      = 2
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = false
      remediation = "Create CHANGELOG.md"
      parameters = {
        file_path = "CHANGELOG.md"
      }
    }

    code_of_conduct_present = {
      id          = "code-of-conduct-present"
      name        = "CODE_OF_CONDUCT.md present"
      description = "Repository has code of conduct"
      points      = 2
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = false
      remediation = "Add CODE_OF_CONDUCT.md from template"
      parameters = {
        file_path = "CODE_OF_CONDUCT.md"
      }
    }

    security_policy_present = {
      id          = "security-policy-present"
      name        = "SECURITY.md present"
      description = "Repository has security policy"
      points      = 3
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create SECURITY.md from template"
      parameters = {
        file_path = "SECURITY.md"
      }
    }

    docs_directory_present = {
      id          = "docs-directory-present"
      name        = "docs/ directory present"
      description = "Repository has documentation directory"
      points      = 2
      check_type  = "directory-exists"
      category    = "required-documentation"
      required    = false
      remediation = "Create docs/ directory"
      parameters = {
        directory_path = "docs"
      }
    }
  }

  # Required Folders Checks (10 points)
  folder_checks = {
    github_directory = {
      id          = "github-directory"
      name        = ".github/ directory present"
      description = "Repository has .github configuration"
      points      = 2
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = true
      remediation = "Create .github/ directory"
      parameters = {
        directory_path = ".github"
      }
    }

    workflows_directory = {
      id          = "workflows-directory"
      name        = ".github/workflows/ directory present"
      description = "Repository has workflows directory"
      points      = 3
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = true
      remediation = "Create .github/workflows/ directory"
      parameters = {
        directory_path = ".github/workflows"
      }
    }

    tests_directory = {
      id          = "tests-directory"
      name        = "tests/ or test/ directory present"
      description = "Repository has test directory"
      points      = 3
      check_type  = "directory-exists-any"
      category    = "required-folders"
      required    = false
      remediation = "Create tests/ directory"
      parameters = {
        directory_paths = ["tests", "test", "__tests__", "spec"]
      }
    }

    scripts_directory = {
      id          = "scripts-directory"
      name        = "scripts/ directory present"
      description = "Repository has scripts directory"
      points      = 2
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = false
      remediation = "Create scripts/ directory for automation"
      parameters = {
        directory_path = "scripts"
      }
    }
  }

  # Note: Additional check categories (workflows, issue_templates, security, 
  # repository_settings, deployment_secrets) are defined but checks are not
  # yet fully implemented. They require GitHub API integration.
  # TODO: Add remaining health checks for complete 103-point scoring
}

# Output all configuration for consumption by validation scripts
output "repo_health_config" {
  description = "Complete repository health configuration"
  value = {
    metadata   = local.repo_health_metadata
    scoring    = local.scoring
    categories = local.categories
    thresholds = local.thresholds
    checks = merge(
      local.ci_cd_checks,
      local.documentation_checks,
      local.folder_checks
      # TODO: Add workflows_checks, issue_template_checks, security_checks, etc.
    )
  }
}
