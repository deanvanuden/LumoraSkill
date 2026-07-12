# GitHub Pages Output Contract

## Default Architecture

For new Lumora sites, publish directly from the repository root on the selected branch. Keep the runtime static:

```text
index.html
styles.css
script.js
404.html
.nojekyll
lumora-plan.json
assets/
  images/
  video/
  fonts/
  models/
  textures/
```

This shape can be uploaded to GitHub and published from `/<root>` without an npm build. A custom domain can be connected later in repository Pages settings.

## URL Rules

- Use `./styles.css`, `./script.js`, and `./assets/...` from root pages.
- From nested directories, calculate relative paths correctly or keep route files at the root.
- Use `./about.html`, `./work.html`, and equivalent relative routes.
- Never use root-absolute project assets such as `/assets/hero.webp`; they fail on repository Pages paths.
- Preserve query strings and fragments only when the target exists.
- Match filename casing exactly. GitHub hosting is case-sensitive.
- Do not hardcode a repository name into URLs. Relative paths work before and after a custom domain is attached.

## Multipage Sites

Prefer root-level `.html` routes for simple static sites. Share the same CSS and JavaScript where practical, but allow page-specific files for genuinely different canvas, gallery, or product logic.

Navigation and footer links must resolve from every page. Build `404.html` with the same brand system and a working relative route back home.

### Existing-Site Route Migration

Before copying or generating runtime files, inventory every public source route and record it in `build_contract.source_route_inventory`. Store downloaded source HTML and assets in a sibling archive outside the publishing root, for example:

```text
project/
  source-archive/        # inspection only; never published
  site/                  # exact GitHub Pages root
    index.html
    about.html
    contact.html
    404.html
    lumora-plan.json
```

For every source route choose one disposition:

- `redesigned`: build the route in the new system
- `consolidated`: move its truthful content into another designed route and update all navigation
- `redirected`: ship a branded, accessible static redirect with a visible destination link
- `retired`: remove it for a recorded factual or user-approved reason

Do not leave scraped HTML, legacy CSS/JS, mojibake, or broken asset references in the publishing root. A redesigned homepage beside untouched old pages is not a completed redesign.

Complete `build_contract.route_manifest` after implementation. It must exactly match every `.html` file under the publish root, including legal and system pages. Each route records its purpose, status, shared design system, and terminal-headless-render verification result.

## Domains

Add a plain `CNAME` file only when the user supplies the exact domain. The file contains one hostname without protocol or path. The user must still configure and verify the domain in GitHub Pages settings and at their DNS provider.

Do not guess DNS records or commit a placeholder domain.

## Static Runtime

- Pin external CDN versions rather than using `latest`.
- Keep critical layout and content available if animation libraries fail.
- Avoid runtime dependencies on protected MotionSites URLs.
- Use local images, videos, fonts, JSON, and 3D assets whenever licensing allows.
- Do not expose secrets, API keys, private endpoints, or paid prompt bodies in client files.
- Do not add a service worker unless offline behavior is explicitly requested and tested; stale caches make visual iterations difficult.

Three.js can run from a CDN import map, but every import must use one exact version and one CDN. Serve locally over HTTP during testing because module imports may not work from `file://`.

Keep art-direction references, rejected generated assets, terminal-headless screenshots, and review notes in a project `work/` folder outside the publishing root when practical. Copy only final runtime assets into the site. Do not ship image-generation caches, source prompts, or large unused variants.

Do not create a reduced `work/validation-site` mirror and validate that instead of the real output. Run the strict validator against the exact directory selected in GitHub Pages settings. `lumora-plan.json` belongs in that directory and `build_contract.publishing_root` remains `.`.

## Forms And Dynamic Features

GitHub Pages has no server runtime. Use one of these truthful patterns:

- a supplied external form endpoint
- a supplied booking or ecommerce service URL
- a `mailto:` or `tel:` action for simple contact
- a client-side demo explicitly described as local-only when the user requested a prototype

Never show a success message for data that was not actually sent. Do not invent checkout, account, inventory, or authentication behavior. Link to a real provider or explain the integration gap.

## Existing Framework Projects

If the user explicitly requests Vite or the existing site already uses it, keep the framework and make the built output publishable through `/docs`, a `gh-pages` branch, or a GitHub Pages Actions workflow. Set the correct base path and test the deployed artifact, not only the dev server.

Do not introduce Vite solely because a donor prompt mentions it. Static translation is the default for fresh Lumora builds.

## Local Preview

Serve the site from its root before verification:

```bash
python -m http.server 8000
```

Use another open port when needed. Test the server URL through terminal-headless Playwright, not by double-clicking HTML or connecting an in-app site preview, especially when modules, fetch, video, canvas, or route checks are involved.

## Publishing Handoff

At delivery, report:

- the exact folder that should be the repository root
- the route-manifest count and disposition of any migrated source routes
- whether Pages should publish from root, `/docs`, or Actions
- whether `CNAME` is present
- all external services or CDN dependencies
- all local video, model, texture, font, and generated-image dependencies
- any dynamic feature that still needs a real endpoint
