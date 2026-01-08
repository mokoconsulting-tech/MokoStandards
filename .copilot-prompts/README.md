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

### Repository Health System Integration

**File**: `github-private-integration-repo-health.md`

**Purpose**: Coordinates the XML-based repository health system implementation between:
- **MokoStandards** (public): Provides schemas, default configuration, and checking scripts
- **.github-private** (private): Implements organization-specific configurations and workflows

**When to Use**: When deploying the repository health system organization-wide or customizing it for internal needs.

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
**Last Updated**: 2026-01-08
