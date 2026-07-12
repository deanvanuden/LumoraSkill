# Lumora Asset Direction

## Contents

1. Asset strategy
2. Audit supplied media
3. Direct three connected references
4. Build the continuity bible
5. Decompose the campaign into asset layers
6. Plan complete asset coverage
7. Generate final assets
8. Truth and representation
9. Slot-specific direction
10. Image, video, 3D, SVG, and texture roles
11. Responsive crops and optimization
12. Asset review gate

## Asset Strategy

Media is part of the product, not decoration added after layout. A visual website needs enough authored material to sustain its world from entry through conversion.

The asset strategy must answer:

- What is the signature subject?
- Which supplied assets are documentary evidence?
- Which campaign assets must be generated, photographed, edited, captured, modeled, or drawn?
- Which visual roles recur across pages?
- How do camera, lighting, material, color grade, and crop remain coherent?
- Which assets are required at desktop, mobile, and interaction states?
- What may be reused, and what must remain unique?

There is no fixed image count. Generate or prepare every asset the experience needs, no more and no fewer. A single-page studio may need six strong images; a product campaign may need fifteen stills, cutouts, and details; a restrained professional site may need three truthful photographs and one evidence diagram.

Do not stop after producing one hero asset.

## Audit Supplied Media

Inventory logos, brand marks, product images, people, places, project photography, video, UI screenshots, illustrations, diagrams, documents, textures, fonts, and icons.

For each asset record:

- source and ownership
- documentary or campaign role
- dimensions, duration, format, and transparency
- subject and factual meaning
- focal point and safe crop range
- color, light, lens, grain, and material character
- whether quality supports the largest planned render
- whether editing or background removal is allowed
- routes and slots where it could be used

Classify it:

- `hero-capable`: strong enough to carry the first viewport
- `supporting`: useful at a smaller or specific crop
- `evidence-only`: factual but visually weak; present clearly without enlarging beyond quality
- `reference-only`: informs direction but should not ship
- `reject`: irrelevant, low quality, stale, misleading, duplicated, or unlicensed

Do not enlarge weak media into a full-bleed hero. Do not discard strong real photography merely because generation is available.

## Direct Three Connected References

When the user has not supplied a complete and strong design direction, load the `imagegen` skill and create three implementation-oriented reference frames before coding.

The three frames depict the same site and world:

1. `entry`: first viewport plus visible continuation
2. `signature-state`: dominant transformation at its clearest
3. `decision`: proof, action, and closing state

These are design specifications, not abstract moodboards. They must expose:

- viewport composition and focal point
- relative headline, subject, navigation, copy, and control scale
- grid and negative-space logic
- media frames and crop language
- color roles and material behavior
- type character and hierarchy
- interaction state and visible change
- continuation and section rhythm
- mobile-safe subject framing

### Reference Prompt Structure

Build prompts from the locked plan:

```text
Create an implementation-oriented website design frame for [company and offer].
This is the [entry/signature/decision] state of one continuous site.
Experience world: [world].
Signature subject: [object, interface, process, or environment].
Visible transformation: [transformation at this state].
Composition and camera: [grid, viewpoint, lens, framing, negative space].
Material and light: [material, lighting, texture, grade].
Typography character: [display and body relationship; no readable raster copy].
Media roles: [hero, supporting crop, proof, control].
Interaction evidence: [what the state makes visible].
Responsive requirement: [mobile-safe focal area and continuation].
Maintain exact continuity with the other two frames.
No fake logo, readable raster text, watermark, generic gradient orb, decorative primitive art, unrelated stock subject, or impossible interface.
```

Generate enough variants to obtain one usable frame per state. Inspect every result with an image-viewing tool. Reject frames that are attractive but impossible to implement, visually generic, inconsistent, text-heavy, or missing the signature subject.

### Deep Reference Analysis

Record for every selected frame:

- primary focal point and eye path
- text-safe region and maximum line count
- column proportions and alignment anchors
- media aspect ratios and object positions
- palette roles rather than sampled color noise
- material edges, shadows, highlights, texture, and depth
- type size relationships and density
- control shape, icon, radius, border, and active-state logic
- transition into adjacent chapters
- implementable decisions versus image-generation artifacts

Keep the frames visible during implementation and compare rendered screenshots against them.

## Build The Continuity Bible

Complete `media_plan.continuity_bible` before generating final assets.

### Subjects

Define hero subject, supporting subjects, people policy, environment, props, and exclusions. State whether objects must match supplied product geometry or may be conceptual campaign representations.

### Camera And Lens

Define camera height, distance, angle, perspective, lens character, depth of field, and movement. A macro product world and a documentary venue world should not silently mix camera languages.

### Lighting

Define source direction, hardness, color temperature, time of day, reflections, shadows, practical lights, and contrast behavior.

### Materials

Define concrete surfaces and how they react to light: matte, wet, translucent, fibrous, polished, scratched, printed, metallic, oily, dusty, soft, or architectural.

### Environment

Define stage, room, landscape, interface context, background depth, floor, horizon, weather, and recurring props.

### Palette And Grade

Define neutral base, action color, secondary contrast, skin handling, saturation, black point, highlight color, grain, and consistency with supplied brand assets.

### Texture And Finish

Define whether the campaign is clean, tactile, photocopied, glossy, cinematic, archival, technical, analog, or hyperreal. Use one controlled finish.

### Crop Behavior

Define preferred aspect ratios, subject anchor, text-safe area, negative space, edge cropping, portrait and landscape variants, and mobile recomposition.

### Negative Constraints

List recurring failures to exclude: readable text, fake logos, malformed product, extra fingers, impossible architecture, duplicate objects, irrelevant props, stock poses, oversmoothed skin, excessive glow, generic luxury styling, or any concept-specific risk.

## Decompose The Campaign Into Asset Layers

Do not treat a beautiful reference frame as one giant image to place beside copy. It is a system of subjects, materials, depth, crops, and transitions. Record that decomposition in `media_plan.asset_layers` before final generation.

### Signature

One primary object, place, interface, person, process, or film state carries the central idea. It may have responsive and interaction variants, but it remains one recognizable subject.

### Narrative

Distinct scenes or states advance the story. They must change evidence, viewpoint, time, material, use, or outcome rather than repeating the hero crop. A typical visual site needs at least two narrative assets.

### Supporting

Small assets let the world enter the layout instead of remaining trapped inside rectangular media frames. Useful supporting assets include:

- transparent product, ingredient, tool, ticket, material, or architectural cutouts
- masks, torn or scanned edges, frame fragments, route lines, depth maps, and displacement maps
- macro details, contact-sheet crops, process fragments, shadow plates, reflections, and foreground occluders
- material textures, printed marks, interface cursors, labels rendered separately in HTML, and transition frames

Use at least two supporting assets when the concept is visual. Give each a semantic target section, integration method, desktop behavior, mobile behavior, and reduced-motion role. Do not scatter generated fragments as decoration; each one must reinforce subject, evidence, depth, orientation, or transformation.

Write every asset target as `page.html#section-id`. This makes reuse and multipage coverage auditable and prevents ambiguous section names from silently pointing at the wrong route.

List the asset IDs used by an implemented section in `data-lumora-assets="asset-id,second-id"`. The marker is traceability, not decoration; the corresponding raster, video, model, SVG, canvas, or CSS layer must still exist and render in that section.

### Utility

Plan marks, icons, thumbnails, posters, loaders, social previews, 404 media, and static fallbacks. Use supplied vectors or code-native SVG for identity and diagrams; use generated raster media only when the utility role genuinely needs it.

### Decomposition Review

Write `asset_decomposition_review` after comparing the three references. Identify which visual elements become final assets, which are recreated in HTML/CSS/SVG, which are animation states, and which are image-generation artifacts to reject. Final assets never contain surrounding page copy or an entire rendered section.

## Plan Complete Asset Coverage

Create `media_plan.slots` before final generation. Include major and supporting roles across all pages and states.

```json
{
  "id": "ritual-macro",
  "role": "material macro proving oil texture and application",
  "page": "product.html",
  "aspect_ratio": "3:2",
  "target_render": "1440x960",
  "focal_point": "oil thread crossing 56% x and 44% y",
  "text_safe_area": "top-left 30%",
  "source": "generated from locked continuity bible",
  "truthfulness": "conceptual campaign material; no clinical result claim",
  "reuse": "ritual chapter and mobile crop only",
  "text_relationship": "the macro crosses behind the section label but leaves the claim in a clear HTML text column",
  "desktop_geometry": "seven-column media field with the focal thread at the inner grid line",
  "mobile_geometry": "4:3 crop below the claim, capped at 58svh with the focal thread centered",
  "motion_role": "the oil thread advances once as the ritual step becomes active"
}
```

Potential roles include:

- signature hero object, environment, interface, or film
- alternate mobile hero composition
- product cutout, variant, exploded state, material macro, ingredient, or usage scene
- place exterior, interior, detail, route, day/night state, or service moment
- editorial portrait, archive image, poster, program image, contact sheet, or artwork crop
- real interface state, input, output, workflow detail, data evidence, or integration view
- project overview, detail, plan, material, process, before/after, or result
- transparent foreground object for layered interaction
- transition frame, mask source, displacement texture, depth map, video poster, or fallback still
- closing campaign image that advances the story rather than repeating the hero
- 404 and social-preview image when needed

Small assets matter when they reinforce the world: stamped marks, paper fibers, scanned edges, product labels supplied as HTML overlays, real UI cursors, diagram fragments, material textures, icons, and state thumbnails. Do not generate decorative clutter merely to increase asset count.

### Coverage Review

For every section ask:

- Does this chapter need visual evidence, atmosphere, explanation, or no media?
- Is the assigned asset unique enough for its prominence?
- Does its crop and resolution match the actual render?
- Does it continue the selected world?
- Is it truthful in context?
- Does mobile have a usable composition?
- Does nearby copy have enough visual weight to balance the media, or is the layout creating an accidental blank column?
- Could a decomposed cutout, texture, or state asset integrate the world more naturally than another rectangular image?

Write `asset_coverage_review` after implementation.

## Generate Final Assets

Generate final assets separately from the reference frames. A reference frame contains a layout; a final asset contains only the media needed by a slot.

### Final Asset Prompt Structure

Every prompt should include:

- exact subject and company relationship
- slot role and aspect ratio
- target focal point and text-safe area
- camera distance, angle, lens, and depth
- lighting and material behavior
- environment and palette grade
- relationship to the continuity bible and sibling assets
- transparent, isolated, environmental, or full-bleed background requirement
- factual status and prohibited implications
- negative constraints

Example structure:

```text
Create a [aspect ratio] campaign asset for [slot role].
Subject: [exact product/object/place/process].
Company relationship: [why this belongs to the company].
Camera: [distance, angle, lens, focal point].
Composition: [subject position, negative space, crop behavior, mobile safety].
Lighting and material: [locked continuity].
Environment and grade: [locked continuity].
Consistency: match [reference states and sibling assets].
Output: [isolated transparent cutout / full-bleed scene / macro / poster / video poster].
Do not include [text, logo, watermark, extra objects, false evidence, known failure modes].
```

### Generation Sequence

1. Generate the signature asset first.
2. Inspect geometry, subject identity, light, and material.
3. Lock a successful look before generating siblings.
4. Generate related assets in logical families: product, environment, detail, people, transition, closing.
5. Inspect every asset at full resolution and at planned render size.
6. Regenerate inconsistent or malformed work; do not repair major conceptual failures with CSS.
7. Copy selected assets into project-local folders with descriptive stable filenames.
8. Optimize only after the final selection.

When an edit can preserve a real supplied product, person, or place better than generating from scratch, use image editing with the source attached. Do not alter documentary evidence in a misleading way.

## Truth And Representation

### Products

Do not generate a supposedly exact commercial product from text when its geometry, packaging, label, or color must be truthful. Use supplied product photography, a supplied image edit, or clearly label the site as a fictional prototype.

### People

Generated people may support conceptual campaign imagery, but may not be presented as actual founders, staff, customers, patients, artists, guests, or testimonial authors. Prefer real supplied portraits for identity and proof.

### Places

Generated environments may establish a conceptual world, but may not be presented as the company's real venue, office, restaurant, clinic, property, or completed project. Use supplied place photography for factual claims.

### Results And Evidence

Do not generate before/after results, clinical outcomes, financial charts, event attendance, project photography, reviews, certificates, awards, or screenshots that imply real performance.

### Campaign Props And Metaphors

When the selected world needs an artifact as campaign language rather than evidence, create it instead of stalling the build. A conceptual access band, ticket fragment, packaging sleeve, stamped card, tool arrangement, route token, or editorial object can be generated, modeled, photographed, or built in code when:

- it is clearly a campaign interpretation rather than a claimed real credential or product
- real company facts and logos remain supplied assets or HTML/SVG overlays
- it contains no scannable credential, fake event data, invented certification, or misleading result
- its material, camera, and palette follow the continuity bible
- copy and surrounding context do not present it as documentary proof

Prefer a truthful authored metaphor over a placeholder. Ask for an exact source asset only when identity, geometry, legal accuracy, or evidence genuinely requires it.

### Disclosure Through Context

Do not add distracting disclaimers to every image. Make role and copy truthful: campaign image, illustrative process, conceptual product visualization, or real supplied evidence. Never place a generated image next to copy that makes it appear documentary.

## Slot-Specific Direction

### Hero

- one inspectable focal subject or environment
- first-viewport brand, product, place, person, or offer signal
- copy-safe region derived from layout
- enough resolution for largest viewport
- a mobile composition, not an accidental crop
- a mobile aspect ratio and maximum viewport-height bound; never let a wide desktop image become an excessively tall static poster
- visible continuation into the next chapter

### Product

- preserve shape, label, cap, scale, color, and variant truth
- include useful angles, material details, application, packaging, and size relationships
- let interaction inspect the product rather than floating it over decoration

### Place And Hospitality

- reveal actual environment when the user needs to inspect it
- use wide, detail, service, and location images with consistent light
- avoid dark atmospheric crops that hide the room, food, property, or venue

### SaaS And Interfaces

- use real UI or clearly conceptual product states
- maintain consistent data, navigation, spacing, and device framing across captures
- show the input-to-output relationship, not a pile of fake dashboard cards
- capture desktop and mobile states where the product supports both

### Editorial, Culture, And Events

- treat real posters, programs, archives, tickets, access artifacts, artwork, and photography as content
- create a campaign system that can hold changing events without becoming a generic club aesthetic
- preserve artist, date, venue, and ticket truth in HTML, not raster text

### Services And Trust

- prioritize real people, work, tools, process, place, and evidence
- generated conceptual imagery should clarify a method, not impersonate proof
- avoid interchangeable stock gestures and meeting-room scenes

## Image, Video, 3D, SVG, And Texture Roles

Use the medium that carries the subject best.

### Raster Image

Best for photography, products, people, place, food, material, campaign art, editorial scenes, and complex texture.

### Video

Best for time, performance, craft, atmosphere, motion behavior, transformation, or spatial movement. Provide a poster and a still fallback. Do not use an unrelated ambient loop.

### 3D

Best when the visitor benefits from inspecting an actual object, environment, assembly, material, or spatial relationship. Prepare model, texture, HDR/environment, poster, loading, and fallback assets as one system.

### SVG

Best for logos supplied as vector, diagrams, paths, maps, masks, technical marks, UI icons, and code-native line systems. Do not hand-draw a fake campaign illustration when raster or 3D is required.

### Texture

Use project-specific scans, material maps, grain, paper, ink, noise, displacement, or depth assets with restraint. A texture should reinforce material and survive compression. Avoid generic noise pasted over every site.

## Responsive Crops And Optimization

- Generate distinct portrait and landscape compositions when crop requirements materially differ.
- Prefer a mobile-native crop over a portrait stretch. Bound prominent mobile media with an intentional `aspect-ratio`, `max-height`, and focal point; use `<picture>` when the source must change.
- Set explicit width and height attributes and stable aspect ratios.
- Use `object-position` or `<picture>` sources based on known focal points.
- Keep subject scale and text-safe area stable across viewports.
- Encode photographic assets as AVIF or WebP where supported, with a sensible fallback when needed.
- Size major raster media near twice its largest CSS render dimension when practical.
- Preserve alpha only when needed; transparent images are often substantially larger.
- Compress video, limit resolution and bitrate to the visible role, and include a useful poster.
- Lazy-load below-fold media, but do not delay the hero's decisive asset.
- Avoid loading desktop and mobile hero variants simultaneously when `<picture>` can select one.

## Asset Review Gate

Before coding:

- three connected reference states are selected and deeply analyzed
- the signature asset is supplied, generated, authored, or modeled and visually credible
- continuity-bible fields are locked
- every prominent slot has a source and aspect ratio

Before delivery:

- every asset loads locally and uses a stable filename
- no placeholder, hotlink, watermark, readable generated text, fake logo, or malformed subject remains
- crop, focal point, text-safe area, and resolution work at actual viewports
- prominent images are not reused as filler
- generated media is not presented as documentary proof
- all assets belong to the same campaign world
- media continues through the closing state
- mobile and reduced-motion fallbacks remain visually complete
