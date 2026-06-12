# Lumora

Lumora is a Codex skill for making premium websites and landing pages. It turns a company brief into a structured design direction, chooses relevant website archetypes from a bundled MotionSites-inspired prompt library, extracts reusable layout and motion patterns, builds the site in the current project stack, and verifies the result visually.

The skill is meant for prompts like:

```text
$lumora make a high-end website for Aurelia Roots, a botanical hair oil brand.
The page should feel premium, organic, product-led, and include shop conversion.
```

or:

```text
Use Lumora to redesign this SaaS landing page into something cinematic but still clear.
```

## What Lumora Does

Lumora gives Codex a repeatable website-building workflow:

- Picks relevant archetypes from the bundled prompt library.
- Builds a source mix with clear roles: market fit, visual engine, information architecture, conversion pattern, motion system, and restraint counterweight.
- Extracts reusable prompt atoms from prompt bodies without dumping the full source prompts into the chat.
- Converts those influences into an original implementation brief for the current company.
- Builds with the existing project stack when there is one.
- Verifies desktop and mobile layouts, console health, asset loading, text fit, and motion behavior.

The goal is not to copy a prompt verbatim. The goal is to use the prompt library as a design-pattern library and synthesize a new website direction for each project.

## How Codex Skills Work

Codex skills are folders that contain a required `SKILL.md` file and optional bundled resources such as scripts, references, and assets. Codex first sees only the skill metadata, then loads the full skill instructions when the task matches the skill or the user invokes it explicitly.

Lumora follows that structure:

```text
LumoraSkill/
  SKILL.md
  agents/
    openai.yaml
  references/
    archetype-catalog.md
    composition-system.md
    deep-library-workflow.md
    motionsites-prompt-library.json
    permissions.md
  scripts/
    compose_lumora_brief.py
    scrape_motionsites_prompts.py
    select_lumora_archetypes.py
```

Useful official Codex docs:

- Agent skills: https://developers.openai.com/codex/skills
- Codex config and state locations: https://developers.openai.com/codex/config-advanced

## Installation

### Option 1: Install With `$skill-installer`

In Codex, ask the built-in installer to install from this repository:

```text
$skill-installer install the lumora skill from https://github.com/deanvanuden/LumoraSkill
```

Codex detects newly installed skills automatically. If Lumora does not appear, restart Codex.

### Option 2: Download ZIP

Use this when you do not want to use Git directly.
These commands replace any existing Lumora folder at the target path.

PowerShell on Windows:

```powershell
$zip = "$env:TEMP\lumora-skill.zip"
$extract = "$env:TEMP\lumora-skill"
$target = "$HOME\.agents\skills\lumora"

Invoke-WebRequest "https://github.com/deanvanuden/LumoraSkill/archive/refs/heads/main.zip" -OutFile $zip
Remove-Item -LiteralPath $extract -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath $target -Recurse -Force -ErrorAction SilentlyContinue
Expand-Archive -LiteralPath $zip -DestinationPath $extract
New-Item -ItemType Directory -Force "$HOME\.agents\skills" | Out-Null
Move-Item -LiteralPath "$extract\LumoraSkill-main" -Destination $target
```

macOS or Linux:

```bash
curl -L "https://github.com/deanvanuden/LumoraSkill/archive/refs/heads/main.zip" -o /tmp/lumora-skill.zip
rm -rf /tmp/lumora-skill "$HOME/.agents/skills/lumora"
mkdir -p "$HOME/.agents/skills"
unzip -q /tmp/lumora-skill.zip -d /tmp/lumora-skill
mv /tmp/lumora-skill/LumoraSkill-main "$HOME/.agents/skills/lumora"
```

Restart Codex if the skill does not show up.

### Option 3: Manual Per-User Git Install

Clone the repository into your user skills folder.

PowerShell on Windows:

```powershell
New-Item -ItemType Directory -Force "$HOME\.agents\skills" | Out-Null
git clone https://github.com/deanvanuden/LumoraSkill.git "$HOME\.agents\skills\lumora"
```

macOS or Linux:

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/deanvanuden/LumoraSkill.git "$HOME/.agents/skills/lumora"
```

Restart Codex if the skill does not show up.

### Option 4: Manual Per-Repo Install

Use this when a project should carry Lumora with it for everyone working in that repo.

PowerShell on Windows:

```powershell
New-Item -ItemType Directory -Force ".agents\skills" | Out-Null
git clone https://github.com/deanvanuden/LumoraSkill.git ".agents\skills\lumora"
```

macOS or Linux:

```bash
mkdir -p ".agents/skills"
git clone https://github.com/deanvanuden/LumoraSkill.git ".agents/skills/lumora"
```

### Compatibility Note

Some existing Codex Desktop setups may already use `~/.codex/skills` for local personal skills. If your Codex installation lists skills from that location, you can clone Lumora there instead:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
git clone https://github.com/deanvanuden/LumoraSkill.git "$HOME\.codex\skills\lumora"
```

Use the location your Codex build scans. Current official Codex documentation lists `.agents/skills` locations for direct skill folders.

## Updating

If you installed with `git clone`, update with:

```bash
git -C "$HOME/.agents/skills/lumora" pull
```

PowerShell:

```powershell
git -C "$HOME\.agents\skills\lumora" pull
```

Restart Codex if the update does not appear immediately.

## How To Use

Invoke Lumora directly:

```text
$lumora build a premium website for a luxury architecture studio.
Audience: high-net-worth homeowners and developers.
Goal: project inquiry form.
Style: cinematic, editorial, restrained, image-led.
```

Or ask naturally:

```text
Use Lumora to make a high-quality landing page for a cybersecurity SaaS.
It should feel technical, trustworthy, and conversion-focused.
```

Good inputs:

- Company or product name.
- What the business sells.
- Target audience.
- Conversion goal.
- Required sections.
- Brand constraints.
- Visual references or competitors.
- Preferred stack or existing repo details.
- Any assets that must be used.

If details are missing, Lumora makes practical assumptions unless the missing detail would change the business goal.

## Internal Workflow

Lumora runs as a design/build pipeline inside Codex.

1. Gather the brief.
   Codex identifies the company, audience, offer, conversion goal, stack, brand constraints, visual references, and must-have sections.

2. Select archetypes.
   Codex can read `references/archetype-catalog.md` and run:

   ```bash
   python scripts/select_lumora_archetypes.py "<brief text>"
   ```

   This gives a fast shortlist of relevant website archetypes.

3. Build a deep source pack.
   For substantial websites, Codex runs:

   ```bash
   python scripts/compose_lumora_brief.py "<brief text>"
   ```

   This script searches the bundled prompt library, assigns source prompts to roles, and extracts normalized prompt atoms.

4. Compose an original brief.
   Codex uses `references/composition-system.md` and `references/deep-library-workflow.md` to turn the source pack into a page-specific plan.

5. Build the website.
   Codex follows the repo's existing stack and conventions. If there is no existing app, it creates the simplest viable site that supports the requested experience.

6. Verify and iterate.
   Lumora expects desktop and mobile browser checks, console checks, asset checks, text-fit checks, responsive checks, and interaction checks before the work is considered done.

## Source Pack Roles

A deep Lumora build usually mixes 3 to 6 prompt sources:

- Market fit: closest industry, audience, and proof style.
- Visual engine: main media idea, mood, composition, depth, or 3D/cinematic direction.
- Information architecture: section rhythm and story order.
- Conversion pattern: signup, contact, booking, ecommerce, pricing, cart, or trust flow.
- Motion system: scroll, reveal, hover, parallax, 3D, or transition behavior.
- Restraint counterweight: a calmer reference that keeps the page usable.

This role system prevents the output from becoming a collage of effects. One source can provide market language, another can provide product framing, another can provide motion, and another can provide conversion behavior.

## Scripts

### `scripts/select_lumora_archetypes.py`

Quick first-pass selector.

```bash
python scripts/select_lumora_archetypes.py "premium botanical ecommerce hair oil landing page"
```

Outputs a ranked archetype list with rough role hints.

### `scripts/compose_lumora_brief.py`

Deep prompt-library composer.

```bash
python scripts/compose_lumora_brief.py "AI automation agency website with demo booking"
```

Outputs a source pack:

- selected source mix
- role assignments
- extracted layout atoms
- visual atoms
- motion atoms
- conversion atoms
- implementation atoms
- build brief template

JSON output is also available:

```bash
python scripts/compose_lumora_brief.py "luxury real estate landing page" --format json
```

### `scripts/scrape_motionsites_prompts.py`

Maintainer utility for refreshing the bundled prompt library from MotionSites.

Premium prompt bodies require an authenticated MotionSites access token:

```bash
MOTIONSITES_ACCESS_TOKEN="..." python scripts/scrape_motionsites_prompts.py
```

PowerShell:

```powershell
$env:MOTIONSITES_ACCESS_TOKEN = "..."
python scripts/scrape_motionsites_prompts.py
```

Most users do not need this script. The repository already includes the bundled library.

## Prompt Library

The bundled library is stored at:

```text
references/motionsites-prompt-library.json
```

Current library state:

- 254 prompt records.
- 250 records include collected prompt bodies.
- Prompt bodies are used as source material for extraction and synthesis.
- Lumora is designed to transform those sources into original implementation briefs instead of pasting full prompt bodies into chat.

## Permission Notes

The bundled MotionSites prompt library is included based on maintainer-reported commercial-use access and owner approval to include the prompt library in the Lumora skill. Keep `references/permissions.md` with any redistributed copy.

Before broad public distribution, add exact written permission or license text if available. This README describes how the skill works; it is not a substitute for a formal license.

## Requirements

- Codex CLI, Codex IDE extension, or Codex app.
- Git for clone-based installation.
- Python 3 for the helper scripts.
- No Python package dependencies are required for the bundled scripts; they use the standard library.

Website builds may require whatever the target project already uses, such as Node, npm, pnpm, Vite, React, Tailwind, or Playwright.

## Troubleshooting

### Lumora does not appear in Codex

- Confirm the folder contains `SKILL.md`.
- Confirm it is inside a skill-scanned location such as `$HOME/.agents/skills/lumora` or a repo-local `.agents/skills/lumora`.
- Restart Codex.
- If using an older local setup that scans `~/.codex/skills`, install there instead.

### The output feels too generic

Ask Lumora to run the deep source-pack workflow with more specific business and visual constraints:

```text
$lumora rerun the source pack for this brief with stronger ecommerce, product ritual, organic luxury, and mobile conversion constraints.
```

### The output feels overdesigned

Ask Lumora to add a restraint counterweight:

```text
$lumora revise with a calmer restraint source. Keep the main visual idea, but simplify sections, motion, and component density.
```

### The wrong archetypes are selected

Give a narrower brief:

```text
$lumora use product ecommerce references, not SaaS or agency references. The conversion goal is checkout, not demo booking.
```

## Example

Prompt:

```text
$lumora make a one-page website for Aurelia Roots, a botanical hair oil.
It should be premium, organic, product-led, and include a shop section with bundle selection.
```

The deep source pack should prefer product and ecommerce sources such as luxury ecommerce, botanical, product, and shop patterns. Codex then turns those into a new page structure: hero, formula, ingredients, ritual, results, bundle selector, FAQ, and final CTA.

## Repository Status

This repository is a direct skill folder. It can be cloned into a Codex skill location as-is because `SKILL.md` lives at the repository root.
