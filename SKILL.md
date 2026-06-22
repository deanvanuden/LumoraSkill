---
name: lumora
description: Build or redesign premium static websites with "$lumora" or "Lumora" by selecting MotionSites-derived section recipes, generating or inspecting an image-first visual reference, then assembling plain HTML/CSS/vanilla JS pages. Use for high-quality websites, landing pages, product/ecommerce pages, SaaS sites, agency sites, portfolios, waitlists, signup pages, multipage company sites, redesigns, and motion-rich frontend builds. Must use the bundled static section library, support multipage static output, use image generation when no useful media/reference exists, and avoid Vite or framework scaffolding unless explicitly requested or already present.
---

# Lumora

Lumora is a premium static website assembly workflow. It turns the bundled MotionSites prompt collection into clean reusable section recipes, then uses an image-first taste pass to make the selected sections feel like one high-end website.

The bundled MotionSites prompt library is included under owner-approved commercial redistribution permission reported by the skill maintainer on 2026-06-12. See `references/permissions.md`. Do not edit prompt bodies in `references/motionsites-prompt-library.json`.

## Non-Negotiables

- Build static websites by default: `index.html`, `styles.css`, `script.js`, assets, and optional extra `.html` pages.
- Do not use Vite, React, Next, Tailwind, or a bundler unless the user explicitly asks or the existing project already uses that stack.
- Use `references/static-section-library.json` as the default section source.
- Run `scripts/select_lumora_sections.py "<brief>"` before implementation.
- Generate or inspect a visual reference before coding. If the user supplies no usable media/reference, use image generation.
- Use selected section recipes for structure. Use the visual reference only to tune palette, typography mood, spacing, media framing, button/card finish, and motion feel.
- Support multipage sites when the source/brief calls for real routes.
- Wire every visible link, button, form, tab, accordion, selector, carousel, nav item, and route.
- Verify desktop and mobile layout before final delivery.

## Required Workflow

1. Build a source inventory from the user brief, supplied files, URLs, brand facts, products, pages, audience, CTAs, and existing media.
2. If the request involves an existing website, inspect it first and preserve useful source media, copy facts, routes, and brand identity.
3. Run:

   ```bash
   python scripts/select_lumora_sections.py "<website brief>"
   ```

4. Read the chosen recipe entries from `references/static-section-library.json`.
5. Read `references/static-section-workflow.md` for build rules.
6. Read `references/lumora-taste-system.md` for the image-first taste pass.
7. Create or inspect the visual reference:
   - Use supplied visual references/media first.
   - If none exist, generate a reference image from the selector's `image_first.prompt`.
   - For product/ecommerce/local/portfolio/beauty/restaurant/real-estate sites with no media, generate fit-for-slot assets before coding.
8. Analyze the visual reference and extract palette, type character, spacing rhythm, section density, media frame shapes, CTA styling, and component finish.
9. Create the static page map:
   - Onepage: `index.html`.
   - Multipage: `index.html` plus route files such as `about.html`, `services.html`, `product.html`, `pricing.html`, or `contact.html`.
10. Implement sections using selected recipe contracts:
    - add `data-lumora-section="<recipe-id>"` to each major section
    - use recipe `html_structure` for content blocks
    - use recipe `css_hooks` or compatible class names
    - implement recipe `js_behaviors` when visible
11. Apply one site-wide visual system with CSS variables for fonts, colors, surfaces, borders, radii, shadows, spacing, and motion.
12. Use vanilla JS only for interactions and state.
13. Verify responsive containment, links/routes, interactions, media loading, forms, console errors, and visual fidelity to the reference.

## Section Library Maintenance

Regenerate the transformed section library after updating the MotionSites prompt library:

```bash
python scripts/build_static_section_library.py
```

The generated `references/static-section-library.json` must include every source record but must not duplicate full prompt bodies. It stores transformed recipes, source hashes, section roles, atoms, static contracts, and media needs.

## What To Report

During a Lumora build, report the practical build plan before coding:

- selected section IDs and roles
- onepage or multipage file map
- media/image generation plan
- visual reference summary after inspection
- static files that will be created or edited

After implementation, report:

- files created or changed
- section recipe IDs used
- generated/source assets used
- verification performed
- any remaining gaps such as missing real product photos or unverified external links

## References

- `references/static-section-workflow.md`: full static assembly process and verification checklist.
- `references/lumora-taste-system.md`: image-first visual direction and premium design rules.
- `references/static-section-library.json`: generated section recipes from every MotionSites record.
- `references/motionsites-prompt-library.json`: original licensed prompt library and hashes.
- `scripts/select_lumora_sections.py`: required planner for new builds.
- `scripts/build_static_section_library.py`: regenerates the recipe library.
