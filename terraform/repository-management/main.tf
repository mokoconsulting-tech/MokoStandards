# Terraform Configuration for Repository Template Management
# This directory contains Terraform configurations for managing repository templates
# using the GitHub provider to update multiple repositories declaratively.


locals {
  # Metadata for this configuration
  # Enterprise-ready: Includes audit logging, monitoring, and compliance features
  config_metadata = {
    name               = "Repository Management Main"
    description        = "Repository template management and bulk operations configuration"
    version            = "04.00.00"
    last_updated       = "2026-02-11"
    maintainer         = "MokoStandards Team"
    schema_version     = "2.0"
    repository_url     = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type    = "standards"
    format             = "terraform"
    enterprise_ready   = true
    monitoring_enabled = true
    audit_logging      = true
  }
}

terraform {
  required_version = ">= 1.7.0"

  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
  }

  # Configure backend for state storage
  # For production, use remote backend (S3, Azure Storage, GCS, Terraform Cloud)
  backend "s3" {
    # bucket         = "mokostandards-terraform-state"
    # key            = "repository-templates/terraform.tfstate"
    # region         = "us-east-1"
    # dynamodb_table = "mokostandards-terraform-locks"
    # encrypt        = true
  }
}

# GitHub Provider Configuration
provider "github" {
  token = var.github_token
  owner = var.github_org
}

# Variables
variable "github_token" {
  description = "GitHub personal access token with repo and admin:org permissions"
  type        = string
  sensitive   = true
}

variable "github_org" {
  description = "GitHub organization name"
  type        = string
  default     = "mokoconsulting-tech"
}

variable "target_repositories" {
  description = "Map of repositories to manage with their types"
  type = map(object({
    repository_type = string # generic, terraform, joomla, dolibarr
    enabled         = bool
    custom_files    = map(string) # Additional custom file mappings
  }))
  default = {}
}

# Data source to fetch repository information
data "github_repositories" "org_repos" {
  query = "org:${var.github_org}"
}

data "github_repository" "repos" {
  for_each  = var.target_repositories
  full_name = "${var.github_org}/${each.key}"
}

# Local values for template mappings
locals {
  # Base template mappings by file and repository type
  base_templates = {
    ".github/workflows/ci.yml" = {
      generic   = "../../templates/workflows/generic/ci.yml"
      terraform = "../../templates/workflows/terraform/ci.yml"
      joomla    = "../../templates/workflows/joomla/ci-joomla.yml.template"
      dolibarr  = "../../templates/workflows/dolibarr/ci-dolibarr.yml.template"
    }
    ".github/workflows/terraform-deploy.yml" = {
      terraform = "../../templates/workflows/terraform/deploy.yml.template"
    }
    ".github/workflows/terraform-drift.yml" = {
      terraform = "../../templates/workflows/terraform/drift-detection.yml.template"
    }
    ".github/workflows/code-quality.yml" = {
      generic   = "../../templates/workflows/generic/code-quality.yml"
      terraform = "../../templates/workflows/generic/code-quality.yml"
    }
    # Enterprise workflow distributions for audit, metrics, and health monitoring
    ".github/workflows/audit-log-archival.yml" = {
      all = "../../templates/workflows/audit-log-archival.yml"
    }
    ".github/workflows/metrics-collection.yml" = {
      all = "../../templates/workflows/metrics-collection.yml"
    }
    ".github/workflows/health-check.yml" = {
      all = "../../templates/workflows/health-check.yml"
    }
    ".github/workflows/security-scan.yml" = {
      all = "../../templates/workflows/security-scan.yml"
    }
    ".github/workflows/integration-tests.yml" = {
      all = "../../templates/workflows/integration-tests.yml"
    }
    # Version management scripts - required in all repositories
    "scripts/lib/version_bump_detector.py" = {
      all = "../../scripts/lib/version_bump_detector.py"
    }
    "scripts/automation/detect_version_bump.py" = {
      all = "../../scripts/automation/detect_version_bump.py"
    }
    "scripts/lib/common.py" = {
      all = "../../scripts/lib/common.py"
    }
    "scripts/tests/test_version_bump_detector.py" = {
      all = "../../scripts/tests/test_version_bump_detector.py"
    }
    # Branch management scripts - required in all repositories
    "scripts/maintenance/clean_old_branches.py" = {
      all = "../../scripts/maintenance/clean_old_branches.py"
    }
    "scripts/maintenance/release_version.py" = {
      all = "../../scripts/maintenance/release_version.py"
    }
    # Release management scripts - required in all repositories
    "scripts/release/unified_release.py" = {
      all = "../../scripts/release/unified_release.py"
    }
    "scripts/release/detect_platform.py" = {
      all = "../../scripts/release/detect_platform.py"
    }
    "scripts/release/package_extension.py" = {
      all = "../../scripts/release/package_extension.py"
    }
    # Terraform installation scripts - required in all repositories for IaC capabilities
    "scripts/automation/install_terraform.sh" = {
      all = "../../scripts/automation/install_terraform.sh"
    }
    "scripts/automation/install_terraform.py" = {
      all = "../../scripts/automation/install_terraform.py"
    }
    # Terraform setup workflow - reusable workflow for Terraform operations
    ".github/workflows/terraform-setup.yml" = {
      all = "../../.github/workflows/terraform-setup.yml"
    }
    # Enterprise library files (10 required) - distributed to all repositories
    "scripts/lib/enterprise_audit.py" = {
      all = "../../scripts/lib/enterprise_audit.py"
    }
    "scripts/lib/audit_logger.py" = {
      all = "../../scripts/lib/audit_logger.py"
    }
    "scripts/lib/validation_framework.py" = {
      all = "../../scripts/lib/validation_framework.py"
    }
    "scripts/lib/unified_validation.py" = {
      all = "../../scripts/lib/unified_validation.py"
    }
    "scripts/lib/config_manager.py" = {
      all = "../../scripts/lib/config_manager.py"
    }
    "scripts/lib/security_validator.py" = {
      all = "../../scripts/lib/security_validator.py"
    }
    "scripts/lib/error_recovery.py" = {
      all = "../../scripts/lib/error_recovery.py"
    }
    "scripts/lib/transaction_manager.py" = {
      all = "../../scripts/lib/transaction_manager.py"
    }
    "scripts/lib/cli_framework.py" = {
      all = "../../scripts/lib/cli_framework.py"
    }
    # Enterprise readiness and setup scripts - distributed to all repositories
    "scripts/validate/check_enterprise_readiness.py" = {
      all = "../../scripts/validate/check_enterprise_readiness.py"
    }
    "scripts/automation/setup_enterprise_repo.py" = {
      all = "../../scripts/automation/setup_enterprise_repo.py"
    }
    ".github/workflows/codeql-analysis.yml" = {
      all = "../../templates/workflows/codeql-analysis.yml.template"
    }
    ".editorconfig" = {
      all = "../../templates/configs/.editorconfig"
    }
    "README.md" = {
      all = "../../templates/docs/required/template-README.md"
    }
  }

  # Generate file mappings for each enabled repository
  repository_files = flatten([
    for repo_name, repo_config in var.target_repositories : [
      for file_path, type_templates in local.base_templates : {
        key       = "${repo_name}/${file_path}"
        repo      = repo_name
        file_path = file_path
        template_path = try(
          type_templates[repo_config.repository_type],
          type_templates["all"],
          null
        )
      }
      if repo_config.enabled && try(
        type_templates[repo_config.repository_type],
        type_templates["all"],
        null
      ) != null
    ]
  ])

  # Convert to map for resource creation
  repository_file_map = {
    for item in local.repository_files :
    item.key => item
  }
}

# Manage repository files from templates
resource "github_repository_file" "template_files" {
  for_each = local.repository_file_map

  repository          = each.value.repo
  branch              = "main"
  file                = each.value.file_path
  content             = file("${path.module}/${each.value.template_path}")
  commit_message      = "chore: Update ${each.value.file_path} from MokoStandards template [skip ci]"
  commit_author       = "MokoStandards Automation"
  commit_email        = "automation@mokoconsulting.tech"
  overwrite_on_create = true
}

# Manage repository topics for categorization
resource "github_repository" "managed_repos" {
  for_each = {
    for name, config in var.target_repositories :
    name => config if config.enabled
  }

  name        = each.key
  description = data.github_repository.repos[each.key].description

  # Ensure standard topics are present
  topics = distinct(concat(
    data.github_repository.repos[each.key].topics,
    ["mokostandards-managed", each.value.repository_type]
  ))

  # Preserve existing settings
  visibility             = data.github_repository.repos[each.key].visibility
  has_issues             = data.github_repository.repos[each.key].has_issues
  has_projects           = data.github_repository.repos[each.key].has_projects
  has_wiki               = data.github_repository.repos[each.key].has_wiki
  allow_merge_commit     = true
  allow_squash_merge     = true
  allow_rebase_merge     = true
  delete_branch_on_merge = true

  # Security settings
  vulnerability_alerts = true
}

# Outputs
output "managed_repositories" {
  description = "List of repositories managed by this configuration"
  value = {
    for name, config in var.target_repositories :
    name => {
      type    = config.repository_type
      enabled = config.enabled
    }
  }
}

output "updated_files" {
  description = "Files updated in each repository"
  value = {
    for k, v in github_repository_file.template_files :
    k => {
      repository = v.repository
      file       = v.file
      commit_sha = v.commit_sha
    }
  }
}

output "repository_topics" {
  description = "Topics configured for each repository"
  value = {
    for name, repo in github_repository.managed_repos :
    name => repo.topics
  }
}
