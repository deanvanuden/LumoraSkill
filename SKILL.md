---
name: lumora
description: Premium website and landing-page design/build workflow inspired by a categorized MotionSites archetype catalog. Use when Codex is asked to make, redesign, improve, or generate a high-quality website, landing page, hero section, SaaS site, agency site, portfolio, ecommerce page, waitlist, signup page, presentation-like web page, or visually rich frontend using "$lumora" or "Lumora"; also use when the user asks to mix prompt styles, choose website prompt directions, or create motion-heavy/cinematic web experiences.
---

# Lumora

Use Lumora to turn a company brief into a polished website direction and implementation. Select relevant archetypes from the bundled MotionSites prompt library, synthesize an original design brief, build the site, then verify it visually.

The bundled MotionSites prompt library is included under owner-approved commercial redistribution permission reported by the skill maintainer on 2026-06-12. See `references/permissions.md`. Treat it as a licensed bundled resource: use it to search, compare, and compose website directions, but prefer transforming selected prompts into an original implementation brief for each website instead of pasting large source prompts into chat.

## Workflow

1. Gather the brief:
   - Company/product name, offer, audience, conversion goal, must-have sections, brand constraints, reference sites/images, target stack, and whether this is a new build or redesign.
   - If details are missing, make practical assumptions and continue unless the missing detail would change the business goal.

2. Select archetypes:
   - Read `references/archetype-catalog.md` for the visible MotionSites archetype index.
   - If `references/motionsites-prompt-library.json` exists, use it as the bundled prompt-body library. Search it locally for matching industries, page types, and visual patterns; do not paste large prompt bodies into the chat unless the user explicitly asks for a specific prompt.
   - Optionally run `python scripts/select_lumora_archetypes.py "<brief text>"` to get a first-pass shortlist.
   - For substantial websites, run `python scripts/compose_lumora_brief.py "<brief text>"` and use the source pack as the main planning artifact. It mines prompt bodies into roles and reusable atoms without dumping full source prompts.
   - To refresh the bundled prompt-body library, run `python scripts/scrape_motionsites_prompts.py`. Premium bodies require an authenticated MotionSites access token in `MOTIONSITES_ACCESS_TOKEN`.
   - Pick 3-6 archetypes with distinct roles:
     - **Market fit**: closest industry/page type.
     - **Visual engine**: strongest atmosphere, motion, 3D, cinematic, or image direction.
     - **Conversion pattern**: signup, contact, waitlist, ecommerce, booking, pricing, trust, or demo flow.
     - **Restraint counterweight**: a quieter reference that prevents overdesigned pages when the company needs clarity.

3. Compose an original Lumora brief:
   - Read `references/composition-system.md` before major builds.
   - Read `references/deep-library-workflow.md` when the build should use the full bundled prompt library or when the first output feels good but not deep enough.
   - Name the chosen archetypes and explain what each contributes in one sentence.
   - Convert source-pack atoms into original instructions for layout, hierarchy, assets, motion, color, type, components, responsive behavior, and conversion flow.
   - Assign every major section a job and at least one source atom before coding.
   - Prefer one strong visual idea over a collage of effects.

4. Build the website:
   - Match the existing project stack and conventions when editing a repo.
   - For new static work, create the simplest viable app that supports the requested experience.
   - Use real visual assets, generated bitmap assets, video, canvas, WebGL, or code-native visuals when the experience needs them.
   - Make the first viewport immediately communicate the brand/product/object and leave a hint of the next section visible.
   - Build complete states and core flows, not a static poster.

5. Quality pass:
   - Verify desktop and mobile layouts in a browser.
   - Check text fit, overflow, contrast, responsive navigation, animation performance, asset loading, and console errors.
   - Revise until the page feels deliberate, not like a generic AI landing page.

## Selection Rules

Use these default mappings when the request is underspecified:

- **AI/SaaS/workflow**: start with Minimal Workflow SaaS, AI Workflow Hero, Growth Marketing SaaS, ClearInvoice SaaS Hero, CoderCrest, or AuraMail.
- **Agency/creative studio**: start with Velorah, Modern Agency, Creative Studio, Bold Studio, Prisma Creative Studio, or Framelix 3D Studios.
- **Portfolio/personal brand**: start with 3D Portfolio, Portfolio Cosmic, Bold Portfolio Hero, Dark Portfolio Hero, xPortfolio Hero, or Viktor Portfolio.
- **Luxury/product/real estate/travel**: start with Luxury Real Estate, Luxury Ecommerce Design, SkyElite Private Jets, Yacht Club, Scenic Travel, or Zenith Realty.
- **Fintech/crypto/Web3**: start with FinFlow, Evergreen Finance, Veloce Finance, RIVR DeFi, Web3 EOS Hero, Orbit Web3, or Orbis NFT.
- **Security/data/IT**: start with Securify Data Security, Guardnet, Cybersecurity Hero, AKOR Security, Nexus IT Solutions, or VaultShield.
- **High-drama/cinematic/3D**: layer in Pulse 3D, 3D Collectible Hero, Cinematic Landing Page, Cinematic Brand, Reveal Hero, Layered Depth, or Futuristic Cinematic.
- **Conversion utility**: layer in No-Code Waitlist, Waitlist Hero, NovaDesk Signup, Aurora Onboard, Build With Us, or Datacore Booking.

## Output Standard

Every Lumora build should include:

- A clear concept sentence that can guide implementation.
- A selected archetype mix with each archetype's purpose.
- A source-pack summary for substantial builds: market fit, visual engine, information architecture, conversion, motion, and restraint roles.
- A high-fidelity page structure with section-by-section intent.
- A concrete visual system: type scale, palette, layout rhythm, imagery/media, motion behavior, and component shape language.
- Responsive and interaction behavior.
- Implementation and verification steps appropriate to the repo.

Avoid:

- Removing the permission/provenance note when redistributing the bundled prompt library.
- Generic purple SaaS gradients, decorative blobs, nested cards, and vague hero copy.
- Motion without product meaning.
- Asset placeholders when the site depends on visual credibility.
- Overbuilding a marketing landing page when the user asked for an operational tool.
