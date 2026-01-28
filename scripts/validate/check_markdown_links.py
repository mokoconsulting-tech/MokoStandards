#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts.Validate
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: scripts/validate/check_markdown_links.py
VERSION: 02.00.00
BRIEF: Validates links in markdown files to ensure they are not broken
PATH: /scripts/validate/check_markdown_links.py
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def extract_markdown_links(file_path: Path) -> List[Tuple[int, str, str]]:
    """
    Extract all links from a markdown file.
    
    Args:
        file_path: Path to markdown file
        
    Returns:
        List of (line_number, link_text, link_url) tuples
    """
    links = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = list(f)

        # First pass: collect reference definitions of the form:
        # [ref]: url
        ref_definitions: Dict[str, str] = {}
        for line in lines:
            ref_def_match = re.match(r'^\s*\[([^\]]+)\]:\s*(\S+)', line)
            if ref_def_match:
                ref_label = ref_def_match.group(1)
                ref_url = ref_def_match.group(2)
                ref_definitions[ref_label] = ref_url

        # Second pass: extract links
        for line_num, line in enumerate(lines, start=1):
            # Skip reference definition lines
            if re.match(r'^\s*\[([^\]]+)\]:\s*\S+', line):
                continue

            # Match markdown links: [text](url)
            for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', line):
                text = match.group(1)
                url = match.group(2)
                links.append((line_num, text, url))

            # Match reference links: [text][ref]
            for match in re.finditer(r'\[([^\]]+)\]\[([^\]]+)\]', line):
                text = match.group(1)
                ref = match.group(2)
                # Only include reference links that have a defined target
                if ref in ref_definitions:
                    resolved_url = ref_definitions[ref]
                    links.append((line_num, text, resolved_url))

            # Match shortcut reference links: [text] (where text is also the ref)
            # Exclude inline links [text](url) and explicit reference links [text][ref]
            # Also exclude the second bracket in [text1][text2]
            for match in re.finditer(r'(?<!\])\[([^\]]+)\](?!\(|\[)', line):
                text = match.group(1)
                # Check if this text has a reference definition
                if text in ref_definitions:
                    resolved_url = ref_definitions[text]
                    links.append((line_num, text, resolved_url))

            # Match autolinks: <url>
            for match in re.finditer(r'<(https?://[^>]+)>', line):
                url = match.group(1)
                links.append((line_num, url, url))
    
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
    
    return links


def is_external_link(url: str) -> bool:
    """
    Check if a URL is an external link.
    
    Args:
        url: URL to check
        
    Returns:
        True if external link
    """
    return url.startswith(("http://", "https://", "ftp://", "mailto:"))


def is_anchor_link(url: str) -> bool:
    """
    Check if a URL is an anchor/fragment link.
    
    Args:
        url: URL to check
        
    Returns:
        True if anchor link
    """
    return url.startswith("#")


def validate_local_file_link(base_path: Path, url: str) -> bool:
    """
    Validate a local file link.
    
    Args:
        base_path: Base path of the markdown file
        url: Relative file path
        
    Returns:
        True if file exists
    """
    # Remove any anchor/fragment
    if "#" in url:
        url = url.split("#")[0]
    
    # Remove any query parameters
    if "?" in url:
        url = url.split("?")[0]
    
    if not url:  # Pure anchor link
        return True
    
    # Resolve the path
    try:
        target_path = (base_path.parent / url).resolve()
        return target_path.exists()
    except Exception:
        return False


def analyze_markdown_files(root: Path, skip_external: bool = False) -> Dict:
    """
    Analyze all markdown files for broken links.
    
    Args:
        root: Root directory to search
        skip_external: Whether to skip checking external links
        
    Returns:
        Dictionary with analysis results
    """
    results = {
        "total_files": 0,
        "total_links": 0,
        "external_links": 0,
        "local_links": 0,
        "anchor_links": 0,
        "broken_links": [],
    }
    
    # Find all markdown files
    md_files = list(root.rglob("*.md"))
    results["total_files"] = len(md_files)
    
    for md_file in md_files:
        links = extract_markdown_links(md_file)
        
        for line_num, text, url in links:
            results["total_links"] += 1
            
            if is_anchor_link(url):
                results["anchor_links"] += 1
                # We don't validate anchor links within the same file
                continue
            
            elif is_external_link(url):
                results["external_links"] += 1
                # Skip external link validation if requested
                if skip_external:
                    continue
                # Note: We don't validate external links by default as it requires network access
                continue
            
            else:
                results["local_links"] += 1
                # Validate local file link
                if not validate_local_file_link(md_file, url):
                    rel_path = md_file.relative_to(root)
                    results["broken_links"].append({
                        "file": str(rel_path),
                        "line": line_num,
                        "text": text,
                        "url": url,
                    })
    
    return results


def print_report(results: Dict, root: Path) -> None:
    """
    Print validation report.
    
    Args:
        results: Analysis results
        root: Root directory analyzed
    """
    print("\n" + "=" * 80)
    print("MARKDOWN LINK VALIDATION REPORT")
    print("=" * 80)
    print(f"\nDirectory: {root}")
    
    print(f"\n📊 SUMMARY")
    print("-" * 80)
    print(f"Markdown files:   {results['total_files']:,}")
    print(f"Total links:      {results['total_links']:,}")
    print(f"External links:   {results['external_links']:,}")
    print(f"Local links:      {results['local_links']:,}")
    print(f"Anchor links:     {results['anchor_links']:,}")
    print(f"Broken links:     {len(results['broken_links']):,}")
    
    if results["broken_links"]:
        print(f"\n❌ BROKEN LINKS")
        print("-" * 80)
        
        for broken in results["broken_links"]:
            print(f"\nFile: {broken['file']}")
            print(f"Line: {broken['line']}")
            print(f"Text: {broken['text']}")
            print(f"URL:  {broken['url']}")
    else:
        print(f"\n✅ No broken links found!")
    
    print("\n" + "=" * 80)


def main() -> int:
    """
    Main entry point for link validator.
    
    Returns:
        Exit code (0 for success, 1 if broken links found)
    """
    parser = argparse.ArgumentParser(
        description="Validate links in markdown files"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Root directory to analyze (default: current directory)"
    )
    parser.add_argument(
        "--skip-external",
        action="store_true",
        help="Skip external link validation"
    )
    
    args = parser.parse_args()
    root = Path(args.path).resolve()
    
    if not root.exists():
        print(f"Error: Path does not exist: {root}", file=sys.stderr)
        return 1
    
    print(f"Analyzing markdown links in: {root}")
    
    results = analyze_markdown_files(root, args.skip_external)
    print_report(results, root)
    
    # Return non-zero exit code if broken links found
    return 1 if results["broken_links"] else 0


if __name__ == "__main__":
    sys.exit(main())
