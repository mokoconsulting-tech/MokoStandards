# Build Scripts

This directory contains scripts for build system management and compilation tasks.

## Scripts

### resolve_makefile.py
Resolve and identify the appropriate Makefile for different project types.

**Usage:**
```bash
# Auto-detect platform and find appropriate Makefile
./scripts/build/resolve_makefile.py

# Check specific directory
./scripts/build/resolve_makefile.py --dir /path/to/project

# Verbose output
./scripts/build/resolve_makefile.py --verbose
```

### moko-make
Build system wrapper script that automatically detects the correct Makefile to use based on project type and platform.

**Usage:**
```bash
# Build project (auto-detects Makefile)
./scripts/build/moko-make build

# Clean project
./scripts/build/moko-make clean

# Run tests
./scripts/build/moko-make test
```

## Purpose

These scripts automate the build process by:
- Detecting project type (Joomla, Dolibarr, generic PHP, etc.)
- Finding or generating the appropriate Makefile
- Providing a unified interface for build commands across different project types
