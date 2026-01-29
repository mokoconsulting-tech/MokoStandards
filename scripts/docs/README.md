# Documentation Scripts

This directory contains scripts for documentation generation, maintenance, and validation, as well as comprehensive documentation about scripts and processes.

## Documentation Generation Scripts

### rebuild_indexes.py
Generate index.md files for all documentation folders automatically.

**Usage:**
```bash
# Rebuild all indexes in docs/
./scripts/docs/rebuild_indexes.py

# Rebuild indexes in custom directory
./scripts/docs/rebuild_indexes.py --root scripts

# Check if indexes need updates (CI mode)
./scripts/docs/rebuild_indexes.py --check
```

### check_doc_coverage.py
Check documentation coverage and identify missing documentation.

**Usage:**
```bash
# Check documentation coverage
./scripts/docs/check_doc_coverage.py

# Generate coverage report
./scripts/docs/check_doc_coverage.py --report
```

### generate_script_catalog.py
Generate a comprehensive catalog of all scripts in the repository.

**Usage:**
```bash
# Generate script catalog
./scripts/docs/generate_script_catalog.py

# Output in JSON format
./scripts/docs/generate_script_catalog.py --format json
```

### update_metadata.py
Update metadata in scripts and documentation files.

**Usage:**
```bash
# Update metadata for all scripts
./scripts/docs/update_metadata.py

# Update specific file
./scripts/docs/update_metadata.py --file path/to/script.py
```

## Documentation Files

### ARCHITECTURE.md
Comprehensive documentation of the scripts architecture, including organization, design patterns, and best practices.

### AUTO_CREATE_ORG_PROJECTS.md
Guide for automatically creating GitHub Projects for organization repositories.

### DRY_RUN_PATTERN.md
Standard pattern and implementation guide for adding dry-run support to scripts.

### NEW_SCRIPTS.md
Guidelines and templates for creating new scripts in the MokoStandards repository.

### QUICKSTART_ORG_PROJECTS.md
Quick start guide for setting up organization-wide GitHub Projects.

### REBUILD_STRATEGY.md
Strategy document for documentation rebuild and maintenance processes.

### REBUILD_PROGRESS.md
Progress tracking for documentation rebuild efforts.

### README_REBUILD.md
Documentation about README file rebuild and maintenance.

### README_update_gitignore_patterns.md
Guide for updating .gitignore patterns across repositories.

### LEGAL_DOC_GENERATOR_WEB_README.md
Documentation for the legal document generator web interface.

### legal_doc_generator.html
Web-based interface for generating legal documents (GPL notices, licensing info, etc.).

## Purpose

This directory serves dual purposes:
1. **Tools**: Scripts that generate, validate, and maintain documentation
2. **Documentation**: Comprehensive guides about scripts, processes, and development patterns
