# Dev Workstation Terraform Configuration

This directory contains Terraform definitions for Windows development workstation provisioning configuration.

## Purpose

These Terraform files define the configuration-as-code for standardized Windows developer workstations, based on the PowerShell provisioner script at `scripts/automation/dev-workstation-provisioner.ps1`.

## Files

- **`dev-workstation.tf`** - Main configuration defining workstation setup parameters

## Configuration Structure

The Terraform configuration defines:

### Metadata
- Version information
- Platform (Windows)
- Documentation references

### Workspace Configuration
- Default workspace path: `%USERPROFILE%\Documents\Workspace`
- Artifacts to be created (update scripts, logs)

### Package Management (Winget)
- Monthly update schedule (1st of month at 09:00)
- Excluded packages:
  - Python 3.10 (pinned for compatibility)
  - PHP (managed via WSL)
- Log location: `C:\Logs\Winget`

### WSL (Windows Subsystem for Linux)
- Ubuntu as default distribution
- Required Windows features
- User confirmation gates for install/reset

### Ubuntu WSL PHP Configuration
- PHP 8.3 with common extensions
- Development packages (CLI, MySQL, cURL, etc.)
- Enabled modules for web development

### Security & Governance
- Requires administrator privileges
- User confirmation required for destructive actions
- Confirmation gates for WSL operations

### Runtime Versions
- Python 3.10 (pinned)
- PHP 8.3 (WSL-managed)

## Usage

### View Configuration

```bash
cd terraform/workstation
terraform init
terraform output dev_workstation_config
```

### Access PowerShell Template

```bash
terraform output powershell_script_template
```

### Access Validation Rules

```bash
terraform output workstation_validation
```

## Integration with PowerShell Script

The PowerShell provisioner (`scripts/automation/dev-workstation-provisioner.ps1`) can read this Terraform configuration to:

1. Get default configuration values
2. Validate against defined parameters
3. Generate update scripts with correct exclusions
4. Apply security and governance policies

## Configuration Changes

To modify workstation configuration:

1. Edit `dev-workstation.tf` locals block
2. Run `terraform fmt` to format
3. Run `terraform validate` to check syntax
4. Commit changes to version control
5. PowerShell script will use updated configuration

## Benefits of Terraform Definition

1. **Version Control**: Track configuration changes over time
2. **Documentation**: Self-documenting configuration
3. **Validation**: Terraform validates configuration syntax
4. **Reusability**: Easy to clone for different workstation types
5. **Consistency**: Single source of truth for workstation config
6. **Auditability**: Clear history of configuration changes

## Related Files

- Source PowerShell script: `scripts/automation/dev-workstation-provisioner.ps1`
- Documentation: `docs/scripts/automation/dev-workstation-provisioner.md`
- Parent Terraform: `terraform/main.tf`

## Example Output

The configuration exports three outputs:

1. **dev_workstation_config** - Complete configuration structure
2. **powershell_script_template** - Template values for PowerShell script generation
3. **workstation_validation** - Validation rules and security gates

## Future Enhancements

Potential additions to this configuration:

- Additional WSL distributions (Debian, Alpine)
- Node.js/npm configuration
- Docker Desktop settings
- IDE/editor configurations
- Git configuration templates
- SSH key management
- Network proxy settings
- Firewall rules

## Notes

- This is a configuration definition, not infrastructure provisioning
- No actual resources are created by Terraform
- Configuration is consumed by the PowerShell provisioner script
- Changes require PowerShell script execution to take effect
