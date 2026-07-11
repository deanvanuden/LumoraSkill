#!/usr/bin/env python3
"""Build Lumora's searchable design-DNA index from every source prompt."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIBRARY = ROOT / "references" / "motionsites-prompt-library.json"
DEFAULT_OUTPUT = ROOT / "references" / "design-dna-index.json"


TAXONOMY: dict[str, dict[str, tuple[str, ...]]] = {
    "roles": {
        "complete-page": (r"\blanding\s+page\b", r"\bfull(?:-|\s)?page\b", r"\bwebsite\b", r"\bsingle-page\b"),
        "navigation": (r"\bnav(?:bar|igation)?\b", r"\bmega\s+menu\b"),
        "hero": (r"\bhero\b", r"\babove[- ]the[- ]fold\b", r"\bfirst\s+viewport\b"),
        "features": (r"\bfeatures?\b", r"\bbenefits?\b", r"\bcapabilit(?:y|ies)\b", r"\bwhy\s+us\b"),
        "story-about": (r"\babout\b", r"\bour\s+story\b", r"\bmanifesto\b", r"\bmission\b"),
        "services": (r"\bservices?\b", r"\bofferings?\b"),
        "portfolio-gallery": (r"\bportfolio\b", r"\bcase\s+stud(?:y|ies)\b", r"\bprojects?\b", r"\bgallery\b"),
        "product-commerce": (r"\be-?commerce\b", r"\bproducts?\b", r"\bshop\b", r"\bcart\b", r"\bcheckout\b", r"\bcollection\b"),
        "process": (r"\bprocess\b", r"\bworkflow\b", r"\bhow\s+it\s+works\b", r"\bsteps?\b"),
        "proof": (r"\btestimonials?\b", r"\breviews?\b", r"\bsocial\s+proof\b", r"\bmetrics?\b", r"\bstats?\b"),
        "pricing": (r"\bpricing\b", r"\bprice\s+plans?\b", r"\bsubscriptions?\b"),
        "faq": (r"\bfaq\b", r"frequently\s+asked"),
        "contact-booking": (r"\bcontact\b", r"\bbooking\b", r"\bappointment\b", r"\binquiry\b"),
        "cta": (r"\bcta\b", r"call[- ]to[- ]action", r"\bget\s+started\b"),
        "footer": (r"\bfooter\b",),
        "dashboard-app": (r"\bdashboard\b", r"\bapp\s+(?:ui|interface)\b", r"\badmin\s+panel\b"),
        "form-auth": (r"\bsign[ -]?in\b", r"\bsign[ -]?up\b", r"\bwaitlist\b", r"\bform\b"),
    },
    "styles": {
        "editorial": (r"\beditorial\b", r"\bmagazine\b"),
        "cinematic": (r"\bcinematic\b", r"\bfilm(?:ic)?\b"),
        "luxury": (r"\bluxury\b", r"\bpremium\b", r"\bhigh[- ]end\b"),
        "minimal": (r"\bminimal(?:ist|ism)?\b", r"\bclean\s+design\b"),
        "brutalist": (r"\bbrutalist\b", r"\bneo[- ]brutal"),
        "swiss": (r"\bswiss\b", r"\binternational\s+typographic\b"),
        "organic-botanical": (r"\bbotanical\b", r"\borganic\b", r"\bnatural\s+texture\b"),
        "industrial": (r"\bindustrial\b", r"\bmechanical\b"),
        "playful": (r"\bplayful\b", r"\bwhimsical\b"),
        "futuristic": (r"\bfuturistic\b", r"\bsci[- ]fi\b", r"\bcyber"),
        "retro": (r"\bretro\b", r"\bvintage\b", r"\bnostalg"),
        "glass": (r"\bglassmorphism\b", r"\bliquid\s+glass\b", r"\bfrosted\s+glass\b"),
        "monochrome": (r"\bmonochrome\b", r"\bblack\s+and\s+white\b"),
        "dark": (r"\bdark\s+(?:theme|mode|background)\b", r"\boled\b"),
        "light": (r"\blight\s+(?:theme|mode|background)\b", r"\boff[- ]white\b"),
        "colorful": (r"\bcolorful\b", r"\bvibrant\b", r"\bmulticolor"),
        "tactile": (r"\btactile\b", r"\bpaper\s+texture\b", r"\bgrain\b", r"\bmateriality\b"),
        "spatial-3d": (r"\bspatial\b", r"\b3d\b", r"\bdepth\b"),
        "typography-led": (r"\btypography[- ]led\b", r"\bkinetic\s+typography\b", r"\btype[- ]driven\b"),
        "image-led": (r"\bimage[- ]led\b", r"\bimage[- ]first\b", r"\bfull[- ]bleed\s+(?:image|photo)\b"),
    },
    "layouts": {
        "full-bleed": (r"\bfull[- ]bleed\b", r"\bfull[- ]screen\b", r"\bfullscreen\b"),
        "split-screen": (r"\bsplit[- ]screen\b", r"\btwo[- ]column\s+hero\b", r"\b50\s*/\s*50\b"),
        "asymmetric": (r"\basymmetr", r"\boff[- ]grid\b", r"\boffset\s+(?:layout|composition)\b"),
        "centered-stage": (r"\bcentered\s+(?:hero|layout|content)\b", r"\btext-align:\s*center\b"),
        "bento": (r"\bbento\b", r"\bgrid-flow-dense\b"),
        "masonry": (r"\bmasonry\b",),
        "horizontal-scroll": (r"\bhorizontal\s+scroll\b", r"\boverflow-x:\s*(?:auto|scroll)\b"),
        "pinned-sticky": (r"\bpin(?:ned|ning)?\b", r"\bsticky\b", r"position:\s*sticky"),
        "stacked": (r"\bstack(?:ed|ing)\s+(?:cards?|panels?|sections?)\b", r"\bcard\s+stack\b"),
        "layered-overlap": (r"\boverlap", r"\blayered\s+(?:cards?|images?|panels?)\b", r"\bz-axis\b"),
        "accordion-slices": (r"\baccordion\b", r"\bexpand(?:ing|able)\s+slices?\b"),
        "carousel": (r"\bcarousel\b", r"\bcoverflow\b", r"\bslider\b"),
        "tabs": (r"\btabs?\b", r"\btablist\b"),
        "timeline": (r"\btimeline\b", r"\bjourney\s+line\b"),
        "collage": (r"\bcollage\b", r"\bpolaroid\b", r"\bimage\s+scatter\b"),
        "radial-circular": (r"\bradial\s+(?:menu|layout|gallery)\b", r"\bcircular\s+(?:layout|menu|text)\b", r"\bcylinder\b"),
        "editorial-columns": (r"\beditorial\s+(?:grid|columns?|layout)\b", r"\bmulti[- ]column\s+layout\b"),
        "scrollytelling": (r"\bscroll(?:y|-)telling\b", r"\bscroll[- ]driven\s+(?:story|narrative|experience)\b"),
        "single-screen": (r"\bsingle[- ]screen\b", r"overflow:\s*hidden.*(?:body|html)", r"no\s+native\s+(?:browser\s+)?scroll"),
    },
    "motion": {
        "scroll-trigger": (r"\bscrolltrigger\b", r"\bscroll[- ]triggered\b", r"whileinview"),
        "scroll-scrub": (r"\bscrub\b", r"\bscrollprogress\b", r"scroll[- ]linked"),
        "pinned-scroll": (r"\bpin(?:ned|ning)?\b", r"position:\s*sticky"),
        "parallax": (r"\bparallax\b",),
        "mask-reveal": (r"\bmask(?:ed)?\s+reveal\b", r"\bclip-path\b", r"\bcurtain\s+reveal\b"),
        "split-text": (r"\bsplittext\b", r"\bchar(?:acter)?[- ]level\b", r"\bword[- ]by[- ]word\b"),
        "text-scramble": (r"\btext\s+scramble\b", r"\bdecode\s+(?:text|effect)\b"),
        "marquee": (r"\bmarquee\b", r"\binfinite\s+(?:ticker|text\s+loop)\b"),
        "magnetic": (r"\bmagnetic\b", r"\bpull\s+toward\s+the\s+cursor\b"),
        "tilt-depth": (r"\btilt\b", r"rotate[XY]\(", r"\b3d\s+hover\b"),
        "hover-reveal": (r"\bhover\s+(?:reveal|expand|preview|image)\b", r"group-hover"),
        "page-transition": (r"\bpage\s+transition\b", r"\broute\s+transition\b", r"\btransition\s+overlay\b"),
        "morph": (r"\bmorph(?:ing)?\b", r"\bflips?\b", r"layoutId"),
        "liquid": (r"\bliquid\b", r"\bgooey\b", r"\bviscous\b"),
        "video-scrub": (r"\bvideo\s+scrub", r"currentTime.*scroll", r"\bframe\s+scrub"),
        "image-sequence": (r"\bimage\s+sequence\b", r"\bframe[- ]by[- ]frame\b"),
        "drag-gesture": (r"\bdrag(?:gable|ging)?\b", r"\bgesture\b", r"\bwheel/touch\b"),
        "cursor-follow": (r"\bcursor[- ]follow", r"\bmouse[- ]follow", r"\bhover\s+trail\b"),
        "count-up": (r"\bcount[- ]?up\b", r"\banimated\s+(?:number|counter)\b"),
        "stagger": (r"\bstagger", r"animation-delay:\s*calc"),
        "autoplay-loop": (r"\bautoplay\b", r"repeat:\s*-1", r"\binfinite\s+loop\b"),
        "theme-transition": (r"\btheme\s+toggle\b", r"\bdark/light\b", r"\bday/night\b"),
        "glitch": (r"\bglitch\b", r"\brgb[- ]split\b"),
        "particles": (r"\bparticles?\b", r"\bpoint\s+cloud\b"),
    },
    "media": {
        "background-video": (r"\bbackground\s+videos?\b", r"<video[^>]+(?:fixed|background)", r"\bfullscreen\s+video\b"),
        "video": (r"\bvideo\b", r"\.mp4\b", r"\.webm\b", r"\.m3u8\b"),
        "photography": (r"\bphotograph", r"\bphoto\b", r"\bportrait\b"),
        "product-render": (r"\bproduct\s+render\b", r"\bpackshot\b", r"\bproduct\s+image\b"),
        "gallery": (r"\bgallery\b", r"\bimage\s+grid\b", r"\blookbook\b"),
        "ui-screens": (r"\bui\s+(?:screens?|mockups?|previews?)\b", r"\bdashboard\s+(?:image|preview|mockup)\b"),
        "3d-model": (r"\bgltf\b", r"\bglb\b", r"\b3d\s+model\b"),
        "canvas-webgl": (r"\bwebgl\b", r"<canvas", r"\bthree\.js\b", r"\breact[- ]three[- ]fiber\b"),
        "image-sequence": (r"\bimage\s+sequence\b", r"\bframe[- ]by[- ]frame\b"),
        "svg": (r"\bsvg\b", r"<svg"),
        "map": (r"\bmapbox\b", r"\bgoogle\s+maps?\b", r"\bmap\s+(?:section|embed|canvas)\b"),
        "audio": (r"\baudio\b", r"\bsound\b"),
        "logos-icons": (r"\blogo\s+(?:row|strip|wall|cloud)\b", r"\bicon\s+(?:library|set)\b"),
    },
    "interactions": {
        "mobile-menu": (r"\bmobile\s+(?:menu|drawer|nav)\b", r"\bhamburger\b"),
        "mega-menu": (r"\bmega\s+menu\b",),
        "tabs": (r"\btablist\b", r"\bactive\s+tab\b", r"\btab\s+button\b"),
        "accordion": (r"\baccordion\b", r"aria-expanded"),
        "carousel": (r"\bcarousel\b", r"\bslider\b", r"\bnext/previous\b"),
        "drag": (r"\bdraggable\b", r"\bdrag\s+to\b", r"\bswipe\b"),
        "theme-toggle": (r"\btheme\s+toggle\b", r"\bdark\s+mode\s+toggle\b", r"\bday/night\b"),
        "selector": (r"\bselector\b", r"\bsegmented\s+control\b", r"\bvariant\s+picker\b"),
        "form": (r"<form\b", r"\bform\s+validation\b", r"\bemail\s+input\b"),
        "commerce": (r"\badd\s+to\s+cart\b", r"\bcheckout\b", r"\bquantity\s+(?:stepper|selector)\b"),
        "hover": (r"\bon\s+hover\b", r":hover\b", r"\bhover\s+state\b"),
        "mouse-follow": (r"\bmouse[- ]follow", r"\bcursor[- ]follow", r"pointermove"),
        "filter": (r"\bfilter\s+(?:buttons?|tabs?|chips?)\b", r"\bcategory\s+filter\b"),
        "modal-overlay": (r"\bmodal\b", r"\bdialog\b", r"\boverlay\s+menu\b"),
        "scroll-progress": (r"\bscroll\s+progress\b", r"\bprogress\s+indicator\b"),
    },
    "stack": {
        "vite": (r"\bvite\b",),
        "react": (r"\breact\b", r"\.tsx\b", r"useState\("),
        "typescript": (r"\btypescript\b", r"\.tsx\b"),
        "tailwind": (r"\btailwind",),
        "vanilla-css": (r"\bvanilla\s+css\b", r"\bcustom\s+css\b", r"index\.css"),
        "gsap": (r"\bgsap\b",),
        "scrolltrigger": (r"\bscrolltrigger\b",),
        "framer-motion": (r"\bframer[- ]motion\b", r"from\s+[\"']motion[\"']"),
        "threejs": (r"\bthree\.js\b", r"from\s+[\"']three[\"']"),
        "react-three-fiber": (r"\breact[- ]three[- ]fiber\b", r"@react-three/fiber"),
        "lenis": (r"\blenis\b",),
        "swiper": (r"\bswiper\b",),
        "lucide": (r"\blucide",),
        "phosphor": (r"\bphosphor",),
        "material-icons": (r"\bmaterial\s+(?:symbols|icons)\b",),
    },
    "constraints": {
        "scroll-lock": (r"overflow:\s*hidden", r"no\s+native\s+(?:browser\s+)?scroll", r"\bscroll\s+hijack"),
        "fixed-scene": (r"position:\s*fixed", r"\bfixed\s+inset\b"),
        "requires-video": (r"\bvideo\b", r"\.mp4\b", r"\.webm\b", r"\.m3u8\b"),
        "requires-webgl": (r"\bwebgl\b", r"\bthree\.js\b", r"@react-three/fiber"),
        "external-media": (r"https?://",),
        "responsive-specified": (r"\bresponsive\b", r"\bmobile\b", r"@media", r"\bbreakpoint\b"),
        "reduced-motion-specified": (r"prefers-reduced-motion", r"\breduced\s+motion\b"),
    },
}


def compile_taxonomy() -> dict[str, dict[str, tuple[re.Pattern[str], ...]]]:
    return {
        group: {
            tag: tuple(re.compile(pattern, re.IGNORECASE | re.MULTILINE) for pattern in patterns)
            for tag, patterns in tags.items()
        }
        for group, tags in TAXONOMY.items()
    }


COMPILED = compile_taxonomy()


def normalized_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def matching_tags(text: str, group: str) -> list[str]:
    return [tag for tag, patterns in COMPILED[group].items() if any(pattern.search(text) for pattern in patterns)]


def evidence_snippet(text: str, patterns: Iterable[re.Pattern[str]]) -> str | None:
    match = next((candidate for pattern in patterns if (candidate := pattern.search(text))), None)
    if match is None:
        return None
    start = max(0, match.start() - 140)
    end = min(len(text), match.end() + 260)
    return normalized_space(text[start:end])[:520]


def extract_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip().strip("#").strip()
        is_markdown = bool(re.match(r"^#{1,5}\s+\S", line.strip()))
        is_label = bool(stripped.endswith(":") and 2 <= len(stripped.split()) <= 9 and stripped.upper() == stripped)
        if not (is_markdown or is_label):
            continue
        clean = normalized_space(stripped.rstrip(":"))
        if clean and clean not in headings:
            headings.append(clean[:140])
        if len(headings) >= 30:
            break
    return headings


def family_for(prompt_id: str, prefix_counts: Counter[str]) -> str:
    prefix = prompt_id.split("-", 1)[0]
    return prefix if prefix_counts[prefix] > 1 else prompt_id


def static_portability(dna: dict[str, list[str]]) -> str:
    stack = set(dna["stack"])
    constraints = set(dna["constraints"])
    motion = set(dna["motion"])
    if stack.intersection({"threejs", "react-three-fiber"}) or constraints.intersection({"requires-webgl", "scroll-lock"}) or "video-scrub" in motion:
        return "complex-adaptation"
    if stack.intersection({"vite", "react", "tailwind", "framer-motion", "gsap"}):
        return "static-translation"
    return "direct-static"


def complexity_for(prompt_text: str, dna: dict[str, list[str]]) -> str:
    signal_count = sum(len(values) for values in dna.values())
    if len(prompt_text) > 20000 or signal_count >= 38 or dna["constraints"] and "requires-webgl" in dna["constraints"]:
        return "high"
    if len(prompt_text) > 9000 or signal_count >= 22:
        return "medium"
    return "low"


def build_index(library_path: Path) -> dict[str, Any]:
    raw = library_path.read_bytes()
    library = json.loads(raw.decode("utf-8"))
    prompts = library.get("prompts") or []
    prefix_counts = Counter(str(item.get("id", "")).split("-", 1)[0] for item in prompts if item.get("id"))
    records: list[dict[str, Any]] = []
    frequencies: dict[str, Counter[str]] = {group: Counter() for group in TAXONOMY}

    for item in prompts:
        metadata = item.get("metadata") or {}
        prompt_text = item.get("prompt_text") if isinstance(item.get("prompt_text"), str) else ""
        prompt_id = str(item.get("id") or metadata.get("id") or "")
        title = str(item.get("title") or item.get("ui_title") or metadata.get("title") or prompt_id)
        category = str(item.get("ui_category") or metadata.get("category") or "")
        metadata_text = " ".join(
            str(value or "")
            for value in (
                prompt_id,
                title,
                category,
                metadata.get("type"),
                metadata.get("page_type"),
                metadata.get("types"),
            )
        )
        searchable = f"{metadata_text}\n{prompt_text}"
        dna = {group: matching_tags(searchable, group) if prompt_text else [] for group in TAXONOMY}
        for group, tags in dna.items():
            frequencies[group].update(tags)

        evidence: dict[str, dict[str, str]] = {}
        if prompt_text:
            for group in ("roles", "styles", "layouts", "motion", "media", "interactions"):
                group_evidence: dict[str, str] = {}
                for tag in dna[group]:
                    snippet = evidence_snippet(prompt_text, COMPILED[group][tag])
                    if snippet:
                        group_evidence[tag] = snippet
                if group_evidence:
                    evidence[group] = group_evidence

        records.append(
            {
                "id": prompt_id,
                "title": title,
                "category": category,
                "family": family_for(prompt_id, prefix_counts),
                "available": bool(prompt_text),
                "fetch_status": item.get("fetch_status"),
                "prompt_length": len(prompt_text),
                "prompt_sha256": item.get("prompt_sha256") or (hashlib.sha256(prompt_text.encode("utf-8")).hexdigest() if prompt_text else None),
                "metadata": {
                    "type": metadata.get("type"),
                    "types": metadata.get("types"),
                    "page_type": metadata.get("page_type"),
                    "is_free": metadata.get("is_free"),
                },
                "preview": {
                    "image": metadata.get("image_preview_url"),
                    "video": metadata.get("video_preview_url"),
                },
                "dna": dna,
                "headings": extract_headings(prompt_text),
                "evidence": evidence,
                "complexity": complexity_for(prompt_text, dna),
                "static_portability": static_portability(dna),
            }
        )

    return {
        "schema": "lumora.design_dna_index.v2",
        "source": {
            "path": "references/motionsites-prompt-library.json",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "generated_at": library.get("generated_at"),
        },
        "counts": {
            "total": len(records),
            "available": sum(1 for record in records if record["available"]),
            "unavailable": sum(1 for record in records if not record["available"]),
        },
        "prompt_bodies_omitted": True,
        "tag_frequency": {
            group: dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))
            for group, counter in frequencies.items()
        },
        "prompts": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    payload = build_index(args.library.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(
        f"Indexed {payload['counts']['available']}/{payload['counts']['total']} prompts "
        f"to {args.output.resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
