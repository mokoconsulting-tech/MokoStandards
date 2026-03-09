/**
 * MokoCRM Module Structure Definition
 * Standard repository structure for MokoCRM (Dolibarr) modules
 * 
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * Version: 1.0
 * Schema Version: 1.0
 */

locals {
  repository_structure = {
    metadata = {
      name             = "MokoCRM Module"
      description      = "Standard repository structure for MokoCRM (Dolibarr) modules"
      repository_type  = "crm-module"
      platform         = "dolibarr"
      last_updated     = "2026-01-07T00:00:00Z"
      maintainer       = "Moko Consulting"
      version          = "1.0"
      schema_version   = "1.0"
    }

    root_files = [
      {
        name              = "README.md"
        extension         = "md"
        description       = "Developer-focused documentation for contributors and maintainers"
        required          = true
        audience          = "developer"
        stub_content      = <<-EOT
# {MODULE_NAME}

## For Developers

This README is for developers contributing to this module.

### Development Setup

1. Clone this repository
2. Install dependencies: `make install-dev`
3. Run tests: `make test`

### Building

```bash
make build
```

### Testing

```bash
make test
make lint
```

### Contributing

See CONTRIBUTING.md for contribution guidelines.

## For End Users

End user documentation is available in `src/README.md` after installation.

## License

See LICENSE file for details.
EOT
      },
      {
        name              = "CONTRIBUTING.md"
        extension         = "md"
        description       = "Contribution guidelines"
        required          = true
        audience          = "contributor"
      },
      {
        name              = "ROADMAP.md"
        extension         = "md"
        description       = "Project roadmap with version goals and milestones"
        required          = false
        audience          = "general"
      },
      {
        name              = "LICENSE"
        extension         = ""
        description       = "License file (GPL-3.0-or-later) - Default for Dolibarr/CRM modules"
        required          = true
        audience          = "general"
        template          = "templates/licenses/GPL-3.0"
        license_type      = "GPL-3.0-or-later"
      },
      {
        name              = "CHANGELOG.md"
        extension         = "md"
        description       = "Version history and changes"
        required          = true
        audience          = "general"
      },
      {
        name                = "Makefile"
        description         = "Build automation using MokoStandards templates"
        required            = true
        always_overwrite    = true
        audience            = "developer"
        source_path         = "templates/makefiles"
        source_filename     = "Makefile.dolibarr.template"
        source_type         = "template"
        destination_path    = "."
        destination_filename = "Makefile"
        create_path         = false
        template            = "templates/makefiles/Makefile.dolibarr.template"
      },
      {
        name              = ".editorconfig"
        extension         = "editorconfig"
        description       = "Editor configuration for consistent coding style"
        required          = true
        audience          = "developer"
      },
      {
        name              = ".gitignore"
        extension         = "gitignore"
        description       = "Git ignore patterns - preserved during sync operations"
        required          = true
        always_overwrite  = false
        audience          = "developer"
      },
      {
        name              = ".gitattributes"
        extension         = "gitattributes"
        description       = "Git attributes configuration"
        required          = true
        audience          = "developer"
      },
      {
        name              = ".moko-standards"
        extension         = "yml"
        description       = "MokoStandards governance attachment — links this repo back to the standards source"
        required          = true
        always_overwrite  = true
        audience          = "developer"
        template          = "templates/configs/moko-standards.yml.template"
      }
    ]

    directories = [
      {
        name                = "src"
        path                = "src"
        description         = "Module source code for deployment"
        required            = true
        purpose             = "Contains the actual module code that gets deployed to Dolibarr"
        files = [
          {
            name              = "README.md"
            extension         = "md"
            description       = "End-user documentation deployed with the module"
            required          = true
            audience          = "end-user"
            stub_content      = <<-EOT
# {MODULE_NAME}

## For End Users

This module provides {MODULE_DESCRIPTION}.

### Installation

1. Navigate to Home → Setup → Modules/Applications
2. Find "{MODULE_NAME}" in the list
3. Click "Activate"

### Configuration

After activation, configure the module:
1. Go to Home → Setup → Modules/Applications
2. Click on the module settings icon
3. Configure as needed

### Usage

{USAGE_INSTRUCTIONS}

### Support

For support, contact: {SUPPORT_EMAIL}

## Version

Current version: {VERSION}

See CHANGELOG.md for version history.
EOT
          },
          {
            name              = "core/modules/mod{ModuleName}.class.php"
            extension         = "php"
            description       = "Main module descriptor file"
            required          = true
            audience          = "developer"
          }
        ]
        subdirectories = [
          {
            name                = "core"
            path                = "src/core"
            description         = "Core module files"
            required            = true
          },
          {
            name                = "langs"
            path                = "src/langs"
            description         = "Language translation files"
            required            = true
          },
          {
            name                = "sql"
            path                = "src/sql"
            description         = "Database schema files"
            requirement_status  = "suggested"
          },
          {
            name                = "css"
            path                = "src/css"
            description         = "Stylesheets"
            requirement_status  = "suggested"
          },
          {
            name                = "js"
            path                = "src/js"
            description         = "JavaScript files"
            requirement_status  = "suggested"
          },
          {
            name                = "class"
            path                = "src/class"
            description         = "PHP class files"
            requirement_status  = "suggested"
          },
          {
            name                = "lib"
            path                = "src/lib"
            description         = "Library files"
            requirement_status  = "suggested"
          }
        ]
      },
      {
        name                = "docs"
        path                = "docs"
        description         = "Developer and technical documentation"
        required            = true
        purpose             = "Contains technical documentation, API docs, architecture diagrams"
        files = [
          {
            name              = "index.md"
            extension         = "md"
            description       = "Documentation index"
            required          = true
          }
        ]
      },
      {
        name                = "scripts"
        path                = "scripts"
        description         = "Build and maintenance scripts"
        required            = true
        purpose             = "Contains scripts for building, testing, and deploying"
        files = [
          {
            name                = "index.md"
            extension           = "md"
            description         = "Scripts documentation"
            requirement_status  = "required"
          },
          {
            name                = "build_package.sh"
            extension           = "sh"
            description         = "Package building script for Dolibarr module"
            requirement_status  = "suggested"
            template            = "templates/scripts/release/package_dolibarr.sh"
          },
          {
            name                = "validate_module.sh"
            extension           = "sh"
            description         = "Module validation script"
            requirement_status  = "suggested"
            template            = "templates/scripts/validate/dolibarr_module.sh"
          },
          {
            name                = "MokoStandards.override.xml"
            extension           = "xml"
            description         = "MokoStandards sync override configuration"
            requirement_status  = "optional"
            always_overwrite    = false
          }
        ]
      },
      {
        name                = "tests"
        path                = "tests"
        description         = "Test files"
        required            = true
        purpose             = "Contains unit tests, integration tests, and test fixtures"
        subdirectories = [
          {
            name                = "unit"
            path                = "tests/unit"
            description         = "Unit tests"
            required            = true
          },
          {
            name                = "integration"
            path                = "tests/integration"
            description         = "Integration tests"
            requirement_status  = "suggested"
          }
        ]
      },
      {
        name                = "templates"
        path                = "templates"
        description         = "Template files for code generation"
        requirement_status  = "suggested"
        purpose             = "Contains templates used by build scripts"
      },
      {
        name                = ".github"
        path                = ".github"
        description         = "GitHub-specific configuration"
        requirement_status  = "suggested"
        purpose             = "Contains GitHub Actions workflows, issue templates, etc."
        files = [
          {
            name                = "copilot.yml"
            extension           = "yml"
            description         = "GitHub Copilot allowed domains configuration"
            requirement_status  = "required"
            always_overwrite    = true
            template            = ".github/copilot.yml"
          },
          {
            name                = "copilot-instructions.md"
            extension           = "md"
            description         = "GitHub Copilot custom instructions enforcing MokoStandards"
            requirement_status  = "required"
            always_overwrite    = false
            destination_path    = ".github"
            destination_filename = "copilot-instructions.md"
            template            = "templates/github/copilot-instructions.md.template"
          },
          {
            name                = "CLAUDE.md"
            extension           = "md"
            description         = "Claude AI assistant context enforcing MokoStandards"
            requirement_status  = "required"
            always_overwrite    = false
            destination_path    = ".github"
            destination_filename = "CLAUDE.md"
            template            = "templates/github/CLAUDE.md.template"
          }
        ]
        subdirectories = [
          {
            name                = "workflows"
            path                = ".github/workflows"
            description         = "GitHub Actions workflows"
            requirement_status  = "required"
            files = [
              {
                name                = "ci-dolibarr.yml"
                extension           = "yml"
                description         = "Dolibarr-specific CI workflow"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/workflows/dolibarr/ci-dolibarr.yml.template"
              },
              {
                name                = "codeql-analysis.yml"
                extension           = "yml"
                description         = "CodeQL security analysis workflow"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/workflows/generic/codeql-analysis.yml.template"
              },
              {
                name                = "standards-compliance.yml"
                extension           = "yml"
                description         = "MokoStandards compliance validation"
                requirement_status  = "required"
                always_overwrite    = true
                template            = ".github/workflows/standards-compliance.yml"
              },
              {
                name                = "enterprise-firewall-setup.yml"
                extension           = "yml"
                description         = "Enterprise firewall configuration for trusted domain access"
                requirement_status  = "required"
                always_overwrite    = true
                template            = "templates/workflows/shared/enterprise-firewall-setup.yml.template"
              }
            ]
          }
        ]
      },
      {
        name                = "img"
        path                = "img"
        description         = "Module image assets including Dolibarr picto"
        requirement_status  = "required"
        purpose             = "Contains the module picto displayed in the Dolibarr UI"
        files = [
          {
            name                = "object_mokoconsulting.png"
            extension           = "png"
            description         = "Moko Consulting picto shown in Dolibarr module list"
            requirement_status  = "required"
            always_overwrite    = true
            template            = "templates/build/dolibarr/img/object_mokoconsulting.png"
          }
        ]
      }
    ]
  }
}
