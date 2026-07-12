# Lumora Motion And Experience Choreography

## Contents

1. Motion as meaning
2. Interaction hierarchy
3. Storyboard the dominant interaction
4. Distribute supporting motion
5. Scroll occupancy
6. Choosing input and transformation
7. Film, 3D, canvas, and shader choreography
8. Structural and micro motion
9. Implementation strategy
10. Responsive, touch, and reduced motion
11. Performance and failure recovery
12. Motion review gate

## Motion As Meaning

Motion should make a company truth visible. It may explain, inspect, compare, assemble, reveal, intensify, navigate, or transform. It should not exist merely because a donor prompt contains an effect.

Every meaningful animation should answer at least one question:

- What changed?
- What is connected?
- What should I inspect?
- What happens next?
- What is the difference between states?
- Where am I in the story?
- How does this mirror the company's product, craft, place, or culture?

Delete or subordinate motion that answers none of them.

There is no fixed maximum number of animations. Hierarchy matters more than count. A sophisticated experience may contain many local transitions, material responses, and media states while still having one unmistakable dominant interaction.

## Interaction Hierarchy

### Dominant Interaction

One memorable transformation owns the experience. It may span several chapters when they are consecutive beats of the same subject and narrative.

Examples:

- a venue access object is scanned, opens, and becomes the event program
- product layers assemble while material evidence and configuration become visible
- a real interface receives input, routes work, and resolves into output
- a building plan moves from drawing to material detail to inhabited space
- an ingredient or craft process changes physical state as the story advances

The dominant interaction can use scroll, drag, pointer inspection, typed input, time, camera movement, video, 3D, sound with consent, or a combination. Inputs must cooperate rather than compete.

### Structural Language

Use one family of recurring transitions to connect sections: mask, registration, focus, crop, depth, type baseline, paper edge, camera cut, interface state, or another world-specific behavior.

Structural motion should support rhythm and orientation. It must not become a second spectacle.

### Micro Interactions

Use responsive feedback for:

- navigation and menu state
- links and buttons
- selectors, tabs, accordions, filters, and galleries
- media controls
- forms, validation, errors, success, and disabled state
- keyboard focus and active selection

Micro motion should feel made from the same material and tempo as the larger experience.

The hierarchy is a constellation, not a hero demo followed by a static template. The dominant interaction sets the language; supporting, structural, and micro moments echo it with lower intensity through the rest of the journey.

## Storyboard The Dominant Interaction

Complete `motion_plan` before coding.

Define:

- `name`: a company-specific interaction name, not "scroll animation"
- `subject`: the object, interface, process, or environment that transforms
- `input`: what the visitor does
- `transformation`: the visible state change
- `narrative_purpose`: why this change matters
- `desktop_implementation`: exact spatial and technical behavior
- `mobile_recomposition`: equivalent idea for narrow and touch contexts
- `reduced_motion`: complete state without movement dependency

Write at least three visible choreography beats:

```json
{
  "beat": "The scanner recognizes the access band",
  "trigger": "Chapter progress reaches the first registration mark",
  "visible_change": "A narrow scan line reveals the event date inside the band while the surrounding street scene remains stable",
  "exit_condition": "Date, venue, and ticket state are fully readable before the next beat starts",
  "fallback": "The band, date, and venue render together as a static editorial frame"
}
```

Each beat must have a visible change and a legible settled state. Do not animate continuously without moments the visitor can understand.

## Distribute Supporting Motion

Plan at least two authored supporting moments in distinct later chapters. They are not additional spectacles. Each should reuse one property of the dominant language: subject, material response, crop, registration, camera behavior, depth, route, assembly, scan, focus, or state transition.

Record for every supporting moment:

- section and subject
- page and stable section ID
- trigger or user input
- exact visible change
- narrative or orientation purpose
- desktop implementation
- mobile implementation
- reduced-motion state

Build a `continuity_map` from entry through orientation, deepening, evidence, decision, and close. It should explain how motion intensity rises, settles, and returns, and how the signature motif remains visible. A generic IntersectionObserver fade-up may reveal ordinary copy, but it does not count as a supporting moment.

Mark each implemented target section with `data-lumora-motion="<meaningful-name>"` so the plan can be traced to shipped code.

Strong distribution examples:

- the hero assembles a product, later ingredient cutouts align to the same joints, and the package selector closes the assembly
- the entry scans a ticket, later program rows register on the same scan line, and the checkout state prints the final access mark
- the opening moves through a building plan, later material images focus at plan coordinates, and contact completes the route

Weak distribution includes unrelated countups, magnetic buttons, marquee text, parallax, and cursor effects added only to make the page feel animated.

## Scroll Occupancy

Long, pinned, sticky, or scrubbed chapters are allowed when every viewport of travel earns its space.

For each viewport-equivalent segment ask:

- What new subject state becomes visible?
- What information becomes readable?
- What spatial relationship changes?
- Has the previous state settled before the next begins?
- Does the scene still have a focal point?
- Is the page progressing, or only consuming scroll distance?

Avoid spacer-only travel, hidden text that waits too long to resolve, and pinning that leaves most of the viewport empty.

Record `long_scroll_justification` when a CSS track reaches roughly 240vh or more. This is not a hard limit; it is a requirement to explain and verify the visual beats.

### Pinned Chapters

- use a stable parent with a deliberate height or ScrollTrigger end condition
- keep one dominant subject visible and framed throughout
- prevent unrelated next or previous sections from overlapping
- define exact start, settle, and release states
- avoid a second pinned narrative elsewhere unless it is visibly part of the same interaction
- disable or recompose pinning when mobile flow becomes fragile

### Horizontal Movement

Use horizontal movement when sequence, archive, route, comparison, or spatial continuity benefits from it. Maintain orientation, progress, keyboard access, and touch behavior. Do not convert vertical scroll to a long horizontal gallery merely for novelty.

### Text Reveals

Reveal text when its timing supports reading or transformation. Avoid long word-by-word opacity or blur scrubs that create empty pages in full-page captures, hide essential information, or compete with media. Keep semantic text present in the DOM and visible without animation.

## Choosing Input And Transformation

| Company truth | Strong input/behavior candidates | Weak default |
| --- | --- | --- |
| Physical product | inspect, rotate, configure, compare, apply, assemble, reveal material | floating object over glow |
| Service or process | handoff, route, stamp, sequence, before/after, evidence progression | icon cards with fade-up |
| SaaS/interface | real typed input, state change, guided workflow, data relationship | fake dashboard parallax |
| Place/hospitality | day/night, route, room movement, menu ritual, environmental film | generic atmospheric autoplay |
| Culture/event | access, program, sound or poster behavior, archive navigation, ticket state | endless marquees and giant type |
| Portfolio/studio | crop transition, project inspection, case-study chapter, process artifact | equal cards and hover gimmicks |
| Architecture | plan-to-space, material focus, model inspection, route through project | decorative line drawing |
| Professional trust | evidence chain, clause, decision state, risk comparison, expert process | count-up metrics |
| Automotive/spatial | real model inspection, engineering assembly, configuration consequence | spinning primitive |

Use the donor prompt's exact choreography as technical evidence only after the semantic relationship fits.

## Film, 3D, Canvas, And Shader Choreography

### Video

Use video when time, environment, performance, transformation, or craft is the subject.

- keep video local and compressed
- provide a useful poster and still fallback
- use `muted` and `playsinline` for autoplay
- provide controls for nonessential or audio media
- pause when offscreen or the page is hidden
- avoid looping a moment whose visible jump destroys the world
- use object position and responsive sources intentionally

A background video must reveal something the still version cannot. Do not use an unrelated mood loop.

### Three.js And WebGL

Use 3D when the user benefits from an inspectable object, material, assembly, environment, model, or spatial relationship.

- make the scene full-bleed or structurally integrated, not a decorative card preview
- use real geometry or a credible generated model, not default primitives as finished art
- define camera framing for desktop and mobile
- use physically coherent material and lighting
- include loading, error, static-poster, and reduced-motion states
- pause or lower work when offscreen
- test that the canvas is nonblank and subject pixels occupy the intended region
- keep controls purposeful; do not expose orbit controls unless inspection benefits from them

Static GitHub Pages can host Three.js modules, models, textures, and HDR assets. Pin one library version and one import source.

### Canvas And Shaders

Use canvas or shaders for concept-specific material behavior, generative systems, particles derived from real data, image displacement, fluid material, or spatial transition.

- provide a noncanvas fallback
- avoid high-DPI overdraw and unbounded particle counts
- stop requestAnimationFrame work when hidden or offscreen
- respond to resize without reallocating every frame
- keep pointer behavior optional on touch
- ensure text and controls remain HTML when accessibility or sharpness requires it

Decorative noise, arbitrary particles, and gradient blobs are not sufficient concepts.

### Sound

Use sound only when central to the company experience and acceptable to the user. Never autoplay audible media. Provide explicit controls, clear state, keyboard access, and a complete silent experience.

## Structural And Micro Motion

### Timing

Derive tempo from the company world. Precision may use short settled transitions; ceremony may use slower reveals; nightlife may use impact and release; a product ritual may use viscous or layered movement.

Use consistent easing families and durations. Do not use a different spring, overshoot, and blur style for every component.

### Hover

Hover may reveal media, preview a route, inspect detail, or intensify a control. Every important hover behavior needs a tap, focus, or always-visible equivalent.

### Buttons And Links

Use transform, color, fill, underline, icon displacement, mask, or material response appropriate to the world. Preserve stable dimensions and at least 44 by 44 CSS-pixel touch targets.

### Menus

Menus may be minimal, spatial, editorial, or immersive. They must still expose current page, close behavior, focus order, escape handling, body-scroll policy, and mobile-safe navigation.

### Forms

Animate state changes only after behavior is truthful. Show loading, inline error, successful external submission, and disabled state without false confirmation.

## Implementation Strategy

For advanced static choreography, GSAP and ScrollTrigger are appropriate:

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js"></script>
```

Pin exact versions. Register plugins explicitly.

Use `gsap.matchMedia()` for desktop, mobile, coarse pointer, and reduced-motion setups. Keep teardown functions for timelines, observers, requestAnimationFrame loops, event listeners, and media.

Prefer:

- transform and opacity for continuous motion
- clip-path or masks when bounded and tested
- shader uniforms for canvas effects
- CSS custom properties updated inside requestAnimationFrame for pointer response
- IntersectionObserver for simple visibility state
- native scroll unless interpolation materially improves the concept

Avoid:

- continuous layout animation of top, left, width, height, or expensive filters
- broad `transition: all`
- permanent `will-change` on many elements
- large backdrop filters on scrolling content
- scroll listeners that force layout on every event
- multiple libraries controlling the same transform
- hidden overflow used to conceal layout defects

Smooth scrolling is optional. If used, pin the version, integrate one frame loop, preserve anchors and keyboard input, and disable it when it harms touch or reduced motion.

## Responsive, Touch, And Reduced Motion

Every dominant interaction needs three intentional implementations.

### Desktop

Use the full spatial, film, 3D, or scroll concept with stable framing and visible settled states.

### Mobile

Recompose rather than shrink:

- convert fragile pinning to explicit vertical states
- replace hover inspection with tap or swipe
- simplify camera movement while preserving the subject and transformation
- use alternate crops or assets
- keep controls reachable and content in normal flow
- avoid fixed UI covering the focal subject or CTA

Complete `motion_plan.mobile_signature` as its own implementation contract. Choose a real input such as scroll, tap, swipe, drag, time, or a bounded hybrid; name the subject and visible change; define implementation, fallback, and browser evidence.

Do not treat mobile as reduced motion. Outside the user's reduced-motion preference, these are failures:

- setting the dominant progress directly to `1`
- activating every hero state at load
- replacing the transformation with one static desktop image
- making the media extremely tall so the entire desktop composition can fit
- requiring hover or precise pointer input

Use a shorter scroll track, discrete snap states, tap/swipe progression, a safe autoplay sequence with controls, or a mobile-specific crop and camera path. Keep media within deliberate width, aspect-ratio, and viewport-height bounds. The interaction may be simpler, but the company-specific visible change must still occur.

Mobile can use a different interaction if it expresses the same thesis more clearly.

### Reduced Motion

- expose all content immediately
- remove scrub, parallax, autoplay, large camera movement, and disorienting transitions
- show a complete representative state for video, canvas, and 3D
- preserve short opacity or color feedback where useful
- never require animation to understand or reach content

## Performance And Failure Recovery

- Keep the base document readable before JavaScript initializes.
- Load advanced libraries after critical structure where practical.
- Reserve stable dimensions for media, canvas, controls, and dynamic text.
- Pause video, canvas, 3D, and perpetual loops when offscreen or hidden.
- Limit texture, model, video, and raster size to the visible role.
- Avoid loading desktop and mobile media variants simultaneously.
- Handle missing libraries and failed assets by exposing static content, not blank scenes.
- Remove dev overlays and console errors.
- Test CPU and memory behavior during the full scroll, not only at load.

## Motion Review Gate

Before implementation:

- dominant interaction subject, input, transformation, and purpose are locked
- at least three visible beats have settled states and fallbacks
- structural and micro languages are defined
- competing donor systems were removed
- desktop, mobile, reduced-motion, and dependency-failure paths exist
- at least two distinct supporting moments and the entry-to-close continuity map are written

Before delivery:

- every scroll viewport has visible content or change
- the dominant interaction is unmistakable
- no autoplay, drag, marquee, cursor, or secondary scrub competes with it
- content remains readable during and after animation
- mobile preserves the thesis
- the mobile signature actually changes state under touch-sized browser verification and is not forced to its final state
- at least two later chapters visibly continue the dominant motion language; the rest of the site is not generic reveal-only motion
- reduced motion exposes the complete experience
- there are no blank canvases, stuck pins, overlap, layout shift, or failed cleanup
- performance remains stable across the full page and route transitions
