# Repository Health Configuration for Generic Repositories
# This defines health scoring for generic/library repositories
# Total: 88 points (lighter requirements than standards repositories)

locals {
  generic_config_metadata = {
    name              = "Repository Type Generic Health Configuration"
    description       = "Health scoring for generic libraries and projects"
    version           = "04.00.03"
    last_updated      = "2026-02-27"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type   = "generic"
    format            = "terraform"
    enterprise_ready  = true
  }

  generic_repo_health_metadata = {
    name           = "Generic Repository Health Configuration"
    description    = "Health scoring for generic libraries and projects"
    effective_date = "2026-02-27T00:00:00Z"
    maintainer     = "Moko Consulting"
    version        = "1.0.0"
    schema_version = "1.0"
  }

  generic_scoring = {
    # Categories: CI/CD (15) + Docs (16) + Folders (10) + Workflows (10) + 
    # Issue Templates (5) + Security (12) + Repo Settings (10) + Deployment (10) = 88
    total_points = 88
  }

  generic_categories = {
    ci_cd_status = {
      id          = "ci-cd-status"
      name        = "CI/CD Status"
      description = "Continuous integration health"
      max_points  = 15
      enabled     = true
    }

    required_documentation = {
      id          = "required-documentation"
      name        = "Required Documentation"
      description = "Core documentation files"
      max_points  = 16
      enabled     = true
    }

    required_folders = {
      id          = "required-folders"
      name        = "Required Folders"
      description = "Standard directory structure"
      max_points  = 10
      enabled     = true
    }

    workflows = {
      id          = "workflows"
      name        = "Workflows"
      description = "Basic GitHub Actions workflows"
      max_points  = 10
      enabled     = true
    }

    issue_templates = {
      id          = "issue-templates"
      name        = "Issue Templates"
      description = "Issue and PR templates"
      max_points  = 5
      enabled     = true
    }

    security = {
      id          = "security"
      name        = "Security"
      description = "Security scanning basics"
      max_points  = 12
      enabled     = true
    }

    repository_settings = {
      id          = "repository-settings"
      name        = "Repository Settings"
      description = "GitHub repository configuration"
      max_points  = 10
      enabled     = true
    }

    deployment_secrets = {
      id          = "deployment-secrets"
      name        = "Deployment Secrets"
      description = "Basic deployment configuration"
      max_points  = 10
      enabled     = true
    }
  }

  generic_thresholds = {
    excellent = {
      level          = "excellent"
      min_percentage = 90
      max_percentage = 100
      indicator      = "✅"
      description    = "Production-ready"
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
      description    = "Improvements required"
    }

    poor = {
      level          = "poor"
      min_percentage = 0
      max_percentage = 49
      indicator      = "❌"
      description    = "Critical issues"
    }
  }

  # CI/CD Checks (15 points)
  generic_ci_cd_checks = {
    ci_workflow_present = {
      id          = "ci-workflow-present"
      name        = "CI workflow present"
      description = "Check if .github/workflows/ci.yml or similar exists"
      points      = 5
      check_type  = "workflow-exists"
      category    = "ci-cd-status"
      required    = true
      remediation = "Add CI workflow from templates"
      parameters = {
        workflow_paths = [".github/workflows/ci.yml", ".github/workflows/build.yml"]
        type          = "path"
      }
    }

    ci_workflow_passing = {
      id          = "ci-workflow-passing"
      name        = "CI workflow passing"
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

  # Documentation Checks (16 points) - same as standards
  generic_documentation_checks = {
    readme_present = {
      id          = "readme-present"
      name        = "README.md present"
      description = "Repository has a README.md file"
      points      = 3
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create README.md"
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
      remediation = "Create CONTRIBUTING.md"
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
      remediation = "Add CODE_OF_CONDUCT.md"
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
      remediation = "Create SECURITY.md"
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

  # Folder Checks (10 points) - same as standards
  generic_folder_checks = {
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
      remediation = "Create scripts/ directory"
      parameters = {
        directory_path = "scripts"
      }
    }

    override_config = {
      id          = "override-config"
      name        = "Override configuration in .github/"
      description = "Check for .github/override.tf for repository-specific customization"
      points      = 0
      check_type  = "file-exists"
      category    = "required-folders"
      required    = false
      remediation = "Create .github/override.tf for repository-specific customization"
      parameters = {
        file_path = ".github/override.tf"
      }
    }
  }

  # Security Checks (12 points) - lighter than standards
  generic_security_checks = {
    dependabot_present = {
      id          = "dependabot-present"
      name        = "Dependabot configuration present"
      description = "Check for .github/dependabot.yml"
      points      = 5
      check_type  = "file-exists"
      category    = "security"
      required    = true
      remediation = "Add .github/dependabot.yml"
      parameters = {
        file_path = ".github/dependabot.yml"
      }
    }

    security_workflow = {
      id          = "security-workflow"
      name        = "Security scanning workflow"
      description = "CodeQL or security scanning workflow present"
      points      = 7
      check_type  = "workflow-exists"
      category    = "security"
      required    = true
      remediation = "Add security scanning workflow"
      parameters = {
        workflow_paths = [".github/workflows/codeql-analysis.yml", ".github/workflows/security-scan.yml"]
      }
    }
  }

  # Workflow Checks (10 points) - simpler than standards
  generic_workflows_checks = {
    ci_workflow = {
      id          = "ci-workflow"
      name        = "CI Workflow"
      description = "Check for CI workflow"
      points      = 5
      check_type  = "file-exists"
      category    = "workflows"
      required    = true
      remediation = "Add CI workflow"
      parameters = {
        file_path = ".github/workflows/ci.yml"
      }
    }

    code_quality_workflow = {
      id          = "code-quality-workflow"
      name        = "Code Quality Workflow"
      description = "Check for code quality workflow"
      points      = 3
      check_type  = "file-exists"
      category    = "workflows"
      required    = false
      remediation = "Add code quality workflow"
      parameters = {
        file_path = ".github/workflows/code-quality.yml"
      }
    }

    release_workflow = {
      id          = "release-workflow"
      name        = "Release Workflow"
      description = "Check for release workflow"
      points      = 2
      check_type  = "file-exists"
      category    = "workflows"
      required    = false
      remediation = "Add release workflow"
      parameters = {
        file_path = ".github/workflows/release.yml"
      }
    }
  }

  # Issue Template Checks (5 points) - same as standards
  generic_issue_template_checks = {
    issue_template_directory = {
      id          = "issue-template-directory"
      name        = "Issue Template Directory"
      description = "Check for .github/ISSUE_TEMPLATE directory"
      points      = 1
      check_type  = "directory-exists"
      category    = "issue-templates"
      required    = true
      remediation = "Create .github/ISSUE_TEMPLATE directory"
      parameters = {
        directory_path = ".github/ISSUE_TEMPLATE"
      }
    }

    bug_report_template = {
      id          = "bug-report-template"
      name        = "Bug Report Template"
      description = "Check for bug report issue template"
      points      = 2
      check_type  = "file-exists"
      category    = "issue-templates"
      required    = true
      remediation = "Add bug_report.md template"
      parameters = {
        file_path = ".github/ISSUE_TEMPLATE/bug_report.md"
      }
    }

    feature_request_template = {
      id          = "feature-request-template"
      name        = "Feature Request Template"
      description = "Check for feature request issue template"
      points      = 2
      check_type  = "file-exists"
      category    = "issue-templates"
      required    = true
      remediation = "Add feature_request.md template"
      parameters = {
        file_path = ".github/ISSUE_TEMPLATE/feature_request.md"
      }
    }
  }

  # Repository Settings Checks (10 points) - same as standards
  generic_repository_settings_checks = {
    branch_protection_enabled = {
      id          = "branch-protection-enabled"
      name        = "Branch Protection Enabled"
      description = "Check if branch protection is enabled"
      points      = 5
      check_type  = "api-check"
      category    = "repository-settings"
      required    = true
      remediation = "Enable branch protection"
      parameters = {
        branch    = "main"
        api_path  = "/repos/{owner}/{repo}/branches/{branch}/protection"
        check_for = "enabled"
      }
    }

    required_status_checks = {
      id          = "required-status-checks"
      name        = "Required Status Checks"
      description = "Check if required status checks are configured"
      points      = 3
      check_type  = "api-check"
      category    = "repository-settings"
      required    = true
      remediation = "Configure required status checks"
      parameters = {
        branch    = "main"
        api_path  = "/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks"
        check_for = "contexts"
      }
    }

    require_pull_request_reviews = {
      id          = "require-pull-request-reviews"
      name        = "Require Pull Request Reviews"
      description = "Check if PR reviews are required"
      points      = 2
      check_type  = "api-check"
      category    = "repository-settings"
      required    = false
      remediation = "Enable required reviews"
      parameters = {
        branch    = "main"
        api_path  = "/repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews"
        check_for = "required_approving_review_count"
      }
    }
  }

  # Deployment Secrets Checks (10 points) - lighter than standards
  generic_deployment_secrets_checks = {
    github_token_available = {
      id          = "github-token-available"
      name        = "GITHUB_TOKEN Available"
      description = "Check if GITHUB_TOKEN is configured"
      points      = 5
      check_type  = "secret-exists"
      category    = "deployment-secrets"
      required    = true
      remediation = "GITHUB_TOKEN is automatically provided"
      parameters = {
        secret_name   = "GITHUB_TOKEN"
        scope         = "automatic"
        documentation = "Automatically provided by GitHub Actions"
      }
    }

    deployment_secrets_documented = {
      id          = "deployment-secrets-documented"
      name        = "Secrets Documented"
      description = "Check if secrets are documented"
      points      = 5
      check_type  = "content-pattern"
      category    = "deployment-secrets"
      required    = false
      remediation = "Document required secrets in README.md"
      parameters = {
        file_paths = ["README.md", "docs/deployment.md"]
        pattern    = "(?i)(secret|token|credential)"
      }
    }
  }
}

# Output configuration for generic repositories
output "generic_repo_health_config" {
  description = "Complete repository health configuration for generic repositories"
  value = {
    metadata   = local.generic_repo_health_metadata
    scoring    = local.generic_scoring
    categories = local.generic_categories
    thresholds = local.generic_thresholds
    checks = merge(
      local.generic_ci_cd_checks,
      local.generic_documentation_checks,
      local.generic_folder_checks,
      local.generic_security_checks,
      local.generic_workflows_checks,
      local.generic_issue_template_checks,
      local.generic_repository_settings_checks,
      local.generic_deployment_secrets_checks
    )
  }
}
