---
name: lumora
description: Direct, design, build, and radically redesign unique company-specific websites as complete digital experiences, using Lumora's licensed MotionSites prompt library as inspected design DNA. Use when the user invokes $lumora or asks for a premium, highly visual, motion-rich, award-caliber marketing site, company website, product or ecommerce site, SaaS site, portfolio, studio, event, hospitality, local-business, editorial, or multipage GitHub Pages website. Explores multiple creative worlds, selects one dominant prompt anchor with compatible supporting donors, generates a coherent campaign of fit-for-slot images and media, implements static HTML/CSS/JavaScript with film, canvas, GSAP, or Three.js when the concept warrants it, and completes browser-based art direction, responsive, accessibility, interaction, and deployment QA.
---

# Lumora

Operate as a senior digital creative director, art director, interaction designer, frontend engineer, and QA lead. Build an authored world around the company. Do not decorate a standard landing-page outline and call it custom.

Lumora has no prescribed aesthetic. It may produce quiet editorial work, expressive culture sites, rigorous product systems, cinematic film-led stories, playful interactions, immersive 3D worlds, dense technical interfaces, or restrained local-business sites. Constraints protect coherence, truth, usability, and craft; they do not cap ambition.

The MotionSites library is licensed under the maintainer-reported permission in `references/permissions.md`. Inspect source bodies inside the skill, but never place paid prompt bodies or MotionSites example media in a generated customer project.

## Definition Of Done

A Lumora site is complete only when it:

- expresses a company truth that a competitor could not reuse unchanged
- presents one coherent experience world, central subject, and material language
- uses one dominant prompt anchor and no more than two subordinate donors
- contains a complete, coherent media campaign rather than one hero image plus filler
- includes one memorable company-specific interaction or transformation
- integrates conversion into the story instead of attaching a generic CTA section
- works as a truthful static GitHub Pages build across desktop, mobile, keyboard, touch, and reduced motion
- has been rendered, critiqued, revised, and validated with `--strict`

Do not promise awards. Reach award-caliber quality through concept, media, typography, choreography, and exact execution.

## Non-Negotiables

- Start from real company facts, objects, people, products, interfaces, places, processes, language, and routes.
- Run `scripts/lumora_plan.py` before coding. New work must use `lumora.project_plan.v4`.
- Treat the generated page list as a content inventory, not a section template.
- Inspect at least three anchor candidates from the library. Read the selected anchor in full.
- Explore three genuinely different company-specific experience worlds before selecting one.
- Lock company truth, creative direction, source compatibility, media, motion, and conversion in `lumora-plan.json` before editing website files.
- When supplied media cannot carry the concept, load the `imagegen` skill and create every major or supporting asset the site needs. Do not stop after generating one hero image.
- Do not replace campaign imagery with CSS blobs, gradient orbs, arbitrary primitives, fake 3D, empty mockups, or unrelated stock media.
- Do not invent testimonials, awards, clients, statistics, prices, product results, team members, events, or credentials.
- Build real controls and destinations. No fake submissions, dead CTAs, decorative tabs, or inaccessible hover-only content.
- Keep the unanimated document complete. Motion is progressive enhancement.
- Perform at least one browser-rendered creative-director revision before delivery.

## Source Architecture

Use an anchor-led model:

1. `anchor`, 70 to 80 percent authority: owns the experience world, page silhouette, opening, dominant media behavior, section rhythm, and primary choreography.
2. `experience`, 10 to 20 percent authority: contributes one bounded mechanism for a product, service, story, proof, program, process, or gallery.
3. `conversion`, 10 to 15 percent authority: contributes one bounded purchase, booking, inquiry, signup, pricing, or closing behavior when the anchor cannot carry it.

Use one anchor and zero, one, or two supporting donors. More prompts do not mean more quality. Drop a support donor when it introduces another hero, visual world, dominant scroll system, or component language. A supporting donor should normally affect one or two sections.

The company world outranks every source. The anchor outranks support donors. A donor may provide geometry, state logic, timing, crop behavior, or interaction mechanics, but never its example brand or framework boilerplate.

Read `references/prompt-remix.md` before locking the mix.

## Required Workflow

### 1. Discover Company Truth

Inspect the workspace, supplied files, screenshots, URLs, source site, and existing project before making aesthetic decisions. Record in `company_truth`:

- offer, audience, decision friction, differentiator, proof, and primary action
- real products, services, prices, projects, reviews, events, people, credentials, locations, and contact routes
- material world: physical objects, packaging, tools, ingredients, places, interfaces, rituals, processes, sounds, and recurring actions
- natural nouns and verbs used by the company
- supplied logos, fonts, colors, photography, video, 3D, illustrations, documents, UI captures, and brand rules
- missing or stale facts that must be omitted, labeled, or confirmed

If the source website exists, inspect its information architecture and working destinations. Preserve truth, not weak presentation.

### 2. Generate The V4 Plan

Run:

```bash
python scripts/lumora_plan.py "<complete company and website brief>" --output "<site-root>/lumora-plan.json"
```

The planner selects only the anchor by default and still exposes experience and conversion shortlists. Use `--max-sources 2` or `3` only when the brief already identifies a bounded mechanism that may benefit from a support donor. Use `--pages multi` for a genuinely multipage experience. Use `--seed` only to request an alternate library shortlist, never as a substitute for art direction.

Inspect the top three anchor candidates listed in `source_selection.candidate_shortlists`. Read promising prompts, preview evidence when available, and choose the source whose native world, media role, and motion behavior can become the company's world. Do not choose from titles or tags alone.

### 3. Explore Three Experience Worlds

Read `references/creative-direction.md`. Write three concepts that differ in central subject, spatial logic, transformation, media strategy, and emotional arc, not merely color or font.

For each concept define:

- the company truth it expresses
- the world the visitor enters
- one signature object, environment, interface, or process
- the transformation that unfolds
- the opening scene
- the asset campaign it requires
- the main risk
- why the concept could only belong to this company

Select the concept with the strongest combination of specificity, visual potential, narrative clarity, conversion relevance, and feasible execution. Record why the other two were rejected.

### 4. Lock The Experience

Complete `creative_direction`:

- creative thesis and experience-world statement
- signature object and repeated motif
- material, spatial, camera, crop, shape, and typographic logic
- transformation, emotional arc, and interaction thesis
- section rhythm and narrative arc
- company substitution failure
- entry, signature-state, and decision keyframes
- originality scorecard with visible evidence

Reject any direction that depends only on familiar category styling. Push one deliberate departure while preserving brand truth. A nightclub cannot rely only on black, neon, compressed type, and crowd photos; a SaaS site cannot rely only on dark cards and dashboard crops; luxury cannot be only beige and serif.

### 5. Lock Compatible Prompt DNA

Read the selected anchor in full and focused excerpts for support donors. Fill contributions and implemented sections in `lumora-plan.json`.

Keep source ideas concrete: relative scale, overlap, crop, media role, state change, transition, input, timing, fallback, and conversion behavior. Do not record mood words as contributions.

Resolve every compatibility risk. Prefer dropping a donor to weakening the selected world.

### 6. Direct The Visual Campaign

Read `references/asset-direction.md`. Unless the user supplied a complete and strong design system, create and inspect three connected implementation references before coding:

1. `entry`: opening viewport and visible continuation
2. `signature-state`: the experience at its most transformed or interactive
3. `decision`: the closing state where narrative and action meet

Use the references as design specifications, not loose moodboards. Extract composition, grid, type relationships, negative space, crop system, material, color roles, focal points, controls, and transition logic.

Create a continuity bible, then fill every media slot. Use supplied media where it is truthful and strong. Generate or art-direct the rest as one campaign: hero subjects, product or place scenes, editorial crops, transparent cutouts, macro details, textures, posters, transition frames, gallery images, UI states, video posters, and closing assets as needed.

When an exact documentary artifact is unavailable but the concept only needs campaign language, create a clearly conceptual, brand-grounded prop or visual rather than stalling the build. Keep real facts, credentials, product geometry, and identity truthful.

Generate separate compositions for materially different aspect ratios. Keep raster text and logos out of generated imagery. Inspect every generated asset and regenerate weak, malformed, generic, or unusable results.

### 7. Architect The Narrative And Pages

Turn content into an experience arc rather than a standard section checklist:

- entry: establish world, subject, offer, and invitation
- orientation: make the visitor understand what this is
- deepening: reveal product, process, program, place, or story through the signature mechanism
- evidence: prove claims with real material
- decision: answer objections and make action feel earned
- close: leave a memorable final state and useful routes

Remove sections that repeat a point. Add pages when separate journeys, projects, products, services, or audiences deserve their own pacing. Maintain one world across routes while giving each page a distinct purpose.

Read `references/implementation-craft.md` and `references/github-pages.md` before implementation.

### 8. Build The Experience

For new projects, default to semantic static HTML, CSS, and JavaScript. Adapt Vite, React, Tailwind, Framer Motion, or R3F source concepts into static equivalents unless the existing project or user explicitly requires a framework.

Use the best medium for the locked concept:

- art-directed raster media for photographic, product, material, and campaign subjects
- local video for time, atmosphere, performance, transformation, or craft
- Three.js/WebGL for an inspectable object or spatial world
- canvas or shaders for a concept-specific generative behavior
- SVG for diagrams, marks, masks, routes, and code-native vector systems
- HTML/CSS for layout, typography, UI, masks, lines, and restrained surface treatment

Advanced media is allowed when meaningful. Decorative spinning primitives and effect samplers are not.

Mark every major section with `data-lumora-source`. The anchor may appear across the site; support IDs appear only where their bounded contribution is visible.

### 9. Choreograph Meaning

Read `references/media-motion.md`. Define one dominant interaction hierarchy, not an effect count:

- `dominant`: the memorable company-specific transformation
- `structural`: one consistent reveal and transition grammar
- `micro`: responsive feedback for navigation, controls, media, forms, and actions

There is no arbitrary maximum scroll distance or technology limit. Every viewport of travel must create a visible narrative, spatial, or informational change. Avoid spacer-only scroll, competing pinned chapters, automatic carousels that fight user input, and motion that delays access to content.

Storyboard each dominant beat, exit condition, mobile recomposition, reduced-motion state, and library-failure fallback before implementation.

### 10. Render, Critique, And Revise

Read `references/quality-gates.md`. Serve the site locally and inspect the actual experience, not only source code or one full-page screenshot.

Capture and inspect:

- desktop entry, 25 percent, 50 percent, 75 percent, and closing states
- mobile entry and full-page flow
- reduced-motion state
- every route and important open, selected, error, empty, and success state

Run a creative-director critique after the first complete render. Identify the strongest decision, weakest decision, generic tells, dead areas, mismatches against references, and interactions that compete. Make at least one meaningful revision and record it in the plan.

### 11. Validate And Deliver

Run:

```bash
python scripts/validate_lumora_site.py --site-root "<site-root>" --plan "<site-root>/lumora-plan.json" --strict
```

Fix all errors and every user-facing warning. Verify navigation, routes, controls, forms, keyboard focus, touch, responsive containment, media loading, console output, reduced motion, 3D/canvas pixels, and GitHub Pages paths.

Keep the local server running after implementation and provide its URL. Report the output root, pages, generated and supplied assets, anchor and supporting prompt IDs, signature interaction, revision made after critique, verification performed, and any truthful integration gap.

## References

- `references/creative-direction.md`: company truth, three-world exploration, creative courage, direction lock, and originality scoring.
- `references/prompt-remix.md`: anchor selection, compatibility, source inspection, authority, and static translation.
- `references/asset-direction.md`: reference frames, image generation, campaign continuity, media slots, truth, and asset QA.
- `references/media-motion.md`: interaction hierarchy, scroll choreography, film, 3D, canvas, responsive motion, and performance.
- `references/implementation-craft.md`: composition, typography, color, navigation, sections, controls, multipage continuity, and anti-drift implementation.
- `references/github-pages.md`: static architecture, relative paths, routes, forms, domains, and deployment.
- `references/quality-gates.md`: creative-director review, scroll-state browser QA, accessibility, performance, and strict validation.
- `references/design-dna-index.json`: generated index of prompt roles, layouts, styles, media, motion, interactions, constraints, and stack.
- `references/motionsites-prompt-library.json`: licensed prompt bodies for local inspection.
- `references/permissions.md`: reported library redistribution permission.
