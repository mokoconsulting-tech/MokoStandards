# Fix Scripts

This directory contains scripts for fixing and repairing code issues automatically.

## Scripts

### file_headers.py
Fix and standardize file headers across the repository.

**Usage:**
```bash
# Fix file headers in current directory
./scripts/fix/file_headers.py

# Fix specific file
./scripts/fix/file_headers.py --file path/to/file.py

# Dry run to preview changes
./scripts/fix/file_headers.py --dry-run

# Fix headers in specific directory
./scripts/fix/file_headers.py --dir src/
```

### tabs.py
Convert tabs to spaces (or vice versa) according to file type and coding standards.

**Usage:**
```bash
# Fix tabs in all files (respecting language-specific rules)
./scripts/fix/tabs.py --type all

# Fix tabs in Python files (convert to 4 spaces)
./scripts/fix/tabs.py --type python

# Fix tabs in YAML files (convert to 2 spaces)
./scripts/fix/tabs.py --type yaml

# Dry run to preview changes
./scripts/fix/tabs.py --type python --dry-run

# Fix specific file
./scripts/fix/tabs.py --type python --file path/to/file.py
```

**Supported Languages:**
- YAML (.yml, .yaml) - 2 spaces
- Python (.py) - 4 spaces (PEP 8)
- Haskell (.hs, .lhs) - 2 spaces
- F# (.fs, .fsx, .fsi) - 4 spaces
- CoffeeScript (.coffee) - 2 spaces
- Nim (.nim, .nims, .nimble) - 2 spaces
- JSON (.json) - 2 spaces
- reStructuredText (.rst) - 3 spaces

### trailing_spaces.py
Remove trailing whitespace from files.

**Usage:**
```bash
# Remove trailing spaces from all files
./scripts/fix/trailing_spaces.py

# Remove trailing spaces from specific file
./scripts/fix/trailing_spaces.py --file path/to/file

# Dry run to preview changes
./scripts/fix/trailing_spaces.py --dry-run

# Fix specific directory
./scripts/fix/trailing_spaces.py --dir src/
```

## Purpose

These scripts automatically fix common code quality issues:
- Standardize file headers according to MokoStandards policy
- Enforce indentation standards (tabs vs spaces based on language)
- Remove trailing whitespace
- Apply consistent formatting

All scripts support `--dry-run` mode to preview changes before applying them.
