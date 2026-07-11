#!/usr/bin/env python3
"""Run Lumora planner, prompt-inspection, and validator smoke tests."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import build_lumora_index
import inspect_lumora_prompt
import lumora_plan
import validate_lumora_site


BRIEFS = (
    (
        "product-commerce",
        "Premium botanical hair oil ecommerce site with ingredient proof, ritual, bottle selector, reviews, FAQ, and purchase.",
    ),
    (
        "saas-product",
        "B2B logistics SaaS with a real dispatch workflow, integrations, enterprise trust, pricing, and demo booking.",
    ),
    (
        "architecture-property",
        "Architecture studio full website with residential projects, material case studies, studio philosophy, and inquiry.",
    ),
    (
        "hospitality-place",
        "Neighborhood seafood restaurant with seasonal menu, chef story, food photography, reservations, hours, and location.",
    ),
)


def lock_plan(plan: dict) -> None:
    direction = plan["creative_direction"]
    direction["status"] = "locked"
    direction["creative_thesis"] = "Make the real offer legible through a subject-specific visual and interaction system."
    direction["signature_motif"] = "A factual object or process from the brief controls crops and transitions."
    direction["company_specificity_test"] = "The motif, copy, and media stop making sense when replaced with another company."
    source_ids = [source["id"] for source in plan["source_mix"]]
    for source in plan["source_mix"]:
        source["implemented_contributions"] = [
            f"Use the {source['job']} source's primary spatial relationship.",
            f"Use the {source['job']} source's interaction or media behavior.",
        ]
        source["implemented_sections"] = ["fixture"]
    plan["source_to_section_map"] = [
        {
            "section_id": "fixture",
            "purpose": "validator fixture",
            "source_jobs": [source["job"] for source in plan["source_mix"]],
            "source_ids": source_ids,
            "implementation_notes": ["Smoke-test mapping"],
        }
    ]
    plan["media_plan"]["slots"] = [
        {
            "id": "hero-media",
            "role": "hero subject",
            "aspect_ratio": "16:9",
            "source": "generated test fixture",
        }
    ]
    plan["motion_plan"]["desktop_implementation"] = "Bounded transform and opacity choreography."
    plan["motion_plan"]["mobile_recomposition"] = "Normal vertical flow with tap-safe controls."


def fixture_html(source_ids: list[str], title: str, home: bool) -> str:
    nav = '<a href="#main">Skip to content</a>' if home else '<a href="./index.html">Home</a>'
    source_attr = ",".join(source_ids)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Lumora validation fixture.">
  <title>{title}</title>
  <link rel="stylesheet" href="./styles.css">
</head>
<body>
  <nav>{nav}</nav>
  <main id="main">
    <section id="fixture" data-lumora-source="{source_attr}"><h1>{title}</h1><button type="button">Act</button></section>
  </main>
  <script src="./script.js"></script>
</body>
</html>
"""


def main() -> int:
    index = build_lumora_index.build_index(lumora_plan.DEFAULT_LIBRARY)
    assert index["counts"] == {"total": 254, "available": 250, "unavailable": 4}
    disk_index, _library, prompt_text = lumora_plan.load_inputs(lumora_plan.DEFAULT_INDEX, lumora_plan.DEFAULT_LIBRARY)

    plans: list[dict] = []
    source_sets: list[tuple[str, ...]] = []
    for expected_profile, brief in BRIEFS:
        plan = lumora_plan.build_plan(brief, disk_index, prompt_text, "auto", None, 5)
        assert plan["profile"]["name"] == expected_profile
        ids = tuple(source["id"] for source in plan["source_mix"])
        assert len(ids) == 5 and len(set(ids)) == 5
        plans.append(plan)
        source_sets.append(ids)
    assert len(set(source_sets)) == len(source_sets), "different company profiles produced identical source mixes"

    first_source = plans[0]["source_mix"][0]["id"]
    prompt = inspect_lumora_prompt.load_prompt(lumora_plan.DEFAULT_LIBRARY, first_source)
    excerpts = inspect_lumora_prompt.focused_excerpt(prompt["prompt_text"], ["layout", "motion"], 4000)
    assert excerpts and sum(len(item.body) for item in excerpts) <= 4000

    plan = plans[0]
    lock_plan(plan)
    with tempfile.TemporaryDirectory(prefix="lumora-self-test-") as tmp:
        root = Path(tmp)
        source_ids = [source["id"] for source in plan["source_mix"]]
        (root / "lumora-plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
        (root / "index.html").write_text(fixture_html(source_ids, "Fixture Home", True), encoding="utf-8")
        (root / "404.html").write_text(fixture_html(source_ids, "Page Not Found", False), encoding="utf-8")
        (root / "styles.css").write_text(
            "body{margin:0} section{min-height:100dvh} @media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}\n",
            encoding="utf-8",
        )
        (root / "script.js").write_text("document.documentElement.classList.add('js');\n", encoding="utf-8")
        (root / ".nojekyll").write_text("", encoding="utf-8")
        auditor = validate_lumora_site.Auditor(root, root / "lumora-plan.json")
        findings = auditor.run()
        errors = [finding for finding in findings if finding.severity == "error"]
        assert not errors, "validator fixture failed: " + "; ".join(error.message for error in errors)

    print("Lumora self-test passed: 254 prompts indexed, 4 profiles planned, prompt excerpts loaded, site audit clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
