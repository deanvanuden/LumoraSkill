---
name: lumora
description: Create or radically redesign unique, company-specific, award-level websites for GitHub Pages using Lumora's licensed MotionSites prompt library as directly inspected design DNA. Use when the user invokes $lumora or asks for a premium marketing site, product or ecommerce site, SaaS site, portfolio, studio, local-business site, multipage company website, or motion-rich visual redesign. Plans a traceable source mix, generates fit-for-slot imagery when needed, implements static HTML/CSS/JavaScript with advanced motion or 3D only when justified, and verifies responsive behavior, interactions, media, accessibility, and deployment readiness.
---

# Lumora

Build a bespoke digital experience around the company, not a decorated template. Use the bundled MotionSites prompts as a creative engineering library: inspect the selected prompt bodies, extract their strongest composition and interaction ideas, then reinterpret those ideas for the current brand and a static GitHub Pages build.

The prompt library is distributed under the maintainer-reported permission in `references/permissions.md`. Never place prompt bodies in a generated customer project.

## Non-Negotiables

- Start from company truth: offer, audience, proof, personality, place, product, story, real routes, and real media.
- Run `scripts/lumora_plan.py` before implementation. Do not select sources from titles alone.
- Inspect every selected source prompt with `scripts/inspect_lumora_prompt.py`; read the primary composition source in full.
- Give each donor a defined job. Never average five unrelated styles into one generic result.
- Establish one company-specific creative thesis, one visual motif, and one signature interaction before coding.
- Generate or source real visual media when the project lacks it. Do not substitute CSS blobs, gradient orbs, primitive pseudo-art, empty mockups, or placeholder stock imagery.
- Build plain static HTML, CSS, and JavaScript for new projects by default. Adapt Vite/React prompt concepts rather than reproducing their framework scaffolding.
- Use motion to explain, reveal, compare, or intensify content. Do not add every available effect.
- Make all navigation, routes, controls, forms, accordions, tabs, selectors, galleries, and CTAs behave truthfully.
- Respect reduced motion, coarse pointers, touch, keyboard access, and mobile document flow.
- Finish with browser screenshots and `scripts/validate_lumora_site.py`; do not hand off an unverified poster.

## Source Hierarchy

Use at most five prompt donors, each with a different responsibility:

1. `foundation`: page composition, section cadence, and global spatial logic.
2. `hero`: first-viewport architecture and dominant media behavior.
3. `narrative`: one distinctive mechanism for product, service, story, proof, or work.
4. `motion`: one signature scroll or interaction sequence.
5. `conversion`: purchase, inquiry, booking, signup, pricing, or closing behavior.

The foundation source wins when donors conflict. The site-wide brand system wins on copy, colors, fonts, and media. The motion source may change choreography but may not reorganize the whole page.

Each selected source must contribute at least two concrete decisions recorded in `lumora-plan.json` and mapped to actual sections. Drop a donor that contributes only a mood word.

## Required Workflow

### 1. Discover

Inspect the workspace and any supplied URL, screenshots, files, brand assets, and media. Build a factual inventory covering:

- company, audience, offer, differentiators, and primary conversion
- real claims, products, services, prices, reviews, credentials, contact details, and locations
- current pages and routes
- available logos, photography, product media, video, illustration, type, and color signals
- facts that are missing and must not be invented

If a source site exists, inspect it with the available browser tooling before selecting prompts.

### 2. Plan From The Full Library

Run from the skill directory or with an absolute script path:

```bash
python scripts/lumora_plan.py "<complete company and website brief>" --output "<site-root>/lumora-plan.json"
```

Use `--pages multi` for an explicitly multipage build and `--seed <value>` only when a deliberate alternate direction is wanted.

Read `references/prompt-remix.md`, then follow each selected source's inspection command. Use full inspection for `foundation`; use full or focused inspection for the other sources as directed by the plan. Extract visible layout relationships, media roles, component behavior, choreography, responsive behavior, and conversion mechanics. Ignore example-brand copy and framework boilerplate.

### 3. Lock The Creative Direction

Read `references/creative-direction.md`. Before editing website files, update `lumora-plan.json` with:

- a one-sentence creative thesis rooted in the company
- a company-specific signature motif
- the visual system: composition, type character, palette logic, material, media treatment, shape language, and section rhythm
- the source-to-section map
- the media-slot plan
- the motion map and reduced-motion alternatives

Set `creative_direction.status` to `locked` after these decisions are final. For every source, fill at least two `implemented_contributions` and one or more `implemented_sections`. Fill `media_plan.slots`, `motion_plan.desktop_implementation`, and `motion_plan.mobile_recomposition`; the validator treats omissions as blockers.

Reject a direction if the same art direction could be pasted onto an unrelated company without changing its meaning.

### 4. Direct And Create Media

Read `references/media-motion.md` whenever the site uses prominent imagery, video, canvas, 3D, or scroll choreography.

- Use supplied company media first when it is strong enough.
- If no useful visual reference exists, generate one or more implementation-oriented art-direction frames before coding, inspect them, and extract the visible system.
- Generate separate fit-for-slot assets for hero, product, editorial, gallery, texture, or background roles when the existing media cannot carry them.
- Keep generated text and logos out of raster images; render brand text in HTML/CSS.
- Never imply that generated people, premises, results, certifications, or products are real company evidence.
- Download or generate project-local media. Do not hotlink MotionSites example assets in the final site.

Use video only when movement is central to the concept. When no suitable video can be created or sourced, redesign that slot as an intentional still-image interaction instead of shipping an unrelated clip.

### 5. Build For GitHub Pages

Read `references/github-pages.md` before implementation.

For a new site, default to:

```text
index.html
styles.css
script.js
404.html
.nojekyll
lumora-plan.json
assets/images/
assets/video/
assets/fonts/
```

Add real route files such as `about.html`, `work.html`, `product.html`, or `contact.html` when the page map needs them. Use relative URLs so both repository Pages URLs and custom domains work. Add `CNAME` only when the user supplied the domain.

Use semantic HTML, a deliberate CSS token system, and project-specific JavaScript. Load GSAP 3.13+ with ScrollTrigger through pinned static scripts when advanced choreography is justified. Use Three.js only when an actual inspectable 3D subject is part of the concept. Smooth scrolling is optional, never a default requirement.

Mark major sections with `data-lumora-source="<prompt-id>"` so the final implementation remains traceable to `lumora-plan.json`.

### 6. Choreograph

Use three motion layers:

- `signature`: one memorable scroll, video, spatial, or narrative interaction unique to this company
- `structural`: one consistent reveal/transition language across sections
- `micro`: hover, press, focus, menu, gallery, and form feedback

Prefer transform and opacity. Bound pinned/sticky effects to stable containers, disable them when mobile flow becomes fragile, and provide a no-motion state that exposes all content immediately.

### 7. Verify

Read `references/quality-gates.md`. Serve the site locally, then inspect at minimum:

- desktop around 1440 x 1000
- mobile around 390 x 844
- one wide desktop viewport when composition or canvas framing depends on width

Test navigation, routes, keyboard focus, touch behavior, forms, controls, asset loading, console errors, reduced motion, and horizontal overflow. For canvas/Three.js, verify nonblank pixels, framing, interaction, and mobile fallback.

Run:

```bash
python scripts/validate_lumora_site.py --site-root "<site-root>" --plan "<site-root>/lumora-plan.json"
```

Fix errors and visually meaningful warnings before delivery.

## Anti-Generic Gate

Do not ship any of these unless the company or selected source specifically requires them:

- centered headline over an atmospheric dark image
- equal three-card feature rows or card-heavy page composition
- purple/blue glow, gradient text, glass panels, or floating decorative blobs as automatic premium styling
- fake dashboard panels, fake metrics, generic testimonials, or invented awards
- repeated left-copy/right-image sections
- the same generated image reused across unrelated prominent slots
- motion that merely moves decoration without supporting content
- copy such as "elevate," "unleash," "revolutionize," "next-gen," or "seamless" without a concrete factual reason

Award-level does not mean maximum effects. It means a clear idea, excellent media, controlled hierarchy, exact execution, and motion that belongs to this company.

## Reporting

Before coding, briefly report the creative thesis, selected source IDs and jobs, page map, signature moment, and media-generation plan.

After implementation, report changed files, generated/source media, prompt IDs used, interactions implemented, validation performed, local preview URL, and any truthful remaining gaps.

## References

- `references/creative-direction.md`: company DNA, originality controls, and visual-system decisions.
- `references/prompt-remix.md`: how to inspect and translate MotionSites prompts without losing their strongest ideas.
- `references/media-motion.md`: image direction, video/3D decisions, motion hierarchy, and performance rules.
- `references/github-pages.md`: static architecture, routes, domains, asset paths, forms, and deployment constraints.
- `references/quality-gates.md`: browser, responsive, interaction, accessibility, and visual verification.
- `references/design-dna-index.json`: generated index of every prompt's roles, layouts, styles, motion, media, interactions, and stack.
- `references/motionsites-prompt-library.json`: licensed source prompt bodies.
- `references/permissions.md`: reported redistribution permission.
