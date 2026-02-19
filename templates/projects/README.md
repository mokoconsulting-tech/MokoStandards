<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: GitHub.Projects
INGROUP: MokoStandards.Standards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /templates/projects/README.md
VERSION: 04.00.01
BRIEF: GitHub Projects v2 setup standard with remote template selection
-->

# GitHub Projects v2 Setup Standard

## Purpose

This standard defines the configuration, structure, and governance for GitHub Projects v2 used across MokoStandards-governed repositories. It provides JSON/XML-based templates and a script system for remote selection and automated project generation.

## Quick Start

### Create a New Project

```bash
# Interactive mode - select template from menu
python3 scripts/project_manager.py create

# Direct template selection
python3 scripts/project_manager.py create --template joomla --name "MokoForms Component"

# From remote URL
python3 scripts/project_manager.py create --remote-url https://github.com/mokoconsulting-tech/MokoStandards/raw/main/templates/projects/joomla-project-config.json
```

### Update an Existing Project

```bash
# Interactive mode
python3 scripts/project_manager.py update --project-number 42

# Update with specific template
python3 scripts/project_manager.py update --project-number 42 --template dolibarr
```

### List Available Templates

```bash
python3 scripts/project_manager.py list-templates
```

## Project Types

### 1. Joomla Extension Projects
Track development of Joomla components, modules, plugins, libraries, packages, and templates.

**Configuration:** [joomla-project-config.json](./joomla-project-config.json)

**Custom Fields:**
- Joomla Version Compatibility
- Extension Type
- Marketplace Status
- Update Server URL
- Extension Version

### 2. Dolibarr Module Projects
Manage Dolibarr ERP/CRM module development and deployment lifecycle.

**Configuration:** [dolibarr-project-config.json](./dolibarr-project-config.json)

**Custom Fields:**
- Dolibarr Version Compatibility
- Module Number
- Database Changes Required
- Module Descriptor Path
- Module Version

### 3. Generic Development Projects
General-purpose project management for any technology stack.

**Configuration:** [generic-project-config.json](./generic-project-config.json)

**Custom Fields:**
- Technology Stack
- Environment
- Release Channel
- API Version
- Deployment Status

### 4. Documentation Governance Projects
Control register for documentation artifacts and compliance tracking.

**Configuration:** [documentation-project-config.json](./documentation-project-config.json)

**Custom Fields:**
- Document Type
- Document Subtype
- Review Cycle
- Compliance Tags
- Retention Policy

## Configuration Formats

### JSON Format

All project templates are provided in JSON format for easy parsing and automation:

```json
{
  "project": {
    "name": "Project Name",
    "description": "Project description",
    "visibility": "private"
  },
  "custom_fields": [...],
  "views": [...],
  "workflows": [...]
}
```

### XML Format

Equivalent XML configurations are also provided for teams preferring XML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<github-project version="2.0">
  <metadata>...</metadata>
  <custom-fields>...</custom-fields>
  <views>...</views>
  <workflows>...</workflows>
</github-project>
```

## Script System

### project_manager.py

Main script for managing GitHub Projects v2:

**Features:**
- Create new projects from templates
- Update existing projects with new fields
- List available templates (local and remote)
- Import templates from remote URLs
- Export existing project configurations
- Dry-run mode for testing
- Verbose logging for debugging

**Usage:**
```bash
# Create project
python3 scripts/project_manager.py create [OPTIONS]

# Update project
python3 scripts/project_manager.py update --project-number N [OPTIONS]

# List templates
python3 scripts/project_manager.py list-templates [--remote]

# Export configuration
python3 scripts/project_manager.py export --project-number N --output config.json
```

**Options:**
- `--template TYPE` - Template type (joomla, dolibarr, generic, documentation)
- `--name NAME` - Project name
- `--remote-url URL` - Load template from remote URL
- `--config FILE` - Load template from local file
- `--dry-run` - Test without making changes
- `--verbose` - Enable detailed logging
- `--org ORG` - Organization name (default: mokoconsulting-tech)

### template_validator.py

Validates JSON/XML template configurations:

```bash
# Validate JSON template
python3 scripts/template_validator.py templates/projects/joomla-project-config.json

# Validate XML template
python3 scripts/template_validator.py templates/projects/joomla-project-config.xml

# Validate all templates
python3 scripts/template_validator.py --all
```

### field_migrator.py

Migrates fields between projects or updates field definitions:

```bash
# Copy fields from one project to another
python3 scripts/field_migrator.py --from-project 10 --to-project 20

# Update field options in existing project
python3 scripts/field_migrator.py --project 15 --field-config fields.json
```

## Remote Template Selection

### Template Registry

Templates can be loaded from:

1. **Local files:** Templates in `templates/projects/` directory
2. **GitHub URLs:** Direct links to raw JSON/XML files
3. **Template registry:** Central registry of approved templates

### Loading Remote Templates

```bash
# From GitHub raw URL
python3 scripts/project_manager.py create \
  --remote-url https://github.com/mokoconsulting-tech/MokoStandards/raw/main/templates/projects/joomla-project-config.json \
  --name "My Joomla Component"

# From template registry
python3 scripts/project_manager.py create \
  --template-id moko-joomla-v1 \
  --name "My Joomla Component"
```

### Template Registry Format

The template registry (`template-registry.json`) maintains a list of approved templates:

```json
{
  "templates": [
    {
      "id": "moko-joomla-v1",
      "name": "Joomla Extension Project",
      "description": "Standard project for Joomla extension development",
      "version": "1.0.0",
      "url": "https://github.com/mokoconsulting-tech/MokoStandards/raw/main/templates/projects/joomla-project-config.json",
      "type": "joomla",
      "tags": ["joomla", "extension", "development"]
    },
    {
      "id": "moko-dolibarr-v1",
      "name": "Dolibarr Module Project",
      "description": "Standard project for Dolibarr module development",
      "version": "1.0.0",
      "url": "https://github.com/mokoconsulting-tech/MokoStandards/raw/main/templates/projects/dolibarr-project-config.json",
      "type": "dolibarr",
      "tags": ["dolibarr", "module", "erp", "crm"]
    }
  ]
}
```

## Standard Custom Fields

### Core Fields (All Project Types)

Every project includes these standard fields:

| Field Name | Type | Options/Format |
|------------|------|----------------|
| Status | Single Select | Backlog, Todo, In Progress, In Review, Testing, Done, Blocked, Cancelled |
| Priority | Single Select | Critical, High, Medium, Low |
| Size/Effort | Single Select | XS, S, M, L, XL, XXL |
| Sprint | Text | Sprint NN or YYYY-MM-DD |
| Target Version | Text | Semantic version (e.g., 1.2.3) |
| Blocked Reason | Text | Description of blocker |
| Acceptance Criteria | Text | List of criteria for completion |

### Joomla-Specific Fields

| Field Name | Type | Options/Format |
|------------|------|----------------|
| Joomla Version | Single Select | 3.10, 4.4, 5.0, 5.1 |
| Extension Type | Single Select | Component, Module, Plugin, Library, Package, Template |
| Marketplace Status | Single Select | Not Published, In Review, Published, Rejected |
| Update Server URL | Text | URL to update XML |
| Extension Version | Text | Semantic version |
| PHP Minimum | Single Select | 7.4, 8.0, 8.1, 8.2 |
| Installation Type | Single Select | Fresh Install, Update, Migration |

### Dolibarr-Specific Fields

| Field Name | Type | Options/Format |
|------------|------|----------------|
| Dolibarr Version | Single Select | 16.0, 17.0, 18.0, 19.0 |
| Module Number | Number | 100000 - 999999 |
| Database Changes | Single Select | None, Schema Only, Data Migration, Both |
| Module Descriptor | Text | Path to modMyModule.class.php |
| Module Version | Text | Semantic version |
| PHP Minimum | Single Select | 7.4, 8.0, 8.1, 8.2 |
| Requires Sudo | Single Select | Yes, No |

### Generic Development Fields

| Field Name | Type | Options/Format |
|------------|------|----------------|
| Technology Stack | Text | Languages/frameworks used |
| Environment | Single Select | Development, Staging, Production |
| Release Channel | Single Select | Alpha, Beta, RC, Stable |
| API Version | Text | API version number |
| Deployment Status | Single Select | Not Deployed, Deployed, Failed, Rollback |
| Infrastructure | Single Select | On-Premise, Cloud, Hybrid |
| Database Type | Single Select | MySQL, PostgreSQL, MongoDB, Redis, None |

## Standard Views

### Required Views (All Projects)

1. **Master Backlog** (Table)
   - All items ordered by priority
   - Columns: Title, Status, Priority, Size, Assignee, Sprint

2. **Sprint Board** (Board)
   - Group by Status
   - Filter: Current sprint only
   - Columns: Backlog, Todo, In Progress, In Review, Testing, Done

3. **Release Roadmap** (Roadmap)
   - Group by Target Version
   - Timeline view of releases

4. **Blocked Items** (Table)
   - Filter: Status = Blocked
   - Columns: Title, Priority, Blocked Reason, Assignee, Days Blocked

### Joomla-Specific Views

5. **Extension Compatibility Matrix** (Table)
   - Group by Joomla Version
   - Filter: Extension-specific items

6. **Marketplace Pipeline** (Board)
   - Group by Marketplace Status
   - Track submission and review process

### Dolibarr-Specific Views

5. **Module Compatibility Matrix** (Table)
   - Group by Dolibarr Version
   - Filter: Module-specific items

6. **Database Migration Tracker** (Table)
   - Filter: Database Changes != None
   - Track schema changes and migrations

### Generic Development Views

5. **Deployment Pipeline** (Board)
   - Group by Deployment Status
   - Track deployment progress

6. **Technology Stack View** (Table)
   - Group by Technology Stack
   - Overview of tech diversity

## Workflows and Automation

### Standard Automations

All projects should implement:

1. **Auto-status on PR creation** → Set to "In Review"
2. **Auto-status on PR merge** → Set to "Testing"
3. **Auto-status on PR close** → Set to "Blocked" or "Cancelled"
4. **Stale item detection** → Flag items blocked > 7 days
5. **Sprint rollover** → Move incomplete items to next sprint

### Project-Specific Automations

**Joomla Projects:**
- Update Extension Version field when release tag is created
- Sync Marketplace Status with release workflow
- Validate PHP minimum version compatibility

**Dolibarr Projects:**
- Validate Module Number uniqueness
- Alert on database schema changes
- Check module descriptor syntax

**Generic Projects:**
- Sync deployment status with CI/CD pipeline
- Alert on failed deployments
- Track API version compatibility

## Implementation Guide

### Step 1: Choose Template

```bash
# List available templates
python3 scripts/project_manager.py list-templates

# Output:
# Available Project Templates:
#
# 1. joomla - Joomla Extension Project
#    Description: Standard project for Joomla extension development
#    Config: templates/projects/joomla-project-config.json
#
# 2. dolibarr - Dolibarr Module Project
#    Description: Standard project for Dolibarr module development
#    Config: templates/projects/dolibarr-project-config.json
#
# 3. generic - Generic Development Project
#    Description: General-purpose project for any technology stack
#    Config: templates/projects/generic-project-config.json
#
# 4. documentation - Documentation Governance Project
#    Description: Control register for documentation artifacts
#    Config: templates/projects/documentation-project-config.json
```

### Step 2: Create Project

```bash
# Interactive mode
python3 scripts/project_manager.py create

# Direct creation
python3 scripts/project_manager.py create \
  --template joomla \
  --name "MokoForms Component" \
  --description "Joomla 5.x forms component with advanced validation"
```

### Step 3: Configure Automations

After project creation, configure GitHub Actions automations:

```bash
# Copy automation workflow
cp templates/workflows/github-projects-automation.yml .github/workflows/

# Edit workflow to specify project number
# PROJECT_NUMBER: 42  # Update with your project number
```

### Step 4: Populate Initial Items

```bash
# Import issues from milestone
python3 scripts/project_manager.py import-issues \
  --project-number 42 \
  --milestone "v1.0.0"

# Import from CSV
python3 scripts/project_manager.py import-csv \
  --project-number 42 \
  --csv-file backlog.csv
```

## Best Practices

### Project Setup

1. **Start from template** - Always use standard templates
2. **Customize minimally** - Only add fields if absolutely necessary
3. **Document deviations** - Explain why you deviated from standard
4. **Test first** - Use `--dry-run` flag before making changes
5. **Version control** - Keep project configuration in Git

### Field Management

1. **Don't delete fields** - Archive or hide unused fields instead
2. **Validate data** - Use single-select for controlled values
3. **Use consistent naming** - Follow field naming conventions
4. **Document field purpose** - Add descriptions to custom fields
5. **Regular cleanup** - Remove obsolete field values

### View Organization

1. **Limit views** - Don't create too many views (max 10-12)
2. **Clear naming** - View names should be self-explanatory
3. **Filter strategically** - Use filters to reduce noise
4. **Sort meaningfully** - Default sort should make sense
5. **Share views** - Make important views accessible to team

### Automation Guidelines

1. **Test thoroughly** - Automations can cause cascading issues
2. **Handle errors** - Build in error handling and notifications
3. **Log changes** - Keep audit trail of automated changes
4. **Review regularly** - Ensure automations still make sense
5. **Avoid conflicts** - Don't create competing automations

## Troubleshooting

### Common Issues

**Issue:** "Project not found"
**Solution:** Verify project number and organization permissions

**Issue:** "Field already exists"
**Solution:** Use update mode or skip existing fields

**Issue:** "Remote template not accessible"
**Solution:** Check URL and network connectivity

**Issue:** "Invalid template format"
**Solution:** Validate template with `template_validator.py`

### Debug Mode

```bash
# Enable verbose logging
python3 scripts/project_manager.py create \
  --template joomla \
  --name "Test Project" \
  --verbose \
  --dry-run
```

### Support

For issues or questions:
1. Check documentation in `docs/guide/`
2. Review script help: `python3 scripts/project_manager.py --help`
3. Open issue in MokoStandards repository
4. Contact project governance team

## Files and Structure

```
templates/projects/
├── README.md                           # This file
├── github-projects-v2-standard.md     # Detailed standard document
├── joomla-project-config.json         # Joomla template (JSON)
├── joomla-project-config.xml          # Joomla template (XML)
├── dolibarr-project-config.json       # Dolibarr template (JSON)
├── dolibarr-project-config.xml        # Dolibarr template (XML)
├── generic-project-config.json        # Generic template (JSON)
├── generic-project-config.xml         # Generic template (XML)
├── documentation-project-config.json  # Documentation template (JSON)
├── documentation-project-config.xml   # Documentation template (XML)
├── template-registry.json             # Template registry
└── index.md                           # Auto-generated index

scripts/
├── project_manager.py                 # Main project management script
├── template_validator.py              # Template validation script
├── field_migrator.py                  # Field migration script
└── export_project_config.py           # Export existing project config

.github/workflows/
└── github-projects-automation.yml     # Project automation workflow
```

## Metadata

| Field      | Value                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| Document   | GitHub Projects v2 Setup Standard                                                                           |
| Path       | /templates/projects/README.md                                                                               |
| Repository | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner      | Moko Consulting                                                                                              |
| Status     | Active                                                                                                       |
| Effective  | 2026-01-04                                                                                                   |

## Version History

| Version  | Date       | Changes                                          |
| -------- | ---------- | ------------------------------------------------ |
| 01.00.00 | 2026-01-04 | Initial GitHub Projects v2 standard with remote template selection |
