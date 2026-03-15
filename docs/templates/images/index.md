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
 DEFGROUP: MokoStandards.Templates.Images
 INGROUP: MokoStandards
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/templates/images/index.md
 VERSION: 04.00.15
 BRIEF: Catalogue of all image assets in templates/images/ and their usage guidance
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.15-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Templates: Image Assets

## Overview

The `templates/images/` directory is the canonical source of branding, favicon, and background
image assets for all Moko Consulting governed repositories. Assets are organised into sub-collections
by brand tier. The **primary** collection contains the current production brand set.

## Directory Structure

```
templates/images/
└── primary/                 # Current production brand set
    ├── logo.png             # Primary logo (colour, raster)
    ├── logo.svg             # Primary logo (colour, vector)
    ├── logo_tiger.png       # Tiger-head logo variant (raster)
    ├── tigerhead_3.svg      # Tiger-head illustration (vector)
    ├── background.png       # Full-width background image (raster)
    ├── background.svg       # Full-width background image (vector)
    ├── favicon_256.png      # ★ Canonical favicon – 256 × 256 px (sync template)
    ├── favicon_120.png      # Favicon – 120 × 120 px
    ├── favicon-96x96.png    # Favicon – 96 × 96 px
    ├── favicon.svg          # Favicon (vector source)
    ├── favicon.gif          # Animated favicon (legacy)
    ├── favicon.ico          # ICO bundle (legacy browsers)
    ├── apple-touch-icon.png # iOS home-screen icon – 180 × 180 px
    ├── web-app-manifest-192x192.png  # PWA manifest icon – 192 × 192 px
    └── web-app-manifest-512x512.png  # PWA manifest icon – 512 × 512 px
```

## Asset Reference

### Logos

| File | Format | Use Case |
|---|---|---|
| `primary/logo.png` | PNG (raster) | README headers, documentation, HTML `<img>` |
| `primary/logo.svg` | SVG (vector) | Web pages, print, scalable contexts |
| `primary/logo_tiger.png` | PNG (raster) | Alternate brand contexts using the tiger-head motif |
| `primary/tigerhead_3.svg` | SVG (vector) | Decorative tiger-head illustration, scalable contexts |

The `logo.png` file is the **canonical README logo** for all governed repositories. The
MokoStandards repository `README.md` references it at `templates/images/primary/logo.png`.

### Backgrounds

| File | Format | Use Case |
|---|---|---|
| `primary/background.png` | PNG (raster) | Web hero sections, slide decks |
| `primary/background.svg` | SVG (vector) | Web hero sections where vector scaling is required |

### Favicons

| File | Format | Size | Use Case |
|---|---|---|---|
| `primary/favicon_256.png` | PNG | 256 × 256 | **Sync template** – synced to Dolibarr module `img/` directories as `object_favicon_256.png` (module picto) |
| `primary/favicon_120.png` | PNG | 120 × 120 | General favicon use |
| `primary/favicon-96x96.png` | PNG | 96 × 96 | General favicon use |
| `primary/favicon.svg` | SVG | Vector | Modern browsers (preferred source) |
| `primary/favicon.gif` | GIF | Variable | Animated favicon (legacy use only) |
| `primary/favicon.ico` | ICO | Multi-size bundle | Legacy browser support |

#### Sync Template — favicon_256.png → object_favicon_256.png

`templates/images/primary/favicon_256.png` is the **canonical favicon sync template** used
by the bulk sync system. It is declared in `api/definitions/default/crm-module.tf` and is
deployed to `img/object_favicon_256.png` in every Dolibarr (MokoCRM) module repository.
The `object_` prefix follows Dolibarr's icon naming convention for module pictos.

```hcl
file {
  name               = "object_favicon_256.png"
  template           = "templates/images/primary/favicon_256.png"
  requirement_status = "required"
  always_overwrite   = true
}
```

### PWA / App Icons

| File | Format | Size | Use Case |
|---|---|---|---|
| `primary/apple-touch-icon.png` | PNG | 180 × 180 | iOS Safari home-screen shortcut |
| `primary/web-app-manifest-192x192.png` | PNG | 192 × 192 | PWA `manifest.json` `icons[]` entry |
| `primary/web-app-manifest-512x512.png` | PNG | 512 × 512 | PWA `manifest.json` `icons[]` entry (splash) |

## Usage Guidelines

### Using the Logo in a Repository README

Reference the asset with a repo-relative path so the logo renders correctly on GitHub, in
local checkouts, and in forks — without depending on any external URL:

```markdown
![Moko Consulting](templates/images/primary/logo.png)
```

### Using the Favicon in a Web Project

Copy the favicon set from `templates/images/primary/` into your project's public assets
directory and reference them in `<head>`:

```html
<link rel="icon" type="image/png" sizes="256x256" href="/img/favicon_256.png">
<link rel="icon" type="image/png" sizes="96x96"   href="/img/favicon-96x96.png">
<link rel="icon" type="image/svg+xml"              href="/img/favicon.svg">
<link rel="apple-touch-icon"                       href="/img/apple-touch-icon.png">
```

### Adding an App Manifest (PWA)

```json
{
  "icons": [
    { "src": "/img/web-app-manifest-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/img/web-app-manifest-512x512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

## Governance

- All image assets are copyright Moko Consulting and licensed under GPL-3.0-or-later.
- Do **not** modify brand assets (logo, tigerhead) without approval from the design lead.
- The `primary/` collection is the single source of truth; do **not** duplicate these files
  inside individual repositories outside of the sync-managed `img/` directory.
- Asset updates must be submitted via PR to this repository; the bulk sync workflow will
  propagate changes to all governed repositories on the next sync run.

## Related

- [Branding Policy](../../policy/branding.md)
- [Templates Catalog](../index.md)
- [Font Assets](../fonts/index.md)
- [crm-module.tf definition](../../../api/definitions/default/crm-module.tf)
- [Google Fonts Policy](../../policy/google-fonts.md)

## Revision History

| Date       | Author         | Change                    | Notes                                    |
| ---------- | -------------- | ------------------------- | ---------------------------------------- |
| 2026-03-10 | GitHub Copilot | Initial catalogue created | Scanned templates/images/primary/ assets |
