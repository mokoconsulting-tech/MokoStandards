# Repository Health Configuration for Joomla Extension Repositories
# This defines health scoring for Joomla extensions and components
# Total: 98 points

locals {
  joomla_config_metadata = {
    name              = "Repository Type Joomla Health Configuration"
    description       = "Health scoring for Joomla extensions and components"
    version           = "04.00.04"
    last_updated      = "2026-02-27"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type   = "joomla"
    format            = "terraform"
    enterprise_ready  = true
  }

  joomla_repo_health_metadata = {
    name           = "Joomla Repository Health Configuration"
    description    = "Health scoring for Joomla extensions and components"
    effective_date = "2026-02-27T00:00:00Z"
    maintainer     = "Moko Consulting"
    version        = "1.0.0"
    schema_version = "1.0"
  }

  joomla_scoring = {
    # Categories: CI/CD (15) + Docs (18) + Folders (12) + Workflows (12) + 
    # Issue Templates (5) + Security (14) + Repo Settings (10) + Deployment (12) = 98
    total_points = 98
  }

  joomla_categories = {
    ci_cd_status = {
      id          = "ci-cd-status"
      name        = "CI/CD Status"
      description = "Joomla extension build and test pipelines"
      max_points  = 15
      enabled     = true
    }

    required_documentation = {
      id          = "required-documentation"
      name        = "Required Documentation"
      description = "Joomla-specific documentation"
      max_points  = 18
      enabled     = true
    }

    required_folders = {
      id          = "required-folders"
      name        = "Required Folders"
      description = "Joomla extension structure"
      max_points  = 12
      enabled     = true
    }

    workflows = {
      id          = "workflows"
      name        = "Workflows"
      description = "Joomla-specific workflows"
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
      description = "Joomla security scanning"
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
      description = "Joomla marketplace credentials"
      max_points  = 12
      enabled     = true
    }
  }

  # CI/CD Checks (15 points)
  joomla_ci_cd_checks = {
    ci_workflow_present = {
      id          = "ci-workflow-present"
      name        = "Joomla CI workflow"
      description = "Joomla-specific CI workflow"
      points      = 5
      check_type  = "workflow-exists"
      category    = "ci-cd-status"
      required    = true
      remediation = "Add Joomla CI workflow"
      parameters = {
        workflow_paths = [".github/workflows/ci-joomla.yml", ".github/workflows/ci.yml"]
      }
    }

    joomla_tests_passing = {
      id          = "joomla-tests-passing"
      name        = "Tests passing"
      description = "Joomla extension tests passing"
      points      = 5
      check_type  = "workflow-passing"
      category    = "ci-cd-status"
      required    = true
      remediation = "Fix failing tests"
      parameters = {
        workflow_name = "ci-joomla.yml"
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

  # Documentation Checks (18 points)
  joomla_documentation_checks = {
    readme_present = {
      id          = "readme-present"
      name        = "README.md present"
      description = "Extension documentation"
      points      = 3
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create README.md"
      parameters = {
        file_path = "README.md"
      }
    }

    joomla_manifest = {
      id          = "joomla-manifest"
      name        = "Joomla manifest file"
      description = "Extension manifest XML"
      points      = 4
      check_type  = "file-exists-pattern"
      category    = "required-documentation"
      required    = true
      remediation = "Create Joomla manifest XML"
      parameters = {
        file_pattern = "*.xml"
        contains     = "<extension"
      }
    }

    installation_guide = {
      id          = "installation-guide"
      name        = "Installation guide"
      description = "Joomla installation instructions"
      points      = 3
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
      description = "Extension license"
      points      = 2
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Add LICENSE"
      parameters = {
        file_path = "LICENSE"
      }
    }

    changelog_present = {
      id          = "changelog-present"
      name        = "CHANGELOG.md"
      description = "Extension version history"
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

    joomla_compatibility = {
      id          = "joomla-compatibility"
      name        = "Joomla compatibility documented"
      description = "Supported Joomla versions"
      points      = 2
      check_type  = "content-pattern"
      category    = "required-documentation"
      required    = true
      remediation = "Document Joomla compatibility"
      parameters = {
        file_paths = ["README.md", "manifest.xml"]
        pattern    = "(?i)joomla\\s+[34]\\."
      }
    }
  }

  # Folder Checks (12 points)
  joomla_folder_checks = {
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

    joomla_structure = {
      id          = "joomla-structure"
      name        = "Joomla extension structure"
      description = "Standard Joomla folders"
      points      = 4
      check_type  = "directory-exists-any"
      category    = "required-folders"
      required    = true
      remediation = "Create Joomla extension structure"
      parameters = {
        directory_paths = ["admin", "site", "media", "language"]
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
  joomla_security_checks = {
    joomla_security_scan = {
      id          = "joomla-security-scan"
      name        = "Joomla security scanning"
      description = "Joomla-specific security checks"
      points      = 5
      check_type  = "workflow-exists"
      category    = "security"
      required    = true
      remediation = "Add Joomla security scan workflow"
      parameters = {
        workflow_paths = [".github/workflows/security-scan.yml", ".github/workflows/joomla-security.yml"]
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
      remediation = "Use JDatabase prepared statements"
      parameters = {
        file_pattern = "*.php"
        pattern      = "\\$db->quote|\\$db->escape|JDatabase"
      }
    }
  }

  # Workflow Checks (12 points)
  joomla_workflows_checks = {
    ci_joomla_workflow = {
      id          = "ci-joomla-workflow"
      name        = "Joomla CI Workflow"
      description = "Joomla testing workflow"
      points      = 4
      check_type  = "file-exists"
      category    = "workflows"
      required    = true
      remediation = "Add CI workflow"
      parameters = {
        file_path = ".github/workflows/ci-joomla.yml"
      }
    }

    package_workflow = {
      id          = "package-workflow"
      name        = "Package Workflow"
      description = "Extension packaging"
      points      = 4
      check_type  = "workflow-exists"
      category    = "workflows"
      required    = true
      remediation = "Add package workflow"
      parameters = {
        workflow_paths = [".github/workflows/package-joomla.yml", ".github/workflows/release.yml"]
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

  # Issue Templates, Repo Settings, Deployment (reuse patterns)
  joomla_issue_template_checks = {
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

  joomla_repository_settings_checks = {
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

  joomla_deployment_secrets_checks = {
    joomla_credentials = {
      id          = "joomla-credentials"
      name        = "Joomla Marketplace Credentials"
      description = "JED credentials configured"
      points      = 5
      check_type  = "secret-exists-any"
      category    = "deployment-secrets"
      required    = false
      remediation = "Add Joomla marketplace credentials"
      parameters = {
        secret_names = ["JED_API_KEY", "JOOMLA_MARKETPLACE_TOKEN"]
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
      points      = 2
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

output "joomla_repo_health_config" {
  description = "Repository health configuration for Joomla extensions"
  value = {
    metadata   = local.joomla_repo_health_metadata
    scoring    = local.joomla_scoring
    categories = local.joomla_categories
    thresholds = local.generic_thresholds
    checks = merge(
      local.joomla_ci_cd_checks,
      local.joomla_documentation_checks,
      local.joomla_folder_checks,
      local.joomla_security_checks,
      local.joomla_workflows_checks,
      local.joomla_issue_template_checks,
      local.joomla_repository_settings_checks,
      local.joomla_deployment_secrets_checks
    )
  }
}
