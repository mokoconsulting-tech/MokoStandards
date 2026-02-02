#!/usr/bin/env python3
"""
Script Security Checker

Performs comprehensive security analysis on all scripts to detect
common security vulnerabilities and unsafe practices.

Usage:
    python3 check_script_security.py [--path PATH] [--strict]

METADATA:
    AUTHOR: Moko Consulting LLC
    COPYRIGHT: 2026 Moko Consulting LLC
    LICENSE: GPL-3.0-or-later
    VERSION: 01.00.00
    CREATED: 2026-02-02
    UPDATED: 2026-02-02
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


# Security patterns to detect
SECURITY_PATTERNS = {
    'hardcoded_secrets': {
        'severity': 'critical',
        'patterns': [
            (r'password\s*=\s*["\'](?![\$\{])[^"\']{4,}["\']', 'Hardcoded password'),
            (r'api[_-]?key\s*=\s*["\'][^"\']{10,}["\']', 'Hardcoded API key'),
            (r'secret\s*=\s*["\'][^"\']{10,}["\']', 'Hardcoded secret'),
            (r'token\s*=\s*["\'][^"\']{10,}["\']', 'Hardcoded token'),
            (r'aws[_-]?secret[_-]?access[_-]?key\s*=\s*["\'][^"\']+["\']', 'AWS secret key'),
            (r'private[_-]?key\s*=\s*["\'][^"\']+["\']', 'Private key'),
        ]
    },
    'command_injection': {
        'severity': 'high',
        'patterns': [
            (r'eval\s*\(', 'Use of eval() - command injection risk'),
            (r'exec\s*\(', 'Use of exec() - command injection risk'),
            (r'os\.system\s*\([^\)]*\$', 'os.system with variable - injection risk'),
            (r'subprocess\.(call|run|Popen).*shell\s*=\s*True', 'Shell=True with subprocess'),
            (r'\$\([^\)]*\$[^\)]*\)', 'Nested command substitution'),
        ]
    },
    'path_traversal': {
        'severity': 'high',
        'patterns': [
            (r'open\s*\([^\)]*\+[^\)]*\.\.', 'Path concatenation with ..'),
            (r'Path\s*\([^\)]*\+[^\)]*\.\.', 'Path concatenation with ..'),
            (r'os\.path\.join\s*\([^\)]*\.\.[^\)]*\)', 'Path join with ..'),
        ]
    },
    'sql_injection': {
        'severity': 'high',
        'patterns': [
            (r'execute\s*\([^\)]*%s[^\)]*%', 'SQL query with string formatting'),
            (r'execute\s*\([^\)]*\.format\s*\(', 'SQL query with .format()'),
            (r'execute\s*\([^\)]*f["\']', 'SQL query with f-string'),
            (r'cursor\.execute\s*\([^\)]*\+', 'SQL query with concatenation'),
        ]
    },
    'unsafe_deserialization': {
        'severity': 'high',
        'patterns': [
            (r'pickle\.loads?\s*\(', 'Unsafe pickle deserialization'),
            (r'yaml\.load\s*\([^\)]*(?!Loader)', 'Unsafe YAML load without Loader'),
            (r'marshal\.loads?\s*\(', 'Unsafe marshal deserialization'),
        ]
    },
    'weak_crypto': {
        'severity': 'medium',
        'patterns': [
            (r'hashlib\.md5\s*\(', 'Weak hash algorithm: MD5'),
            (r'hashlib\.sha1\s*\(', 'Weak hash algorithm: SHA1'),
            (r'random\.random\s*\(', 'Weak random for security purposes'),
        ]
    },
    'insecure_functions': {
        'severity': 'medium',
        'patterns': [
            (r'input\s*\([^\)]*password', 'input() echoes password - use getpass'),
            (r'print\s*\([^\)]*password', 'Printing password to console'),
            (r'logging\.[^(]*\([^\)]*password', 'Logging password'),
            (r'chmod\s+777', 'Overly permissive file permissions'),
            (r'os\.chmod\s*\([^\)]*0o777', 'Overly permissive file permissions'),
        ]
    },
    'missing_validation': {
        'severity': 'low',
        'patterns': [
            (r'requests\.get\s*\([^\)]*verify\s*=\s*False', 'SSL verification disabled'),
            (r'urllib\.request.*context\s*=.*ssl\._create_unverified_context', 'Unverified SSL'),
        ]
    }
}

# File extensions to check
SCRIPT_EXTENSIONS = {'.py', '.sh', '.bash', '.ps1'}


class ScriptSecurityChecker:
    """Performs security analysis on scripts."""
    
    def __init__(self, strict: bool = False, verbose: bool = False):
        self.strict = strict
        self.verbose = verbose
        self.findings = []
        self.stats = {
            'files_checked': 0,
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
    
    def check_file(self, file_path: Path) -> List[Dict]:
        """Check a single file for security issues."""
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            self.stats['files_checked'] += 1
            
            # Check each security pattern category
            for category, config in SECURITY_PATTERNS.items():
                severity = config['severity']
                patterns = config['patterns']
                
                for pattern, description in patterns:
                    for line_num, line in enumerate(lines, 1):
                        if re.search(pattern, line, re.IGNORECASE):
                            finding = {
                                'file': str(file_path),
                                'line': line_num,
                                'category': category,
                                'severity': severity,
                                'description': description,
                                'code_snippet': line.strip()
                            }
                            findings.append(finding)
                            self.stats[severity] += 1
        
        except Exception as e:
            if self.verbose:
                print(f"⚠️  Error checking {file_path}: {e}")
        
        return findings
    
    def check_directory(self, path: Path) -> List[Dict]:
        """Check all scripts in a directory recursively."""
        all_findings = []
        
        for file_path in path.rglob('*'):
            if file_path.is_file() and file_path.suffix in SCRIPT_EXTENSIONS:
                # Skip certain directories
                skip_dirs = {'.git', 'node_modules', '.venv', 'venv', '__pycache__'}
                if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                    continue
                
                findings = self.check_file(file_path)
                all_findings.extend(findings)
        
        return all_findings
    
    def generate_report(self, findings: List[Dict]) -> str:
        """Generate formatted security report."""
        report = []
        report.append("=" * 70)
        report.append("🛡️  SCRIPT SECURITY ANALYSIS REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Summary
        report.append("📊 Summary:")
        report.append(f"   Files checked: {self.stats['files_checked']}")
        report.append(f"   Total findings: {len(findings)}")
        report.append("")
        report.append("   By Severity:")
        report.append(f"      🔴 Critical: {self.stats['critical']}")
        report.append(f"      🟠 High:     {self.stats['high']}")
        report.append(f"      🟡 Medium:   {self.stats['medium']}")
        report.append(f"      🟢 Low:      {self.stats['low']}")
        report.append("")
        
        if not findings:
            report.append("✅ No security issues found!")
            report.append("")
            return "\n".join(report)
        
        # Group findings by severity
        by_severity = {}
        for finding in findings:
            severity = finding['severity']
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(finding)
        
        # Report critical findings first
        severity_order = ['critical', 'high', 'medium', 'low']
        severity_emoji = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }
        
        for severity in severity_order:
            if severity not in by_severity:
                continue
            
            findings_list = by_severity[severity]
            report.append("=" * 70)
            report.append(f"{severity_emoji[severity]} {severity.upper()} Severity ({len(findings_list)} findings)")
            report.append("=" * 70)
            report.append("")
            
            # Group by category
            by_category = {}
            for finding in findings_list:
                cat = finding['category']
                if cat not in by_category:
                    by_category[cat] = []
                by_category[cat].append(finding)
            
            for category, cat_findings in by_category.items():
                report.append(f"  {category.replace('_', ' ').title()} ({len(cat_findings)}):")
                report.append("")
                
                for finding in cat_findings[:10]:  # Limit to 10 per category
                    report.append(f"    📄 {finding['file']}:{finding['line']}")
                    report.append(f"       {finding['description']}")
                    if self.verbose:
                        report.append(f"       Code: {finding['code_snippet']}")
                    report.append("")
                
                if len(cat_findings) > 10:
                    report.append(f"    ... and {len(cat_findings) - 10} more")
                    report.append("")
        
        report.append("=" * 70)
        report.append("📋 Recommendations:")
        report.append("=" * 70)
        report.append("")
        report.append("1. Review and fix critical and high severity issues immediately")
        report.append("2. Use environment variables for sensitive data")
        report.append("3. Implement input validation and sanitization")
        report.append("4. Use parameterized queries for SQL")
        report.append("5. Avoid shell=True in subprocess calls")
        report.append("6. Use secure random generators for cryptographic purposes")
        report.append("7. Enable SSL verification for all network requests")
        report.append("")
        
        return "\n".join(report)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Check scripts for security vulnerabilities'
    )
    parser.add_argument(
        '--path',
        default='scripts',
        help='Path to check (default: scripts/)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Fail on any findings'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output including code snippets'
    )
    parser.add_argument(
        '--output',
        help='Output report to file'
    )
    args = parser.parse_args()
    
    repo_root = Path(__file__).parent.parent.parent
    check_path = repo_root / args.path
    
    if not check_path.exists():
        print(f"❌ Path not found: {check_path}")
        return 1
    
    print("🛡️  Script Security Checker")
    print("=" * 70)
    print(f"📂 Scanning: {check_path}")
    print("")
    
    # Perform checks
    checker = ScriptSecurityChecker(strict=args.strict, verbose=args.verbose)
    findings = checker.check_directory(check_path)
    
    # Generate report
    report = checker.generate_report(findings)
    print(report)
    
    # Save to file if requested
    if args.output:
        output_path = repo_root / args.output
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"📄 Report saved to: {output_path}")
        print("")
    
    # Exit code
    if findings:
        if checker.stats['critical'] > 0 or checker.stats['high'] > 0:
            print("❌ Security issues found - immediate action required!")
            return 1
        elif args.strict:
            print("⚠️  Security issues found (strict mode)")
            return 1
        else:
            print("⚠️  Security issues found - review recommended")
            return 0
    else:
        print("✅ No security issues detected")
        return 0


if __name__ == '__main__':
    sys.exit(main())
