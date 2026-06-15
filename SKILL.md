---
name: lumora
description: Lumora builds complete premium websites from exact prompt_text entries in references/motionsites-prompt-library.json after scraping or inventorying the target business, creating a niche-specific section blueprint, and then selecting a complete landing-page prompt or compatible prompt entries. Use when Codex is asked to build, redesign, improve, or generate a website, landing page, hero section, SaaS site, agency site, portfolio, ecommerce page, waitlist, signup page, presentation-like web page, or visually rich frontend using "$lumora" or "Lumora"; Lumora must use selected library prompt_text design, layout, structure, components, section order, and motion 100% 1:1 with no design interpretation, while allowing visible copy to be localized to the user's requested language and company facts.
---

# Lumora

Lumora's default workflow is **Locked Verbatim Page + Diverse Section Composition Mode**.

**Prompt bodies copied 1:1. Design locked. Section structure locked. Copy may be localized to the requested language. Complete pages allowed. Incomplete pages get extra compatible sections only when every selected prompt remains exact.**

Use Lumora to build a website by selecting existing prompt entries from `references/motionsites-prompt-library.json`. Prompt bodies live in each entry's `prompt_text` field. Every selected `prompt_text` must be loaded and used **verbatim, byte-for-byte in meaning and whitespace-sensitive content**, as the implementation instruction for its page or section. Lumora may select one complete Landing Page / Website entry as the base when it is the strongest fit. If that base page is incomplete for a real website, add missing sections from other families only when every selected prompt can remain exact without bridging, interpretation, or harmonization. Lumora may also assemble a page from section-level prompts. It does not mean inventing a new design, creating new archetypes, interpreting sections, inventing layout, or merging prompt bodies into a new prompt. Visible website copy may be localized to German or another requested language, but the prompt's text roles, rhythm, hierarchy, section order, and component slots stay locked.

The bundled MotionSites prompt library is included under owner-approved commercial redistribution permission reported by the skill maintainer on 2026-06-12. See `references/permissions.md`. Treat all `prompt_text` values as licensed bundled resources. During a Lumora build, selected prompt bodies are copied 1:1 into the agent's working instructions and followed exactly. Do not edit, rewrite, summarize, translate, merge, or store prompt bodies in new prompt files.

## Scrape-First Completeness Rule

Before selecting prompts or coding, Lumora must build a **source inventory** and a **niche completeness blueprint**.

When a URL is provided, inspect the live or supplied website first. Scrape or browse enough pages to capture:

- navigation labels and page hierarchy
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

## Non-Negotiable Verbatim Rule

For every selected library entry:

- Load the entry's exact `prompt_text`.
- Treat that `prompt_text` as the direct build prompt.
- Preserve all specified design, layout, stack, component, animation, responsive, asset, and verification instructions exactly.
- Do not replace the prompt with an archetype summary, Lumora brief, design synthesis, mood board, or interpretation.
- Do not omit prompt-specified sections, states, interactions, assets, animations, fonts, colors, dimensions, or verification steps.
- Do not alter a prompt because another selected prompt has a nicer style or because the company context suggests a different direction.
- Do not "harmonize" multiple selected prompts by inventing a shared design system.
- Do not select a prompt unless its design, layout, structure, components, motion, and section order can be implemented as written.
- Visible copy, brand names, labels, headings, product names, prices, testimonials, navigation, and CTA text may be localized to the requested language and sourced company facts, but only inside the same text roles and component slots specified by the selected prompt.

If exact prompts conflict in stack, global CSS, page shell, animation model, or layout assumptions, do not patch over the conflict. Select a compatible complete page base, select a different compatible diverse section set, or stop and report that no compatible verbatim set exists.

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
- add sections that require changing the locked design details of the base prompt

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
- colors
- typography direction
- CTA placement
- responsive behavior
- implementation style

Company context may guide prompt selection, visible copy localization, and background/media replacement only. It must not change design, layout, visual style, section structure, animation, component composition, conversion flow, responsive behavior, creative direction, stack, asset requirements, or verification criteria from the selected prompt_text.

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
- Do not create new prompt entries.
- Do not create prompt files.
- Do not use `references/prompts`; it is not the prompt source.
- Do not merge prompt bodies into a new master prompt.
- Do not paraphrase, translate, shorten, expand, or summarize prompt bodies.
- Do not implement from memory, title, category, or archetype notes when `prompt_text` exists.
- If selection is uncertain, list plausible existing entries and still choose the technically strongest set with a short reason.
- If no matching verbatim-compatible section entry exists for an incomplete base, report the missing section role. Do not freely invent a section.
- In generated test websites, add `data-prompt-id="<id>"` to each section when practical so the source prompt remains traceable.

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

Lumora is allowed to place selected section implementations in sequence only when no glue design, copy rewriting, style translation, or structural interpretation is required. That is section assembly, not prompt-body remixing.

Section assembly is allowed only when each selected prompt can remain exact. If assembling prompts requires changing global setup, stack, CSS prefixes, animation timing, media strategy, responsive behavior, or component structure from any selected `prompt_text`, assembly is forbidden.

## Copy Localization And Background Adaptation

The only permitted adaptations are visible copy localization and changing section backgrounds/media.

Allowed copy localization:

- translate or rewrite visible website copy into the user's requested language, usually German for German businesses
- replace prompt example copy with company facts gathered from the source inventory
- preserve the same text role, approximate length, hierarchy, rhythm, CTA role, and layout footprint from the selected prompt
- keep every selected prompt section and component slot present

Allowed background changes:

- replace a prompt-specified background image or video with a company-relevant image or video of the same role and layout footprint
- change a section background color or background media when needed for brand relevance or asset availability
- keep overlays, contrast behavior, dimensions, border radii, layout, motion, and responsive behavior from the selected prompt intact

Forbidden background-related changes:

- using background changes as a reason to alter section structure, spacing, typography, component hierarchy, or motion
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
- colors
- typography direction
- responsive behavior
- effects such as 3D, glassmorphism, gradients, bento grids, cards, marquees, glow, noise, blur, or parallax unless the selected prompt entry specifies them

## Workflow

1. Inspect the supplied URL or brief and create a source inventory before prompt selection.
2. Infer the niche-specific completeness blueprint, including required section count and section roles.
3. Create a coverage matrix with `Required section`, `Source facts`, `Selected prompt id`, `Prompt family`, and `Status`.
4. Read `references/motionsites-prompt-library.json`.
5. Filter to entries with `prompt_text`.
6. Select either a complete Landing Page / Website base, a page base plus missing diverse sections, or a diverse Hero/Main/Closing section assembly that satisfies the coverage matrix. Selected added sections must use distinct prompt IDs and should come from different prompt families when practical.
7. Record each selected entry's `id`, title, role, prompt family, and why it was selected.
8. Load the selected `prompt_text` values with `scripts/load_lumora_prompt.py --id <prompt-id>` when exact inspection is needed; otherwise read them directly from JSON without alteration.
9. Copy each selected `prompt_text` into the working build context exactly as written and treat it as the immutable implementation prompt.
10. Implement the website section by section. Each section remains locked to its selected prompt entry.
11. Localize visible website copy to the requested language and company facts only inside the selected prompt's existing text roles and component slots.
12. Add `data-prompt-id` to sections when practical.
13. Verify that the JSON library and prompt bodies did not change.
14. Verify source coverage, desktop/mobile layout, copy fit, media loading, responsive behavior, interactions, and console errors required by the selected prompt_text.

## Example Use

User: "Benutze den Lumora Skill und baue eine Website fuer Rheine's Greenhouse."

Expected behavior:

- Lumora inspects the supplied business context or existing website first.
- Lumora creates a niche-specific section blueprint and coverage matrix before picking prompts.
- Lumora opens `references/motionsites-prompt-library.json`.
- Lumora automatically selects either a complete page base or existing prompt entries for Hero, required content sections, proof, conversion, and Closing.
- Lumora loads and follows those selected entries' `prompt_text` bodies 1:1.
- Lumora localizes visible copy to Rheine's Greenhouse in German while preserving the selected prompt's exact design, section order, components, text roles, and layout footprint.
- Lumora reports the selected prompt IDs, prompt families, and coverage status.
- Lumora does not modify prompt bodies or the prompt library.

## Reference Files

- Read `references/composition-system.md` for the Lumora system.
- Use `references/archetype-catalog.md` only as inventory and role orientation for existing library entries.
- Use `scripts/load_lumora_prompt.py --id <prompt-id>` when an exact `prompt_text` needs to be emitted for inspection or hashing. Keep stdout as prompt text only.
