# Repository Health Configuration for Terraform Repositories
# This defines health scoring for Terraform infrastructure repositories
# Total: 110 points (more stringent than generic due to infrastructure criticality)

locals {
  terraform_config_metadata = {
    name              = "Repository Type Terraform Health Configuration"
    description       = "Health scoring for Terraform infrastructure repositories"
    version           = "04.00.04"
    last_updated      = "2026-02-27"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type   = "terraform"
    format            = "terraform"
    enterprise_ready  = true
  }

  terraform_repo_health_metadata = {
    name           = "Terraform Repository Health Configuration"
    description    = "Health scoring for Terraform infrastructure repositories"
    effective_date = "2026-02-27T00:00:00Z"
    maintainer     = "Moko Consulting"
    version        = "1.0.0"
    schema_version = "1.0"
  }

  terraform_scoring = {
    # Categories: CI/CD (18) + Docs (18) + Folders (12) + Workflows (15) + 
    # Issue Templates (5) + Security (17) + Repo Settings (10) + Deployment (15) = 110
    total_points = 110
  }

  terraform_categories = {
    ci_cd_status = {
      id          = "ci-cd-status"
      name        = "CI/CD Status"
      description = "Terraform validation and deployment pipelines"
      max_points  = 18
      enabled     = true
    }

    required_documentation = {
      id          = "required-documentation"
      name        = "Required Documentation"
      description = "Terraform-specific documentation"
      max_points  = 18
      enabled     = true
    }

    required_folders = {
      id          = "required-folders"
      name        = "Required Folders"
      description = "Terraform directory structure"
      max_points  = 12
      enabled     = true
    }

    workflows = {
      id          = "workflows"
      name        = "Workflows"
      description = "Terraform-specific GitHub Actions workflows"
      max_points  = 15
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
      description = "Terraform security scanning and state management"
      max_points  = 17
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
      description = "Cloud provider credentials and Terraform state access"
      max_points  = 15
      enabled     = true
    }
  }

  terraform_thresholds = {
    excellent = {
      level          = "excellent"
      min_percentage = 95
      max_percentage = 100
      indicator      = "✅"
      description    = "Production-ready infrastructure"
    }

    good = {
      level          = "good"
      min_percentage = 80
      max_percentage = 94
      indicator      = "⚠️"
      description    = "Minor improvements needed"
    }

    fair = {
      level          = "fair"
      min_percentage = 60
      max_percentage = 79
      indicator      = "🟡"
      description    = "Significant improvements required"
    }

    poor = {
      level          = "poor"
      min_percentage = 0
      max_percentage = 59
      indicator      = "❌"
      description    = "Critical infrastructure issues"
    }
  }

  # CI/CD Checks (18 points) - Terraform-specific
  terraform_ci_cd_checks = {
    terraform_validate_workflow = {
      id          = "terraform-validate-workflow"
      name        = "Terraform validate workflow"
      description = "Check for terraform validation workflow"
      points      = 6
      check_type  = "workflow-exists"
      category    = "ci-cd-status"
      required    = true
      remediation = "Add terraform validate workflow"
      parameters = {
        workflow_path = ".github/workflows/terraform-validate.yml"
        type          = "path"
      }
    }

    terraform_plan_workflow = {
      id          = "terraform-plan-workflow"
      name        = "Terraform plan workflow"
      description = "Verify terraform plan runs on PR"
      points      = 6
      check_type  = "workflow-exists"
      category    = "ci-cd-status"
      required    = true
      remediation = "Add terraform plan workflow"
      parameters = {
        workflow_path = ".github/workflows/terraform-plan.yml"
      }
    }

    terraform_fmt_check = {
      id          = "terraform-fmt-check"
      name        = "Terraform fmt check"
      description = "Code formatting validation"
      points      = 3
      check_type  = "workflow-step"
      category    = "ci-cd-status"
      required    = true
      remediation = "Add terraform fmt check step"
      parameters = {
        workflow_name = "terraform-validate.yml"
        step_pattern  = "terraform fmt"
      }
    }

    build_status_badge = {
      id          = "build-status-badge"
      name        = "Build status badge"
      description = "README contains validation status badge"
      points      = 3
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

  # Documentation Checks (18 points) - Terraform-specific
  terraform_documentation_checks = {
    readme_present = {
      id          = "readme-present"
      name        = "README.md present"
      description = "Repository has README with terraform docs"
      points      = 3
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create README.md with terraform documentation"
      parameters = {
        file_path = "README.md"
      }
    }

    terraform_readme_content = {
      id          = "terraform-readme-content"
      name        = "Terraform README content"
      description = "README contains terraform usage instructions"
      points      = 3
      check_type  = "content-pattern"
      category    = "required-documentation"
      required    = true
      remediation = "Add terraform usage section to README"
      parameters = {
        file_path = "README.md"
        pattern   = "(?i)(terraform\\s+(init|plan|apply)|usage)"
      }
    }

    terraform_variables_documented = {
      id          = "terraform-variables-documented"
      name        = "Variables documented"
      description = "terraform.tfvars.example or variables documentation exists"
      points      = 3
      check_type  = "file-exists-any"
      category    = "required-documentation"
      required    = true
      remediation = "Create terraform.tfvars.example"
      parameters = {
        file_paths = ["terraform.tfvars.example", "variables.tf.example", "docs/variables.md"]
      }
    }

    license_present = {
      id          = "license-present"
      name        = "LICENSE file present"
      description = "Repository has LICENSE file"
      points      = 2
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Add LICENSE file"
      parameters = {
        file_path = "LICENSE"
      }
    }

    changelog_present = {
      id          = "changelog-present"
      name        = "CHANGELOG.md present"
      description = "Infrastructure changes documented"
      points      = 2
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create CHANGELOG.md for infrastructure changes"
      parameters = {
        file_path = "CHANGELOG.md"
      }
    }

    security_policy_present = {
      id          = "security-policy-present"
      name        = "SECURITY.md present"
      description = "Security policy for infrastructure"
      points      = 3
      check_type  = "file-exists"
      category    = "required-documentation"
      required    = true
      remediation = "Create SECURITY.md"
      parameters = {
        file_path = "SECURITY.md"
      }
    }

    architecture_docs = {
      id          = "architecture-docs"
      name        = "Architecture documentation"
      description = "Infrastructure architecture documented"
      points      = 2
      check_type  = "file-exists-any"
      category    = "required-documentation"
      required    = false
      remediation = "Create architecture documentation"
      parameters = {
        file_paths = ["docs/ARCHITECTURE.md", "ARCHITECTURE.md", "docs/architecture.md"]
      }
    }
  }

  # Folder Checks (12 points) - Terraform-specific
  terraform_folder_checks = {
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
      points      = 2
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = true
      remediation = "Create .github/workflows/ directory"
      parameters = {
        directory_path = ".github/workflows"
      }
    }

    terraform_directory = {
      id          = "terraform-directory"
      name        = "Terraform directory structure"
      description = "Terraform files organized properly"
      points      = 4
      check_type  = "directory-exists-any"
      category    = "required-folders"
      required    = true
      remediation = "Organize terraform files in proper structure"
      parameters = {
        directory_paths = ["terraform", "modules", "."]
      }
    }

    modules_directory = {
      id          = "modules-directory"
      name        = "modules/ directory"
      description = "Reusable terraform modules directory"
      points      = 2
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = false
      remediation = "Create modules/ directory for reusable modules"
      parameters = {
        directory_path = "modules"
      }
    }

    docs_directory = {
      id          = "docs-directory"
      name        = "docs/ directory present"
      description = "Documentation directory exists"
      points      = 2
      check_type  = "directory-exists"
      category    = "required-folders"
      required    = false
      remediation = "Create docs/ directory"
      parameters = {
        directory_path = "docs"
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

  # Security Checks (17 points) - Terraform-specific
  terraform_security_checks = {
    tfsec_workflow = {
      id          = "tfsec-workflow"
      name        = "Terraform security scanning"
      description = "tfsec or similar security scanning"
      points      = 5
      check_type  = "workflow-exists"
      category    = "security"
      required    = true
      remediation = "Add tfsec or terraform security scanning"
      parameters = {
        workflow_paths = [".github/workflows/tfsec.yml", ".github/workflows/security-scan.yml"]
      }
    }

    state_backend_configured = {
      id          = "state-backend-configured"
      name        = "Remote state backend"
      description = "Terraform remote state backend configured"
      points      = 5
      check_type  = "content-pattern"
      category    = "security"
      required    = true
      remediation = "Configure remote state backend (S3, Azure, GCS, etc.)"
      parameters = {
        file_paths = ["main.tf", "backend.tf", "terraform.tf"]
        pattern    = "backend\\s+\"(s3|azurerm|gcs|remote)\""
      }
    }

    state_encryption = {
      id          = "state-encryption"
      name        = "State encryption enabled"
      description = "Terraform state encryption configured"
      points      = 4
      check_type  = "content-pattern"
      category    = "security"
      required    = true
      remediation = "Enable state encryption"
      parameters = {
        file_paths = ["main.tf", "backend.tf", "terraform.tf"]
        pattern    = "encrypt\\s*=\\s*true"
      }
    }

    dependabot_present = {
      id          = "dependabot-present"
      name        = "Dependabot configuration"
      description = "Check for .github/dependabot.yml"
      points      = 3
      check_type  = "file-exists"
      category    = "security"
      required    = false
      remediation = "Add .github/dependabot.yml for terraform providers"
      parameters = {
        file_path = ".github/dependabot.yml"
      }
    }
  }

  # Workflow Checks (15 points) - Terraform-specific
  terraform_workflows_checks = {
    terraform_validate = {
      id          = "terraform-validate"
      name        = "Terraform Validate Workflow"
      description = "Terraform validation workflow"
      points      = 5
      check_type  = "file-exists"
      category    = "workflows"
      required    = true
      remediation = "Add terraform validate workflow"
      parameters = {
        file_path = ".github/workflows/terraform-validate.yml"
      }
    }

    terraform_deploy = {
      id          = "terraform-deploy"
      name        = "Terraform Deploy Workflow"
      description = "Terraform deployment workflow"
      points      = 5
      check_type  = "file-exists"
      category    = "workflows"
      required    = true
      remediation = "Add terraform deploy workflow"
      parameters = {
        file_path = ".github/workflows/terraform-deploy.yml"
      }
    }

    terraform_drift_detection = {
      id          = "terraform-drift-detection"
      name        = "Drift Detection Workflow"
      description = "Terraform drift detection workflow"
      points      = 3
      check_type  = "file-exists"
      category    = "workflows"
      required    = true
      remediation = "Add drift detection workflow"
      parameters = {
        file_path = ".github/workflows/terraform-drift.yml"
      }
    }

    terraform_docs_generation = {
      id          = "terraform-docs-generation"
      name        = "Terraform Docs Generation"
      description = "Automated terraform documentation"
      points      = 2
      check_type  = "workflow-exists"
      category    = "workflows"
      required    = false
      remediation = "Add terraform-docs automation"
      parameters = {
        workflow_paths = [".github/workflows/terraform-docs.yml", ".github/workflows/docs.yml"]
      }
    }
  }

  # Issue Template Checks (5 points) - same as generic
  terraform_issue_template_checks = {
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
      description = "Check for bug report template"
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
      description = "Check for feature request template"
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

  # Repository Settings Checks (10 points) - same as generic
  terraform_repository_settings_checks = {
    branch_protection_enabled = {
      id          = "branch-protection-enabled"
      name        = "Branch Protection Enabled"
      description = "Branch protection for infrastructure"
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
      description = "Terraform validation required before merge"
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
      description = "Infrastructure changes require review"
      points      = 2
      check_type  = "api-check"
      category    = "repository-settings"
      required    = true
      remediation = "Enable required reviews for infrastructure"
      parameters = {
        branch    = "main"
        api_path  = "/repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews"
        check_for = "required_approving_review_count"
      }
    }
  }

  # Deployment Secrets Checks (15 points) - Terraform-specific
  terraform_deployment_secrets_checks = {
    cloud_provider_credentials = {
      id          = "cloud-provider-credentials"
      name        = "Cloud Provider Credentials"
      description = "AWS/Azure/GCP credentials configured"
      points      = 5
      check_type  = "secret-exists-any"
      category    = "deployment-secrets"
      required    = true
      remediation = "Configure cloud provider credentials as secrets"
      parameters = {
        secret_names = ["AWS_ACCESS_KEY_ID", "AZURE_CREDENTIALS", "GCP_SA_KEY", "TF_API_TOKEN"]
        scope        = "repository"
      }
    }

    terraform_backend_credentials = {
      id          = "terraform-backend-credentials"
      name        = "Backend Access Credentials"
      description = "Terraform state backend access configured"
      points      = 5
      check_type  = "secret-exists-any"
      category    = "deployment-secrets"
      required    = true
      remediation = "Configure backend access credentials"
      parameters = {
        secret_names = ["TF_BACKEND_KEY", "STATE_LOCK_KEY", "TERRAFORM_CLOUD_TOKEN"]
        scope        = "repository"
      }
    }

    secrets_documentation = {
      id          = "secrets-documentation"
      name        = "Secrets Documented"
      description = "Required secrets documented in README"
      points      = 5
      check_type  = "content-pattern"
      category    = "deployment-secrets"
      required    = true
      remediation = "Document required secrets in README or DEPLOYMENT.md"
      parameters = {
        file_paths = ["README.md", "DEPLOYMENT.md", "docs/deployment.md"]
        pattern    = "(?i)(secret|credential|aws_access_key|azure_credentials)"
      }
    }
  }
}

# Output configuration for terraform repositories
output "terraform_repo_health_config" {
  description = "Complete repository health configuration for terraform repositories"
  value = {
    metadata   = local.terraform_repo_health_metadata
    scoring    = local.terraform_scoring
    categories = local.terraform_categories
    thresholds = local.terraform_thresholds
    checks = merge(
      local.terraform_ci_cd_checks,
      local.terraform_documentation_checks,
      local.terraform_folder_checks,
      local.terraform_security_checks,
      local.terraform_workflows_checks,
      local.terraform_issue_template_checks,
      local.terraform_repository_settings_checks,
      local.terraform_deployment_secrets_checks
    )
  }
}
