# GitHub Copilot Integration Guide for Repository Sync

**Version**: 1.0.0  
**Date**: 2026-01-18  
**Status**: Production Ready

## Overview

The MokoStandards repository sync now includes GitHub Copilot integration for AI-powered file generation and customization. This allows the sync process to automatically adapt files to specific repository contexts, platforms, and requirements.

## Features

### 1. AI-Powered File Customization

Copilot can customize files based on:
- Repository name and type
- Platform (Joomla, Dolibarr, generic)
- Existing repository context
- Custom prompts in schema definitions

### 2. Supported File Types

The following files can be customized with Copilot:
- **README files** - Automatic content generation based on repo type
- **Workflow files** - CI/CD customization (ci.yml, deploy, release, build.yml)
- **Configuration files** - .editorconfig, CONTRIBUTING.md, CODE_OF_CONDUCT.md

### 3. Workflow-Dependent Scripts

Scripts required by GitHub Actions workflows are automatically marked as:
- `requirement-status: required`
- `always-overwrite: true`
- `workflow-dependency: true`

This ensures critical dependencies are always present and up-to-date.

### 4. Override Schema Generation

Each synced repository receives a `scripts/repository-structure-override.xml` file with:
- Template for repository-specific customizations
- Examples for overriding file requirements
- Copilot prompt examples
- Platform-specific adaptations

## Installation

### Prerequisites

1. **GitHub CLI** (required)
   ```bash
   # Install GitHub CLI
   # macOS
   brew install gh
   
   # Linux
   sudo apt install gh
   
   # Windows
   winget install GitHub.cli
   ```

2. **GitHub Copilot CLI Extension** (optional, for Copilot features)
   ```bash
   gh extension install github/gh-copilot
   ```

3. **Python Dependencies**
   ```bash
   pip install pyyaml defusedxml
   ```

## Usage

### Basic Sync (Without Copilot)

```bash
# Sync to all organization repositories
python3 scripts/automation/bulk_update_repos.py --yes

# Sync to specific repositories
python3 scripts/automation/bulk_update_repos.py --repos repo1 repo2

# Dry run to preview changes
python3 scripts/automation/bulk_update_repos.py --dry-run
```

### Sync with Copilot Customization

```bash
# Enable Copilot for AI-powered customization
python3 scripts/automation/bulk_update_repos.py --use-copilot --yes

# Dry run with Copilot
python3 scripts/automation/bulk_update_repos.py --use-copilot --dry-run

# Sync specific repos with Copilot
python3 scripts/automation/bulk_update_repos.py --use-copilot --repos myrepo --yes
```

### Via GitHub Actions Workflow

The bulk-repo-sync workflow can be triggered manually:

1. Go to Actions → Bulk Repository Sync
2. Click "Run workflow"
3. Optional inputs:
   - **repos**: Space-separated list of specific repos
   - **exclude**: Space-separated list of repos to exclude
   - **dry_run**: Preview changes without applying
   - **use_copilot**: Enable AI-powered customization ✨

## Schema Configuration

### Marking Files for Copilot Customization

In your repository structure definition XML:

```xml
<file extension="md">
  <name>README.md</name>
  <description>Project README</description>
  <requirement-status>required</requirement-status>
  
  <!-- Enable Copilot customization -->
  <copilot-enabled>true</copilot-enabled>
  
  <!-- Optional: Custom prompt for this file -->
  <copilot-prompt>
    Generate a comprehensive README for a Joomla component
    that handles user authentication and permissions.
    Include installation instructions, configuration, and usage examples.
  </copilot-prompt>
</file>
```

### Marking Workflow Dependencies

For scripts required by GitHub Actions workflows:

```xml
<file extension="sh">
  <name>validate_structure.sh</name>
  <description>Repository structure validation (required by CI workflow)</description>
  
  <!-- Mark as workflow dependency -->
  <requirement-status>required</requirement-status>
  <always-overwrite>true</always-overwrite>
  <workflow-dependency>true</workflow-dependency>
  
  <template>templates/scripts/validate/structure.sh</template>
</file>
```

### JSON Schema Configuration

In JSON format:

```json
{
  "name": "README.md",
  "description": "Project README",
  "requirementStatus": "required",
  "copilotEnabled": true,
  "copilotPrompt": "Generate README for a Python library that...",
  "workflowDependency": false
}
```

## Override Schema

After sync, each repository will have `scripts/repository-structure-override.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<repository-structure xmlns="http://mokoconsulting.com/schemas/repository-structure"
                      version="2.0"
                      schema-version="2.0">
  <metadata>
    <name>MyRepo Override Schema</name>
    <description>Repository-specific overrides for MyRepo</description>
    <repository-type>library</repository-type>
    <platform>multi-platform</platform>
    <last-updated>2026-01-18T00:00:00Z</last-updated>
    <maintainer>Repository Maintainers</maintainer>
  </metadata>

  <structure>
    <root-files>
      <!-- Override specific files -->
      <file extension="md">
        <name>README.md</name>
        <copilot-enabled>true</copilot-enabled>
        <copilot-prompt>
          Generate README for MyRepo, emphasizing security features
          and enterprise deployment scenarios
        </copilot-prompt>
      </file>
    </root-files>
  </structure>
</repository-structure>
```

## Copilot Helper API

### Python API

```python
from copilot_helper import create_copilot_helper

# Initialize
helper = create_copilot_helper({
    'name': 'my-repo',
    'type': 'library',
    'platform': 'multi-platform'
})

# Check availability
if helper.is_available():
    # Generate README section
    success, content = helper.generate_readme_section(
        "Installation",
        {'name': 'my-library', 'type': 'python'}
    )
    
    # Customize file
    success, content = helper.customize_file(
        'README.md',
        {'platform': 'joomla'},
        'joomla'
    )
    
    # Get workflow suggestions
    success, suggestions = helper.suggest_workflow_improvements(
        '.github/workflows/ci.yml'
    )
```

## How It Works

### 1. Repository Detection

When sync runs:
1. Clones target repository
2. Detects platform type (Joomla/Dolibarr/generic)
3. Loads appropriate schema definition
4. Checks for existing override schema

### 2. Copilot Processing

For files marked with `copilot-enabled`:
1. Reads source template
2. Gathers repository context
3. Builds AI prompt with context + custom prompt
4. Calls GitHub Copilot CLI
5. Extracts generated content
6. Writes customized file

### 3. Workflow Dependencies

Files with `workflow-dependency: true`:
1. Always required (cannot be skipped)
2. Always overwritten (ensures latest version)
3. Validated before commit
4. Logged in sync report

### 4. Override Schema

On each sync:
1. Checks for `scripts/repository-structure-override.xml`
2. If not exists, generates template
3. If exists, preserves existing content
4. Includes platform-specific examples
5. Documents available customization options

## Best Practices

### When to Use Copilot

✅ **Use Copilot for**:
- README files (context-specific documentation)
- Contributing guidelines (repo-specific processes)
- Configuration files (environment-specific settings)
- Workflow files that vary by platform

❌ **Don't use Copilot for**:
- Exact templates that shouldn't vary
- Security-critical configurations
- License files
- Files with strict formatting requirements

### Copilot Prompts

Good prompts are:
- **Specific**: "Generate a README for a Joomla authentication component"
- **Contextual**: Include repo name, type, platform
- **Detailed**: Specify required sections
- **Focused**: One clear objective

Bad prompts:
- Too vague: "Make a README"
- Too broad: "Document everything"
- Conflicting: Multiple contradictory requirements

### Workflow Dependencies

Mark as workflow dependency if:
- ✅ Script is called directly by workflow
- ✅ Script is required for CI/CD pipeline
- ✅ Missing file would break automated processes
- ✅ File must always match MokoStandards version

Don't mark as workflow dependency if:
- ❌ Script is optional
- ❌ Repository might have custom implementation
- ❌ File is repository-specific

## Troubleshooting

### Copilot Not Available

**Error**: "GitHub Copilot CLI not available"

**Solution**:
```bash
# Install Copilot extension
gh extension install github/gh-copilot

# Verify installation
gh copilot --version

# Authenticate
gh auth login
```

### Copilot Timeout

**Error**: "Copilot generation timed out"

**Solution**:
- Simplify prompt
- Break into smaller requests
- Run without Copilot flag

### Override Schema Not Generated

**Issue**: Override schema file not created

**Check**:
1. scripts/ directory exists in target repo
2. Write permissions available
3. Not running in dry-run mode

**Manual Creation**:
```bash
mkdir -p scripts
cp templates/repository-structure-override.xml scripts/
```

### Workflow Dependencies Not Updated

**Issue**: Workflow-dependent script is outdated

**Solution**:
```bash
# Force sync with standards options
python3 scripts/automation/bulk_update_repos.py \
  --repos myrepo \
  --set-standards \
  --yes
```

## Examples

### Example 1: Sync with Copilot to Single Repo

```bash
python3 scripts/automation/bulk_update_repos.py \
  --repos my-joomla-component \
  --use-copilot \
  --yes
```

Output:
```
Processing repository: mokoconsulting-tech/my-joomla-component
  Cloning repository...
  Detecting platform type...
    Detected platform: joomla
  ✓ Copilot integration enabled
  Creating branch: chore/sync-mokostandards-updates
    Customizing with Copilot: README.md
    ✓ Customized: README.md -> README.md
    Copied: .github/workflows/ci.yml -> .github/workflows/ci.yml
  Generating override schema definition...
    ✓ Generated override schema: scripts/repository-structure-override.xml
  Committing changes...
  Pushing branch...
  Creating pull request...
  ✓ Successfully updated mokoconsulting-tech/my-joomla-component
```

### Example 2: Dry Run with Copilot

```bash
python3 scripts/automation/bulk_update_repos.py \
  --dry-run \
  --use-copilot
```

### Example 3: Monthly Automated Sync

Workflow runs automatically on 1st of each month at 00:00 UTC:
- Syncs to all org repos (except MokoStandards itself)
- Uses standard sync (no Copilot by default)
- Creates PRs for all changes
- Respects override schemas

## Security Considerations

### Copilot Usage

- Copilot-generated content should be reviewed
- Don't use Copilot for security-critical files
- Custom prompts are visible in schema files
- Generated content follows MokoStandards conventions

### Workflow Dependencies

- Always validated before deployment
- Force overwrite ensures consistency
- Breaking changes logged in PRs
- Review required before merging

### Override Schemas

- Override schemas are repository-specific
- Not synced back to MokoStandards
- Can customize any aspect of sync
- Should be version controlled

## FAQ

**Q: Does Copilot require a subscription?**  
A: Yes, GitHub Copilot requires an active subscription. Sync works without Copilot.

**Q: Can I disable Copilot for specific files?**  
A: Yes, set `copilot-enabled: false` in override schema.

**Q: Are workflow dependencies always overwritten?**  
A: Yes, to ensure consistency with MokoStandards requirements.

**Q: Can I customize the override schema template?**  
A: Yes, modify `generate_override_schema()` in bulk_update_repos.py.

**Q: What happens if Copilot generation fails?**  
A: Sync falls back to standard file copy.

## Support

- **Issues**: https://github.com/mokoconsulting-tech/MokoStandards/issues
- **Discussions**: https://github.com/mokoconsulting-tech/MokoStandards/discussions
- **Documentation**: `docs/guide/`

---

**Version**: 1.0.0  
**Last Updated**: 2026-01-18  
**Maintained By**: Moko Consulting  
**License**: GPL-3.0-or-later
