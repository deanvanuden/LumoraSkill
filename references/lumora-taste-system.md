# Lumora Taste System

Use this reference after section selection and before coding. Its job is to make the selected sections look premium without letting the image pass replace the section library.

## Core Rule

Section recipes control structure. The generated or supplied reference image controls the visual skin.

Do not let the image pass invent a new page. Do not let the section recipes produce a generic unstyled stack. The final site should feel like selected MotionSites-derived sections translated into one coherent brand world.

## Image-First Workflow

For visual websites, generate or inspect a reference image before implementation.

Use image generation when:

- no strong visual references are supplied
- no usable product/source media exists
- the request is for a premium landing page, product page, marketing site, portfolio, agency site, ecommerce site, or redesign
- the page depends on art direction, composition, imagery, or motion feel

After image generation, inspect the result and write down:

- hero composition
- section rhythm
- typography character
- approximate type scale
- spacing density
- palette and contrast
- card/panel shape language
- media frame proportions
- CTA/button treatment
- motion cues
- details to avoid because they are not implementable

Then code the website.

## Visual Adaptation Boundaries

Allowed:

- change palette through CSS variables
- change font family and type mood
- adjust spacing rhythm
- adjust border radius, card finish, buttons, and shadows
- create media frames that match the reference
- use generated/source images in the recipe's media slots
- add restrained motion that matches the recipe interaction atoms

Not allowed:

- discard selected recipe structure
- replace selected sections with a generic page layout
- add unrelated sections just because the image looks nice
- make every section a centered text/card block
- convert image-led sections into text-only cards
- use placeholder visual boxes when imagery is needed

## Static Design Standards

- Use semantic HTML and accessible controls.
- Keep cards at stable aspect ratios and prevent layout shift.
- Use `clamp()` for width/spacing constraints, but do not scale font size only by viewport width.
- Use CSS variables instead of scattered one-off colors.
- Use one font system and one button system across every page.
- Use generous section spacing, but keep compact panels from using hero-sized typography.
- Avoid one-note palettes where the whole site becomes only purple/blue, beige, dark slate, or orange/brown.
- Avoid decorative orbs, generic blobs, and fake complexity.
- Avoid generic startup phrases such as "revolutionize", "next-gen", and "seamless" unless the source copy requires them.

## Premium Static Patterns

Use these patterns when they fit the selected recipes:

- Detached pill nav with mobile overlay.
- Product/object-led hero with a strong media frame.
- Editorial split hero with short H1 and generous negative space.
- Proof strip or metrics band directly after the hero.
- Bento or asymmetrical grid for feature density.
- Tabs or accordions for ingredient, workflow, feature, or FAQ detail.
- Purchase/plan selector with live state in vanilla JS.
- Review quote wall with constrained card sizes.
- Final CTA that is visually distinct but shares the same brand tokens.

## Motion Rules

- Use `IntersectionObserver` for scroll reveals.
- Animate `transform` and `opacity`; avoid layout-triggering animation.
- Respect `prefers-reduced-motion`.
- Use custom cubic-bezier easing rather than default linear/ease-in-out.
- Turn off sticky, pinned, or parallax behavior on mobile if it risks overlap or scroll trapping.

## Media Direction

- Use images as structural content, not decoration.
- Product and ecommerce sites need credible object/product imagery.
- Local service sites need believable service imagery, maps, location, or proof media.
- SaaS sites need coded UI frames, dashboard crops, or product-interface visuals.
- Portfolio and agency sites need real project/work image moments.
- If no media exists, generate assets for the specific slot before coding.

## Final Visual Check

Before final delivery, compare the built site against the reference image:

- same broad palette and contrast
- similar hero balance
- similar media frame logic
- similar button finish
- similar section density
- similar typography mood
- no generic template drift

The coded result does not need to be a pixel-perfect copy, but it must clearly belong to the same visual world.
