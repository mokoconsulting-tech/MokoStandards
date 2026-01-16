# Execute Repository Health System in .github-private

## Agent Instructions

You are tasked with implementing the XML-based repository health system in the `mokoconsulting-tech/.github-private` repository. Follow these instructions exactly.

## Prerequisites

Before starting, ensure you have:
- Access to the `mokoconsulting-tech/.github-private` repository
- The repository cloned locally
- Python 3.8+ installed
- Git configured with appropriate permissions

## Implementation Tasks

### Task 1: Update Organization-Level Workflow Template

**File to Create/Update**: `workflow-templates/repo-health-check.yml`

**Action**: Create a GitHub Actions workflow template that uses the XML-based health checking system.

**Exact Content**:
```yaml
name: Repository Health Check

on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  workflow_dispatch:
    inputs:
      config_url:
        description: 'Custom health config URL'
        required: false
        default: 'https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml'

jobs:
  health-check:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Download Health Checker Script
        run: |
          curl -sSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/validate/check_repo_health.py -o check_repo_health.py
          chmod +x check_repo_health.py
      
      - name: Run Health Check
        id: health-check
        run: |
          CONFIG_URL="${{ github.event.inputs.config_url || 'https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml' }}"
          python3 check_repo_health.py --config "$CONFIG_URL" --output json > health-report.json
          python3 check_repo_health.py --config "$CONFIG_URL" --output text > health-report.txt
        continue-on-error: true
      
      - name: Display Health Report
        run: |
          echo "## Repository Health Report" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          cat health-report.txt >> $GITHUB_STEP_SUMMARY
      
      - name: Upload Health Report
        uses: actions/upload-artifact@v4
        with:
          name: health-report
          path: |
            health-report.json
            health-report.txt
          retention-days: 90
      
      - name: Check Health Status
        run: |
          SCORE=$(python3 -c "import json; print(json.load(open('health-report.json'))['summary']['score'])")
          LEVEL=$(python3 -c "import json; print(json.load(open('health-report.json'))['summary']['level'])")
          echo "Health Score: $SCORE"
          echo "Health Level: $LEVEL"
          
          if [ "$LEVEL" = "poor" ]; then
            echo "::warning::Repository health is poor. Please address the failing checks."
          fi
```

**Properties File**: `workflow-templates/repo-health-check.properties.json`

**Exact Content**:
```json
{
  "name": "Repository Health Check",
  "description": "Automated repository health checking using MokoStandards XML-based system",
  "iconName": "health",
  "categories": [
    "automation",
    "quality"
  ],
  "filePatterns": [
    "^.github/workflows/repo-health-check.yml$"
  ]
}
```

### Task 2: Create Organization-Specific Health Configuration

**File to Create**: `configs/repo-health-organization.xml`

**Action**: Create an organization-specific health configuration that extends the default MokoStandards configuration.

**Exact Content**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<repository-health xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:noNamespaceSchemaLocation="https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health.xsd">
  
  <metadata>
    <name>Moko Consulting Organization Health Configuration</name>
    <version>1.0.0</version>
    <description>Organization-specific repository health configuration extending MokoStandards defaults</description>
    <author>Moko Consulting Engineering Team</author>
    <date>YYYY-MM-DD</date> <!-- Update to current date when implementing -->
    <extends>https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml</extends>
  </metadata>
  
  <scoring>
    <total-points>120</total-points>
    <levels>
      <level name="excellent" min="100" max="120" color="green"/>
      <level name="good" min="80" max="99" color="blue"/>
      <level name="fair" min="60" max="79" color="yellow"/>
      <level name="poor" min="0" max="59" color="red"/>
    </levels>
    <categories>
      <category id="org-compliance" name="Organization Compliance" weight="20"/>
    </categories>
  </scoring>
  
  <checks>
    <!-- Organization-specific compliance checks -->
    <check id="check_org_topics">
      <name>Organization Topic Tags</name>
      <description>Verify repository has required organization topic tags</description>
      <category>org-compliance</category>
      <points>5</points>
      <type>custom-script</type>
      <parameters>
        <parameter name="script" value="check_repository_topics.py"/>
        <parameter name="required_topics" value="moko-consulting"/>
      </parameters>
      <remediation>Add organization topic tags via repository settings</remediation>
    </check>
    
    <check id="check_internal_docs">
      <name>Internal Documentation Links</name>
      <description>Verify presence of internal documentation references</description>
      <category>org-compliance</category>
      <points>5</points>
      <type>file-exists</type>
      <parameters>
        <parameter name="path" value="docs/internal/"/>
      </parameters>
      <remediation>Add docs/internal/ directory with organization documentation links</remediation>
    </check>
    
    <check id="check_security_policy">
      <name>Organization Security Policy</name>
      <description>Ensure SECURITY.md references organization security contacts</description>
      <category>org-compliance</category>
      <points>5</points>
      <type>file-content</type>
      <parameters>
        <parameter name="path" value="SECURITY.md"/>
        <parameter name="pattern" value="security@mokoconsulting.tech"/>
      </parameters>
      <remediation>Update SECURITY.md with organization security contact</remediation>
    </check>
    
    <check id="check_codeowners">
      <name>CODEOWNERS Configuration</name>
      <description>Verify CODEOWNERS file exists and has organization teams</description>
      <category>org-compliance</category>
      <points>5</points>
      <type>file-content</type>
      <parameters>
        <parameter name="path" value=".github/CODEOWNERS"/>
        <parameter name="pattern" value="@mokoconsulting-tech/"/>
      </parameters>
      <remediation>Add .github/CODEOWNERS with team assignments</remediation>
    </check>
  </checks>
  
</repository-health>
```

### Task 3: Create Configuration Validator Script

**File to Create**: `scripts/validate/validate_org_health_config.py`

**Action**: Create a validation script specifically for organization configurations.

**Exact Content**:
```python
#!/usr/bin/env python3
"""
Validate organization-specific health configurations.

This script validates that organization health configs properly extend
the MokoStandards default configuration and follow all requirements.
"""

import sys
import argparse
from pathlib import Path
import urllib.request
from xml.etree import ElementTree as ET

def validate_org_config(config_path):
    """Validate organization health configuration."""
    print(f"Validating organization config: {config_path}")
    
    try:
        tree = ET.parse(config_path)
        root = tree.getroot()
        
        # Check for required metadata
        metadata = root.find('metadata')
        if metadata is None:
            print("ERROR: Missing <metadata> section")
            return False
        
        # Check for extends attribute
        extends = metadata.find('extends')
        if extends is None:
            print("WARNING: No <extends> element found. This config does not extend default.")
        else:
            extends_url = extends.text
            print(f"Config extends: {extends_url}")
            
            # Verify the URL is accessible
            try:
                with urllib.request.urlopen(extends_url) as response:
                    if response.status != 200:
                        print(f"ERROR: Cannot access extends URL: {extends_url}")
                        return False
                    print("✓ Extended configuration is accessible")
            except Exception as e:
                print(f"ERROR: Failed to access extends URL: {e}")
                return False
        
        # Check scoring section
        scoring = root.find('scoring')
        if scoring is None:
            print("ERROR: Missing <scoring> section")
            return False
        
        # Check checks section
        checks = root.find('checks')
        if checks is None:
            print("ERROR: Missing <checks> section")
            return False
        
        check_list = checks.findall('check')
        print(f"Found {len(check_list)} organization-specific checks")
        
        # Validate each check
        for check in check_list:
            check_id = check.get('id')
            name = check.find('name')
            category = check.find('category')
            
            if not check_id:
                print(f"ERROR: Check missing 'id' attribute")
                return False
            
            if name is None:
                print(f"ERROR: Check '{check_id}' missing <name>")
                return False
            
            if category is None:
                print(f"ERROR: Check '{check_id}' missing <category>")
                return False
            
            print(f"✓ Check '{check_id}': {name.text}")
        
        print("\n✓ Organization configuration is valid")
        return True
        
    except ET.ParseError as e:
        print(f"ERROR: XML parsing error: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Validate organization health configuration'
    )
    parser.add_argument(
        'config',
        nargs='?',
        default='configs/repo-health-organization.xml',
        help='Path to organization health config XML file'
    )
    
    args = parser.parse_args()
    
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"ERROR: Config file not found: {config_path}")
        return 1
    
    if validate_org_config(config_path):
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

**Make script executable**:
```bash
chmod +x scripts/validate/validate_org_health_config.py
```

### Task 4: Create Custom Check Handler Script

**File to Create**: `scripts/checks/check_repository_topics.py`

**Action**: Create a custom check handler for repository topics validation.

**Exact Content**:
```python
#!/usr/bin/env python3
"""
Check repository topics for organization requirements.

This script verifies that a repository has required organization topic tags.
"""

import sys
import os
import json
import argparse

def check_topics(required_topics):
    """Check if repository has required topics."""
    
    # Try to get topics from GitHub API if available
    repo = os.environ.get('GITHUB_REPOSITORY', '')
    token = os.environ.get('GITHUB_TOKEN', '')
    
    if not repo or not token:
        print("WARNING: GITHUB_REPOSITORY or GITHUB_TOKEN not set, skipping topic check")
        return True
    
    try:
        import urllib.request
        
        api_url = f"https://api.github.com/repos/{repo}"
        request = urllib.request.Request(
            api_url,
            headers={
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
        )
        
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read())
            topics = data.get('topics', [])
            
            missing = []
            for required in required_topics:
                if required not in topics:
                    missing.append(required)
            
            if missing:
                print(f"FAIL: Missing required topics: {', '.join(missing)}")
                print(f"Current topics: {', '.join(topics) if topics else '(none)'}")
                return False
            else:
                print(f"PASS: All required topics present: {', '.join(required_topics)}")
                return True
                
    except Exception as e:
        print(f"ERROR: Failed to check topics: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Check repository topics')
    parser.add_argument(
        '--required',
        nargs='+',
        default=['moko-consulting'],
        help='Required topic tags'
    )
    
    args = parser.parse_args()
    
    if check_topics(args.required):
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

**Make script executable**:
```bash
chmod +x scripts/checks/check_repository_topics.py
```

### Task 5: Create CI/CD Validation Workflow

**File to Create**: `.github/workflows/validate-configs.yml`

**Action**: Create a workflow to validate health configurations on pull requests.

**Exact Content**:
```yaml
name: Validate Health Configurations

on:
  pull_request:
    paths:
      - 'configs/repo-health-*.xml'
      - 'scripts/validate/**'
      - 'scripts/checks/**'
  push:
    branches:
      - main
    paths:
      - 'configs/repo-health-*.xml'

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout .github-private
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Download MokoStandards Validator
        run: |
          curl -sSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/validate/validate_repo_health.py -o validate_repo_health.py
          chmod +x validate_repo_health.py
      
      - name: Validate Organization Config Against XSD
        run: |
          python3 validate_repo_health.py configs/repo-health-organization.xml
      
      - name: Validate Organization Config (Custom Validator)
        run: |
          python3 scripts/validate/validate_org_health_config.py configs/repo-health-organization.xml
      
      - name: Test Health Check Scripts
        run: |
          if [ -f scripts/checks/check_repository_topics.py ]; then
            python3 -m py_compile scripts/checks/check_repository_topics.py
            echo "✓ check_repository_topics.py syntax is valid"
          fi
```

### Task 6: Update Documentation

**File to Create/Update**: `docs/repository-health-system.md`

**Action**: Create comprehensive documentation for the organization's repository health system.

**Exact Content**:
```markdown
# Repository Health System - Organization Implementation

## Overview

This document describes the Moko Consulting organization's implementation of the XML-based repository health checking system from MokoStandards.

## System Architecture

### Public Components (MokoStandards)

- **XSD Schema**: `schemas/repo-health.xsd` - Validation schema
- **Default Config**: `schemas/repo-health-default.xml` - Base configuration (100 points)
- **Health Checker**: `scripts/validate/check_repo_health.py` - Execution script
- **Config Validator**: `scripts/validate/validate_repo_health.py` - Validation script

### Private Components (This Repository)

- **Organization Config**: `configs/repo-health-organization.xml` - Extended configuration (120 points)
- **Workflow Template**: `workflow-templates/repo-health-check.yml` - Reusable workflow
- **Custom Checks**: `scripts/checks/` - Organization-specific check handlers
- **Config Validator**: `scripts/validate/validate_org_health_config.py` - Org config validator

## Configuration

### Default Configuration

All repositories inherit the default configuration from MokoStandards:
```
https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml
```

This provides 8 categories covering 100 points:
- CI/CD (15 points)
- Documentation (20 points)
- Security (20 points)
- Code Quality (15 points)
- Deployment (10 points)
- Testing (10 points)
- Version Control (5 points)
- Dependencies (5 points)

### Organization Configuration

The organization configuration extends the default with 20 additional points:
```
configs/repo-health-organization.xml
```

Additional category:
- **Organization Compliance** (20 points)
  - Organization topic tags (5 points)
  - Internal documentation links (5 points)
  - Organization security policy (5 points)
  - CODEOWNERS configuration (5 points)

Total possible score: **120 points**

## Health Levels

| Level | Score Range | Color | Description |
|-------|-------------|-------|-------------|
| Excellent | 100-120 | Green | All checks passing, exemplary repository |
| Good | 80-99 | Blue | Most checks passing, minor improvements needed |
| Fair | 60-79 | Yellow | Significant issues requiring attention |
| Poor | 0-59 | Red | Critical issues, immediate action required |

## Usage

### Running Health Checks Locally

```bash
# Download health checker
curl -sSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/validate/check_repo_health.py -o check_repo_health.py

# Run with default config
python3 check_repo_health.py

# Run with organization config
python3 check_repo_health.py --config https://raw.githubusercontent.com/mokoconsulting-tech/.github-private/main/configs/repo-health-organization.xml

# Output as JSON
python3 check_repo_health.py --output json > health-report.json
```

### Deploying to Repositories

1. Copy workflow template to target repository:
   ```bash
   cp workflow-templates/repo-health-check.yml <target-repo>/.github/workflows/
   ```

2. Workflow runs automatically:
   - Weekly on Monday at midnight
   - Manually via workflow dispatch

3. View results:
   - Check job summary in Actions tab
   - Download artifacts (JSON and text reports)

## Customizing Checks

### Adding Organization-Specific Checks

1. Edit `configs/repo-health-organization.xml`
2. Add new `<check>` elements under `<checks>`
3. Validate changes:
   ```bash
   python3 scripts/validate/validate_org_health_config.py
   ```

### Creating Custom Check Handlers

For `custom-script` check types, create handler in `scripts/checks/`:

```python
#!/usr/bin/env python3
"""Custom check handler."""

def check_custom_requirement():
    # Implement check logic
    return True  # or False

if __name__ == '__main__':
    import sys
    sys.exit(0 if check_custom_requirement() else 1)
```

## Maintenance

### Updating Configurations

1. Edit configuration file
2. Validate against schema:
   ```bash
   curl -sSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/validate/validate_repo_health.py -o validate.py
   python3 validate.py configs/repo-health-organization.xml
   ```
3. Test with sample repository
4. Commit and push changes
5. Redeploy workflows to affected repositories

### Monitoring Health Scores

Health check results are stored as workflow artifacts for 90 days. To track trends:

1. Collect health reports from all repositories
2. Parse JSON output
3. Generate dashboard/metrics
4. Alert on degrading scores

## Troubleshooting

### Common Issues

**Error: Cannot access remote configuration**
- Verify URL is correct
- Check network/firewall access
- Ensure configuration is in main branch

**Error: Check failed unexpectedly**
- Review check parameters in XML
- Verify custom script exists and is executable
- Check script output for error messages

**Error: XML validation failed**
- Validate against XSD schema
- Check for typos in element names
- Ensure all required elements are present

## Support

For questions or issues:
- Internal: Contact `@mokoconsulting-tech/maintainers`
- Email: `dev@mokoconsulting.tech`

## References

- [MokoStandards Repository](https://github.com/mokoconsulting-tech/MokoStandards)
- [Schema Guide](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/schemas/repohealth/schema-guide.md)
- [Default Configuration](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/schemas/repo-health-default.xml)
```

### Task 7: Update README

**File to Update**: `README.md`

**Action**: Add a section about the repository health system to the repository README.

**Add this section** (location: after introduction, before main content):

```markdown
## Repository Health System

This repository implements the MokoStandards XML-based repository health checking system organization-wide.

**Key Files**:
- `configs/repo-health-organization.xml` - Organization-specific health configuration
- `workflow-templates/repo-health-check.yml` - Deployable workflow template
- `docs/repository-health-system.md` - Complete documentation

**Quick Start**:
```bash
# Validate organization configuration
python3 scripts/validate/validate_org_health_config.py

# Deploy health check to a repository
cp workflow-templates/repo-health-check.yml <repo>/.github/workflows/
```

**Documentation**: See [docs/repository-health-system.md](docs/repository-health-system.md)
```

## Verification Steps

After completing all tasks, verify the implementation:

1. **Validate Organization Config**:
   ```bash
   python3 scripts/validate/validate_org_health_config.py configs/repo-health-organization.xml
   ```
   
2. **Validate Against XSD Schema**:
   ```bash
   curl -sSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/validate/validate_repo_health.py -o validate.py
   python3 validate.py configs/repo-health-organization.xml
   ```

3. **Test Workflow Template**:
   - Create a test repository
   - Copy workflow template
   - Run workflow manually
   - Verify health report is generated

4. **Check CI/CD**:
   - Push changes to a branch
   - Create pull request
   - Verify validation workflow runs
   - Confirm all checks pass

## Directory Structure

After implementation, your `.github-private` repository should have:

```
.github-private/
├── .github/
│   └── workflows/
│       └── validate-configs.yml          # New
├── configs/
│   └── repo-health-organization.xml      # New
├── docs/
│   └── repository-health-system.md       # New
├── scripts/
│   ├── checks/
│   │   └── check_repository_topics.py    # New
│   └── validate/
│       └── validate_org_health_config.py # New
├── workflow-templates/
│   ├── repo-health-check.yml             # New
│   └── repo-health-check.properties.json # New
└── README.md                              # Updated
```

## Success Criteria

- [ ] All files created in correct locations
- [ ] Organization config validates against XSD schema
- [ ] Custom validator script runs successfully
- [ ] Workflow template is valid YAML
- [ ] CI/CD validation workflow passes
- [ ] Documentation is complete and accurate
- [ ] All scripts are executable
- [ ] README updated with health system reference

## Notes

- All file paths are relative to the `.github-private` repository root
- Scripts must be made executable with `chmod +x`
- XML configuration extends the MokoStandards default configuration
- Workflow template uses standard GitHub Actions syntax
- Configuration is validated on every PR to prevent breaking changes
- Update the date field in XML metadata to the current date when implementing
- Email addresses are intentionally different: `security@mokoconsulting.tech` for security issues, `dev@mokoconsulting.tech` for general development support

## Support

If you encounter issues during implementation:

1. Verify you're working in the correct repository (`.github-private`)
2. Check that all file paths are correct
3. Ensure Python 3.8+ is installed
4. Validate XML syntax if config validation fails
5. Review GitHub Actions logs for workflow issues

For additional help, refer to:
- [MokoStandards Repository](https://github.com/mokoconsulting-tech/MokoStandards)
- [Repository Health Schema Guide](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/schemas/repohealth/schema-guide.md)
