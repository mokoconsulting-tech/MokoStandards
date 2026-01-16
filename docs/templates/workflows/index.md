# Workflow Templates Documentation

## Overview

This directory contains comprehensive documentation for GitHub Actions workflow templates provided by MokoStandards. These templates provide standardized CI/CD configurations for different project types and are designed to ensure consistency, quality, and compliance across all repositories in the organization.

## Template Location

All workflow templates are located in `templates/workflows/` with the following structure:

```
templates/workflows/
├── generic/              # Platform-agnostic workflow templates
├── joomla/               # Joomla-specific workflow templates
├── dolibarr/             # Dolibarr-specific workflow templates
└── *.yml.template        # Root-level templates for backward compatibility
```

## Template Naming Convention

**All workflow templates use the `.yml.template` extension** to clearly distinguish them from active workflow files (`.yml`):

- **Template files**: `*.yml.template` (stored in templates/workflows/)
- **Active workflows**: `*.yml` (copied to .github/workflows/ in target repositories)

### Why .yml.template?

1. **Clear Distinction**: Prevents confusion between templates and active workflows
2. **Prevents Accidental Execution**: GitHub Actions ignores .yml.template files
3. **Explicit Intent**: Users must consciously rename when copying
4. **Industry Standard**: Follows common practice (e.g., .env.template, config.template)

## Template Categories

### [Generic Templates](./generic.md)
Platform-agnostic workflow templates for multi-language software development:
- Continuous Integration (CI)
- Testing
- Code Quality & Security
- Deployment
- Repository Health

### [Joomla Templates](./joomla.md)
Workflow templates specifically designed for Joomla extensions (components, modules, plugins, libraries, templates):
- Joomla CI with manifest validation
- PHPUnit testing with Joomla framework
- Extension packaging and release
- Version branch management
- Repository health for Joomla projects

### [Dolibarr Templates](./dolibarr.md)
Workflow templates specifically designed for Dolibarr ERP/CRM modules:
- Dolibarr CI with module structure validation
- PHPUnit testing with Dolibarr integration
- Module packaging and release
- SQL migration validation

## Quick Start

### 1. Choose Your Template

Select the appropriate template based on your project type:

```bash
# For generic projects
ls templates/workflows/generic/

# For Joomla extensions
ls templates/workflows/joomla/

# For Dolibarr modules
ls templates/workflows/dolibarr/
```

### 2. Copy Template to Your Repository

```bash
# Example: Copy generic CI template
cp templates/workflows/generic/ci.yml.template .github/workflows/ci.yml

# Example: Copy Joomla CI template
cp templates/workflows/joomla/ci-joomla.yml.template .github/workflows/ci.yml

# Example: Copy Dolibarr CI template
cp templates/workflows/dolibarr/ci-dolibarr.yml.template .github/workflows/ci.yml
```

**Important**: Note the rename from `.yml.template` to `.yml` when copying to your repository.

### 3. Customize for Your Project

Edit the copied workflow file to customize:
- Repository-specific paths
- Project dependencies
- Build commands
- Deployment targets
- Environment variables

### 4. Commit and Test

```bash
git add .github/workflows/ci.yml
git commit -m "Add CI workflow from MokoStandards template"
git push
```

## Common Workflow Patterns

### Continuous Integration (CI)

Every repository should have a CI workflow that runs on every push and pull request:

**Generic**: `templates/workflows/generic/ci.yml.template`
**Joomla**: `templates/workflows/joomla/ci-joomla.yml.template`
**Dolibarr**: `templates/workflows/dolibarr/ci-dolibarr.yml.template`

Key features:
- Automated testing
- Code quality checks
- Security scanning
- Build verification

### Repository Health

Monitor repository health and compliance with organizational standards:

**Generic**: `templates/workflows/generic/repo_health.yml.template`
**Joomla**: `templates/workflows/joomla/repo_health.yml.template`

Key features:
- Required file validation
- Documentation checks
- License compliance
- Standards verification

### Security Analysis

CodeQL security analysis for vulnerability detection:

**All Projects**: `templates/workflows/generic/codeql-analysis.yml.template`

Key features:
- Automated vulnerability scanning
- Language-specific analysis
- Pull request comments
- Security advisories

## Template Maintenance

### Updating Templates

Templates are maintained in the MokoStandards repository. To update your workflow from the latest template:

```bash
# 1. Fetch latest MokoStandards
cd /path/to/MokoStandards
git pull

# 2. Compare with your current workflow
diff templates/workflows/generic/ci.yml.template /path/to/your-repo/.github/workflows/ci.yml

# 3. Merge relevant updates manually
# (Preserve your customizations while adopting template improvements)
```

### Version Control

Template versions are tracked through:
- Git commit history in MokoStandards repository
- VERSION comments in template files
- CHANGELOG.md entries

### Best Practices

1. **Minimal Customization**: Keep customizations minimal to ease future updates
2. **Comment Changes**: Document why you deviated from the template
3. **Periodic Review**: Review templates quarterly for updates
4. **Test Locally**: Test workflow changes in feature branches
5. **Follow Standards**: Adhere to organizational coding and security standards

## Troubleshooting

### Workflow Not Running

**Problem**: Copied workflow doesn't execute

**Solutions**:
1. Verify file has `.yml` extension (not `.yml.template`)
2. Check file is in `.github/workflows/` directory
3. Ensure workflow has valid YAML syntax
4. Verify trigger conditions match your events

### Workflow Fails

**Problem**: Workflow execution fails

**Solutions**:
1. Check workflow logs in GitHub Actions tab
2. Verify all required secrets are configured
3. Check paths match your repository structure
4. Ensure dependencies are correctly specified
5. Review template documentation for requirements

### Template Differences

**Problem**: Template has changed since you copied it

**Solutions**:
1. Review template CHANGELOG for breaking changes
2. Use `diff` to compare your version with latest template
3. Merge relevant updates preserving your customizations
4. Test in feature branch before merging to main

## Advanced Topics

### Reusable Workflows

Some templates reference reusable workflows from MokoStandards. These provide:
- Centralized maintenance
- Consistent behavior across repositories
- Reduced duplication

See [Reusable Workflows Documentation](../../workflows/REUSABLE_WORKFLOWS.md) for details.

### Custom Templates

To create custom templates for your specific needs:

1. Start with existing template as base
2. Add your customizations
3. Save as `.yml.template` in appropriate category
4. Document usage and requirements
5. Submit PR to MokoStandards (optional)

### Integration with Platform Detection

The platform auto-detection system (`scripts/validate/auto_detect_platform.py`) can recommend appropriate templates based on detected project type:

```bash
# Run platform detection
python3 scripts/validate/auto_detect_platform.py --verbose

# Review recommended templates in detection report
cat validation-reports/detection_report_*.md
```

## Additional Resources

- [Template Source Files](../../../templates/workflows/)
- [Workflow Template README](../../../templates/workflows/README.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Reusable Workflows](../../workflows/REUSABLE_WORKFLOWS.md)
- [Platform Auto-Detection](../../guide/validation/auto-detection.md)

## Support

For questions or issues with workflow templates:

1. Check this documentation and template README files
2. Review GitHub Actions logs for specific errors
3. Consult with team leads or DevOps
4. Open an issue in MokoStandards repository

---

**Last Updated**: 2026-01-16  
**Maintained By**: MokoStandards Team  
**Version**: 1.0.0
