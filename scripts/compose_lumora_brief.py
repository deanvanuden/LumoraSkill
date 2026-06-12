#!/usr/bin/env python3
"""Create a Lumora source pack from the bundled prompt library.

The output is intentionally transformative: it reports selected source names,
roles, and normalized implementation atoms, not full prompt bodies.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TOKEN_RE = re.compile(r"[a-z0-9]+")

STOP_WORDS = {
    "a",
    "about",
    "after",
    "all",
    "also",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "build",
    "but",
    "by",
    "can",
    "company",
    "create",
    "for",
    "from",
    "good",
    "has",
    "have",
    "hero",
    "in",
    "into",
    "is",
    "it",
    "its",
    "landing",
    "make",
    "new",
    "of",
    "on",
    "or",
    "page",
    "section",
    "site",
    "that",
    "the",
    "this",
    "to",
    "use",
    "using",
    "web",
    "website",
    "with",
}


SIGNALS: dict[str, list[tuple[str, tuple[str, ...]]]] = {
    "layout": [
        ("fullscreen object-led hero", ("fullscreen", "full-screen", "100vh", "viewport hero")),
        ("split hero composition", ("split layout", "split-screen", "two column", "two-column")),
        ("asymmetric editorial grid", ("asymmetric", "editorial grid", "magazine", "masonry")),
        ("bento feature system", ("bento", "feature cards", "card grid", "modular grid")),
        ("horizontal or pinned scroll sequence", ("horizontal scroll", "pinned", "sticky section", "scroll sequence")),
        ("section bands with hard transitions", ("section band", "full-width", "hard transition", "edge-to-edge")),
        ("layered depth scene", ("layered", "depth", "foreground", "background layer", "parallax layers")),
        ("dense dashboard/tool surface", ("dashboard", "workspace", "analytics", "data panel", "control panel")),
        ("accordion/tabs for detail disclosure", ("accordion", "tabs", "details", "expandable")),
        ("marquee or proof strip", ("marquee", "logo strip", "ticker", "infinite loop")),
    ],
    "visual": [
        ("oversized editorial typography", ("oversized typography", "large typography", "serif", "editorial")),
        ("premium product photography direction", ("product photography", "product shot", "packshot", "object focus")),
        ("organic premium texture", ("botanical", "organic", "nature", "flower", "plant", "earth", "natural")),
        ("cinematic dark contrast", ("cinematic", "dark", "moody", "dramatic", "spotlight")),
        ("warm luxury neutrals", ("luxury", "warm", "cream", "gold", "amber", "premium")),
        ("glass and translucent surfaces", ("glassmorphism", "frosted", "translucent", "blurred glass")),
        ("technical data aesthetic", ("technical", "blueprint", "grid lines", "data", "terminal")),
        ("3D hero object or scene", ("3d", "three.js", "webgl", "r3f", "canvas")),
        ("bold high-contrast studio identity", ("bold", "monochrome", "high contrast", "brutalist")),
        ("soft wellness palette", ("wellness", "soft", "pastel", "calm", "serene")),
    ],
    "motion": [
        ("scroll-triggered reveal pacing", ("scrolltrigger", "scroll triggered", "scroll reveal", "on scroll")),
        ("subtle pointer or parallax response", ("pointermove", "mouse", "cursor", "parallax")),
        ("ambient product/media movement", ("ambient", "floating", "drift", "looping", "slow rotation")),
        ("staggered content entrance", ("stagger", "cascade", "sequence", "delay")),
        ("magnetic or tactile buttons", ("magnetic", "hover", "microinteraction", "button animation")),
        ("masked image/video reveal", ("mask", "clip-path", "reveal", "wipe")),
        ("reduced-motion fallback", ("prefers-reduced-motion", "reduced motion", "accessibility")),
        ("smooth page transitions", ("page transition", "transition", "gsap", "framer motion")),
    ],
    "conversion": [
        ("clear primary CTA above the fold", ("cta", "call to action", "button", "above the fold")),
        ("shop or package selector", ("shop", "cart", "checkout", "bundle", "product card")),
        ("waitlist or signup form", ("waitlist", "signup", "email form", "join")),
        ("booking/demo conversion", ("book", "booking", "demo", "schedule", "calendar")),
        ("pricing/package comparison", ("pricing", "plans", "package", "tiers")),
        ("proof metrics and testimonials", ("testimonial", "reviews", "metrics", "stats", "social proof")),
        ("FAQ before final CTA", ("faq", "questions", "accordion")),
        ("contact lead form", ("contact form", "lead form", "inquiry", "request")),
    ],
    "implementation": [
        ("React + Vite component build", ("react", "vite", "typescript", "tsx")),
        ("Tailwind utility styling", ("tailwind", "utility")),
        ("CSS variables and responsive constraints", ("css variables", "clamp", "responsive", "mobile")),
        ("GSAP/Framer motion layer", ("gsap", "framer", "motion")),
        ("Three.js/WebGL scene", ("three.js", "webgl", "react three fiber", "r3f")),
        ("accessible semantic HTML", ("aria", "semantic", "keyboard", "screen reader")),
        ("asset-first build plan", ("assets", "images", "video", "media", "photo")),
        ("browser verification required", ("playwright", "screenshot", "console", "verify")),
    ],
}

ROLE_TERMS: dict[str, set[str]] = {
    "market fit": {
        "agency",
        "ai",
        "beauty",
        "botanical",
        "commerce",
        "ecommerce",
        "finance",
        "portfolio",
        "product",
        "saas",
        "security",
        "shop",
        "travel",
        "wellness",
    },
    "visual engine": {
        "3d",
        "cinematic",
        "depth",
        "editorial",
        "fullscreen",
        "glass",
        "image",
        "motion",
        "parallax",
        "product",
        "video",
        "webgl",
    },
    "information architecture": {
        "about",
        "benefits",
        "case",
        "features",
        "process",
        "sections",
        "services",
        "story",
        "tabs",
        "why",
    },
    "conversion pattern": {
        "booking",
        "cart",
        "checkout",
        "contact",
        "cta",
        "demo",
        "faq",
        "form",
        "pricing",
        "signup",
        "waitlist",
    },
    "motion system": {
        "animation",
        "cursor",
        "framer",
        "gsap",
        "hover",
        "parallax",
        "reveal",
        "scroll",
        "transition",
    },
    "restraint counterweight": {
        "clean",
        "editorial",
        "minimal",
        "simple",
        "subtle",
        "white",
    },
}

ROLE_ORDER = [
    "market fit",
    "visual engine",
    "information architecture",
    "conversion pattern",
    "motion system",
    "restraint counterweight",
]


@dataclass
class PromptEntry:
    index: int
    id: str
    title: str
    category: str
    page_type: str
    status: str
    prompt_text: str
    metadata_text: str
    prompt_length: int
    prompt_sha256: str

    @property
    def title_tokens(self) -> set[str]:
        return tokens(f"{self.title} {self.category} {self.page_type} {self.id}")

    @property
    def body_tokens(self) -> set[str]:
        return tokens(self.prompt_text)

    @property
    def surface_text(self) -> str:
        return f"{self.title} {self.category} {self.page_type} {self.metadata_text}"

    @property
    def surface_tokens(self) -> set[str]:
        return tokens(self.surface_text)

    @property
    def searchable(self) -> str:
        return f"{self.title} {self.category} {self.page_type} {self.metadata_text} {self.prompt_text}"


def tokens(text: str) -> set[str]:
    return {token for token in TOKEN_RE.findall(text.lower()) if token not in STOP_WORDS}


def phrase_count(text: str, phrases: Iterable[str]) -> int:
    text_lower = text.lower()
    return sum(text_lower.count(phrase) for phrase in phrases if phrase in text_lower)


def load_entries(path: Path) -> list[PromptEntry]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries: list[PromptEntry] = []
    for index, item in enumerate(data.get("prompts", [])):
        metadata = item.get("metadata") or {}
        title = str(item.get("title") or metadata.get("title") or item.get("id") or f"Prompt {index + 1}")
        category = str(metadata.get("category") or metadata.get("type") or item.get("ui_category") or "Prompt")
        page_type = str(metadata.get("page_type") or metadata.get("type") or "")
        prompt_text = str(item.get("prompt_text") or "")
        metadata_text = " ".join(
            str(value)
            for value in [
                item.get("id"),
                item.get("ui_title"),
                item.get("ui_category"),
                metadata.get("category"),
                metadata.get("type"),
                metadata.get("page_type"),
                " ".join(metadata.get("types") or []),
            ]
            if value
        )
        entries.append(
            PromptEntry(
                index=index,
                id=str(item.get("id") or metadata.get("id") or ""),
                title=title,
                category=category,
                page_type=page_type,
                status=str(item.get("fetch_status") or ""),
                prompt_text=prompt_text,
                metadata_text=metadata_text,
                prompt_length=int(item.get("prompt_length") or len(prompt_text)),
                prompt_sha256=str(item.get("prompt_sha256") or ""),
            )
        )
    return entries


def detect_signals(text: str) -> dict[str, Counter[str]]:
    found: dict[str, Counter[str]] = {}
    text_lower = text.lower()
    for group, rules in SIGNALS.items():
        counter: Counter[str] = Counter()
        for label, phrases in rules:
            hits = phrase_count(text_lower, phrases)
            if hits:
                counter[label] = hits
        found[group] = counter
    return found


def score_entry(entry: PromptEntry, brief: str, brief_tokens: set[str]) -> int:
    title_hits = brief_tokens & entry.title_tokens
    body_hits = brief_tokens & entry.body_tokens
    score = len(title_hits) * 16 + len(body_hits) * 2

    searchable = entry.searchable.lower()
    for token in brief_tokens:
        if len(token) >= 4 and token in entry.title.lower():
            score += 10
        elif len(token) >= 4 and token in entry.metadata_text.lower():
            score += 6
        elif len(token) >= 4 and token in searchable:
            score += 1

    # Exact brief phrases matter for industries like "hair oil" or "AI automation".
    words = [word for word in TOKEN_RE.findall(brief.lower()) if word not in STOP_WORDS]
    for size in (2, 3):
        for start in range(0, max(0, len(words) - size + 1)):
            phrase = " ".join(words[start : start + size])
            if phrase in searchable:
                score += 12 if phrase in entry.title.lower() or phrase in entry.metadata_text.lower() else 5

    if entry.prompt_text:
        score += min(entry.prompt_length // 4000, 6)
    if entry.status == "paid_only":
        score -= 25
    return score


def role_score(entry: PromptEntry, role: str, signals: dict[str, Counter[str]], base_score: int) -> int:
    surface_tokens = entry.surface_tokens
    body_tokens = entry.body_tokens
    terms = ROLE_TERMS[role]
    surface = entry.surface_text.lower()
    score = min(base_score, 120)
    score += len(surface_tokens & terms) * 22
    score += len(body_tokens & terms) * 2

    if role == "visual engine":
        score += min(sum(signals["visual"].values()), 16) * 6
        score += min(sum(signals["motion"].values()), 12) * 2
        score += phrase_count(surface, ("3d", "cinematic", "interactive", "motion", "product", "video")) * 16
    elif role == "information architecture":
        score += min(sum(signals["layout"].values()), 14) * 6
        score += len(surface_tokens & {"about", "features", "process", "services", "website", "landing"}) * 12
    elif role == "conversion pattern":
        score += min(sum(signals["conversion"].values()), 14) * 7
        score += phrase_count(
            surface,
            ("ecommerce", "shop", "pricing", "signup", "waitlist", "booking", "contact", "form", "cta"),
        ) * 24
    elif role == "motion system":
        score += min(sum(signals["motion"].values()), 14) * 9
        score += phrase_count(surface, ("motion", "animation", "cinematic", "3d", "interactive", "scroll")) * 18
    elif role == "restraint counterweight":
        score += phrase_count(surface, ("minimal", "clean", "simple", "subtle", "white", "editorial")) * 26
        score += phrase_count(surface, ("minimal", "workflow", "saas", "utility")) * 18
        restraint_body_hits = phrase_count(entry.prompt_text, ("minimal", "clean", "simple", "subtle", "white", "editorial"))
        score += min(restraint_body_hits, 8) * 3
        score -= phrase_count(entry.searchable, ("neon", "maximal", "chaotic", "cyberpunk")) * 8
    elif role == "market fit":
        score += len(surface_tokens & terms) * 12
        score += phrase_count(surface, ("botanical", "beauty", "ecommerce", "saas", "agency", "security", "portfolio")) * 18
    return score


def pick_source_mix(
    scored: list[tuple[int, PromptEntry, dict[str, Counter[str]]]],
    brief_tokens: set[str],
) -> list[tuple[str, int, PromptEntry, dict[str, Counter[str]]]]:
    selected: list[tuple[str, int, PromptEntry, dict[str, Counter[str]]]] = []
    used: set[int] = set()
    pool = scored[:48]
    top_score = pool[0][0] if pool else 0
    relevance_floor = max(10, int(top_score * 0.18))
    explicit_motion_or_visual = bool(
        brief_tokens
        & {
            "3d",
            "animation",
            "cinematic",
            "interactive",
            "motion",
            "parallax",
            "scroll",
            "video",
            "webgl",
        }
    )
    for role in ROLE_ORDER:
        best: tuple[int, PromptEntry, dict[str, Counter[str]]] | None = None
        role_pool = pool
        if not (explicit_motion_or_visual and role in {"visual engine", "motion system"}):
            role_pool = [item for item in pool if item[0] >= relevance_floor] or pool[:12]

        for base_score, entry, signals in role_pool:
            if entry.index in used:
                continue
            current = role_score(entry, role, signals, base_score)
            if best is None or current > best[0]:
                best = (current, entry, signals)
        if best:
            score, entry, signals = best
            selected.append((role, score, entry, signals))
            used.add(entry.index)
    return selected


def top_atoms(selected: list[tuple[str, int, PromptEntry, dict[str, Counter[str]]]]) -> dict[str, list[str]]:
    merged: dict[str, Counter[str]] = defaultdict(Counter)
    for _role, _score, _entry, signals in selected:
        for group, counter in signals.items():
            merged[group].update(counter)

    atoms: dict[str, list[str]] = {}
    for group in ("layout", "visual", "motion", "conversion", "implementation"):
        labels = [label for label, _count in merged[group].most_common(6)]
        atoms[group] = labels
    return atoms


def fallback_atoms(atoms: dict[str, list[str]]) -> dict[str, list[str]]:
    defaults = {
        "layout": ["hero with proof and primary CTA", "section sequence with clear jobs"],
        "visual": ["one dominant media idea", "balanced neutral palette with one accent"],
        "motion": ["scroll-triggered reveal pacing", "reduced-motion fallback"],
        "conversion": ["clear primary CTA above the fold", "FAQ before final CTA"],
        "implementation": ["CSS variables and responsive constraints", "browser verification required"],
    }
    for group, default_values in defaults.items():
        if not atoms.get(group):
            atoms[group] = default_values
    return atoms


def compact_source_id(entry: PromptEntry) -> str:
    if entry.prompt_sha256:
        return entry.prompt_sha256[:10]
    return entry.id or str(entry.index + 1)


def render_markdown(
    brief: str,
    entries: list[PromptEntry],
    selected: list[tuple[str, int, PromptEntry, dict[str, Counter[str]]]],
    atoms: dict[str, list[str]],
) -> str:
    body_count = sum(1 for entry in entries if entry.prompt_text)
    lines = [
        "# Lumora Deep Source Pack",
        "",
        f"Brief: {brief}",
        f"Library: {len(entries)} prompts, {body_count} with prompt bodies.",
        "",
        "## Selected Source Mix",
    ]
    for role, score, entry, signals in selected:
        detected = []
        for group in ("layout", "visual", "motion", "conversion"):
            detected.extend(label for label, _count in signals[group].most_common(2))
        detected_text = ", ".join(dict.fromkeys(detected[:5])) or "general design guidance"
        lines.extend(
            [
                f"- {role.title()}: {entry.title} ({entry.category})",
                f"  - Use for: {detected_text}.",
                f"  - Match score: {score}; source id: {compact_source_id(entry)}; body length: {entry.prompt_length}.",
            ]
        )

    lines.extend(["", "## Merged Prompt Atoms"])
    for group in ("layout", "visual", "motion", "conversion", "implementation"):
        lines.append(f"- {group.title()}: " + "; ".join(atoms[group]))

    lines.extend(
        [
            "",
            "## Build Brief Template",
            "- Concept: write one sentence that makes the site feel like a product experience, not an aesthetic label.",
            "- Hero: combine the strongest market-fit source with one visual-engine atom; include proof and one primary CTA.",
            "- Sections: assign every major section a job: explain mechanism, show proof, compare options, handle objections, or convert.",
            "- Assets: choose or generate media before polishing layout when credibility depends on product/place/person imagery.",
            "- Motion: use the selected motion atoms to clarify hierarchy or product behavior; avoid ambient motion that competes with reading.",
            "- Conversion: wire the selected conversion pattern into functional controls, form states, or ecommerce/package states.",
            "- Responsive: specify hero crop, navigation behavior, touch targets, and text wrap limits before final CSS.",
            "- Verification: capture desktop and mobile screenshots, inspect console errors, and revise visible issues before final response.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_json(
    brief: str,
    entries: list[PromptEntry],
    selected: list[tuple[str, int, PromptEntry, dict[str, Counter[str]]]],
    atoms: dict[str, list[str]],
) -> str:
    body_count = sum(1 for entry in entries if entry.prompt_text)
    payload = {
        "brief": brief,
        "library": {"prompts": len(entries), "with_prompt_bodies": body_count},
        "selected_source_mix": [
            {
                "role": role,
                "title": entry.title,
                "category": entry.category,
                "page_type": entry.page_type,
                "score": score,
                "source_id": compact_source_id(entry),
                "prompt_length": entry.prompt_length,
                "atoms": {
                    group: [label for label, _count in signals[group].most_common(4)]
                    for group in ("layout", "visual", "motion", "conversion", "implementation")
                },
            }
            for role, score, entry, signals in selected
        ],
        "merged_prompt_atoms": atoms,
    }
    return json.dumps(payload, indent=2)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compose a Lumora source pack from the bundled prompt library.")
    parser.add_argument("brief", nargs="+", help="Company or website brief.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--limit", type=int, default=48, help="Number of ranked entries to keep before role selection.")
    args = parser.parse_args()

    brief = " ".join(args.brief).strip()
    root = Path(__file__).resolve().parents[1]
    library_path = root / "references" / "motionsites-prompt-library.json"
    if not library_path.exists():
        raise SystemExit(f"Missing prompt library: {library_path}")

    entries = load_entries(library_path)
    brief_tokens = tokens(brief)
    scored = []
    for entry in entries:
        signals = detect_signals(entry.searchable)
        score = score_entry(entry, brief, brief_tokens)
        if score > 0:
            scored.append((score, entry, signals))

    if not scored:
        scored = [(1, entry, detect_signals(entry.searchable)) for entry in entries if entry.prompt_text]

    scored.sort(key=lambda item: (-item[0], item[1].title.lower()))
    scored = scored[: max(args.limit, 24)]
    selected = pick_source_mix(scored, brief_tokens)
    atoms = fallback_atoms(top_atoms(selected))

    if args.format == "json":
        print(render_json(brief, entries, selected, atoms))
    else:
        print(render_markdown(brief, entries, selected, atoms))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
