# Terraform configuration for MokoStandards repository schemas
# This replaces the legacy XML/JSON schema system with Terraform-based configuration

locals {
  # Metadata for this configuration
  # Enterprise-ready: Includes audit logging, monitoring, and compliance features
  config_metadata = {
    name              = "MokoStandards Repository Schemas"
    description       = "Terraform configuration for repository structure schemas and type definitions"
    version           = "04.00.01"
    last_updated      = "2026-02-11"
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

terraform {
  required_version = ">= 1.0"
}

# Load repository type definitions
module "default_repository" {
  source = "./repository-types"
}

# Output combined configuration
output "repository_schemas" {
  description = "All repository structure schemas"
  value       = module.default_repository
}
