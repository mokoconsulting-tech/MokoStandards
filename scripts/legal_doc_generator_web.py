#!/usr/bin/env python3
"""
Legal Document Generator - Web Interface

Web-based interface for generating Terms of Service and Privacy Policy documents.

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
PATH: /scripts/legal_doc_generator_web.py
VERSION: 01.00.00
BRIEF: Web interface for generating Terms of Service and Privacy Policy templates
USAGE: python legal_doc_generator_web.py [--port PORT] [--host HOST]

EXAMPLES
    # Start web server on default port 5000
    python legal_doc_generator_web.py
    
    # Start on custom port
    python legal_doc_generator_web.py --port 8080
    
    # Make accessible from network
    python legal_doc_generator_web.py --host 0.0.0.0
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# Try to import Flask
try:
    from flask import Flask, render_template_string, request, jsonify
except ImportError:
    print("Error: Flask is required for the web interface.", file=sys.stderr)
    print("Install it with: pip install flask", file=sys.stderr)
    sys.exit(1)

# Import the generator class from the CLI version
import html as html_module


class LegalDocGenerator:
    """Generator for legal documents based on website type"""
    
    def __init__(self, website_type: str, company_name: str, website_url: str, contact_email: str,
                 website_name: str = None, business_contact: str = None, compliance_email: str = None,
                 physical_address: str = None, country: str = None, 
                 industry: str = None, data_protection_officer: str = None,
                 gdpr_compliant: bool = False, ccpa_compliant: bool = False, 
                 effective_date: str = None, version: str = "1.0"):
        """Initialize legal document generator with enhanced customization options"""
        self.website_type = website_type.lower()
        self.company_name = company_name
        self.website_name = website_name or company_name
        self.website_url = website_url
        self.contact_email = contact_email
        self.business_contact = business_contact or contact_email
        self.compliance_email = compliance_email or contact_email
        self.physical_address = physical_address
        self.country = country or "applicable jurisdiction"
        self.industry = industry
        self.data_protection_officer = data_protection_officer
        self.gdpr_compliant = gdpr_compliant
        self.ccpa_compliant = ccpa_compliant
        self.effective_date = effective_date or datetime.now().strftime("%B %d, %Y")
        self.version = version
        self.current_date = datetime.now().strftime("%B %d, %Y")
        
        if self.website_type not in ['membership', 'plain', 'ecommerce']:
            raise ValueError(f"Invalid website type: {website_type}")
    
    def _markdown_to_html(self, markdown_text: str, title: str) -> str:
        """Convert markdown text to HTML"""
        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_module.escape(title)}</title>
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
    </style>
</head>
<body>
"""
        
        lines = markdown_text.split('\n')
        in_list = False
        
        for line in lines:
            if line.startswith('# '):
                html_doc += f"    <h1>{html_module.escape(line[2:])}</h1>\n"
            elif line.startswith('## '):
                if in_list:
                    html_doc += "    </ul>\n"
                    in_list = False
                html_doc += f"    <h2>{html_module.escape(line[3:])}</h2>\n"
            elif line.startswith('### '):
                if in_list:
                    html_doc += "    </ul>\n"
                    in_list = False
                html_doc += f"    <h3>{html_module.escape(line[4:])}</h3>\n"
            elif line.startswith('**') and '**' in line[2:]:
                text = line[2:]
                if text.endswith('**'):
                    text = text[:-2]
                html_doc += f"    <p><strong>{html_module.escape(text)}</strong></p>\n"
            elif line.startswith('- '):
                if not in_list:
                    html_doc += "    <ul>\n"
                    in_list = True
                html_doc += f"        <li>{html_module.escape(line[2:])}</li>\n"
            elif line.strip() == '---':
                if in_list:
                    html_doc += "    </ul>\n"
                    in_list = False
                html_doc += "    <hr>\n"
            elif line.strip():
                if in_list:
                    html_doc += "    </ul>\n"
                    in_list = False
                html_doc += f"    <p>{html_module.escape(line)}</p>\n"
            else:
                if in_list:
                    html_doc += "    </ul>\n"
                    in_list = False
        
        if in_list:
            html_doc += "    </ul>\n"
        
        html_doc += """</body>
</html>"""
        
        return html_doc
    
    def generate_terms_of_service(self) -> str:
        """Generate Terms of Service document"""
        base_tos = f"""# Terms of Service

**Version:** {self.version}  
**Last Updated:** {self.current_date}  
**Effective Date:** {self.effective_date}

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

These terms and conditions are governed by and construed in accordance with the laws of {self.country} and you irrevocably submit to the exclusive jurisdiction of the courts in that location.
"""
        
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
        
        # Add enterprise compliance sections if applicable
        compliance_sections = ""
        
        if self.gdpr_compliant or self.ccpa_compliant:
            compliance_sections += "\n\n## Regulatory Compliance\n\n"
            
            if self.gdpr_compliant:
                compliance_sections += """### GDPR Compliance (European Users)

For users in the European Union, we comply with the General Data Protection Regulation (GDPR). You have the right to:
- Access your personal data
- Rectify inaccurate data
- Request erasure of your data ("right to be forgotten")
- Restrict processing of your data
- Data portability
- Object to automated decision-making

To exercise these rights, please contact our Data Protection Officer at: {dpo_email}

""".format(dpo_email=self.data_protection_officer or self.compliance_email)
            
            if self.ccpa_compliant:
                compliance_sections += """### CCPA Compliance (California Users)

For California residents, we comply with the California Consumer Privacy Act (CCPA). You have the right to:
- Know what personal information is collected
- Know whether your personal information is sold or disclosed
- Say no to the sale of personal information
- Access your personal information
- Request deletion of your personal information
- Not be discriminated against for exercising your CCPA rights

To submit a request, contact us at: {compliance_email}

""".format(compliance_email=self.compliance_email)
        
        if self.industry:
            compliance_sections += f"\n### Industry-Specific Compliance\n\nThis service operates in the {self.industry} industry and complies with applicable industry-specific regulations and standards.\n"
        
        base_tos += compliance_sections
        
        # Build contact information section
        contact_info = f"""

## Contact Information

For questions about these Terms of Service, please contact us at:
- General Contact: {self.contact_email}
- Business Inquiries: {self.business_contact}"""
        
        if self.compliance_email != self.contact_email:
            contact_info += f"\n- Legal/Compliance: {self.compliance_email}"
        
        if self.data_protection_officer:
            contact_info += f"\n- Data Protection Officer: {self.data_protection_officer}"
        
        contact_info += f"\n- Website: {self.website_url}"
        
        if self.physical_address:
            contact_info += f"\n- Mailing Address: {self.physical_address}"
        
        contact_info += f"""

## Document Information

- Version: {self.version}
- Last Updated: {self.current_date}
- Effective Date: {self.effective_date}

---

*This document was generated by MokoStandards Legal Document Generator*
"""
        
        base_tos += contact_info
        
        return self._markdown_to_html(base_tos, f"{self.website_name} - Terms of Service")
    
    def generate_privacy_policy(self) -> str:
        """Generate Privacy Policy document"""
        base_privacy = f"""# Privacy Policy

**Version:** {self.version}  
**Last Updated:** {self.current_date}  
**Effective Date:** {self.effective_date}

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
        
        # Add regulatory compliance sections for Privacy Policy
        compliance_sections = ""
        
        if self.gdpr_compliant or self.ccpa_compliant:
            compliance_sections += "\n\n## Your Privacy Rights\n\n"
            
            if self.gdpr_compliant:
                compliance_sections += """### GDPR Rights (European Users)

Under the General Data Protection Regulation (GDPR), you have enhanced privacy rights:

**Right to Access:** You can request a copy of your personal data.

**Right to Rectification:** You can request correction of inaccurate data.

**Right to Erasure:** You can request deletion of your personal data ("right to be forgotten").

**Right to Restrict Processing:** You can request limitation of how we process your data.

**Right to Data Portability:** You can receive your data in a structured, machine-readable format.

**Right to Object:** You can object to processing of your personal data.

**Right to Withdraw Consent:** You can withdraw consent for data processing at any time.

**Right to Lodge a Complaint:** You can file a complaint with your local data protection authority.

To exercise your rights, contact our Data Protection Officer at: {dpo_email}

""".format(dpo_email=self.data_protection_officer or self.compliance_email)
            
            if self.ccpa_compliant:
                compliance_sections += """### CCPA Rights (California Residents)

Under the California Consumer Privacy Act (CCPA), you have specific privacy rights:

**Right to Know:** You have the right to know what personal information we collect, use, disclose, and sell.

**Right to Delete:** You have the right to request deletion of your personal information.

**Right to Opt-Out:** You have the right to opt-out of the sale of your personal information.

**Right to Non-Discrimination:** You have the right to not be discriminated against for exercising your CCPA rights.

**Authorized Agent:** You may designate an authorized agent to make requests on your behalf.

To submit a CCPA request, contact us at: {compliance_email}

We will verify your identity before processing your request. We aim to respond within 45 days of receipt.

""".format(compliance_email=self.compliance_email)
        
        if self.data_protection_officer:
            compliance_sections += f"""\n### Data Protection Officer\n\nWe have appointed a Data Protection Officer (DPO) to oversee our data protection strategy and ensure compliance with data protection laws. You can contact our DPO at: {self.data_protection_officer}\n"""
        
        base_privacy += compliance_sections
        
        # Build contact information section
        contact_info = f"""

## Contact Information

If you have any questions about this Privacy Policy, please contact us at:
- General Contact: {self.contact_email}
- Business Inquiries: {self.business_contact}"""
        
        if self.compliance_email != self.contact_email:
            contact_info += f"\n- Privacy/Compliance: {self.compliance_email}"
        
        if self.data_protection_officer:
            contact_info += f"\n- Data Protection Officer: {self.data_protection_officer}"
        
        contact_info += f"\n- Website: {self.website_url}"
        
        if self.physical_address:
            contact_info += f"\n- Mailing Address: {self.physical_address}"
        
        contact_info += f"""

## Document Information

- Version: {self.version}
- Last Updated: {self.current_date}
- Effective Date: {self.effective_date}

---

*This document was generated by MokoStandards Legal Document Generator*
"""
        
        base_privacy += contact_info
        
        return self._markdown_to_html(base_privacy, f"{self.website_name} - Privacy Policy")


# Flask app
app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Legal Document Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 400px 1fr;
            gap: 20px;
            min-height: calc(100vh - 40px);
        }
        
        .form-panel {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            height: fit-content;
            position: sticky;
            top: 20px;
        }
        
        .preview-panel {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            display: flex;
            flex-direction: column;
        }
        
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 28px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 25px;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
            font-size: 14px;
        }
        
        input[type="text"],
        input[type="email"],
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus,
        input[type="email"]:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .radio-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        
        .radio-option {
            display: flex;
            align-items: center;
            gap: 6px;
        }
        
        .radio-option input[type="radio"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        
        .radio-option label {
            margin: 0;
            cursor: pointer;
            font-weight: normal;
        }
        
        .checkbox-label {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            font-weight: normal;
        }
        
        .checkbox-label input[type="checkbox"] {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        
        .checkbox-label span {
            font-weight: normal;
        }
        
        .button-group {
            display: flex;
            gap: 10px;
            margin-top: 25px;
        }
        
        button {
            flex: 1;
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-secondary {
            background: #f0f0f0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #e0e0e0;
        }
        
        .preview-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .preview-title {
            color: #333;
            font-size: 20px;
            font-weight: 600;
        }
        
        .download-btn {
            padding: 10px 20px;
            background: #28a745;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .download-btn:hover {
            background: #218838;
            transform: translateY(-2px);
        }
        
        .preview-content {
            flex: 1;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }
        
        #preview-frame {
            width: 100%;
            height: 100%;
            border: none;
            min-height: 600px;
        }
        
        .disclaimer {
            margin-top: 20px;
            padding: 15px;
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            border-radius: 4px;
            font-size: 12px;
            color: #856404;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        
        @media (max-width: 1024px) {
            .container {
                grid-template-columns: 1fr;
            }
            
            .form-panel {
                position: static;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="form-panel">
            <h1>Legal Document Generator</h1>
            <p class="subtitle">Create professional Terms of Service and Privacy Policy documents</p>
            
            <form id="generator-form">
                <div class="form-group">
                    <label for="website-type">Website Type *</label>
                    <select id="website-type" name="website_type" required>
                        <option value="plain">Plain Website (Informational)</option>
                        <option value="membership">Membership Website</option>
                        <option value="ecommerce">E-commerce Website</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="company-name">Company/Business Name *</label>
                    <input type="text" id="company-name" name="company_name" value="Your Company" required>
                </div>
                
                <div class="form-group">
                    <label for="website-name">Website Name</label>
                    <input type="text" id="website-name" name="website_name" value="" placeholder="Leave blank to use company name">
                </div>
                
                <div class="form-group">
                    <label for="website-url">Website URL *</label>
                    <input type="text" id="website-url" name="website_url" value="https://yourwebsite.com" required>
                </div>
                
                <div class="form-group">
                    <label for="contact-email">General Contact Email *</label>
                    <input type="email" id="contact-email" name="contact_email" value="contact@yourcompany.com" required>
                </div>
                
                <div class="form-group">
                    <label for="business-contact">Business Contact Email</label>
                    <input type="email" id="business-contact" name="business_contact" value="" placeholder="Leave blank to use general contact">
                </div>
                
                <div class="form-group">
                    <label for="compliance-email">Compliance/Legal Contact Email</label>
                    <input type="email" id="compliance-email" name="compliance_email" value="" placeholder="Leave blank to use general contact">
                </div>
                
                <div class="form-group">
                    <label for="physical-address">Physical Address (Optional)</label>
                    <input type="text" id="physical-address" name="physical_address" value="" placeholder="123 Main St, City, State, ZIP">
                </div>
                
                <div class="form-group">
                    <label for="country">Country/Jurisdiction (Optional)</label>
                    <input type="text" id="country" name="country" value="" placeholder="e.g., United States, European Union">
                </div>
                
                <div class="form-group">
                    <label for="industry">Industry (Optional)</label>
                    <select id="industry" name="industry">
                        <option value="">-- Select Industry --</option>
                        <option value="Technology">Technology</option>
                        <option value="Healthcare">Healthcare</option>
                        <option value="Finance">Finance</option>
                        <option value="E-commerce">E-commerce</option>
                        <option value="Education">Education</option>
                        <option value="Entertainment">Entertainment</option>
                        <option value="Real Estate">Real Estate</option>
                        <option value="Manufacturing">Manufacturing</option>
                        <option value="Retail">Retail</option>
                        <option value="Professional Services">Professional Services</option>
                        <option value="Other">Other</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="dpo-email">Data Protection Officer Email (Optional)</label>
                    <input type="email" id="dpo-email" name="dpo_email" value="" placeholder="dpo@yourcompany.com">
                </div>
                
                <div class="form-group">
                    <label for="effective-date">Effective Date (Optional)</label>
                    <input type="date" id="effective-date" name="effective_date" value="">
                </div>
                
                <div class="form-group">
                    <label for="version">Document Version</label>
                    <input type="text" id="version" name="version" value="1.0" placeholder="1.0">
                </div>
                
                <div class="form-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="gdpr" name="gdpr_compliant" value="true">
                        <span>GDPR Compliant (EU Users)</span>
                    </label>
                </div>
                
                <div class="form-group">
                    <label class="checkbox-label">
                        <input type="checkbox" id="ccpa" name="ccpa_compliant" value="true">
                        <span>CCPA Compliant (California Users)</span>
                    </label>
                </div>
                
                <div class="form-group">
                    <label>Document Type *</label>
                    <div class="radio-group">
                        <div class="radio-option">
                            <input type="radio" id="doc-tos" name="doc_type" value="tos">
                            <label for="doc-tos">Terms of Service</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" id="doc-privacy" name="doc_type" value="privacy">
                            <label for="doc-privacy">Privacy Policy</label>
                        </div>
                        <div class="radio-option">
                            <input type="radio" id="doc-both" name="doc_type" value="both" checked>
                            <label for="doc-both">Both</label>
                        </div>
                    </div>
                </div>
                
                <div class="button-group">
                    <button type="submit" class="btn-primary">Generate Preview</button>
                </div>
            </form>
            
            <div class="disclaimer">
                <strong>⚠️ Important:</strong> These generated documents are templates and should be reviewed by a qualified attorney before use. Customize them to fit your specific business needs and comply with applicable laws in your jurisdiction.
            </div>
        </div>
        
        <div class="preview-panel">
            <div class="preview-header">
                <div class="preview-title">Document Preview</div>
                <button class="download-btn" id="download-btn" style="display:none;">Download HTML</button>
            </div>
            <div class="loading" id="loading">Generating document...</div>
            <div class="preview-content">
                <iframe id="preview-frame" srcdoc="<div style='padding:40px; text-align:center; color:#999; font-family:sans-serif;'><h2>Welcome to Legal Document Generator</h2><p>Fill in the form on the left and click 'Generate Preview' to see your document here.</p></div>"></iframe>
            </div>
        </div>
    </div>
    
    <script>
        let currentHTML = '';
        let currentDocType = 'both';
        
        document.getElementById('generator-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            currentDocType = data.doc_type;
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('preview-frame').style.display = 'none';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    currentHTML = result.html;
                    const iframe = document.getElementById('preview-frame');
                    iframe.srcdoc = result.html;
                    iframe.style.display = 'block';
                    document.getElementById('download-btn').style.display = 'block';
                } else {
                    alert('Error: ' + result.error);
                }
            } catch (error) {
                alert('Error generating document: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        document.getElementById('download-btn').addEventListener('click', () => {
            if (currentHTML) {
                const companyName = document.getElementById('company-name').value.replace(/[^a-z0-9]/gi, '_');
                let filename;
                
                if (currentDocType === 'tos') {
                    filename = `${companyName}_TERMS_OF_SERVICE.html`;
                } else if (currentDocType === 'privacy') {
                    filename = `${companyName}_PRIVACY_POLICY.html`;
                } else {
                    filename = `${companyName}_LEGAL_DOCUMENTS.html`;
                }
                
                const blob = new Blob([currentHTML], { type: 'text/html' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            }
        });
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Render the main interface"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/generate', methods=['POST'])
def generate():
    """Generate legal documents based on form input"""
    try:
        data = request.json
        
        website_type = data.get('website_type', 'plain')
        company_name = data.get('company_name', 'Your Company')
        website_name = data.get('website_name', '') or None
        website_url = data.get('website_url', 'https://yourwebsite.com')
        contact_email = data.get('contact_email', 'contact@yourcompany.com')
        business_contact = data.get('business_contact', '') or None
        compliance_email = data.get('compliance_email', '') or None
        physical_address = data.get('physical_address', '') or None
        country = data.get('country', '') or None
        industry = data.get('industry', '') or None
        dpo_email = data.get('dpo_email', '') or None
        effective_date = data.get('effective_date', '') or None
        version = data.get('version', '1.0')
        gdpr_compliant = data.get('gdpr_compliant') == 'true' or data.get('gdpr_compliant') == True
        ccpa_compliant = data.get('ccpa_compliant') == 'true' or data.get('ccpa_compliant') == True
        doc_type = data.get('doc_type', 'both')
        
        # Format effective date if provided
        if effective_date:
            try:
                from datetime import datetime as dt
                date_obj = dt.strptime(effective_date, '%Y-%m-%d')
                effective_date = date_obj.strftime("%B %d, %Y")
            except:
                effective_date = None
        
        generator = LegalDocGenerator(
            website_type=website_type,
            company_name=company_name,
            website_name=website_name,
            website_url=website_url,
            contact_email=contact_email,
            business_contact=business_contact,
            compliance_email=compliance_email,
            physical_address=physical_address,
            country=country,
            industry=industry,
            data_protection_officer=dpo_email,
            gdpr_compliant=gdpr_compliant,
            ccpa_compliant=ccpa_compliant,
            effective_date=effective_date,
            version=version
        )
        
        if doc_type == 'tos':
            html = generator.generate_terms_of_service()
        elif doc_type == 'privacy':
            html = generator.generate_privacy_policy()
        else:  # both
            tos_html = generator.generate_terms_of_service()
            privacy_html = generator.generate_privacy_policy()
            # Combine both documents
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_module.escape(company_name)} - Legal Documents</title>
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
        .document-separator {{
            margin: 60px 0;
            border-top: 3px solid #667eea;
        }}
    </style>
</head>
<body>
{tos_html[tos_html.find('<body>') + 6:tos_html.find('</body>')]}
<div class="document-separator"></div>
{privacy_html[privacy_html.find('<body>') + 6:privacy_html.find('</body>')]}
</body>
</html>"""
        
        return jsonify({'success': True, 'html': html})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Web interface for Legal Document Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=5000,
        help='Port to run the web server on (default: 5000)'
    )
    
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='Host to bind the web server to (default: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Run in debug mode'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("LEGAL DOCUMENT GENERATOR - WEB INTERFACE")
    print("=" * 80)
    print(f"Starting web server on http://{args.host}:{args.port}")
    print("\nOpen your browser and navigate to the URL above to use the generator.")
    print("Press Ctrl+C to stop the server.")
    print("=" * 80)
    
    try:
        app.run(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        return 0
    except Exception as e:
        print(f"\nError starting server: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
