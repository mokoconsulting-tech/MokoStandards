<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Templates.Assets
INGROUP: MokoStandards.Templates
REPO: https://github.com/mokoconsulting-tech/MokoStandards
FILE: templates/assets/README.md
VERSION: 01.00.00
BRIEF: Assets directory documentation for template resources
PATH: /templates/assets/README.md
-->

# Template Assets

This directory contains static assets used by templates in the MokoStandards repository.

## Contents

### Favicon

**favicon.svg** - Moko Consulting favicon in SVG format
- Modern, scalable vector format
- Works across all modern browsers
- Displays "MC" (Moko Consulting) initials on branded purple background (#667eea)
- Size: 32x32 viewport
- Rounded corners (6px radius)

## Usage

### In HTML Templates

Add to the `<head>` section of HTML files:

```html
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
```

### For Relative Paths

Adjust the path based on your file location:

```html
<!-- Same directory as HTML file -->
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">

<!-- One level up from HTML file -->
<link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">

<!-- Two levels up from HTML file -->
<link rel="icon" type="image/svg+xml" href="../../assets/favicon.svg">
```

### Browser Support

SVG favicons are supported by:
- Chrome 80+
- Firefox 41+
- Safari 9+
- Edge 79+
- Opera 67+

For older browsers, a fallback ICO file can be added if needed.

## Customization

To customize the favicon:

1. Edit `favicon.svg` with any text editor or SVG editor
2. Modify the fill color (`#667eea`) to match your branding
3. Change the text content ("MC") if needed
4. Adjust font size or positioning as desired

## License

All assets in this directory are licensed under GPL-3.0-or-later.

See [LICENSE](../../LICENSE) for full license text.
