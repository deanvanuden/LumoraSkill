#!/usr/bin/env python3
"""Create a traceable Lumora creative plan from the full prompt library."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
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
    "foundation": {
        "roles": {"complete-page": 75, "hero": 12, "features": 8},
        "categories": {"landing page", "website", "saas", "agency", "ecommerce", "automotive", "travel"},
        "focus": "layout,visual,media,responsive",
    },
    "hero": {
        "roles": {"hero": 90, "navigation": 16, "complete-page": 12},
        "categories": {"hero", "hero section", "3d website", "creative / 3d"},
        "focus": "layout,visual,media,motion,responsive",
    },
    "narrative": {
        "roles": {"features": 40, "story-about": 40, "process": 38, "portfolio-gallery": 38, "product-commerce": 38, "services": 34, "proof": 24},
        "categories": {"features", "features section", "about", "process", "portfolio", "projects", "product", "products", "services", "benefits", "cards", "tabs"},
        "focus": "layout,visual,media,interaction,responsive",
    },
    "motion": {
        "roles": {"hero": 10, "complete-page": 8, "portfolio-gallery": 8},
        "categories": {"interactive", "animation", "3d website", "creative / 3d", "slider", "carousal", "marquee"},
        "focus": "motion,interaction,media,responsive",
    },
    "conversion": {
        "roles": {"cta": 65, "pricing": 58, "contact-booking": 55, "footer": 45, "form-auth": 34, "product-commerce": 24},
        "categories": {"cta", "cta section", "pricing", "contact us", "footer section", "signup", "waitlist", "form", "ecommerce"},
        "focus": "conversion,interaction,layout,responsive",
    },
}


ADVANCED_MOTION = {
    "scroll-scrub", "pinned-scroll", "parallax", "mask-reveal", "split-text", "text-scramble", "marquee",
    "magnetic", "tilt-depth", "hover-reveal", "page-transition", "morph", "liquid", "video-scrub",
    "image-sequence", "drag-gesture", "count-up", "theme-transition",
}

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
        "narrative": ("product-commerce", "features", "process", "proof"),
        "conversion": ("product-commerce", "pricing", "cta", "contact-booking"),
    },
    "saas-product": {
        "narrative": ("dashboard-app", "features", "process", "proof"),
        "conversion": ("pricing", "cta", "form-auth", "contact-booking"),
    },
    "creative-studio": {
        "narrative": ("portfolio-gallery", "services", "process", "story-about"),
        "conversion": ("contact-booking", "cta", "footer", "form-auth"),
    },
    "hospitality-place": {
        "narrative": ("portfolio-gallery", "story-about", "product-commerce", "proof"),
        "conversion": ("contact-booking", "cta", "footer", "form-auth"),
    },
    "architecture-property": {
        "narrative": ("portfolio-gallery", "story-about", "process", "services"),
        "conversion": ("contact-booking", "cta", "footer", "form-auth"),
    },
    "local-service": {
        "narrative": ("services", "process", "proof", "story-about"),
        "conversion": ("contact-booking", "form-auth", "cta", "footer"),
    },
    "culture-editorial": {
        "narrative": ("portfolio-gallery", "story-about", "product-commerce", "process"),
        "conversion": ("cta", "form-auth", "contact-booking", "footer"),
    },
    "automotive-spatial": {
        "narrative": ("product-commerce", "features", "portfolio-gallery", "process"),
        "conversion": ("product-commerce", "contact-booking", "cta", "footer"),
    },
    "professional-trust": {
        "narrative": ("services", "proof", "process", "story-about"),
        "conversion": ("contact-booking", "cta", "form-auth", "pricing"),
    },
    "brand-story": {
        "narrative": ("features", "story-about", "services", "process"),
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
    multipage_terms = ("multi page", "multipage", "multiple pages", "full website", "full company website", "site map", "separate pages", "routes")
    return "multi" if any(term in lower for term in multipage_terms) else "one"


def page_map(profile: Profile, mode: str) -> list[dict[str, Any]]:
    if mode == "one":
        return [{"file": "index.html", "label": "Home", "sections": list(profile.sections)}]
    return [
        {"file": file, "label": label, "sections": list(sections)}
        for file, label, sections in profile.multi_pages
    ]


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
    amplitude = 3.0 if slot in {"foundation", "hero"} else 12.0
    return unit * amplitude


def slot_eligible(record: dict[str, Any], slot: str, profile: Profile) -> bool:
    category = str(record.get("category") or "").lower()
    if slot == "narrative":
        return category in NARRATIVE_CATEGORIES
    if slot == "conversion":
        return category in PROFILE_CONVERSION_CATEGORIES[profile.name]
    return True


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

    if slot == "foundation":
        score += min(24.0, len(layouts) * 3.0 + len(dna.get("styles") or []) * 1.5)
        if "complete-page" not in roles and str(record.get("category") or "").lower() not in {"landing page", "website", "saas", "agency", "ecommerce", "automotive", "travel"}:
            score -= 100.0
    elif slot == "hero":
        score += min(22.0, len(media) * 3.0 + len(layouts) * 2.0)
        score += 8.0 if record.get("preview", {}).get("video") or record.get("preview", {}).get("image") else 0.0
        if "hero" not in roles:
            score -= 80.0
        if str(record.get("category") or "").lower() not in {"hero", "hero section"}:
            score -= 12.0
    elif slot == "narrative":
        score += min(24.0, len(interactions) * 3.0 + len(layouts) * 1.5)
        if not dynamic_match:
            score -= 70.0
        if "complete-page" in roles:
            score -= 38.0
        if str(record.get("category") or "").lower() in {"hero", "hero section", "landing page", "website"}:
            score -= 28.0
        score -= max(0, len(roles) - 5) * 4.0
    elif slot == "motion":
        score += min(45.0, len(motion.intersection(ADVANCED_MOTION)) * 7.0)
        score += 12.0 if record.get("preview", {}).get("video") else 0.0
        score += 7.0 if "reduced-motion-specified" in set(dna.get("constraints") or []) else 0.0
        if not motion.intersection(ADVANCED_MOTION):
            score -= 120.0
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
    if record.get("static_portability") == "complex-adaptation" and slot not in {"hero", "motion"}:
        score -= 8.0

    selected_families = Counter(item.get("family") for item in selected)
    if selected_families[record.get("family")]:
        score -= 45.0 * selected_families[record.get("family")]
    selected_tags = {
        tag
        for item in selected
        for group in ("styles", "layouts", "motion", "media", "interactions")
        for tag in (item.get("dna", {}).get(group) or [])
    }
    novel_tags = set().union(styles := set(dna.get("styles") or []), layouts, motion, media, interactions) - selected_tags
    score += min(15.0, len(novel_tags) * 1.5)
    if styles and slot in {"foundation", "hero"}:
        score += 2.0
    if slot == "hero" and str(record.get("category") or "").lower() in {"3d website", "creative / 3d"} and not brief_tokens.intersection({"3d", "spatial", "webgl", "model"}):
        score -= 42.0
    if slot == "motion" and str(record.get("category") or "").lower() in {"3d website", "creative / 3d"} and not brief_tokens.intersection({"3d", "spatial", "webgl", "model"}):
        score -= 45.0
    score += deterministic_jitter(seed, slot, str(record.get("id") or ""))
    return score


def select_sources(
    index: dict[str, Any],
    prompt_text: dict[str, str],
    brief: str,
    profile: Profile,
    max_sources: int,
    seed: int,
) -> list[dict[str, Any]]:
    brief_tokens = set(tokens(brief))
    profile_tokens = set(tokens(" ".join((profile.name, " ".join(profile.expansion)))))
    selected: list[dict[str, Any]] = []
    used_ids: set[str] = set()

    for slot in list(SLOT_CONFIG)[:max_sources]:
        ranked = sorted(
            (record for record in index.get("prompts", []) if slot_eligible(record, slot, profile)),
            key=lambda record: slot_score(record, prompt_text.get(record.get("id"), ""), slot, brief_tokens, profile_tokens, profile, selected, seed),
            reverse=True,
        )
        used_families = {source.get("family") for source in selected}
        chosen = next(
            (
                record
                for record in ranked
                if record.get("id") not in used_ids
                and record.get("available")
                and record.get("family") not in used_families
            ),
            None,
        )
        if chosen is None:
            chosen = next((record for record in ranked if record.get("id") not in used_ids and record.get("available")), None)
        if chosen is None:
            continue
        source = dict(chosen)
        source["job"] = slot
        source["selection_score"] = round(slot_score(chosen, prompt_text.get(chosen["id"], ""), slot, brief_tokens, profile_tokens, profile, selected, seed), 2)
        selected.append(source)
        used_ids.add(chosen["id"])
    return selected


def choose_tag(rng: random.Random, selected: list[dict[str, Any]], group: str, fallback: tuple[str, ...]) -> str:
    counter = Counter(tag for source in selected for tag in source.get("dna", {}).get(group, []))
    candidates = [tag for tag, _ in counter.most_common(4) if tag not in {"centered-stage", "dark", "light"}]
    return rng.choice(candidates[:3] or list(fallback))


def atoms_for(source: dict[str, Any]) -> list[str]:
    dna = source.get("dna") or {}
    job = source["job"]
    group_order = {
        "foundation": ("layouts", "styles", "media"),
        "hero": ("layouts", "media", "motion"),
        "narrative": ("layouts", "interactions", "media", "motion", "roles"),
        "motion": ("motion", "interactions", "layouts"),
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
    if job == "foundation":
        return {"mode": "full", "command": f"python scripts/inspect_lumora_prompt.py --id {prompt_id} --full"}
    if job == "hero" and int(source.get("prompt_length") or 0) <= 18000:
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
    for index, name in enumerate(sections):
        jobs = ["foundation"] if "foundation" in by_job else []
        if index == 0 and "hero" in by_job:
            jobs.append("hero")
        elif name in {"pricing", "variants-and-purchase", "booking", "contact", "tickets-or-action", "configure-or-contact", "closing"} and "conversion" in by_job:
            jobs.append("conversion")
        elif index in {3, 4} and "motion" in by_job:
            jobs.extend(["narrative", "motion"] if "narrative" in by_job else ["motion"])
        elif "narrative" in by_job:
            jobs.append("narrative")
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
) -> dict[str, Any]:
    profile, profile_signals = infer_profile(brief)
    mode = page_mode(brief, requested_pages)
    seed_material = "|".join((brief.strip(), seed_value or "", index["source"]["sha256"]))
    seed = int(hashlib.sha256(seed_material.encode("utf-8")).hexdigest()[:16], 16)
    rng = random.Random(seed)
    selected = select_sources(index, prompt_text, brief, profile, max_sources, seed)
    source_payload = [selected_source_payload(source, profile) for source in selected]

    foundation_source = next((source for source in selected if source["job"] == "foundation"), selected[0] if selected else {})
    foundation_layouts = [
        tag
        for tag in foundation_source.get("dna", {}).get("layouts", [])
        if tag not in {"centered-stage", "tabs", "carousel", "timeline"}
    ]
    foundation_styles = [tag for tag in foundation_source.get("dna", {}).get("styles", []) if tag not in {"dark", "light"}]
    composition = rng.choice(foundation_layouts[:3] or ["editorial-offset", "cinematic-stage", "gallery-cadence"])
    material = rng.choice(foundation_styles[:3] or ["tactile", "editorial", "minimal"])
    hero_source = next((source for source in selected if source["job"] == "hero"), selected[0] if selected else {})
    hero_media = hero_source.get("dna", {}).get("media", [])
    media_mode = rng.choice(hero_media[:3] or ["photography", "product-render", "gallery"])
    signature_motion = next(
        (
            tag
            for source in selected
            if source["job"] == "motion"
            for tag in source.get("dna", {}).get("motion", [])
            if tag in ADVANCED_MOTION
        ),
        choose_tag(rng, selected, "motion", ("mask-reveal", "parallax", "scroll-trigger")),
    )
    structural_motion = next(
        (tag for tag in ("mask-reveal", "stagger", "scroll-trigger", "hover-reveal", "parallax") if any(tag in source.get("dna", {}).get("motion", []) for source in selected)),
        "restrained staggered reveal",
    )
    hero_atoms = atoms_for(hero_source)[:4] if hero_source else []
    type_direction = rng.choice(profile.type_directions)
    palette_direction = rng.choice(profile.palette_directions)
    rhythm = rng.choice(("cinematic chapters with calm proof intervals", "editorial cadence alternating media and evidence", "dense interactive chapter followed by generous visual pauses", "gallery-led progression with compact conversion moments"))

    pages = page_map(profile, mode)
    return {
        "schema": "lumora.project_plan.v3",
        "brief": brief,
        "brief_sha256": hashlib.sha256(brief.encode("utf-8")).hexdigest(),
        "creative_seed": seed,
        "profile": {
            "name": profile.name,
            "signals": profile_signals,
            "section_blueprint": list(profile.sections),
        },
        "build_contract": {
            "default_stack": "static HTML, CSS, and JavaScript",
            "github_pages_source": "repository root",
            "vite_by_default": False,
            "relative_urls_required": True,
            "base_files": ["index.html", "styles.css", "script.js", "404.html", ".nojekyll"],
            "page_mode": mode,
            "pages": pages,
        },
        "creative_direction": {
            "status": "must-be-refined-before-code",
            "creative_thesis": "",
            "signature_motif": "",
            "company_specificity_test": "",
            "design_fingerprint": {
                "composition": composition,
                "hero_source_atoms": hero_atoms,
                "typography": type_direction,
                "palette_logic": palette_direction,
                "material": material,
                "media_mode": media_mode,
                "section_rhythm": rhythm,
                "signature_motion": signature_motion,
                "structural_motion": structural_motion,
            },
            "signature_moment_prompt": f"Turn a real company subject or process into a {signature_motion.replace('-', ' ')} sequence; define the exact subject and narrative before coding.",
            "anti_generic_constraints": [
                "No decorative CSS blobs, gradient orbs, primitive pseudo-art, or empty mockups.",
                "No equal three-card feature row unless a selected source and the content both require it.",
                "No invented reviews, awards, clients, metrics, people, prices, or product claims.",
                "No generic centered dark hero unless the hero source makes it company-specific.",
                "No donor may remain in the plan without two implemented contributions.",
            ],
        },
        "source_mix": source_payload,
        "source_to_section_map": source_section_map(profile.sections, selected),
        "media_plan": {
            "status": "slots-must-be-specified-before-code",
            "art_direction_prompt": (
                f"Create an implementation-oriented website art-direction frame for: {brief}. "
                f"Use {composition.replace('-', ' ')} composition, {type_direction}, {palette_direction}, "
                f"and a {media_mode.replace('-', ' ')} media system. Show a clean first viewport plus visible continuation, "
                "clear media frames, varied section rhythm, and one company-specific focal idea. "
                "No readable raster text, no fake logo, no generic gradient orbs, no decorative primitive shapes, and no stock-looking filler."
            ),
            "required_roles": list(profile.media_slots),
            "slots": [],
            "rules": [
                "Use strong supplied company media first.",
                "Generate an implementation-oriented visual reference when no useful reference exists.",
                "Generate final assets per slot and aspect ratio; do not crop one image into every role.",
                "Keep text and logos out of generated raster media.",
                "Do not hotlink MotionSites example assets.",
            ],
        },
        "motion_plan": {
            "signature": signature_motion,
            "structural": structural_motion,
            "micro_interactions": ["action hover and press feedback", "menu and control state transitions", "focus and form feedback"],
            "desktop_implementation": "",
            "mobile_recomposition": "",
            "reduced_motion": "Expose all content immediately; remove scrub, parallax, autoplay, and large spatial movement.",
        },
        "verification": {
            "viewports": ["1440x1000", "390x844", "1920x1080 when full-bleed or canvas framing needs it"],
            "required": [
                "full-page screenshots for every route",
                "working navigation, controls, routes, and truthful forms",
                "no console errors or failed local assets",
                "no horizontal overflow or unrelated section overlap",
                "reduced-motion and touch verification",
                "scripts/validate_lumora_site.py passes",
            ],
        },
    }


def print_markdown(plan: dict[str, Any], output: Path | None) -> None:
    print("# Lumora Creative Selection")
    print()
    print(f"Profile: {plan['profile']['name']}")
    print(f"Pages: {plan['build_contract']['page_mode']}")
    print(f"Creative seed: {plan['creative_seed']}")
    if output:
        print(f"Plan: {output.resolve()}")
    print()
    print("## Source hierarchy")
    for source in plan["source_mix"]:
        print(f"- {source['job']}: {source['id']} ({source['title']})")
        print(f"  Inspect: {source['inspection']['command']}")
        print(f"  Atoms: {', '.join(source['source_atoms'])}")
    print()
    fingerprint = plan["creative_direction"]["design_fingerprint"]
    print("## Candidate fingerprint")
    print(f"- Composition: {fingerprint['composition']}")
    print(f"- Typography: {fingerprint['typography']}")
    print(f"- Palette: {fingerprint['palette_logic']}")
    print(f"- Signature motion: {fingerprint['signature_motion']}")
    print()
    print("Before coding, inspect the listed source bodies and fill the empty creative, contribution, media, and motion fields in lumora-plan.json.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", help="Complete company and website brief")
    parser.add_argument("--pages", choices=("auto", "one", "multi"), default="auto")
    parser.add_argument("--seed", help="Optional alternate-direction seed")
    parser.add_argument("--max-sources", type=int, choices=(3, 4, 5), default=5)
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--output", type=Path, help="Write JSON plan to this path")
    parser.add_argument("--json", action="store_true", help="Write full JSON to stdout")
    args = parser.parse_args()

    try:
        index, _library, prompt_text = load_inputs(args.index.resolve(), args.library.resolve())
        plan = build_plan(args.brief, index, prompt_text, args.pages, args.seed, args.max_sources)
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
