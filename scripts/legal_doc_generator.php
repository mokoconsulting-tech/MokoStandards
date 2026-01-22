#!/usr/bin/env php
<?php
/**
 * Legal Document Generator
 *
 * Generates Terms of Service and Privacy Policy documents for different types of websites.
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program (./LICENSE).
 *
 * FILE INFORMATION
 * DEFGROUP: Scripts.Generators
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /scripts/legal_doc_generator.php
 * VERSION: 01.00.00
 * BRIEF: Generate Terms of Service and Privacy Policy templates for websites
 * USAGE: php legal_doc_generator.php --type <website_type> [options]
 *
 * ARGUMENTS
 *     --type: Type of website (membership, plain, ecommerce)
 *     --output-dir: Directory to save generated documents (default: current directory)
 *     --company-name: Company name (default: "Your Company")
 *     --website-url: Website URL (default: "https://yourwebsite.com")
 *     --contact-email: Contact email (default: "contact@yourcompany.com")
 *     --docs: Generate only one type of document (tos, privacy, or both if not specified)
 *
 * EXAMPLES
 *     # Generate both documents for a membership website
 *     php legal_doc_generator.php --type membership --company-name "Acme Inc" \
 *         --website-url "https://acme.com" --contact-email "legal@acme.com"
 *
 *     # Generate only Terms of Service for an ecommerce site
 *     php legal_doc_generator.php --type ecommerce --docs tos --output-dir ./legal
 *
 *     # Generate Privacy Policy for a plain website
 *     php legal_doc_generator.php --type plain --docs privacy
 */

/**
 * Legal Document Generator Class
 */
class LegalDocGenerator
{
    private string $websiteType;
    private string $companyName;
    private string $websiteUrl;
    private string $contactEmail;
    private string $currentDate;

    /**
     * Initialize legal document generator
     *
     * @param string $websiteType Type of website (membership, plain, ecommerce)
     * @param string $companyName Name of the company
     * @param string $websiteUrl URL of the website
     * @param string $contactEmail Contact email address
     * @throws InvalidArgumentException if website type is invalid
     */
    public function __construct(
        string $websiteType,
        string $companyName,
        string $websiteUrl,
        string $contactEmail
    ) {
        $this->websiteType = strtolower($websiteType);
        $this->companyName = $companyName;
        $this->websiteUrl = $websiteUrl;
        $this->contactEmail = $contactEmail;
        $this->currentDate = date('F d, Y');

        // Validate website type
        if (!in_array($this->websiteType, ['membership', 'plain', 'ecommerce'])) {
            throw new InvalidArgumentException(
                "Invalid website type: $websiteType. Must be 'membership', 'plain', or 'ecommerce'"
            );
        }
    }

    /**
     * Convert markdown text to HTML
     *
     * @param string $markdownText Markdown formatted text
     * @param string $title Document title for HTML head
     * @return string HTML formatted text
     */
    private function markdownToHtml(string $markdownText, string $title): string
    {
        $html = "<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>" . htmlspecialchars($title) . "</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            margin-top: 30px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }
        h3 {
            color: #555;
            margin-top: 20px;
        }
        strong {
            color: #2c3e50;
        }
        ul {
            margin: 10px 0;
            padding-left: 30px;
        }
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }
        .footer {
            margin-top: 40px;
            font-style: italic;
            color: #777;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
";

        $lines = explode("\n", $markdownText);
        $inList = false;

        foreach ($lines as $line) {
            // H1 heading
            if (strpos($line, '# ') === 0) {
                $html .= "    <h1>" . htmlspecialchars(substr($line, 2)) . "</h1>\n";
            }
            // H2 heading
            elseif (strpos($line, '## ') === 0) {
                if ($inList) {
                    $html .= "    </ul>\n";
                    $inList = false;
                }
                $html .= "    <h2>" . htmlspecialchars(substr($line, 3)) . "</h2>\n";
            }
            // H3 heading
            elseif (strpos($line, '### ') === 0) {
                if ($inList) {
                    $html .= "    </ul>\n";
                    $inList = false;
                }
                $html .= "    <h3>" . htmlspecialchars(substr($line, 4)) . "</h3>\n";
            }
            // Bold text
            elseif (strpos($line, '**') === 0 && strpos($line, '**', 2) !== false) {
                // Extract text between first and last **
                $text = substr($line, 2);
                if (substr($text, -2) === '**') {
                    $text = substr($text, 0, -2);
                }
                $html .= "    <p><strong>" . htmlspecialchars($text) . "</strong></p>\n";
            }
            // List item
            elseif (strpos($line, '- ') === 0) {
                if (!$inList) {
                    $html .= "    <ul>\n";
                    $inList = true;
                }
                $html .= "        <li>" . htmlspecialchars(substr($line, 2)) . "</li>\n";
            }
            // Horizontal rule
            elseif (trim($line) === '---') {
                if ($inList) {
                    $html .= "    </ul>\n";
                    $inList = false;
                }
                $html .= "    <hr>\n";
            }
            // Paragraph
            elseif (trim($line) !== '') {
                if ($inList) {
                    $html .= "    </ul>\n";
                    $inList = false;
                }
                $html .= "    <p>" . htmlspecialchars($line) . "</p>\n";
            }
            // Empty line
            else {
                if ($inList) {
                    $html .= "    </ul>\n";
                    $inList = false;
                }
            }
        }

        if ($inList) {
            $html .= "    </ul>\n";
        }

        $html .= "</body>
</html>";

        return $html;
    }

    /**
     * Generate Terms of Service document
     *
     * @return string Terms of Service content
     */
    public function generateTermsOfService(): string
    {
        $baseTos = "# Terms of Service

**Last Updated:** {$this->currentDate}

## 1. Acceptance of Terms

By accessing and using {$this->companyName}'s website ({$this->websiteUrl}), you accept and agree to be bound by the terms and provision of this agreement.

## 2. Use License

Permission is granted to temporarily access the materials on {$this->companyName}'s website for personal, non-commercial transitory viewing only.

## 3. Disclaimer

The materials on {$this->companyName}'s website are provided on an 'as is' basis. {$this->companyName} makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.

## 4. Limitations

In no event shall {$this->companyName} or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on {$this->companyName}'s website.

## 5. Accuracy of Materials

The materials appearing on {$this->companyName}'s website could include technical, typographical, or photographic errors. {$this->companyName} does not warrant that any of the materials on its website are accurate, complete or current.

## 6. Links

{$this->companyName} has not reviewed all of the sites linked to its website and is not responsible for the contents of any such linked site.

## 7. Modifications

{$this->companyName} may revise these terms of service for its website at any time without notice. By using this website you are agreeing to be bound by the then current version of these terms of service.

## 8. Governing Law

These terms and conditions are governed by and construed in accordance with the applicable laws and you irrevocably submit to the exclusive jurisdiction of the courts in that location.
";

        // Add website-type specific sections
        if ($this->websiteType === 'membership') {
            $baseTos .= "

## 9. Membership Terms

### 9.1 Account Registration
Users must register for an account to access membership features. You are responsible for maintaining the confidentiality of your account credentials.

### 9.2 Membership Fees
Certain features may require payment of membership fees. All fees are non-refundable unless otherwise stated.

### 9.3 Account Termination
{$this->companyName} reserves the right to terminate or suspend accounts that violate these terms of service.

### 9.4 User Content
Members may post content on the platform. You retain ownership of your content but grant {$this->companyName} a license to use, display, and distribute it.

### 9.5 Member Conduct
Members must not:
- Post inappropriate, offensive, or illegal content
- Harass or intimidate other members
- Attempt to gain unauthorized access to the platform
- Use the platform for commercial purposes without authorization
";
        } elseif ($this->websiteType === 'ecommerce') {
            $baseTos .= "

## 9. Ecommerce Terms

### 9.1 Product Information
{$this->companyName} attempts to be as accurate as possible. However, we do not warrant that product descriptions or other content is accurate, complete, reliable, current, or error-free.

### 9.2 Pricing
All prices are subject to change without notice. We reserve the right to modify or discontinue products without notice.

### 9.3 Orders and Payment
By placing an order, you agree to provide current, complete, and accurate purchase information. We reserve the right to refuse or cancel any order.

### 9.4 Shipping and Delivery
Shipping times are estimates and not guaranteed. {$this->companyName} is not responsible for delays caused by shipping carriers.

### 9.5 Returns and Refunds
Returns are accepted within 30 days of purchase. Items must be in original condition. Refunds will be processed within 10 business days.

### 9.6 Electronic Communications
When you place an order or send us emails, you consent to receiving electronic communications from us.
";
        }

        $baseTos .= "

## Contact Information

For questions about these Terms of Service, please contact us at:
- Email: {$this->contactEmail}
- Website: {$this->websiteUrl}

---

*This document was generated by MokoStandards Legal Document Generator*
";

        return $this->markdownToHtml($baseTos, "{$this->companyName} - Terms of Service");
    }

    /**
     * Generate Privacy Policy document
     *
     * @return string Privacy Policy content
     */
    public function generatePrivacyPolicy(): string
    {
        $basePrivacy = "# Privacy Policy

**Last Updated:** {$this->currentDate}

## 1. Introduction

{$this->companyName} (\"we\", \"our\", or \"us\") respects your privacy and is committed to protecting your personal data. This privacy policy explains how we collect, use, and protect your information when you visit {$this->websiteUrl}.

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
";

        // Add website-type specific sections
        if ($this->websiteType === 'membership') {
            $basePrivacy .= "

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
";
        } elseif ($this->websiteType === 'ecommerce') {
            $basePrivacy .= "

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
";
        } elseif ($this->websiteType === 'plain') {
            $basePrivacy .= "

## 10. Information Website Privacy Terms

### 10.1 Analytics
We use analytics tools to understand how visitors interact with our website and improve user experience.

### 10.2 Newsletter Subscriptions
If you subscribe to our newsletter, we collect your email address and name (if provided).

### 10.3 Contact Forms
Information submitted through contact forms is used solely to respond to your inquiry.
";
        }

        $basePrivacy .= "

## Contact Information

If you have any questions about this Privacy Policy, please contact us at:
- Email: {$this->contactEmail}
- Website: {$this->websiteUrl}

---

*This document was generated by MokoStandards Legal Document Generator*
";

        return $this->markdownToHtml($basePrivacy, "{$this->companyName} - Privacy Policy");
    }

    /**
     * Save document to file
     *
     * @param string $content Document content
     * @param string $filename Output filename
     * @param string $outputDir Output directory
     * @return string Path to saved file
     * @throws RuntimeException if file cannot be saved
     */
    public function saveDocument(string $content, string $filename, string $outputDir): string
    {
        // Create directory if it doesn't exist
        if (!is_dir($outputDir)) {
            if (!mkdir($outputDir, 0750, true) && !is_dir($outputDir)) {
                throw new RuntimeException("Failed to create directory: $outputDir");
            }
        }

        $filePath = rtrim($outputDir, '/') . '/' . $filename;

        if (file_put_contents($filePath, $content) === false) {
            throw new RuntimeException("Failed to save file: $filePath");
        }

        echo "✓ Generated: $filePath\n";
        return $filePath;
    }
}

/**
 * Display usage information
 */
function showUsage(): void
{
    echo <<<USAGE
Legal Document Generator

Usage:
    php legal_doc_generator.php --type <website_type> [options]

Options:
    --type <type>              Type of website (membership, plain, ecommerce) [REQUIRED]
    --output-dir <dir>         Directory to save generated documents (default: current directory)
    --company-name <name>      Company name (default: "Your Company")
    --website-url <url>        Website URL (default: "https://yourwebsite.com")
    --contact-email <email>    Contact email (default: "contact@yourcompany.com")
    --docs <type>              Type of document to generate: tos, privacy, or both (default: both)
    --help, -h                 Show this help message

Examples:
    # Generate both documents for a membership website
    php legal_doc_generator.php --type membership --company-name "Acme Inc" \\
        --website-url "https://acme.com" --contact-email "legal@acme.com"

    # Generate only Terms of Service for an ecommerce site
    php legal_doc_generator.php --type ecommerce --docs tos --output-dir ./legal

    # Generate Privacy Policy for a plain website
    php legal_doc_generator.php --type plain --docs privacy

USAGE;
}

/**
 * Parse command line arguments
 *
 * @param array $argv Command line arguments
 * @return array Parsed options
 */
function parseArguments(array $argv): array
{
    $options = [
        'type' => null,
        'output-dir' => '.',
        'company-name' => 'Your Company',
        'website-url' => 'https://yourwebsite.com',
        'contact-email' => 'contact@yourcompany.com',
        'docs' => 'both',
    ];

    for ($i = 1; $i < count($argv); $i++) {
        $arg = $argv[$i];

        if ($arg === '--help' || $arg === '-h') {
            showUsage();
            exit(0);
        }

        if (strpos($arg, '--') === 0) {
            $key = substr($arg, 2);
            // Check if there's a next argument and it's not another flag
            if (isset($argv[$i + 1]) && strpos($argv[$i + 1], '--') !== 0) {
                $options[$key] = $argv[$i + 1];
                $i++;
            } elseif (array_key_exists($key, $options)) {
                // Flag provided without value - leave default
                continue;
            }
        }
    }

    return $options;
}

/**
 * Main entry point
 */
function main(array $argv): int
{
    try {
        // Parse arguments
        $options = parseArguments($argv);

        // Check required arguments
        if ($options['type'] === null) {
            fwrite(STDERR, "Error: --type is required\n\n");
            showUsage();
            return 1;
        }

        // Validate docs option
        if (!in_array($options['docs'], ['tos', 'privacy', 'both'])) {
            fwrite(STDERR, "Error: --docs must be 'tos', 'privacy', or 'both'\n");
            return 1;
        }

        // Display header
        echo str_repeat('=', 80) . "\n";
        echo "LEGAL DOCUMENT GENERATOR\n";
        echo str_repeat('=', 80) . "\n";
        echo "Website Type: {$options['type']}\n";
        echo "Company Name: {$options['company-name']}\n";
        echo "Website URL: {$options['website-url']}\n";
        echo "Contact Email: {$options['contact-email']}\n";
        echo "Output Directory: {$options['output-dir']}\n";
        echo "Documents: {$options['docs']}\n";
        echo str_repeat('-', 80) . "\n";

        // Initialize generator
        $generator = new LegalDocGenerator(
            $options['type'],
            $options['company-name'],
            $options['website-url'],
            $options['contact-email']
        );

        // Generate documents
        $generatedFiles = [];

        if ($options['docs'] === 'tos' || $options['docs'] === 'both') {
            $tosContent = $generator->generateTermsOfService();
            $tosFile = $generator->saveDocument($tosContent, 'TERMS_OF_SERVICE.html', $options['output-dir']);
            $generatedFiles[] = $tosFile;
        }

        if ($options['docs'] === 'privacy' || $options['docs'] === 'both') {
            $privacyContent = $generator->generatePrivacyPolicy();
            $privacyFile = $generator->saveDocument($privacyContent, 'PRIVACY_POLICY.html', $options['output-dir']);
            $generatedFiles[] = $privacyFile;
        }

        // Print summary
        echo str_repeat('-', 80) . "\n";
        echo "✅ Document generation complete!\n\n";
        echo "Generated " . count($generatedFiles) . " document(s):\n";
        foreach ($generatedFiles as $file) {
            echo "  📄 $file\n";
        }

        echo "\n⚠️  IMPORTANT NOTICE:\n";
        echo "These generated documents are templates and should be reviewed by a\n";
        echo "qualified attorney before use. Customize them to fit your specific\n";
        echo "business needs and comply with applicable laws in your jurisdiction.\n";

        return 0;
    } catch (Exception $e) {
        fwrite(STDERR, "\n✗ Error: " . $e->getMessage() . "\n");
        return 1;
    }
}

// Run the script
exit(main($argv));
