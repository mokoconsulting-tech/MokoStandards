# Copilot Prompt: Migrate Schema System from XML/JSON to Terraform

Use this prompt with GitHub Copilot to migrate repository schemas from XML/JSON format to Terraform configuration in any repository.

---

## Prompt for Copilot

```
Convert the schema system to Terraform, recreating schema defaults to terraform definition files, removing legacy schema files, completely shutdown schema, and update all scripts accordingly.

Follow this migration pattern:

### 1. Create Terraform Directory Structure

Create the following directory structure:
```
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── README.md
└── repository-types/
    ├── repo-health-defaults.tf
    └── default-repository.tf
```

### 2. Convert Repository Health Schema

If you have a `schemas/repo-health-default.xml` or similar health configuration:

**Create `terraform/repository-types/repo-health-defaults.tf`:**

Convert XML health check configuration to Terraform locals format:
- `metadata` - configuration metadata
- `scoring` - total points and scoring rules
- `categories` - health check categories (CI/CD, Documentation, Security, etc.)
- `thresholds` - health level thresholds (excellent, good, fair, poor)
- `checks` - individual health checks organized by category

Use Terraform `locals` blocks for configuration and `output` blocks to expose the data.

Example structure:
```hcl
locals {
  repo_health_metadata = {
    name = "Repository Health Configuration"
    # ... metadata fields
  }
  
  categories = {
    ci_cd_status = {
      id = "ci-cd-status"
      name = "CI/CD Status"
      max_points = 15
      # ...
    }
    # ... more categories
  }
  
  ci_cd_checks = {
    ci_workflow_present = {
      id = "ci-workflow-present"
      name = "CI workflow present"
      points = 5
      check_type = "file-exists"
      category = "ci-cd-status"
      parameters = {
        file_path = ".github/workflows/ci.yml"
      }
      # ...
    }
    # ... more checks
  }
}

output "repo_health_config" {
  value = {
    metadata = local.repo_health_metadata
    scoring = local.scoring
    categories = local.categories
    thresholds = local.thresholds
    checks = merge(
      local.ci_cd_checks,
      local.documentation_checks,
      # ... merge all check categories
    )
  }
}
```

### 3. Convert Repository Structure Schema

If you have `schemas/repository-structure.schema.json` or similar:

**Create `terraform/repository-types/default-repository.tf`:**

Convert JSON structure definition to Terraform locals:
- `metadata` - repository type information
- `root_files` - expected files at repository root
- `directories` - directory structure with subdirectories

Example structure:
```hcl
locals {
  default_repo_metadata = {
    name = "Default Repository Structure"
    repository_type = "library"
    # ...
  }
  
  default_root_files = {
    readme = {
      name = "README.md"
      requirement_status = "required"
      description = "Project documentation"
      # ...
    }
    # ... more files
  }
  
  default_directories = {
    github = {
      name = ".github"
      path = ".github"
      requirement_status = "required"
      subdirectories = {
        workflows = {
          name = "workflows"
          path = ".github/workflows"
          requirement_status = "required"
        }
      }
    }
    # ... more directories
  }
}

output "default_repository_structure" {
  value = {
    metadata = local.default_repo_metadata
    root_files = local.default_root_files
    directories = local.default_directories
  }
}
```

### 4. Create Main Terraform Configuration

**Create `terraform/main.tf`:**
```hcl
terraform {
  required_version = ">= 1.0"
}

module "default_repository" {
  source = "./repository-types"
}

output "repository_schemas" {
  description = "All repository structure schemas"
  value = module.default_repository
}
```

**Create `terraform/variables.tf`:**
```hcl
variable "schema_version" {
  description = "Version of the schema specification"
  type        = string
  default     = "2.0"
}

variable "enable_strict_validation" {
  description = "Enable strict validation mode"
  type        = bool
  default     = false
}
```

**Create `terraform/outputs.tf`:**
```hcl
output "schema_version" {
  description = "Current schema version"
  value       = var.schema_version
}

output "repository_types" {
  description = "List of supported repository types"
  value = ["default", "library", "application"]
}
```

### 5. Create Python Integration Module

**Create `scripts/lib/terraform_schema_reader.py`:**

This module reads Terraform outputs and provides a Python API:

```python
#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

class TerraformSchemaReader:
    def __init__(self, terraform_dir: str = None):
        if terraform_dir is None:
            terraform_dir = self._find_terraform_dir()
        self.terraform_dir = Path(terraform_dir).resolve()
        self._cache = {}
    
    def _find_terraform_dir(self) -> Path:
        # Search for .git directory to find project root
        current = Path(__file__).resolve().parent
        while current != current.parent:
            if (current / '.git').exists():
                terraform_path = current / 'terraform'
                if terraform_path.exists():
                    return terraform_path
            current = current.parent
        return Path('terraform')
    
    def _run_terraform_output(self, output_name: Optional[str] = None) -> Dict[str, Any]:
        cache_key = output_name or '__all__'
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        cmd = ['terraform', 'output', '-json']
        if output_name:
            cmd.append(output_name)
        
        result = subprocess.run(cmd, cwd=self.terraform_dir, 
                              capture_output=True, text=True, check=True)
        output = json.loads(result.stdout)
        
        if output_name and 'value' in output:
            output = output['value']
        
        self._cache[cache_key] = output
        return output
    
    def get_health_config(self) -> Dict[str, Any]:
        output = self._run_terraform_output()
        if 'repository_schemas' in output and 'value' in output['repository_schemas']:
            schemas = output['repository_schemas']['value']
            if 'repo_health_config' in schemas:
                return schemas['repo_health_config']
        return self._get_fallback_health_config()
    
    def get_repository_structure(self, repo_type: str = 'default') -> Dict[str, Any]:
        output = self._run_terraform_output()
        if 'repository_schemas' in output and 'value' in output['repository_schemas']:
            schemas = output['repository_schemas']['value']
            if 'default_repository_structure' in schemas:
                return schemas['default_repository_structure']
        return self._get_fallback_structure()
    
    def _get_fallback_health_config(self) -> Dict[str, Any]:
        return {
            'metadata': {'name': 'Health Config', 'version': '2.0'},
            'scoring': {'total_points': 100},
            'categories': {},
            'thresholds': {},
            'checks': {}
        }
    
    def _get_fallback_structure(self) -> Dict[str, Any]:
        return {
            'metadata': {'name': 'Default Structure'},
            'root_files': {},
            'directories': {}
        }
```

### 6. Update Validation Scripts

For scripts that read XML schemas (like `scripts/validate/check_repo_health.py`):

**Before:**
```python
from xml.etree import ElementTree as ET

tree = ET.parse('schemas/repo-health-default.xml')
config = tree.getroot()
# Parse XML...
```

**After:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from terraform_schema_reader import TerraformSchemaReader

reader = TerraformSchemaReader()
config = reader.get_health_config()
# Use config dictionary directly
```

Update the script to:
1. Import `TerraformSchemaReader` instead of XML parsing
2. Call `reader.get_health_config()` or `reader.get_repository_structure()`
3. Access configuration as Python dictionaries instead of XML elements
4. Update parameter names from XML format (e.g., `file-path` → `file_path`)

### 7. Remove Legacy Schema Files

Delete the following files:
- `schemas/*.xml` (e.g., repo-health-default.xml)
- `schemas/*.xsd` (e.g., repo-health.xsd, repository-structure.xsd)
- `schemas/*.json` (e.g., repository-structure.schema.json, unified-repository-schema.json)

### 8. Create Deprecation Notice

**Create `schemas/README.md`:**
```markdown
# Schema Directory - DEPRECATED

**Status**: DEPRECATED - Migrated to Terraform

The schema system has been migrated from XML/JSON to Terraform configuration.

## Migration

All schema definitions moved to: `terraform/repository-types/`

- Health checks: `terraform/repository-types/repo-health-defaults.tf`
- Repository structure: `terraform/repository-types/default-repository.tf`

## For Developers

Use the new Python API:

\`\`\`python
from terraform_schema_reader import TerraformSchemaReader

reader = TerraformSchemaReader()
health_config = reader.get_health_config()
structure = reader.get_repository_structure('default')
\`\`\`

See `terraform/README.md` for complete documentation.
```

### 9. Update Documentation

Update the following files to reflect the migration:

**README.md:**
- Replace references to `schemas/` with `terraform/`
- Update schema format description from "XML/JSON" to "Terraform"

**CHANGELOG.md:**
```markdown
## [UNRELEASED]
### Changed - Schema Migration to Terraform
- **BREAKING CHANGE**: Migrated schema system from XML/JSON to Terraform
  - Removed legacy schema files (schemas/*.xml, *.xsd, *.json)
  - Added terraform/ directory with Terraform-based definitions
  - Added scripts/lib/terraform_schema_reader.py for Python integration
  - Updated validation scripts to use Terraform
  - Schema version upgraded to 2.0
```

### 10. Add Terraform to .gitignore

Add these patterns to `.gitignore`:
```
# Terraform
**/.terraform/*
*.tfstate
*.tfstate.*
*.tfvars
*.tfvars.json
override.tf
override.tf.json
*_override.tf
*_override.tf.json
.terraformrc
terraform.rc
*.tfplan
```

### 11. Initialize and Test

Run these commands:
```bash
cd terraform
terraform init
terraform validate
terraform fmt -recursive
terraform output -json
```

Test Python integration:
```bash
python3 scripts/lib/terraform_schema_reader.py
```

Test updated validation scripts:
```bash
python3 scripts/validate/check_repo_health.py --repo-path . --verbose
```

### Benefits of This Migration

1. **Infrastructure as Code**: Schemas treated as infrastructure
2. **Type Safety**: Built-in validation and type checking
3. **Version Control**: Better diff and merge support
4. **Tooling**: Terraform ecosystem (fmt, validate, plan)
5. **Maintainability**: Cleaner, more readable configuration
6. **Industry Standard**: Common IaC approach

### Notes

- This converts schemas to Terraform configuration format
- No actual infrastructure is created (Terraform used as config store)
- Python scripts read Terraform outputs via subprocess
- Backward compatibility maintained where possible
- Mark incomplete features with TODO comments
```

---

## Usage Instructions

1. Copy this entire prompt text
2. Open the repository where you want to apply the migration
3. Paste the prompt to GitHub Copilot Chat
4. Copilot will guide you through creating the Terraform configuration
5. Review and test each step before proceeding

## Expected Results

- Terraform configuration in `terraform/` directory
- Python integration module for reading Terraform outputs
- Updated validation scripts using Terraform instead of XML
- Removed legacy XML/XSD/JSON schema files
- Updated documentation reflecting the migration

## Troubleshooting

If Terraform is not installed:
```bash
# Ubuntu/Debian
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

If Python can't find terraform_schema_reader:
- Ensure `scripts/lib/terraform_schema_reader.py` exists
- Add `scripts/lib` to Python path: `sys.path.insert(0, 'scripts/lib')`

---

**Migration Reference**: Based on MokoStandards PR - Schema to Terraform migration
