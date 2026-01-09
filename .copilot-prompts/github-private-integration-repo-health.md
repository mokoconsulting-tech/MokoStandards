# Coordinating Copilot Prompt for .github-private Repository

## Context

The MokoStandards repository has implemented an XML-based repository health schema and checking system. The .github-private repository needs to be updated to integrate with this new system and provide organization-level implementations.

## Completed Work in MokoStandards

The following has been completed in the **mokoconsulting-tech/MokoStandards** repository:

### 1. XML Schema Definition (XSD)
- **File**: `schemas/repo-health.xsd`
- **Purpose**: Defines the structure and validation rules for repository health configurations
- **Features**:
  - Metadata section for configuration details
  - Scoring system with categories and thresholds
  - Flexible check definitions with multiple check types
  - Parameter system for check configuration
  - Support for local and remote validation

### 2. Default Repository Health Configuration
- **File**: `schemas/repo-health-default.xml`
- **Purpose**: Provides the default health check configuration for all Moko Consulting repositories
- **Coverage**: 
  - 8 categories covering 100 total points
  - 4 health levels (excellent, good, fair, poor)
  - Comprehensive checks across CI/CD, documentation, security, and deployment
- **URL**: `https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml`

### 3. Validation Script
- **File**: `scripts/validate/validate_repo_health.py`
- **Purpose**: Validates repository health XML configurations against the schema
- **Features**:
  - Local file and remote URL support
  - Comprehensive validation of structure, metadata, scoring, and checks
  - Error and warning reporting
  - Can be used in CI/CD pipelines

### 4. Health Checking Script
- **File**: `scripts/validate/check_repo_health.py`
- **Purpose**: Performs actual health checks on repositories based on XML configuration
- **Features**:
  - Loads configuration from local files or remote URLs
  - Executes all defined checks
  - Calculates scores and health levels
  - Outputs results in text or JSON format
  - Defaults to remote configuration from MokoStandards GitHub

## Required Work in .github-private Repository

You need to implement the following in the **mokoconsulting-tech/.github-private** repository:

### 1. Update Organization-Level Workflow Templates

**Files to Update**:
- `workflow-templates/repo-health-org.yml` (create if doesn't exist)
- `workflow-templates/standards-compliance-org.yml` (update if exists)

**Requirements**:
- Update workflows to use the new XML-based health checking system
- Reference the remote configuration URL: `https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml`
- Use the new Python scripts from MokoStandards
- Ensure workflows can be deployed across all organization repositories
- Add workflow dispatch inputs for custom configuration URLs

**Example workflow step**:
```yaml
- name: Check Repository Health
  run: |
    # Download health checker script
    curl -sSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/scripts/validate/check_repo_health.py -o check_repo_health.py
    
    # Run health check with remote config
    python3 check_repo_health.py --config https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml --output json > health-report.json
    
    # Display results
    cat health-report.json
```

### 2. Create Organization-Specific Health Configuration

**File to Create**: `configs/repo-health-organization.xml`

**Requirements**:
- Extend the default configuration with organization-specific checks
- Add checks for proprietary internal standards
- Include organization-specific secret validations
- Add custom checks for internal tooling requirements
- Reference internal documentation and remediation procedures
- Ensure it validates against the XSD schema

**Considerations**:
- Keep sensitive information in this private repository
- Reference organization-level secrets and variables
- Add checks for internal compliance requirements
- Include custom check types for organization-specific tooling

### 3. Update Repository Health Dashboard

**Files to Update**:
- `scripts/dashboard/generate_health_dashboard.py` (update if exists)
- `scripts/dashboard/collect_health_metrics.py` (create if doesn't exist)

**Requirements**:
- Integrate with the new XML-based health system
- Collect health scores from all organization repositories
- Parse JSON output from health checker script
- Generate comprehensive health dashboard
- Store historical health data for trend analysis
- Create visualization of health scores across repositories

### 4. Create Deployment Automation Scripts

**Files to Create**:
- `scripts/deploy/deploy_health_workflows.py`
- `scripts/deploy/update_health_config.py`

**Requirements**:
- Script to deploy health check workflows to all organization repositories
- Script to update health configurations across repositories
- Ability to override with custom configurations per repository
- Validation before deployment
- Rollback capability
- Support for dry-run mode

### 5. Update Organization Documentation

**Files to Update**:
- `docs/repository-health-system.md` (create or update)
- `README.md` (update with new health system references)

**Requirements**:
- Document the new XML-based health system
- Explain how to customize configurations
- Provide examples of extending the default configuration
- Document organization-specific checks
- Include troubleshooting guide
- Add migration guide from old system to new system

### 6. Create Organization Health Configuration Validator

**File to Create**: `scripts/validate/validate_org_health_config.py`

**Requirements**:
- Validate organization-specific configurations
- Check that all custom checks are properly implemented
- Verify secret references are valid
- Ensure category IDs match between scoring and checks
- Validate point calculations
- Can be run in CI/CD to validate config changes

### 7. Implement Custom Check Handlers

**File to Create**: `scripts/checks/custom_check_handlers.py`

**Requirements**:
- Implement handlers for `custom-script` check types
- Support organization-specific validation logic
- Handlers for:
  - `check_platform_workflow` - Verify platform-specific workflows
  - `check_ftp_auth` - Validate FTP authentication configuration
  - `check_sftp_connectivity` - Test SFTP connectivity
  - `check_repository_topics` - Verify repository topic configuration
- Extensible system for adding new custom checks
- Error handling and reporting

### 8. Update CI/CD Pipeline

**Files to Update**:
- `.github/workflows/validate-configs.yml` (create or update)
- `.github/workflows/test-health-system.yml` (create)

**Requirements**:
- Validate all health configurations on PR
- Test health checking scripts against sample repositories
- Ensure organization-specific configurations pass validation
- Run integration tests with MokoStandards public configurations
- Verify remote URL access works correctly

## Integration Points

### Remote Configuration Access
- Default remote config URL: `https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml`
- Organization can override with custom configs stored in .github-private
- Workflows should support both public and private configuration sources

### Script Distribution
- Public scripts from MokoStandards can be downloaded via raw GitHub URLs
- Private scripts should be deployed via internal mechanisms
- Consider using GitHub Actions artifacts for distribution

### Secret Management
- Organization-level secrets (FTP_HOST, FTP_USERNAME, etc.) remain in GitHub organization settings
- Repository-specific secrets/variables handled at repository level
- Health checks verify accessibility without exposing values

### Workflow Deployment
- Use GitHub CLI or API to deploy workflows across repositories
- Support for both organization-wide deployment and per-repository customization
- Version tracking for workflow deployments

## Implementation Checklist

Use this checklist when implementing in .github-private:

- [ ] Update organization-level repo health workflow templates
- [ ] Create organization-specific health configuration XML
- [ ] Validate organization config against XSD schema
- [ ] Update health dashboard generation scripts
- [ ] Create deployment automation scripts
- [ ] Implement custom check handlers for organization-specific checks
- [ ] Update organization documentation
- [ ] Create configuration validator for organization configs
- [ ] Update CI/CD pipelines to validate configurations
- [ ] Test integration with MokoStandards remote configuration
- [ ] Deploy updated workflows to test repositories
- [ ] Verify health checks run successfully
- [ ] Generate health dashboard with new system
- [ ] Document migration path for existing repositories
- [ ] Create runbook for health system operations

## Testing Strategy

1. **Local Testing**:
   - Validate organization config XML against schema
   - Run health checker on sample repositories
   - Test custom check handlers

2. **Integration Testing**:
   - Test with actual organization repositories
   - Verify remote configuration loading
   - Test workflow deployment automation

3. **Production Rollout**:
   - Deploy to pilot repositories first
   - Monitor health check results
   - Gradually roll out to all repositories
   - Update dashboard and monitoring

## Key Considerations

- **Backward Compatibility**: Ensure existing health checks continue to work during transition
- **Performance**: Health checks should complete within reasonable time (< 5 minutes)
- **Extensibility**: System should be easy to extend with new check types
- **Security**: Don't expose sensitive information in health check outputs
- **Documentation**: Keep internal documentation in sync with public MokoStandards docs

## Questions to Address

1. What organization-specific checks need to be added?
2. Are there internal compliance requirements to validate?
3. Should we maintain backward compatibility with the old system?
4. What is the timeline for rolling out to all repositories?
5. Who needs access to the health dashboard?
6. Are there any proprietary tools that need health checks?

## Success Criteria

- [ ] All organization repositories use XML-based health configuration
- [ ] Health dashboard displays accurate scores for all repositories
- [ ] Custom organization checks are implemented and working
- [ ] Workflows successfully reference remote MokoStandards configuration
- [ ] Health scores improve across organization over time
- [ ] Documentation is complete and accessible to all team members

## Next Steps

1. Review this prompt and confirm requirements
2. Begin implementation with workflow template updates
3. Create and validate organization-specific configuration
4. Implement custom check handlers
5. Test with pilot repositories
6. Roll out organization-wide
7. Monitor and iterate based on feedback

---

**Note**: This prompt coordinates work between the public MokoStandards repository and the private .github-private repository. The public repository provides the foundation and default configurations, while the private repository adds organization-specific implementations and sensitive configurations.
