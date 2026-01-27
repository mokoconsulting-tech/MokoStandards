# Terraform configuration for MokoStandards repository schemas
# This replaces the legacy XML/JSON schema system with Terraform-based configuration

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
  value = module.default_repository
}
