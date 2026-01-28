#!/usr/bin/env python3
"""
Add metadata headers to Terraform files according to metadata-standards.md policy.
"""

import os
import sys
from pathlib import Path
import argparse
from datetime import datetime


def get_file_purpose(filepath):
    """Determine the purpose of a Terraform file based on its path and content."""
    name = filepath.name
    parts = filepath.parts
    
    # Map of path patterns to descriptions
    if 'repository-management' in parts:
        return "Repository template management and bulk operations configuration"
    elif 'repository-types' in parts:
        if 'default' in name:
            return "Default repository structure and configuration schema definitions"
        elif 'health' in name:
            return "Repository health scoring thresholds and indicators configuration"
        else:
            return "Repository type definitions and schemas"
    elif 'webserver' in parts:
        if 'ubuntu' in name and 'prod' in name:
            return "Production Ubuntu webserver infrastructure configuration"
        elif 'ubuntu' in name and 'dev' in name:
            return "Development Ubuntu webserver infrastructure configuration"
        elif 'windows' in name and 'prod' in name:
            return "Production Windows webserver infrastructure configuration"
        elif 'windows' in name and 'dev' in name:
            return "Development Windows webserver infrastructure configuration"
        else:
            return "Webserver infrastructure configuration"
    elif 'workstation' in parts:
        if 'ubuntu' in name and 'dev' in name:
            return "Development Ubuntu workstation configuration"
        elif 'windows' in name and 'dev' in name:
            return "Development Windows workstation configuration"
        else:
            return "Workstation configuration"
    elif name == 'main.tf':
        return "Main Terraform configuration entry point"
    elif name == 'variables.tf':
        return "Variable definitions for Terraform configuration"
    elif name == 'outputs.tf':
        return "Output definitions for Terraform configuration"
    else:
        return "Terraform configuration"


def get_file_name(filepath):
    """Generate a human-readable name for the file."""
    name = filepath.stem
    parts = filepath.parts
    
    # Convert snake_case or kebab-case to Title Case
    title = name.replace('-', ' ').replace('_', ' ').title()
    
    if 'repository-management' in parts:
        return f"Repository Management {title}"
    elif 'repository-types' in parts:
        return f"Repository Type {title}"
    elif 'webserver' in parts:
        return f"Webserver {title}"
    elif 'workstation' in parts:
        return f"Workstation {title}"
    else:
        return title


def create_metadata_block(filepath, relative_path):
    """Create a metadata locals block for a Terraform file."""
    name = get_file_name(filepath)
    description = get_file_purpose(filepath)
    today = datetime.now().strftime("%Y-%m-%d")
    
    metadata = f'''locals {{
  # Metadata for this configuration
  config_metadata = {{
    name            = "{name}"
    description     = "{description}"
    version         = "2.0.0"
    last_updated    = "{today}"
    maintainer      = "MokoStandards Team"
    schema_version  = "2.0"
    repository_url  = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type = "standards"
    format          = "terraform"
  }}
}}

'''
    return metadata


def has_metadata(content):
    """Check if file already has metadata."""
    return 'config_metadata' in content and 'locals {' in content


def add_metadata_to_file(filepath, dry_run=False):
    """Add metadata to a Terraform file."""
    repo_root = Path(__file__).resolve().parent.parent.parent
    relative_path = filepath.relative_to(repo_root)
    
    # Read file content
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has metadata
    if has_metadata(content):
        print(f"⏭️  Skipping {relative_path} (already has metadata)")
        return False
    
    # Find the first non-comment, non-empty line
    lines = content.split('\n')
    insert_index = 0
    comment_block = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            comment_block.append(line)
        else:
            insert_index = i
            break
    
    # Create metadata block
    metadata = create_metadata_block(filepath, relative_path)
    
    # Insert metadata after initial comments
    if comment_block:
        new_content = '\n'.join(comment_block) + '\n\n' + metadata
        if insert_index < len(lines):
            new_content += '\n'.join(lines[insert_index:])
    else:
        new_content = metadata + content
    
    if dry_run:
        print(f"[DRY-RUN] Would add metadata to: {relative_path}")
        return True
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Added metadata to: {relative_path}")
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Add metadata to Terraform files')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be changed without making changes')
    args = parser.parse_args()
    
    # Get repository root
    repo_root = Path(__file__).resolve().parent.parent.parent
    terraform_dir = repo_root / 'terraform'
    
    if not terraform_dir.exists():
        print(f"❌ Terraform directory not found: {terraform_dir}")
        return 1
    
    # Find all Terraform files
    tf_files = sorted(terraform_dir.rglob('*.tf'))
    
    print(f"Found {len(tf_files)} Terraform files")
    print()
    
    modified_count = 0
    for tf_file in tf_files:
        if add_metadata_to_file(tf_file, args.dry_run):
            modified_count += 1
    
    print()
    print("=" * 60)
    if args.dry_run:
        print(f"[DRY-RUN] Would modify {modified_count} of {len(tf_files)} files")
    else:
        print(f"Modified {modified_count} of {len(tf_files)} files")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
