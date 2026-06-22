#!/usr/bin/env python3
"""Build Lumora's static section recipe library from MotionSites prompts.

The output intentionally does not duplicate prompt bodies. It turns every
MotionSites record into a compact implementation recipe with source hashes,
section roles, layout atoms, visual atoms, interaction atoms, and plain
HTML/CSS/JS contracts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "references" / "motionsites-prompt-library.json"
DEFAULT_OUTPUT = ROOT / "references" / "static-section-library.json"


TOKEN_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)?")


SECTION_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("navbar", ("navbar", "navigation", "nav menu", "menu", "header nav")),
    ("hero", ("hero", "above the fold", "first viewport", "headline", "landing hero")),
    ("landing-page", ("landing page", "complete website", "full website", "one page", "homepage")),
    ("features", ("features", "feature cards", "benefits", "why choose", "capabilities")),
    ("benefits", ("benefits", "outcomes", "advantages", "results", "proof points")),
    ("services", ("services", "service", "offerings", "solutions")),
    ("about", ("about", "story", "mission", "team", "founder")),
    ("process", ("process", "steps", "workflow", "how it works", "ritual", "timeline")),
    ("product", ("product", "ecommerce", "shop", "commerce", "cart", "checkout", "bundle")),
    ("pricing", ("pricing", "plans", "tiers", "packages", "subscription")),
    ("testimonials", ("testimonials", "reviews", "quote", "social proof", "customers")),
    ("portfolio", ("portfolio", "case studies", "projects", "gallery", "work")),
    ("dashboard", ("dashboard", "analytics", "metrics panel", "product ui", "app screen")),
    ("faq", ("faq", "questions", "accordion", "objections")),
    ("contact", ("contact", "booking", "form", "schedule", "appointment")),
    ("cta", ("cta", "call to action", "signup", "waitlist", "join", "download")),
    ("footer", ("footer", "closing", "site map", "newsletter")),
    ("stats", ("stats", "numbers", "metrics", "kpi", "counters")),
    ("tabs", ("tabs", "tabbed", "switcher", "segmented")),
    ("cards", ("cards", "card grid", "bento", "tiles")),
    ("slider", ("slider", "carousel", "marquee", "scrolling")),
]


DOMAIN_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("saas", ("saas", "software", "platform", "dashboard", "analytics", "ai", "startup")),
    ("agency", ("agency", "studio", "creative", "brand", "design", "marketing")),
    ("ecommerce", ("ecommerce", "shop", "product", "commerce", "cart", "checkout", "bundle")),
    ("beauty-wellness", ("beauty", "skincare", "hair", "oil", "wellness", "spa", "cosmetic")),
    ("local-service", ("local", "service", "booking", "appointment", "repair", "clinic")),
    ("portfolio", ("portfolio", "case study", "projects", "designer", "creator")),
    ("finance", ("fintech", "finance", "bank", "payment", "invest", "crypto")),
    ("web3", ("web3", "blockchain", "crypto", "wallet", "nft")),
    ("restaurant-food", ("restaurant", "food", "chef", "menu", "cafe")),
    ("real-estate", ("real estate", "property", "architecture", "interior", "home")),
    ("energy", ("solar", "energy", "climate", "green", "sustainability")),
    ("education", ("course", "education", "academy", "learn", "training")),
    ("events", ("event", "conference", "festival", "ticket", "venue")),
]


LAYOUT_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("asymmetric-split", ("asymmetric", "split", "offset", "left", "right")),
    ("centered-cinematic", ("centered", "cinematic", "fullscreen", "full-screen")),
    ("bento-grid", ("bento", "grid", "tiles", "cards", "masonry")),
    ("editorial-stack", ("editorial", "magazine", "story", "narrative", "large typography")),
    ("sticky-scroll", ("sticky", "pinned", "scroll", "scrolltrigger", "parallax")),
    ("gallery-collage", ("gallery", "collage", "masonry", "image grid", "portfolio")),
    ("product-stage", ("product", "object", "bottle", "device", "mockup", "3d")),
    ("dashboard-frame", ("dashboard", "screen", "interface", "ui panel", "app")),
    ("pricing-table", ("pricing", "plans", "tiers", "comparison")),
    ("form-panel", ("form", "contact", "booking", "signup")),
    ("marquee-strip", ("marquee", "ticker", "logos", "infinite")),
    ("accordion-stack", ("accordion", "faq", "collapse", "tabs")),
]


VISUAL_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("dark-cinematic", ("dark", "black", "charcoal", "cinematic", "noir")),
    ("warm-editorial", ("warm", "cream", "beige", "editorial", "serif", "paper")),
    ("luxury-product", ("luxury", "premium", "elegant", "boutique", "high-end")),
    ("glass-depth", ("glass", "glassmorphism", "blur", "translucent", "frosted")),
    ("bold-studio", ("bold", "studio", "poster", "color field", "oversized")),
    ("technical-precision", ("technical", "grid", "data", "system", "interface")),
    ("organic-botanical", ("organic", "botanical", "natural", "plant", "earth")),
    ("minimal-light", ("minimal", "white", "clean", "light", "simple")),
    ("gradient-glow", ("gradient", "glow", "neon", "orb", "mesh")),
    ("three-dimensional", ("3d", "depth", "isometric", "perspective", "object")),
]


INTERACTION_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("scroll-reveal", ("scroll reveal", "fade up", "fade-up", "while in view", "intersection")),
    ("parallax", ("parallax", "depth", "drift")),
    ("sticky-pin", ("sticky", "pinned", "pinning")),
    ("tabs", ("tabs", "tabbed", "switcher", "segmented")),
    ("accordion", ("accordion", "faq", "expand", "collapse")),
    ("carousel", ("carousel", "slider", "slides")),
    ("marquee", ("marquee", "ticker", "infinite scroll")),
    ("hover-depth", ("hover", "magnetic", "tilt", "lift", "cursor")),
    ("countup", ("countup", "counter", "animated number")),
    ("form-feedback", ("form", "input", "validation", "submit")),
    ("selector-state", ("selector", "toggle", "variant", "quantity", "package")),
    ("reduced-motion", ("reduced motion", "prefers-reduced-motion", "accessibility")),
]


CONVERSION_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("buy", ("buy", "shop", "cart", "checkout", "order", "add to bag")),
    ("signup", ("signup", "sign up", "join", "waitlist", "start trial")),
    ("book", ("book", "schedule", "appointment", "demo", "consultation")),
    ("contact", ("contact", "message", "email", "call", "form")),
    ("pricing", ("pricing", "plans", "subscribe", "package")),
    ("download", ("download", "get app", "install")),
    ("learn", ("learn more", "case study", "explore", "view work")),
]


BLUEPRINTS: dict[str, dict[str, list[str]]] = {
    "navbar": {
        "html_structure": ["brand link", "primary navigation", "mobile menu button", "primary CTA"],
        "css_hooks": ["site-nav", "nav__brand", "nav__links", "nav__toggle", "nav__cta"],
        "js_behaviors": ["mobile menu toggle", "escape key closes menu", "active route state"],
    },
    "hero": {
        "html_structure": ["eyebrow or proof label", "H1", "supporting copy", "CTA group", "hero media", "trust/proof strip"],
        "css_hooks": ["hero", "hero__content", "hero__title", "hero__media", "hero__proof"],
        "js_behaviors": ["entry reveal", "media parallax when appropriate", "CTA scroll/route target"],
    },
    "landing-page": {
        "html_structure": ["shared navbar", "hero", "proof", "main content sections", "conversion block", "footer"],
        "css_hooks": ["page-shell", "section", "section__inner", "site-footer"],
        "js_behaviors": ["nav routing", "scroll reveal", "all visible controls wired"],
    },
    "features": {
        "html_structure": ["section heading", "feature grid", "feature cards", "supporting media or proof"],
        "css_hooks": ["features", "feature-grid", "feature-card", "feature-card__media"],
        "js_behaviors": ["staggered reveal", "hover depth"],
    },
    "benefits": {
        "html_structure": ["benefit intro", "outcome list", "metric/proof modules", "supporting visual"],
        "css_hooks": ["benefits", "benefit-list", "benefit-item", "proof-metric"],
        "js_behaviors": ["countup when metrics exist", "scroll reveal"],
    },
    "services": {
        "html_structure": ["service overview", "service cards", "detail links", "booking/contact CTA"],
        "css_hooks": ["services", "service-grid", "service-card", "service-card__cta"],
        "js_behaviors": ["card link routing", "hover depth"],
    },
    "about": {
        "html_structure": ["story headline", "founder/team/media block", "values or facts", "supporting CTA"],
        "css_hooks": ["about", "about__story", "about__media", "value-list"],
        "js_behaviors": ["entry reveal"],
    },
    "process": {
        "html_structure": ["process heading", "ordered steps", "sticky or visual companion", "completion CTA"],
        "css_hooks": ["process", "process-step", "process__media", "step-index"],
        "js_behaviors": ["step reveal", "sticky companion disabled on small screens if unsafe"],
    },
    "product": {
        "html_structure": ["product media", "product facts", "option selector", "price/quantity state", "purchase CTA", "trust note"],
        "css_hooks": ["product", "product__media", "product-options", "product-price", "purchase-panel"],
        "js_behaviors": ["variant selector", "quantity/price update", "add-to-cart feedback"],
    },
    "pricing": {
        "html_structure": ["pricing intro", "plan cards", "feature comparison", "recommended state", "FAQ/CTA link"],
        "css_hooks": ["pricing", "plan-grid", "plan-card", "plan-card--featured"],
        "js_behaviors": ["billing toggle", "plan selection", "CTA routing"],
    },
    "testimonials": {
        "html_structure": ["testimonial heading", "quote cards", "review metrics", "customer logos or portraits"],
        "css_hooks": ["testimonials", "quote-grid", "quote-card", "review-metric"],
        "js_behaviors": ["carousel or reveal when needed"],
    },
    "portfolio": {
        "html_structure": ["work intro", "project gallery", "case study cards", "project links"],
        "css_hooks": ["portfolio", "project-grid", "project-card", "project-card__media"],
        "js_behaviors": ["filter or carousel if recipe calls for it", "project route links"],
    },
    "dashboard": {
        "html_structure": ["product UI frame", "metric panels", "workflow explanation", "screen/detail callouts"],
        "css_hooks": ["dashboard-showcase", "ui-frame", "metric-panel", "callout"],
        "js_behaviors": ["tabs or metric animation", "reduced-motion fallback"],
    },
    "faq": {
        "html_structure": ["FAQ heading", "accordion list", "support/contact CTA"],
        "css_hooks": ["faq", "faq-list", "faq-item", "faq-trigger"],
        "js_behaviors": ["accessible accordion", "keyboard support"],
    },
    "contact": {
        "html_structure": ["contact intro", "contact form", "contact methods", "map/location or proof panel"],
        "css_hooks": ["contact", "contact-form", "contact-methods", "form-field"],
        "js_behaviors": ["form validation", "submit feedback", "mailto/tel/map links"],
    },
    "cta": {
        "html_structure": ["closing headline", "short conversion copy", "primary CTA", "secondary CTA/proof"],
        "css_hooks": ["final-cta", "cta__title", "cta__actions", "cta__proof"],
        "js_behaviors": ["CTA route/scroll target", "entry reveal"],
    },
    "footer": {
        "html_structure": ["brand recap", "route columns", "contact/social/legal links", "copyright"],
        "css_hooks": ["site-footer", "footer__brand", "footer__links", "footer__legal"],
        "js_behaviors": ["all links resolve", "newsletter validation if present"],
    },
    "stats": {
        "html_structure": ["metrics strip", "number labels", "supporting proof copy"],
        "css_hooks": ["stats", "stats-grid", "stat", "stat__number"],
        "js_behaviors": ["countup", "reduced-motion fallback"],
    },
    "tabs": {
        "html_structure": ["tab list", "tab panels", "supporting image or details"],
        "css_hooks": ["tabs", "tab-list", "tab-button", "tab-panel"],
        "js_behaviors": ["accessible tabs", "keyboard arrow support"],
    },
    "cards": {
        "html_structure": ["card section heading", "card grid", "mixed media/text cards"],
        "css_hooks": ["card-section", "card-grid", "card", "card__media"],
        "js_behaviors": ["hover depth", "entry reveal"],
    },
    "slider": {
        "html_structure": ["slider heading", "track", "slides", "previous/next controls", "progress or dots"],
        "css_hooks": ["slider", "slider__track", "slide", "slider__controls"],
        "js_behaviors": ["vanilla JS carousel", "keyboard controls", "reduced-motion fallback"],
    },
    "general": {
        "html_structure": ["section heading", "content modules", "media/proof when useful", "section CTA"],
        "css_hooks": ["section", "section__inner", "section__media", "section__actions"],
        "js_behaviors": ["entry reveal only when it supports the section"],
    },
}


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def tokens(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


def contains_phrase(haystack: str, phrase: str) -> bool:
    return phrase in haystack


def matched(rule_set: list[tuple[str, tuple[str, ...]]], haystack: str) -> list[str]:
    found: list[str] = []
    for label, phrases in rule_set:
        if any(contains_phrase(haystack, phrase) for phrase in phrases):
            found.append(label)
    return found


def first_section_type(metadata: dict[str, Any], haystack: str) -> str:
    category = normalize_space(str(metadata.get("category") or "")).lower()
    page_type = normalize_space(str(metadata.get("page_type") or "")).lower()
    declared_type = normalize_space(str(metadata.get("type") or "")).lower()

    if "landing" in category or "landing" in page_type:
        return "landing-page"
    if "footer" in category:
        return "footer"
    if "hero" in category or declared_type == "hero":
        return "hero"
    if "pricing" in category:
        return "pricing"
    if "testimonial" in category:
        return "testimonials"
    if "feature" in category:
        return "features"
    if "cta" in category:
        return "cta"
    if "about" in category:
        return "about"
    if "portfolio" in category:
        return "portfolio"
    if "ecommerce" in category or "product" in category:
        return "product"

    matches = matched(SECTION_RULES, haystack)
    return matches[0] if matches else "general"


def source_family(prompt_id: str) -> str:
    if not prompt_id:
        return "unknown"
    parts = prompt_id.split("-")
    if len(parts) == 1:
        return parts[0]
    if parts[0] in {"ai", "saas", "web3", "3d"} and len(parts) > 1:
        return "-".join(parts[:2])
    return parts[0]


def derive_media_needs(section_type: str, visual_atoms: list[str], layout_atoms: list[str]) -> list[str]:
    needs: list[str] = []
    if section_type in {"hero", "landing-page"}:
        needs.append("hero visual or product/source media")
    if section_type in {"product", "portfolio", "services", "features", "testimonials"}:
        needs.append("slot-specific card or product media")
    if "product-stage" in layout_atoms:
        needs.append("object-led product render/photo")
    if "dashboard-frame" in layout_atoms:
        needs.append("credible UI screenshot or coded UI mock")
    if "gallery-collage" in layout_atoms:
        needs.append("cohesive gallery image set")
    if "organic-botanical" in visual_atoms:
        needs.append("botanical or natural texture/image system")
    if not needs:
        needs.append("optional supporting texture or icon system")
    return sorted(set(needs))


def derive_static_contract(section_type: str, interaction_atoms: list[str]) -> dict[str, Any]:
    blueprint = BLUEPRINTS.get(section_type, BLUEPRINTS["general"])
    js_needed = [atom for atom in interaction_atoms if atom not in {"scroll-reveal", "reduced-motion"}]
    return {
        "stack": "plain-html-css-vanilla-js",
        "no_vite": True,
        "default_files": ["index.html", "styles.css", "script.js"],
        "html_structure": blueprint["html_structure"],
        "css_hooks": blueprint["css_hooks"],
        "js_behaviors": blueprint["js_behaviors"],
        "js_required": bool(js_needed or section_type in {"navbar", "faq", "contact", "product", "pricing", "tabs", "slider"}),
        "implementation_notes": [
            "Use semantic HTML and data-lumora-section attributes for traceability.",
            "Use CSS variables for the site-wide visual skin generated by the taste pass.",
            "Use vanilla JS only for visible interactions; do not require a bundler.",
            "Keep responsive dimensions stable with grid constraints, min/max sizes, and aspect-ratio.",
        ],
    }


def recipe_for(prompt: dict[str, Any]) -> dict[str, Any]:
    metadata = prompt.get("metadata") or {}
    prompt_id = str(prompt.get("id") or metadata.get("id") or "")
    title = normalize_space(str(prompt.get("title") or metadata.get("title") or prompt_id))
    category = normalize_space(str(prompt.get("ui_category") or metadata.get("category") or ""))
    page_type = normalize_space(str(metadata.get("page_type") or ""))
    prompt_text = prompt.get("prompt_text") or ""
    meta_haystack = " ".join(
        [
            prompt_id,
            title,
            category,
            page_type,
            normalize_space(str(metadata.get("type") or "")),
            normalize_space(str(metadata.get("types") or "")),
        ]
    ).lower()
    haystack = " ".join(
        [
            meta_haystack,
            prompt_text,
        ]
    ).lower()

    section_type = first_section_type(metadata, haystack)
    section_roles = sorted(set([section_type] + matched(SECTION_RULES, haystack)))
    layout_atoms = matched(LAYOUT_RULES, haystack)
    visual_atoms = matched(VISUAL_RULES, haystack)
    interaction_atoms = matched(INTERACTION_RULES, haystack)
    conversion_atoms = matched(CONVERSION_RULES, haystack)
    suitable_for = matched(DOMAIN_RULES, meta_haystack)

    term_counts = Counter(token for token in tokens(haystack) if len(token) > 3)
    search_terms = [term for term, _ in term_counts.most_common(36)]

    prompt_hash = prompt.get("prompt_sha256")
    if prompt_text and not prompt_hash:
        prompt_hash = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()

    return {
        "id": prompt_id,
        "title": title,
        "source": {
            "category": category,
            "page_type": page_type,
            "family": source_family(prompt_id),
            "fetch_status": prompt.get("fetch_status"),
            "has_prompt_text": bool(prompt_text),
            "prompt_length": len(prompt_text),
            "prompt_sha256": prompt_hash,
            "preview": {
                "image": metadata.get("image_preview_url"),
                "video": metadata.get("video_preview_url"),
            },
            "load_prompt_command": f"python scripts/load_lumora_prompt.py --id {prompt_id} --sha256",
        },
        "section": {
            "type": section_type,
            "roles": section_roles,
            "multipage_role": "page-base" if section_type == "landing-page" else "section",
            "suitable_for": suitable_for or ["general"],
        },
        "atoms": {
            "layout": layout_atoms or ["standard-section"],
            "visual": visual_atoms or ["brand-token-driven"],
            "interaction": interaction_atoms or ["static-or-scroll-reveal"],
            "conversion": conversion_atoms or ["contextual-cta"],
        },
        "static_contract": derive_static_contract(section_type, interaction_atoms),
        "media_needs": derive_media_needs(section_type, visual_atoms, layout_atoms),
        "search_terms": search_terms,
        "recipe_summary": (
            f"Build a {section_type.replace('-', ' ')} section from the {title} source, "
            f"using its inferred {', '.join((layout_atoms or ['standard-section'])[:3])} structure "
            f"and {', '.join((visual_atoms or ['brand-token-driven'])[:3])} visual language."
        ),
    }


def load_prompts(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("prompts"), list):
        return data, data["prompts"]
    if isinstance(data, list):
        return {"source": str(path), "prompts": data}, data
    raise ValueError(f"Unsupported prompt library shape: {path}")


def build(source: Path, output: Path) -> dict[str, Any]:
    source_data, prompts = load_prompts(source)
    recipes = [recipe_for(prompt) for prompt in prompts]
    try:
        source_path = source.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        source_path = source.as_posix()
    counts = {
        "total": len(recipes),
        "with_prompt_text": sum(1 for recipe in recipes if recipe["source"]["has_prompt_text"]),
        "without_prompt_text": sum(1 for recipe in recipes if not recipe["source"]["has_prompt_text"]),
        "by_section_type": dict(Counter(recipe["section"]["type"] for recipe in recipes).most_common()),
        "by_family": dict(Counter(recipe["source"]["family"] for recipe in recipes).most_common()),
    }
    payload = {
        "schema": "lumora.static_section_library.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_library": {
            "path": source_path,
            "source": source_data.get("source"),
            "generated_at": source_data.get("generated_at"),
            "permission_reference": "references/permissions.md",
            "prompt_bodies_omitted": True,
            "body_policy": "Recipes are transformed metadata and build contracts; full prompt_text remains only in motionsites-prompt-library.json.",
        },
        "counts": counts,
        "recipes": recipes,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    payload = build(args.source, args.output)
    print(f"Wrote {args.output}")
    print(json.dumps(payload["counts"], ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
