# Lumora

Lumora is a Codex skill for directing and building company-specific, highly visual websites as complete static GitHub Pages projects. It combines a licensed MotionSites prompt library with a strict creative-direction, asset-generation, interaction-design, implementation, terminal-headless render review, and release-validation workflow.

Lumora does not choose a template and replace its copy. It researches the company, explores distinct experience worlds, selects one prompt as the dominant design-DNA anchor, generates a coherent media campaign, plans desktop and mobile choreography, redesigns every required route, and verifies the real published output.

Award-caliber is the quality target, not a promised award.

## What Lumora Produces

For a new project, Lumora defaults to a directly publishable static site:

```text
index.html
styles.css
script.js
404.html
.nojekyll
lumora-plan.json
assets/
```

It can also create multipage sites with shared design, navigation, motion, and content systems. Vite, React, Three.js, GSAP, canvas, shaders, video, or other tools may be used when the concept or existing codebase warrants them, but a framework is not introduced only because a source prompt mentions one.

Typical uses include:

- company and service websites
- products and ecommerce experiences
- SaaS and technical products
- studios, portfolios, and case studies
- events, venues, hospitality, and culture
- architecture, property, and place-based sites
- editorial and campaign websites
- complete redesigns of existing multipage sites

## Core Principles

1. **Company truth first.** The concept starts from real products, services, people, places, tools, materials, interfaces, language, processes, evidence, and routes.
2. **One coherent world.** One central subject, material language, spatial logic, and transformation govern the experience.
3. **Anchor-led prompt use.** One MotionSites prompt owns most of the design authority. Up to two donors may contribute narrowly bounded mechanics.
4. **A campaign, not one image.** Lumora plans signature, narrative, supporting, and utility assets, including mobile variants, cutouts, textures, masks, details, posters, and fallbacks.
5. **Motion with narrative purpose.** One dominant company-specific transformation is supported by authored moments later in the site. Mobile receives a real recomposed interaction, not a disabled hero.
6. **Every route is intentional.** Existing routes are redesigned, consolidated, redirected, or retired. Untouched legacy pages cannot ship beside a new homepage.
7. **The publish root is the product.** Validation runs against the exact directory GitHub Pages will publish, never against a smaller mirror.
8. **Crash-safe render evidence is required.** Lumora uses terminal-only headless Playwright, critiques local screenshots, revises, measures, and validates the result before handoff.

## Crash-Safe Tool Policy

Lumora never invokes or attaches Codex's in-app Browser connector. It does not use `Connect to site preview`, browser-control MCP actions, or visible `--headed` Playwright windows. This avoids a known Codex Desktop crash path.

Public source sites are inspected through terminal HTTP tools, ordinary noninteractive web results, downloaded source, or terminal-headless Playwright. Local sites are served by a terminal process and rendered with Playwright CLI in headless mode. Screenshots and traces stay outside the publishing root and screenshots are inspected directly from disk.

If terminal Playwright is unavailable, Lumora reports which render checks could not run. It never falls back to the in-app Browser connector. See [`references/headless-qa.md`](references/headless-qa.md).

## Install For Codex

### Option 1: Clone Directly

On Windows PowerShell:

```powershell
git clone https://github.com/deanvanuden/LumoraSkill.git "$env:USERPROFILE\.codex\skills\lumora"
```

On macOS or Linux:

```bash
git clone https://github.com/deanvanuden/LumoraSkill.git "$HOME/.codex/skills/lumora"
```

Start a new Codex task after installation. If Lumora does not appear in the skill picker, restart Codex so it rescans the skills directory.

### Option 2: Copy An Existing Checkout

Copy the repository folder to:

```text
~/.codex/skills/lumora
```

The installed directory must contain `SKILL.md` at its root:

```text
~/.codex/skills/lumora/SKILL.md
```

### Update An Installed Clone

```powershell
Set-Location "$env:USERPROFILE\.codex\skills\lumora"
git pull
python scripts/self_test.py
```

## Invoke Lumora

Use the skill picker or name it directly in the request. Depending on the Codex surface, direct invocation may appear as `$lumora` or `/lumora`.

Example:

```text
$lumora Build a complete website for Northline Instruments.

They manufacture hand-calibrated field sensors for environmental teams.
Audience: municipal and industrial field engineers.
Primary action: request a field demo.
Proof: supplied calibration reports and product photography.
Pages: home, instruments, calibration process, field cases, company, contact.
Visual references: attached campaign photography and current site URL.
Publish as a static GitHub Pages site.
```

Useful information to provide:

- company name and source URL
- offer, audience, differentiator, and primary action
- products, services, prices, projects, proof, and locations
- required pages and working destinations
- logo, brand files, fonts, images, video, screenshots, or documents
- visual references and explicit dislikes
- required integrations or external booking, commerce, and form URLs
- target repository or output directory

Lumora should still research available local and public material when the brief is short. It must not invent missing evidence.

## How The Workflow Works

### 1. Discovery And Route Inventory

Lumora inspects the workspace, supplied media, source site, and public information architecture. It records company facts, material vocabulary, evidence, conversion routes, available media, missing facts, and every public source route.

For an existing site, source downloads remain outside the publish directory. Every source route receives a migration decision:

- `redesigned`
- `consolidated`
- `redirected`
- `retired`

### 2. V5 Project Plan

Lumora runs:

```bash
python scripts/lumora_plan.py "<complete brief>" --output "<publish-root>/lumora-plan.json"
```

Important options:

```text
--pages auto|one|multi
--site-origin auto|new|existing
--max-sources 1|2|3
--seed <alternate-direction-seed>
```

The current schema is `lumora.project_plan.v5`. It contains enforceable contracts for:

- company truth
- existing-site origin and public route migration
- exact publishing root and route manifest
- three distinct creative worlds
- selected creative direction and originality score
- section-by-section composition
- prompt authority and source traceability
- layered asset campaign
- desktop and mobile signature behavior
- supporting motion and entry-to-close continuity
- conversion behavior
- responsive measurements
- visual review and completed revisions

### 3. Prompt Inspection And Selection

The bundled library currently indexes 254 MotionSites records, with 250 prompt bodies available and four recorded as unavailable. The planner ranks candidates by company profile and exposes separate shortlists for anchor, experience, and conversion roles.

Inspect a candidate in full:

```bash
python scripts/inspect_lumora_prompt.py --id <prompt-id> --full
```

Inspect focused evidence:

```bash
python scripts/inspect_lumora_prompt.py --id <prompt-id> --focus layout motion media
```

The chosen anchor owns roughly 70 to 80 percent of the page world. Supporting donors are optional and may solve only a named local need. Lumora extracts geometry, crop behavior, media roles, state logic, timing, interaction, and fallback ideas. It does not copy source branding, source media, or framework boilerplate into customer projects.

### 4. Three Creative Worlds

Before coding, Lumora proposes three genuinely different experiences. They must differ in central subject, spatial logic, transformation, campaign media, opening scene, and emotional arc, not just palette and typography.

The selected world defines:

- creative thesis
- signature object or environment
- material and camera language
- spatial logic and section rhythm
- dominant transformation
- typography and shape behavior
- company substitution failure
- entry, signature, and decision keyframes

### 5. Visual Direction And Asset Decomposition

When no complete visual system is supplied, Lumora uses image generation to create three connected implementation references: entry, signature state, and decision state. It inspects those frames before coding.

The references are then decomposed into final assets:

- `signature`: the central subject or scene
- `narrative`: distinct scenes and states that advance the story
- `supporting`: transparent cutouts, fragments, masks, depth, textures, props, details, and transitions
- `utility`: marks, icons, thumbnails, posters, social images, 404 media, loaders, and fallbacks

Asset targets use `page.html#section-id`, and implemented sections expose their integrated IDs through `data-lumora-assets`. Final assets are generated for their actual slots and aspect ratios. A reference frame is never shipped as a screenshot of a whole section. Generated imagery cannot impersonate real staff, premises, products, outcomes, reviews, awards, or credentials.

### 6. Composition And Multipage Architecture

Every major section on every route receives a composition-map entry defining:

- focal subject
- relationship between copy and media
- desktop geometry
- mobile order, crop, and bounds
- purpose of negative space
- motion moment

Every shipped HTML file appears in the route manifest. All pages use the same core typography, material, navigation, footer, motion grammar, and responsive discipline while retaining a route-specific focal subject and pacing.

### 7. Motion Constellation

Lumora plans:

- one dominant company-specific transformation
- a mobile-native version using scroll, tap, swipe, drag, time, pointer, or a bounded hybrid
- at least two supporting authored moments in distinct later sections
- one structural reveal language
- useful micro-interactions for controls and navigation
- reduced-motion and library-failure fallbacks

Generic fade-up reveals may support ordinary content but cannot be the entire site after the hero. Mobile cannot simply set the dominant animation to its final state unless the user requests reduced motion.

### 8. Static Implementation

The default runtime is semantic HTML, CSS, and JavaScript. Lumora may use local video, GSAP, Three.js, canvas, shaders, SVG, generated raster assets, or other fit-for-purpose media when the selected concept requires them.

All essential content exists without animation. Controls are real, routes work, forms use a truthful endpoint or destination, and local URLs remain compatible with GitHub project pages and custom domains.

### 9. Terminal-Headless Review And Revision

Lumora serves the exact publish directory through a terminal process, uses a named headless Playwright CLI session, and inspects local screenshot files. It never connects the in-app Browser or passes `--headed`.

The review covers:

- desktop entry, 25 percent, 50 percent, 75 percent, and close
- mobile entry, live signature state, and full page
- tablet and reduced-motion states
- all routes and meaningful interaction states
- console errors and failed requests
- canvas and 3D subject pixels when applicable

Responsive containment is measured at 320, 360, 390, 430, 768, 1024, and 1440 CSS pixels. Every route is checked at least at 390 and 1440. Root overflow clipping is prohibited because it conceals defects.

After the first complete render, Lumora records a creative-director critique, makes at least one meaningful revision, and rerenders the result.

### 10. Strict Release Validation

Run against the exact directory that will be published:

```bash
python scripts/validate_lumora_site.py --site-root "<publish-root>" --strict
```

The validator checks planning completeness, prompt integrity, route coverage, section traceability, asset layers, composition decisions, mobile and supporting motion, responsive evidence, GitHub Pages paths, accessibility basics, media behavior, placeholder URLs, generic copy, image reuse, motion risk, and required review evidence.

A zero-error audit is required. A passing audit does not replace visual judgment.

## Publish With GitHub Pages

1. Put the finished publishing root at the repository root, or configure the repository so the chosen `/docs` or Actions artifact is the exact validated root.
2. Confirm `index.html`, `404.html`, `.nojekyll`, and `lumora-plan.json` are present.
3. Push the repository to GitHub.
4. Open repository **Settings > Pages**.
5. Select the publishing branch and folder, or the configured Actions workflow.
6. Add a custom domain in Pages settings when ready.
7. Add a `CNAME` file only when the exact domain is known.

All runtime asset URLs should be relative. Root-absolute paths such as `/assets/hero.webp` can fail when Pages publishes under a repository path.

## Repository Structure

```text
SKILL.md                              Main Codex skill workflow
agents/openai.yaml                    Skill presentation metadata
references/creative-direction.md      Company-specific world exploration
references/prompt-remix.md            Anchor and donor authority model
references/asset-direction.md         Reference and final-asset campaign
references/media-motion.md            Motion hierarchy and choreography
references/implementation-craft.md    Composition and frontend craft
references/headless-qa.md              Crash-safe terminal rendering workflow
references/quality-gates.md            Headless render and release gates
references/github-pages.md            Static publishing contract
references/design-dna-index.json      Searchable prompt metadata
references/motionsites-prompt-library.json
                                      Licensed local prompt bodies
references/permissions.md             Reported redistribution permission
scripts/lumora_plan.py                V5 planner
scripts/inspect_lumora_prompt.py      Focused/full prompt inspection
scripts/validate_lumora_site.py       Strict publish-root validator
scripts/build_lumora_index.py         Library index builder
scripts/scrape_motionsites_prompts.py Authorized library collection tool
scripts/self_test.py                  Planner and validator regression suite
```

## Development And Verification

Run the complete local regression suite:

```bash
python scripts/self_test.py
```

Rebuild the design-DNA index after an authorized library update:

```bash
python scripts/build_lumora_index.py
```

Before publishing skill changes, verify:

- `python scripts/self_test.py` passes
- the installed `~/.codex/skills/lumora` copy matches the repository
- no generated customer project, source scrape, render cache, key, or temporary output was committed
- permission and attribution notes remain intact

## Permission And Content Boundaries

The MotionSites prompt library is included under the maintainer-reported permission documented in [`references/permissions.md`](references/permissions.md). The prompt bodies are design-research inputs for Lumora. Generated customer sites must not include the prompt library, prompt text, MotionSites example branding, protected example media, private endpoints, or credentials.

Lumora's truth rules also prohibit invented testimonials, reviews, staff, clients, awards, metrics, prices, product results, events, credentials, and documentary evidence.
