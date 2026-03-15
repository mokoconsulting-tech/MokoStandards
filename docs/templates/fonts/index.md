<!--
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
 along with this program. If not, see <https://www.gnu.org/licenses/>.

 # FILE INFORMATION
 DEFGROUP: MokoStandards.Templates.Fonts
 INGROUP: MokoStandards
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/templates/fonts/index.md
 VERSION: 04.00.15
 BRIEF: Catalogue of locally bundled font assets in templates/fonts/ and Google Fonts usage guidance
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.06-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Templates: Font Assets

## Overview

The `templates/fonts/` directory holds locally bundled typeface files that may be distributed
as part of governed repository templates. For runtime web use, **Google Fonts is the approved
delivery mechanism** — see the [Google Fonts Policy](../../policy/google-fonts.md) for full
requirements.

## Directory Structure

```
templates/fonts/
├── osaka-re.ttf                           # Osaka Re — stylized logo font (TrueType)
└── Google/                                # Open Sans — offline/print/native fallback (TrueType)
    ├── Open Sans-300.ttf                  # Weight 300, Regular
    ├── Open Sans-300italic.ttf            # Weight 300, Italic
    ├── Open Sans-500.ttf                  # Weight 500, Regular
    ├── Open Sans-500italic.ttf            # Weight 500, Italic
    ├── Open Sans-600.ttf                  # Weight 600, Regular
    ├── Open Sans-600italic.ttf            # Weight 600, Italic
    ├── Open Sans-700.ttf                  # Weight 700, Regular
    ├── Open Sans-700italic.ttf            # Weight 700, Italic
    ├── Open Sans-800.ttf                  # Weight 800, Regular
    ├── Open Sans-800italic.ttf            # Weight 800, Italic
    ├── Open Sans-Italic.ttf               # Weight 400, Italic
    ├── Open Sans-Regular.ttf              # Weight 400, Regular
    ├── OpenSans-Bold.ttf                  # Weight 700, Regular (named variant)
    ├── OpenSans-BoldItalic.ttf            # Weight 700, Italic (named variant)
    ├── OpenSans-ExtraBold.ttf             # Weight 800, Regular (named variant)
    ├── OpenSans-ExtraBoldItalic.ttf       # Weight 800, Italic (named variant)
    ├── OpenSans-Italic.ttf                # Weight 400, Italic (full subset)
    ├── OpenSans-ItalicVariable.ttf        # Variable weight, Italic
    ├── OpenSans-Light.ttf                 # Weight 300, Regular (named variant)
    ├── OpenSans-LightItalic.ttf           # Weight 300, Italic (named variant)
    ├── OpenSans-Medium.ttf                # Weight 500, Regular (named variant)
    ├── OpenSans-MediumItalic.ttf          # Weight 500, Italic (named variant)
    ├── OpenSans-Regular.ttf               # Weight 400, Regular (full subset)
    ├── OpenSans-RegularVariable.ttf       # Variable weight, Regular
    ├── OpenSans-SemiBold.ttf              # Weight 600, Regular (named variant)
    └── OpenSans-SemiBoldItalic.ttf        # Weight 600, Italic (named variant)
```

## Asset Reference

### Bundled Fonts

| File | Format | Family | Style | Weight | Size | Classification |
|---|---|---|---|---|---|---|
| `osaka-re.ttf` | TrueType (TTF) | Osaka Re | Regular | 400 | 12 KB | **Stylized Logo Font** |

#### osaka-re.ttf

**Osaka Re** is the **official stylized logo font** for Moko Consulting. It is used exclusively
for the brand wordmark, logo lockups, and stylized display contexts (e.g., splash screens,
printed brand collateral). It is **not** used for body text or UI labels — use
**Open Sans** (via Google Fonts) for those purposes.

**Usage:**

```css
@font-face {
    font-family: 'Osaka Re';
    src: url('/fonts/osaka-re.ttf') format('truetype');
    font-weight: 400;
    font-style: normal;
    font-display: swap;
}
```

**License note:** Confirm the license for `osaka-re.ttf` before distributing in client
deliverables. Bundled font files are only for internal tooling unless the licence permits
redistribution.

---

### Google/  — Open Sans Offline Collection

The `Google/` subdirectory holds a complete offline copy of the **Open Sans** typeface family.
These files are provided as a fallback for **offline, print, and native-app** contexts where
the Google Fonts CDN is unavailable. **Web projects must still use the CDN** — see the
[Google Fonts Policy](../../policy/google-fonts.md).

**Total: 26 files (~5.0 MB)**

#### Numbered-weight naming (`Open Sans-{weight}[italic].ttf`)

| File | Format | Family | Style | Weight | Size |
|---|---|---|---|---|---|
| `Open Sans-300.ttf` | TrueType (TTF) | Open Sans | Regular | 300 | 128 KB |
| `Open Sans-300italic.ttf` | TrueType (TTF) | Open Sans | Italic | 300 | 134 KB |
| `Open Sans-500.ttf` | TrueType (TTF) | Open Sans | Regular | 500 | 128 KB |
| `Open Sans-500italic.ttf` | TrueType (TTF) | Open Sans | Italic | 500 | 134 KB |
| `Open Sans-600.ttf` | TrueType (TTF) | Open Sans | Regular | 600 | 128 KB |
| `Open Sans-600italic.ttf` | TrueType (TTF) | Open Sans | Italic | 600 | 134 KB |
| `Open Sans-700.ttf` | TrueType (TTF) | Open Sans | Regular | 700 | 128 KB |
| `Open Sans-700italic.ttf` | TrueType (TTF) | Open Sans | Italic | 700 | 133 KB |
| `Open Sans-800.ttf` | TrueType (TTF) | Open Sans | Regular | 800 | 128 KB |
| `Open Sans-800italic.ttf` | TrueType (TTF) | Open Sans | Italic | 800 | 134 KB |
| `Open Sans-Italic.ttf` | TrueType (TTF) | Open Sans | Italic | 400 | 134 KB |
| `Open Sans-Regular.ttf` | TrueType (TTF) | Open Sans | Regular | 400 | 128 KB |

#### Named-weight naming (`OpenSans-{Name}[Italic].ttf`)

| File | Format | Family | Style | Weight | Size |
|---|---|---|---|---|---|
| `OpenSans-Bold.ttf` | TrueType (TTF) | Open Sans | Regular | 700 | 128 KB |
| `OpenSans-BoldItalic.ttf` | TrueType (TTF) | Open Sans | Italic | 700 | 133 KB |
| `OpenSans-ExtraBold.ttf` | TrueType (TTF) | Open Sans | Regular | 800 | 128 KB |
| `OpenSans-ExtraBoldItalic.ttf` | TrueType (TTF) | Open Sans | Italic | 800 | 134 KB |
| `OpenSans-Italic.ttf` | TrueType (TTF) | Open Sans | Italic | 400 | 567 KB |
| `OpenSans-Light.ttf` | TrueType (TTF) | Open Sans | Regular | 300 | 128 KB |
| `OpenSans-LightItalic.ttf` | TrueType (TTF) | Open Sans | Italic | 300 | 134 KB |
| `OpenSans-Medium.ttf` | TrueType (TTF) | Open Sans | Regular | 500 | 128 KB |
| `OpenSans-MediumItalic.ttf` | TrueType (TTF) | Open Sans | Italic | 500 | 134 KB |
| `OpenSans-Regular.ttf` | TrueType (TTF) | Open Sans | Regular | 400 | 517 KB |
| `OpenSans-SemiBold.ttf` | TrueType (TTF) | Open Sans | Regular | 600 | 128 KB |
| `OpenSans-SemiBoldItalic.ttf` | TrueType (TTF) | Open Sans | Italic | 600 | 134 KB |

#### Variable fonts

| File | Format | Family | Style | Weight | Size |
|---|---|---|---|---|---|
| `OpenSans-RegularVariable.ttf` | TrueType (TTF) | Open Sans | Regular | Variable (300–800) | 517 KB |
| `OpenSans-ItalicVariable.ttf` | TrueType (TTF) | Open Sans | Italic | Variable (300–800) | 567 KB |

> **Note on file sizes:** The `OpenSans-Regular.ttf`, `OpenSans-Italic.ttf`,
> `OpenSans-RegularVariable.ttf`, and `OpenSans-ItalicVariable.ttf` files are significantly
> larger (~517–567 KB) because they contain full Unicode coverage or variable-font axis data.
> The numbered/named single-weight files (~128–134 KB each) contain only the Latin character
> subset.

## Web Font Strategy

For all **web-facing** projects, fonts must be loaded via Google Fonts rather than
self-hosted files. The official body text font is **Open Sans** (400, 600, 700).
See the [Google Fonts Policy](../../policy/google-fonts.md) for:

- Approved font families and approved weights
- Required `<link>` preconnect and stylesheet tags
- `font-display: swap` requirement
- Privacy and GDPR considerations

## Governance

- Locally bundled fonts in `templates/fonts/` are supplemental for **offline / print / native**
  use cases only.
- Web projects must use the Google Fonts CDN unless a documented exception has been approved.
- New font files must be reviewed for licence compatibility before being added to this directory.
- Font updates must be submitted via PR to this repository.

## Related

- [Branding Policy](../../policy/branding.md)
- [Google Fonts Policy](../../policy/google-fonts.md)
- [Templates Catalog](../index.md)
- [Image Assets](../images/index.md)
- [Network Egress Policy](../../policy/network-egress.md) (approves `fonts.googleapis.com` + `fonts.gstatic.com`)

## Revision History

| Date       | Author         | Change                         | Notes                                                    |
| ---------- | -------------- | ------------------------------ | -------------------------------------------------------- |
| 2026-03-10 | GitHub Copilot | Initial catalogue created      | Scanned templates/fonts/ assets                          |
| 2026-03-10 | GitHub Copilot | Full font inventory documented | Added Google/ Open Sans collection (26 files, ~5.0 MB)   |
