# Lumora System

Use this reference when Lumora builds a website from `references/motionsites-prompt-library.json`.

**Prompt bodies copied 1:1. Design locked. Copy adaptive. Complete pages allowed. Incomplete pages get extra diverse sections.**

Lumora selects existing JSON prompt entries and applies their `prompt_text` bodies as exact page or section prompts. Complete Landing Page / Website prompts are allowed as base pages. If a base page is incomplete, Lumora adds missing compatible sections from other prompt families. It is not free design mixing, prompt summarization, or creative synthesis.

## Source

The prompt library is `references/motionsites-prompt-library.json`.

Prompt bodies live in each entry's `prompt_text` field. Select only entries that have `prompt_text`. During a build, copy every selected `prompt_text` 1:1 into the working implementation context and follow it exactly. Do not create prompt files, do not copy prompt bodies into `.md` files, and do not use `references/prompts` as a source.

## Composition Shape

Default website assembly chooses one of three shapes:

1. Complete page base: one Landing Page / Website prompt that already includes Hero, multiple content sections, and a clear closing/conversion end.
2. Page base plus additions: one Landing Page / Website prompt plus 1 to 3 extra compatible section prompts from other prompt families when the base is incomplete.
3. Diverse section assembly: no page base; separate Hero, content, and Closing sections.

For a diverse section assembly:

1. One Hero/Header entry.
2. Two to four main content entries.
3. One Contact/Footer/CTA/Closing entry.

Main content entries can include About, Services, Categories, Features, Product, Story, Gallery, Benefits, Testimonials, Pricing, or similar section roles.

If no Footer entry fits, use the strongest Contact, CTA, Signup, Waitlist, Booking, or Closing entry.

Selected entries must use different prompt IDs across the page. Added sections should come from different prompt families when practical. Infer family from shared prefix, title, brand, or repeated package pattern, such as `arceage-*`, `nimbus-*`, `rocket-*`, `orbis-*`, `kova-*`, or similar.

Avoid using most of the page from one prompt family such as all `arceage-*` when other compatible families exist. Use at most two entries from the same family unless there is no compatible alternative, and explain the exception.

A complete Landing Page / Website prompt may be the whole site only when it is complete enough by itself. If it is incomplete, add missing compatible sections from other families. If exact prompts conflict in stack, global CSS, page shell, animation model, or layout assumptions, select a different compatible base or diverse section set, or stop and explain why. Do not invent missing sections.

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

Compact landing pages such as `prisma-landing` may be used as a base, but they must be extended with missing compatible sections when they are not complete enough for the requested website.

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
- Confirm every selected `prompt_text` was loaded and followed 1:1.
- Confirm selected website sections use different prompt IDs.
- Confirm added sections avoid overusing one prompt family when compatible alternatives exist.
- If a complete Landing Page / Website prompt was used alone, confirm it already included enough content and a clear closing/conversion end.
- If a compact/incomplete page prompt such as `prisma-landing` was used, confirm missing sections were added from other compatible families.
- Confirm no prompt bodies changed.
- Confirm `references/motionsites-prompt-library.json` changed only if the user explicitly requested library maintenance.
- Confirm no prompt files or `references/prompts` folder were created.
- Confirm company context changed only visible copy.
- Confirm desktop/mobile layout, copy fit, media loading, interactions, responsive behavior, and console errors.
