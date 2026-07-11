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

Use another open port when needed. Test through the server URL, not by double-clicking HTML, especially when modules, fetch, video, canvas, or route checks are involved.

## Publishing Handoff

At delivery, report:

- the exact folder that should be the repository root
- whether Pages should publish from root, `/docs`, or Actions
- whether `CNAME` is present
- all external services or CDN dependencies
- any dynamic feature that still needs a real endpoint

