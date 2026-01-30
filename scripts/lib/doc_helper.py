"""
Documentation Helper Module

Provides utilities for loading and displaying script documentation from markdown files.

METADATA:
    AUTHOR: Moko Consulting LLC
    COPYRIGHT: 2025-2026 Moko Consulting LLC
    LICENSE: MIT
    VERSION: 01.00.00
    CREATED: 2026-01-29
    UPDATED: 2026-01-29
"""

import os
import sys
from pathlib import Path
from typing import Optional


def get_doc_path(script_path: str, doc_filename: Optional[str] = None) -> Optional[Path]:
    """
    Get the path to the documentation file for a script.
    
    Args:
        script_path: Path to the script file (__file__)
        doc_filename: Optional specific documentation filename
    
    Returns:
        Path to documentation file, or None if not found
    """
    script_file = Path(script_path)
    script_name = script_file.stem
    
    # Try to find documentation in multiple locations
    search_paths = []
    
    # 1. docs/scripts/{category}/{script_name}.md
    script_category = script_file.parent.name
    search_paths.append(Path("docs/scripts") / script_category / f"{script_name}.md")
    
    # 2. docs/{category}/{script_name}.md
    search_paths.append(Path("docs") / script_category / f"{script_name}.md")
    
    # 3. Specific doc file if provided
    if doc_filename:
        search_paths.append(Path("docs") / doc_filename)
    
    # 4. README in same directory
    search_paths.append(script_file.parent / "README.md")
    
    # Find first existing path
    repo_root = get_repo_root()
    for path in search_paths:
        full_path = repo_root / path
        if full_path.exists():
            return full_path
    
    return None


def get_repo_root() -> Path:
    """Get the repository root directory."""
    current = Path(__file__).resolve()
    
    # Walk up until we find .git or reach root
    for parent in [current] + list(current.parents):
        if (parent / ".git").exists():
            return parent
        if (parent / "README.md").exists() and (parent / "CHANGELOG.md").exists():
            return parent
    
    # Fallback to 2 levels up from this file
    return current.parent.parent


def load_documentation(script_path: str, doc_filename: Optional[str] = None) -> str:
    """
    Load documentation content for a script.
    
    Args:
        script_path: Path to the script file (__file__)
        doc_filename: Optional specific documentation filename
    
    Returns:
        Documentation content as string
    """
    doc_path = get_doc_path(script_path, doc_filename)
    
    if doc_path and doc_path.exists():
        return doc_path.read_text()
    
    # Return minimal help if no documentation found
    script_name = Path(script_path).name
    return f"""
{script_name}

No detailed documentation found for this script.

Run with --help to see command-line options.

For general MokoStandards documentation, see:
https://github.com/mokoconsulting-tech/MokoStandards
"""


def display_help(script_path: str, doc_filename: Optional[str] = None, 
                 show_full: bool = True) -> None:
    """
    Display help documentation for a script.
    
    Args:
        script_path: Path to the script file (__file__)
        doc_filename: Optional specific documentation filename
        show_full: If True, show full documentation; if False, show summary
    """
    content = load_documentation(script_path, doc_filename)
    
    if not show_full:
        # Extract just the first section (up to first ##)
        lines = content.split('\n')
        summary_lines = []
        header_found = False
        
        for line in lines:
            if line.startswith('# '):
                header_found = True
                summary_lines.append(line)
            elif line.startswith('## ') and header_found:
                break
            elif header_found:
                summary_lines.append(line)
        
        content = '\n'.join(summary_lines[:30])  # Limit to 30 lines
        content += "\n\n... (use --help-full for complete documentation)"
    
    print(content)


def add_help_argument(parser, script_path: str, doc_filename: Optional[str] = None):
    """
    Add help arguments to an ArgumentParser.
    
    Args:
        parser: argparse.ArgumentParser instance
        script_path: Path to the script file (__file__)
        doc_filename: Optional specific documentation filename
    
    Example:
        parser = argparse.ArgumentParser(description='My script')
        add_help_argument(parser, __file__)
    """
    parser.add_argument(
        '--help-doc',
        action='store_true',
        help='Display full documentation from markdown files'
    )
    
    parser.add_argument(
        '--help-full',
        action='store_true',
        help='Display complete documentation (same as --help-doc)'
    )
    
    # Store for later use
    parser._script_path = script_path
    parser._doc_filename = doc_filename


def handle_help_flags(args, script_path: str, doc_filename: Optional[str] = None) -> bool:
    """
    Handle help flags and display documentation if requested.
    
    Args:
        args: Parsed arguments from ArgumentParser
        script_path: Path to the script file (__file__)
        doc_filename: Optional specific documentation filename
    
    Returns:
        True if help was displayed (script should exit), False otherwise
    
    Example:
        args = parser.parse_args()
        if handle_help_flags(args, __file__):
            sys.exit(0)
    """
    if hasattr(args, 'help_doc') and args.help_doc:
        display_help(script_path, doc_filename, show_full=True)
        return True
    
    if hasattr(args, 'help_full') and args.help_full:
        display_help(script_path, doc_filename, show_full=True)
        return True
    
    return False


def get_version_from_file(script_path: str) -> str:
    """
    Extract version from script file metadata.
    
    Args:
        script_path: Path to the script file
    
    Returns:
        Version string or 'unknown'
    """
    try:
        content = Path(script_path).read_text()
        
        # Look for VERSION: pattern in metadata
        for line in content.split('\n')[:50]:  # Check first 50 lines
            if 'VERSION:' in line:
                # Extract version number
                parts = line.split('VERSION:')
                if len(parts) > 1:
                    version = parts[1].strip().split()[0]
                    return version
        
        return 'unknown'
    except Exception:
        return 'unknown'
