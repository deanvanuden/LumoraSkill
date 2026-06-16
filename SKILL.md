---
name: lumora
description: Lumora builds complete premium websites from exact prompt_text entries in references/motionsites-prompt-library.json after scraping the target business, creating a niche-specific blueprint, and selecting a complete page prompt or compatible section prompts. Use when Codex is asked to build, redesign, improve, or generate a website, landing page, hero, SaaS site, agency site, portfolio, ecommerce page, waitlist, signup page, or rich frontend using "$lumora" or "Lumora"; Lumora must load and hash every selected prompt_text before coding, reject any section not built directly from a loaded prompt_text, use design/layout/components/motion 100% 1:1 with no interpretation, localize copy only inside prompt slots, use one cohesive font/color/background token layer, prepare fit-for-slot media or generated assets, enforce brand color tokens, make all clickable UI work, preserve multipage source sites, and verify responsive containment.
---

# Lumora

Lumora's default workflow is **Locked Verbatim Page + Diverse Section Composition Mode**.

**Prompt bodies copied 1:1. Design locked. Section structure locked. No loaded prompt_text, no section. Copy may be localized to the requested language. A single site-wide typography/color/background token layer is mandatory for cohesion. Complete pages allowed. Incomplete pages get extra compatible sections only when every selected prompt remains structurally exact.**

Use Lumora to build a website by selecting existing prompt entries from `references/motionsites-prompt-library.json`. Prompt bodies live in each entry's `prompt_text` field. Every selected `prompt_text` must be loaded and used **verbatim, byte-for-byte in meaning and whitespace-sensitive content**, as the implementation instruction for its page or section. Lumora may select one complete Landing Page / Website entry as the base when it is the strongest fit. If that base page is incomplete for a real website, add missing sections from other families only when every selected prompt can remain structurally exact without bridging, interpretation, or freeform harmonization. Lumora may also assemble a page from section-level prompts. It does not mean inventing a new design, creating new archetypes, interpreting sections, inventing layout, or merging prompt bodies into a new prompt. Visible website copy may be localized to German or another requested language, but the prompt's text roles, rhythm, hierarchy, section order, and component slots stay locked. When multiple prompts are composed, Lumora must apply the Site-Wide Visual Cohesion Rule so the final website feels like one brand, not a stack of unrelated sections.

The bundled MotionSites prompt library is included under owner-approved commercial redistribution permission reported by the skill maintainer on 2026-06-12. See `references/permissions.md`. Treat all `prompt_text` values as licensed bundled resources. During a Lumora build, selected prompt bodies are copied 1:1 into the agent's working instructions and followed exactly. Do not edit, rewrite, summarize, translate, merge, or store prompt bodies in new prompt files.

## Hard Prompt Evidence Gate

Lumora has no fallback mode. A section is valid Lumora output only when it is built directly from a loaded `prompt_text` entry in `references/motionsites-prompt-library.json`.

Before coding any page or section:

- Load every selected prompt with `scripts/load_lumora_prompt.py --id <prompt-id> --sha256`.
- Read the exact `prompt_text` emitted on stdout and treat it as the immutable build instruction for that page or section.
- Record the exact SHA256 emitted on stderr.
- Create a `lumora-manifest.json` in the generated site root before or during implementation.
- Include one `selected_prompts` entry per selected prompt with at least: `id`, `sha256`, `role`, `source`, and `loaded: true`.
- Run `scripts/verify_lumora_manifest.py --manifest <site-root>/lumora-manifest.json --output-root <site-root>` before reporting a build as Lumora.

The manifest is mandatory evidence, not decoration. A generated site without a valid `lumora-manifest.json` is not a Lumora site.

Hard stops:

- Do not write, scaffold, or implement a section before its exact `prompt_text` has been loaded and inspected.
- Do not create a section from a prompt ID, title, category, metadata, memory, vibes, previous outputs, or a hand-written approximation.
- Do not use `data-prompt-id` as proof by itself. `data-prompt-id` is only valid when the same ID exists in the manifest with a matching SHA256.
- Do not claim a section used a library prompt unless the exact prompt was loaded before coding and the section follows that prompt's structure, layout, components, motion, responsive behavior, and verification requirements.
- Do not call an output a Lumora test if any section was invented, approximated, rebuilt from taste, or merely inspired by a prompt.
- If a selected prompt cannot be implemented 1:1 after loading it, discard it and select another loaded prompt. Do not bridge the gap with original design.
- If time, context, tooling, or compatibility prevents exact prompt loading and implementation, stop and report that Lumora cannot honestly complete the build in that state.

## Scrape-First Completeness Rule

Before selecting prompts or coding, Lumora must build a **source inventory** and a **niche completeness blueprint**.

When a URL is provided, inspect the live or supplied website first. Scrape or browse enough pages to capture:

- navigation labels and page hierarchy
- whether the existing site is a onepager or multipage site, including all main routes/pages
- services, products, packages, pricing, guarantees, and booking rules
- contact data, address, opening hours, route, and location details
- proof points, reviews, testimonials, ratings, years, certifications, or guarantees
- imagery and media that can make the new site credible
- recurring copy tone, audience, and conversion intent
- legal, appointment, availability, or operational constraints that affect the website

When no URL is provided, build the inventory from the user's brief and clearly mark missing facts.

Then infer the required section blueprint for the niche before prompt selection. Do not let the prompt library decide site completeness by itself. Local service businesses usually need 8-14 meaningful sections, not a compact 3-section landing page. Ecommerce, SaaS, portfolios, venues, practices, agencies, restaurants, real estate, and local shops each need their own section count and section roles.

For a local photo studio, the default blueprint includes:

- Hero with primary service, location, rating/proof, and contact CTA
- Trust strip or fast facts
- Service overview
- E-passport/pass photo detail
- Application/business photo detail
- Portrait/family/baby/children detail or gallery
- Products such as albums, frames, prints, or gifts when sourced
- Pricing or package overview when sourced
- Process/how it works
- Reviews/testimonials or proof
- Location, opening hours, route, and phone
- FAQ
- Footer

Create a coverage matrix before coding with: `Required section`, `Source facts`, `Selected prompt id`, `Prompt family`, and `Status`. Aim for at least 85% of required niche sections covered. If coverage is lower, scrape more pages, pick a richer complete base, add compatible prompt sections, or report the missing source data instead of shipping a thin page.

Complete Landing Page / Website prompts are allowed only after the blueprint. A complete base may stand alone only if it covers the blueprint for that niche. A compact base such as `prisma-landing` is automatically incomplete for content-rich local businesses unless the blueprint proves otherwise.

## Functional Interaction And Multipage Rule

Every element that looks clickable must work. Do not ship dead UI.

For links and buttons:

- Do not leave `href="#"`, empty `href`, `javascript:void(0)`, placeholder routes, or buttons without actions.
- Navigation, footer, card, CTA, icon, social, legal, and utility links must point to real section IDs, real app routes, or real external URLs.
- Internal onepage links must scroll to existing sections.
- Internal multipage links must load existing routes/pages.
- Phone links use `tel:`, email links use `mailto:`, route links use a real map URL, and social links use real profiles when available.
- If a prompt visually requires a link but no real target exists, use the closest truthful internal target or convert it to non-clickable text only when that does not violate the selected prompt structure. Do not invent fake external URLs.
- Buttons must perform a concrete action such as route, scroll, call, mail, submit with feedback, open a modal/menu, change carousel state, or toggle an accordion.
- Forms must validate and show useful feedback or submit to a real available endpoint/action. They must not silently do nothing.

When the source website is multipage, the Lumora build must also be multipage. Preserve the main page structure discovered in the source inventory, such as `/passbilder`, `/bewerbung`, `/portrait`, `/kontakt`, or equivalent routes/pages. Each generated page must still be built from selected library prompt entries, with design and section structure locked 1:1. Do not collapse a real multipage source into a onepager unless the user explicitly requests a onepage redesign.

Multipage routing must be verified. All nav, footer, CTA, and card links between generated pages must resolve without 404s.

## Site-Wide Visual Cohesion Rule

Every generated website must feel like one coherent product, even when sections come from different prompt families. This is a mandatory token-mapping pass, not permission to invent new section designs.

After prompt selection and before coding, create a site cohesion sheet with:

- one global heading font family and one global body/UI font family, or one unified family when that fits better
- one shared type scale for headings, body, captions, buttons, numbers, and navigation
- one shared color token system for canvas, surface, ink, muted text, border, primary accent, secondary accent, focus, and destructive/success states when needed
- one background rhythm across the page or routes, including how light/dark/image sections transition
- one media treatment for overlays, image contrast, duotone/tint, grain, borders, or masks when those roles exist in the selected prompts

Apply the cohesion sheet globally:

- Do not let different sections import or use unrelated font families.
- Do not let each selected section keep an unrelated standalone palette.
- Map prompt-specified colors to the closest global color token by role, such as ink, surface, muted, accent, border, or canvas.
- Map prompt-specified font choices to the global font system while preserving hierarchy, weight contrast, size relationships, and text rhythm.
- Harmonize section background colors or background media so adjacent sections feel intentional, not accidental.
- Use shared CSS variables or equivalent theme tokens for fonts, colors, backgrounds, borders, shadows, focus states, and repeated surfaces.
- Use the same cohesion sheet across every route in a multipage build.

The cohesion sheet may change font family names, exact color values, and section background colors/media. It may not change layout, section structure, component structure, spacing logic, CTA placement, motion concept, responsive behavior, effects, or the selected prompt's content roles. If a selected prompt depends on a distinctive font/color treatment that cannot be mapped into the shared site identity without breaking its visual role, select a more compatible prompt instead of forcing the mismatch.

## Brand Token Discipline Rule

Before coding, extract a brand palette from the source website, logo, photos, visible signage, or user brief. If the source clearly has brand colors, those colors must dominate the site-wide cohesion sheet.

Create brand token evidence with:

- `brand_primary`, `brand_secondary`, `brand_neutral_dark`, `brand_neutral_light`, `canvas`, `surface`, `border`, `muted`, `focus`, and status colors when needed
- source evidence for each major brand color, such as logo, signage, existing CSS, or user statement
- allowed accent exceptions, with a reason tied to the selected prompt role or source brand

Apply the brand tokens globally:

- Use CSS variables or equivalent theme tokens for repeated colors. Avoid section-local hard-coded colors except when they directly reference a global token or are documented one-off states.
- Map prompt-specific colors into the brand token system by role. A prompt's warm, green, blue, purple, gold, or cream accent should become the closest brand role unless the source brand actually uses that color.
- Do not let imported prompt sections keep unrelated standalone palettes. If a section still reads as a different brand after token mapping, revise the token mapping or choose a more compatible prompt.
- For businesses with a clear two-color identity, such as white/red, make that identity visible across hero accents, CTAs, focus states, section transitions, media overlays, icons, and repeated surfaces.
- Neutral backgrounds should support the brand colors. Avoid drifting into unrelated cream, green, orange, blue, purple, or brown themes unless the source brand or selected prompt role requires it and the exception is documented.

Brand token discipline may change exact colors and backgrounds through the cohesion layer. It may not change section layout, component hierarchy, spacing logic, motion, or prompt-defined visual roles.

## Media Asset Discipline And Generation Rule

Prompt selection is design-led. Do not reject a strong, compatible, media-heavy prompt only because the scraped source images are too small, blurry, duplicated, or poorly cropped. Solve asset limitations through a required media preparation pass.

After prompt selection and before coding, create `lumora-media-plan.json` in the generated site root with one entry for every hero, card, gallery, background, video poster, or major decorative image. Each media slot must include:

- `id`, `prompt_id`, `section_id`, `role`, and `src`
- target render size or maximum expected render size: `target_width`, `target_height`
- required `aspect_ratio`, `fit`, and `focal_point`
- `source_type`: `source`, `enhanced`, `generated`, `icon`, `logo`, or `texture`
- whether the asset is meant to represent a real company place/person/product
- the asset treatment, such as crop, tint, overlay, grain, blur level, or duotone
- reuse policy, such as `allow_reuse: true` only for logos, icons, textures, repeated patterns, or an intentional prompt-specified repetition

Asset rules:

- Final bitmap media used in large cards or heroes should be at least 1.5x the target render width and height. Use 2x when practical for hero and full-bleed slots.
- Never stretch tiny source images into premium hero or card media. If a source image fails the size or sharpness requirement, find a larger original, enhance/upscale it, or generate a fit-for-slot replacement.
- Generated assets are allowed and preferred over downgrading prompt choice when source images cannot satisfy the selected media slots.
- Generated assets must be created for the exact slot role, aspect ratio, target size, focal point, and brand palette. Generate separate assets for materially different slots instead of reusing one image everywhere.
- Do not generate images that falsely imply they are real photos of the exact business premises, employees, customers, vehicles, certificates, or products unless the user provided those references or explicitly approved that representation. Use generic, staged, abstract, texture, or brand-world imagery for generated support visuals.
- Avoid embedded text, fake logos, fake signage, watermarks, distorted vehicles, warped tools, and unreadable UI inside generated images unless the slot explicitly requires a graphic texture and the artifacts are visually acceptable.
- Do not reuse the same non-logo image in adjacent prominent cards or multiple first-viewport media slots unless the selected prompt intentionally repeats it and the reuse is documented.
- Every `object-fit: cover` image must have a deliberate `object-position` or equivalent focal-point crop. Faces, vehicles, signs, logos, and primary tools should not be accidentally cut off.
- For contact pages and route heroes, verify that the image crop leaves room for forms, CTA buttons, and text on the tested desktop and mobile viewports.

Run `scripts/audit_lumora_visuals.py --site-root <site-root> --media-plan <site-root>/lumora-media-plan.json` before reporting a Lumora build. Treat failures as build failures unless the user explicitly accepts the visual risk.

## Responsive Containment And Sticky Safety Rule

Every generated website must prevent visual breakouts across desktop, tablet, and mobile. This is a mandatory responsive safety pass, not permission to redesign selected prompts.

Before finishing implementation, identify every selected prompt section that uses or implies:

- sticky, pinned, scroll-linked, parallax, stacking, or overlapping layouts
- full-height media, absolute-positioned media, carousels, masonry, wide grids, or galleries
- cards or media wrappers where child images, videos, canvases, or iframes can exceed the parent
- `height: 100%`, `position: sticky`, `position: fixed`, `position: absolute`, negative margins, transforms, or viewport-height sizing on major section elements

For those sections:

- Preserve the selected prompt's desktop design, structure, and motion as written whenever it is safe.
- Add breakpoint-specific containment so media and cards cannot spill over adjacent sections.
- Disable or convert desktop sticky, pinned, stacked, scroll-linked, or overlapping behavior into normal document flow on tablet/mobile when keeping it would cover other sections, trap scrolling, or create oversized media.
- Give images, videos, canvases, iframes, cards, and their parents stable dimensions with `aspect-ratio`, explicit `min-height`/`max-height`, grid constraints, or container-relative sizing before using `height: 100%`.
- Use `overflow: hidden` only on framed media/card wrappers where the prompt already treats the content as bounded. Do not use page-level clipping to hide broken content.
- Ensure no section visually covers, floats above, or obscures previous or next content except for prompt-specified intentional overlap that is bounded and verified.
- Ensure horizontal overflow is eliminated at every tested viewport.
- If the selected prompt's required desktop effect cannot be made responsive-safe without structural redesign, choose a different compatible prompt or report the incompatibility instead of shipping the broken section.

Responsive containment may adjust breakpoint behavior, container constraints, image fitting, overflow bounds, sticky activation, and mobile stacking only to prevent breakage. It may not introduce a new layout concept, new component structure, new visual effect, or freeform redesign.

## Non-Negotiable Verbatim Rule

For every selected library entry:

- Load the entry's exact `prompt_text`.
- Load it before coding starts, not afterward as documentation.
- Record its SHA256 in `lumora-manifest.json`.
- Treat that `prompt_text` as the direct build prompt.
- Preserve all specified design, layout, stack, component, animation, responsive, asset, and verification instructions exactly.
- Do not replace the prompt with an archetype summary, Lumora brief, design synthesis, mood board, or interpretation.
- Do not replace the loaded prompt with a prompt ID, title, report row, fake traceability marker, or `data-prompt-id` label.
- Do not omit prompt-specified sections, states, interactions, assets, animations, dimensions, or verification steps.
- Do not alter a prompt because another selected prompt has a nicer style or because the company context suggests a different direction.
- Do not harmonize multiple selected prompts by inventing new layouts, components, effects, motion, spacing, or arbitrary styles. Use only the required Site-Wide Visual Cohesion Rule for fonts, colors, backgrounds, and repeated visual tokens, plus the Responsive Containment And Sticky Safety Rule only where needed to prevent breakpoint breakage.
- Do not select a prompt unless its design, layout, structure, components, motion, and section order can be implemented as written.
- Do not keep a selected prompt in the report if the implementation is not actually built from that loaded `prompt_text`.
- Prompt-specified typography and color roles may be remapped only through the Site-Wide Visual Cohesion Rule.
- Prompt-specified responsive behavior must be preserved unless the minimum breakpoint-specific containment adjustment is required to prevent visual overlap, scroll trapping, horizontal overflow, or media breakout.
- Visible copy, brand names, labels, headings, product names, prices, testimonials, navigation, and CTA text may be localized to the requested language and sourced company facts, but only inside the same text roles and component slots specified by the selected prompt.

If exact prompts conflict in stack, global CSS, page shell, animation model, layout assumptions, or cannot share one coherent font/color/background token layer, do not patch over the conflict. Select a compatible complete page base, select a different compatible diverse section set, or stop and report that no compatible verbatim set exists.

## Page Base And Diverse Section Rule

Complete Landing Page / Website prompts are allowed. Treat them as a **base page**, not as the only possible answer.

Use the base page alone only when it already feels complete for the requested website, including:

- a strong Hero/Header
- the required niche-specific content sections from the coverage blueprint
- a clear closing, CTA, Contact, Footer, signup, booking, or equivalent conversion/ending

If a base page is not complete enough, such as a compact 3-section page like `prisma-landing`, keep its prompt body locked and add the missing blueprint sections from other compatible prompt entries.

For added sections, prefer variety:

- choose different prompt IDs
- choose different prompt families when practical
- infer a prompt family from the shared prefix, title, brand, or repeated package pattern, such as `arceage-*`, `nimbus-*`, `rocket-*`, `orbis-*`, `kova-*`, or similar
- avoid building most of the page from one family such as all `arceage-*`
- use at most two entries from the same family unless the library has no compatible alternative, and explain the exception
- never select the same prompt ID for every section

Do not:

- select the same prompt ID for every section
- fill all added sections from one prompt family when other compatible families exist
- add sections that require changing the locked design details of the base prompt beyond the permitted Site-Wide Visual Cohesion Rule

If the library lacks compatible diverse sections for an incomplete base page, report the limitation and use the strongest compatible fallback only when the result is still honest about what was selected.

## Source Of Truth

Use `references/motionsites-prompt-library.json` as the prompt library.

Each selected JSON entry is the single source of truth for that section's:

- design
- layout
- section structure
- section order within its role
- motion
- components
- visual direction
- spacing
- color roles, later mapped through the site cohesion sheet
- typography direction, later mapped through the site cohesion sheet
- CTA placement
- responsive behavior
- implementation style

Company context may guide prompt selection, visible copy localization, background/media replacement, and site-wide font/color token selection only. It must not change design, layout, visual style beyond the allowed cohesion layer, section structure, animation, component composition, conversion flow, responsive behavior, creative direction, stack, asset requirements, or verification criteria from the selected prompt_text.

## Standard Composition

When the user asks generally to build a website with Lumora, choose one of these shapes:

1. **Complete page base:** exactly 1 Landing Page / Website entry that already covers the niche blueprint, source inventory, and closing/conversion need.
2. **Page base + additions:** exactly 1 Landing Page / Website entry, plus as many compatible section entries as needed to cover the blueprint. Use the smallest set that reaches complete coverage; for content-rich local businesses this can be more than 3 added sections.
3. **Diverse section assembly:** no page base; assemble sections from multiple different prompt entries and families.

For a diverse section assembly, use:

- **Hero/Header:** exactly 1 existing library entry with a Hero/Header role or category.
- **Main Sections:** enough existing library entries to cover the blueprint, usually 4 to 10 for full websites, with roles such as About, Services, Categories, Features, Product, Story, Gallery, Benefits, Testimonials, Pricing, Process, Location, or similar content sections.
- **Closing:** exactly 1 existing library entry with Contact, Footer, CTA, Closing, Signup, Waitlist, Booking, or similar role.

If no suitable Footer section exists, use the closest Contact, CTA, or Closing entry.

Use different prompt IDs and prefer different prompt families. A complete Landing Page entry may be the whole site only when it satisfies the coverage matrix by itself. If it is incomplete, add missing compatible sections from other families. Do not improvise missing sections.

## Automatic Selection Rules

Select only entries that already exist in `references/motionsites-prompt-library.json`.

Use available JSON fields such as:

- `id`
- `title`
- `metadata.title`
- `metadata.category`
- `metadata.type`
- `metadata.page_type`
- `metadata.types`
- tags or similar metadata fields when present
- `prompt_text` content as the exact design and implementation instructions to copy into the build context and follow verbatim

Selection rules:

- Choose no entry without `prompt_text`.
- Use one existing entry per section role.
- Prefer no more than two entries from the same prompt family; never use one family for most sections when other compatible families exist.
- Copy every selected `prompt_text` 1:1 into the implementation reasoning/context before coding.
- Generate `lumora-manifest.json` with matching SHA256 values before declaring any output valid.
- Do not create new prompt entries.
- Do not create prompt files.
- Do not use `references/prompts`; it is not the prompt source.
- Do not merge prompt bodies into a new master prompt.
- Do not paraphrase, translate, shorten, expand, or summarize prompt bodies.
- Do not implement from memory, title, category, or archetype notes when `prompt_text` exists.
- If selection is uncertain, list plausible existing entries and still choose the technically strongest set with a short reason.
- If no matching verbatim-compatible section entry exists for an incomplete base, report the missing section role. Do not freely invent a section.
- In generated test websites, add `data-prompt-id="<id>"` to each section when practical so the source prompt remains traceable.

`data-prompt-id` is never sufficient evidence. It must match an entry in `lumora-manifest.json`, and the manifest SHA256 must match the exact library `prompt_text`. If manifest verification fails, the output is invalid and must not be presented as Lumora-built.

## Prompt Integrity

Never alter the stored prompt library or prompt bodies.

Do not:

- edit `references/motionsites-prompt-library.json`
- change any `prompt_text`
- copy prompt bodies into `.md` files
- rewrite prompt bodies
- translate prompt bodies
- shorten prompt bodies
- expand prompt bodies
- merge prompt bodies
- combine prompt fragments into a new prompt
- create a new Lumora brief
- create an original creative direction
- use company type as a reason to change design
- add missing design ideas from taste or preference

Lumora is allowed to place selected section implementations in sequence only when no glue design, copy rewriting, style translation beyond the required cohesion token mapping, or structural interpretation is required. That is section assembly, not prompt-body remixing.

Section assembly is allowed only when each selected prompt can remain structurally exact and can share the required site cohesion sheet. If assembling prompts requires changing global setup beyond shared theme tokens, stack, CSS prefixes, animation timing, media strategy, responsive behavior, or component structure from any selected `prompt_text`, assembly is forbidden.

## Copy Localization, Background, And Cohesion Adaptation

The only permitted adaptations are visible copy localization, changing section backgrounds/media, and applying the Site-Wide Visual Cohesion Rule.

Allowed copy localization:

- translate or rewrite visible website copy into the user's requested language, usually German for German businesses
- replace prompt example copy with company facts gathered from the source inventory
- preserve the same text role, approximate length, hierarchy, rhythm, CTA role, and layout footprint from the selected prompt
- keep every selected prompt section and component slot present

Allowed background changes:

- replace a prompt-specified background image or video with a company-relevant image or video of the same role and layout footprint
- change a section background color or background media when needed for brand relevance, asset availability, or whole-site cohesion
- keep overlays, contrast behavior, dimensions, border radii, layout, motion, and responsive behavior from the selected prompt intact

Allowed cohesion changes:

- use one global font system across every selected prompt section and route
- map prompt-specific colors into shared site tokens while keeping color roles, contrast, hierarchy, and component states intact
- normalize repeated surfaces, borders, focus rings, and background transitions through global CSS variables or equivalent theme tokens

Forbidden background-related changes:

- using background changes as a reason to alter section structure, spacing, typography hierarchy, component hierarchy, or motion
- replacing a required video/canvas/3D/background behavior with a static design unless the selected prompt allows it
- adding new visual concepts that are not in the selected prompt

## Forbidden Design Changes

Company context must not change:

- layout
- section count beyond the selected entry roles
- section order inside an entry
- visual hierarchy
- component structure
- CTA placement
- conversion flow
- motion concept
- design direction
- imagery style
- spacing
- color roles beyond the permitted site-wide token mapping
- typography hierarchy or direction beyond the permitted global font-family mapping
- responsive behavior beyond the minimum permitted responsive containment safety adjustments
- effects such as 3D, glassmorphism, gradients, bento grids, cards, marquees, glow, noise, blur, or parallax unless the selected prompt entry specifies them

## Workflow

1. Inspect the supplied URL or brief and create a source inventory before prompt selection.
2. Determine whether the source is onepage or multipage, including required routes/pages.
3. Infer the niche-specific completeness blueprint, including required section count and section roles.
4. Create a coverage matrix with `Required section/page`, `Source facts`, `Selected prompt id`, `Prompt family`, and `Status`.
5. Read `references/motionsites-prompt-library.json`.
6. Filter to entries with `prompt_text`.
7. Select either a complete Landing Page / Website base, a page base plus missing diverse sections, or a diverse Hero/Main/Closing section assembly that satisfies the coverage matrix. Selected added sections must use distinct prompt IDs and should come from different prompt families when practical.
8. Record each selected entry's `id`, title, role, prompt family, and why it was selected.
9. Load every selected `prompt_text` with `scripts/load_lumora_prompt.py --id <prompt-id> --sha256` before coding. This is mandatory for every selected prompt, not optional.
10. Copy each selected `prompt_text` into the working build context exactly as written and treat it as the immutable implementation prompt.
11. Create `lumora-manifest.json` in the generated site root with `selected_prompts` entries containing each prompt `id`, `sha256`, `role`, `source`, and `loaded: true`.
12. Create the site cohesion sheet for global fonts, type scale, brand color tokens, background rhythm, and repeated visual tokens.
13. Create `lumora-media-plan.json` and prepare source, enhanced, or generated assets for every major media slot. Do not downgrade prompt selection because source images are weak; make the assets fit the selected prompt.
14. Implement the website section by section and page by page. Each section remains locked to its selected loaded prompt entry.
15. Localize visible website copy to the requested language and company facts only inside the selected prompt's existing text roles and component slots.
16. Wire every clickable link, button, form, menu, accordion, carousel, and route to a real target or action.
17. Apply the responsive containment and sticky safety pass to sticky, pinned, stacking, overlapping, and media-heavy sections without changing the selected prompt's structure.
18. Add `data-prompt-id` to sections when practical.
19. Run `scripts/verify_lumora_manifest.py --manifest <site-root>/lumora-manifest.json --output-root <site-root>` and treat failure as a failed build.
20. Run `scripts/audit_lumora_visuals.py --site-root <site-root> --media-plan <site-root>/lumora-media-plan.json` and treat failure as a failed build unless the user explicitly accepts the visual risk.
21. Verify that the JSON library and prompt bodies did not change.
22. Verify source coverage, multipage routing when applicable, desktop/mobile layout, copy fit, media loading, responsive behavior, sticky/pinned/media containment, interactions, links/buttons/forms, global font/color/background cohesion, media slot sharpness/cropping/duplication, and console errors required by the selected prompt_text.

## Example Use

User: "Benutze den Lumora Skill und baue eine Website fuer Rheine's Greenhouse."

Expected behavior:

- Lumora inspects the supplied business context or existing website first.
- Lumora preserves multipage source sites as multipage builds.
- Lumora creates a niche-specific section blueprint and coverage matrix before picking prompts.
- Lumora opens `references/motionsites-prompt-library.json`.
- Lumora automatically selects either a complete page base or existing prompt entries for Hero, required content sections, proof, conversion, and Closing.
- Lumora loads and follows those selected entries' `prompt_text` bodies 1:1 before coding, records hashes in `lumora-manifest.json`, and rejects any section that only has a prompt ID label.
- Lumora creates one global cohesion sheet so every section shares the same font system, color tokens, and background rhythm.
- Lumora creates a media plan, uses fit-for-slot source/enhanced/generated assets, avoids duplicated prominent images, and preserves deliberate image focal points.
- Lumora localizes visible copy to Rheine's Greenhouse in German while preserving the selected prompt's exact design, section order, components, text roles, and layout footprint.
- Lumora wires every visible link and button to a real target/action and verifies routes, footer links, CTAs, forms, accordions, and carousels.
- Lumora verifies sticky, pinned, stacking, and media-heavy sections cannot overlap, spill out of their containers, or create horizontal overflow on desktop or mobile.
- Lumora reports the selected prompt IDs, prompt families, and coverage status.
- Lumora reports manifest verification status and never presents a fake traceability label as prompt usage.
- Lumora does not modify prompt bodies or the prompt library.

## Reference Files

- Read `references/composition-system.md` for the Lumora system.
- Use `references/archetype-catalog.md` only as inventory and role orientation for existing library entries.
- Use `scripts/load_lumora_prompt.py --id <prompt-id>` when an exact `prompt_text` needs to be emitted for inspection or hashing. Keep stdout as prompt text only.
- Use `scripts/verify_lumora_manifest.py --manifest <site-root>/lumora-manifest.json --output-root <site-root>` before reporting any generated site as Lumora-built.
- Use `scripts/audit_lumora_visuals.py --site-root <site-root> --media-plan <site-root>/lumora-media-plan.json` to enforce media slot size, duplicate media, focal point, generated-asset disclosure, and off-brand saturated color checks.
