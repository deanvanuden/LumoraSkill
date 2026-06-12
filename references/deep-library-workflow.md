# Lumora Deep Library Workflow

Use this when a website should draw deeply from the bundled MotionSites prompt library instead of using the catalog as a loose mood board.

## Required Source Pack

For every new full website or landing page, run this before coding unless the user explicitly asks for a quick draft:

```bash
python scripts/compose_lumora_brief.py "<company and website brief>"
```

Use the output as the planning artifact. It selects source prompts, assigns them roles, and extracts normalized prompt atoms for layout, visual system, motion, conversion, implementation, and verification. It does not need to print full prompt bodies.

The source-pack step is not optional for normal Lumora website builds. If a run skips it, pause before coding and run the command.

Before creating or editing website files, produce these three visible planning blocks from the source pack:

1. **Source mix**: selected sources, their roles, and what each contributes.
2. **Merged atoms**: layout, visual, motion, conversion, and implementation atoms used for this build.
3. **Source-to-section map + media plan**: section jobs, source atoms per section, existing-media check, and imagegen fallback prompt inputs when needed.

If these blocks are not present, the Lumora planning step is incomplete.

## Prompt-Body Use

Treat source prompts as a pattern library:

- Extract reusable atoms: hero structure, section rhythm, motion technique, visual metaphor, asset direction, conversion component, responsive rule, and QA requirement.
- Transform atoms into a new brief matched to the current company. Do not copy source names, fake brands, or full prompt prose into the final website.
- Prefer a small source mix with clear roles over many half-used influences.
- Let one source drive market fit, one drive visual atmosphere, one drive information architecture, one drive conversion, and one or two fill motion or restraint gaps.
- If a source is only relevant for one atom, use only that atom.

## Source Mix Matrix

Before coding, decide:

| Role | What It Contributes | What To Avoid |
| --- | --- | --- |
| Market fit | Industry language, audience, offer framing, proof type | Borrowing the source company or claims |
| Visual engine | Main media idea, composition, type mood, color temperature | Combining multiple dominant visual metaphors |
| Information architecture | Section order and narrative pacing | Decorative sections with no job |
| Conversion pattern | CTA, form, package selector, booking, pricing, or cart behavior | Static buttons that imply unavailable flows |
| Motion system | Scroll, hover, reveal, cursor, or 3D behavior with purpose | Motion applied equally to everything |
| Restraint counterweight | Readability, whitespace, calmer components, accessibility | Flattening the one memorable visual idea |

## Section-Level Composition

Each major section should have a job and at least one source atom:

1. Hero: product/object/service recognition, proof, primary CTA, and next-section hint.
2. Mechanism: how the company creates the promised outcome.
3. Benefits/features: concrete capabilities or ingredients, not generic adjectives.
4. Proof: metrics, testimonials, work samples, compliance, outcomes, or operational evidence.
5. Conversion: package selector, lead form, waitlist, booking, checkout, or contact workflow.
6. Objection handling: FAQ, comparison, process, guarantee, security, or care notes.
7. Final CTA: compressed promise with one low-friction action.

Before creating files, write a short source-to-section map. Use this shape:

```text
Hero: <market fit source> + <visual engine source> -> recognition, proof, primary CTA, media crop.
Mechanism: <market fit source> + <information architecture source> -> explain how the outcome happens.
Proof: <information architecture source> + <restraint source> -> concrete evidence without clutter.
Conversion: <conversion source> -> functional selector/form/cart/booking/pricing state.
Motion: <motion source> -> only the interactions that clarify hierarchy or product behavior.
Final CTA: <conversion source> + <restraint source> -> objection handling and one low-friction action.
```

Add the media plan directly after the section map:

```text
Media plan:
- Existing media: <what repo/user media exists, or "none found">
- Imagegen fallback: <yes/no and why>
- Source basis: <market fit source> + <visual engine source>
- Asset direction: <subject, composition, negative space, desktop/mobile crop, overlay needs>
- Avoid: <text/watermarks/clutter/incorrect materials/etc>
```

## Build-Time Rules

- Start with asset direction. Use existing user/repo media first. If no suitable images, video, or product media are available and visual credibility matters, use the imagegen skill to generate project-bound assets before final layout tuning.
- Derive imagegen prompts from the source pack: subject, composition, negative space for copy, mobile crop, overlay contrast, material texture, lighting, aspect ratio, and avoid list. Avoid in-image text and watermarks unless the user provides exact required text.
- Encode interactions as real UI states: selected plan, open drawer, submitted form, active tab, expanded FAQ, paused motion, or hover/touch state.
- Keep the visual system specific: named type relationship, palette role, component geometry, spacing rhythm, image treatment, and motion timing.
- Use the prompt atoms to fill gaps after the first screenshot, not only before the first code pass.

## Screenshot Feedback Loop

After desktop and mobile screenshots:

- If the page feels generic, re-run the source pack with more specific industry and visual language.
- If the page feels overdesigned, add a restraint source and remove one visual atom.
- If conversion feels weak, add a source with a stronger form, package, booking, cart, or pricing pattern.
- If mobile feels like a compressed desktop page, prioritize mobile hero crop, touch targets, section order, and text density.
