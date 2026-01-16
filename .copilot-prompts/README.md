# Copilot Coordination Prompts

This directory contains prompts designed to coordinate work between the MokoStandards repository and other related repositories in the Moko Consulting ecosystem.

## Purpose

When implementing features in MokoStandards that require corresponding changes in other repositories (especially private repositories like `.github-private`), these prompts provide:

1. **Context**: What was implemented in MokoStandards
2. **Requirements**: What needs to be implemented in the related repository
3. **Integration Points**: How the systems connect and interact
4. **Implementation Guidance**: Step-by-step instructions for coordinated work
5. **Success Criteria**: How to verify the integration is complete

## Available Prompts

### Comprehensive Framework Summary

**File**: `comprehensive-framework-summary.md`

**Purpose**: Complete overview of the MokoStandards framework including:
- Schema System v2.0 with source/destination mapping
- Platform auto-detection for Joomla (all types) and Dolibarr
- Repository requirements validation
- Template organization and naming conventions
- Enterprise firewall configuration
- Bulk repository sync with schema deployment
- Issue template management approach
- Recent updates and breaking changes

**When to Use**: When onboarding new team members, implementing features across the framework, or needing a complete reference of capabilities.

### Repository Health System Integration (Planning)

**File**: `github-private-integration-repo-health.md`

**Purpose**: High-level coordination document for the XML-based repository health system:
- **MokoStandards** (public): Provides schemas, default configuration, and checking scripts
- **.github-private** (private): Implements organization-specific configurations and workflows

**When to Use**: When understanding the overall architecture and planning the repository health system deployment.

### Repository Health System Execution (Implementation)

**File**: `execute-github-private-repo-health.md`

**Purpose**: Exact, actionable instructions for implementing the repository health system in .github-private:
- Step-by-step file creation with exact content
- Workflow templates ready to deploy
- Validation scripts and custom check handlers
- Complete documentation updates

**When to Use**: When actually implementing the repository health system in .github-private. This prompt provides exact code and commands for a Copilot agent to execute.

## How to Use These Prompts

1. **Read the Context Section**: Understand what has been completed in the source repository
2. **Review Required Work**: Identify what needs to be implemented in the target repository
3. **Check Integration Points**: Understand how the systems connect
4. **Follow Implementation Checklist**: Work through each item systematically
5. **Verify Success Criteria**: Ensure all requirements are met

## Creating New Coordination Prompts

When adding new features that span multiple repositories:

1. Create a new prompt file in this directory
2. Use the existing prompts as templates
3. Include these sections:
   - Context
   - Completed Work (in source repo)
   - Required Work (in target repo)
   - Integration Points
   - Implementation Checklist
   - Testing Strategy
   - Success Criteria
4. Update this README with a reference to the new prompt

## Best Practices

- **Be Specific**: Include exact file paths, URLs, and code examples
- **Stay Current**: Update prompts when implementations change
- **Document Dependencies**: Clearly state what must be done first
- **Provide Examples**: Show concrete code snippets where helpful
- **Include Links**: Reference relevant documentation and resources
- **Think Security**: Note any security considerations for private repos

## Repository References

- **MokoStandards**: `https://github.com/mokoconsulting-tech/MokoStandards` (public)
- **.github-private**: `https://github.com/mokoconsulting-tech/.github-private` (private, internal only)

---

**Maintained by**: Moko Consulting Engineering Team  
**Last Updated**: 2026-01-16
