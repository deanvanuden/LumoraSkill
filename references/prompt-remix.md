# MotionSites Prompt Remixing

## Purpose

The MotionSites library contains detailed Vite, React, Tailwind, motion, media, and interaction specifications. Lumora uses those prompts as design and engineering donors. It does not flatten them into generic section labels, and it does not copy their example brand, framework scaffold, or remote assets into the finished site.

## Inspection Order

1. Run `scripts/lumora_plan.py` against a complete brief.
2. Read the selected `foundation` prompt in full.
3. Read the `hero` prompt in full when the plan requests it; otherwise inspect layout, visual, media, motion, and responsive excerpts.
4. Inspect focused excerpts for narrative, motion, and conversion donors.
5. Return to the full source whenever an excerpt leaves behavior or geometry ambiguous.

Commands:

```bash
python scripts/inspect_lumora_prompt.py --id <prompt-id> --full
python scripts/inspect_lumora_prompt.py --id <prompt-id> --focus layout,visual,media,responsive
python scripts/inspect_lumora_prompt.py --id <prompt-id> --focus motion,interaction,responsive
```

Do not implement from the index, title, category, or selector summary alone. Those tools find candidates; the source body supplies the detail.

## Donor Authority

| Donor | Controls | Does not control |
| --- | --- | --- |
| Foundation | page silhouette, section cadence, broad grid, transitions between chapters | company copy, brand palette, all local interactions |
| Hero | first viewport, dominant media role, hero control or reveal | the whole page system |
| Narrative | one story, product, service, project, proof, or process mechanic | global navigation or closing flow |
| Motion | one signature choreography and its timing logic | unrelated layout or extra effects |
| Conversion | action hierarchy, selector, pricing, booking, inquiry, or closing mechanic | hero or global visual identity |

When donors conflict, keep the higher-authority source and drop or replace the conflicting donor. Do not compromise into a weaker hybrid.

## Preserve The Concept

Extract these invariants from each source:

- visual hierarchy and relative scale
- spatial relationships, overlap, pinning, and crop behavior
- media role and focal movement
- interaction states and user input
- animation sequence, timing relationships, and scroll mapping
- conversion placement and state changes
- responsive behavior and fallback logic

Preserve those invariants unless they conflict with accessibility, truthful content, mobile containment, or the company-specific creative thesis.

## Translate The Stack

| Source instruction | Static Lumora translation |
| --- | --- |
| React component/state | semantic HTML plus scoped DOM state and event listeners |
| Vite paths such as `/images/x.webp` | project-relative `./assets/images/x.webp` |
| Tailwind utility composition | project CSS classes and custom properties |
| Framer Motion entrance | CSS animation or GSAP timeline using equivalent timing and transform intent |
| Framer layout animation | FLIP-style GSAP animation or a simpler state transition that preserves the visible relationship |
| GSAP/ScrollTrigger | keep GSAP through pinned CDN scripts when the choreography needs it |
| React Three Fiber | use Three.js directly only if 3D is essential; otherwise create purpose-built raster or video media |
| component icon library | use an available thin icon library or accessible familiar symbols; do not hand-draw arbitrary SVGs |
| remote example image/video | source, download, or generate a company-specific local asset with the same role and crop |
| SPA route | real relative `.html` route or same-page anchor |
| package-only widget | implement the minimum static equivalent or choose a compatible donor |

Do not reproduce unused package lists, build config, placeholder routes, or example-company content.

## Contribution Ledger

Every selected source needs at least two visible contributions in `lumora-plan.json`:

```json
{
  "id": "source-id",
  "job": "motion",
  "contributions": [
    "Pinned product chapter with bounded scroll distance",
    "Image scale follows chapter progress and settles before copy changes"
  ],
  "sections": ["product-story"]
}
```

Use concrete descriptions. "Luxury feel" and "nice animation" are not contributions.

Mark implemented sections with `data-lumora-source`. One section may list multiple comma-separated IDs only when their responsibilities are different and documented. Keep prompt bodies out of the generated project.

## Compatibility Review

Before accepting a mix, check:

- Can all donors share one type system and palette without losing their hierarchy?
- Do sticky, horizontal, or scroll-locked concepts compete for the same part of the page?
- Does more than one donor try to control the hero or page shell?
- Can every media role be supplied with truthful, high-resolution assets?
- Can the effect degrade to normal document flow on mobile and reduced motion?
- Does the combined page still have a clear primary conversion?
- Is the total animation and dependency cost justified by the idea?

Replace a donor when the answer is no. The goal is a coherent authored site, not maximum library coverage.

## Source Security

- Keep `references/motionsites-prompt-library.json` inside the skill.
- Do not copy prompt bodies into website repositories, HTML comments, public JSON, screenshots, or reports.
- Store only prompt IDs, hashes, contribution notes, and section mappings in `lumora-plan.json`.
- Do not hotlink MotionSites preview or example media in generated customer sites.

