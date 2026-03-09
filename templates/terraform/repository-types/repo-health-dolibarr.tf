# Repository Health Configuration for Dolibarr Module Repositories
# This defines health scoring for Dolibarr modules and extensions
# Total: 96 points

locals {
  dolibarr_config_metadata = {
    name              = "Repository Type Dolibarr Health Configuration"
    description       = "Health scoring for Dolibarr modules and extensions"
    version           = "04.00.03"
    last_updated      = "2026-02-27"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type   = "dolibarr"
    format            = "terraform"
    enterprise_ready  = true
  }

  dolibarr_repo_health_metadata = {
    name           = "Dolibarr Repository Health Configuration"
    description    = "Health scoring for Dolibarr modules and extensions"
    effective_date = "2026-02-27T00:00:00Z"
    maintainer     = "Moko Consulting"
    version        = "1.0.0"
    schema_version = "1.0"
  }

  dolibarr_scoring = {
    # Categories: CI/CD (15) + Docs (17) + Folders (12) + Workflows (12) + 
    # Issue Templates (5) + Security (14) + Repo Settings (10) + Deployment (11) = 96
    total_points = 96
  }

  dolibarr_categories = {
    ci_cd_status = {
      id          = "ci-cd-status"
      name        = "CI/CD Status"
      description = "Dolibarr module build and test pipelines"
      max_points  = 15
      enabled     = true
    }

    required_documentation = {
      id          = "required-documentation"
      name        = "Required Documentation"
      description = "Dolibarr-specific documentation"
      max_points  = 17
      enabled     = true
    }

    required_folders = {
      id          = "required-folders"
      name        = "Required Folders"
      description = "Dolibarr module structure"
      max_points  = 12
      enabled     = true
    }

    workflows = {
      id          = "workflows"
      name        = "Workflows"
      description = "Dolibarr-specific workflows"
      max_points  = 12
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
      description = "Dolibarr security scanning"
      max_points  = 14
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
      description = "Dolibarr marketplace credentials"
      max_points  = 11
      enabled     = true
    }
  }

  # CI/CD Checks (15 points)
  dolibarr_ci_cd_checks = {
    ci_workflow_present = {
      id          = "ci-workflow-present"
      name        = "Dolibarr CI workflow"
      description = "Dolibarr-specific CI workflow"
      points      = 5
      check_type  = "workflow-exists"
      category    = "ci-cd-status"
      required    = true
      remediation = "Add Dolibarr CI workflow"
      parameters = {
        workflow_paths = [".github/workflows/ci-dolibarr.yml", ".github/workflows/ci.yml"]
      }
    }

    dolibarr_tests_passing = {
      id          = "dolibarr-tests-passing"
      name        = "Tests passing"
      description = "Dolibarr module tests passing"
      points      = 5
      check_type  = "workflow-passing"
      category    = "ci-cd-status"
      required    = true
      remediation = "Fix failing tests"
      parameters = {
        workflow_name = "ci-dolibarr.yml"
        branch        = "main"
      }
    }

    build_status_badge = {
      id          = "build-status-badge"
      name        = "Build status badge"
      description = "README contains CI badge"
      points      = 5
      check_type  = "content-pattern"
      category    = "ci-cd-status"
      required    = false
      remediation = "Add status badge"
      parameters = {
        file_path = "README.md"
        pattern   = "\\[!\\[.*\\]\\(.*\\)\\]\\(.*\\)"
      }
    }
  }

  # Documentation Checks (17 points)
  dolibarr_documentation_checks = {
    readme_present = {
      id          = "readme-present"
      name        = "README.md present"
      description = "Module documentation"
      points      = 3
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create README.md"
      parameters = {
        file_path = "README.md"
      }
    }

    module_descriptor = {
      id          = "module-descriptor"
      name        = "Module descriptor file"
      description = "Dolibarr module descriptor"
      points      = 4
      check_type  = "file-exists-pattern"
      category    = "required-documentation"
      required    = true
      remediation = "Create module descriptor (modMyModule.class.php)"
      parameters = {
        file_pattern = "core/modules/mod*.class.php"
        required     = true
      }
    }

    installation_guide = {
      id          = "installation-guide"
      name        = "Installation guide"
      description = "Dolibarr installation instructions"
      points      = 2
      check_type  = "content-pattern"
      category    = "required-documentation"
      required    = true
      remediation = "Add installation guide to README"
      parameters = {
        file_path = "README.md"
        pattern   = "(?i)(install|installation)"
      }
    }

    license_present = {
      id          = "license-present"
      name        = "LICENSE file"
      description = "Module license"
      points      = 2
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Add LICENSE (GPL-3.0 recommended)"
      parameters = {
        file_path = "LICENSE"
      }
    }

    changelog_present = {
      id          = "changelog-present"
      name        = "CHANGELOG.md"
      description = "Module version history"
      points      = 2
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create CHANGELOG.md"
      parameters = {
        file_path = "CHANGELOG.md"
      }
    }

    security_policy = {
      id          = "security-policy"
      name        = "SECURITY.md"
      description = "Security policy"
      points      = 2
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create SECURITY.md"
      parameters = {
        file_path = "SECURITY.md"
      }
    }

    dolibarr_compatibility = {
      id          = "dolibarr-compatibility"
      name        = "Dolibarr compatibility documented"
      description = "Supported Dolibarr versions"
      points      = 2
      check_type  = "content-pattern"
      category    = "required-documentation"
      required    = true
      remediation = "Document Dolibarr compatibility in README"
      parameters = {
        file_paths = ["README.md", "core/modules/mod*.class.php"]
        pattern    = "(?i)dolibarr\\s+(\\d+\\.\\d+|version)"
      }
    }
  }

  # Folder Checks (12 points)
  dolibarr_folder_checks = {
    github_directory = {
      id          = "github-directory"
      name        = ".github/ directory"
      description = "GitHub configuration"
      points      = 2
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = true
      remediation = "Create .github/"
      parameters = {
        directory_path = ".github"
      }
    }

    workflows_directory = {
      id          = "workflows-directory"
      name        = ".github/workflows/"
      description = "Workflows directory"
      points      = 2
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = true
      remediation = "Create .github/workflows/"
      parameters = {
        directory_path = ".github/workflows"
      }
    }

    dolibarr_core_structure = {
      id          = "dolibarr-core-structure"
      name        = "Dolibarr module structure"
      description = "Standard Dolibarr folders"
      points      = 4
      check_type  = "directory-exists-any"
      category    = "required-folders"
      required    = true
      remediation = "Create Dolibarr module structure"
      parameters = {
        directory_paths = ["core/modules", "core/triggers", "admin", "class", "langs"]
      }
    }

    scripts_directory = {
      id          = "scripts-directory"
      name        = "scripts/ directory"
      description = "Build and release scripts"
      points      = 2
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = false
      remediation = "Create scripts/"
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

  # Security Checks (14 points)
  dolibarr_security_checks = {
    dolibarr_security_scan = {
      id          = "dolibarr-security-scan"
      name        = "Dolibarr security scanning"
      description = "Dolibarr-specific security checks"
      points      = 5
      check_type  = "workflow-exists"
      category    = "security"
      required    = true
      remediation = "Add Dolibarr security scan workflow"
      parameters = {
        workflow_paths = [".github/workflows/security-scan.yml", ".github/workflows/dolibarr-security.yml"]
      }
    }

    dependabot_present = {
      id          = "dependabot-present"
      name        = "Dependabot configuration"
      description = "Dependency updates"
      points      = 4
      check_type  = "file-exists"
      category    = "security"
      required    = true
      remediation = "Add .github/dependabot.yml"
      parameters = {
        file_path = ".github/dependabot.yml"
      }
    }

    sql_injection_check = {
      id          = "sql-injection-check"
      name        = "SQL injection prevention"
      description = "Database query security"
      points      = 5
      check_type  = "content-pattern"
      category    = "security"
      required    = true
      remediation = "Use Dolibarr $db->query() with proper escaping"
      parameters = {
        file_pattern = "*.php"
        pattern      = "\\$db->escape|\\$db->query"
      }
    }
  }

  # Workflow Checks (12 points)
  dolibarr_workflows_checks = {
    ci_dolibarr_workflow = {
      id          = "ci-dolibarr-workflow"
      name        = "Dolibarr CI Workflow"
      description = "Dolibarr testing workflow"
      points      = 4
      check_type  = "file-exists"
      category    = "workflows"
      required    = true
      remediation = "Add CI workflow"
      parameters = {
        file_path = ".github/workflows/ci-dolibarr.yml"
      }
    }

    package_workflow = {
      id          = "package-workflow"
      name        = "Package Workflow"
      description = "Module packaging"
      points      = 4
      check_type  = "workflow-exists"
      category    = "workflows"
      required    = true
      remediation = "Add package workflow"
      parameters = {
        workflow_paths = [".github/workflows/package-dolibarr.yml", ".github/workflows/release.yml"]
      }
    }

    release_workflow = {
      id          = "release-workflow"
      name        = "Release Workflow"
      description = "Automated releases"
      points      = 4
      check_type  = "file-exists"
      category    = "workflows"
      required    = false
      remediation = "Add release workflow"
      parameters = {
        file_path = ".github/workflows/release-cycle.yml"
      }
    }
  }

  # Issue Templates (5 points)
  dolibarr_issue_template_checks = {
    issue_template_directory = {
      id          = "issue-template-directory"
      name        = "Issue Template Directory"
      description = "GitHub issue templates"
      points      = 1
      check_type  = "directory-exists"
      category    = "issue-templates"
      required    = true
      remediation = "Create .github/ISSUE_TEMPLATE/"
      parameters = {
        directory_path = ".github/ISSUE_TEMPLATE"
      }
    }

    bug_report_template = {
      id          = "bug-report-template"
      name        = "Bug Report Template"
      description = "Bug reports"
      points      = 2
      check_type  = "file-exists"
      category    = "issue-templates"
      required    = true
      remediation = "Add bug_report.md"
      parameters = {
        file_path = ".github/ISSUE_TEMPLATE/bug_report.md"
      }
    }

    feature_request_template = {
      id          = "feature-request-template"
      name        = "Feature Request Template"
      description = "Feature requests"
      points      = 2
      check_type  = "file-exists"
      category    = "issue-templates"
      required    = true
      remediation = "Add feature_request.md"
      parameters = {
        file_path = ".github/ISSUE_TEMPLATE/feature_request.md"
      }
    }
  }

  # Repository Settings (10 points)
  dolibarr_repository_settings_checks = {
    branch_protection_enabled = {
      id          = "branch-protection-enabled"
      name        = "Branch Protection"
      description = "Branch protection enabled"
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
      description = "Required CI checks"
      points      = 3
      check_type  = "api-check"
      category    = "repository-settings"
      required    = true
      remediation = "Configure required checks"
      parameters = {
        branch    = "main"
        api_path  = "/repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks"
        check_for = "contexts"
      }
    }

    require_pull_request_reviews = {
      id          = "require-pull-request-reviews"
      name        = "Require PR Reviews"
      description = "PR reviews required"
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

  # Deployment Secrets (11 points)
  dolibarr_deployment_secrets_checks = {
    dolibarr_credentials = {
      id          = "dolibarr-credentials"
      name        = "Dolibarr Marketplace Credentials"
      description = "DoliStore credentials configured"
      points      = 5
      check_type  = "secret-exists-any"
      category    = "deployment-secrets"
      required    = false
      remediation = "Add Dolibarr marketplace credentials"
      parameters = {
        secret_names = ["DOLISTORE_API_KEY", "DOLIBARR_MARKETPLACE_TOKEN"]
        scope        = "repository"
      }
    }

    gh_token_available = {
      id          = "gh-token-available"
      name        = "GH_TOKEN"
      description = "Org-level GitHub PAT available"
      points      = 5
      check_type  = "secret-exists"
      category    = "deployment-secrets"
      required    = true
      remediation = "Set GH_TOKEN in organisation Actions secrets"
      parameters = {
        secret_name = "GH_TOKEN"
        scope       = "automatic"
      }
    }

    deployment_docs = {
      id          = "deployment-docs"
      name        = "Deployment Documentation"
      description = "Release process documented"
      points      = 1
      check_type  = "content-pattern"
      category    = "deployment-secrets"
      required    = false
      remediation = "Document release process"
      parameters = {
        file_paths = ["README.md", "docs/DEPLOYMENT.md"]
        pattern    = "(?i)(release|deploy|publish)"
      }
    }
  }
}

output "dolibarr_repo_health_config" {
  description = "Repository health configuration for Dolibarr modules"
  value = {
    metadata   = local.dolibarr_repo_health_metadata
    scoring    = local.dolibarr_scoring
    categories = local.dolibarr_categories
    thresholds = local.generic_thresholds
    checks = merge(
      local.dolibarr_ci_cd_checks,
      local.dolibarr_documentation_checks,
      local.dolibarr_folder_checks,
      local.dolibarr_security_checks,
      local.dolibarr_workflows_checks,
      local.dolibarr_issue_template_checks,
      local.dolibarr_repository_settings_checks,
      local.dolibarr_deployment_secrets_checks
    )
  }
}
