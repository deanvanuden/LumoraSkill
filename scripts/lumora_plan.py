#!/usr/bin/env python3
"""Create a traceable Lumora creative plan from the full prompt library."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIBRARY = ROOT / "references" / "motionsites-prompt-library.json"
DEFAULT_INDEX = ROOT / "references" / "design-dna-index.json"
TOKEN_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)?")
STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "build", "by", "company", "create", "for", "from",
    "has", "have", "in", "is", "it", "make", "of", "on", "or", "page", "site", "that", "the", "their",
    "this", "to", "use", "website", "with",
}
BANNED_IDS = {"arceage-contact-us", "agency-services"}


@dataclass(frozen=True)
class Profile:
    name: str
    keywords: tuple[str, ...]
    expansion: tuple[str, ...]
    sections: tuple[str, ...]
    multi_pages: tuple[tuple[str, str, tuple[str, ...]], ...]
    media_slots: tuple[str, ...]
    type_directions: tuple[str, ...]
    palette_directions: tuple[str, ...]


PROFILES: tuple[Profile, ...] = (
    Profile(
        name="product-commerce",
        keywords=("product", "ecommerce", "e-commerce", "shop", "store", "skincare", "beauty", "hair oil", "cosmetics", "fashion", "jewelry", "supplement"),
        expansion=("product", "ecommerce", "shop", "collection", "product render", "selector", "ingredients", "ritual", "purchase", "editorial"),
        sections=("hero", "product-proposition", "proof", "product-story", "materials-or-ingredients", "ritual-or-use", "variants-and-purchase", "reviews", "faq", "closing"),
        multi_pages=(
            ("index.html", "Home", ("hero", "product-proposition", "proof", "product-story", "closing")),
            ("product.html", "Product", ("hero", "materials-or-ingredients", "variants-and-purchase", "reviews", "faq")),
            ("story.html", "Story", ("product-story", "ritual-or-use", "proof", "closing")),
            ("contact.html", "Contact", ("contact", "faq", "closing")),
        ),
        media_slots=("dominant product or offer image", "material or ingredient macro", "lifestyle or use image", "detail or variant image", "closing campaign image"),
        type_directions=("characterful display sans with restrained humanist body", "editorial serif display with precise neutral sans", "condensed campaign display with quiet utility sans"),
        palette_directions=("material-derived neutrals with one product accent", "high-contrast campaign field with a restrained secondary color", "light editorial canvas with dark ink and one tactile accent"),
    ),
    Profile(
        name="saas-product",
        keywords=("saas", "software", "platform", "dashboard", "app", "b2b", "analytics", "ai product", "developer tool", "fintech app"),
        expansion=("saas", "dashboard", "interface", "workflow", "features", "data", "demo", "pricing", "integrations", "security"),
        sections=("hero", "product-proof", "guided-demo", "capabilities", "workflow", "evidence", "integrations", "pricing", "faq", "closing"),
        multi_pages=(
            ("index.html", "Home", ("hero", "product-proof", "guided-demo", "evidence", "closing")),
            ("product.html", "Product", ("capabilities", "workflow", "integrations", "faq")),
            ("pricing.html", "Pricing", ("pricing", "evidence", "faq", "closing")),
            ("contact.html", "Contact", ("contact", "closing")),
        ),
        media_slots=("real interface hero state", "guided product state", "workflow detail", "proof or integration visual"),
        type_directions=("precise grotesk with mono for interface evidence", "wide geometric sans with compact utility sans", "neutral technical sans with expressive display cut"),
        palette_directions=("neutral technical canvas with one saturated action color", "light product surface with dark ink and a signal accent", "charcoal interface field with restrained warm contrast"),
    ),
    Profile(
        name="creative-studio",
        keywords=("agency", "studio", "creative", "design", "branding", "portfolio", "photographer", "production company"),
        expansion=("portfolio", "projects", "case studies", "agency", "studio", "services", "editorial", "gallery", "contact"),
        sections=("hero", "selected-work", "services", "case-study", "process", "studio", "proof", "contact", "closing"),
        multi_pages=(
            ("index.html", "Home", ("hero", "selected-work", "services", "proof", "closing")),
            ("work.html", "Work", ("selected-work", "case-study", "closing")),
            ("studio.html", "Studio", ("studio", "process", "proof", "contact")),
            ("contact.html", "Contact", ("contact", "closing")),
        ),
        media_slots=("hero project image or reel", "project gallery set", "case-study detail", "studio or process image", "contact image"),
        type_directions=("expressive display grotesk with disciplined body sans", "editorial serif and rational sans pairing", "compressed poster type with neutral utility face"),
        palette_directions=("bold studio color field with crisp neutral counterpoint", "paper canvas with ink and one project-derived accent", "deep neutral gallery field with image-derived accents"),
    ),
    Profile(
        name="hospitality-place",
        keywords=("restaurant", "hotel", "resort", "cafe", "bar", "travel", "destination", "chef", "menu", "hospitality"),
        expansion=("travel", "restaurant", "hotel", "gallery", "booking", "menu", "location", "cinematic", "experience"),
        sections=("hero", "experience", "offerings", "place-story", "gallery", "proof", "booking", "visit", "closing"),
        multi_pages=(
            ("index.html", "Home", ("hero", "experience", "gallery", "proof", "booking")),
            ("experience.html", "Experience", ("offerings", "place-story", "gallery", "closing")),
            ("visit.html", "Visit", ("visit", "booking", "proof", "faq")),
            ("contact.html", "Contact", ("contact", "visit", "closing")),
        ),
        media_slots=("environmental hero still or loop", "food room or experience detail", "place story image", "gallery set", "visit or map visual"),
        type_directions=("editorial display serif with understated sans", "warm humanist sans with a distinctive title face", "high-contrast hospitality serif with compact utility sans"),
        palette_directions=("place-derived natural palette with one service accent", "deep evening field with warm light and pale copy space", "bright daylight canvas with material-derived secondary tones"),
    ),
    Profile(
        name="architecture-property",
        keywords=("architecture", "architect", "real estate", "property", "interior", "construction", "developer", "building", "homes"),
        expansion=("architecture", "projects", "properties", "gallery", "floor plan", "materials", "location", "portfolio", "contact"),
        sections=("hero", "featured-projects", "project-details", "approach", "materials", "gallery", "proof", "contact", "closing"),
        multi_pages=(
            ("index.html", "Home", ("hero", "featured-projects", "approach", "proof", "closing")),
            ("projects.html", "Projects", ("featured-projects", "project-details", "gallery")),
            ("studio.html", "Studio", ("approach", "materials", "proof", "contact")),
            ("contact.html", "Contact", ("contact", "closing")),
        ),
        media_slots=("full-bleed project hero", "project exterior", "material or detail crop", "plan or spatial diagram", "project gallery set"),
        type_directions=("architectural grotesk with fine editorial serif", "strict Swiss sans with restrained mono details", "wide modern sans with small technical captions"),
        palette_directions=("material neutral canvas with drawing-line accent", "high-contrast monochrome with one site-derived color", "daylight white with stone, metal, or landscape tones"),
    ),
    Profile(
        name="local-service",
        keywords=("local business", "clinic", "dentist", "salon", "plumber", "electrician", "repair", "contractor", "law firm", "accountant", "service area"),
        expansion=("services", "local", "booking", "reviews", "process", "contact", "location", "trust", "faq"),
        sections=("hero", "trust", "services", "results", "process", "about", "reviews", "service-area", "faq", "contact"),
        multi_pages=(
            ("index.html", "Home", ("hero", "trust", "services", "reviews", "contact")),
            ("services.html", "Services", ("services", "results", "process", "faq")),
            ("about.html", "About", ("about", "trust", "service-area", "proof")),
            ("contact.html", "Contact", ("contact", "service-area", "faq")),
        ),
        media_slots=("real team place or service hero", "service detail", "process or equipment image", "result or project image", "location image"),
        type_directions=("distinctive humanist sans with direct utility face", "confident display sans with highly readable body", "local editorial headline face with neutral sans"),
        palette_directions=("brand-led light canvas with clear action contrast", "workwear neutral palette with one confident accent", "warm local palette balanced by crisp dark text"),
    ),
    Profile(
        name="culture-editorial",
        keywords=("museum", "gallery", "magazine", "editorial", "event", "festival", "music", "film", "fashion", "exhibition", "artist"),
        expansion=("editorial", "museum", "gallery", "event", "projects", "typography", "program", "archive", "tickets"),
        sections=("hero", "program-or-collection", "feature-story", "archive", "contributors", "schedule", "tickets-or-action", "newsletter", "closing"),
        multi_pages=(
            ("index.html", "Home", ("hero", "program-or-collection", "feature-story", "tickets-or-action")),
            ("program.html", "Program", ("program-or-collection", "schedule", "contributors")),
            ("archive.html", "Archive", ("archive", "feature-story", "newsletter")),
            ("visit.html", "Visit", ("tickets-or-action", "contact", "closing")),
        ),
        media_slots=("campaign hero", "collection or program image", "editorial portrait or artwork", "archive set", "ticket or visit visual"),
        type_directions=("expressive editorial serif with Swiss utility sans", "poster display type with neutral reading face", "compressed cultural display with quiet grotesk"),
        palette_directions=("campaign color field with paper and ink neutrals", "monochrome editorial base with one exhibition accent", "image-led palette with strict black and white UI"),
    ),
    Profile(
        name="automotive-spatial",
        keywords=("automotive", "car", "vehicle", "motorcycle", "mobility", "aviation", "yacht", "machine", "racing"),
        expansion=("automotive", "3d", "product", "specifications", "gallery", "scroll", "video", "performance", "configurator"),
        sections=("hero", "model-story", "performance", "engineering", "details", "gallery", "specifications", "configure-or-contact", "closing"),
        multi_pages=(
            ("index.html", "Home", ("hero", "model-story", "performance", "gallery", "closing")),
            ("model.html", "Model", ("engineering", "details", "specifications", "configure-or-contact")),
            ("gallery.html", "Gallery", ("gallery", "model-story")),
            ("contact.html", "Contact", ("configure-or-contact", "contact", "closing")),
        ),
        media_slots=("vehicle hero still video or 3d", "engineering detail", "material close-up", "driving environment", "gallery set"),
        type_directions=("wide technical grotesk with condensed specification face", "motorsport display sans with neutral utility face", "precise geometric sans with mono data accents"),
        palette_directions=("dark technical field with material and signal accents", "bright studio canvas with body-color accent", "monochrome engineering palette with one performance color"),
    ),
    Profile(
        name="professional-trust",
        keywords=("finance", "financial", "consulting", "consultant", "legal", "law", "insurance", "healthcare", "medical", "investment", "advisory"),
        expansion=("trust", "finance", "services", "proof", "process", "team", "results", "contact", "pricing"),
        sections=("hero", "credibility", "services", "approach", "evidence", "team", "insights", "faq", "contact", "closing"),
        multi_pages=(
            ("index.html", "Home", ("hero", "credibility", "services", "evidence", "contact")),
            ("services.html", "Services", ("services", "approach", "faq", "closing")),
            ("about.html", "About", ("team", "credibility", "insights")),
            ("contact.html", "Contact", ("contact", "faq", "closing")),
        ),
        media_slots=("credible subject or environment hero", "service or process visual", "evidence graphic", "team or expert image", "contact image"),
        type_directions=("authoritative grotesk with measured editorial serif", "precise sans with restrained mono evidence", "humanist professional sans with a confident display cut"),
        palette_directions=("high-contrast neutral base with a credible brand accent", "light editorial canvas with deep ink and quiet status colors", "dark professional field with warm human contrast"),
    ),
    Profile(
        name="brand-story",
        keywords=(),
        expansion=("brand", "landing", "hero", "story", "features", "proof", "contact", "cta"),
        sections=("hero", "proposition", "story", "offerings", "proof", "process", "feature", "contact", "closing"),
        multi_pages=(
            ("index.html", "Home", ("hero", "proposition", "proof", "closing")),
            ("about.html", "About", ("story", "process", "proof")),
            ("services.html", "Offerings", ("offerings", "feature", "faq")),
            ("contact.html", "Contact", ("contact", "closing")),
        ),
        media_slots=("hero subject image", "story image", "offer detail", "proof image", "closing image"),
        type_directions=("characterful display face with neutral body sans", "editorial display and rational sans pairing", "confident grotesk with restrained utility face"),
        palette_directions=("brand-led neutral system with one clear accent", "image-derived palette with stable ink and surface roles", "high-contrast canvas with one material-derived secondary color"),
    ),
)


SLOT_CONFIG: dict[str, dict[str, Any]] = {
    "anchor": {
        "roles": {"complete-page": 100, "hero": 38, "story-about": 22, "portfolio-gallery": 20, "product-commerce": 20},
        "categories": {
            "landing page", "website", "saas", "agency", "ecommerce", "automotive", "travel",
            "interactive", "3d website", "creative / 3d",
        },
        "focus": "layout,visual,media,motion,interaction,responsive",
    },
    "experience": {
        "roles": {"features": 48, "story-about": 48, "process": 46, "portfolio-gallery": 46, "product-commerce": 46, "services": 42, "proof": 34},
        "categories": {"features", "features section", "about", "process", "portfolio", "projects", "product", "products", "services", "benefits", "cards", "tabs", "interactive"},
        "focus": "layout,visual,media,interaction,motion,responsive",
    },
    "conversion": {
        "roles": {"cta": 72, "pricing": 64, "contact-booking": 62, "footer": 46, "form-auth": 42, "product-commerce": 32},
        "categories": {"cta", "cta section", "pricing", "contact us", "footer section", "signup", "waitlist", "form", "ecommerce"},
        "focus": "conversion,interaction,layout,responsive",
    },
}


ADVANCED_MOTION = {
    "scroll-scrub", "pinned-scroll", "parallax", "mask-reveal", "split-text", "text-scramble", "marquee",
    "magnetic", "tilt-depth", "hover-reveal", "page-transition", "morph", "liquid", "video-scrub",
    "image-sequence", "drag-gesture", "count-up", "theme-transition",
}

DOMINANT_SCROLL_MOTION = {"scroll-scrub", "pinned-scroll", "video-scrub", "image-sequence"}
DOMINANT_LAYOUTS = {"pinned-sticky", "horizontal-scroll"}
SPATIAL_SIGNALS = {"spatial-3d", "3d", "webgl", "product-render"}
GENERIC_STYLES = {"dark", "light", "minimal"}

NARRATIVE_CATEGORIES = {
    "features", "features section", "about", "process", "portfolio", "projects", "product", "products",
    "services", "benefits", "cards", "tabs", "testimonial", "testimonials", "stats", "bento", "slider",
    "carousal", "use case", "why us", "info", "dashboard", "dashboard demo",
}
CONVERSION_CATEGORIES = {
    "cta", "cta section", "pricing", "contact us", "footer", "footer section", "signup", "waitlist",
    "form", "ecommerce", "product", "products", "faq", "accordion",
}

PROFILE_CONVERSION_CATEGORIES: dict[str, set[str]] = {
    "product-commerce": {"cta", "cta section", "pricing", "ecommerce", "product", "products", "faq", "accordion", "contact us"},
    "saas-product": {"cta", "cta section", "pricing", "signup", "waitlist", "form", "contact us", "faq", "accordion"},
    "creative-studio": {"cta", "cta section", "contact us", "footer", "footer section", "form", "signup"},
    "hospitality-place": {"cta", "cta section", "contact us", "footer", "footer section", "form", "faq", "accordion"},
    "architecture-property": {"cta", "cta section", "contact us", "footer", "footer section", "form"},
    "local-service": {"cta", "cta section", "contact us", "footer", "footer section", "form", "faq", "accordion"},
    "culture-editorial": {"cta", "cta section", "contact us", "footer", "footer section", "signup", "waitlist", "form"},
    "automotive-spatial": {"cta", "cta section", "contact us", "footer", "footer section", "product", "products", "form"},
    "professional-trust": {"cta", "cta section", "contact us", "footer", "footer section", "form", "faq", "accordion", "pricing"},
    "brand-story": CONVERSION_CATEGORIES,
}


PROFILE_ROLE_PREFERENCES: dict[str, dict[str, tuple[str, ...]]] = {
    "product-commerce": {
        "experience": ("product-commerce", "features", "process", "proof"),
        "conversion": ("product-commerce", "pricing", "cta", "contact-booking"),
    },
    "saas-product": {
        "experience": ("dashboard-app", "features", "process", "proof"),
        "conversion": ("pricing", "cta", "form-auth", "contact-booking"),
    },
    "creative-studio": {
        "experience": ("portfolio-gallery", "services", "process", "story-about"),
        "conversion": ("contact-booking", "cta", "footer", "form-auth"),
    },
    "hospitality-place": {
        "experience": ("portfolio-gallery", "story-about", "product-commerce", "proof"),
        "conversion": ("contact-booking", "cta", "footer", "form-auth"),
    },
    "architecture-property": {
        "experience": ("portfolio-gallery", "story-about", "process", "services"),
        "conversion": ("contact-booking", "cta", "footer", "form-auth"),
    },
    "local-service": {
        "experience": ("services", "process", "proof", "story-about"),
        "conversion": ("contact-booking", "form-auth", "cta", "footer"),
    },
    "culture-editorial": {
        "experience": ("portfolio-gallery", "story-about", "product-commerce", "process"),
        "conversion": ("cta", "form-auth", "contact-booking", "footer"),
    },
    "automotive-spatial": {
        "experience": ("product-commerce", "features", "portfolio-gallery", "process"),
        "conversion": ("product-commerce", "contact-booking", "cta", "footer"),
    },
    "professional-trust": {
        "experience": ("services", "proof", "process", "story-about"),
        "conversion": ("contact-booking", "cta", "form-auth", "pricing"),
    },
    "brand-story": {
        "experience": ("features", "story-about", "services", "process"),
        "conversion": ("cta", "contact-booking", "form-auth", "footer"),
    },
}


def tokens(value: str) -> list[str]:
    return [token for token in TOKEN_RE.findall(value.lower()) if token not in STOP_WORDS and len(token) > 1]


def slug(value: str) -> str:
    clean = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return clean or "section"


def profile_score(profile: Profile, brief: str) -> int:
    lower = brief.lower()
    brief_tokens = set(tokens(brief))
    score = 0
    for keyword in profile.keywords:
        keyword_tokens = set(tokens(keyword))
        if keyword.lower() in lower:
            score += 8 + len(keyword_tokens) * 2
        score += len(brief_tokens.intersection(keyword_tokens))
    return score


def infer_profile(brief: str) -> tuple[Profile, list[dict[str, Any]]]:
    scored = [(profile_score(profile, brief), profile) for profile in PROFILES[:-1]]
    scored.sort(key=lambda item: item[0], reverse=True)
    chosen = scored[0][1] if scored and scored[0][0] > 0 else PROFILES[-1]
    signals = [{"profile": profile.name, "score": score} for score, profile in scored[:4] if score > 0]
    return chosen, signals


def page_mode(brief: str, requested: str) -> str:
    if requested != "auto":
        return requested
    lower = brief.lower()
    explicit_single_terms = ("homepage only", "home page only", "single page only", "one page only", "landing page only")
    if any(term in lower for term in explicit_single_terms):
        return "one"
    multipage_terms = (
        "multi page", "multipage", "multiple pages", "full website", "full company website", "site map",
        "separate pages", "all pages", "all routes", "preserve routes", "preserve working destinations",
        "service pages", "legal pages", "existing pages", "source routes",
    )
    existing_site_terms = ("redesign", "existing site", "current site", "source site", "live site", "http://", "https://")
    return "multi" if any(term in lower for term in multipage_terms + existing_site_terms) else "one"


def site_origin(brief: str, requested: str) -> str:
    if requested != "auto":
        return requested
    lower = brief.lower()
    existing_terms = ("redesign", "existing site", "current site", "source site", "live site", "scrape", "preserve working", "http://", "https://")
    return "existing" if any(term in lower for term in existing_terms) else "new"


def page_map(profile: Profile, mode: str) -> list[dict[str, Any]]:
    if mode == "one":
        return [{"file": "index.html", "label": "Home", "sections": list(profile.sections)}]
    return [
        {"file": file, "label": label, "sections": list(sections)}
        for file, label, sections in profile.multi_pages
    ]


def initial_route_manifest(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    manifest = [
        {
            "file": page["file"],
            "status": "must-be-designed",
            "purpose": page["label"],
            "shared_system": "",
            "verified": False,
        }
        for page in pages
    ]
    if not any(item["file"] == "404.html" for item in manifest):
        manifest.append(
            {
                "file": "404.html",
                "status": "must-be-designed",
                "purpose": "Branded not-found route",
                "shared_system": "",
                "verified": False,
            }
        )
    return manifest


def load_inputs(index_path: Path, library_path: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    index = json.loads(index_path.read_text(encoding="utf-8"))
    library_bytes = library_path.read_bytes()
    actual_hash = hashlib.sha256(library_bytes).hexdigest()
    expected_hash = index.get("source", {}).get("sha256")
    if expected_hash != actual_hash:
        raise ValueError("design DNA index is stale; run scripts/build_lumora_index.py")
    library = json.loads(library_bytes.decode("utf-8"))
    prompt_text = {
        item["id"]: item["prompt_text"]
        for item in library.get("prompts", [])
        if isinstance(item.get("id"), str) and isinstance(item.get("prompt_text"), str) and item["prompt_text"]
    }
    return index, library, prompt_text


def lexical_score(
    record: dict[str, Any],
    prompt_text: str,
    brief_tokens: set[str],
    profile_tokens: set[str],
) -> float:
    metadata = " ".join(
        str(value or "")
        for value in (record.get("id"), record.get("title"), record.get("category"), record.get("family"))
    ).lower()
    body = prompt_text.lower()
    score = 0.0
    for token in brief_tokens:
        if token in metadata:
            score += 11.0
        count = body.count(token)
        if count:
            score += min(7.0, 1.2 + 1.4 * math.log2(count + 1))
    for token in profile_tokens - brief_tokens:
        if token in metadata:
            score += 4.0
        count = body.count(token)
        if count:
            score += min(2.2, 0.4 + 0.45 * math.log2(count + 1))
    return score


def deterministic_jitter(seed: int, slot: str, prompt_id: str) -> float:
    digest = hashlib.sha256(f"{seed}|{slot}|{prompt_id}".encode("utf-8")).hexdigest()
    unit = int(digest[:8], 16) / 0xFFFFFFFF
    return unit * 0.75


def slot_eligible(record: dict[str, Any], slot: str, profile: Profile) -> bool:
    category = str(record.get("category") or "").lower()
    if slot == "experience":
        return category in NARRATIVE_CATEGORIES
    if slot == "conversion":
        return category in PROFILE_CONVERSION_CATEGORIES[profile.name]
    return True


def source_compatibility(
    record: dict[str, Any],
    selected: list[dict[str, Any]],
    slot: str,
    brief_tokens: set[str],
) -> dict[str, Any]:
    if not selected:
        return {"score": 0.0, "supports": ["Establishes the primary experience world."], "risks": []}

    anchor = selected[0]
    anchor_dna = anchor.get("dna") or {}
    dna = record.get("dna") or {}
    score = 0.0
    supports: list[str] = []
    risks: list[str] = []

    anchor_styles = set(anchor_dna.get("styles") or []) - GENERIC_STYLES
    styles = set(dna.get("styles") or []) - GENERIC_STYLES
    shared_styles = anchor_styles.intersection(styles)
    if shared_styles:
        score += min(16.0, len(shared_styles) * 6.0)
        supports.append(f"Shares the anchor's {', '.join(sorted(shared_styles))} material or visual language.")
    elif anchor_styles and styles:
        score -= 16.0
        risks.append("Introduces a separate visual style with no anchor overlap.")

    anchor_media = set(anchor_dna.get("media") or [])
    media = set(dna.get("media") or [])
    shared_media = anchor_media.intersection(media)
    if shared_media:
        score += min(12.0, len(shared_media) * 4.0)
        supports.append(f"Can reuse the anchor's {', '.join(sorted(shared_media))} asset language.")

    anchor_motion = set(anchor_dna.get("motion") or [])
    motion = set(dna.get("motion") or [])
    if anchor_motion.intersection(DOMINANT_SCROLL_MOTION) and motion.intersection(DOMINANT_SCROLL_MOTION):
        score -= 44.0
        risks.append("Competes with the anchor through a second dominant scroll system.")
    elif anchor_motion.intersection(motion):
        score += 8.0
        supports.append("Extends an existing motion language instead of adding another one.")

    anchor_layouts = set(anchor_dna.get("layouts") or [])
    layouts = set(dna.get("layouts") or [])
    if anchor_layouts.intersection(DOMINANT_LAYOUTS) and layouts.intersection(DOMINANT_LAYOUTS):
        score -= 30.0
        risks.append("Competes for sticky, pinned, or horizontal page authority.")
    elif anchor_layouts.intersection(layouts):
        score += 7.0
        supports.append("Uses a compatible spatial relationship.")

    spatial = set(dna.get("styles") or []).union(media).intersection(SPATIAL_SIGNALS)
    anchor_spatial = set(anchor_dna.get("styles") or []).union(anchor_media).intersection(SPATIAL_SIGNALS)
    if spatial and not anchor_spatial and not brief_tokens.intersection({"3d", "spatial", "webgl", "model", "object"}):
        score -= 28.0
        risks.append("Adds a 3D or spatial world that the brief and anchor do not support.")

    roles = set(dna.get("roles") or [])
    if slot != "anchor" and "complete-page" in roles:
        score -= 14.0
        risks.append("A complete-page donor must be reduced to one local mechanism.")
    if slot != "anchor" and str(record.get("category") or "").lower() in {"hero", "hero section"}:
        score -= 26.0
        risks.append("A second hero concept would compete with the anchor opening.")

    for existing in selected[1:]:
        existing_dna = existing.get("dna") or {}
        if set(existing_dna.get("motion") or []).intersection(DOMINANT_SCROLL_MOTION) and motion.intersection(DOMINANT_SCROLL_MOTION):
            score -= 24.0
            risks.append("Duplicates a dominant motion system already introduced by a supporting donor.")

    if record.get("family") == anchor.get("family"):
        score -= 80.0
        risks.append("Duplicates the anchor prompt family.")

    if not risks:
        supports.append("Adds a narrow capability without challenging the anchor's authority.")
    return {"score": round(score, 2), "supports": supports[:4], "risks": risks[:4]}


def slot_score(
    record: dict[str, Any],
    prompt_text: str,
    slot: str,
    brief_tokens: set[str],
    profile_tokens: set[str],
    profile: Profile,
    selected: list[dict[str, Any]],
    seed: int,
) -> float:
    if not record.get("available") or record.get("id") in BANNED_IDS:
        return -10_000.0

    config = SLOT_CONFIG[slot]
    dna = record.get("dna") or {}
    roles = set(dna.get("roles") or [])
    score = lexical_score(record, prompt_text, brief_tokens, profile_tokens)
    configured_matches = sorted((weight for role, weight in config["roles"].items() if role in roles), reverse=True)
    if configured_matches:
        score += configured_matches[0] + min(15.0, max(0, len(configured_matches) - 1) * 4.0)
    if str(record.get("category") or "").lower() in config["categories"]:
        score += 34.0

    motion = set(dna.get("motion") or [])
    layouts = set(dna.get("layouts") or [])
    media = set(dna.get("media") or [])
    interactions = set(dna.get("interactions") or [])
    dynamic_roles = PROFILE_ROLE_PREFERENCES[profile.name].get(slot, ())
    dynamic_match = roles.intersection(dynamic_roles)
    dynamic_weights = [max(12.0, 62.0 - index * 11.0) for index, role in enumerate(dynamic_roles) if role in roles]
    if dynamic_weights:
        score += max(dynamic_weights) + min(12.0, max(0, len(dynamic_weights) - 1) * 3.0)

    lower_metadata = " ".join(str(value or "") for value in (record.get("id"), record.get("title"), record.get("category"))).lower()
    lower_body = prompt_text.lower()
    for keyword in profile.keywords:
        if keyword in lower_metadata:
            score += 24.0
        elif keyword in lower_body:
            score += 7.0

    if slot == "anchor":
        score += min(38.0, len(layouts) * 3.0 + len(dna.get("styles") or []) * 2.0 + len(media) * 2.0)
        score += min(18.0, len(motion.intersection(ADVANCED_MOTION)) * 3.0)
        if record.get("preview", {}).get("video") or record.get("preview", {}).get("image"):
            score += 8.0
        if "complete-page" not in roles and str(record.get("category") or "").lower() not in SLOT_CONFIG["anchor"]["categories"]:
            score -= 105.0
        if "complete-page" not in roles and "hero" not in roles:
            score -= 40.0
    elif slot == "experience":
        score += min(24.0, len(interactions) * 3.0 + len(layouts) * 1.5)
        if not dynamic_match:
            score -= 70.0
        if "complete-page" in roles:
            score -= 26.0
        if str(record.get("category") or "").lower() in {"hero", "hero section", "landing page", "website"}:
            score -= 42.0
        score -= max(0, len(roles) - 5) * 4.0
    elif slot == "conversion":
        score += min(18.0, len(interactions) * 2.0)
        if not dynamic_match:
            score -= 85.0
        if "complete-page" in roles:
            score -= 32.0
        score -= max(0, len(roles) - 5) * 3.0

    length = int(record.get("prompt_length") or 0)
    if 4000 <= length <= 26000:
        score += 9.0
    elif length > 45000:
        score -= 9.0
    elif length < 1200:
        score -= 7.0

    if "responsive-specified" in set(dna.get("constraints") or []):
        score += 4.0
    if record.get("static_portability") == "complex-adaptation" and slot != "anchor":
        score -= 8.0

    selected_families = Counter(item.get("family") for item in selected)
    if selected_families[record.get("family")]:
        score -= 60.0 * selected_families[record.get("family")]
    styles = set(dna.get("styles") or [])
    if styles and slot == "anchor":
        score += 2.0
    if slot == "anchor" and str(record.get("category") or "").lower() in {"3d website", "creative / 3d"} and not brief_tokens.intersection({"3d", "spatial", "webgl", "model", "object"}):
        score -= 38.0
    score += source_compatibility(record, selected, slot, brief_tokens)["score"]
    score += deterministic_jitter(seed, slot, str(record.get("id") or ""))
    return score


def select_sources(
    index: dict[str, Any],
    prompt_text: dict[str, str],
    brief: str,
    profile: Profile,
    max_sources: int,
    seed: int,
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    brief_tokens = set(tokens(brief))
    profile_tokens = set(tokens(" ".join((profile.name, " ".join(profile.expansion)))))
    selected: list[dict[str, Any]] = []
    used_ids: set[str] = set()
    shortlists: dict[str, list[dict[str, Any]]] = {}

    for slot_index, slot in enumerate(SLOT_CONFIG):
        ranked = sorted(
            (record for record in index.get("prompts", []) if slot_eligible(record, slot, profile)),
            key=lambda record: slot_score(record, prompt_text.get(record.get("id"), ""), slot, brief_tokens, profile_tokens, profile, selected, seed),
            reverse=True,
        )
        shortlist: list[dict[str, Any]] = []
        for record in ranked:
            if not record.get("available") or record.get("id") in used_ids:
                continue
            compatibility = source_compatibility(record, selected, slot, brief_tokens)
            shortlist.append(
                {
                    "id": record.get("id"),
                    "title": record.get("title"),
                    "category": record.get("category"),
                    "family": record.get("family"),
                    "score": round(slot_score(record, prompt_text.get(record.get("id"), ""), slot, brief_tokens, profile_tokens, profile, selected, seed), 2),
                    "compatibility": compatibility,
                    "inspection_command": (
                        f"python scripts/inspect_lumora_prompt.py --id {record.get('id')} --full"
                        if slot == "anchor"
                        else f"python scripts/inspect_lumora_prompt.py --id {record.get('id')} --focus {SLOT_CONFIG[slot]['focus']}"
                    ),
                }
            )
            if len(shortlist) >= 5:
                break
        shortlists[slot] = shortlist
        if slot_index >= max_sources:
            continue
        used_families = {source.get("family") for source in selected}
        chosen = next(
            (
                record
                for record in ranked
                if record.get("id") not in used_ids
                and record.get("available")
                and record.get("family") not in used_families
                and source_compatibility(record, selected, slot, brief_tokens)["score"] >= -8.0
            ),
            None,
        )
        if chosen is None:
            continue
        source = dict(chosen)
        source["job"] = slot
        source["selection_score"] = round(slot_score(chosen, prompt_text.get(chosen["id"], ""), slot, brief_tokens, profile_tokens, profile, selected, seed), 2)
        source["compatibility"] = source_compatibility(chosen, selected, slot, brief_tokens)
        selected.append(source)
        used_ids.add(chosen["id"])
    return selected, shortlists


def atoms_for(source: dict[str, Any]) -> list[str]:
    dna = source.get("dna") or {}
    job = source["job"]
    group_order = {
        "anchor": ("layouts", "styles", "media", "motion", "interactions"),
        "experience": ("layouts", "interactions", "media", "motion", "roles"),
        "conversion": ("interactions", "layouts", "motion", "roles"),
    }[job]
    atoms: list[str] = []
    for group in group_order:
        for tag in dna.get(group, []):
            if tag not in atoms:
                atoms.append(tag)
            if len(atoms) >= 7:
                return atoms
    return atoms


def evidence_for(source: dict[str, Any], atoms: list[str]) -> list[str]:
    evidence = source.get("evidence") or {}
    snippets: list[str] = []
    for group in ("layouts", "styles", "media", "motion", "interactions", "roles"):
        for atom in atoms:
            snippet = (evidence.get(group) or {}).get(atom)
            if snippet and snippet not in snippets:
                snippets.append(snippet)
            if len(snippets) >= 3:
                return snippets
    return snippets


def inspection_for(source: dict[str, Any]) -> dict[str, str]:
    job = source["job"]
    prompt_id = source["id"]
    if job == "anchor":
        return {"mode": "full", "command": f"python scripts/inspect_lumora_prompt.py --id {prompt_id} --full"}
    focus = SLOT_CONFIG[job]["focus"]
    return {"mode": "focused", "command": f"python scripts/inspect_lumora_prompt.py --id {prompt_id} --focus {focus}"}


def source_reason(source: dict[str, Any], profile: Profile) -> str:
    atoms = atoms_for(source)
    atom_text = ", ".join(atom.replace("-", " ") for atom in atoms[:4]) or "detailed source behavior"
    return f"Selected as the {source['job']} donor for the {profile.name} profile because it contributes {atom_text}."


def selected_source_payload(source: dict[str, Any], profile: Profile) -> dict[str, Any]:
    atoms = atoms_for(source)
    return {
        "job": source["job"],
        "id": source["id"],
        "title": source.get("title"),
        "category": source.get("category"),
        "family": source.get("family"),
        "selection_score": source.get("selection_score"),
        "prompt_length": source.get("prompt_length"),
        "prompt_sha256": source.get("prompt_sha256"),
        "static_portability": source.get("static_portability"),
        "authority": {"anchor": 0.75, "experience": 0.15, "conversion": 0.10}[source["job"]],
        "compatibility": source.get("compatibility") or {"score": 0.0, "supports": [], "risks": []},
        "compatibility_resolution": "",
        "why": source_reason(source, profile),
        "source_atoms": atoms,
        "source_evidence": evidence_for(source, atoms),
        "inspection": inspection_for(source),
        "implemented_contributions": [],
        "implemented_sections": [],
    }


def source_section_map(sections: tuple[str, ...], selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_job = {source["job"]: source["id"] for source in selected}
    mapping: list[dict[str, Any]] = []
    experience_index = min(3, max(1, len(sections) // 3))
    conversion_names = {"pricing", "variants-and-purchase", "booking", "contact", "tickets-or-action", "configure-or-contact", "closing", "newsletter"}
    conversion_indexes = [index for index, name in enumerate(sections) if name in conversion_names]
    conversion_index = conversion_indexes[0] if conversion_indexes else len(sections) - 1
    for index, name in enumerate(sections):
        jobs = ["anchor"] if "anchor" in by_job else []
        if index == experience_index and "experience" in by_job:
            jobs.append("experience")
        if index == conversion_index and "conversion" in by_job:
            jobs.append("conversion")
        mapping.append(
            {
                "section_id": slug(name),
                "purpose": name.replace("-", " "),
                "source_jobs": jobs,
                "source_ids": [by_job[job] for job in jobs],
                "implementation_notes": [],
            }
        )
    return mapping


def build_plan(
    brief: str,
    index: dict[str, Any],
    prompt_text: dict[str, str],
    requested_pages: str,
    seed_value: str | None,
    max_sources: int,
    requested_origin: str = "auto",
) -> dict[str, Any]:
    profile, profile_signals = infer_profile(brief)
    mode = page_mode(brief, requested_pages)
    origin = site_origin(brief, requested_origin)
    seed_material = "|".join((brief.strip(), seed_value or "", index["source"]["sha256"]))
    seed = int(hashlib.sha256(seed_material.encode("utf-8")).hexdigest()[:16], 16)
    selected, shortlists = select_sources(index, prompt_text, brief, profile, max_sources, seed)
    source_payload = [selected_source_payload(source, profile) for source in selected]
    anchor = selected[0] if selected else {}
    anchor_dna = anchor.get("dna") or {}
    pages = page_map(profile, mode)
    return {
        "schema": "lumora.project_plan.v5",
        "brief": brief,
        "brief_sha256": hashlib.sha256(brief.encode("utf-8")).hexdigest(),
        "creative_seed": seed,
        "profile": {
            "name": profile.name,
            "signals": profile_signals,
            "content_inventory": list(profile.sections),
            "note": "This is a content inventory, not a required section order or layout template.",
        },
        "build_contract": {
            "default_stack": "static HTML, CSS, and JavaScript",
            "github_pages_source": "repository root",
            "vite_by_default": False,
            "relative_urls_required": True,
            "base_files": ["index.html", "styles.css", "script.js", "404.html", ".nojekyll"],
            "page_mode": mode,
            "pages": pages,
            "site_origin": origin,
            "publishing_root": ".",
            "route_strategy": "",
            "source_route_inventory": [],
            "route_manifest": initial_route_manifest(pages),
            "route_migrations": [],
            "source_archive_location": "",
            "route_rules": [
                "Inventory every public route before implementation when site_origin is existing.",
                "Keep source scrapes, legacy runtime files, references, and validation mirrors outside this publishing root.",
                "Every shipped HTML file must appear in route_manifest and use the current shared system or a branded accessible redirect.",
                "Validate this exact directory, never a reduced copy or handcrafted subset.",
            ],
        },
        "company_truth": {
            "status": "must-be-completed-before-direction",
            "name": "",
            "offer": "",
            "audience": "",
            "difference": "",
            "proof": [],
            "material_world": [],
            "place_or_context": "",
            "vocabulary": [],
            "real_routes": [],
            "available_media": [],
            "missing_facts": [],
        },
        "direction_exploration": {
            "status": "three-distinct-worlds-required",
            "minimum_concepts": 3,
            "concepts": [],
            "selected_concept_id": "",
            "selection_reason": "",
            "rejected_concepts": [],
        },
        "creative_direction": {
            "status": "must-be-refined-before-code",
            "creative_thesis": "",
            "experience_world": "",
            "signature_object": "",
            "signature_motif": "",
            "material_language": "",
            "spatial_logic": "",
            "camera_behavior": "",
            "transformation": "",
            "emotional_arc": "",
            "interaction_thesis": "",
            "company_specificity_test": "",
            "substitution_failure": "",
            "category_conventions": [],
            "deliberate_departure": "",
            "narrative_arc": {
                "entry": "",
                "orientation": "",
                "deepening": "",
                "evidence": "",
                "decision": "",
                "close": "",
            },
            "composition_map": [],
            "design_fingerprint": {
                "composition": "",
                "typography": "",
                "palette_logic": "",
                "material": "",
                "media_mode": "",
                "shape_language": "",
                "section_rhythm": "",
                "signature_motion": "",
                "structural_motion": "",
                "library_signals": {
                    "anchor_layouts": list(anchor_dna.get("layouts") or []),
                    "anchor_styles": list(anchor_dna.get("styles") or []),
                    "anchor_media": list(anchor_dna.get("media") or []),
                    "anchor_motion": list(anchor_dna.get("motion") or []),
                    "type_candidates": list(profile.type_directions),
                    "palette_candidates": list(profile.palette_directions),
                },
            },
            "experience_keyframes": [
                {"id": "entry", "purpose": "First-viewport world, subject, and invitation", "description": "", "reference_asset": ""},
                {"id": "signature-state", "purpose": "The experience at its most transformed or interactive", "description": "", "reference_asset": ""},
                {"id": "decision", "purpose": "Closing state where story and conversion become one", "description": "", "reference_asset": ""},
            ],
            "originality_scorecard": [
                {"dimension": "company-specificity", "score": 0, "evidence": ""},
                {"dimension": "concept-unity", "score": 0, "evidence": ""},
                {"dimension": "hero-memorability", "score": 0, "evidence": ""},
                {"dimension": "asset-authorship", "score": 0, "evidence": ""},
                {"dimension": "section-rhythm", "score": 0, "evidence": ""},
                {"dimension": "motion-relevance", "score": 0, "evidence": ""},
                {"dimension": "typographic-character", "score": 0, "evidence": ""},
                {"dimension": "conversion-integration", "score": 0, "evidence": ""},
                {"dimension": "mobile-recomposition", "score": 0, "evidence": ""},
                {"dimension": "category-departure", "score": 0, "evidence": ""},
            ],
            "anti_generic_constraints": [
                "No decorative CSS blobs, gradient orbs, primitive pseudo-art, or empty mockups.",
                "No fixed aesthetic, section formula, or effect checklist may replace company-specific art direction.",
                "No equal card row or repeated split section unless the content and experience world require it.",
                "No invented reviews, awards, clients, metrics, people, prices, or product claims.",
                "No familiar category styling may be the entire concept; define a deliberate departure.",
                "No supporting donor may introduce a second page world, hero, or dominant scroll system.",
                "Ambition is allowed: film, 3D, canvas, shaders, spatial sound, unconventional navigation, and nonlinear layouts are available when the locked concept requires them and fallbacks remain usable.",
            ],
        },
        "source_selection": {
            "status": "provisional-until-candidates-are-inspected",
            "model": "one anchor plus zero to two narrow supporting donors",
            "authority_budget": {"anchor": 0.75, "experience": 0.15, "conversion": 0.10},
            "candidate_shortlists": shortlists,
            "inspected_candidates": [],
            "compatibility_statement": "",
            "rejected_candidates": [],
        },
        "source_mix": source_payload,
        "source_to_section_map": source_section_map(profile.sections, selected),
        "media_plan": {
            "status": "campaign-system-must-be-directed-before-code",
            "asset_strategy": "",
            "asset_layers": {
                "signature": [],
                "narrative": [],
                "supporting": [],
                "utility": [],
            },
            "asset_decomposition_review": "",
            "signature_asset": {
                "required": True,
                "status": "unresolved",
                "role": "",
                "subject": "",
                "medium": "",
                "company_reason": "",
                "source_or_generation_method": "",
            },
            "continuity_bible": {
                "subjects": "",
                "camera_and_lens": "",
                "lighting": "",
                "materials": "",
                "environment": "",
                "palette_and_grade": "",
                "texture_and_finish": "",
                "crop_behavior": "",
                "negative_constraints": "",
            },
            "reference_set": [
                {"id": "entry", "status": "required", "prompt": "", "analysis": ""},
                {"id": "signature-state", "status": "required", "prompt": "", "analysis": ""},
                {"id": "decision", "status": "required", "prompt": "", "analysis": ""},
            ],
            "required_roles": list(profile.media_slots),
            "slots": [],
            "generated_assets": [],
            "asset_coverage_review": "",
            "rules": [
                "Audit all supplied media and keep only assets that can carry their assigned render size and truth role.",
                "Generate three connected experience references before coding when no complete supplied design direction exists.",
                "Generate or art-direct a coherent family of final assets for every unresolved prominent slot, including small transition and detail assets when they support the world.",
                "Decompose references into signature media, narrative scenes, supporting cutouts/textures/masks, and utility assets; never ship a reference comp as a section screenshot.",
                "Generate final assets per role and aspect ratio; do not crop one image into every role.",
                "Every media slot must define its text relationship, desktop frame, mobile frame, and motion role before implementation.",
                "Every asset-layer target uses page.html#section-id and must resolve to a shipped section.",
                "Each target section declares the integrated asset ids in data-lumora-assets.",
                "Keep text and logos out of generated raster media.",
                "Do not portray generated people, premises, outcomes, products, or credentials as documentary evidence.",
                "Do not hotlink MotionSites example assets.",
            ],
        },
        "motion_plan": {
            "status": "storyboard-required-before-implementation",
            "dominant_interaction": {
                "name": "",
                "subject": "",
                "input": "",
                "transformation": "",
                "narrative_purpose": "",
                "desktop_implementation": "",
                "mobile_recomposition": "",
                "reduced_motion": "",
            },
            "mobile_signature": {
                "mode": "",
                "input": "",
                "subject": "",
                "visible_change": "",
                "implementation": "",
                "fallback": "",
                "verified": False,
            },
            "structural_language": "",
            "micro_interactions": [],
            "supporting_moments": [],
            "continuity_map": {
                "entry": "",
                "orientation": "",
                "deepening": "",
                "evidence": "",
                "decision": "",
                "close": "",
            },
            "choreography_beats": [],
            "competing_systems_removed": [],
            "scroll_occupancy_rule": "Every viewport of scroll must create a visible narrative, spatial, or informational change; no spacer-only travel.",
            "long_scroll_justification": "",
            "dependency_strategy": "",
            "rules": [
                "Mobile is not reduced motion: preserve a real company-specific visible transformation unless the user prefers reduced motion.",
                "Do not set mobile progress directly to its final state or activate every signature state at load.",
                "Author at least two lower-intensity supporting moments in distinct later sections and mark them with data-lumora-motion.",
                "Generic fade-up reveals may support ordinary copy but do not satisfy supporting_moments.",
            ],
        },
        "conversion_plan": {
            "primary_action": "",
            "truthful_destination": "",
            "readiness_moment": "",
            "story_integration": "",
            "secondary_actions": [],
        },
        "director_review": {
            "status": "required-after-first-browser-render",
            "revision_rounds": 0,
            "strongest_decision": "",
            "weakest_decision": "",
            "generic_risks": [],
            "revisions_required": [],
            "revisions_completed": [],
        },
        "verification": {
            "viewports": ["320x780", "360x800", "390x844", "430x932", "768x1024", "1024x900", "1440x1000", "1920x1080 when full-bleed or canvas framing needs it"],
            "required": [
                "entry, 25%, 50%, 75%, and closing scroll-state screenshots on desktop",
                "entry, signature, and full-page screenshots on mobile plus one tablet state",
                "every published route tested at 390 and 1440 widths; index and interaction-heavy routes tested across the full viewport matrix",
                "working navigation, controls, routes, and truthful forms",
                "no console errors or failed local assets",
                "no unintended blank viewport, dead scroll, horizontal overflow, or unrelated section overlap",
                "no overflow-x hidden or clip on html, body, or :root; identify and fix the actual overflowing element",
                "the exact GitHub Pages publishing root matches the route manifest; no source scrape or validation mirror is shipped",
                "reduced-motion and touch verification",
                "reference-to-build comparison and one completed director revision round",
                "scripts/validate_lumora_site.py --strict passes",
            ],
            "publishing_root_review": "",
            "responsive_review": {
                "status": "required",
                "tested_widths": [],
                "containment_results": [],
                "longest_content_checks": [],
                "mobile_media_review": "",
            },
            "visual_review": {
                "status": "required",
                "checked_states": [],
                "dead_space_review": "",
                "reference_comparison": "",
                "mobile_recomposition_review": "",
                "mobile_signature_review": "",
                "motion_continuity_review": "",
                "image_composition_review": "",
                "route_consistency_review": "",
                "interaction_review": "",
                "revisions_after_review": [],
            },
        },
    }


def print_markdown(plan: dict[str, Any], output: Path | None) -> None:
    print("# Lumora Creative Selection")
    print()
    print(f"Profile: {plan['profile']['name']}")
    print(f"Site origin: {plan['build_contract']['site_origin']}")
    print(f"Pages: {plan['build_contract']['page_mode']}")
    print(f"Creative seed: {plan['creative_seed']}")
    if output:
        print(f"Plan: {output.resolve()}")
    print()
    print("## Provisional anchor-led source mix")
    for source in plan["source_mix"]:
        print(f"- {source['job']}: {source['id']} ({source['title']})")
        print(f"  Inspect: {source['inspection']['command']}")
        print(f"  Atoms: {', '.join(source['source_atoms'])}")
        if source["job"] != "anchor":
            print(f"  Compatibility: {source['compatibility']['score']}")
    print()
    print("## Required direction work")
    print("- Complete the company-truth inventory.")
    print("- Inspect at least three anchor candidates and write three genuinely different experience worlds.")
    print("- Select one world, lock the anchor, and add a support donor only for a concrete unsolved need.")
    print("- Direct three connected visual keyframes and the complete asset campaign before coding.")
    print()
    print("Do not code until the company truth, selected world, source compatibility, asset system, motion storyboard, and conversion plan are locked in lumora-plan.json.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", help="Complete company and website brief")
    parser.add_argument("--pages", choices=("auto", "one", "multi"), default="auto")
    parser.add_argument("--site-origin", choices=("auto", "new", "existing"), default="auto")
    parser.add_argument("--seed", help="Optional alternate-direction seed")
    parser.add_argument("--max-sources", type=int, choices=(1, 2, 3), default=1)
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--output", type=Path, help="Write JSON plan to this path")
    parser.add_argument("--json", action="store_true", help="Write full JSON to stdout")
    args = parser.parse_args()

    try:
        index, _library, prompt_text = load_inputs(args.index.resolve(), args.library.resolve())
        plan = build_plan(args.brief, index, prompt_text, args.pages, args.seed, args.max_sources, args.site_origin)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(plan, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        if args.json:
            print(json.dumps(plan, ensure_ascii=True, indent=2))
        else:
            print_markdown(plan, args.output)
        return 0
    except Exception as exc:
        raise SystemExit(f"ERROR: {exc}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
