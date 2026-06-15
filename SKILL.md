---
name: lumora
description: Lumora builds premium websites from exact prompt_text entries in references/motionsites-prompt-library.json, using either a complete landing-page prompt plus missing diverse section prompts or a diverse multi-section assembly. Use when Codex is asked to build, redesign, improve, or generate a website, landing page, hero section, SaaS site, agency site, portfolio, ecommerce page, waitlist, signup page, presentation-like web page, or visually rich frontend using "$lumora" or "Lumora"; Lumora must copy selected library prompt_text bodies 1:1, keep design locked, adapt only visible website copy, and avoid using many sections from the same prompt family.
---

# Lumora

Lumora's default workflow is **Locked Verbatim Page + Diverse Section Composition Mode**.

**Prompt bodies copied 1:1. Design locked. Copy adaptive. Complete pages allowed. Incomplete pages get extra diverse sections.**

Use Lumora to build a website by selecting existing prompt entries from `references/motionsites-prompt-library.json`. Prompt bodies live in each entry's `prompt_text` field. Every selected `prompt_text` must be loaded and used **verbatim, byte-for-byte in meaning and whitespace-sensitive content**, as the implementation instruction for its page or section. Lumora may select one complete Landing Page / Website entry as the base when it is the strongest fit. If that base page is incomplete for a real website, add missing sections from other prompt families. Lumora may also assemble a page from section-level prompts. It does not mean inventing a new design, creating new archetypes, paraphrasing prompts, or merging prompt bodies into a new prompt.

The bundled MotionSites prompt library is included under owner-approved commercial redistribution permission reported by the skill maintainer on 2026-06-12. See `references/permissions.md`. Treat all `prompt_text` values as licensed bundled resources. During a Lumora build, selected prompt bodies are copied 1:1 into the agent's working instructions and followed exactly. Do not edit, rewrite, summarize, translate, merge, or store prompt bodies in new prompt files.

## Non-Negotiable Verbatim Rule

For every selected library entry:

- Load the entry's exact `prompt_text`.
- Treat that `prompt_text` as the direct build prompt.
- Preserve all specified design, layout, stack, component, animation, responsive, asset, and verification instructions exactly.
- Do not replace the prompt with an archetype summary, Lumora brief, design synthesis, mood board, or interpretation.
- Do not omit prompt-specified sections, states, interactions, assets, animations, fonts, colors, dimensions, or verification steps.
- Do not alter a prompt because another selected prompt has a nicer style or because the company context suggests a different direction.
- Do not "harmonize" multiple selected prompts by inventing a shared design system.
- Do not select a prompt unless it can be implemented as written except for permitted visible copy adaptation.

If exact prompts conflict in stack, global CSS, page shell, animation model, or layout assumptions, do not patch over the conflict. Select a compatible complete page base, select a different compatible diverse section set, or stop and report that no compatible verbatim set exists.

## Page Base And Diverse Section Rule

Complete Landing Page / Website prompts are allowed. Treat them as a **base page**, not as the only possible answer.

Use the base page alone only when it already feels complete for the requested website, including:

- a strong Hero/Header
- at least two meaningful content sections
- a clear closing, CTA, Contact, Footer, signup, booking, or equivalent conversion/ending

If a base page is not complete enough, such as a compact 3-section page like `prisma-landing`, keep its prompt body locked and add missing sections from other compatible prompt entries.

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

Company context may only change visible website copy. It must not change design, layout, visual style, section structure, animation, component composition, conversion flow, responsive behavior, creative direction, stack, asset requirements, or verification criteria from the selected prompt_text.

## Standard Composition

When the user asks generally to build a website with Lumora, choose one of these shapes:

1. **Complete page base:** exactly 1 Landing Page / Website entry that already contains Hero, multiple content sections, and a closing/conversion end.
2. **Page base + additions:** exactly 1 Landing Page / Website entry, plus 1 to 3 extra compatible section entries from other prompt families when the base is missing enough content or a closing.
3. **Diverse section assembly:** no page base; assemble sections from multiple different prompt entries and families.

For a diverse section assembly, use:

- **Hero/Header:** exactly 1 existing library entry with a Hero/Header role or category.
- **Main Sections:** 2 to 4 existing library entries with roles such as About, Services, Categories, Features, Product, Story, Gallery, Benefits, Testimonials, Pricing, or similar content sections.
- **Closing:** exactly 1 existing library entry with Contact, Footer, CTA, Closing, Signup, Waitlist, Booking, or similar role.

If no suitable Footer section exists, use the closest Contact, CTA, or Closing entry.

Use different prompt IDs and prefer different prompt families. A complete Landing Page entry may be the whole site only when it is complete enough by itself. If it is incomplete, add missing compatible sections from other families. Do not improvise missing sections.

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

Lumora is allowed to place selected section implementations in sequence. That is section assembly, not prompt-body remixing.

Section assembly is allowed only when each selected prompt can remain exact. If assembling prompts requires changing global setup, stack, CSS prefixes, animation timing, media strategy, responsive behavior, or component structure from any selected `prompt_text`, assembly is forbidden.

## Copy Adaptation

The only permitted adaptation is user-facing website copy.

Copy may adapt to the company, offer, audience, location, brand tone, and factual details. Allowed copy fields include:

- Navigation labels
- Hero headline
- Hero subheadline
- CTA labels
- Section headlines
- Paragraphs
- Feature titles
- Feature descriptions
- Benefits
- Category names
- Product or service copy
- Form labels
- Form placeholders
- Footer copy
- Meta title
- Meta description
- Alt text
- Microcopy
- Badge text
- Testimonial copy, only when clearly treated as example or dummy content
- Pricing words, but not pricing layout

Copy must preserve the text role, approximate length, rhythm, tone, and layout footprint implied by the selected prompt entry. A short hero line stays short. A compact CTA stays compact. Minimal copy must not become long paragraphs. Copy must not break the intended layout, spacing, rhythm, or visual composition.

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

1. Read `references/motionsites-prompt-library.json`.
2. Filter to entries with `prompt_text`.
3. Select either a complete Landing Page / Website base, a page base plus missing diverse sections, or a diverse Hero/Main/Closing section assembly using existing metadata and role fit. Selected added sections must use distinct prompt IDs and should come from different prompt families when practical.
4. Record each selected entry's `id`, title, role, and why it was selected.
5. Load the selected `prompt_text` values with `scripts/load_lumora_prompt.py --id <prompt-id>` when exact inspection is needed; otherwise read them directly from JSON without alteration.
6. Copy each selected `prompt_text` into the working build context exactly as written and treat it as the immutable implementation prompt.
7. Implement the website section by section. Each section remains locked to its selected prompt entry.
8. Adapt only visible website copy for the company context.
9. Add `data-prompt-id` to sections when practical.
10. Verify that the JSON library and prompt bodies did not change.
11. Verify desktop/mobile layout, copy fit, media loading, responsive behavior, interactions, and console errors required by the selected prompt_text.

## Example Use

User: "Benutze den Lumora Skill und baue eine Website fuer Rheine's Greenhouse."

Expected behavior:

- Lumora opens `references/motionsites-prompt-library.json`.
- Lumora automatically selects either a complete page base or existing prompt entries for Hero, content sections, and Closing.
- Lumora loads and follows those selected entries' `prompt_text` bodies 1:1.
- Lumora adapts only visible copy to Rheine's Greenhouse.
- Lumora does not modify prompt bodies or the prompt library.

## Reference Files

- Read `references/composition-system.md` for the Lumora system.
- Use `references/archetype-catalog.md` only as inventory and role orientation for existing library entries.
- Use `scripts/load_lumora_prompt.py --id <prompt-id>` when an exact `prompt_text` needs to be emitted for inspection or hashing. Keep stdout as prompt text only.
