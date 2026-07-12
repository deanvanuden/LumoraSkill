# Lumora Crash-Safe Headless QA

## Purpose

Lumora requires rendered evidence, but the Codex Desktop in-app Browser connector is unstable in the target environment. All source-site inspection and rendered QA therefore use terminal processes. This is a transport constraint, not a reduction in quality.

## Absolute Prohibition

Never use:

- `browser:control-in-app-browser`
- any browser-control MCP action
- `Connect to site preview`
- `Inspect site browser controls`
- an attached in-app page, tab, or authenticated browser session
- a visible `--headed` Playwright window

Do not retry the in-app connector after a failure. Do not use it because another skill suggests a visual browser check. Lumora's terminal-only policy wins for the entire task.

Safe tools are:

- terminal HTTP clients such as `curl`, `curl.exe`, or `Invoke-WebRequest`
- ordinary search and noninteractive page-fetch results
- terminal-only Playwright CLI in headless mode
- local filesystem screenshots inspected with `view_image`
- static HTML, CSS, JavaScript, media, and Lumora validation scripts

## Source-Site Inspection

For a public source site:

1. Fetch `robots.txt`, `sitemap.xml`, navigation HTML, and known routes with terminal HTTP tools.
2. Use public search results to discover routes, company facts, and external destinations.
3. Download only the material needed for inspection into a source archive outside the publishing root.
4. Use terminal-headless Playwright only when client rendering is required to reveal navigation, text, screenshots, or interaction state.
5. Record the discovered routes and migration decisions in `lumora-plan.json`.

When the only available authentication is inside Codex's in-app browser, stop that inspection path. Ask the user for exported HTML, screenshots, downloaded assets, or another noninteractive source. Never attach to the authenticated in-app session.

## Exact Publishing Root

Keep runtime and QA evidence separate:

```text
project/
  work/
    lumora-qa/
      playwright-cli.json
      screenshots/
      traces/
      reports/
  site/
    index.html
    404.html
    lumora-plan.json
    assets/
```

`site/` is the exact GitHub Pages root. Start the local server from it. Store screenshots, snapshots, traces, and reports in `work/lumora-qa/`, never in `site/`.

## Start A Terminal Server

Launch a persistent terminal process bound to loopback:

```bash
python -m http.server 4173 --bind 127.0.0.1 --directory "<exact-publishing-root>"
```

Use another free port when necessary. Do not click a site-preview or connect-browser action. Keep the terminal session ID so it can be polled and stopped deliberately after QA.

## Configure Headless Playwright

Load the `playwright` skill for its terminal CLI instructions and wrapper. Do not use the in-app Browser skill. Run the CLI from the external QA directory so artifacts cannot enter the published site.

Create `work/lumora-qa/playwright-cli.json`:

```json
{
  "browser": {
    "launchOptions": {
      "headless": true
    },
    "contextOptions": {
      "viewport": { "width": 1440, "height": 1000 },
      "reducedMotion": "no-preference"
    }
  }
}
```

Use one named session per QA mode:

```bash
pwcli --session lumora-desktop --config ./playwright-cli.json open http://127.0.0.1:4173/
pwcli --session lumora-desktop snapshot
pwcli --session lumora-desktop screenshot
pwcli --session lumora-desktop console
pwcli --session lumora-desktop network
pwcli --session lumora-desktop close
```

Never add `--headed`. If the CLI reports a rendering problem, diagnose it through screenshots, DOM snapshots, console output, network output, and source inspection.

## Required Render Matrix

Use separate named sessions or explicit resize commands for:

- `320 x 780`
- `360 x 800`
- `390 x 844`
- `430 x 932`
- `768 x 1024`
- `1024 x 900`
- `1440 x 1000`
- `1920 x 1080` when full-bleed media, canvas, film, 3D, or pinned framing needs it

Capture:

- desktop entry, 25 percent, 50 percent, 75 percent, and close
- mobile entry, live mobile-signature state, and full flow
- one tablet state
- reduced-motion entry and representative complete state
- menus, dialogs, selectors, galleries, forms, errors, success, media, canvas, and 3D states that materially affect the experience
- every route at `390` and `1440`; interaction-heavy routes across the full matrix

Use native mouse-wheel, keyboard, click, tap-sized pointer, and drag commands through the CLI. Take a fresh DOM snapshot before using element references and after major state changes.

## Containment Evidence

Terminal Playwright evaluation is appropriate for precise geometry. At every required width collect:

```js
JSON.stringify({
  clientWidth: document.documentElement.clientWidth,
  scrollWidth: document.documentElement.scrollWidth,
  overflow: [...document.querySelectorAll('*')]
    .map((element) => ({
      element,
      rect: element.getBoundingClientRect()
    }))
    .filter(({ rect }) => rect.left < -1 || rect.right > document.documentElement.clientWidth + 1)
    .map(({ element, rect }) => ({
      selector: element.id ? `#${element.id}` : element.className || element.tagName,
      left: Math.round(rect.left),
      right: Math.round(rect.right),
      width: Math.round(rect.width)
    }))
})
```

Record actual values and overflowing selectors in `verification.responsive_review`. Intentional inner scrollers still need bounded parents and must not increase root `scrollWidth`. Never solve the measurement by clipping `html`, `body`, or `:root`.

## Reduced Motion

Create a second config with:

```json
{
  "browser": {
    "launchOptions": { "headless": true },
    "contextOptions": {
      "viewport": { "width": 1440, "height": 1000 },
      "reducedMotion": "reduce"
    }
  }
}
```

Open a fresh named session with that config. Verify all content, routes, controls, media fallbacks, and conversion remain available without scrub, autoplay dependency, parallax, or large camera movement.

## Local Screenshot Review

After terminal Playwright writes screenshots:

1. Locate the exact image files in `work/lumora-qa/`.
2. Inspect them with `view_image`; do not open them through an in-app browser page.
3. Compare entry, signature, decision, mobile, tablet, and reduced-motion states with the selected references.
4. Record composition, crop, dead space, motion continuity, route consistency, and revision notes in the plan.
5. Make at least one meaningful revision and rerun the affected states.

## Cleanup And Failure Handling

- Close every named Playwright session.
- Stop the local server only after required QA and user handoff are complete.
- Keep evidence outside the publishing root.
- If a terminal session hangs, terminate that terminal process and start one fresh headless session.
- If terminal Playwright remains unavailable, run static validation and report the missing render checks. Never fall back to the in-app Browser connector.

Set these plan fields truthfully:

```json
{
  "render_transport": "terminal-headless-playwright",
  "in_app_browser_used": false,
  "render_artifact_root": "../work/lumora-qa"
}
```

