# Lumora Creative Direction

## Contents

1. Purpose
2. Company truth
3. Creative freedom
4. Three-world exploration
5. Anatomy of an experience world
6. Category-departure review
7. Selecting and locking a direction
8. Signature object and motif
9. Experience keyframes
10. Originality scorecard
11. Rejection conditions

## Purpose

The creative direction must convert company truth into a world, not convert a business category into a familiar website style. The visitor should remember a subject, spatial relationship, transformation, or interaction that belongs to the company.

Do not begin with colors, fonts, effects, or sections. Begin with what is real and what can become experience material.

## Company Truth

Complete `company_truth` before generating concepts.

| Signal | Questions | Experience consequence |
| --- | --- | --- |
| Offer | What is sold, booked, joined, visited, or understood? | Primary action and information order |
| Audience | Who decides, what do they know, and what makes them hesitate? | Density, language, proof, and friction |
| Difference | What can this company credibly claim that competitors cannot? | Hero thesis and signature interaction |
| Proof | Which products, results, projects, reviews, people, credentials, or demonstrations are real? | Evidence chapters and media hierarchy |
| Material world | Which objects, ingredients, interfaces, surfaces, places, tools, rituals, documents, sounds, or movements belong to the work? | Signature subject, media, texture, crop, and motion |
| Place | Where does the work happen and what environmental conditions matter? | Light, sound, camera, scale, and pacing |
| Tempo | Is the experience precise, urgent, sensual, ceremonial, playful, raw, technical, direct, or quiet? | Timing, density, navigation, and transition behavior |
| Vocabulary | Which nouns and verbs do employees and customers naturally use? | Copy, labels, controls, and interaction names |
| Conversion | What real destination or next step exists? | Closing scene and functional integration |
| Missing facts | What is stale, unknown, unavailable, or unsupported? | Omission, neutral copy, or visible integration gap |

Missing facts are constraints, not invitations to invent. Generated imagery may build a campaign world, but it may not fabricate documentary evidence.

## Creative Freedom

Lumora has no preferred visual genre. The selected company truth may justify:

- a full-screen 3D object with minimal interface
- a film-led place or performance narrative
- a precise technical instrument or real product demo
- a tactile paper, fabric, metal, oil, glass, stone, food, or print world
- a typographic cultural poster that behaves like a program or publication
- a spatial archive, interactive map, route, timeline, score, recipe, ritual, or assembly
- a restrained editorial website with almost no animation
- a playful game-like interaction when play belongs to the company
- a dense operating interface when repeated work, comparison, or data is the subject
- a nonlinear or multipage journey when the audience benefits from exploration

Do not select an ambitious medium merely to signal quality. Do not reject one merely because it is difficult. Select the medium that most truthfully expresses the subject.

Constraints govern coherence:

- one primary world
- one dominant subject or relationship
- one transformation or interaction thesis
- one continuous media and material system
- truthful content and usable fallbacks

They do not require visual minimalism or a small number of local details.

## Three-World Exploration

Write at least three concepts before selecting a direction. A concept is not distinct when only the palette, font, or effect changes.

Make the concepts structurally divergent. Useful lenses include:

- `object`: organize the experience around a product, tool, document, ingredient, ticket, garment, building element, or physical artifact
- `process`: turn a real transformation, handoff, ritual, route, assembly, comparison, or decision into page progression
- `place`: let geography, venue, studio, room, landscape, light, or community behavior become the world
- `interface`: expose a real input-to-output relationship through inspectable product states
- `archive`: create a publication, collection, catalog, contact sheet, score, or evidence system from real work
- `performance`: use time, sound, choreography, or camera movement to embody what happens

Do not mechanically use the first three lenses. Choose lenses that produce meaningfully different possibilities for the company.

For every concept record:

```json
{
  "id": "concept-id",
  "name": "short working title",
  "company_truth": "the exact fact or behavior being expressed",
  "experience_world": "the world the visitor enters",
  "signature_object": "the central inspectable subject or relationship",
  "transformation": "what visibly changes from entry to decision",
  "hero_scene": "the first viewport as a scene, not a component list",
  "asset_strategy": "the supplied and generated media needed to sustain the world",
  "risk": "the most likely conceptual or production failure",
  "why_only_this_company": "the substitution failure"
}
```

### Divergence Test

Place the three concepts side by side and ask:

- Do they use different central subjects?
- Do they produce different first viewports?
- Do they imply different spatial behavior and transformations?
- Do they require different asset campaigns?
- Would a visitor describe them with different nouns, not only adjectives?

If not, continue exploring.

### Concept Escalation

Do not accept the first competent concept. Improve each promising direction by asking:

- What is the most specific real object or behavior available?
- What could become an inspectable hero subject instead of background decoration?
- What can the visitor do that mirrors the company's work or culture?
- What visual material can continue through every chapter and route?
- What would make the opening recognizable with the logo removed?
- Which expected category convention can be replaced with something more truthful?

Creativity is controlled surprise backed by company evidence.

## Anatomy Of An Experience World

Lock every field below. These decisions must describe the same world.

### Creative Thesis

Use:

`Make <company truth> feel <desired perception> by turning <company material or behavior> into <page and transformation idea>.`

Reject adjective-only theses such as "make the company feel bold, premium, and modern."

### Experience World

Describe the environment and operating logic in one or two sentences. Examples:

- a perfume laboratory where notes volatilize, combine, and settle as the visitor moves from first impression to ritual
- a venue threshold where a real access artifact is scanned and opens into program, crowd, and ticket states
- a dispatch table where real ownership and route states hand off through an inspectable product interface

### Signature Object

Choose a real or credibly campaign-authored subject that can carry the first viewport and survive transformation. It may be physical, spatial, interface-based, typographic, or procedural.

Weak: floating sphere, glowing card, abstract wave, random chrome object.

Strong: the actual bottle and oil behavior, a venue access band, a floor-plan fragment, a real control surface, a chef's ingredient sequence, a machine component, a contract clause, a route handoff, or an artist's archive object.

### Material Language

Define concrete surface behavior: uncoated paper, lacquer, condensation, brushed aluminum, Tyvek, ink transfer, glass refraction, LED scan light, darkroom grain, daylight concrete, woven fabric, wet stone, polished interface glass, or another relevant material.

Material must influence media, color, edge treatment, transition, typography, and interaction. Do not simulate material with arbitrary gradients.

### Spatial Logic

Define how subjects occupy the viewport: stage, table, corridor, layered sheet, contact sheet, instrument panel, room, map, orbit, assembly, split state, archive rail, or another company-specific relationship.

### Composition Map

Translate the spatial logic into one entry for every major section on every published page. Record:

- page, stable section ID, and narrative role
- focal subject
- relationship between HTML copy and media
- desktop geometry and relative visual weight
- mobile order, crop, aspect, and viewport-height bounds
- purpose of negative space
- one meaningful motion moment or an explicit static reason

This prevents the reference world from dissolving into improvised split sections during implementation. Reject a map entry that merely says "text left, image right." State the actual ratio, anchors, subject position, and why the imbalance belongs to that chapter.

### Camera Behavior

Define point of view and movement: fixed overhead inspection, slow dolly, macro rack focus, lateral tracking, orbit, handheld documentary, static catalog, architectural elevation, interface zoom, or no camera movement. Use one coherent language across references and assets.

### Transformation

Define a verb that connects company truth to progression: scan, open, pour, assemble, tune, route, focus, cut, stamp, fold, compare, refine, unlock, reveal, layer, grow, archive, or another truthful action.

### Emotional Arc

State how perception changes. Examples: mystery to recognition to invitation; uncertainty to evidence to trust; anticipation to entry to collective release; raw material to craft to ownership.

### Interaction Thesis

Describe how input and transformation belong together. Scroll may advance a physical process, pointer movement may inspect a material, drag may compare states, tap may choose a product, or keyboard input may reveal a real product response. Avoid input that has no semantic relationship.

## Category-Departure Review

Category conventions can communicate quickly, but they cannot be the whole direction.

| Category | Familiar default that is insufficient alone | Search for a truthful departure |
| --- | --- | --- |
| Beauty/product | beige serif, bottle over glow, ingredient cards | formula behavior, application ritual, texture, packaging mechanics, real material macro |
| SaaS/AI | dark dashboard, gradients, bento features, floating UI | real input-to-output states, workflow ownership, inspectable data relationship, live product behavior |
| Nightlife/culture | black, acid/neon, condensed uppercase, party photos | access ritual, venue geography, sound or program structure, ticket material, community behavior |
| Hospitality | cinematic room photo, menu cards, booking button | day-to-night change, service ritual, ingredient journey, room sequence, neighborhood context |
| Studio/portfolio | giant type, horizontal gallery, hover trail | project-specific process, studio tools, decision evidence, a coherent archive or case-study world |
| Architecture | white grid, project carousel, thin type | plan logic, material joins, movement through space, site conditions, model or drawing relationship |
| Local service | smiling team hero, icon cards, review strip | real tools, place, service choreography, before/after evidence, local route or response behavior |
| Professional trust | navy palette, stock portrait, metric cards | decision process, document logic, evidence trail, expert method, transparent risk or handoff model |
| Automotive/spatial | dark render, scroll rotation, specification cards | actual engineering detail, material change, driving environment, configuration consequence |

Using a brand's real category colors or typography is not a failure. Stopping there is.

Record the expected conventions and the deliberate departure in the selected concept and originality evidence.

## Selecting And Locking A Direction

Select the world with the strongest combined answer to these questions:

1. Is it rooted in the strongest real company truth?
2. Does it produce a memorable opening without relying on the logo?
3. Can its subject and material continue across the whole site?
4. Does the transformation explain, embody, or intensify the offer?
5. Can supplied and generated assets carry it at production quality?
6. Does conversion become a natural next state?
7. Can mobile preserve the idea through recomposition?
8. Is the technical ambition feasible for a static GitHub Pages runtime?

Record why the winner was selected and why at least two alternatives were rejected. A rejected concept may be strong but wrong for available facts, media, schedule, or conversion.

Set `company_truth.status`, `direction_exploration.status`, and `creative_direction.status` to `locked` only after these decisions are coherent.

## Signature Object And Motif

The signature object is the focal subject. The motif is a repeated relationship derived from it.

Examples:

- bottle silhouette becomes crop geometry and selector track
- floor-plan grid controls alignment, page transitions, and project labels
- access-band perforations become navigation rhythm, scene boundaries, and ticket action
- handoff states become progress, feature demonstration, and closing invitation
- ingredient layers become depth, reveal order, and product comparison

Use the motif in two to four meaningful places. Do not stamp it onto every component.

## Experience Keyframes

Define three connected states before coding:

### Entry

- one primary focal subject
- company or offer immediately legible
- clear invitation or action
- enough continuation visible to establish page rhythm
- safe crops for desktop and mobile

### Signature State

- shows the central transformation at peak clarity
- proves how media, typography, UI, and motion share one world
- demonstrates what changes as the user interacts or scrolls
- remains implementable, not an impossible mood render

### Decision

- carries the same subject and material language into conversion
- answers the final objection or presents the strongest proof
- makes the action feel like the next narrative state
- leaves useful navigation and contact routes visible

The keyframes may be generated images, edited supplied references, 3D look-development frames, storyboard stills, or precise existing designs. Record the asset and a deep visual analysis.

## Originality Scorecard

Score each dimension from 0 to 2 after visual references and again after implementation.

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Company specificity | Fits any company | Fits the category | Could only fit this company |
| Concept unity | Several unrelated ideas | Mostly coherent | One world controls all decisions |
| Hero memorability | Familiar template | Refined opening | Recognizable subject-led scene |
| Asset authorship | Placeholder or one image | Useful media set | Art-directed campaign system |
| Section rhythm | Repeated blocks | Some variation | Narrative cadence with deliberate tempo |
| Motion relevance | Decorative | Content-related | Interaction embodies the offer |
| Typographic character | Default hierarchy | Appropriate | Distinctive and world-consistent |
| Conversion integration | Attached CTA | Clear action | Action completes the story |
| Mobile recomposition | Desktop stack | Adapted | Purpose-built equivalent experience |
| Category departure | Pure convention | One variation | Truthful and memorable departure |

Require at least 16/20 and no zero before delivery. Every score needs visible evidence. Self-scoring does not replace terminal-headless render critique.

## Rejection Conditions

Reject or revise the direction when:

- replacing the company name with a competitor leaves the experience equally valid
- the hero relies on an atmospheric backdrop without an inspectable subject
- the concept exists only in copy while layout and media remain generic
- the signature object cannot be produced credibly
- the media language ends after the hero
- the selected donors imply different worlds or dominant interactions
- conversion feels attached rather than earned
- mobile removes the central idea instead of recomposing it
- the concept requires invented evidence
- implementation would become a collection of effects rather than one experience
