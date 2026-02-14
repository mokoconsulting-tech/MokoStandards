[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Visual References

This directory contains visual documentation for MokoStandards including diagrams, flowcharts, and screenshots.

## Contents

- [Workflow Diagrams](#workflow-diagrams)
- [Architecture Diagrams](#architecture-diagrams)
- [Process Flowcharts](#process-flowcharts)
- [GUI Screenshots](#gui-screenshots)

## Workflow Diagrams

### Release Workflow
See [release-workflow.md](./release-workflow.md) for the complete release process diagram.

### CI/CD Pipeline
See [cicd-pipeline.md](./cicd-pipeline.md) for the continuous integration and deployment workflow.

### Standards Compliance
See [standards-compliance.md](./standards-compliance.md) for the compliance checking workflow.

## Architecture Diagrams

### Repository Structure
See [repository-structure.md](./repository-structure.md) for the visual repository organization.

### Two-Tier Architecture
See [two-tier-architecture.md](./two-tier-architecture.md) for the organizational architecture.

## Process Flowcharts

### Script Execution Flow
See [script-execution-flow.md](./script-execution-flow.md) for how scripts process data.

### Validation Process
See [validation-process.md](./validation-process.md) for the validation workflow.

## GUI Screenshots

GUI screenshots are stored in `docs/images/gui/` directory:

- Bulk Update GUI
- Health Check GUI
- Demo Data Loader GUI
- File Distributor GUI

## Using These References

All diagrams use Mermaid syntax which renders natively in GitHub markdown. To view:

1. Open the markdown file on GitHub
2. Diagrams render automatically
3. Can also use Mermaid live editor: https://mermaid.live/

## Creating New Visual References

When adding new visuals:

1. Use Mermaid for diagrams (renders in markdown)
2. Store screenshots in `docs/images/`
3. Reference from relevant documentation
4. Update this README with new content
