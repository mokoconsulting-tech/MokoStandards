#!/usr/bin/env python3
"""
Legal Document Generator

Generates Terms of Service and Privacy Policy documents for different types of websites.

Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program (./LICENSE).

FILE INFORMATION
DEFGROUP: Scripts.Generators
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/legal_doc_generator.py
VERSION: 01.00.00
BRIEF: Generate Terms of Service and Privacy Policy templates for websites
USAGE: python legal_doc_generator.py --type <website_type> [options]

ARGUMENTS
    --type: Type of website (membership, plain, ecommerce)
    --output-dir: Directory to save generated documents (default: current directory)
    --company-name: Company name (default: "Your Company")
    --website-url: Website URL (default: "https://yourwebsite.com")
    --contact-email: Contact email (default: "contact@yourcompany.com")
    --docs: Generate only one type of document (tos, privacy, or both if not specified)

EXAMPLES
    # Generate both documents for a membership website
    python legal_doc_generator.py --type membership --company-name "Acme Inc" \\
        --website-url "https://acme.com" --contact-email "legal@acme.com"
    
    # Generate only Terms of Service for an ecommerce site
    python legal_doc_generator.py --type ecommerce --docs tos --output-dir ./legal
    
    # Generate Privacy Policy for a plain website
    python legal_doc_generator.py --type plain --docs privacy
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict


class LegalDocGenerator:
    """Generator for legal documents based on website type"""
    
    def __init__(self, website_type: str, company_name: str, website_url: str, contact_email: str):
        """
        Initialize legal document generator
        
        Args:
            website_type: Type of website (membership, plain, ecommerce)
            company_name: Name of the company
            website_url: URL of the website
            contact_email: Contact email address
        """
        self.website_type = website_type.lower()
        self.company_name = company_name
        self.website_url = website_url
        self.contact_email = contact_email
        self.current_date = datetime.now().strftime("%B %d, %Y")
        
        # Validate website type
        if self.website_type not in ['membership', 'plain', 'ecommerce']:
            raise ValueError(f"Invalid website type: {website_type}. Must be 'membership', 'plain', or 'ecommerce'")
    
    def _markdown_to_html(self, markdown_text: str, title: str) -> str:
        """
        Convert markdown text to HTML
        
        Args:
            markdown_text: Markdown formatted text
            title: Document title for HTML head
            
        Returns:
            HTML formatted text
        """
        import re
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #555;
            margin-top: 20px;
        }}
        strong {{
            color: #2c3e50;
        }}
        ul {{
            margin: 10px 0;
            padding-left: 30px;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }}
        .footer {{
            margin-top: 40px;
            font-style: italic;
            color: #777;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
"""
        
        # Convert markdown to HTML
        lines = markdown_text.split('\n')
        in_list = False
        
        for line in lines:
            # H1 heading
            if line.startswith('# '):
                html += f"    <h1>{line[2:]}</h1>\n"
            # H2 heading
            elif line.startswith('## '):
                if in_list:
                    html += "    </ul>\n"
                    in_list = False
                html += f"    <h2>{line[3:]}</h2>\n"
            # H3 heading
            elif line.startswith('### '):
                if in_list:
                    html += "    </ul>\n"
                    in_list = False
                html += f"    <h3>{line[4:]}</h3>\n"
            # Bold text
            elif line.startswith('**') and '**' in line[2:]:
                html += f"    <p><strong>{line[2:].replace('**', '')}</strong></p>\n"
            # List item
            elif line.startswith('- '):
                if not in_list:
                    html += "    <ul>\n"
                    in_list = True
                html += f"        <li>{line[2:]}</li>\n"
            # Horizontal rule
            elif line.strip() == '---':
                if in_list:
                    html += "    </ul>\n"
                    in_list = False
                html += "    <hr>\n"
            # Paragraph
            elif line.strip():
                if in_list:
                    html += "    </ul>\n"
                    in_list = False
                html += f"    <p>{line}</p>\n"
            # Empty line
            else:
                if in_list:
                    html += "    </ul>\n"
                    in_list = False
        
        if in_list:
            html += "    </ul>\n"
        
        html += """</body>
</html>"""
        
        return html
    
    def generate_terms_of_service(self) -> str:
        """
        Generate Terms of Service document
        
        Returns:
            Terms of Service content as string
        """
        base_tos = f"""# Terms of Service

**Last Updated:** {self.current_date}

## 1. Acceptance of Terms

By accessing and using {self.company_name}'s website ({self.website_url}), you accept and agree to be bound by the terms and provision of this agreement.

## 2. Use License

Permission is granted to temporarily access the materials on {self.company_name}'s website for personal, non-commercial transitory viewing only.

## 3. Disclaimer

The materials on {self.company_name}'s website are provided on an 'as is' basis. {self.company_name} makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.

## 4. Limitations

In no event shall {self.company_name} or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on {self.company_name}'s website.

## 5. Accuracy of Materials

The materials appearing on {self.company_name}'s website could include technical, typographical, or photographic errors. {self.company_name} does not warrant that any of the materials on its website are accurate, complete or current.

## 6. Links

{self.company_name} has not reviewed all of the sites linked to its website and is not responsible for the contents of any such linked site.

## 7. Modifications

{self.company_name} may revise these terms of service for its website at any time without notice. By using this website you are agreeing to be bound by the then current version of these terms of service.

## 8. Governing Law

These terms and conditions are governed by and construed in accordance with the applicable laws and you irrevocably submit to the exclusive jurisdiction of the courts in that location.
"""
        
        # Add website-type specific sections
        if self.website_type == 'membership':
            base_tos += f"""

## 9. Membership Terms

### 9.1 Account Registration
Users must register for an account to access membership features. You are responsible for maintaining the confidentiality of your account credentials.

### 9.2 Membership Fees
Certain features may require payment of membership fees. All fees are non-refundable unless otherwise stated.

### 9.3 Account Termination
{self.company_name} reserves the right to terminate or suspend accounts that violate these terms of service.

### 9.4 User Content
Members may post content on the platform. You retain ownership of your content but grant {self.company_name} a license to use, display, and distribute it.

### 9.5 Member Conduct
Members must not:
- Post inappropriate, offensive, or illegal content
- Harass or intimidate other members
- Attempt to gain unauthorized access to the platform
- Use the platform for commercial purposes without authorization
"""
        
        elif self.website_type == 'ecommerce':
            base_tos += f"""

## 9. Ecommerce Terms

### 9.1 Product Information
{self.company_name} attempts to be as accurate as possible. However, we do not warrant that product descriptions or other content is accurate, complete, reliable, current, or error-free.

### 9.2 Pricing
All prices are subject to change without notice. We reserve the right to modify or discontinue products without notice.

### 9.3 Orders and Payment
By placing an order, you agree to provide current, complete, and accurate purchase information. We reserve the right to refuse or cancel any order.

### 9.4 Shipping and Delivery
Shipping times are estimates and not guaranteed. {self.company_name} is not responsible for delays caused by shipping carriers.

### 9.5 Returns and Refunds
Returns are accepted within 30 days of purchase. Items must be in original condition. Refunds will be processed within 10 business days.

### 9.6 Electronic Communications
When you place an order or send us emails, you consent to receiving electronic communications from us.
"""
        
        base_tos += f"""

## Contact Information

For questions about these Terms of Service, please contact us at:
- Email: {self.contact_email}
- Website: {self.website_url}

---

*This document was generated by MokoStandards Legal Document Generator*
"""
        
        return self._markdown_to_html(base_tos, f"{self.company_name} - Terms of Service")
    
    def generate_privacy_policy(self) -> str:
        """
        Generate Privacy Policy document
        
        Returns:
            Privacy Policy content as string
        """
        base_privacy = f"""# Privacy Policy

**Last Updated:** {self.current_date}

## 1. Introduction

{self.company_name} ("we", "our", or "us") respects your privacy and is committed to protecting your personal data. This privacy policy explains how we collect, use, and protect your information when you visit {self.website_url}.

## 2. Information We Collect

We may collect the following types of information:

### 2.1 Information You Provide
- Contact information (name, email address, phone number)
- Communication preferences
- Any other information you choose to provide

### 2.2 Automatically Collected Information
- IP address
- Browser type and version
- Operating system
- Pages visited and time spent on pages
- Referring website addresses
- Cookies and similar tracking technologies

## 3. How We Use Your Information

We use collected information for the following purposes:
- To provide and maintain our services
- To notify you about changes to our services
- To provide customer support
- To gather analysis or valuable information to improve our services
- To monitor the usage of our services
- To detect, prevent and address technical issues

## 4. Data Retention

We will retain your personal data only for as long as necessary for the purposes set out in this privacy policy.

## 5. Data Security

The security of your data is important to us. We strive to use commercially acceptable means to protect your personal data, but no method of transmission over the Internet or electronic storage is 100% secure.

## 6. Your Rights

You have the right to:
- Access your personal data
- Correct inaccurate data
- Request deletion of your data
- Object to processing of your data
- Request restriction of processing
- Data portability
- Withdraw consent

## 7. Cookies

We use cookies and similar tracking technologies to track activity on our website. You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent.

## 8. Third-Party Services

We may employ third-party companies and individuals to facilitate our service. These third parties have access to your personal data only to perform these tasks on our behalf.

## 9. Changes to This Privacy Policy

We may update our privacy policy from time to time. We will notify you of any changes by posting the new privacy policy on this page.
"""
        
        # Add website-type specific sections
        if self.website_type == 'membership':
            base_privacy += f"""

## 10. Membership-Specific Privacy Terms

### 10.1 Account Information
We collect account registration information including username, email, and password (encrypted).

### 10.2 Profile Information
Members may create profiles with additional personal information. You control what information is publicly visible.

### 10.3 Activity Data
We collect information about your activities on the platform, including posts, comments, and interactions with other members.

### 10.4 Communication Data
We may collect information from communications between members through our platform.

### 10.5 Member Directory
With your consent, your profile may be included in a member directory accessible to other members.
"""
        
        elif self.website_type == 'ecommerce':
            base_privacy += f"""

## 10. Ecommerce-Specific Privacy Terms

### 10.1 Payment Information
We collect payment information necessary to process transactions. Payment data is processed securely through third-party payment processors.

### 10.2 Order Information
We collect information about your purchases, including:
- Products ordered
- Shipping address
- Billing address
- Order history

### 10.3 Marketing Communications
With your consent, we may send you promotional emails about new products, special offers, or other information.

### 10.4 Transaction Data
We maintain records of all transactions for accounting, tax compliance, and customer service purposes.

### 10.5 Fraud Prevention
We may use your information to detect and prevent fraudulent transactions and other illegal activities.
"""
        
        elif self.website_type == 'plain':
            base_privacy += """

## 10. Information Website Privacy Terms

### 10.1 Analytics
We use analytics tools to understand how visitors interact with our website and improve user experience.

### 10.2 Newsletter Subscriptions
If you subscribe to our newsletter, we collect your email address and name (if provided).

### 10.3 Contact Forms
Information submitted through contact forms is used solely to respond to your inquiry.
"""
        
        base_privacy += f"""

## Contact Information

If you have any questions about this Privacy Policy, please contact us at:
- Email: {self.contact_email}
- Website: {self.website_url}

---

*This document was generated by MokoStandards Legal Document Generator*
"""
        
        return self._markdown_to_html(base_privacy, f"{self.company_name} - Privacy Policy")
    
    def save_document(self, content: str, filename: str, output_dir: Path) -> Path:
        """
        Save document to file
        
        Args:
            content: Document content
            filename: Output filename
            output_dir: Output directory
            
        Returns:
            Path to saved file
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        file_path = output_dir / filename
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Generated: {file_path}")
            return file_path
        except Exception as e:
            print(f"✗ Error saving {filename}: {e}", file=sys.stderr)
            raise


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate Terms of Service and Privacy Policy documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate both documents for a membership website
  python legal_doc_generator.py --type membership --company-name "Acme Inc" \\
      --website-url "https://acme.com" --contact-email "legal@acme.com"
  
  # Generate only Terms of Service for an ecommerce site
  python legal_doc_generator.py --type ecommerce --docs tos --output-dir ./legal
  
  # Generate Privacy Policy for a plain website
  python legal_doc_generator.py --type plain --docs privacy
        """
    )
    
    parser.add_argument(
        '--type',
        required=True,
        choices=['membership', 'plain', 'ecommerce'],
        help='Type of website (membership, plain, or ecommerce)'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='.',
        help='Directory to save generated documents (default: current directory)'
    )
    parser.add_argument(
        '--company-name',
        type=str,
        default='Your Company',
        help='Company name (default: "Your Company")'
    )
    parser.add_argument(
        '--website-url',
        type=str,
        default='https://yourwebsite.com',
        help='Website URL (default: "https://yourwebsite.com")'
    )
    parser.add_argument(
        '--contact-email',
        type=str,
        default='contact@yourcompany.com',
        help='Contact email (default: "contact@yourcompany.com")'
    )
    parser.add_argument(
        '--docs',
        choices=['tos', 'privacy', 'both'],
        default='both',
        help='Type of document to generate (tos, privacy, or both)'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir).resolve()
    
    print("=" * 80)
    print("LEGAL DOCUMENT GENERATOR")
    print("=" * 80)
    print(f"Website Type: {args.type}")
    print(f"Company Name: {args.company_name}")
    print(f"Website URL: {args.website_url}")
    print(f"Contact Email: {args.contact_email}")
    print(f"Output Directory: {output_dir}")
    print(f"Documents: {args.docs}")
    print("-" * 80)
    
    try:
        # Initialize generator
        generator = LegalDocGenerator(
            website_type=args.type,
            company_name=args.company_name,
            website_url=args.website_url,
            contact_email=args.contact_email
        )
        
        # Generate documents
        generated_files = []
        
        if args.docs in ['tos', 'both']:
            tos_content = generator.generate_terms_of_service()
            tos_file = generator.save_document(tos_content, 'TERMS_OF_SERVICE.html', output_dir)
            generated_files.append(tos_file)
        
        if args.docs in ['privacy', 'both']:
            privacy_content = generator.generate_privacy_policy()
            privacy_file = generator.save_document(privacy_content, 'PRIVACY_POLICY.html', output_dir)
            generated_files.append(privacy_file)
        
        # Print summary
        print("-" * 80)
        print("✅ Document generation complete!")
        print(f"\nGenerated {len(generated_files)} document(s):")
        for file_path in generated_files:
            print(f"  📄 {file_path}")
        
        print("\n⚠️  IMPORTANT NOTICE:")
        print("These generated documents are templates and should be reviewed by a")
        print("qualified attorney before use. Customize them to fit your specific")
        print("business needs and comply with applicable laws in your jurisdiction.")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
