# Lumora Media And Motion

## Contents

1. Media hierarchy
2. Image generation
3. Video and 3D
4. Motion hierarchy
5. Effect selection
6. Implementation and performance
7. Responsive and reduced motion

## Media Hierarchy

Treat media as content architecture. Define every major slot before generation or sourcing:

```json
{
  "id": "hero-product",
  "role": "dominant product still",
  "page": "index.html",
  "aspect_ratio": "4:5",
  "target_render": "820x1025",
  "focal_point": "bottle cap at 58% x, 32% y",
  "text_safe_area": "left 42%",
  "source": "generated",
  "truthfulness": "fictional campaign image; no real-person or clinical claim",
  "reuse": "hero and product detail only"
}
```

Use project-local files. Size hero and full-width raster media for roughly twice their largest render dimensions when practical. Use AVIF or WebP for photography with a reasonable fallback when support or source quality requires it. Give every `object-fit: cover` slot an intentional `object-position`.

Do not reuse one non-logo image in adjacent prominent sections. Do not use low-resolution source media as full-bleed content.

## Image Generation

Generate a visual reference before coding when the user provides no strong design reference and visual quality is central. Generate final assets separately from the reference comp.

Each final asset prompt must specify:

- exact subject and its relationship to the company
- slot role and aspect ratio
- camera distance, angle, lens character, and focal point
- lighting, material, palette, and environment
- text-safe area and crop behavior
- whether the background should be transparent, isolated, environmental, or full-bleed
- consistency requirements shared with the other site assets
- negative constraints: no readable text, no fake logo, no watermark, no extra products, no anatomy errors, no irrelevant props

Generate different compositions for different aspect ratios. Cropping one image into every slot is not art direction.

Prefer real or generated bitmap media over CSS illustrations made from circles, blobs, gradients, or pseudo-elements. CSS is appropriate for interface chrome, layout, masks, lines, and restrained textures, not for pretending to be campaign art.

## Video And 3D

Use video when time, transformation, craft, environment, or product behavior is the subject. A background video must be local, compressed, muted, looping only when appropriate, `playsinline`, and have a useful poster. Do not autoplay audio.

Use Three.js only when the visitor benefits from inspecting or manipulating a real object, spatial scene, product, model, or data relationship. A decorative spinning primitive is not enough. Provide a static poster fallback and verify that the canvas is nonblank and correctly framed.

If video or 3D cannot be sourced or generated credibly, use a strong still-image sequence, before/after control, layered crop reveal, or editorial gallery instead.

## Motion Hierarchy

Budget the page around three layers:

1. Signature motion: one memorable company-specific sequence.
2. Structural motion: one reveal language reused with restraint.
3. Micro motion: feedback for actionable elements.

A normal marketing page rarely needs more than one pinned sequence, one marquee or horizontal section, and one reveal system. Do not combine scroll lock, smooth-scroll hijacking, multiple pinned chapters, cursor replacement, particle fields, and perpetual card motion on the same page.

Motion must answer at least one question:

- What changed?
- What is connected?
- What should I inspect?
- What happens next?
- What is the difference between two states?
- Where am I in the story?

Delete motion that answers none of them.

## Effect Selection

| Company/content | Strong candidates | Weak default |
| --- | --- | --- |
| Physical product | controlled rotation, material close-up, ingredient/component layers, size or variant selector, scroll-linked assembly | floating product over glow |
| Service/process | bounded pinned chapters, path progress, before/after comparison, evidence reveal | generic icon cards |
| Portfolio/studio | project crop transitions, horizontal gallery, hover preview, case-study chapter stack | equal project cards |
| Hospitality/place | cinematic environmental video, day/night state, map journey, room/menu gallery | atmospheric stock hero only |
| SaaS/interface | guided real UI state change, feature focus, input-to-output demo, data relationship | fake dashboard bento |
| Editorial/culture | mask reveals, image cadence, typographic interruption, chapter navigation | endless centered copy |
| Automotive/spatial | real model inspection, spec scrub, speed-sensitive media, route sequence | decorative 3D sphere |

Use the selected prompt body's exact choreography as the technical reference, then adapt its subject and implementation.

## Implementation And Performance

For advanced static choreography, pin GSAP and ScrollTrigger at a known 3.13+ release:

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js"></script>
```

Register plugins explicitly. Use `gsap.matchMedia()` to scope desktop/mobile and reduced-motion setups. Keep all ScrollTriggers in the natural document flow and call cleanup when the page or media query changes.

- Animate transform, opacity, clip-path, or shader uniforms; avoid repeatedly animating layout dimensions and positions.
- Use `requestAnimationFrame` for pointer-following math and update CSS variables or transforms without framework rerenders.
- Apply `will-change` only while an element is likely to animate.
- Bound sticky and pinned scenes with stable heights and an explicit end condition.
- Pause video, canvas, and perpetual loops when offscreen or when the page is hidden.
- Avoid large backdrop filters on scrolling content.
- Do not conceal broken overflow at the page root.
- Keep touch targets at least 44 by 44 CSS pixels.
- Use familiar icons and visible focus states for controls.

Smooth scrolling is optional. Native scrolling plus ScrollTrigger is preferred unless the concept clearly benefits from interpolation. If Lenis is used, pin its version, integrate its frame loop once, and disable it for reduced motion or when it harms keyboard/touch navigation.

## Responsive And Reduced Motion

Every signature effect needs three implementations in the plan:

- desktop full effect
- mobile recomposition
- reduced-motion state

Do not merely scale desktop overlap down. On mobile, convert fragile pinned, horizontal, layered, or hover-only mechanics into readable vertical flow, swipe controls, tap states, or static sequences. Preserve all information and actions.

For reduced motion:

- reveal all content immediately
- remove parallax, scrub, autoplay, and large spatial transitions
- keep short opacity feedback only when useful
- provide controls for any nonessential moving media
- never require motion to understand or reach content

