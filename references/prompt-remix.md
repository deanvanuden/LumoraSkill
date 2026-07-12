# MotionSites Prompt Direction And Remixing

## Contents

1. Purpose
2. Anchor-led authority
3. Candidate inspection
4. Selecting the anchor
5. Selecting supporting donors
6. Compatibility review
7. Extracting source invariants
8. Translating the stack
9. Contribution and section ledger
10. Failure patterns
11. Source security

## Purpose

The MotionSites library contains detailed composition, media, interaction, motion, responsive, and conversion specifications. Lumora uses the full source bodies as creative engineering references. The index finds candidates; it does not replace reading the prompt.

Do not flatten a source into labels such as "luxury," "scroll," or "tabs." Extract the relationships that make the source work, then reinterpret those relationships through the selected company world.

## Anchor-Led Authority

Use one to three donors:

| Job | Authority | Controls | Must not control |
| --- | ---: | --- | --- |
| Anchor | 70-80% | experience world, page silhouette, first viewport, dominant media, section cadence, primary choreography | company facts, final brand copy, unsupported assets |
| Experience support | 10-20% | one bounded product, service, story, process, proof, gallery, or program mechanism | global shell, second hero, another world, another dominant scroll story |
| Conversion support | 10-15% | one purchase, booking, inquiry, signup, pricing, selector, or closing behavior | global visual identity or unrelated sections |

The company world outranks the anchor. The anchor outranks support donors. Use zero supporting donors when the anchor and original design decisions already solve the site.

Do not select a separate hero donor or motion donor by default. The anchor owns both so the opening, spatial system, media, and choreography stay coherent.

## Candidate Inspection

Run the planner, then inspect at least three anchor candidates from `source_selection.candidate_shortlists.anchor`.

The planner selects one anchor by default while still producing experience and conversion shortlists. Do not promote a support candidate until the selected world and content architecture expose a concrete unsolved need.

Commands:

```bash
python scripts/inspect_lumora_prompt.py --id <prompt-id> --full
python scripts/inspect_lumora_prompt.py --id <prompt-id> --focus layout,visual,media,motion,interaction,responsive
python scripts/inspect_lumora_prompt.py --id <prompt-id> --focus conversion,interaction,layout,responsive
```

For each anchor candidate record:

- native experience world and first-viewport subject
- page silhouette and chapter cadence
- dominant media role and required asset quality
- primary transformation or interaction
- typography-to-media relationship
- conversion path
- mobile and reduced-motion behavior
- static portability and dependency cost
- which parts can become company-specific
- which parts would remain visibly tied to the example brand

Read the selected anchor in full. Read support prompts in full when focused excerpts leave geometry, timing, or behavior ambiguous.

Do not choose from title, category, tags, screenshot mood, or planner score alone.

## Selecting The Anchor

Choose the anchor that can become the selected experience world without losing its strongest relationships.

An anchor is strong when:

- its native subject role can be replaced with the company's signature object or environment
- its media behavior matches assets that can actually be supplied or generated
- its broad composition can carry the company's information and conversion
- its dominant motion can embody the selected transformation
- its responsive behavior can preserve the experience on mobile
- it does not depend on an example-brand convention that conflicts with the company

An anchor need not come from the same business category. A museum, automotive, or editorial prompt may become a product or event site when the spatial and media relationships fit. Semantic distance is allowed; world incompatibility is not.

### Anchor Rejection

Reject an anchor when:

- it needs a media subject the project cannot credibly produce
- the example's visual identity is inseparable from its mechanics
- the page depends on a framework or runtime that cannot be translated without losing the concept
- its primary interaction conflicts with the real conversion
- its mobile fallback removes the central idea
- it would make the company look like a donor demo instead of itself

Record inspected and rejected candidates in `source_selection`.

## Selecting Supporting Donors

Add a support donor only after the anchor and creative world are chosen. Start from a concrete unsolved need:

- a product comparison needs a tactile selector
- a service process needs a clear state mechanism
- a project archive needs a bounded navigation pattern
- a ticket purchase needs a useful availability or package state
- an inquiry flow needs better progressive disclosure

Then inspect candidates for that need.

A support donor contributes one mechanic, not a second visual direction. Apply it to one or two sections and restyle its media, typography, controls, and motion into the anchor world.

If no donor improves the need without conflict, design the mechanism directly. Library coverage is not a success metric.

## Compatibility Review

The planner provides a preliminary score and risks. Perform a manual review after reading the prompts.

Score every proposed support donor from -2 to +2 on each axis:

| Axis | -2 | 0 | +2 |
| --- | --- | --- | --- |
| Semantic fit | Mechanic does not serve real content | Adaptable | Directly clarifies the content need |
| World/material | Requires another aesthetic world | Neutral after restyling | Extends the anchor material |
| Media | Needs unrelated assets | Can share treatment | Uses the same campaign family |
| Spatial authority | Tries to reorganize the page | Local and containable | Reinforces anchor geometry |
| Motion hierarchy | Adds another dominant interaction | Static or subordinate | Extends the same transformation |
| Responsive behavior | Breaks or disappears on mobile | Can recompose | Has a strong equivalent state |
| Conversion | Distracts from action | Neutral | Makes action clearer or more truthful |

Reject negative totals unless a written resolution removes the conflict. Resolve every risk in `compatibility_resolution`.

### Automatic Veto Conditions

Drop or replace a support donor when it:

- introduces a second hero
- introduces another pinned or scrubbed narrative that competes with the dominant interaction
- requires another material, lighting, or camera world
- introduces a second type or control language that cannot be absorbed
- adds autoplay that competes with user-controlled state
- depends on unavailable video, 3D, or interface evidence
- expands beyond two major sections
- exists only because the planner selected it

## Extracting Source Invariants

For every accepted source, extract concrete invariants.

### Composition

- relative scale between text, subject, controls, and continuation
- alignment, columns, overlap, crop, negative space, and section boundaries
- when the page changes density, background, or spatial mode

### Media

- subject role, aspect ratio, focal point, crop behavior, depth, and sequence
- whether media is evidence, atmosphere, product inspection, interface demonstration, archive, or transition
- what changes between desktop and mobile

### Interaction

- input: scroll, pointer, drag, tap, keyboard, time, device orientation, or form state
- state model and user control
- visible response and semantic purpose
- exit condition and restoration

### Motion

- ordering, timing relationships, progress mapping, easing, pinning, and settling behavior
- relationship between media movement and copy change
- reduced-motion and mobile alternatives

### Conversion

- when the action becomes relevant
- control hierarchy and selected state
- price, availability, package, booking, or form behavior
- truthful destination and error state

Preserve these relationships where they support the company world. Discard example copy, branding, decorative effects, remote media, and package lists.

## Translating The Stack

| Source instruction | Static Lumora translation |
| --- | --- |
| React component/state | semantic HTML plus scoped DOM state and event listeners |
| Vite root path such as `/images/x.webp` | page-correct relative `./assets/images/x.webp` path |
| Tailwind utilities | deliberate project CSS classes and custom properties |
| Framer Motion entrance | CSS or GSAP animation preserving visible timing and transform intent |
| Framer layout animation | FLIP-style transform or a simpler state transition preserving the relationship |
| GSAP/ScrollTrigger | pinned version through a static script when choreography needs it |
| React Three Fiber | direct Three.js module setup when the object or world truly needs 3D |
| component icon package | existing project icon library or an accessible familiar symbol |
| remote example image/video | supplied, sourced, generated, or edited company-specific local asset with the same role |
| SPA route | real relative `.html` route or same-page anchor |
| package-only widget | minimal truthful static equivalent or a different compatible donor |

Do not reproduce unused dependencies, build configuration, placeholder routes, fake data, or example-company content.

## Contribution And Section Ledger

The anchor needs at least three visible contributions and should control at least two sections. Each support donor needs at least one visible contribution and one bounded section.

```json
{
  "job": "experience",
  "id": "source-id",
  "authority": 0.15,
  "implemented_contributions": [
    "A three-state material comparison uses one persistent subject and tap-controlled labels"
  ],
  "implemented_sections": ["material-comparison"],
  "compatibility_resolution": "Removed the donor's glass styling and autoplay; kept only its state relationship inside the anchor's paper world."
}
```

Weak contribution: "luxury feel."

Strong contribution: "The product remains fixed at 60 percent width while three ingredient states replace the right-side evidence panel; mobile converts the relationship to a tap-controlled vertical sequence."

Mark every major HTML section with `data-lumora-source`. Include the anchor across the experience. Add support IDs only where their contribution is visible.

## Failure Patterns

### Donor Collage

Symptoms: every chapter uses a different effect, palette block, control, or motion system. Fix by returning authority to the anchor, removing support donors, and rebuilding transitions in one material language.

### Mechanical Translation

Symptoms: a solar day/night control becomes an unrelated event toggle, or a SaaS glass tab becomes a cultural program because both happen to use tabs. Fix by asking whether the source's native relationship has semantic meaning for the new content. If not, choose another mechanic.

### Library Theater

Symptoms: the plan names several prompts and maps them to sections, but the visible result is a generic site. Fix by extracting and implementing the actual spatial, media, and state invariants from the full source.

### Source Dominance

Symptoms: example-brand mood, assets, or copy structure remain more recognizable than the company. Fix by strengthening the company world, signature asset, and campaign system. Replace the anchor when its identity cannot be separated from its mechanics.

### Effect Accumulation

Symptoms: scroll scrub, autoplay tabs, drag gallery, cursor effect, word reveal, and page transition all demand attention. Fix by selecting one dominant interaction and converting the rest to subordinate or static states.

## Source Security

- Keep `references/motionsites-prompt-library.json` inside the skill.
- Never copy prompt bodies into website repositories, HTML comments, public JSON, screenshots, reports, or generated assets.
- Store only source IDs, hashes, contribution notes, compatibility decisions, and section mappings in `lumora-plan.json`.
- Never hotlink MotionSites preview or example media in customer sites.
