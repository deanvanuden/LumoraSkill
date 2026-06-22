# Lumora Static Section Workflow

Lumora builds premium static websites by assembling transformed MotionSites section recipes, then applying one generated or supplied visual reference as the site skin.

## Source Files

- `references/motionsites-prompt-library.json`: licensed source prompt library with full prompt bodies.
- `references/static-section-library.json`: generated section recipe library. This is the default build source for selection and implementation.
- `scripts/build_static_section_library.py`: regenerates the recipe library from every MotionSites record.
- `scripts/select_lumora_sections.py`: creates a page, section, media, and image-first plan from a user brief.
- `references/lumora-taste-system.md`: visual direction rules used after section selection.

The static section library intentionally omits prompt bodies. It stores source IDs, titles, hashes, categories, inferred roles, layout atoms, visual atoms, interaction atoms, media needs, and plain HTML/CSS/JS contracts.

## Required Build Order

1. Build a source inventory from the user's brief, files, links, product info, brand assets, and existing media.
2. Run the section selector:

   ```bash
   python scripts/select_lumora_sections.py "<website brief>"
   ```

3. Read the selected recipes from `references/static-section-library.json`.
4. Create or inspect the visual reference before coding:
   - If the user supplied design references or media, inspect those first.
   - If no useful visual reference/media exists, use image generation before implementation.
   - Use the `image_first.prompt` from the selector as the base image prompt.
5. Analyze the image/reference and extract:
   - palette
   - type character
   - spacing rhythm
   - section density
   - media frame shapes
   - CTA style
   - card/panel treatment
   - motion feel
6. Assemble static files directly:
   - `index.html`
   - `styles.css`
   - `script.js`
   - optional additional `.html` pages for multipage builds
7. Use selected recipes as the structural source of truth. Use the image/reference only as the visual skin.
8. Wire all links, buttons, forms, tabs, accordions, selectors, drawers, carousels, and routes.
9. Verify desktop and mobile screenshots, console errors, responsive containment, links/routes, and media loading.

## Static Output Rules

- Do not scaffold Vite, React, Next, Tailwind, or a bundler unless the existing project already uses it or the user explicitly asks.
- Prefer one `styles.css` and one `script.js` shared across pages.
- Use semantic sections with `data-lumora-section="<recipe-id>"`.
- Use CSS variables for all theme values:
  - fonts
  - canvas/surface/ink/muted colors
  - accent colors
  - border/radius/shadow values
  - spacing steps
  - motion durations/easing
- Use vanilla JS for behavior only:
  - mobile navigation
  - accordions
  - tabs
  - sliders
  - selectors
  - form validation and feedback
  - scroll reveal through `IntersectionObserver`
- Do not leave placeholder `href="#"`, empty buttons, fake routes, or inert forms.

## Page Assembly Rules

Create a page map before coding.

For a onepage build:

- `index.html`: nav, hero, proof, main sections, conversion, footer.

For multipage builds:

- Reuse the same nav, footer, CSS variables, and interaction patterns.
- Make every linked page real.
- Put only page-relevant sections on each route.
- Keep routes simple static files unless the existing project uses another router:
  - `index.html`
  - `about.html`
  - `services.html`
  - `product.html`
  - `pricing.html`
  - `contact.html`

## Section Recipe Usage

Each selected recipe contains:

- `id`: source recipe ID for traceability.
- `section.type` and `section.roles`: the section's job.
- `atoms.layout`: layout structures to preserve.
- `atoms.visual`: visual cues to map into the generated image skin.
- `atoms.interaction`: behaviors to implement when visible.
- `atoms.conversion`: CTA or conversion intent.
- `static_contract.html_structure`: required content blocks.
- `static_contract.css_hooks`: suggested class/module names.
- `static_contract.js_behaviors`: expected behavior.
- `media_needs`: assets to source or generate.

Use the recipe structure directly. Do not replace it with a generic landing-page template after image generation.

## Image And Media Rules

Use this priority:

1. Client/source media supplied by the user or existing project.
2. Existing project assets that fit the section role.
3. Generated fit-for-slot assets when no useful media exists.

Generate media when the site needs visual credibility and no suitable images exist. For product, ecommerce, portfolio, beauty, restaurant, real estate, local service, or highly visual brand sites, avoid placeholder boxes.

Generated images must:

- match the slot role and aspect ratio
- avoid embedded readable text unless the text is meant to be replaced in HTML
- avoid fake logos or fake claims
- avoid claiming to show real staff, locations, products, certifications, or customers unless the user supplied references
- be copied into the project assets folder

## Implementation Pattern

Recommended static structure:

```text
site-root/
  index.html
  styles.css
  script.js
  assets/
    generated-or-source-media.png
```

Each section should follow this pattern:

```html
<section class="section section--role" id="role" data-lumora-section="source-id">
  <div class="section__inner">
    <!-- Recipe blocks translated into project copy and media -->
  </div>
</section>
```

## Verification Checklist

Before final delivery:

- Every selected recipe ID appears in the built sections through `data-lumora-section`.
- The build uses plain static files unless explicitly justified.
- The visual reference was generated or inspected before coding.
- Site styling visibly follows the reference image's palette, spacing, media framing, and component finish.
- Every expected section role from the plan is present or consciously omitted with a reason.
- Desktop and mobile layouts have no horizontal overflow or overlapping text.
- All nav/footer/CTA links resolve.
- Forms validate and show feedback.
- Interactive controls are keyboard-reachable where relevant.
- Console has no runtime errors.
- Media loads from project assets or valid URLs.
