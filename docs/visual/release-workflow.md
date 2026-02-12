[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Release Workflow

Visual representation of the automated release process in MokoStandards.

## Overview

This workflow automat triggers when changes are merged to the `main` branch and automatically creates releases based on commit messages.

## Release Workflow Diagram

```mermaid
flowchart TD
    A[Push to Main Branch] --> B{Check Commit Message}
    B -->|Contains '[skip release]'| Z[Skip Release]
    B -->|No skip marker| C[Analyze Commit Messages]
    
    C --> D{Determine Version Bump}
    D -->|'BREAKING CHANGE:'| E[Major Version]
    D -->|'feat:' or 'feature:'| F[Minor Version]
    D -->|Other commits| G[Patch Version]
    
    E --> H[Update Version Numbers]
    F --> H
    G --> H
    
    H --> I[Update CHANGELOG.md]
    I --> J[Move [Unreleased] to New Version]
    J --> K[Add Date Stamp]
    K --> L[Create New [Unreleased] Section]
    L --> M[Update H1 Version Header]
    
    M --> N[Run release_version.py]
    N --> O[Update VERSION in Files]
    O --> P[Update CONTRIBUTING.md]
    P --> Q[Update README.md]
    
    Q --> R[Create Git Tag]
    R --> S[Push Changes to Repository]
    S --> T[Extract Release Notes]
    T --> U[Create GitHub Release]
    
    U --> V[Attach Release Notes]
    V --> W[Publish Release]
    W --> X[✓ Release Complete]
    
    style A fill:#e1f5ff
    style X fill:#c8e6c9
    style Z fill:#ffccbc
    style E fill:#fff9c4
    style F fill:#fff9c4
    style G fill:#fff9c4
```

## Manual Override

The workflow can also be triggered manually with version override:

```mermaid
flowchart LR
    A[GitHub Actions Tab] --> B[Select 'Auto Release']
    B --> C[Click 'Run workflow']
    C --> D{Select Branch}
    D --> E[Choose Version Type]
    E -->|major| F[X.0.0]
    E -->|minor| G[0.X.0]
    E -->|patch| H[0.0.X]
    E -->|auto| I[Detect from Commits]
    
    F --> J[Trigger Workflow]
    G --> J
    H --> J
    I --> J
    
    style A fill:#e1f5ff
    style J fill:#c8e6c9
```

## Version Detection Logic

```mermaid
flowchart TD
    A[Scan Recent Commits] --> B{Check Messages}
    
    B -->|Pattern: 'BREAKING CHANGE:'| C[MAJOR Version]
    B -->|Pattern: 'feat:' or 'feature:'| D[MINOR Version]
    B -->|Pattern: 'fix:' or other| E[PATCH Version]
    
    C --> F[Example: 03.01.00 → 04.00.00]
    D --> G[Example: 03.01.00 → 03.02.00]
    E --> H[Example: 03.01.00 → 03.01.02]
    
    style C fill:#ff5252
    style D fill:#ffc107
    style E fill:#4caf50
```

## CHANGELOG Update Process

```mermaid
sequenceDiagram
    participant W as Workflow
    participant S as release_version.py
    participant C as CHANGELOG.md
    participant G as Git
    
    W->>S: Execute with version
    S->>C: Read current content
    C-->>S: Return content
    
    S->>S: Extract [Unreleased] items
    S->>C: Replace [Unreleased] with [X.Y.Z]
    S->>C: Add date stamp
    S->>C: Create new [Unreleased] section
    S->>C: Update H1 version
    
    S->>G: Stage changes
    S->>G: Create version tag
    G-->>S: Tag created
    
    S-->>W: Success
    W->>G: Push all changes
```

## File Updates

```mermaid
graph LR
    A[Version Bump] --> B[CHANGELOG.md]
    A --> C[README.md]
    A --> D[CONTRIBUTING.md]
    A --> E[VERSION file]
    A --> F[All Script Headers]
    
    B --> G[Git Commit]
    C --> G
    D --> G
    E --> G
    F --> G
    
    G --> H[Git Tag]
    H --> I[GitHub Release]
    
    style A fill:#2196f3
    style I fill:#4caf50
```

## Skip Release

To skip automatic release creation, include `[skip release]` anywhere in the commit message:

```bash
git commit -m "docs: Update README [skip release]"
```

## Related Files

- Workflow: `.github/workflows/auto-release.yml`
- Script: `scripts/maintenance/release_version.py`
- Policy: `docs/policy/changelog-standards.md`

## See Also

- [CHANGELOG Standards](../policy/changelog-standards.md)
- [Release Management](../guide/release-management.md)
- [CI/CD Pipeline](./cicd-pipeline.md)
