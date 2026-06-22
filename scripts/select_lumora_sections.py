#!/usr/bin/env python3
"""Select Lumora static section recipes for a website brief."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIBRARY = ROOT / "references" / "static-section-library.json"
TOKEN_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)?")


ROLE_ALIASES: dict[str, tuple[str, ...]] = {
    "hero": ("hero", "landing-page"),
    "trust": ("stats", "testimonials", "benefits", "features"),
    "proof": ("stats", "testimonials", "benefits", "features"),
    "features": ("features", "cards", "tabs"),
    "benefits": ("benefits", "features", "stats"),
    "services": ("services", "features", "cards"),
    "about": ("about", "process", "features"),
    "process": ("process", "tabs", "features"),
    "product": ("product", "pricing", "features"),
    "ingredients": ("features", "benefits", "tabs", "product"),
    "pricing": ("pricing", "product", "cta"),
    "testimonials": ("testimonials", "stats"),
    "portfolio": ("portfolio", "cards", "slider"),
    "dashboard": ("dashboard", "features", "tabs"),
    "faq": ("faq", "tabs"),
    "contact": ("contact", "cta", "footer"),
    "cta": ("cta", "contact", "footer"),
    "footer": ("footer", "contact", "cta"),
}


BLUEPRINTS: list[tuple[str, tuple[str, ...], list[str]]] = [
    (
        "ecommerce-product",
        ("ecommerce", "shop", "product", "commerce", "cart", "checkout", "hair", "oil", "skincare", "beauty"),
        ["hero", "trust", "benefits", "ingredients", "process", "testimonials", "product", "faq", "cta", "footer"],
    ),
    (
        "saas-platform",
        ("saas", "software", "platform", "dashboard", "analytics", "ai", "app", "b2b"),
        ["hero", "trust", "features", "dashboard", "process", "testimonials", "pricing", "faq", "cta", "footer"],
    ),
    (
        "agency-studio",
        ("agency", "studio", "portfolio", "creative", "design", "brand", "marketing"),
        ["hero", "trust", "services", "portfolio", "process", "testimonials", "contact", "footer"],
    ),
    (
        "local-service",
        ("local", "service", "clinic", "repair", "booking", "appointment", "restaurant", "salon", "dentist"),
        ["hero", "trust", "services", "about", "process", "testimonials", "faq", "contact", "footer"],
    ),
    (
        "portfolio",
        ("portfolio", "case study", "work", "creator", "artist", "photographer"),
        ["hero", "portfolio", "about", "process", "testimonials", "contact", "footer"],
    ),
]


def tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall((text or "").lower()))


def load_library(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload.get("recipes"), list):
        raise ValueError(f"{path} does not look like a Lumora static section library")
    return payload


def infer_blueprint(brief: str) -> tuple[str, list[str]]:
    brief_tokens = tokens(brief)
    best_name = "premium-marketing"
    best_roles = ["hero", "trust", "features", "process", "testimonials", "pricing", "faq", "cta", "footer"]
    best_score = 0
    for name, keywords, roles in BLUEPRINTS:
        score = len(brief_tokens.intersection(tokens(" ".join(keywords))))
        if score > best_score:
            best_name = name
            best_roles = roles
            best_score = score
    return best_name, best_roles


def infer_pages(brief: str, blueprint_name: str) -> list[dict[str, Any]]:
    lower = brief.lower()
    wants_multipage = any(term in lower for term in ["multi page", "multipage", "multiple pages", "full website", "company website", "routes"])
    if not wants_multipage:
        return [{"file": "index.html", "label": "Home", "roles": "all selected sections"}]

    if blueprint_name == "ecommerce-product":
        return [
            {"file": "index.html", "label": "Home", "roles": ["hero", "trust", "benefits", "product", "cta"]},
            {"file": "product.html", "label": "Product", "roles": ["product", "ingredients", "testimonials", "faq"]},
            {"file": "ritual.html", "label": "Ritual", "roles": ["process", "benefits", "faq", "cta"]},
            {"file": "contact.html", "label": "Contact", "roles": ["contact", "faq", "footer"]},
        ]
    if blueprint_name == "saas-platform":
        return [
            {"file": "index.html", "label": "Home", "roles": ["hero", "trust", "features", "dashboard", "cta"]},
            {"file": "product.html", "label": "Product", "roles": ["features", "dashboard", "process", "faq"]},
            {"file": "pricing.html", "label": "Pricing", "roles": ["pricing", "testimonials", "faq", "cta"]},
            {"file": "contact.html", "label": "Contact", "roles": ["contact", "footer"]},
        ]
    if blueprint_name == "agency-studio":
        return [
            {"file": "index.html", "label": "Home", "roles": ["hero", "trust", "services", "cta"]},
            {"file": "work.html", "label": "Work", "roles": ["portfolio", "testimonials", "cta"]},
            {"file": "studio.html", "label": "Studio", "roles": ["about", "process", "contact"]},
            {"file": "contact.html", "label": "Contact", "roles": ["contact", "footer"]},
        ]
    return [
        {"file": "index.html", "label": "Home", "roles": ["hero", "trust", "services", "cta"]},
        {"file": "about.html", "label": "About", "roles": ["about", "process", "testimonials"]},
        {"file": "services.html", "label": "Services", "roles": ["services", "faq", "cta"]},
        {"file": "contact.html", "label": "Contact", "roles": ["contact", "footer"]},
    ]


def role_match_score(recipe: dict[str, Any], wanted_role: str) -> int:
    aliases = ROLE_ALIASES.get(wanted_role, (wanted_role,))
    recipe_type = recipe["section"]["type"]
    recipe_roles = set(recipe["section"]["roles"])
    score = 0
    for index, alias in enumerate(aliases):
        if alias == wanted_role:
            if recipe_type == alias:
                score += 140
            if alias in recipe_roles:
                score += 90
            continue
        if recipe_type == alias:
            score += max(15, 50 - index * 10)
        if alias in recipe_roles:
            score += max(8, 30 - index * 4)
    return score


def score_recipe(recipe: dict[str, Any], brief_tokens: set[str], wanted_role: str) -> int:
    source = recipe["source"]
    if not source.get("has_prompt_text"):
        return -999

    score = role_match_score(recipe, wanted_role)
    terms = set(recipe.get("search_terms") or [])
    suitable_for = set(recipe["section"].get("suitable_for") or [])
    atoms = recipe.get("atoms") or {}
    atom_terms = set()
    for values in atoms.values():
        atom_terms.update(tokens(" ".join(values)))

    score += len(brief_tokens.intersection(terms)) * 9
    score += len(brief_tokens.intersection(suitable_for)) * 25
    score += len(brief_tokens.intersection(atom_terms)) * 6

    title_terms = tokens(recipe.get("title") or "")
    score += len(brief_tokens.intersection(title_terms)) * 14

    if source.get("prompt_length", 0) > 4000:
        score += 8
    if source.get("preview", {}).get("video") or source.get("preview", {}).get("image"):
        score += 4
    return score


def choose_sections(recipes: list[dict[str, Any]], brief: str, roles: list[str], max_sections: int | None) -> list[dict[str, Any]]:
    brief_tokens = tokens(brief)
    selected: list[dict[str, Any]] = []
    used_ids: set[str] = set()
    family_counts: Counter[str] = Counter()

    for role in roles[: max_sections or len(roles)]:
        ranked = sorted(
            recipes,
            key=lambda recipe: score_recipe(recipe, brief_tokens, role),
            reverse=True,
        )
        chosen = None
        for recipe in ranked:
            if score_recipe(recipe, brief_tokens, role) < 0:
                break
            if recipe["id"] in used_ids:
                continue
            family = recipe["source"].get("family") or "unknown"
            if family_counts[family] >= 2 and len(selected) >= 3:
                continue
            if role_match_score(recipe, role) <= 0 and len(selected) < 3:
                continue
            chosen = recipe
            break
        if chosen is None:
            continue
        selected.append({"required_role": role, "recipe": chosen, "score": score_recipe(chosen, brief_tokens, role)})
        used_ids.add(chosen["id"])
        family_counts[chosen["source"].get("family") or "unknown"] += 1

    return selected


def image_brief(brief: str, blueprint_name: str, selected: list[dict[str, Any]]) -> str:
    visual_atoms: list[str] = []
    layout_atoms: list[str] = []
    for item in selected:
        recipe = item["recipe"]
        visual_atoms.extend(recipe["atoms"].get("visual", []))
        layout_atoms.extend(recipe["atoms"].get("layout", []))
    top_visual = [name for name, _ in Counter(visual_atoms).most_common(5)]
    top_layout = [name for name, _ in Counter(layout_atoms).most_common(5)]
    return (
        "Generate a premium website design reference for: "
        f"{brief}. Blueprint: {blueprint_name}. Use an implementation-friendly composition with "
        f"layout cues {', '.join(top_layout or ['image-led sections'])} and visual cues "
        f"{', '.join(top_visual or ['brand-token-driven premium design'])}. "
        "Show real section rhythm, strong media frames, clear nav/CTA hierarchy, and enough detail to code in plain HTML/CSS/JS. "
        "Do not include readable product label text or fake brand logos inside the image."
    )


def as_plan(brief: str, library: dict[str, Any], max_sections: int | None = None) -> dict[str, Any]:
    blueprint_name, roles = infer_blueprint(brief)
    selected = choose_sections(library["recipes"], brief, roles, max_sections)
    pages = infer_pages(brief, blueprint_name)
    brief_tokens = tokens(brief)
    media_needs = sorted({need for item in selected for need in item["recipe"].get("media_needs", [])})
    if not brief_tokens.intersection({"botanical", "natural", "plant", "plants", "hair", "oil", "skincare", "beauty", "organic"}):
        media_needs = [need for need in media_needs if "botanical" not in need]
    if not brief_tokens.intersection({"saas", "software", "dashboard", "analytics", "app", "platform", "interface", "ui"}):
        media_needs = [need for need in media_needs if "UI screenshot" not in need]

    return {
        "schema": "lumora.static_section_plan.v1",
        "brief": brief,
        "blueprint": {
            "name": blueprint_name,
            "required_roles": roles,
            "coverage": f"{len(selected)}/{len(roles)}",
        },
        "static_build": {
            "stack": "plain HTML, CSS, and vanilla JS",
            "no_vite": True,
            "base_files": ["index.html", "styles.css", "script.js"],
            "pages": pages,
        },
        "image_first": {
            "required": True,
            "prompt": image_brief(brief, blueprint_name, selected),
            "after_generation": [
                "Inspect the reference image before coding.",
                "Extract palette, type character, spacing rhythm, media frames, component shapes, and section density.",
                "Apply the visual system as a thin skin over the selected section recipes.",
            ],
        },
        "selected_sections": [
            {
                "required_role": item["required_role"],
                "id": item["recipe"]["id"],
                "title": item["recipe"]["title"],
                "section_type": item["recipe"]["section"]["type"],
                "family": item["recipe"]["source"].get("family"),
                "score": item["score"],
                "source_hash": item["recipe"]["source"].get("prompt_sha256"),
                "layout_atoms": item["recipe"]["atoms"].get("layout", []),
                "visual_atoms": item["recipe"]["atoms"].get("visual", []),
                "interaction_atoms": item["recipe"]["atoms"].get("interaction", []),
                "conversion_atoms": item["recipe"]["atoms"].get("conversion", []),
                "html_structure": item["recipe"]["static_contract"].get("html_structure", []),
                "css_hooks": item["recipe"]["static_contract"].get("css_hooks", []),
                "js_behaviors": item["recipe"]["static_contract"].get("js_behaviors", []),
                "media_needs": item["recipe"].get("media_needs", []),
            }
            for item in selected
        ],
        "media_plan": {
            "existing_media_check": "Use project/client media first. If none is available, generate fit-for-slot assets with imagegen before coding.",
            "needs": media_needs,
        },
        "implementation_contract": [
            "Build static files directly; do not scaffold Vite unless the user explicitly asks or the existing project already requires it.",
            "Use selected section recipes as the structural source of truth.",
            "Use the generated/inspected image only to tune palette, spacing, type mood, media framing, and component finish.",
            "Wire every visible button, link, form, tab, accordion, selector, and route.",
            "Verify desktop and mobile screenshots before final delivery.",
        ],
    }


def print_markdown(plan: dict[str, Any]) -> None:
    print("# Lumora Static Section Plan")
    print()
    print(f"Brief: {plan['brief']}")
    print(f"Blueprint: {plan['blueprint']['name']} ({plan['blueprint']['coverage']} roles covered)")
    print("Stack: plain HTML/CSS/JS; no Vite.")
    print()
    print("## Image-first prompt")
    print(plan["image_first"]["prompt"])
    print()
    print("## Pages")
    for page in plan["static_build"]["pages"]:
        print(f"- {page['file']}: {page['label']} - {page['roles']}")
    print()
    print("## Selected sections")
    for section in plan["selected_sections"]:
        print(
            f"- {section['required_role']}: {section['id']} ({section['title']}) "
            f"as {section['section_type']} | layout: {', '.join(section['layout_atoms'][:3])} | "
            f"visual: {', '.join(section['visual_atoms'][:3])}"
        )
    print()
    print("## Media needs")
    for need in plan["media_plan"]["needs"]:
        print(f"- {need}")
    print()
    print("## Contract")
    for item in plan["implementation_contract"]:
        print(f"- {item}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", help="Website brief to plan for")
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument("--max-sections", type=int, default=None)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args()

    library = load_library(args.library)
    plan = as_plan(args.brief, library, args.max_sections)
    if args.json:
        print(json.dumps(plan, ensure_ascii=True, indent=2))
    else:
        print_markdown(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
