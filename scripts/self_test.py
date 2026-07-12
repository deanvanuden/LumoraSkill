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
    contract = plan["build_contract"]
    contract.update(
        {
            "site_origin": "new",
            "publishing_root": ".",
            "route_strategy": "Ship a redesigned home route and a branded system-consistent not-found route from this exact directory.",
            "source_route_inventory": [],
            "route_migrations": [],
            "source_archive_location": "",
            "route_manifest": [
                {
                    "file": "index.html",
                    "status": "redesigned",
                    "purpose": "Primary fixture experience",
                    "shared_system": "Fixture typography, material, navigation, motion, and footer system",
                    "verified": True,
                },
                {
                    "file": "404.html",
                    "status": "system",
                    "purpose": "Branded not-found route",
                    "shared_system": "Fixture typography, material, navigation, motion, and footer system",
                    "verified": True,
                },
            ],
        }
    )
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
    direction["composition_map"] = [
        {
            "page": page,
            "section_id": section_id,
            "role": role,
            "focal_subject": "The supplied handoff artifact",
            "text_media_relationship": "Copy names the state visible in the adjacent artifact without competing with it.",
            "desktop_geometry": "A 5/7 text-to-artifact grid with a bounded 16:9 media frame.",
            "mobile_geometry": "A single-column state with copy before a viewport-capped 4:3 artifact crop.",
            "negative_space_intent": "Space isolates the active registration marks and keeps the next chapter visible.",
            "motion_moment": "Registration marks align as the chapter enters, then settle before reading begins.",
        }
        for page in ("index.html", "404.html")
        for section_id, role in (("fixture", "entry"), ("proof", "evidence"))
    ]

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
            "asset_decomposition_review": "The keyframe was decomposed into one signature artifact, two narrative views, two transparent registration details, and one utility mark.",
            "asset_coverage_review": "Every prominent slot has a distinct truthful asset and no hero image is reused as filler.",
        }
    )
    def asset(asset_id: str, role: str, medium: str, sections: list[str]) -> dict:
        return {
            "id": asset_id,
            "role": role,
            "medium": medium,
            "source": "Authored fixture evidence",
            "target_sections": sections,
            "integration": "Rendered as a project-local semantic media layer, not a flattened section screenshot.",
            "responsive_variants": ["desktop crop", "mobile crop"],
        }

    plan["media_plan"]["asset_layers"] = {
        "signature": [asset("signature-artifact", "Primary handoff subject", "art-directed raster", ["index.html#fixture"])],
        "narrative": [
            asset("input-state", "Unverified process state", "art-directed raster", ["index.html#fixture"]),
            asset("proof-state", "Verified output state", "art-directed raster", ["index.html#proof"]),
        ],
        "supporting": [
            asset("registration-cutout", "Transparent alignment detail", "transparent raster", ["index.html#fixture"]),
            asset("paper-grain", "Material continuity texture", "seamless raster texture", ["index.html#fixture", "index.html#proof"]),
        ],
        "utility": [asset("fixture-mark", "Navigation and favicon mark", "SVG", ["index.html#fixture", "404.html#fixture"])],
    }
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
            "text_relationship": "The title identifies the visible artifact state and remains outside the media.",
            "desktop_geometry": "Media occupies seven of twelve columns with a bounded 16:9 frame.",
            "mobile_geometry": "Media follows copy in a 4:3 crop capped below 62svh.",
            "motion_role": "The artifact is the subject of the dominant registration transformation.",
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
    plan["motion_plan"]["mobile_signature"].update(
        {
            "mode": "scroll",
            "input": "Native vertical scroll through a short bounded chapter",
            "subject": "The supplied handoff artifact",
            "visible_change": "Registration marks move from offset input to inspected output in three readable states.",
            "implementation": "A mobile-specific 4:3 crop advances CSS custom properties while content remains in normal flow.",
            "fallback": "Reduced motion shows the three complete states as a static vertical sequence.",
            "verified": True,
        }
    )
    plan["motion_plan"]["supporting_moments"] = [
        {
            "page": "index.html",
            "section": "fixture",
            "subject": "Registration detail",
            "trigger": "Section entry",
            "visible_change": "A small alignment mark resolves into place.",
            "purpose": "Reinforce the handoff language after the dominant state begins.",
            "desktop": "Translate and rotate a transparent cutout by a restrained amount.",
            "mobile": "Use a shorter transform inside the media bounds.",
            "reduced_motion": "Show the mark in its resolved position.",
        },
        {
            "page": "index.html",
            "section": "proof",
            "subject": "Evidence rule",
            "trigger": "Proof chapter entry",
            "visible_change": "The rule grows to the exact width of the verified artifact.",
            "purpose": "Connect proof to the same registration system without another spectacle.",
            "desktop": "Scale the rule from its left origin once.",
            "mobile": "Use the same one-shot scale within the content column.",
            "reduced_motion": "Render the complete rule immediately.",
        },
    ]
    plan["motion_plan"]["continuity_map"] = {
        "entry": "The artifact arrives offset and visibly unresolved.",
        "orientation": "Labels and marks establish how its states are read.",
        "deepening": "A supporting detail reveals the inspection method.",
        "evidence": "The proof rule resolves to the artifact's verified bounds.",
        "decision": "The completed artifact becomes the action surface.",
        "close": "The final mark remains as a quiet system signature.",
    }
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
            "checked_states": ["desktop-entry", "desktop-25", "desktop-50", "desktop-75", "desktop-close", "mobile-entry", "mobile-signature", "mobile-full", "tablet", "reduced-motion"],
            "dead_space_review": "Every viewport contains an intentional visible state.",
            "reference_comparison": "The fixture preserves the reference hierarchy and artifact framing.",
            "mobile_recomposition_review": "Mobile uses three explicit states without overlap.",
            "mobile_signature_review": "The mobile artifact transforms through all three states without becoming a tall static poster.",
            "motion_continuity_review": "Entry, supporting marks, proof rule, and close use one registration language.",
            "image_composition_review": "Desktop and mobile media-to-copy ratios remain deliberate with no accidental blank column.",
            "route_consistency_review": "Home and not-found routes share the same type, material, navigation, and motion system.",
            "interaction_review": "Controls, focus, and fallbacks remain truthful.",
            "revisions_after_review": ["Tightened the proof chapter spacing."],
        }
    )
    plan["verification"]["publishing_root_review"] = "Validated the exact directory containing every file that will be published by GitHub Pages; no mirror or source scrape is present."
    plan["verification"]["render_transport"] = "terminal-headless-playwright"
    plan["verification"]["in_app_browser_used"] = False
    plan["verification"]["render_artifact_root"] = "../work/lumora-qa"
    required_widths = [320, 360, 390, 430, 768, 1024, 1440]
    containment_results = [
        {
            "page": "index.html",
            "width": width,
            "client_width": width,
            "scroll_width": width,
            "overflow_elements": [],
            "pass": True,
        }
        for width in required_widths
    ]
    containment_results.extend(
        {
            "page": "404.html",
            "width": width,
            "client_width": width,
            "scroll_width": width,
            "overflow_elements": [],
            "pass": True,
        }
        for width in (390, 1440)
    )
    plan["verification"]["responsive_review"] = {
        "status": "passed",
        "tested_widths": required_widths,
        "containment_results": containment_results,
        "longest_content_checks": ["Longest title", "Longest action label", "Longest proof sentence"],
        "mobile_media_review": "At 320, 360, 390, and 430 pixels the artifact uses its mobile crop, stays within the viewport, and never exceeds 62svh.",
    }


def fixture_html(source_ids: list[str], title: str, home: bool) -> str:
    nav = '<a href="#main">Skip to content</a>' if home else '<a href="./index.html">Home</a>'
    source_attr = ",".join(source_ids)
    anchor_id = source_ids[0]
    fixture_assets = "signature-artifact,input-state,registration-cutout,paper-grain,fixture-mark" if home else "fixture-mark"
    proof_assets = "proof-state,paper-grain" if home else ""
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
    <section id="fixture" data-lumora-source="{source_attr}" data-lumora-assets="{fixture_assets}" data-lumora-motion="registration-align"><h1>{title}</h1><button type="button">Act</button></section>
    <section id="proof" data-lumora-source="{anchor_id}" data-lumora-assets="{proof_assets}" data-lumora-motion="evidence-rule"><h2>Proof</h2><p>The fixture exposes its anchor-led evidence.</p></section>
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
        assert plan["schema"] == "lumora.project_plan.v5"
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

    existing = lumora_plan.build_plan(
        "Redesign https://example.com and preserve working destinations for all routes, service pages, and legal pages.",
        disk_index,
        prompt_text,
        "auto",
        None,
        1,
    )
    assert existing["build_contract"]["site_origin"] == "existing"
    assert existing["build_contract"]["page_mode"] == "multi"
    source_url = lumora_plan.build_plan("Redesign https://example.com for the company.", disk_index, prompt_text, "auto", None, 1)
    assert source_url["build_contract"]["page_mode"] == "multi"
    homepage_only = lumora_plan.build_plan("Redesign the homepage only for https://example.com.", disk_index, prompt_text, "auto", None, 1)
    assert homepage_only["build_contract"]["page_mode"] == "one"

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

        unsafe_plan = json.loads(json.dumps(plan))
        unsafe_plan["verification"]["render_transport"] = "in-app-browser"
        unsafe_plan["verification"]["in_app_browser_used"] = True
        unsafe_plan["verification"]["render_artifact_root"] = "work/lumora-qa"
        (root / "lumora-plan.json").write_text(json.dumps(unsafe_plan, indent=2), encoding="utf-8")
        unsafe_codes = {finding.code for finding in validate_lumora_site.Auditor(root, root / "lumora-plan.json").run()}
        assert {"plan.render-transport", "plan.in-app-browser", "plan.render-artifacts-inside"}.issubset(unsafe_codes)
        (root / "lumora-plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")

        (root / "legacy.html").write_text(fixture_html(source_ids, "Unmanaged Legacy Route", False), encoding="utf-8")
        unmanaged_codes = {finding.code for finding in validate_lumora_site.Auditor(root, root / "lumora-plan.json").run()}
        assert "plan.route-unmanaged" in unmanaged_codes
        (root / "legacy.html").unlink()

        (root / "styles.css").write_text(
            "body{margin:0;overflow-x:hidden} section{min-height:100dvh} @media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}\n",
            encoding="utf-8",
        )
        overflow_findings = validate_lumora_site.Auditor(root, root / "lumora-plan.json").run()
        assert any(finding.code == "responsive.root-overflow-mask" and finding.severity == "error" for finding in overflow_findings)

        (root / "styles.css").write_text(
            ".long-track{height:260vh} @media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}\n",
            encoding="utf-8",
        )
        (root / "script.js").write_text(
            "const a={scrub:true};const b={scrub:.5};setInterval(()=>{},1000);"
            "document.addEventListener('pointerdown',()=>document.body.scrollBy({left:1}));"
            "const compact=matchMedia('(max-width: 820px)');if(compact.matches){document.body.style.setProperty('--p','1');}\n",
            encoding="utf-8",
        )
        warning_auditor = validate_lumora_site.Auditor(root, root / "lumora-plan.json")
        warning_codes = {finding.code for finding in warning_auditor.run() if finding.severity == "warning"}
        assert {"motion.multiple-scrubs", "motion.competing-systems", "motion.long-scroll", "motion.mobile-final-bypass"}.issubset(warning_codes)

    print("Lumora self-test passed: 254 prompts indexed, v5 profiles and existing-route inference planned, prompt excerpts loaded, clean audit verified, in-app browser use rejected, route and overflow regressions caught, motion-risk warnings verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
