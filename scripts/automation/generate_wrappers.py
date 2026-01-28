#!/usr/bin/env python3
"""
Generate shell and PowerShell wrappers for all Python scripts.

This script automatically creates wrapper scripts for each Python script in the repository,
making them easier to call from different environments.
"""

import os
import sys
from pathlib import Path
import argparse


def get_category_from_path(script_path):
    """Determine the script category from its path."""
    parts = script_path.parts
    if 'automation' in parts:
        return 'automation'
    elif 'validation' in parts or 'validate' in parts:
        return 'validation'
    elif 'maintenance' in parts:
        return 'maintenance'
    elif 'analysis' in parts:
        return 'analysis'
    elif 'build' in parts:
        return 'build'
    elif 'release' in parts:
        return 'release'
    elif 'tests' in parts:
        return 'tests'
    elif 'docs' in parts:
        return 'docs'
    else:
        return 'automation'  # default


def create_bash_wrapper(script_path, script_name, category, template_content, output_dir):
    """Create a bash wrapper for a Python script."""
    wrapper_name = script_name.replace('.py', '.sh')
    wrapper_path = output_dir / wrapper_name
    
    # Replace template placeholders
    wrapper_content = template_content
    wrapper_content = wrapper_content.replace('{{SCRIPT_NAME}}', script_name.replace('.py', ''))
    wrapper_content = wrapper_content.replace('{{SCRIPT_PATH}}', str(script_path))
    wrapper_content = wrapper_content.replace('{{SCRIPT_CATEGORY}}', category)
    
    with open(wrapper_path, 'w', encoding='utf-8') as f:
        f.write(wrapper_content)
    
    # Make executable
    os.chmod(wrapper_path, 0o755)
    
    return wrapper_path


def create_powershell_wrapper(script_path, script_name, category, template_content, output_dir):
    """Create a PowerShell wrapper for a Python script."""
    wrapper_name = script_name.replace('.py', '.ps1')
    wrapper_path = output_dir / wrapper_name
    
    # Replace template placeholders
    wrapper_content = template_content
    wrapper_content = wrapper_content.replace('{{SCRIPT_NAME}}', script_name.replace('.py', ''))
    wrapper_content = wrapper_content.replace('{{SCRIPT_PATH}}', str(script_path).replace('\\', '/'))
    wrapper_content = wrapper_content.replace('{{SCRIPT_CATEGORY}}', category)
    
    with open(wrapper_path, 'w', encoding='utf-8') as f:
        f.write(wrapper_content)
    
    return wrapper_path


def find_python_scripts(repo_root):
    """Find all Python scripts in the repository."""
    scripts_dir = repo_root / 'scripts'
    python_scripts = []
    
    # Exclude lib and tests directories, and template files
    exclude_dirs = {'lib', '__pycache__', '.pytest_cache'}
    exclude_files = {'__init__.py', 'wrapper-template.py'}
    
    for script_path in scripts_dir.rglob('*.py'):
        # Skip if in excluded directory
        if any(excluded in script_path.parts for excluded in exclude_dirs):
            continue
        
        # Skip if excluded file
        if script_path.name in exclude_files:
            continue
        
        # Make path relative to repo root
        rel_path = script_path.relative_to(repo_root)
        python_scripts.append(rel_path)
    
    return sorted(python_scripts)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate wrappers for Python scripts')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be created without creating wrappers')
    parser.add_argument('--bash-only', action='store_true',
                        help='Generate only bash wrappers')
    parser.add_argument('--powershell-only', action='store_true',
                        help='Generate only PowerShell wrappers')
    args = parser.parse_args()
    
    # Get repository root
    repo_root = Path(__file__).resolve().parent.parent.parent
    
    # Load wrapper templates
    templates_dir = repo_root / 'scripts' / 'lib'
    bash_template_path = templates_dir / 'wrapper-template.sh'
    ps_template_path = templates_dir / 'wrapper-template.ps1'
    
    if not bash_template_path.exists():
        print(f"❌ Bash template not found: {bash_template_path}")
        return 1
    
    if not ps_template_path.exists():
        print(f"❌ PowerShell template not found: {ps_template_path}")
        return 1
    
    with open(bash_template_path, 'r', encoding='utf-8') as f:
        bash_template = f.read()
    
    with open(ps_template_path, 'r', encoding='utf-8') as f:
        ps_template = f.read()
    
    # Create wrappers directory
    wrappers_dir = repo_root / 'scripts' / 'wrappers'
    if not args.dry_run:
        wrappers_dir.mkdir(exist_ok=True)
        (wrappers_dir / 'bash').mkdir(exist_ok=True)
        (wrappers_dir / 'powershell').mkdir(exist_ok=True)
    
    # Find all Python scripts
    python_scripts = find_python_scripts(repo_root)
    
    print(f"Found {len(python_scripts)} Python scripts")
    print()
    
    bash_count = 0
    ps_count = 0
    
    # Generate wrappers
    for script_path in python_scripts:
        script_name = script_path.name
        category = get_category_from_path(script_path)
        
        # Generate bash wrapper
        if not args.powershell_only:
            if args.dry_run:
                print(f"[DRY-RUN] Would create bash wrapper: wrappers/bash/{script_name.replace('.py', '.sh')}")
            else:
                wrapper_path = create_bash_wrapper(
                    script_path, script_name, category, bash_template,
                    wrappers_dir / 'bash'
                )
                print(f"✅ Created bash wrapper: {wrapper_path.relative_to(repo_root)}")
            bash_count += 1
        
        # Generate PowerShell wrapper
        if not args.bash_only:
            if args.dry_run:
                print(f"[DRY-RUN] Would create PowerShell wrapper: wrappers/powershell/{script_name.replace('.py', '.ps1')}")
            else:
                wrapper_path = create_powershell_wrapper(
                    script_path, script_name, category, ps_template,
                    wrappers_dir / 'powershell'
                )
                print(f"✅ Created PowerShell wrapper: {wrapper_path.relative_to(repo_root)}")
            ps_count += 1
    
    print()
    print("=" * 60)
    if args.dry_run:
        print("[DRY-RUN] Summary:")
    else:
        print("Summary:")
    print(f"  Python scripts found: {len(python_scripts)}")
    if not args.powershell_only:
        print(f"  Bash wrappers: {bash_count}")
    if not args.bash_only:
        print(f"  PowerShell wrappers: {ps_count}")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
