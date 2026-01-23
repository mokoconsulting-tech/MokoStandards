# Legal Document Generator - Web Interface

## Overview

The Legal Document Generator Web Interface provides a browser-based UI for creating Terms of Service and Privacy Policy documents. Users can configure all options through an intuitive form and preview the generated HTML directly in their browser.

## Features

- **Interactive Web Interface**: Modern, responsive web UI
- **Real-time Preview**: See generated documents instantly in the browser
- **Download Capability**: Download generated HTML files directly
- **Three Website Types**: Support for membership, plain, and ecommerce websites
- **Customizable Options**: Company name, website URL, contact email
- **Professional Styling**: Generated documents include responsive CSS

## Installation

### Prerequisites

- Python 3.7 or higher
- Flask web framework

### Install Dependencies

```bash
pip install flask
```

## Usage

### Starting the Web Server

Basic usage (runs on http://127.0.0.1:5000):
```bash
python scripts/legal_doc_generator_web.py
```

Custom port:
```bash
python scripts/legal_doc_generator_web.py --port 8080
```

Make accessible from network:
```bash
python scripts/legal_doc_generator_web.py --host 0.0.0.0 --port 8080
```

Debug mode:
```bash
python scripts/legal_doc_generator_web.py --debug
```

### Using the Interface

1. **Start the server** using one of the commands above
2. **Open your browser** and navigate to the displayed URL (e.g., http://127.0.0.1:5000)
3. **Fill in the form**:
   - Select your website type (Plain, Membership, or E-commerce)
   - Enter your company name
   - Enter your website URL
   - Enter your contact email
   - Choose which document(s) to generate
4. **Click "Generate Preview"** to see the document in the preview pane
5. **Click "Download HTML"** to save the generated document

## Form Options

### Website Type
- **Plain Website**: For informational websites with basic analytics and contact forms
- **Membership Website**: Includes terms for user accounts, membership fees, and user-generated content
- **E-commerce Website**: Includes terms for online sales, payments, shipping, and returns

### Document Type
- **Terms of Service**: Generate only the Terms of Service document
- **Privacy Policy**: Generate only the Privacy Policy document
- **Both**: Generate a combined document with both policies

## Features

### Live Preview
The preview pane shows exactly how your document will look, with professional styling applied.

### Instant Download
Click the download button to save the generated HTML file with an appropriate filename based on your company name.

### Responsive Design
The web interface works on desktop, tablet, and mobile devices.

## Security

- All user input is sanitized using HTML escaping
- XSS vulnerabilities are prevented
- No data is stored on the server
- Documents are generated on-demand

## Troubleshooting

### Flask Not Found
If you see "Flask is required for the web interface":
```bash
pip install flask
```

### Port Already in Use
If port 5000 is already in use, specify a different port:
```bash
python scripts/legal_doc_generator_web.py --port 8080
```

### Cannot Access from Other Devices
To make the server accessible from other devices on your network:
```bash
python scripts/legal_doc_generator_web.py --host 0.0.0.0
```

## Command Line Alternative

If you prefer command-line usage, the original CLI versions are still available:

**Python:**
```bash
python scripts/legal_doc_generator.py --type membership --company-name "Acme Inc"
```

**PHP:**
```bash
php scripts/legal_doc_generator.php --type membership --company-name "Acme Inc"
```

## Disclaimer

⚠️ **Important:** These generated documents are templates and should be reviewed by a qualified attorney before use. Customize them to fit your specific business needs and comply with applicable laws in your jurisdiction.

## License

Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
