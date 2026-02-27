# Repository Health Default Configuration
# Converted from schemas/repo-health-default.xml
# This defines the default repository health scoring and validation configuration


locals {
  # Metadata for this configuration
  # Enterprise-ready: Includes audit logging, monitoring, and compliance features
  config_metadata = {
    name              = "Repository Type Repo Health Defaults"
    description       = "Default repository structure and configuration schema definitions"
    version           = "04.00.03"
    last_updated      = "2026-02-27"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type   = "standards"
    format            = "terraform"
    enterprise_ready  = true
    monitoring_enabled = true
    audit_logging     = true
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
    # Total points based on category max_points sum
    # Categories: CI/CD (15) + Docs (16) + Folders (10) + Workflows (12) + 
    # Issue Templates (5) + Security (15) + Repo Settings (10) + Deployment (20) = 103
    # All checks now implemented (completed 2026-02-27)
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

  # Security Checks (15 points)
  security_checks = {
    script_integrity_critical = {
      id          = "script-integrity-critical"
      name        = "Critical Script Integrity Validation"
      description = "Validate SHA-256 integrity of critical priority scripts"
      points      = 8
      check_type  = "script-integrity"
      category    = "security"
      required    = true
      remediation = "Update script registry: python3 scripts/maintenance/generate_script_registry.py --update"
      parameters = {
        priority = "critical"
      }
    }

    security_vulnerability_scan = {
      id          = "security-vulnerability-scan"
      name        = "Script Security Vulnerability Scan"
      description = "Scan scripts for security vulnerabilities (hardcoded secrets, injection, etc.)"
      points      = 7
      check_type  = "security-scan"
      category    = "security"
      required    = true
      remediation = "Fix security issues: python3 scripts/validate/check_script_security.py --verbose"
      parameters = {
        max_severity = "high"
      }
    }
  }

  # Workflow Checks (12 points)
  workflows_checks = {
    standards_compliance_workflow = {
      id          = "standards-compliance-workflow"
      name        = "Standards Compliance Workflow"
      description = "Check for standards-compliance.yml workflow"
      points      = 4
      check_type  = "file-exists"
      category    = "workflows"
      required    = true
      remediation = "Add standards-compliance workflow from MokoStandards templates"
      parameters = {
        file_path = ".github/workflows/standards-compliance.yml"
      }
    }

    code_quality_workflow = {
      id          = "code-quality-workflow"
      name        = "Code Quality Workflow"
      description = "Check for code-quality.yml workflow"
      points      = 3
      check_type  = "file-exists"
      category    = "workflows"
      required    = true
      remediation = "Add code-quality workflow from MokoStandards templates"
      parameters = {
        file_path = ".github/workflows/code-quality.yml"
      }
    }

    build_workflow = {
      id          = "build-workflow"
      name        = "Build Workflow"
      description = "Check for build.yml workflow"
      points      = 3
      check_type  = "file-exists"
      category    = "workflows"
      required    = false
      remediation = "Add build workflow from MokoStandards templates"
      parameters = {
        file_path = ".github/workflows/build.yml"
      }
    }

    release_cycle_workflow = {
      id          = "release-cycle-workflow"
      name        = "Release Cycle Workflow"
      description = "Check for release-cycle.yml workflow"
      points      = 2
      check_type  = "file-exists"
      category    = "workflows"
      required    = false
      remediation = "Add release-cycle workflow from MokoStandards templates"
      parameters = {
        file_path = ".github/workflows/release-cycle.yml"
      }
    }
  }

  # Issue Template Checks (5 points)
  issue_template_checks = {
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
      remediation = "Add bug_report.md template from MokoStandards"
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
      remediation = "Add feature_request.md template from MokoStandards"
      parameters = {
        file_path = ".github/ISSUE_TEMPLATE/feature_request.md"
      }
    }
  }

  # Repository Settings Checks (10 points)
  repository_settings_checks = {
    branch_protection_enabled = {
      id          = "branch-protection-enabled"
      name        = "Branch Protection Enabled"
      description = "Check if branch protection is enabled on main/master branch"
      points      = 5
      check_type  = "api-check"
      category    = "repository-settings"
      required    = true
      remediation = "Enable branch protection in repository settings"
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
      remediation = "Configure required status checks in branch protection settings"
      parameters = {
        branch    = "main"
        api_path  = "/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks"
        check_for = "contexts"
      }
    }

    require_pull_request_reviews = {
      id          = "require-pull-request-reviews"
      name        = "Require Pull Request Reviews"
      description = "Check if PR reviews are required before merging"
      points      = 2
      check_type  = "api-check"
      category    = "repository-settings"
      required    = false
      remediation = "Enable required reviews in branch protection settings"
      parameters = {
        branch    = "main"
        api_path  = "/repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews"
        check_for = "required_approving_review_count"
      }
    }
  }

  # Deployment Secrets Checks (20 points)
  deployment_secrets_checks = {
    github_token_available = {
      id          = "github-token-available"
      name        = "GITHUB_TOKEN Available"
      description = "Check if GITHUB_TOKEN is configured and accessible"
      points      = 5
      check_type  = "secret-exists"
      category    = "deployment-secrets"
      required    = true
      remediation = "GITHUB_TOKEN is automatically provided by GitHub Actions"
      parameters = {
        secret_name   = "GITHUB_TOKEN"
        scope         = "automatic"
        documentation = "Automatically provided by GitHub Actions"
      }
    }

    org_admin_token_configured = {
      id          = "org-admin-token-configured"
      name        = "ORG_ADMIN_TOKEN Configured"
      description = "Check if organization admin token is configured for cross-repo operations"
      points      = 5
      check_type  = "secret-exists"
      category    = "deployment-secrets"
      required    = false
      remediation = "Add ORG_ADMIN_TOKEN secret in repository or organization settings"
      parameters = {
        secret_name   = "ORG_ADMIN_TOKEN"
        scope         = "organization"
        documentation = "Required for bulk repository operations"
      }
    }

    deployment_secrets_configured = {
      id          = "deployment-secrets-configured"
      name        = "Deployment Secrets Configured"
      description = "Check if deployment-specific secrets are configured"
      points      = 5
      check_type  = "api-check"
      category    = "deployment-secrets"
      required    = false
      remediation = "Configure deployment secrets based on project needs"
      parameters = {
        api_path  = "/repos/{owner}/{repo}/actions/secrets"
        check_for = "total_count"
        min_count = 1
      }
    }

    secrets_documentation_present = {
      id          = "secrets-documentation-present"
      name        = "Secrets Documentation Present"
      description = "Check if secrets are documented (e.g., in DEPLOYMENT.md or README.md)"
      points      = 5
      check_type  = "content-pattern"
      category    = "deployment-secrets"
      required    = false
      remediation = "Document required secrets in DEPLOYMENT.md or README.md"
      parameters = {
        file_paths = ["DEPLOYMENT.md", "README.md", "docs/deployment.md"]
        pattern    = "(?i)(secret|token|credential|api[_\\s]key)"
      }
    }
  }
}

# Output all configuration for consumption by validation scripts
output "repo_health_config" {
  description = "Complete repository health configuration with all 103 points implemented"
  value = {
    metadata   = local.repo_health_metadata
    scoring    = local.scoring
    categories = local.categories
    thresholds = local.thresholds
    checks = merge(
      local.ci_cd_checks,
      local.documentation_checks,
      local.folder_checks,
      local.security_checks,
      local.workflows_checks,
      local.issue_template_checks,
      local.repository_settings_checks,
      local.deployment_secrets_checks
    )
  }
}
