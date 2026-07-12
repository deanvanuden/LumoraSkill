# Lumora Implementation Craft

## Contents

1. Build from the locked world
2. Reference-to-code translation
3. Page composition and rhythm
4. First viewport
5. Typography
6. Color, material, and shape
7. Media integration
8. Navigation and controls
9. Content and conversion
10. Multipage continuity
11. Responsive recomposition
12. Interaction completeness
13. Anti-drift review

## Build From The Locked World

Code is the production layer of the selected creative direction. Do not redesign freely after the visual references, asset system, and motion storyboard are locked.

Every visible decision should trace to one of these sources:

1. company truth
2. selected experience world and keyframes
3. anchor prompt invariants
4. a documented supporting contribution
5. usability, accessibility, performance, or GitHub Pages requirements

Avoid filling ambiguity with generic defaults. Resolve missing details through the same material, spatial, type, crop, and interaction language.

## Reference-To-Code Translation

Before writing CSS, extract a build specification from the three selected reference states:

- layout grid, max widths, gutters, alignment anchors, and intentional overflow
- first-viewport height, focal subject, copy-safe area, and visible continuation
- headline, body, label, caption, control, and numeric scale relationships
- section spacing, density changes, and calm intervals
- media frame ratios, object positions, masks, and edge behavior
- surface, line, radius, shadow, texture, and focus treatment
- navigation dimensions and open state
- dominant and subordinate interaction states
- desktop-to-mobile changes

Record the result in `creative_direction.composition_map`, with one entry for every major section on every published page. Each entry names the role, focal subject, text/media relationship, desktop geometry, mobile geometry, negative-space intention, and motion moment. Implement these as tokens and stable component rules. Compare terminal-headless screenshots against the references during the build, not only at the end.

## Page Composition And Rhythm

The page should feel like a directed sequence, not repeated content modules.

### Composition

- choose geometry from the experience world: stage, table, corridor, archive, instrument, poster, plan, map, gallery, product theater, or another specific relationship
- maintain alignment anchors while varying image-to-copy ratio, density, scale, and spatial tension
- use full-width bands and unframed sections for chapter changes
- use cards only for repeated independent items, modals, or genuinely framed tools
- never place cards inside cards or style every section as a floating card
- avoid repeated equal columns and cloned left-copy/right-image sections
- let asymmetry serve focus and narrative, not random novelty

### Media-To-Copy Balance

Treat media size, copy weight, and blank space as one composition. A large image does not automatically justify a tiny side list or narrow paragraph. At each viewport inspect:

- which element the eye reaches first
- whether the copy block has enough scale, density, or anchoring to answer the media
- whether the image carries the section's actual evidence or merely occupies space
- whether blank space isolates a focal point or reads as missing content
- whether the next section enters at a deliberate rhythm

Flag any chapter where media occupies roughly two thirds or more of the viewport while adjacent copy occupies only a small corner and the remaining column is empty. Keep it only when that imbalance is the named idea, not an accident. Fix weak balance by changing geometry, crop, copy hierarchy, supporting assets, or chapter sequence, not by adding decorative shapes.

### Rhythm

- follow dense, interactive, or high-contrast chapters with calm proof or media states
- vary section height based on content and transformation
- preserve a consistent spacing scale even when tempo changes
- avoid both accidental cramped transitions and empty uncomposed voids
- ensure every large blank region creates focus, anticipation, or separation visible in the viewport

### Stable Geometry

Define stable dimensions for boards, galleries, toolbars, selectors, tiles, media, counters, and controls. Dynamic content, loading, hover, labels, and active states must not shift the surrounding layout.

Use `aspect-ratio`, grid tracks, min/max constraints, and reserved media dimensions. Do not conceal overflow defects on `html` or `body`.

## First Viewport

The first viewport is an opening scene, not a checklist.

- make the company, product, place, person, or literal offer a primary signal
- use one dominant focal subject or environment
- keep the H1 readable and normally within one to three lines
- place supporting value in concise copy, not a long headline
- keep the primary action obvious without surrounding it with many competing pills or badges
- reveal a hint of the next chapter on common mobile, desktop, and wide viewports
- use relevant visual media when the visitor needs to inspect a real product, place, project, person, or state
- render text and brand marks in HTML or supplied vectors, not generated raster text

Do not default to a centered headline over a dark atmospheric image. Do not use a split card-and-copy marketing composition when a full-bleed subject-led scene can express the world more directly.

For tools and operational products, make the usable product or real interface state the first experience rather than creating an unrelated marketing hero.

## Typography

Typography must express voice and organize information.

### Selection

- use supplied brand fonts when licensed and usable
- otherwise choose type families whose construction matches the company and content
- pair expressive display type with a disciplined reading face when needed
- use mono only for genuine data, technical labels, tickets, coordinates, timestamps, or interface language
- avoid defaulting to the same fashionable font pairing across projects
- limit families and variable axes to what the hierarchy needs

### Scale And Measure

- define a bounded type scale with `clamp()` or media queries
- do not scale font size directly from viewport width without minimum and maximum bounds
- keep letter spacing at zero unless the real typographic treatment specifically requires positive tracking for small labels
- keep body measure readable and adapt it to page density
- reserve hero-scale type for true hero or manifesto moments, not compact panels
- use tighter heading scale in sidebars, tools, selectors, and dense evidence chapters

### Fit And Breaks

- test the longest company, product, location, and action strings
- control intentional line breaks without making them brittle on mobile
- allow wrapping before text overflows a control
- use dynamic sizing only when a fixed-format display requires it
- prevent text from occluding previous or following content

Typography should still look designed with all animations disabled.

## Color, Material, And Shape

### Color Roles

Define functional roles rather than a bag of shades:

- canvas and alternate canvas
- primary and muted ink
- surface and elevated surface when truly needed
- line and divider
- primary action
- secondary or signal accent
- focus, error, success, and disabled states
- media grade and overlay behavior

Derive color from brand, subject, material, place, or campaign media. Avoid automatic purple-blue gradients, beige luxury shorthand, all-black club shorthand, or a page dominated by variations of one hue. A real brand color may dominate, but neutral, media, material, status, and contrast roles must create depth and legibility.

Do not use gradient orbs, bokeh blobs, or glowing pseudo-elements as substitute artwork.

### Material

Express the locked material through real media, texture, edges, light, depth, transition, and interaction. Do not fake paper, metal, glass, oil, fabric, or film with an unrelated preset.

### Shape

- derive crop geometry, line weight, radius, and control shapes from the world
- keep one controlled radius system; cards are normally 8px or less unless a supplied or concept-specific system requires otherwise
- prefer sharp or lightly softened edges for editorial and operational work unless physical material implies another form
- use shadows only when elevation or material requires depth

## Media Integration

- use each asset at the role, crop, and size recorded in `media_plan.slots`
- keep focal points stable with `object-position` or `<picture>` variants
- use full-bleed or unframed presentation when the subject is the primary experience
- avoid tiny thumbnails for media that users need to inspect
- avoid darkening, blurring, or cropping real subjects until they become unreadable
- continue the media campaign through middle chapters and the closing state
- do not reuse one non-logo image across adjacent prominent slots
- integrate video, 3D, and canvas structurally rather than placing them inside decorative preview cards

Use CSS for layout, masks, UI, lines, and restrained textures. Use raster, video, 3D, or SVG assets for visual subjects that CSS primitives cannot carry credibly.

## Navigation And Controls

Navigation should belong to the experience while remaining predictable.

- expose company identity, current location, primary routes, and a useful action
- use sticky or fixed behavior only when it aids repeated navigation or the experience framing
- make mobile navigation a complete designed state, not a last-minute dropdown
- manage focus, escape, close, scroll locking, and current-page indication
- keep fixed controls away from focal media, browser safe areas, and page content

Use familiar icons for familiar actions. Prefer Lucide when available in the existing stack; otherwise use the project's established icon library. Do not hand-draw arbitrary SVG icons when a standard icon exists. Add accessible names and tooltips for unfamiliar icon-only controls.

Use the correct control type:

- icon buttons for familiar tools
- swatches for color
- segmented controls for a small mode set
- toggles or checkboxes for binary state
- sliders, steppers, or inputs for numeric values
- menus for larger option sets
- tabs for parallel views
- text or icon-plus-text buttons for commands

Maintain 44 by 44 CSS-pixel touch targets and visible focus.

## Content And Conversion

Use concrete company language. Prefer products, places, materials, actions, project names, quantities, ingredients, and process terms over vague claims.

Avoid unsupported copy such as "elevate," "unleash," "revolutionize," "next-gen," "seamless," "cutting-edge," or "transformative."

### Conversion Integration

- present the primary action when the visitor has enough context
- connect its language and visual state to the dominant transformation
- repeat it only at meaningful readiness moments
- keep secondary routes subordinate but available
- link to real purchase, booking, inquiry, signup, email, phone, map, social, or service destinations
- expose price, availability, selected state, errors, and constraints truthfully

The closing chapter should advance or complete the world, not become a generic oversized CTA card.

### Forms

- use real endpoints or a truthful `mailto:`/external service route
- label every field and show useful helper and error text
- implement loading, disabled, validation, error, and actual success behavior
- never show success for data that was not sent
- preserve entered data after recoverable errors

## Multipage Continuity

Use separate pages when products, services, case studies, program, archive, studio, contact, or audience journeys need distinct depth.

Across routes preserve:

- company identity and core tokens
- material, media grade, type, and control language
- navigation and footer behavior
- signature motif and transition grammar
- relative hierarchy and grid anchors

Give each route its own focal subject, purpose, and pacing. Do not clone the home-page hero and swap the heading.

For existing sites, create a route migration decision for every discovered source route. A route may be redesigned, consolidated, redirected, or retired. Never copy a source site into the publishing root and redesign only `index.html`; old HTML, stylesheets, scripts, mojibake, and broken asset paths are release failures even when the new homepage is strong.

Every shipped route must appear in `build_contract.route_manifest` and use the shared system named there. Legal and system pages may be quieter, but they still need the current typography, navigation, footer, spacing, focus states, and responsive containment. Consolidated routes need a branded accessible redirect or updated destination, not an untouched legacy page.

Use real relative `.html` routes for default static builds. Verify links from every page and design `404.html` as part of the same world.

Page transitions may reinforce the world when they remain fast, accessible, and failure-safe. Never delay navigation merely to show an animation.

## Responsive Recomposition

Do not treat mobile as stacked desktop.

For every major chapter decide:

- which subject remains primary
- whether copy moves before or after media
- which overlap becomes normal flow
- which crop or asset changes
- which hover becomes tap, swipe, or always-visible state
- which pinned or horizontal chapter becomes explicit vertical states
- how fixed navigation and controls avoid covering content
- how long words, actions, and labels fit

Use dynamic viewport units or robust minimums. Test narrow and tall mobile, not only one screenshot size. Keep the next chapter visible when the first viewport concept allows it.

Test `320`, `360`, `390`, `430`, `768`, `1024`, and `1440` CSS-pixel widths. The home page must pass all seven. Every route must pass at least `390` and `1440`, and interaction-heavy routes need the full matrix. Measure `document.documentElement.clientWidth` and `scrollWidth`, identify every overflowing selector, and fix the actual child. Never declare containment after applying root-level `overflow-x: hidden` or `clip`.

For prominent mobile media:

- define a stable aspect ratio and a maximum height in `svh` or another intentional bound
- use `object-position` from the planned focal point
- switch source or crop with `<picture>` when desktop geometry cannot survive
- keep borders, transforms, shadows, pseudo-elements, and absolute children inside the measured bounds
- verify the live signature state, not only the initial and full-page screenshots

## Interaction Completeness

Implement all states a real user expects:

- default, hover, focus, active, selected, disabled
- loading, empty, error, success where relevant
- open and closed menu, dialog, accordion, and selector states
- current route and selected product or package
- media playing, paused, muted, loading, and failed
- canvas or 3D loading, ready, error, fallback, and reduced-motion

On-screen copy should serve the visitor, not explain that the site has animations, keyboard shortcuts, responsive design, or premium visual features.

## Anti-Drift Review

After the first complete implementation, compare it with each reference state.

Check:

- focal point and subject scale
- headline line count and position
- negative space and section occupancy
- media-to-copy balance
- color and material behavior
- crop and frame language
- control and navigation character
- transition and interaction state
- continuation between chapters
- mobile equivalence

Common drift:

- converting image-led scenes into generic cards
- replacing unusual geometry with centered containers
- shrinking generous whitespace into dense blocks
- using one hero image and text-only middle sections
- adding generic pills, stats, badges, icons, and cards not present in the world
- simplifying the signature interaction into fade-ups
- adding several effects to compensate for weak assets
- losing the motif in later pages or the closing state

Fix drift by restoring the locked reference relationship, not by adding polish on top of a generic layout.
