# Lumora System

Use this reference when Lumora builds a website from `references/motionsites-prompt-library.json`.

**Design locked. Copy adaptive.**

Lumora selects existing JSON prompt entries and applies them as section sources. It is not free design mixing.

## Source

The prompt library is `references/motionsites-prompt-library.json`.

Prompt bodies live in each entry's `prompt_text` field. Select only entries that have `prompt_text`. Do not create prompt files, do not copy prompt bodies into `.md` files, and do not use `references/prompts` as a source.

## Composition Shape

Default website assembly:

1. One Hero/Header entry.
2. Two to four main content entries.
3. One Contact/Footer/CTA/Closing entry.

Main content entries can include About, Services, Categories, Features, Product, Story, Gallery, Benefits, Testimonials, Pricing, or similar section roles.

If no Footer entry fits, use the strongest Contact, CTA, Signup, Waitlist, Booking, or Closing entry.

If a real multi-section composition is not sensible, use exactly one existing Landing Page entry and explain why. Do not invent missing sections.

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
- `prompt_text` only to understand the stored section instructions

When selection is uncertain, list suitable existing entries and choose the technically strongest option. Do not invent a new archetype or creative direction.

## Locked Section Rule

Each selected entry remains locked for its own section.

The selected entry determines that section's design, layout, structure, motion, components, visual direction, spacing, colors, typography direction, CTA placement, responsive behavior, and implementation style.

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

Section assembly is allowed; prompt-body remixing is not.

## Copy-Only Adaptation

Company context may only change visible website copy.

Allowed copy includes navigation labels, hero headline, hero subheadline, CTA labels, section headlines, paragraphs, feature titles, feature descriptions, benefits, category names, product or service copy, form labels, form placeholders, footer copy, meta title, meta description, alt text, microcopy, badge text, and pricing words.

Copy must preserve the role, approximate length, rhythm, tone, and layout footprint implied by the selected prompt entry. It must not break the original section composition.

## Traceability

For generated test websites, add `data-prompt-id="<id>"` to each section when practical. Report selected IDs, titles, roles, and selection reasons at the end.

## Verification

Before finishing:

- Confirm all selected entries came from `references/motionsites-prompt-library.json`.
- Confirm every selected entry has `prompt_text`.
- Confirm no prompt bodies changed.
- Confirm `references/motionsites-prompt-library.json` changed only if the user explicitly requested library maintenance.
- Confirm no prompt files or `references/prompts` folder were created.
- Confirm company context changed only visible copy.
- Confirm desktop/mobile layout, copy fit, media loading, interactions, responsive behavior, and console errors.
