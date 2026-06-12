#!/usr/bin/env python3
"""Suggest Lumora archetypes from a short website brief.

This script prefers the bundled MotionSites prompt library when present,
falling back to the public metadata catalog.
"""

from __future__ import annotations

import re
import sys
import json
from dataclasses import dataclass, field
from pathlib import Path


TOKEN_RE = re.compile(r"[a-z0-9]+")

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "build",
    "company",
    "for",
    "in",
    "make",
    "of",
    "on",
    "page",
    "site",
    "the",
    "to",
    "website",
    "with",
}

CATEGORY_KEYWORDS = {
    "saas": {
        "ai",
        "app",
        "automation",
        "b2b",
        "dashboard",
        "productivity",
        "saas",
        "software",
        "tool",
        "workflow",
    },
    "agency": {
        "agency",
        "brand",
        "creative",
        "design",
        "portfolio",
        "studio",
        "work",
    },
    "luxury": {
        "aviation",
        "commerce",
        "ecommerce",
        "estate",
        "fashion",
        "hotel",
        "luxury",
        "premium",
        "product",
        "real",
        "travel",
        "yacht",
    },
    "fintech": {
        "bank",
        "crypto",
        "defi",
        "finance",
        "fintech",
        "investment",
        "payments",
        "wealth",
        "web3",
    },
    "security": {
        "cyber",
        "cybersecurity",
        "data",
        "infrastructure",
        "it",
        "security",
        "secure",
    },
    "motion": {
        "3d",
        "animation",
        "cinematic",
        "interactive",
        "motion",
        "parallax",
        "scroll",
        "video",
        "webgl",
    },
    "conversion": {
        "booking",
        "contact",
        "demo",
        "lead",
        "signup",
        "waitlist",
    },
    "nature": {
        "agriculture",
        "bio",
        "biotech",
        "botanical",
        "climate",
        "energy",
        "farming",
        "health",
        "medical",
        "nature",
        "solar",
    },
}

GROUP_BOOSTS = {
    "saas": {"saas", "ai", "product"},
    "agency": {"agency", "portfolio"},
    "luxury": {"commerce", "luxury", "travel", "automotive"},
    "fintech": {"fintech", "web3"},
    "security": {"security", "data", "infrastructure"},
    "motion": {"interactive", "3d", "motion", "hero"},
    "conversion": {"conversion", "utility", "signup", "waitlist"},
    "nature": {"nature", "biotech", "energy", "sustainability"},
}


@dataclass
class Archetype:
    title: str
    type_label: str
    groups: set[str] = field(default_factory=set)
    tags: set[str] = field(default_factory=set)

    @property
    def searchable(self) -> str:
        return " ".join([self.title, self.type_label, *self.groups, *self.tags])


def tokens(text: str) -> set[str]:
    return {token for token in TOKEN_RE.findall(text.lower()) if token not in STOP_WORDS}


def load_catalog(path: Path) -> list[Archetype]:
    catalog: dict[tuple[str, str], Archetype] = {}
    current_group = ""
    in_index = False

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line == "## Complete Visible Index":
            in_index = True
            current_group = ""
            continue
        if line.startswith("### "):
            current_group = line[4:].strip()
            continue
        if not line.startswith("- ") or "|" not in line:
            continue

        parts = [part.strip() for part in line[2:].split("|")]
        if len(parts) < 2:
            continue

        title, type_label = parts[0], parts[1]
        extra_tags = set()
        if len(parts) > 2:
            extra_tags |= tokens(" ".join(parts[2:]))
        if current_group:
            extra_tags |= tokens(current_group)
        if not in_index:
            extra_tags.add("curated")

        key = (title.lower(), type_label.lower())
        entry = catalog.get(key)
        if entry is None:
            entry = catalog[key] = Archetype(title=title, type_label=type_label)
        if current_group:
            entry.groups.add(current_group)
        entry.tags |= extra_tags

    return sorted(catalog.values(), key=lambda item: item.title.lower())


def load_bundled_catalog(path: Path) -> list[Archetype]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = []
    for item in data.get("prompts", []):
        metadata = item.get("metadata") or {}
        title = item.get("title") or metadata.get("title") or item.get("id")
        type_label = metadata.get("category") or metadata.get("type") or "Prompt"
        if not title:
            continue
        raw_groups = [
            metadata.get("category"),
            metadata.get("type"),
            metadata.get("page_type"),
            *(metadata.get("types") or []),
        ]
        tags = tokens(" ".join(str(value) for value in raw_groups if value))
        if item.get("prompt_text"):
            tags |= tokens(str(item["prompt_text"]))
        entries.append(
            Archetype(
                title=str(title),
                type_label=str(type_label),
                groups={str(value) for value in raw_groups if value},
                tags=tags,
            )
        )
    return sorted(entries, key=lambda item: item.title.lower())


def infer_categories(query_tokens: set[str]) -> set[str]:
    categories = set()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if query_tokens & keywords:
            categories.add(category)
    return categories


def score_entry(entry: Archetype, query_tokens: set[str], categories: set[str]) -> int:
    entry_tokens = tokens(entry.searchable)
    score = 0

    direct = query_tokens & entry_tokens
    score += len(direct) * 4

    for category in categories:
        category_terms = CATEGORY_KEYWORDS[category] | GROUP_BOOSTS.get(category, set())
        if entry_tokens & category_terms:
            score += 7
        if any(term in " ".join(entry.groups).lower() for term in GROUP_BOOSTS.get(category, set())):
            score += 5

    title_lower = entry.title.lower()
    type_lower = entry.type_label.lower()
    if "hero" in query_tokens and ("hero" in title_lower or "hero" in type_lower):
        score += 6
    if "landing" in query_tokens and "landing" in type_lower:
        score += 6
    if "premium" in query_tokens and ("luxury" in title_lower or "premium" in title_lower):
        score += 5
    if "dark" in query_tokens and "dark" in title_lower:
        score += 5

    return score


def role_hint(entry: Archetype) -> str:
    text = entry.searchable.lower()
    if any(term in text for term in ["waitlist", "signup", "contact", "booking", "404", "presentation"]):
        return "conversion"
    if any(term in text for term in ["3d", "cinematic", "interactive", "animation", "scroll", "cursor", "portal", "depth"]):
        return "visual engine"
    if any(term in text for term in ["saas", "agency", "portfolio", "fintech", "web3", "ecommerce", "travel", "security"]):
        return "market fit"
    return "support"


def main() -> int:
    query = " ".join(sys.argv[1:]).strip()
    root = Path(__file__).resolve().parents[1]
    bundled_catalog_path = root / "references" / "motionsites-prompt-library.json"
    catalog_path = root / "references" / "archetype-catalog.md"
    entries = load_bundled_catalog(bundled_catalog_path) if bundled_catalog_path.exists() else load_catalog(catalog_path)

    if not query:
        print("Usage: python scripts/select_lumora_archetypes.py \"brief text\"")
        print()
        print("Starter packs:")
        print("- AI SaaS: Minimal Workflow SaaS, AI Workflow Hero, ClearInvoice SaaS Hero, Datacore Booking")
        print("- Creative agency: Velorah, Modern Agency, Bold Studio, Scroll Landing Page, Build With Us")
        print("- Luxury product: Luxury Ecommerce Design, SkyElite Private Jets, Layered Depth, Waitlist Hero")
        print("- Security SaaS: Securify Data Security, VaultShield, Minimal Workflow SaaS, Cybersecurity Hero")
        print(f"Catalog entries: {len(entries)}")
        return 0

    query_tokens = tokens(query)
    categories = infer_categories(query_tokens)
    ranked = []
    for entry in entries:
        score = score_entry(entry, query_tokens, categories)
        if score > 0:
            ranked.append((score, entry))

    if not ranked:
        ranked = [(1, entry) for entry in entries if entry.type_label.lower() in {"landing page", "hero", "saas"}]

    ranked.sort(key=lambda item: (-item[0], item[1].title.lower()))

    print("Lumora archetype shortlist")
    print(f"Query: {query}")
    if categories:
        print("Detected categories: " + ", ".join(sorted(categories)))
    print()

    for score, entry in ranked[:14]:
        group = "; ".join(sorted(entry.groups)) if entry.groups else "General"
        print(f"- {entry.title} | {entry.type_label} | {role_hint(entry)} | score {score} | {group}")

    print()
    print("Recommended mix: choose 1 market-fit archetype, 1 visual engine, 1 conversion pattern, and 1 restraint counterweight.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
