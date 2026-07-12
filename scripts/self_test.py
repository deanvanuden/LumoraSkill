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
    plan["company_truth"].update(
        {
            "status": "locked",
            "name": "Fixture Company",
            "offer": "A factual service used for Lumora tests.",
            "audience": "People evaluating the fixture service.",
            "difference": "Its visible handoff process is unique to the test brief.",
            "proof": ["A supplied process artifact"],
            "material_world": ["handoff document", "work surface", "final artifact"],
            "place_or_context": "A real working environment",
            "vocabulary": ["inspect", "handoff", "deliver"],
            "real_routes": ["contact"],
            "available_media": ["supplied process artifact"],
            "missing_facts": [],
        }
    )
    plan["direction_exploration"].update(
        {
            "status": "locked",
            "concepts": [
                {
                    "id": f"world-{index}",
                    "name": f"Fixture world {index}",
                    "company_truth": "The visible handoff process.",
                    "experience_world": f"A distinct working environment organized around handoff state {index}.",
                    "signature_object": f"Handoff artifact {index}",
                    "transformation": "The artifact moves from input to inspected output.",
                    "hero_scene": "One inspectable artifact establishes the opening state.",
                    "asset_strategy": "Use supplied evidence plus authored process details.",
                    "risk": "The process could become too abstract without the real artifact.",
                    "why_only_this_company": "The states and language come from this exact handoff process.",
                }
                for index in range(1, 4)
            ],
            "selected_concept_id": "world-2",
            "selection_reason": "World 2 turns the strongest real process into one coherent interaction.",
            "rejected_concepts": ["World 1 was too literal.", "World 3 required unsupported media."],
        }
    )
    direction = plan["creative_direction"]
    direction["status"] = "locked"
    direction["creative_thesis"] = "Make the real offer legible through a subject-specific visual and interaction system."
    direction["experience_world"] = "A precise handoff table where one real artifact changes state as evidence accumulates."
    direction["signature_object"] = "The supplied handoff artifact"
    direction["signature_motif"] = "A factual object or process from the brief controls crops and transitions."
    direction["material_language"] = "Uncoated paper, registration marks, and neutral work surfaces."
    direction["spatial_logic"] = "One anchored artifact with evidence entering from its working edges."
    direction["camera_behavior"] = "A stable overhead view moves closer only when proof is introduced."
    direction["transformation"] = "The artifact changes from unverified input to registered output."
    direction["emotional_arc"] = "Uncertainty becomes clarity and then readiness to act."
    direction["interaction_thesis"] = "Scroll advances the real handoff states while controls inspect details."
    direction["company_specificity_test"] = "The motif, copy, and media stop making sense when replaced with another company."
    direction["substitution_failure"] = "A competitor without this handoff artifact cannot use the same world or choreography."
    direction["category_conventions"] = ["Generic service cards", "Stock team photography"]
    direction["deliberate_departure"] = "The real handoff artifact replaces generic service imagery and controls the entire experience."
    for key in direction["narrative_arc"]:
        direction["narrative_arc"][key] = f"The {key} chapter advances the handoff artifact toward verified delivery."
    for key in ("composition", "typography", "palette_logic", "material", "media_mode", "shape_language", "section_rhythm", "signature_motion", "structural_motion"):
        direction["design_fingerprint"][key] = f"fixture {key.replace('_', ' ')}"
    for keyframe in direction["experience_keyframes"]:
        keyframe["description"] = f"A concrete {keyframe['id']} state of the handoff artifact."
        keyframe["reference_asset"] = f"work/{keyframe['id']}.png"
    for item in direction["originality_scorecard"]:
        item["score"] = 2
        item["evidence"] = f"The fixture visibly proves {item['dimension']} through its handoff world."

    plan["source_selection"].update(
        {
            "status": "locked",
            "inspected_candidates": [item["id"] for item in plan["source_selection"]["candidate_shortlists"]["anchor"][:3]],
            "compatibility_statement": "The anchor owns the page world; each support contributes one local behavior without another hero or scroll narrative.",
            "rejected_candidates": ["Rejected one alternate anchor after full inspection."],
        }
    )
    source_ids = [source["id"] for source in plan["source_mix"]]
    for source in plan["source_mix"]:
        contribution_count = 3 if source["job"] == "anchor" else 1
        source["implemented_contributions"] = [f"Use {source['job']} contribution {index + 1} as a visible, bounded decision." for index in range(contribution_count)]
        source["implemented_sections"] = ["fixture", "proof"] if source["job"] == "anchor" else ["fixture"]
        source["compatibility_resolution"] = "Any source risks are neutralized by preserving the anchor's world and limiting this donor to the fixture section."
    anchor_id = plan["source_mix"][0]["id"]
    plan["source_to_section_map"] = [
        {
            "section_id": "fixture",
            "purpose": "validator fixture",
            "source_jobs": [source["job"] for source in plan["source_mix"]],
            "source_ids": source_ids,
            "implementation_notes": ["Smoke-test mapping"],
        },
        {
            "section_id": "proof",
            "purpose": "anchor proof",
            "source_jobs": ["anchor"],
            "source_ids": [anchor_id],
            "implementation_notes": ["Anchor-only proof chapter"],
        },
    ]
    plan["media_plan"].update(
        {
            "status": "locked",
            "asset_strategy": "Use one real artifact as the signature subject and authored detail crops as a coherent supporting family.",
            "asset_coverage_review": "Every prominent slot has a distinct truthful asset and no hero image is reused as filler.",
        }
    )
    plan["media_plan"]["signature_asset"].update(
        {
            "status": "authored",
            "role": "Inspectable hero artifact",
            "subject": "The supplied handoff document",
            "medium": "Art-directed raster still",
            "company_reason": "It is the real object that embodies the service process.",
            "source_or_generation_method": "Supplied evidence with an authored project-local treatment.",
        }
    )
    for key in plan["media_plan"]["continuity_bible"]:
        plan["media_plan"]["continuity_bible"][key] = f"Locked fixture {key.replace('_', ' ')} direction."
    for reference in plan["media_plan"]["reference_set"]:
        reference["status"] = "selected"
        reference["prompt"] = f"Create the {reference['id']} implementation frame for the locked fixture world."
        reference["analysis"] = f"The {reference['id']} frame confirms composition, media role, crop, and hierarchy."
    plan["media_plan"]["slots"] = [
        {
            "id": "hero-media",
            "role": "hero subject",
            "page": "index.html",
            "aspect_ratio": "16:9",
            "target_render": "1200x675",
            "focal_point": "artifact center at 55% x and 45% y",
            "source": "authored test fixture",
            "truthfulness": "Uses the supplied artifact without adding claims.",
            "reuse": "Hero only",
        }
    ]
    plan["motion_plan"].update(
        {
            "status": "locked",
            "structural_language": "Evidence enters through one restrained registration reveal.",
            "micro_interactions": ["Tactile action state", "Visible keyboard focus"],
            "dependency_strategy": "Progressive enhancement with static content when motion code is unavailable.",
            "competing_systems_removed": ["No autoplay carousel", "No second scrubbed chapter"],
        }
    )
    plan["motion_plan"]["dominant_interaction"].update(
        {
            "name": "Registered handoff",
            "subject": "The handoff artifact",
            "input": "Native scroll",
            "transformation": "Input marks align and resolve into inspected output.",
            "narrative_purpose": "Explain how the service turns uncertain input into a verified delivery.",
            "desktop_implementation": "A bounded transform and opacity sequence tied to one stable chapter.",
            "mobile_recomposition": "Three explicit artifact states in normal vertical flow.",
            "reduced_motion": "All three states remain visible without scrub or autoplay.",
        }
    )
    plan["motion_plan"]["choreography_beats"] = [
        {"beat": f"Beat {index}", "trigger": f"Chapter progress {index}", "visible_change": f"Artifact state {index} becomes visible.", "exit_condition": f"State {index} is fully legible.", "fallback": f"Static state {index}."}
        for index in range(1, 4)
    ]
    plan["conversion_plan"].update(
        {
            "primary_action": "Contact the fixture company",
            "truthful_destination": "A real mailto route",
            "readiness_moment": "After the verified output state",
            "story_integration": "The final action is presented as the next handoff.",
            "secondary_actions": [],
        }
    )
    plan["director_review"].update(
        {
            "status": "passed",
            "revision_rounds": 1,
            "strongest_decision": "The real artifact controls the entire experience.",
            "weakest_decision": "The initial proof transition was too generic.",
            "generic_risks": ["Generic reveal timing"],
            "revisions_required": ["Tie reveal timing to registration marks."],
            "revisions_completed": ["Rebuilt the reveal around registration marks."],
        }
    )
    plan["verification"]["visual_review"].update(
        {
            "status": "passed",
            "checked_states": ["desktop-entry", "desktop-25", "desktop-50", "desktop-75", "desktop-close", "mobile-entry", "mobile-full", "reduced-motion"],
            "dead_space_review": "Every viewport contains an intentional visible state.",
            "reference_comparison": "The fixture preserves the reference hierarchy and artifact framing.",
            "mobile_recomposition_review": "Mobile uses three explicit states without overlap.",
            "interaction_review": "Controls, focus, and fallbacks remain truthful.",
            "revisions_after_review": ["Tightened the proof chapter spacing."],
        }
    )


def fixture_html(source_ids: list[str], title: str, home: bool) -> str:
    nav = '<a href="#main">Skip to content</a>' if home else '<a href="./index.html">Home</a>'
    source_attr = ",".join(source_ids)
    anchor_id = source_ids[0]
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
    <section id="proof" data-lumora-source="{anchor_id}"><h2>Proof</h2><p>The fixture exposes its anchor-led evidence.</p></section>
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
        plan = lumora_plan.build_plan(brief, disk_index, prompt_text, "auto", None, 3)
        assert plan["profile"]["name"] == expected_profile
        ids = tuple(source["id"] for source in plan["source_mix"])
        assert 1 <= len(ids) <= 3 and len(set(ids)) == len(ids)
        assert plan["source_mix"][0]["job"] == "anchor"
        assert len(plan["source_selection"]["candidate_shortlists"]["anchor"]) >= 3
        assert all(source["compatibility"]["score"] >= -8 for source in plan["source_mix"][1:])
        plans.append(plan)
        source_sets.append(ids)
    assert len(set(source_sets)) == len(source_sets), "different company profiles produced identical source mixes"

    anchor_only = lumora_plan.build_plan(BRIEFS[0][1], disk_index, prompt_text, "auto", None, 1)
    assert len(anchor_only["source_mix"]) == 1 and anchor_only["source_mix"][0]["job"] == "anchor"
    assert set(anchor_only["source_selection"]["candidate_shortlists"]) == {"anchor", "experience", "conversion"}

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

        (root / "styles.css").write_text(
            ".long-track{height:260vh} @media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}\n",
            encoding="utf-8",
        )
        (root / "script.js").write_text(
            "const a={scrub:true};const b={scrub:.5};setInterval(()=>{},1000);"
            "document.addEventListener('pointerdown',()=>document.body.scrollBy({left:1}));\n",
            encoding="utf-8",
        )
        warning_auditor = validate_lumora_site.Auditor(root, root / "lumora-plan.json")
        warning_codes = {finding.code for finding in warning_auditor.run() if finding.severity == "warning"}
        assert {"motion.multiple-scrubs", "motion.competing-systems", "motion.long-scroll"}.issubset(warning_codes)

    print("Lumora self-test passed: 254 prompts indexed, 4 profiles planned, prompt excerpts loaded, clean audit verified, motion-risk warnings verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
