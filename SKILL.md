---
name: lumora
description: Lumora builds premium websites from existing Lumora prompt_text entries in references/motionsites-prompt-library.json. Use when Codex is asked to build, redesign, improve, or generate a website, landing page, hero section, SaaS site, agency site, portfolio, ecommerce page, waitlist, signup page, presentation-like web page, or visually rich frontend using "$lumora" or "Lumora"; Lumora automatically selects existing library entries for hero, content sections, and closing while keeping design locked and adapting only visible website copy.
---

# Lumora

Lumora's default workflow is **Lumora**.

**Design locked. Copy adaptive.**

Use Lumora to build a website by selecting existing prompt entries from `references/motionsites-prompt-library.json`. Prompt bodies live in each entry's `prompt_text` field. Lumora selects existing entries by role and applies them section by section. It does not mean inventing a new design, creating new archetypes, or merging prompt bodies into a new prompt.

The bundled MotionSites prompt library is included under owner-approved commercial redistribution permission reported by the skill maintainer on 2026-06-12. See `references/permissions.md`. Treat all `prompt_text` values as licensed bundled resources. Do not edit, rewrite, summarize, translate, merge, or copy prompt bodies into new prompt files.

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

Company context may only change visible website copy. It must not change design, layout, visual style, section structure, animation, component composition, conversion flow, responsive behavior, or creative direction.

## Standard Composition

When the user asks generally to build a website with Lumora, assemble:

- **Hero/Header:** exactly 1 existing library entry with a Hero/Header role or category.
- **Main Sections:** 2 to 4 existing library entries with roles such as About, Services, Categories, Features, Product, Story, Gallery, Benefits, Testimonials, Pricing, or similar content sections.
- **Closing:** exactly 1 existing library entry with Contact, Footer, CTA, Closing, Signup, Waitlist, Booking, or similar role.

If no suitable Footer section exists, use the closest Contact, CTA, or Closing entry.

If a real multi-section composition is not sensible because the library only has complete landing-page templates for the requested need, use exactly one existing Landing Page entry and briefly explain why. Do not improvise missing sections.

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
- `prompt_text` content only for understanding the stored design instructions, not for rewriting

Selection rules:

- Choose no entry without `prompt_text`.
- Use one existing entry per section role.
- Do not create new prompt entries.
- Do not create prompt files.
- Do not use `references/prompts`; it is not the prompt source.
- Do not merge prompt bodies into a new master prompt.
- Do not paraphrase, translate, shorten, expand, or summarize prompt bodies.
- If selection is uncertain, list plausible existing entries and still choose the technically strongest set with a short reason.
- If no matching entry exists, stop or use one complete Landing Page entry. Do not freely invent a section.
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
3. Select a Hero/Header entry, 2 to 4 main section entries, and a Contact/Footer/CTA/Closing entry using existing metadata and role fit.
4. Record each selected entry's `id`, title, role, and why it was selected.
5. Read the selected `prompt_text` values as immutable design instructions.
6. Implement the website section by section. Each section remains locked to its selected prompt entry.
7. Adapt only visible website copy for the company context.
8. Add `data-prompt-id` to sections when practical.
9. Verify that the JSON library and prompt bodies did not change.
10. Verify desktop/mobile layout, copy fit, media loading, responsive behavior, interactions, and console errors.

## Example Use

User: "Benutze den Lumora Skill und baue eine Website fuer Rheine's Greenhouse."

Expected behavior:

- Lumora opens `references/motionsites-prompt-library.json`.
- Lumora automatically selects existing prompt entries for Hero, content sections, and Closing.
- Lumora builds a website from those selected entries.
- Lumora adapts only visible copy to Rheine's Greenhouse.
- Lumora does not modify prompt bodies or the prompt library.

## Reference Files

- Read `references/composition-system.md` for the Lumora system.
- Use `references/archetype-catalog.md` only as inventory and role orientation for existing library entries.
- Use `scripts/load_lumora_prompt.py --id <prompt-id>` when an exact `prompt_text` needs to be emitted for inspection or hashing. Keep stdout as prompt text only.
