# Lumora System

Use this reference when Lumora builds a website from `references/motionsites-prompt-library.json`.

**Prompt bodies copied 1:1. Design locked. Section structure locked. Copy may be localized to the requested language. Complete pages allowed. Incomplete pages get extra compatible sections only when every selected prompt remains exact.**

Lumora selects existing JSON prompt entries and applies their `prompt_text` bodies as exact page or section prompts. Complete Landing Page / Website prompts are allowed as base pages. If a base page is incomplete, Lumora adds missing compatible sections from other prompt families. It is not free design mixing, prompt summarization, or creative synthesis.

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

A complete Landing Page / Website prompt may be the whole site only when it satisfies the coverage matrix by itself. If it is incomplete, add missing compatible sections from other families. If exact prompts conflict in stack, global CSS, page shell, animation model, or layout assumptions, select a different compatible base or diverse section set, or stop and explain why. Do not invent missing sections.

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

The selected entry determines that section's design, layout, structure, motion, components, visual direction, spacing, colors, typography direction, CTA placement, responsive behavior, and implementation style.

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
- harmonize designs by inventing new colors, typography, spacing, motion, effects, or layouts
- implement from memory, title, category, or metadata when `prompt_text` exists

Section assembly is allowed only when every selected prompt can remain exact. Prompt-body remixing is never allowed. A single landing-page prompt is acceptable only when it already satisfies the requested site shape.

## Copy Localization And Background Adaptation

Company context may guide prompt selection, visible copy localization, and section background/media replacement only. It must not change design, layout, visual style, section structure, animation, component composition, conversion flow, responsive behavior, creative direction, stack, asset requirements, or verification criteria from the selected prompt.

Allowed copy localization:

- translate or rewrite visible website copy into the user's requested language
- replace prompt example copy with source-inventory company facts
- preserve the same text role, approximate length, hierarchy, rhythm, CTA role, and layout footprint from the selected prompt
- keep every selected prompt section and component slot present

Allowed background changes:

- replace a prompt-specified background image or video with a company-relevant image or video of the same role and layout footprint
- change a section background color or background media when needed for brand relevance or asset availability
- keep overlays, contrast behavior, dimensions, border radii, layout, motion, and responsive behavior from the selected prompt intact

Forbidden changes include section structure, spacing, typography, component hierarchy, motion, and any visual concept not present in the selected prompt.

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
- Confirm selected website sections use different prompt IDs.
- Confirm added sections avoid overusing one prompt family when compatible alternatives exist.
- If a complete Landing Page / Website prompt was used alone, confirm it already included enough content and a clear closing/conversion end.
- If a compact/incomplete page prompt such as `prisma-landing` was used, confirm missing sections were added from other compatible families.
- Confirm no prompt bodies changed.
- Confirm `references/motionsites-prompt-library.json` changed only if the user explicitly requested library maintenance.
- Confirm no prompt files or `references/prompts` folder were created.
- Confirm visible website copy localization stayed inside the selected prompt's existing text roles and component slots.
- Confirm any background/media adaptation stayed within the selected prompt's layout footprint.
- Confirm desktop/mobile layout, copy fit, media loading, interactions, responsive behavior, and console errors.
- Confirm every clickable link/button/form/menu/accordion/carousel works.
- Confirm no dead links, placeholder links, empty buttons, or internal 404 routes remain.
- Confirm multipage routes load when the source was multipage.
