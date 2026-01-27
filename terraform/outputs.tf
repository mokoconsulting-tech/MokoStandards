# Outputs for Terraform schema configuration

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
