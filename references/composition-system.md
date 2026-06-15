# Lumora System

Use this reference when Lumora builds a website from `references/motionsites-prompt-library.json`.

**Prompt bodies copied 1:1. Design locked. Section structure locked. Copy may be localized to the requested language. A single site-wide typography/color/background token layer is mandatory for cohesion. Complete pages allowed. Incomplete pages get extra compatible sections only when every selected prompt remains structurally exact.**

Lumora selects existing JSON prompt entries and applies their `prompt_text` bodies as exact page or section prompts. Complete Landing Page / Website prompts are allowed as base pages. If a base page is incomplete, Lumora adds missing compatible sections from other prompt families. It is not free design mixing, prompt summarization, or creative synthesis. When multiple prompts are composed, Lumora must apply a site-wide cohesion layer so the final website feels like one brand instead of unrelated sections.

## Scrape-First Blueprint

Before prompt selection, inspect the supplied URL or business brief and create a source inventory. Capture navigation, page hierarchy, whether the source is onepage or multipage, services/products, pricing, guarantees, booking rules, address, phone, opening hours, proof, reviews, images, tone, and operational constraints.

Then define a niche-specific section blueprint. Do not let a nice-looking prompt decide completeness. Local service businesses usually need 8-14 meaningful sections. A local photo studio, for example, normally needs Hero, trust facts, service overview, E-pass/pass photo detail, application/business photo detail, portrait/family gallery, products such as albums or frames when sourced, pricing, process, reviews, location/hours/contact, FAQ, and Footer.

Create a coverage matrix before building:

- Required section
- Source facts
- Selected prompt id
- Prompt family
- Status

Target at least 85% blueprint coverage. If coverage is lower, scrape more, select a richer complete base, add compatible sections, or report the gap instead of shipping a thin page.

## Functional Interactions And Multipage

Every clickable element must work. Do not ship dead UI.

- Do not leave `href="#"`, empty `href`, `javascript:void(0)`, placeholder routes, or buttons without actions.
- Navigation, footer, card, CTA, icon, social, legal, and utility links must point to real section IDs, real app routes, or real external URLs.
- Internal onepage links must scroll to existing sections.
- Internal multipage links must load existing routes/pages without 404s.
- Phone links use `tel:`, email links use `mailto:`, route links use a real map URL, and social links use real profiles when available.
- If no real target exists for a visually required link, use the closest truthful internal target or convert it to non-clickable text only when that preserves the selected prompt structure. Do not invent fake external URLs.
- Buttons must perform concrete actions such as route, scroll, call, mail, submit with feedback, open a modal/menu, change carousel state, or toggle an accordion.
- Forms must validate and show useful feedback or submit to a real available endpoint/action.

When the source website is multipage, the Lumora build must also be multipage unless the user explicitly requests a onepage redesign. Preserve the main source routes/pages, and build each generated page from selected library prompt entries with design and section structure locked 1:1.

## Site-Wide Visual Cohesion

Every generated website must feel like one coherent product, even when sections come from different prompt families. This is a mandatory token-mapping pass, not permission to invent new section designs.

After prompt selection and before coding, create a site cohesion sheet:

- one global heading font family and one global body/UI font family, or one unified family when that fits better
- one shared type scale for headings, body, captions, buttons, numbers, and navigation
- one shared color token system for canvas, surface, ink, muted text, border, primary accent, secondary accent, focus, and status states when needed
- one background rhythm across the page or routes, including how light/dark/image sections transition
- one media treatment for overlays, image contrast, tint, grain, borders, or masks when those roles exist in the selected prompts

Apply the cohesion sheet globally:

- Do not let different sections import or use unrelated font families.
- Do not let each selected section keep an unrelated standalone palette.
- Map prompt-specified colors to the closest global color token by role, such as ink, surface, muted, accent, border, or canvas.
- Map prompt-specified font choices to the global font system while preserving hierarchy, weight contrast, size relationships, and text rhythm.
- Harmonize section background colors or background media so adjacent sections feel intentional.
- Use shared CSS variables or equivalent theme tokens for fonts, colors, backgrounds, borders, shadows, focus states, and repeated surfaces.
- Use the same cohesion sheet across every route in a multipage build.

The cohesion sheet may change font family names, exact color values, and section background colors/media. It may not change layout, section structure, component structure, spacing logic, CTA placement, motion concept, responsive behavior, effects, or the selected prompt's content roles. If a selected prompt depends on a distinctive font/color treatment that cannot be mapped into the shared site identity without breaking its visual role, select a more compatible prompt instead of forcing the mismatch.

## Responsive Containment And Sticky Safety

Every generated website must include a responsive safety pass for sticky, pinned, scroll-linked, stacking, overlapping, and media-heavy sections. This pass prevents visual breakouts; it is not permission to redesign selected prompts.

Before finishing, identify sections that use or imply sticky/pinned layouts, parallax, stacked cards, full-height media, absolute-positioned media, carousels, masonry, wide grids, galleries, `height: 100%`, viewport-height sizing, transforms, negative margins, or absolute/fixed/sticky positioning on major elements.

For those sections:

- Preserve the selected prompt's desktop design and structure whenever it is safe.
- Add breakpoint-specific containment so images, videos, canvases, iframes, cards, and wrappers cannot spill over adjacent sections.
- Use stable parent dimensions such as `aspect-ratio`, explicit `min-height`/`max-height`, grid constraints, or container-relative sizing before relying on `height: 100%`.
- Disable or convert sticky, pinned, stacking, scroll-linked, or overlapping desktop behavior into normal document flow on tablet/mobile when keeping it would cover other content, trap scrolling, or produce oversized media.
- Use `overflow: hidden` only on bounded framed media/card wrappers, not as page-level clipping to hide broken layout.
- Ensure no section visually covers previous or next content except prompt-specified intentional overlap that is bounded and verified.
- Ensure horizontal overflow is eliminated at every tested viewport.
- If the selected prompt's required effect cannot be made responsive-safe without structural redesign, choose a different compatible prompt or report the incompatibility.

Responsive containment may adjust breakpoint behavior, container constraints, image fitting, overflow bounds, sticky activation, and mobile stacking only to prevent breakage. It may not introduce a new layout concept, component structure, visual effect, or freeform redesign.

## Source

The prompt library is `references/motionsites-prompt-library.json`.

Prompt bodies live in each entry's `prompt_text` field. Select only entries that have `prompt_text`. During a build, copy every selected `prompt_text` 1:1 into the working implementation context and follow it exactly. Do not create prompt files, do not copy prompt bodies into `.md` files, and do not use `references/prompts` as a source.

## Composition Shape

Default website assembly chooses one of three shapes:

1. Complete page base: one Landing Page / Website prompt that already covers the niche blueprint and clear closing/conversion end.
2. Page base plus additions: one Landing Page / Website prompt plus as many compatible section prompts as needed to cover the blueprint.
3. Diverse section assembly: no page base; separate Hero, content, and Closing sections.

For a diverse section assembly:

1. One Hero/Header entry.
2. Enough main content entries to cover the blueprint, usually 4 to 10 for full websites.
3. One Contact/Footer/CTA/Closing entry.

Main content entries can include About, Services, Categories, Features, Product, Story, Gallery, Benefits, Testimonials, Pricing, or similar section roles.

If no Footer entry fits, use the strongest Contact, CTA, Signup, Waitlist, Booking, or Closing entry.

Selected entries must use different prompt IDs across the page. Added sections should come from different prompt families when practical. Infer family from shared prefix, title, brand, or repeated package pattern, such as `arceage-*`, `nimbus-*`, `rocket-*`, `orbis-*`, `kova-*`, or similar.

Avoid using most of the page from one prompt family such as all `arceage-*` when other compatible families exist. Use at most two entries from the same family unless there is no compatible alternative, and explain the exception.

A complete Landing Page / Website prompt may be the whole site only when it satisfies the coverage matrix by itself. If it is incomplete, add missing compatible sections from other families. If exact prompts conflict in stack, global CSS, page shell, animation model, layout assumptions, or cannot share one coherent font/color/background token layer, select a different compatible base or diverse section set, or stop and explain why. Do not invent missing sections.

## Selection Signals

Use existing JSON metadata only:

- `id`
- `title`
- `metadata.title`
- `metadata.category`
- `metadata.type`
- `metadata.page_type`
- `metadata.types`
- tags or similar metadata when present
- `prompt_text` as the exact section or page instructions to copy into the build context and follow verbatim

When selection is uncertain, list suitable existing entries and choose the technically strongest option. Do not invent a new archetype or creative direction.

Compact landing pages such as `prisma-landing` may be used as a base only after the blueprint, and they must be extended with missing compatible sections when they are not complete enough for the requested niche.

## Locked Section Rule

Each selected entry remains locked for its own section.

The selected entry determines that section's design, layout, structure, motion, components, visual direction, spacing, color roles, typography direction, CTA placement, responsive behavior, and implementation style. Color roles and font family choices are later mapped through the required site cohesion sheet.

The selected entry's `prompt_text` is the direct prompt. Do not replace it with a summary, transformed brief, archetype interpretation, or house style.

Do not:

- rewrite prompt bodies
- translate prompt bodies
- summarize prompt bodies
- shorten prompt bodies
- expand prompt bodies
- merge prompt bodies into a new prompt
- combine prompt fragments
- create a new Lumora brief
- create new archetypes
- invent a creative direction
- alter design based on company type
- harmonize designs by inventing new layouts, components, spacing, motion, effects, or arbitrary styles
- implement from memory, title, category, or metadata when `prompt_text` exists

Section assembly is allowed only when every selected prompt can remain structurally exact and can share the required site cohesion sheet. Prompt-body remixing is never allowed. A single landing-page prompt is acceptable only when it already satisfies the requested site shape.

## Copy Localization, Background, And Cohesion Adaptation

Company context may guide prompt selection, visible copy localization, section background/media replacement, site-wide font/color token selection, and minimum responsive containment safety adjustments only. It must not change design, layout, visual style beyond the allowed cohesion layer, section structure, animation, component composition, conversion flow, responsive behavior beyond the containment safety rule, creative direction, stack, asset requirements, or verification criteria from the selected prompt.

Allowed copy localization:

- translate or rewrite visible website copy into the user's requested language
- replace prompt example copy with source-inventory company facts
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

Forbidden changes include section structure, spacing logic, typography hierarchy beyond global font-family mapping, component hierarchy, motion, effects, and any visual concept not present in the selected prompt.

## Traceability

For generated test websites, add `data-prompt-id="<id>"` to each section when practical. Report selected IDs, titles, roles, and selection reasons at the end.

## Verification

Before finishing:

- Confirm the supplied URL or brief was inventoried before prompt selection.
- Confirm onepage vs multipage source structure was identified.
- Confirm a niche-specific section blueprint and coverage matrix were created.
- Confirm at least 85% of required blueprint sections are covered, or report why coverage is lower.
- Confirm all selected entries came from `references/motionsites-prompt-library.json`.
- Confirm every selected entry has `prompt_text`.
- Confirm every selected `prompt_text` was loaded and followed 1:1.
- Confirm a site cohesion sheet was created before coding.
- Confirm all sections and routes share one font system, color token system, and background rhythm.
- Confirm selected website sections use different prompt IDs.
- Confirm added sections avoid overusing one prompt family when compatible alternatives exist.
- If a complete Landing Page / Website prompt was used alone, confirm it already included enough content and a clear closing/conversion end.
- If a compact/incomplete page prompt such as `prisma-landing` was used, confirm missing sections were added from other compatible families.
- Confirm no prompt bodies changed.
- Confirm `references/motionsites-prompt-library.json` changed only if the user explicitly requested library maintenance.
- Confirm no prompt files or `references/prompts` folder were created.
- Confirm visible website copy localization stayed inside the selected prompt's existing text roles and component slots.
- Confirm any background/media adaptation stayed within the selected prompt's layout footprint.
- Confirm any font/color changes were only role-preserving site-wide cohesion token mapping.
- Confirm desktop/mobile layout, copy fit, media loading, interactions, responsive behavior, responsive containment, sticky/pinned/stacking section safety, and console errors.
- Confirm `scrollWidth <= clientWidth` at tested viewports and no media/card/section bounding box covers unrelated previous or next content.
- Confirm every clickable link/button/form/menu/accordion/carousel works.
- Confirm no dead links, placeholder links, empty buttons, or internal 404 routes remain.
- Confirm multipage routes load when the source was multipage.
