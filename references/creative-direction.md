# Lumora Creative Direction

## Contents

1. Company DNA
2. Creative thesis
3. Design genome
4. Signature motif
5. Visual reference pass
6. Originality review
7. Content integrity

## Company DNA

Do not choose an aesthetic until the company has been reduced to useful design material. Capture:

| Signal | Questions | Design consequence |
| --- | --- | --- |
| Offer | What is sold, booked, joined, or understood? | Primary page action and information order |
| Audience | Who decides, what do they already know, and what makes them hesitate? | Copy density, proof, navigation, conversion friction |
| Difference | What can this company credibly claim that competitors cannot? | Hero idea and signature moment |
| Material world | What objects, surfaces, places, tools, ingredients, interfaces, or rituals belong to it? | Image direction, texture, shape language, motion metaphor |
| Tempo | Is the experience precise, urgent, calm, sensual, playful, ceremonial, technical, or direct? | Spacing and animation timing |
| Evidence | Which results, products, projects, reviews, credentials, or people are real? | Proof sections and media hierarchy |
| Vocabulary | Which nouns and verbs are naturally used by this company? | Headings, labels, microcopy, interaction names |
| Avoidance | Which category cliches would make the company look interchangeable? | Anti-pattern list |

Missing facts are constraints, not invitations to invent. Use neutral truthful copy or visibly incomplete contact paths when no fact is available.

## Creative Thesis

Write one sentence before coding:

`Make <company truth> feel <desired perception> by turning <company-specific material> into <page and motion idea>.`

Examples of useful specificity:

- Turn a perfumer's note pyramid into a layered product journey whose images and copy reveal from volatile top notes to lasting base notes.
- Treat an architecture studio's floor plans as the alignment grid for project stories and route transitions.
- Make a logistics product's handoff chain visible as a pinned sequence where ownership moves through real interface states.

Reject theses built only from adjectives such as premium, bold, modern, clean, cinematic, or innovative.

## Design Genome

Lock one decision on every axis. Record it in `lumora-plan.json`.

### Composition

Choose the page geometry that fits the content: cinematic stage, editorial offset, strict technical grid, gallery cadence, layered product theater, poster narrative, spatial scroll, or compact conversion flow. Do not default to bento. Do not repeat the same geometry for every section.

### Typography

Choose type by voice and content:

- editorial or cultural: expressive display or serif with a disciplined sans
- technical or financial: precise grotesk with optional mono for data
- consumer product: characterful display with a highly readable body face
- local service: distinctive but direct sans or humanist pairing

Keep the hero to one to three readable lines. Use a fluid scale with `clamp()` and stable line lengths. Do not scale type directly from viewport width without bounds. Do not mix more than two type families unless supplied brand rules demand it.

### Palette

Build roles, not a bag of colors: canvas, ink, muted ink, surface, border, primary action, secondary accent, focus, and media treatment. Derive the accent from real brand or subject matter. Avoid the automatic purple/blue AI palette, beige luxury shorthand, and one-hue pages.

### Material

Choose one material behavior that belongs to the subject: paper, lacquer, glass, brushed metal, fabric, oil, stone, film, ink, pixels, daylight, or something equally concrete. Express it through photography, surfaces, transitions, and detail. Do not imitate material with arbitrary blobs.

### Shape Language

Derive frames and controls from the subject and reference. Pick a controlled radius system, line weight, crop language, and icon style. Cards are only for repeated independent items or framed tools, not for every section.

### Rhythm

Alternate visual tempo. Follow a dense or interactive chapter with a calm proof or image chapter. Vary image-to-copy ratio and alignment while maintaining one spacing scale. Let the next section remain slightly visible below a first-viewport hero.

### Media

Decide whether the site is product-led, portrait-led, place-led, interface-led, process-led, or typographic. The media system must continue after the hero; one image cannot carry a long site.

### Motion

Select one signature interaction and one structural reveal language. The motion metaphor must arise from a real action or property: pour, fold, scan, assemble, compare, orbit, focus, layer, travel, tune, reveal, or transform.

## Signature Motif

A signature motif is a repeated relationship, not a decorative sticker. It can be:

- a crop shape drawn from the product silhouette
- a route line based on a real process or geography
- section dividers based on packaging, architecture, or interface geometry
- a typographic interruption that embeds real project or product media
- a day/night, before/after, raw/refined, or input/output state change central to the offer
- a controlled depth system for a product with layers, components, or stages

Use the motif in two to four meaningful places. Stop before it becomes a theme-park effect.

## Visual Reference Pass

When no strong supplied reference exists, generate an art-direction frame before coding. It should show the hero and enough continuation to communicate rhythm, media treatment, palette, type character, spacing, and the signature motif. Avoid readable raster text and logos.

After generation, inspect and record:

- first-viewport focal point and text-safe area
- section alignment and grid
- dominant and supporting crop ratios
- palette roles, not sampled color noise
- type character and scale relationships
- surface, border, radius, and shadow logic
- section spacing and density changes
- which visual decisions are implementable and which are image-generation artifacts

Do not code from memory after this pass. Keep the image open during implementation and compare screenshots against it.

## Originality Review

Before implementation, score each item from 0 to 2. A direction below 12/16 must be revised.

| Test | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Company specificity | Fits any company | Category-specific | Could only fit this company |
| Hero idea | Familiar template | Refined variation | Memorable subject-led opening |
| Media system | Placeholder or one image | Useful media | Art-directed multi-slot system |
| Section rhythm | Repeated blocks | Some variation | Deliberate narrative cadence |
| Signature interaction | Decorative | Relevant | Explains or embodies the offer |
| Typography | Default hierarchy | Appropriate | Distinctive and controlled |
| Conversion | Generic CTA | Clear | Integrated into the story |
| Mobile | Desktop stacked | Adapted | Purposefully recomposed |

Run a final substitution test: replace the company name with a competitor. If the page still makes equal sense, strengthen the thesis, media, copy, or signature moment.

## Content Integrity

- Use concrete nouns, verbs, quantities, ingredients, services, project names, and places from source facts.
- Do not invent reviews, customers, awards, certifications, prices, results, or team biographies.
- Avoid empty phrases such as elevate, unleash, revolutionize, next-gen, seamless, transformative, and future-proof.
- Match copy length to the visual composition. Rewrite for clarity without turning every section into marketing slogans.
- Make the primary action explicit and repeat it only where the user has enough context to act.

