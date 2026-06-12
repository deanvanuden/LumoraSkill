# Lumora Composition System

Use this guide after selecting archetypes from `archetype-catalog.md`.

## Build The Mix

Choose 3-6 archetypes. Assign each a role:

- **Market fit**: proves the page understands the industry, audience, and conversion context.
- **Visual engine**: supplies the main visual metaphor, such as object focus, cinematic media, depth, scroll, 3D, glass, editorial type, or organic texture.
- **Information architecture**: supplies the section rhythm and narrative order.
- **Conversion pattern**: supplies signup, waitlist, booking, contact, ecommerce, pricing, demo, or trust behavior.
- **Restraint counterweight**: keeps the page usable when the visual engine is dramatic.

When the bundled prompt-body library is present, prefer running `scripts/compose_lumora_brief.py` before choosing manually. Use its source-pack output to see which prompt bodies contribute layout, visual, motion, conversion, and implementation atoms.

Example mix:
- For an AI automation agency: Modern Agency for service clarity, AI Workflow Hero for system orchestration, Scroll Landing Page for controlled motion, Build With Us for contact conversion.
- For a luxury real estate brokerage: Luxury Real Estate for market fit, SkyElite Private Jets for luxury pacing, Layered Depth for cinematic depth, Build With Us for lead capture.
- For a security SaaS: Securify Data Security for market fit, VaultShield for visual metaphor, Minimal Workflow SaaS for clarity, Datacore Booking for demo conversion.

## Convert Archetypes Into Original Directions

Write a short design brief with these fields:

1. **Concept**: one sentence describing the site as a product experience, not an aesthetic label.
2. **Archetype mix**: list selected archetypes and the specific role each plays.
3. **Hero**: headline strategy, primary proof point, CTA, visual anchor, motion behavior, and first-viewport composition.
4. **Sections**: 5-8 sections with clear jobs. Include proof, features, process, outcomes, trust, pricing/contact, and final CTA as needed.
5. **Visual system**: type scale, color relationship, spacing rhythm, surfaces, image/video/canvas/3D direction, iconography, and component geometry.
6. **Motion system**: state what moves, why it moves, and when it should stop. Use reduced-motion fallbacks.
7. **Responsive behavior**: mobile navigation, hero crop/stack, media constraints, touch targets, and text wrapping rules.
8. **Implementation notes**: stack-specific components, asset plan, performance constraints, and verification steps.

For deeper builds, add a **Source pack** field before the hero field:

- Market fit source and the industry/proof language it contributes.
- Visual engine source and the dominant media/composition idea it contributes.
- Information architecture source and the section rhythm it contributes.
- Conversion source and the functional UI state it contributes.
- Motion source and the reason motion belongs in the experience.
- Restraint source and the readability/accessibility guardrail it contributes.

## Common Prompt Atoms

Use these atoms to build original implementation briefs:

- **Editorial authority**: oversized headline, strong grid, restrained copy, confident whitespace.
- **Product object focus**: one inspectable visual anchor, simple background, measured parallax or rotation.
- **Cinematic reveal**: dark-to-light transition, video/image reveal, scroll pacing, strong scene composition.
- **Operational dashboard**: dense but calm panels, real data states, quiet color, repeatable workflow.
- **Luxury pacing**: fewer sections, larger photography/media, slower motion, high contrast, precise typography.
- **Technical trust**: diagrams, metrics, security proof, architecture cards, code/data artifacts.
- **Organic premium**: natural materials, soft motion, tactile imagery, asymmetric layout, low saturation.
- **Launch conversion**: single promise, social proof, waitlist/demo form, concise FAQ, repeated CTA.
- **Ecommerce ritual**: inspectable product media, package selector, usage steps, ingredient/proof detail, cart or checkout state.
- **Prompt-body extraction**: source prompt bodies are mined for reusable structure and implementation patterns, then rewritten for the current company.

## Section Patterns

Default full site sequence:

1. Hero with proof and primary CTA.
2. Problem or shift in the market.
3. Product/service mechanism.
4. Feature or offer grid.
5. Visual proof: dashboard, process, case study, or interactive demo.
6. Trust: metrics, logos, testimonials, security, press, or founder proof.
7. Pricing, package, waitlist, booking, or contact.
8. Final CTA with a compressed value proposition.

For product launches, shorten to hero, product proof, benefits, social proof, waitlist.

For service businesses, use hero, outcomes, services, process, case studies, team/proof, contact.

For portfolios, use hero, selected work, capability stack, process, about proof, contact.

## Visual Discipline

- Let one media idea dominate: video background, 3D object, editorial photography, data interface, or animated canvas.
- Use cards only for repeated items or actual framed tools. Do not nest cards.
- Prefer real or generated image/video/canvas assets when visual credibility matters.
- Keep text readable over media with deliberate overlays and contrast, not blur-heavy decoration.
- Avoid single-hue pages unless the brand requires it. Use neutrals plus one accent and one counter-accent.
- Keep hero-scale typography in the hero. Use compact type inside tool panels, nav, pricing, and dashboards.
- Define stable dimensions for boards, grids, toolbars, counters, tiles, and media frames.

## Motion Discipline

- Motion must explain hierarchy, reveal product behavior, or deepen the brand world.
- Use scroll-linked motion sparingly and verify it does not block reading.
- Keep continuous ambient motion subtle and pauseable through reduced-motion preferences.
- Avoid every element animating from opacity/translate at the same time.
- For 3D or WebGL, verify the canvas is nonblank, correctly framed, interactive or moving, and does not cover essential UI.

## Quality Checklist

Before finishing a Lumora build:

- Check desktop and mobile in a browser.
- Check console errors and failed asset requests.
- Verify hero content fits in the first viewport and hints at the next section.
- Verify no text overlaps, clips, or becomes unreadable.
- Verify CTAs are visible, enabled, and aligned with the requested business goal.
- Verify images/video/canvas/3D assets render and are not decorative noise.
- Revise CSS color balance if the page reads as a generic purple/blue SaaS gradient, beige luxury template, or dark slate dashboard by default.
- If the first pass is good but shallow, run `compose_lumora_brief.py` again with more specific industry, audience, conversion, and visual constraints, then add or replace one source atom at a time.
