# Repository Health Configuration for Node.js Repositories
# This defines health scoring for Node.js/JavaScript/TypeScript projects
# Total: 95 points

locals {
  nodejs_config_metadata = {
    name              = "Repository Type Node.js Health Configuration"
    description       = "Health scoring for Node.js/JavaScript/TypeScript projects"
    version           = "04.00.04"
    last_updated      = "2026-02-27"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type   = "nodejs"
    format            = "terraform"
    enterprise_ready  = true
  }

  nodejs_repo_health_metadata = {
    name           = "Node.js Repository Health Configuration"
    description    = "Health scoring for Node.js/JavaScript/TypeScript projects"
    effective_date = "2026-02-27T00:00:00Z"
    maintainer     = "Moko Consulting"
    version        = "1.0.0"
    schema_version = "1.0"
  }

  nodejs_scoring = {
    # Categories: CI/CD (15) + Docs (16) + Folders (10) + Workflows (12) + 
    # Issue Templates (5) + Security (15) + Repo Settings (10) + Deployment (12) = 95
    total_points = 95
  }

  nodejs_categories = {
    ci_cd_status = {
      id          = "ci-cd-status"
      name        = "CI/CD Status"
      description = "Node.js build and test pipelines"
      max_points  = 15
      enabled     = true
    }

    required_documentation = {
      id          = "required-documentation"
      name        = "Required Documentation"
      description = "Node.js project documentation"
      max_points  = 16
      enabled     = true
    }

    required_folders = {
      id          = "required-folders"
      name        = "Required Folders"
      description = "Node.js project structure"
      max_points  = 10
      enabled     = true
    }

    workflows = {
      id          = "workflows"
      name        = "Workflows"
      description = "Node.js-specific workflows"
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
      description = "npm/yarn security and dependency scanning"
      max_points  = 15
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
      description = "npm registry and deployment credentials"
      max_points  = 12
      enabled     = true
    }
  }

  # CI/CD Checks (15 points)
  nodejs_ci_cd_checks = {
    ci_workflow_present = {
      id          = "ci-workflow-present"
      name        = "CI workflow present"
      description = "Node.js build and test workflow"
      points      = 5
      check_type  = "workflow-exists"
      category    = "ci-cd-status"
      required    = true
      remediation = "Add CI workflow with npm/yarn commands"
      parameters = {
        workflow_path = ".github/workflows/ci.yml"
      }
    }

    npm_test_passing = {
      id          = "npm-test-passing"
      name        = "Tests passing"
      description = "npm test or yarn test passing"
      points      = 5
      check_type  = "workflow-passing"
      category    = "ci-cd-status"
      required    = true
      remediation = "Fix failing tests"
      parameters = {
        workflow_name = "ci.yml"
        branch        = "main"
      }
    }

    build_status_badge = {
      id          = "build-status-badge"
      name        = "Build status badge"
      description = "README contains CI status badge"
      points      = 5
      check_type  = "content-pattern"
      category    = "ci-cd-status"
      required    = false
      remediation = "Add status badge to README.md"
      parameters = {
        file_path = "README.md"
        pattern   = "\\[!\\[.*\\]\\(.*\\)\\]\\(.*\\)"
      }
    }
  }

  # Documentation Checks (16 points)
  nodejs_documentation_checks = {
    readme_present = {
      id          = "readme-present"
      name        = "README.md present"
      description = "Project documentation"
      points      = 3
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create README.md"
      parameters = {
        file_path = "README.md"
      }
    }

    package_json_present = {
      id          = "package-json-present"
      name        = "package.json present"
      description = "Node.js package configuration"
      points      = 3
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create package.json with npm init"
      parameters = {
        file_path = "package.json"
      }
    }

    license_present = {
      id          = "license-present"
      name        = "LICENSE file present"
      description = "Repository has LICENSE"
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
      description = "Contribution guidelines"
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
      description = "Version history"
      points      = 2
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = false
      remediation = "Create CHANGELOG.md"
      parameters = {
        file_path = "CHANGELOG.md"
      }
    }

    security_policy_present = {
      id          = "security-policy-present"
      name        = "SECURITY.md present"
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

    api_documentation = {
      id          = "api-documentation"
      name        = "API documentation"
      description = "JSDoc or similar documentation"
      points      = 2
      check_type  = "file-exists-any"
      category    = "required-documentation"
      required    = false
      remediation = "Add API documentation"
      parameters = {
        file_paths = ["docs/API.md", "API.md", "docs/api"]
      }
    }
  }

  # Folder Checks (10 points)
  nodejs_folder_checks = {
    github_directory = {
      id          = "github-directory"
      name        = ".github/ directory"
      description = "GitHub configuration"
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
      name        = ".github/workflows/ directory"
      description = "GitHub Actions workflows"
      points      = 2
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = true
      remediation = "Create .github/workflows/"
      parameters = {
        directory_path = ".github/workflows"
      }
    }

    tests_directory = {
      id          = "tests-directory"
      name        = "tests/ or test/ directory"
      description = "Test files location"
      points      = 3
      check_type  = "directory-exists-any"
      category    = "required-folders"
      required    = true
      remediation = "Create tests/ or api/tests/ directory"
      parameters = {
        directory_paths = ["tests", "test", "__tests__", "spec", "api/tests"]
      }
    }

    src_directory = {
      id          = "src-directory"
      name        = "src/ or lib/ directory"
      description = "Source code organization"
      points      = 3
      check_type  = "directory-exists-any"
      category    = "required-folders"
      required    = false
      remediation = "Organize code in src/, api/src/, or lib/"
      parameters = {
        directory_paths = ["src", "lib", "app", "api/src"]
      }
    }

    logs_directory = {
      id          = "logs-directory"
      name        = "logs/ directory"
      description = "Centralized logs directory"
      points      = 2
      check_type  = "directory-exists"
      category    = "optional-folders"
      required    = false
      remediation = "Create logs/ directory for centralized logging"
      parameters = {
        directory_path = "logs"
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

  # Security Checks (15 points)
  nodejs_security_checks = {
    npm_audit_workflow = {
      id          = "npm-audit-workflow"
      name        = "npm audit in CI"
      description = "npm audit runs in CI pipeline"
      points      = 5
      check_type  = "workflow-step"
      category    = "security"
      required    = true
      remediation = "Add npm audit step to CI"
      parameters = {
        workflow_name = "ci.yml"
        step_pattern  = "npm audit"
      }
    }

    dependabot_present = {
      id          = "dependabot-present"
      name        = "Dependabot configuration"
      description = "Automated dependency updates"
      points      = 5
      check_type  = "file-exists"
      category    = "security"
      required    = true
      remediation = "Add .github/dependabot.yml"
      parameters = {
        file_path = ".github/dependabot.yml"
      }
    }

    codeql_workflow = {
      id          = "codeql-workflow"
      name        = "CodeQL analysis"
      description = "CodeQL security scanning"
      points      = 5
      check_type  = "workflow-exists"
      category    = "security"
      required    = false
      remediation = "Add CodeQL workflow"
      parameters = {
        workflow_paths = [".github/workflows/codeql-analysis.yml", ".github/workflows/security-scan.yml"]
      }
    }
  }

  # Workflow Checks (12 points)
  nodejs_workflows_checks = {
    ci_workflow = {
      id          = "ci-workflow"
      name        = "CI Workflow"
      description = "Build and test workflow"
      points      = 4
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
      description = "ESLint/Prettier checks"
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
      description = "Automated releases"
      points      = 3
      check_type  = "file-exists"
      category    = "workflows"
      required    = false
      remediation = "Add release workflow"
      parameters = {
        file_path = ".github/workflows/release.yml"
      }
    }

    npm_publish_workflow = {
      id          = "npm-publish-workflow"
      name        = "npm Publish Workflow"
      description = "Automated npm publishing"
      points      = 2
      check_type  = "workflow-exists"
      category    = "workflows"
      required    = false
      remediation = "Add npm publish workflow"
      parameters = {
        workflow_paths = [".github/workflows/npm-publish.yml", ".github/workflows/publish.yml"]
      }
    }
  }

  # Issue Template, Repo Settings, Deployment Secrets - reuse from generic
  nodejs_issue_template_checks = {
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
      description = "Bug report template"
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
      description = "Feature request template"
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

  nodejs_repository_settings_checks = {
    branch_protection_enabled = {
      id          = "branch-protection-enabled"
      name        = "Branch Protection Enabled"
      description = "Branch protection on main"
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

  nodejs_deployment_secrets_checks = {
    npm_token = {
      id          = "npm-token"
      name        = "NPM Token"
      description = "npm registry authentication"
      points      = 5
      check_type  = "secret-exists"
      category    = "deployment-secrets"
      required    = false
      remediation = "Add NPM_TOKEN secret"
      parameters = {
        secret_name = "NPM_TOKEN"
        scope       = "repository"
      }
    }

    gh_token_available = {
      id          = "gh-token-available"
      name        = "GH_TOKEN Available"
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

    deployment_secrets_documented = {
      id          = "deployment-secrets-documented"
      name        = "Secrets Documented"
      description = "Deployment secrets documented"
      points      = 2
      check_type  = "content-pattern"
      category    = "deployment-secrets"
      required    = false
      remediation = "Document secrets in README"
      parameters = {
        file_paths = ["README.md", "docs/deployment.md"]
        pattern    = "(?i)(npm_token|secret|credential)"
      }
    }
  }
}

output "nodejs_repo_health_config" {
  description = "Repository health configuration for Node.js projects"
  value = {
    metadata   = local.nodejs_repo_health_metadata
    scoring    = local.nodejs_scoring
    categories = local.nodejs_categories
    thresholds = local.generic_thresholds # Reuse generic thresholds
    checks = merge(
      local.nodejs_ci_cd_checks,
      local.nodejs_documentation_checks,
      local.nodejs_folder_checks,
      local.nodejs_security_checks,
      local.nodejs_workflows_checks,
      local.nodejs_issue_template_checks,
      local.nodejs_repository_settings_checks,
      local.nodejs_deployment_secrets_checks
    )
  }
}
