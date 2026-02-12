[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# CI/CD Pipeline

Visual representation of the continuous integration and deployment pipeline in MokoStandards.

## Overview

The CI/CD pipeline automatically validates code quality, security, and compliance on every push and pull request.

## Complete CI/CD Pipeline

```mermaid
flowchart TD
    A[Code Push/PR] --> B[GitHub Actions Trigger]
    
    B --> C[Standards Compliance Check]
    B --> D[Security Scanning]
    B --> E[Code Quality Analysis]
    
    C --> C1[File Headers]
    C --> C2[Tabs/Spaces Policy]
    C --> C3[File Encoding]
    C --> C4[Trailing Spaces]
    C --> C5[CHANGELOG Format]
    
    D --> D1[Secret Scanning]
    D --> D2[CodeQL Analysis]
    D --> D3[Dependency Review]
    
    E --> E1[Python Syntax]
    E --> E2[Shell Script Validation]
    E --> E3[PowerShell Linting]
    E --> E4[Markdown Links]
    
    C1 --> F{All Checks Pass?}
    C2 --> F
    C3 --> F
    C4 --> F
    C5 --> F
    D1 --> F
    D2 --> F
    D3 --> F
    E1 --> F
    E2 --> F
    E3 --> F
    E4 --> F
    
    F -->|Yes| G[✓ Build Passes]
    F -->|No| H[✗ Build Fails]
    
    G --> I{Is Main Branch?}
    I -->|Yes| J[Trigger Auto-Release]
    I -->|No| K[Ready for Merge]
    
    J --> L[Create Release]
    L --> M[Deploy to GitHub]
    
    style A fill:#e1f5ff
    style G fill:#c8e6c9
    style H fill:#ffccbc
    style M fill:#4caf50
```

## Standards Compliance Workflow

```mermaid
flowchart LR
    A[Start Compliance Check] --> B[File Headers]
    B --> C{Valid Headers?}
    C -->|Yes| D[Check Tabs/Spaces]
    C -->|No| FAIL1[❌ Fail: Missing/Invalid Headers]
    
    D --> E{Correct Indentation?}
    E -->|Yes| F[Check Encoding]
    E -->|No| FAIL2[❌ Fail: Tab/Space Policy Violation]
    
    F --> G{UTF-8 or ASCII?}
    G -->|Yes| H[Check Trailing Spaces]
    G -->|No| FAIL3[❌ Fail: Invalid Encoding]
    
    H --> I{No Trailing Spaces?}
    I -->|Yes| J[Check CHANGELOG]
    I -->|No| FAIL4[❌ Fail: Trailing Spaces Found]
    
    J --> K{[Unreleased] Present?}
    K -->|Yes| PASS[✅ Pass: All Standards Met]
    K -->|No| FAIL5[❌ Fail: Missing [Unreleased]]
    
    style PASS fill:#c8e6c9
    style FAIL1 fill:#ffccbc
    style FAIL2 fill:#ffccbc
    style FAIL3 fill:#ffccbc
    style FAIL4 fill:#ffccbc
    style FAIL5 fill:#ffccbc
```

## Security Scanning Pipeline

```mermaid
sequenceDiagram
    participant CI as CI Pipeline
    participant CS as CodeQL Scanner
    participant SS as Secret Scanner
    participant DR as Dependency Reviewer
    participant GH as GitHub
    
    CI->>CS: Initialize CodeQL
    CS->>CS: Build code database
    CS->>CS: Run security queries
    CS-->>CI: Report vulnerabilities
    
    CI->>SS: Scan for secrets
    SS->>SS: Check hardcoded credentials
    SS->>SS: Check API keys
    SS-->>CI: Report findings
    
    CI->>DR: Check dependencies
    DR->>DR: Analyze advisory database
    DR->>DR: Check version requirements
    DR-->>CI: Report vulnerable deps
    
    CI->>GH: Post results
    GH->>GH: Create security alerts
    GH-->>CI: Confirmation
```

## Code Quality Checks

```mermaid
graph TD
    A[Code Quality Gate] --> B[Python Validation]
    A --> C[Shell Validation]
    A --> D[PowerShell Validation]
    A --> E[Documentation Validation]
    
    B --> B1[Syntax Check]
    B --> B2[Import Validation]
    B --> B3[Docstring Check]
    
    C --> C1[ShellCheck]
    C --> C2[Bash Syntax]
    C --> C3[POSIX Compliance]
    
    D --> D1[PSScriptAnalyzer]
    D --> D2[Syntax Check]
    D --> D3[Best Practices]
    
    E --> E1[Markdown Link Check]
    E --> E2[Spelling Check]
    E --> E3[Format Validation]
    
    B1 --> F{All Pass?}
    B2 --> F
    B3 --> F
    C1 --> F
    C2 --> F
    C3 --> F
    D1 --> F
    D2 --> F
    D3 --> F
    E1 --> F
    E2 --> F
    E3 --> F
    
    F -->|Yes| G[✓ Quality Gate Passed]
    F -->|No| H[✗ Quality Gate Failed]
    
    style G fill:#c8e6c9
    style H fill:#ffccbc
```

## Pull Request Workflow

```mermaid
stateDiagram-v2
    [*] --> Draft: Create PR
    Draft --> InReview: Mark Ready
    InReview --> CIRunning: Trigger CI
    
    CIRunning --> CIPassed: All Checks Pass
    CIRunning --> CIFailed: Check Fails
    
    CIFailed --> FixingIssues: Developer Fixes
    FixingIssues --> CIRunning: Push Changes
    
    CIPassed --> CodeReview: Request Review
    CodeReview --> ChangesRequested: Issues Found
    CodeReview --> Approved: Looks Good
    
    ChangesRequested --> MakingChanges: Developer Updates
    MakingChanges --> CIRunning: Push Changes
    
    Approved --> ReadyToMerge: All Requirements Met
    ReadyToMerge --> Merged: Merge to Main
    Merged --> [*]
    
    note right of CIRunning
        Standards Compliance
        Security Scanning
        Code Quality Checks
    end note
```

## Deployment Flow

```mermaid
flowchart TD
    A[Merge to Main] --> B[Run Full CI Suite]
    B --> C{All Tests Pass?}
    C -->|No| D[Alert Team]
    C -->|Yes| E[Version Detection]
    
    E --> F{Version Bump Type}
    F -->|Major| G[X.0.0]
    F -->|Minor| H[0.X.0]
    F -->|Patch| I[0.0.X]
    
    G --> J[Update Versions]
    H --> J
    I --> J
    
    J --> K[Update CHANGELOG]
    K --> L[Create Git Tag]
    L --> M[Build Release Artifacts]
    M --> N[Create GitHub Release]
    N --> O[Publish Release Notes]
    O --> P[✓ Deployment Complete]
    
    style P fill:#4caf50
    style D fill:#ffccbc
```

## Workflow Triggers

```mermaid
graph LR
    A[Trigger Events] --> B[push]
    A --> C[pull_request]
    A --> D[workflow_dispatch]
    A --> E[schedule]
    
    B --> F[Standards Compliance]
    B --> G[Auto-Release on Main]
    
    C --> F
    C --> H[Security Scanning]
    
    D --> I[Manual Workflows]
    
    E --> J[Scheduled Maintenance]
    
    style A fill:#2196f3
```

## Related Files

- Workflow: `.github/workflows/standards-compliance.yml`
- Workflow: `.github/workflows/auto-release.yml`
- Workflow: `.github/workflows/codeql.yml`

## See Also

- [Release Workflow](./release-workflow.md)
- [Standards Compliance](./standards-compliance.md)
- [Security Policy](../policy/security/)
