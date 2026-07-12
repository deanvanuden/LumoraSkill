# Lumora Quality Gates

## Contents

1. Quality philosophy
2. Gate 1: company truth and direction exploration
3. Gate 2: selected world and prompt authority
4. Gate 3: asset campaign
5. Gate 4: composition and implementation fidelity
6. Gate 5: interaction and motion
7. Gate 6: responsive experience
8. Gate 7: content, conversion, and behavior
9. Gate 8: accessibility, performance, and resilience
10. Gate 9: GitHub Pages
11. Browser review protocol
12. Creative-director critique
13. Automated audit
14. Rebuild conditions

## Quality Philosophy

Structural correctness is necessary but not sufficient. A site can have valid HTML, working links, responsive CSS, prompt traceability, and zero console errors while still being generic, visually weak, overlong, or incoherent.

Lumora therefore uses three forms of evidence:

1. `plan evidence`: company truth, explored worlds, selected direction, source authority, asset strategy, choreography, and conversion
2. `render evidence`: screenshots and interaction states across scroll, routes, desktop, mobile, and reduced motion
3. `revision evidence`: a recorded creative-director critique and at least one meaningful completed revision

Do not treat self-scored plan fields as proof without browser inspection.

## Gate 1: Company Truth And Direction Exploration

- `lumora-plan.json` uses `lumora.project_plan.v4` for new work.
- Company name, offer, audience, difference, place/context, material world, vocabulary, routes, supplied media, proof, and missing facts are recorded.
- Stale dates, unsupported claims, fake prices, and invented evidence are absent.
- Three concepts differ in subject, world, transformation, hero scene, and asset strategy.
- One concept is selected for a concrete reason.
- At least two concepts are rejected with meaningful reasons.
- The selected direction passes the substitution test.

Fail when the three concepts are color variants of one layout or when the selected world could fit any competitor.

## Gate 2: Selected World And Prompt Authority

- Creative thesis, experience world, signature object, motif, material, spatial logic, camera, transformation, emotional arc, and interaction thesis describe one coherent system.
- Design fingerprint fields are concrete and mutually compatible.
- Entry, signature-state, and decision keyframes are defined and reference inspected assets.
- Originality score is at least 16/20 with no zero and visible evidence for every dimension.
- At least three anchor candidates were inspected.
- Source mix contains one anchor and zero to two supporting donors.
- Anchor authority remains at least 70 percent.
- Every support donor solves one named need, remains within one or two sections, and does not create another hero or dominant interaction.
- Every compatibility risk is resolved or the donor is removed.
- Source contributions describe actual visible relationships, not style adjectives.

Fail when prompt traceability exists only on paper while the rendered site is generic.

## Gate 3: Asset Campaign

- Supplied assets are audited for truth, quality, crop, and ownership.
- Entry, signature-state, and decision reference frames belong to one site and one world.
- Each selected reference has a deep visual analysis.
- The signature asset is supplied, generated, authored, modeled, captured, or filmed and visually credible.
- The continuity bible defines subject, camera, lens, light, material, environment, grade, finish, crop, and negative constraints.
- Every prominent media slot has role, page, aspect ratio, target render, focal point, source, truth status, and reuse policy.
- Final assets were produced separately from layout reference frames.
- Generated assets contain no fake logo, readable raster text, watermark, malformed subject, irrelevant prop, or false documentary evidence.
- Different prominent slots do not reuse one image as filler.
- Media continues after the hero and reaches the closing state.
- Desktop and mobile use intentional crops or variants.
- Local asset dimensions and compression suit the actual render.

Fail when the concept promises a physical object or world but implementation substitutes CSS primitives, empty mockups, or one repeated image.

## Gate 4: Composition And Implementation Fidelity

- Rendered states match references in focal point, hierarchy, negative space, grid, crop, material, type character, control language, and section rhythm.
- The first viewport makes the company, product, place, person, or offer a primary signal.
- One focal subject leads the opening.
- Hero copy remains readable, concise, and normally within one to three headline lines.
- A hint of continuation is visible where the concept permits it.
- Page chapters vary in density and media-to-copy ratio without losing alignment.
- Cards are used only for real independent items or framed tools.
- Sections are not nested floating cards.
- Repeated media and controls have stable dimensions.
- Text, controls, prices, long words, and labels fit at every tested width.
- No element overlaps unrelated previous or following content.
- Blank space reads as composed focus rather than missing content.
- The closing state advances or completes the world.

Fail when the generated reference is strong but the coded result collapses into centered headings, equal card rows, repeated split sections, generic gradients, or text-heavy filler.

## Gate 5: Interaction And Motion

- One dominant interaction is clearly identifiable.
- Its subject, input, transformation, and narrative purpose derive from company truth.
- At least three storyboarded beats produce visible changes and settled readable states.
- Structural and micro motion remain subordinate and use one coherent language.
- Every viewport of a long or pinned chapter contains visible subject, information, or transformation.
- Long scroll tracks have a written occupancy justification and pass screenshot review.
- Autoplay, drag, hover, marquee, cursor, and scrub systems do not compete for attention.
- Motion never hides essential content indefinitely.
- Controls remain user-directed and truthful.
- Mobile and reduced-motion versions preserve the thesis.
- Missing motion libraries reveal static content instead of a blank page.

Fail when the experience feels like several donor demos, when the visitor waits through empty scroll, or when effects are memorable but the company is not.

## Gate 6: Responsive Experience

Test at minimum:

- desktop around 1440 x 1000
- mobile around 390 x 844
- wide desktop around 1920 x 1080 for full-bleed, 3D, film, or pinned work
- one narrower mobile width when names, labels, or controls are long

Verify:

- `document.documentElement.scrollWidth <= document.documentElement.clientWidth`
- first viewport subject and copy remain correctly framed
- mobile uses deliberate order, crop, and interaction changes
- pinned, sticky, horizontal, and overlapping scenes have stable parents and explicit mobile behavior
- touch controls do not require hover or precise pointer movement
- fixed controls respect safe areas and do not cover content
- viewport-height sections remain stable with browser chrome
- galleries and selectors remain operable by touch and keyboard
- alternate assets do not cause layout shifts
- all pages maintain the world without repeating the same hero composition

Fail when mobile is only a single-column collapse that loses the signature object, transformation, or conversion hierarchy.

## Gate 7: Content, Conversion, And Behavior

- Copy uses concrete company vocabulary, facts, products, places, materials, and actions.
- Unsupported superlatives and generic AI marketing phrases are removed.
- Heading hierarchy and reading order are clear without animation.
- Primary conversion is obvious, real, and appears at earned readiness moments.
- Secondary actions remain available but subordinate.
- Product variants, prices, event status, availability, route, contact, and booking facts are truthful.
- Navigation, route links, menus, dialogs, tabs, accordions, selectors, galleries, media controls, forms, and CTAs work.
- Forms implement real submission or a truthful external/mail route.
- Loading, disabled, empty, error, and actual success states exist where relevant.
- There are no `href="#"`, `javascript:void(0)`, empty controls, fake destinations, or false success messages.

Fail when the visual story and conversion do not connect or when a beautiful control has no truthful behavior.

## Gate 8: Accessibility, Performance, And Resilience

### Accessibility

- Semantic landmarks and heading order are correct.
- Images have contextual alt text or empty alt when decorative.
- Controls have accessible names and correct native semantics where possible.
- Menus, tabs, dialogs, accordions, and carousels expose state appropriately.
- Keyboard order is logical and focus is visible over every media state.
- Contrast remains readable as media or theme states change.
- Touch targets are at least 44 by 44 CSS pixels.
- The experience remains understandable without animation, audio, hover, color alone, or precise pointer input.

### Performance

- Hero media and fonts do not block the entire experience unnecessarily.
- Images have stable dimensions and appropriate formats.
- Video, canvas, 3D, and perpetual motion pause or reduce work when hidden or offscreen.
- Animation uses transform, opacity, clip, or shader uniforms rather than repeated layout work.
- Expensive blur, filter, and backdrop effects do not cover large moving regions.
- Models, textures, video, and raster assets are sized to their visible role.
- No repeated layout thrashing, runaway requestAnimationFrame, duplicate listener, or abandoned ScrollTrigger remains.

### Resilience

- Core content exists in the base document.
- Failed images, video, modules, libraries, or canvas scenes have useful fallbacks.
- Reduced motion exposes all content.
- Console has no errors and local requests do not fail.
- 3D/canvas screenshots or pixel checks prove the scene is nonblank and correctly framed.

## Gate 9: GitHub Pages

- Publishing root contains `index.html`, `404.html`, and `.nojekyll`.
- All local URLs are relative, route-correct, and case-correct.
- No prompt bodies, secrets, private endpoints, API keys, or protected media are public.
- The site works from a local static server without a build step unless a retained framework is explicitly configured.
- Multipage links work from every route.
- `CNAME` exists only for an exact supplied domain.
- External libraries use pinned versions.
- Forms and commerce use real external services or truthful gaps.

## Browser Review Protocol

Use Playwright or available browser tooling. Serve the site over HTTP from its publishing root.

### 1. Load And Settle

- open each route
- wait for fonts, hero media, 3D/model loading, and initialization
- inspect console and failed requests
- do not capture before the intended opening state settles

### 2. Capture Narrative States

On desktop capture:

- `desktop-entry`
- `desktop-25`
- `desktop-50`
- `desktop-75`
- `desktop-close`

Capture additional states at exact interaction beats, selected tabs, open menus, product variants, gallery states, or 3D positions.

On mobile capture:

- `mobile-entry`
- `mobile-full`
- any recomposed signature state

Capture `reduced-motion` with the preference emulated.

Full-page screenshots are useful for rhythm, but can misrepresent pinned and scrubbed content when capture advances the page faster than animation settles. Always pair a full-page image with viewport screenshots at real narrative states.

### 3. Inspect Visual Occupancy

At each state ask:

- Is there a clear focal subject?
- Does the viewport contain enough meaningful content?
- Is blank space intentional and composed?
- Is text fully readable?
- Has the previous animation settled?
- Is the next change already competing?
- Does the section boundary appear at the intended moment?

Inspect section bounding boxes and viewport intersection. Reject unexplained blank regions near or larger than a viewport.

### 4. Exercise Behavior

- open and close menus and dialogs with pointer, keyboard, and Escape
- follow every navigation and route link
- activate selectors, tabs, accordions, carousels, galleries, media controls, and CTAs
- test form validation, error, disabled, and real destination behavior
- verify hover alternatives on touch and focus
- rotate or resize where full-bleed framing is fragile
- hide and restore the page to test paused media and animation recovery

### 5. Inspect Containment And Runtime

- measure root scroll width against client width
- inspect large section bounding boxes and sticky parents
- ensure fixed controls do not cover content
- verify no blank canvas, failed texture, missing poster, or broken crop
- check that animation cleanup does not duplicate after resize

Record all checked states and review notes in `verification.visual_review`.

## Creative-Director Critique

After the first complete render, stop implementation and review the site as a director.

Record:

- strongest decision
- weakest decision
- three to five generic or incoherent risks
- mismatch against each reference keyframe
- dead, overlong, crowded, or repetitive sections
- weakest asset or crop
- motion that competes, delays, or lacks meaning
- conversion or content gap
- mobile loss of concept

Prioritize revisions by impact:

1. concept and signature subject
2. asset quality and continuity
3. composition and section rhythm
4. dominant interaction and scroll occupancy
5. typography and copy
6. conversion and behavior
7. micro polish

Complete at least one meaningful revision. Changing only color, border radius, or animation duration does not count when the underlying problem is concept, media, or structure.

Set `director_review.status` and `verification.visual_review.status` to `passed` only after rerendering the revised result.

## Automated Audit

Run:

```bash
python scripts/validate_lumora_site.py --site-root <site-root> --plan <site-root>/lumora-plan.json --strict
```

The validator checks:

- v4 company truth, direction exploration, world lock, scorecard, source authority, compatibility, asset plan, motion storyboard, conversion, director revision, and visual-review evidence
- prompt IDs and source hashes
- section traceability
- GitHub Pages files and relative local targets
- metadata, alt text, image dimensions, video behavior, forms, buttons, and placeholder URLs
- generic copy patterns
- reduced-motion support
- repeated image reuse
- multiple scrub systems, competing scrub/autoplay/drag behavior, and unjustified long scroll tracks

The validator cannot judge beauty. A passing audit never overrides weak screenshots.

## Rebuild Conditions

Do not keep polishing the same implementation when:

- the central concept is not visible without reading explanatory copy
- the signature asset is weak or unavailable
- the first viewport resembles a familiar template more than the selected world
- donors remain visibly stitched together
- multiple effects compete and no dominant interaction is clear
- long scroll creates dead or empty viewports
- reference-to-code drift affects the page silhouette or focal subject
- mobile removes the concept
- conversion conflicts with the narrative
- the experience depends on invented evidence

Return to the earliest failed gate: company truth, selected world, anchor, asset campaign, composition, or choreography. Rebuild from that decision instead of adding effects.
