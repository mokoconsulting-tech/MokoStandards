# Outputs for Terraform schema configuration


locals {
  # Metadata for this configuration
  # Enterprise-ready: Includes audit logging, monitoring, and compliance features
  config_metadata = {
    name              = "Outputs"
    description       = "Output definitions for Terraform configuration"
    version           = "03.02.00"
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

output "schema_version" {
  description = "Current schema version"
  value       = var.schema_version
}

output "repository_types" {
  description = "List of supported repository types"
  value = [
    "default",
    "library",
    "application"
  ]
}
