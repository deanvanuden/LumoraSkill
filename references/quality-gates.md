# Lumora Quality Gates

## Gate 1: Source And Direction

- `lumora-plan.json` exists and matches the current company brief.
- The creative thesis, motif, design genome, page map, source hierarchy, source contributions, media slots, and motion map are concrete.
- Every selected source prompt was inspected; the foundation prompt was read in full.
- Every source contributes at least two implemented decisions.
- The result passes the company substitution test.

## Gate 2: Content And Conversion

- Company facts, products, services, prices, people, reviews, awards, and claims are sourced or visibly omitted.
- The primary conversion is obvious and works.
- Navigation, footer, cards, CTAs, forms, selectors, accordions, tabs, galleries, and menus have real behavior.
- There are no `href="#"`, `javascript:void(0)`, fake external URLs, empty buttons, or false success states.
- Multipage links work from every route.

## Gate 3: Visual Fidelity

- The coded result matches the visual reference in composition, hierarchy, spacing, crop language, color roles, and material treatment.
- The hero has one clear focal point and leaves a hint of the next chapter visible.
- Text does not overlap media or controls unintentionally.
- Long words, labels, prices, and CTA text fit their containers.
- Repeated cards and media frames keep stable dimensions.
- The page has at least one memorable company-specific moment and does not read as a generic template.

## Gate 4: Media

- Every prominent slot uses a deliberate local asset with sufficient resolution.
- Raster text, fake logos, watermarks, and unrelated stock imagery are absent.
- Generated assets do not impersonate real company evidence.
- Every cover crop has an intentional focal point.
- Videos have posters, useful compression, `muted`, and `playsinline` when autoplaying.
- Three.js or canvas scenes are nonblank, correctly framed, and have a static fallback.

## Gate 5: Responsive Containment

Test at minimum 1440 x 1000 and 390 x 844. Add a wide desktop viewport for full-bleed, pinned, or canvas work.

- `document.documentElement.scrollWidth <= document.documentElement.clientWidth`.
- No section bounding box covers unrelated previous or next content.
- Pinned, sticky, horizontal, stacked, and overlapping scenes have stable parents and explicit mobile behavior.
- Mobile is recomposed into usable document flow, not a shrunken desktop layout.
- Touch controls do not depend on hover.
- Fixed controls respect safe areas and do not cover content.
- Viewport-height sections use dynamic viewport units or safe minimums and still reveal the next chapter where appropriate.

## Gate 6: Motion And Performance

- One signature sequence, one structural reveal language, and restrained micro-interactions are present.
- Motion supports content and does not compete for attention across multiple sections.
- Reduced-motion mode exposes all content and disables scrub, parallax, autoplay, and large movement.
- GSAP/ScrollTrigger setups are responsive and cleaned up.
- Offscreen video, canvas, and perpetual motion pause where practical.
- Animation uses transform and opacity for continuous movement.
- There are no console errors, failed local assets, or repeated layout thrashing.

## Gate 7: Accessibility

- Semantic landmarks, heading order, labels, alt text, and accessible control names are present.
- Keyboard focus is visible and follows a logical order.
- Menus, dialogs, tabs, accordions, and carousels expose state through appropriate ARIA only where native semantics are insufficient.
- Contrast is readable over every media state.
- Controls meet a practical 44 by 44 CSS pixel touch target.
- The experience remains understandable without animation, audio, hover, or a precise pointer.

## Gate 8: GitHub Pages

- `index.html`, `404.html`, and `.nojekyll` exist in the publishing root.
- All local URLs are relative and case-correct.
- No secrets or prompt bodies are public.
- The site works from a local static server without a build step, unless a framework was explicitly retained.
- `CNAME` exists only for a supplied domain.
- Forms and dynamic features use real external endpoints or truthful fallbacks.

## Browser Verification

Use Playwright or the available browser tooling to:

1. Open every page and capture full-page desktop and mobile screenshots.
2. Exercise menus, route links, selectors, tabs, accordions, galleries, forms, and CTAs.
3. Inspect console errors and failed requests.
4. Check overflow and major section bounding boxes with page evaluation.
5. Emulate reduced motion and confirm all content remains visible.
6. For canvas, sample pixels or inspect a screenshot to prove the scene rendered.

Do not accept a build solely because the structural validator passes. The screenshots are the visual test.

## Automated Audit

Run:

```bash
python scripts/validate_lumora_site.py --site-root <site-root> --plan <site-root>/lumora-plan.json
```

Treat errors as blockers. Review warnings individually; fix any warning that reflects a real user-facing issue.

