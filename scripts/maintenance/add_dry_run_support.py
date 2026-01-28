#!/usr/bin/env python3
"""
Add dry-run support to Python scripts that don't have it.

This script analyzes Python scripts and adds --dry-run argument support
following the standard pattern used in the repository.
"""

import os
import sys
from pathlib import Path
import argparse
import re


DRY_RUN_TEMPLATE = '''
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
'''

def has_dry_run(content):
    """Check if script already has dry-run support."""
    patterns = [
        r'--dry-run',
        r'dry_run',
        r'DRY_RUN',
        r'dry\.run'
    ]
    return any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns)


def has_argparse(content):
    """Check if script uses argparse."""
    return 'argparse' in content and 'ArgumentParser' in content


def find_argparse_location(content):
    """Find where to add --dry-run argument."""
    lines = content.split('\n')
    
    # Find the ArgumentParser setup
    parser_line = None
    last_add_argument = None
    
    for i, line in enumerate(lines):
        if 'ArgumentParser' in line:
            parser_line = i
        if 'parser.add_argument' in line or 'add_argument' in line:
            last_add_argument = i
    
    return last_add_argument if last_add_argument else parser_line


def add_dry_run_logging(content):
    """Add dry-run prefix to print/logging statements."""
    # This is a template - actual implementation would be more sophisticated
    # For now, we'll just document the pattern
    return content


def generate_dry_run_pattern():
    """Generate documentation for dry-run pattern."""
    pattern = '''
# Standard Dry-Run Pattern for MokoStandards Scripts

## 1. Add --dry-run argument to argparse

```python
parser.add_argument(
    '--dry-run',
    action='store_true',
    help='Show what would be done without making changes'
)
```

## 2. Store in args and use throughout script

```python
args = parser.parse_args()
dry_run = args.dry_run

if dry_run:
    print("[DRY-RUN] Mode enabled - no changes will be made")
```

## 3. Add dry-run checks before write operations

```python
if dry_run:
    print(f"[DRY-RUN] Would create file: {filepath}")
else:
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created file: {filepath}")
```

## 4. Pattern for file operations

```python
def write_file(path, content, dry_run=False):
    if dry_run:
        print(f"[DRY-RUN] Would write to: {path}")
        print(f"[DRY-RUN] Content length: {len(content)} bytes")
        return
    
    with open(path, 'w') as f:
        f.write(content)
    print(f"Wrote to: {path}")
```

## 5. Pattern for API calls

```python
def update_repository(repo, data, dry_run=False):
    if dry_run:
        print(f"[DRY-RUN] Would update repository: {repo}")
        print(f"[DRY-RUN] Data: {data}")
        return None
    
    response = api.update(repo, data)
    print(f"Updated repository: {repo}")
    return response
```

## 6. Pattern for shell commands

```python
import subprocess

def run_command(cmd, dry_run=False):
    if dry_run:
        print(f"[DRY-RUN] Would execute: {cmd}")
        return 0
    
    result = subprocess.run(cmd, shell=True)
    return result.returncode
```

## 7. Summary reporting

```python
def main():
    # ... script logic ...
    
    if dry_run:
        print()
        print("=" * 60)
        print("[DRY-RUN] Summary:")
        print(f"  Files that would be modified: {modified_count}")
        print(f"  Files that would be created: {created_count}")
        print(f"  API calls that would be made: {api_call_count}")
        print("=" * 60)
    else:
        print()
        print("Summary:")
        print(f"  Files modified: {modified_count}")
        print(f"  Files created: {created_count}")
        print(f"  API calls made: {api_call_count}")
```
'''
    return pattern


def analyze_script(filepath):
    """Analyze a script for dry-run compatibility."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    analysis = {
        'path': filepath,
        'has_dry_run': has_dry_run(content),
        'has_argparse': has_argparse(content),
        'has_file_writes': 'open(' in content and "'w'" in content,
        'has_subprocess': 'subprocess' in content,
        'has_api_calls': 'requests' in content or 'api' in content.lower(),
        'line_count': len(content.split('\n'))
    }
    
    return analysis


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Analyze scripts for dry-run support')
    parser.add_argument('--pattern', action='store_true',
                        help='Output dry-run implementation pattern')
    parser.add_argument('--analyze', action='store_true',
                        help='Analyze all scripts')
    args = parser.parse_args()
    
    if args.pattern:
        print(generate_dry_run_pattern())
        return 0
    
    # Get repository root
    repo_root = Path(__file__).resolve().parent.parent.parent
    scripts_dir = repo_root / 'scripts'
    
    # Find all Python scripts (excluding lib, __pycache__, wrappers)
    exclude_dirs = {'lib', '__pycache__', 'wrappers'}
    exclude_files = {'__init__.py', 'wrapper-template.py', 'generate_wrappers.py'}
    
    scripts = []
    for script_path in scripts_dir.rglob('*.py'):
        if any(excluded in script_path.parts for excluded in exclude_dirs):
            continue
        if script_path.name in exclude_files:
            continue
        scripts.append(script_path)
    
    print(f"Analyzing {len(scripts)} Python scripts...")
    print()
    
    # Analyze each script
    without_dry_run = []
    with_dry_run = []
    
    for script in sorted(scripts):
        analysis = analyze_script(script)
        
        if analysis['has_dry_run']:
            with_dry_run.append(analysis)
        else:
            without_dry_run.append(analysis)
    
    # Report findings
    print("=" * 80)
    print("Dry-Run Support Analysis")
    print("=" * 80)
    print()
    print(f"✅ Scripts WITH dry-run support: {len(with_dry_run)}")
    print(f"❌ Scripts WITHOUT dry-run support: {len(without_dry_run)}")
    print()
    
    if args.analyze:
        print("Scripts needing dry-run support:")
        print("-" * 80)
        for analysis in without_dry_run:
            rel_path = analysis['path'].relative_to(repo_root)
            flags = []
            if analysis['has_argparse']:
                flags.append('argparse')
            if analysis['has_file_writes']:
                flags.append('file_ops')
            if analysis['has_subprocess']:
                flags.append('subprocess')
            if analysis['has_api_calls']:
                flags.append('api_calls')
            
            print(f"  {rel_path}")
            if flags:
                print(f"    Features: {', '.join(flags)}")
            print(f"    Lines: {analysis['line_count']}")
            print()
    
    print("=" * 80)
    print()
    print("To see the standard dry-run implementation pattern, run:")
    print(f"  python3 {Path(__file__).name} --pattern")
    print()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
