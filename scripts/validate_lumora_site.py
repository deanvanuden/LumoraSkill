#!/usr/bin/env python3
"""Validate Lumora planning evidence, source traceability, motion risk, and GitHub Pages delivery."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SOURCE_LIBRARY = ROOT / "references" / "motionsites-prompt-library.json"
PLACEHOLDER_HOSTS = ("picsum.photos", "unsplash.com", "images.unsplash.com", "placehold.co", "placeholder.com", "dummyimage.com")
GENERIC_COPY = (
    r"\belevate\b", r"\bunleash\b", r"\brevolutioni[sz]e\b", r"\bnext[- ]gen\b",
    r"\bseamless(?:ly)?\b", r"\btransformative\b", r"\bcutting[- ]edge\b", r"\bfuture[- ]proof\b",
)
URL_ATTRS = {
    "a": ("href",),
    "link": ("href",),
    "script": ("src",),
    "img": ("src", "srcset"),
    "source": ("src", "srcset"),
    "video": ("src", "poster"),
    "audio": ("src",),
    "iframe": ("src",),
}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    file: str
    line: int
    message: str


class AuditParser(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids: set[str] = set()
        self.urls: list[tuple[str, str, str, int]] = []
        self.images: list[tuple[dict[str, str], int]] = []
        self.videos: list[tuple[dict[str, str], int]] = []
        self.forms: list[tuple[dict[str, str], int]] = []
        self.sections: list[tuple[dict[str, str], int]] = []
        self.buttons: list[dict[str, Any]] = []
        self._button_stack: list[int] = []
        self.visible_text: list[str] = []
        self._ignored_depth = 0
        self.html_lang = ""
        self.has_viewport = False
        self.has_description = False
        self.title_text = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line, _ = self.getpos()
        attr = {name.lower(): value or "" for name, value in attrs}
        tag = tag.lower()
        if tag in {"script", "style", "template"}:
            self._ignored_depth += 1
        if tag == "html":
            self.html_lang = attr.get("lang", "")
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            if attr.get("name", "").lower() == "viewport":
                self.has_viewport = True
            if attr.get("name", "").lower() == "description" and attr.get("content", "").strip():
                self.has_description = True
        element_id = attr.get("id")
        if element_id:
            self.ids.add(element_id)
        for name in URL_ATTRS.get(tag, ()):
            value = attr.get(name)
            if not value:
                continue
            if name == "srcset":
                for candidate in value.split(","):
                    url = candidate.strip().split()[0] if candidate.strip() else ""
                    if url:
                        self.urls.append((tag, name, url, line))
            else:
                self.urls.append((tag, name, value, line))
        if tag == "img":
            self.images.append((attr, line))
        elif tag == "video":
            self.videos.append((attr, line))
        elif tag == "form":
            self.forms.append((attr, line))
        elif tag == "section":
            self.sections.append((attr, line))
        elif tag == "button":
            self.buttons.append({"attrs": attr, "line": line, "text": ""})
            self._button_stack.append(len(self.buttons) - 1)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"script", "style", "template"} and self._ignored_depth:
            self._ignored_depth -= 1
        if tag == "title":
            self._in_title = False
        if tag == "button" and self._button_stack:
            self._button_stack.pop()

    def handle_data(self, data: str) -> None:
        clean = re.sub(r"\s+", " ", data).strip()
        if self._in_title and clean:
            self.title_text = f"{self.title_text} {clean}".strip()
        if not clean or self._ignored_depth:
            return
        self.visible_text.append(clean)
        if self._button_stack:
            index = self._button_stack[-1]
            self.buttons[index]["text"] = f"{self.buttons[index]['text']} {clean}".strip()


class Auditor:
    def __init__(self, site_root: Path, plan_path: Path, strict: bool = False) -> None:
        self.site_root = site_root.resolve()
        self.plan_path = plan_path.resolve()
        self.strict = strict
        self.findings: list[Finding] = []
        self.parsers: dict[Path, AuditParser] = {}
        self.plan: dict[str, Any] = {}
        self.used_source_ids: set[str] = set()
        self.section_sources: dict[str, set[str]] = {}
        self.image_usage: Counter[str] = Counter()

    def add(self, severity: str, code: str, path: Path, message: str, line: int = 0) -> None:
        try:
            display = str(path.resolve().relative_to(self.site_root))
        except (ValueError, FileNotFoundError):
            display = str(path)
        self.findings.append(Finding(severity, code, display.replace("\\", "/"), line, message))

    def error(self, code: str, path: Path, message: str, line: int = 0) -> None:
        self.add("error", code, path, message, line)

    def warning(self, code: str, path: Path, message: str, line: int = 0) -> None:
        self.add("warning", code, path, message, line)

    def parse_html(self, path: Path) -> AuditParser:
        if path not in self.parsers:
            parser = AuditParser(path)
            parser.feed(path.read_text(encoding="utf-8", errors="replace"))
            parser.close()
            self.parsers[path] = parser
        return self.parsers[path]

    @staticmethod
    def filled(value: Any) -> bool:
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, (list, tuple, set, dict)):
            return bool(value)
        return value is not None

    def require_text(self, container: dict[str, Any], key: str, code: str, label: str) -> None:
        if not str(container.get(key) or "").strip():
            self.error(code, self.plan_path, f"fill {label}")

    def check_source_mix(self, schema: str) -> None:
        source_library = json.loads(SOURCE_LIBRARY.read_text(encoding="utf-8"))
        valid_sources = {
            item.get("id"): item.get("prompt_sha256")
            for item in source_library.get("prompts", [])
            if item.get("id") and item.get("prompt_text")
        }
        source_mix = self.plan.get("source_mix") or []
        if schema == "lumora.project_plan.v3" and len(source_mix) < 3:
            self.error("plan.source-count", self.plan_path, "legacy v3 plans require at least three prompt donors")
        if schema == "lumora.project_plan.v4" and not 1 <= len(source_mix) <= 3:
            self.error("plan.source-count", self.plan_path, "v4 requires one anchor and no more than two supporting donors")

        seen_ids: set[str] = set()
        jobs = [source.get("job") for source in source_mix]
        if schema == "lumora.project_plan.v4":
            if jobs.count("anchor") != 1 or (jobs and jobs[0] != "anchor"):
                self.error("plan.anchor", self.plan_path, "source_mix must begin with exactly one anchor donor")
            if any(job not in {"anchor", "experience", "conversion"} for job in jobs):
                self.error("plan.source-job", self.plan_path, "v4 donor jobs are anchor, experience, and conversion")

        for source in source_mix:
            prompt_id = source.get("id")
            if prompt_id in seen_ids:
                self.error("plan.source-duplicate", self.plan_path, f"duplicate prompt donor {prompt_id!r}")
            seen_ids.add(prompt_id)
            if prompt_id not in valid_sources:
                self.error("plan.source-invalid", self.plan_path, f"unknown or unavailable prompt donor {prompt_id!r}")
            elif source.get("prompt_sha256") != valid_sources[prompt_id]:
                self.error("plan.source-hash", self.plan_path, f"source hash does not match the library for {prompt_id!r}")

            contributions = [str(value).strip() for value in source.get("implemented_contributions") or [] if str(value).strip()]
            sections = [str(value).strip() for value in source.get("implemented_sections") or [] if str(value).strip()]
            minimum = 3 if schema == "lumora.project_plan.v4" and source.get("job") == "anchor" else (1 if schema == "lumora.project_plan.v4" else 2)
            if len(contributions) < minimum:
                self.error("plan.source-contributions", self.plan_path, f"{prompt_id!r} needs at least {minimum} concrete implemented contribution(s)")
            minimum_sections = 2 if schema == "lumora.project_plan.v4" and source.get("job") == "anchor" else 1
            if len(sections) < minimum_sections:
                self.error("plan.source-sections", self.plan_path, f"{prompt_id!r} needs at least {minimum_sections} implemented section(s)")
            if schema == "lumora.project_plan.v4" and source.get("job") != "anchor" and len(sections) > 2:
                self.warning("plan.support-scope", self.plan_path, f"supporting donor {prompt_id!r} controls more than two sections; confirm it remains subordinate")
            if schema == "lumora.project_plan.v4":
                authority = source.get("authority")
                if source.get("job") == "anchor" and (not isinstance(authority, (int, float)) or authority < 0.70):
                    self.error("plan.anchor-authority", self.plan_path, "anchor authority must remain at least 0.70")
                if source.get("job") != "anchor" and (not isinstance(authority, (int, float)) or authority > 0.20):
                    self.error("plan.support-authority", self.plan_path, f"supporting donor {prompt_id!r} authority must not exceed 0.20")
                risks = (source.get("compatibility") or {}).get("risks") or []
                if risks and not str(source.get("compatibility_resolution") or "").strip():
                    self.error("plan.compatibility-risk", self.plan_path, f"resolve or reject compatibility risks for {prompt_id!r}")

    def check_v3_plan(self) -> None:
        self.warning("plan.legacy-schema", self.plan_path, "v3 does not enforce Lumora's anchor-led experience and director-review gates; regenerate the plan for new work")
        direction = self.plan.get("creative_direction") or {}
        for key, label in {
            "creative_thesis": "the creative thesis",
            "signature_motif": "the signature motif",
            "company_specificity_test": "the company specificity test",
        }.items():
            self.require_text(direction, key, f"plan.{key}", label)
        if direction.get("status") != "locked":
            self.warning("plan.direction-status", self.plan_path, "set creative_direction.status to 'locked' after the direction is approved")
        self.check_source_mix("lumora.project_plan.v3")
        media = self.plan.get("media_plan") or {}
        if media.get("required_roles") and not media.get("slots"):
            self.error("plan.media-slots", self.plan_path, "define the media slots before delivery")
        motion = self.plan.get("motion_plan") or {}
        self.require_text(motion, "desktop_implementation", "plan.motion-desktop", "the desktop signature-motion implementation")
        self.require_text(motion, "mobile_recomposition", "plan.motion-mobile", "the mobile motion recomposition")

    def check_v4_plan(self) -> None:
        truth = self.plan.get("company_truth") or {}
        if truth.get("status") != "locked":
            self.error("plan.truth-status", self.plan_path, "lock the company-truth inventory before delivery")
        for key in ("name", "offer", "audience", "difference", "place_or_context"):
            self.require_text(truth, key, f"plan.truth-{key}", f"company truth: {key.replace('_', ' ')}")
        for key in ("material_world", "vocabulary", "real_routes", "available_media"):
            if not isinstance(truth.get(key), list):
                self.error(f"plan.truth-{key}", self.plan_path, f"company truth {key.replace('_', ' ')} must be an explicit list, even when empty")
        if not truth.get("material_world"):
            self.error("plan.truth-material-world", self.plan_path, "identify real objects, interfaces, places, rituals, or processes that can become design material")

        exploration = self.plan.get("direction_exploration") or {}
        if exploration.get("status") != "locked":
            self.error("plan.exploration-status", self.plan_path, "lock the three-world direction exploration")
        concepts = exploration.get("concepts") or []
        if len(concepts) < 3:
            self.error("plan.exploration-count", self.plan_path, "write at least three genuinely different company-specific experience worlds")
        concept_ids: set[str] = set()
        concept_fields = ("id", "name", "company_truth", "experience_world", "signature_object", "transformation", "hero_scene", "asset_strategy", "risk", "why_only_this_company")
        for index, concept in enumerate(concepts):
            concept_ids.add(str(concept.get("id") or ""))
            for field in concept_fields:
                if not str(concept.get(field) or "").strip():
                    self.error("plan.exploration-concept", self.plan_path, f"direction concept {index + 1} needs {field.replace('_', ' ')}")
        if len(concept_ids) != len(concepts) or "" in concept_ids:
            self.error("plan.exploration-ids", self.plan_path, "direction concepts need distinct nonempty ids")
        selected_concept = str(exploration.get("selected_concept_id") or "")
        if not selected_concept or selected_concept not in concept_ids:
            self.error("plan.exploration-selection", self.plan_path, "selected_concept_id must identify one of the explored worlds")
        self.require_text(exploration, "selection_reason", "plan.exploration-reason", "the creative director's concept-selection reason")
        if len(exploration.get("rejected_concepts") or []) < 2:
            self.error("plan.exploration-rejections", self.plan_path, "record why at least two alternate worlds were rejected")

        direction = self.plan.get("creative_direction") or {}
        if direction.get("status") != "locked":
            self.error("plan.direction-status", self.plan_path, "lock the selected creative direction before delivery")
        direction_fields = (
            "creative_thesis", "experience_world", "signature_object", "signature_motif", "material_language",
            "spatial_logic", "camera_behavior", "transformation", "emotional_arc", "interaction_thesis",
            "company_specificity_test", "substitution_failure",
        )
        for field in direction_fields:
            self.require_text(direction, field, f"plan.direction-{field}", f"creative direction: {field.replace('_', ' ')}")
        if not direction.get("category_conventions"):
            self.error("plan.category-conventions", self.plan_path, "record the familiar category conventions the direction must move beyond")
        self.require_text(direction, "deliberate_departure", "plan.deliberate-departure", "the truthful departure from category defaults")
        narrative_arc = direction.get("narrative_arc") or {}
        for field in ("entry", "orientation", "deepening", "evidence", "decision", "close"):
            self.require_text(narrative_arc, field, f"plan.narrative-{field}", f"narrative arc: {field}")
        fingerprint = direction.get("design_fingerprint") or {}
        for field in ("composition", "typography", "palette_logic", "material", "media_mode", "shape_language", "section_rhythm", "signature_motion", "structural_motion"):
            self.require_text(fingerprint, field, f"plan.fingerprint-{field}", f"design fingerprint: {field.replace('_', ' ')}")
        keyframes = direction.get("experience_keyframes") or []
        if len(keyframes) < 3:
            self.error("plan.keyframes", self.plan_path, "define entry, signature-state, and decision keyframes")
        for keyframe in keyframes:
            if not str(keyframe.get("description") or "").strip() or not str(keyframe.get("reference_asset") or "").strip():
                self.error("plan.keyframe-detail", self.plan_path, f"keyframe {keyframe.get('id')!r} needs a description and inspected reference asset")

        scorecard = direction.get("originality_scorecard") or []
        total = 0
        if len(scorecard) < 10:
            self.error("plan.originality-count", self.plan_path, "complete all ten originality dimensions")
        for item in scorecard:
            score = item.get("score")
            if not isinstance(score, (int, float)) or score < 1 or score > 2:
                self.error("plan.originality-score", self.plan_path, f"originality dimension {item.get('dimension')!r} must score 1 or 2 after revision")
            else:
                total += score
            if not str(item.get("evidence") or "").strip():
                self.error("plan.originality-evidence", self.plan_path, f"originality dimension {item.get('dimension')!r} needs visible evidence")
        if total < 16:
            self.error("plan.originality-total", self.plan_path, f"originality score is {total}/20; revise directions below 16")

        selection = self.plan.get("source_selection") or {}
        if selection.get("status") != "locked":
            self.error("plan.source-selection-status", self.plan_path, "lock the inspected anchor-led source selection")
        inspected_candidates = set(selection.get("inspected_candidates") or [])
        anchor_shortlist = (selection.get("candidate_shortlists") or {}).get("anchor") or []
        anchor_shortlist_ids = {item.get("id") for item in anchor_shortlist if item.get("id")}
        if len(anchor_shortlist_ids) < 3:
            self.error("plan.anchor-shortlist", self.plan_path, "retain at least three anchor candidates in the plan")
        if len(inspected_candidates.intersection(anchor_shortlist_ids)) < 3:
            self.error("plan.source-inspection", self.plan_path, "inspect at least three anchor candidates before choosing the anchor")
        self.require_text(selection, "compatibility_statement", "plan.source-compatibility", "the donor compatibility statement")
        self.check_source_mix("lumora.project_plan.v4")
        source_mix = self.plan.get("source_mix") or []
        if source_mix and source_mix[0].get("id") not in inspected_candidates:
            self.error("plan.anchor-inspection", self.plan_path, "the selected anchor must appear in inspected_candidates")

        media = self.plan.get("media_plan") or {}
        if media.get("status") != "locked":
            self.error("plan.media-status", self.plan_path, "lock the complete asset campaign before delivery")
        self.require_text(media, "asset_strategy", "plan.asset-strategy", "the site-wide asset strategy")
        signature = media.get("signature_asset") or {}
        if signature.get("status") not in {"ready", "supplied", "generated", "authored"}:
            self.error("plan.signature-asset-status", self.plan_path, "the signature asset must be supplied, generated, authored, or ready")
        for field in ("role", "subject", "medium", "company_reason", "source_or_generation_method"):
            self.require_text(signature, field, f"plan.signature-asset-{field}", f"signature asset: {field.replace('_', ' ')}")
        continuity = media.get("continuity_bible") or {}
        for field in ("subjects", "camera_and_lens", "lighting", "materials", "environment", "palette_and_grade", "texture_and_finish", "crop_behavior", "negative_constraints"):
            self.require_text(continuity, field, f"plan.asset-continuity-{field}", f"asset continuity: {field.replace('_', ' ')}")
        references = media.get("reference_set") or []
        if len(references) < 3:
            self.error("plan.reference-set", self.plan_path, "direct and inspect three connected visual reference states")
        for reference in references:
            if reference.get("status") not in {"selected", "supplied", "approved"}:
                self.error("plan.reference-status", self.plan_path, f"reference {reference.get('id')!r} must be selected, supplied, or approved")
            if reference.get("status") != "supplied" and not str(reference.get("prompt") or "").strip():
                self.error("plan.reference-prompt", self.plan_path, f"generated reference {reference.get('id')!r} needs its generation prompt")
            if not str(reference.get("analysis") or "").strip():
                self.error("plan.reference-detail", self.plan_path, f"reference {reference.get('id')!r} needs a visual analysis")
        slots = media.get("slots") or []
        if not slots:
            self.error("plan.media-slots", self.plan_path, "define every prominent and supporting media slot")
        for slot in slots:
            for field in ("id", "role", "page", "aspect_ratio", "target_render", "focal_point", "source", "truthfulness", "reuse"):
                if not str(slot.get(field) or "").strip():
                    self.error("plan.media-slot-detail", self.plan_path, f"media slot {slot.get('id')!r} needs {field.replace('_', ' ')}")
        self.require_text(media, "asset_coverage_review", "plan.asset-coverage", "the final asset coverage review")

        motion = self.plan.get("motion_plan") or {}
        if motion.get("status") != "locked":
            self.error("plan.motion-status", self.plan_path, "lock the motion storyboard before delivery")
        dominant = motion.get("dominant_interaction") or {}
        for field in ("name", "subject", "input", "transformation", "narrative_purpose", "desktop_implementation", "mobile_recomposition", "reduced_motion"):
            self.require_text(dominant, field, f"plan.motion-{field}", f"dominant interaction: {field.replace('_', ' ')}")
        self.require_text(motion, "structural_language", "plan.motion-structural", "the structural reveal language")
        self.require_text(motion, "dependency_strategy", "plan.motion-dependencies", "the motion dependency and fallback strategy")
        beats = motion.get("choreography_beats") or []
        if len(beats) < 3:
            self.error("plan.motion-beats", self.plan_path, "storyboard at least three visible beats for the dominant interaction")
        for beat in beats:
            for field in ("beat", "trigger", "visible_change", "exit_condition", "fallback"):
                if not str(beat.get(field) or "").strip():
                    self.error("plan.motion-beat-detail", self.plan_path, f"motion beat needs {field.replace('_', ' ')}")

        conversion = self.plan.get("conversion_plan") or {}
        for field in ("primary_action", "truthful_destination", "readiness_moment", "story_integration"):
            self.require_text(conversion, field, f"plan.conversion-{field}", f"conversion plan: {field.replace('_', ' ')}")

        review = self.plan.get("director_review") or {}
        if review.get("status") != "passed":
            self.error("plan.director-review", self.plan_path, "complete and pass the post-render creative-director review")
        if int(review.get("revision_rounds") or 0) < 1:
            self.error("plan.revision-round", self.plan_path, "complete at least one browser-rendered revision round")
        for field in ("strongest_decision", "weakest_decision"):
            self.require_text(review, field, f"plan.review-{field}", f"director review: {field.replace('_', ' ')}")
        if not review.get("revisions_completed"):
            self.error("plan.revisions-completed", self.plan_path, "record the revisions completed after the director critique")

        visual = (self.plan.get("verification") or {}).get("visual_review") or {}
        if visual.get("status") != "passed":
            self.error("plan.visual-review", self.plan_path, "complete and pass the visual browser review")
        required_states = {"desktop-entry", "desktop-25", "desktop-50", "desktop-75", "desktop-close", "mobile-entry", "mobile-full", "reduced-motion"}
        checked_states = {str(value) for value in visual.get("checked_states") or []}
        missing_states = required_states - checked_states
        if missing_states:
            self.error("plan.visual-states", self.plan_path, f"visual review is missing: {', '.join(sorted(missing_states))}")
        for field in ("dead_space_review", "reference_comparison", "mobile_recomposition_review", "interaction_review"):
            self.require_text(visual, field, f"plan.visual-{field}", f"visual review: {field.replace('_', ' ')}")
        if not visual.get("revisions_after_review"):
            self.error("plan.visual-revisions", self.plan_path, "record at least one revision made after visual review")

    def load_plan(self) -> None:
        if not self.plan_path.is_file():
            self.error("plan.missing", self.plan_path, "lumora-plan.json is required")
            return
        try:
            self.plan = json.loads(self.plan_path.read_text(encoding="utf-8"))
        except Exception as exc:
            self.error("plan.invalid-json", self.plan_path, f"cannot parse plan: {exc}")
            return
        schema = self.plan.get("schema")
        if schema == "lumora.project_plan.v3":
            self.check_v3_plan()
        elif schema == "lumora.project_plan.v4":
            self.check_v4_plan()
        else:
            self.error("plan.schema", self.plan_path, "expected schema lumora.project_plan.v4")

    def check_required_files(self) -> None:
        for name in ("index.html", "404.html", ".nojekyll"):
            path = self.site_root / name
            if not path.exists():
                self.error("pages.required-file", path, f"missing GitHub Pages file {name}")

    def check_html_metadata(self, path: Path, parser: AuditParser) -> None:
        if not parser.html_lang:
            self.error("html.lang", path, "html element needs a language")
        if not parser.has_viewport:
            self.error("html.viewport", path, "missing viewport meta tag")
        if not parser.title_text:
            self.error("html.title", path, "missing page title")
        if not parser.has_description:
            self.warning("html.description", path, "missing meta description")

    @staticmethod
    def is_external(value: str) -> bool:
        split = urlsplit(value)
        return bool(split.scheme in {"http", "https", "mailto", "tel", "sms", "data", "blob"} or value.startswith("//"))

    def check_external_placeholder(self, path: Path, value: str, line: int) -> None:
        host = (urlsplit(value).hostname or "").lower()
        if any(host == blocked or host.endswith(f".{blocked}") for blocked in PLACEHOLDER_HOSTS):
            self.error("media.placeholder", path, f"placeholder/stock URL is not final media: {value}", line)

    def resolve_local(self, owner: Path, value: str) -> tuple[Path, str]:
        split = urlsplit(value)
        raw_path = unquote(split.path)
        target = (owner.parent / raw_path).resolve() if raw_path else owner.resolve()
        if raw_path.endswith("/"):
            target = target / "index.html"
        return target, split.fragment

    def check_url(self, owner: Path, tag: str, attr: str, value: str, line: int) -> None:
        clean = value.strip()
        if not clean:
            self.error("url.empty", owner, f"empty {attr} on <{tag}>", line)
            return
        if clean == "#" or clean.lower().startswith("javascript:"):
            self.error("url.placeholder", owner, f"nonfunctional URL {clean!r}", line)
            return
        if clean.startswith("/") and not clean.startswith("//"):
            self.error("pages.root-absolute", owner, f"root-absolute URL breaks repository Pages: {clean}", line)
            return
        if self.is_external(clean):
            self.check_external_placeholder(owner, clean, line)
            if "gsap" in clean.lower() and ("@latest" in clean.lower() or "gsap@" not in clean.lower()):
                self.warning("dependency.unpinned-gsap", owner, f"pin the GSAP CDN version: {clean}", line)
            return

        target, fragment = self.resolve_local(owner, clean)
        try:
            target.relative_to(self.site_root)
        except ValueError:
            self.error("url.escape", owner, f"local URL escapes the site root: {clean}", line)
            return
        if not target.exists():
            self.error("url.missing-target", owner, f"missing local target for {clean}", line)
            return
        if fragment and target.suffix.lower() in {"", ".html", ".htm"}:
            html_target = target if target.suffix else target / "index.html"
            if html_target.is_file() and fragment not in self.parse_html(html_target).ids:
                self.error("url.missing-anchor", owner, f"missing anchor #{fragment} in {html_target.name}", line)

    def check_html_elements(self, path: Path, parser: AuditParser) -> None:
        for tag, attr, value, line in parser.urls:
            self.check_url(path, tag, attr, value, line)
        for attrs, line in parser.images:
            src = attrs.get("src", "").strip()
            if src:
                self.image_usage[src] += 1
            if "alt" not in attrs:
                self.error("image.alt", path, "image is missing alt text", line)
            if not attrs.get("width") or not attrs.get("height"):
                self.warning("image.dimensions", path, "set image width and height to stabilize layout", line)
        for attrs, line in parser.videos:
            if "autoplay" in attrs and ("muted" not in attrs or "playsinline" not in attrs):
                self.error("video.autoplay", path, "autoplay video must be muted and playsinline", line)
            if not attrs.get("poster"):
                self.warning("video.poster", path, "video should have a useful poster", line)
        for attrs, line in parser.forms:
            action = attrs.get("action", "").strip()
            if action in {"#", "javascript:void(0)"}:
                self.error("form.fake-action", path, "form action is not real", line)
            if not action and not any(name.startswith("data-") and value for name, value in attrs.items()):
                self.warning("form.no-action", path, "form has no action or declared client handler", line)
        for button in parser.buttons:
            attrs = button["attrs"]
            if not button["text"] and not attrs.get("aria-label") and not attrs.get("title"):
                self.error("button.name", path, "button has no accessible name", button["line"])
            if not attrs.get("type"):
                self.warning("button.type", path, "set an explicit button type", button["line"])

        selected_ids = {source.get("id") for source in self.plan.get("source_mix", [])}
        for attrs, line in parser.sections:
            section_id = attrs.get("id", "").strip()
            if not section_id:
                self.error("trace.section-id", path, "major section is missing a stable id", line)
            source_attr = attrs.get("data-lumora-source", "")
            if not source_attr:
                self.error("trace.section-source", path, "major section is missing data-lumora-source", line)
                continue
            section_ids = {value.strip() for value in source_attr.split(",") if value.strip()}
            self.used_source_ids.update(section_ids)
            if section_id:
                self.section_sources.setdefault(section_id, set()).update(section_ids)
            unknown = section_ids - selected_ids
            if unknown:
                self.error("trace.unknown-source", path, f"section uses unselected source ids: {', '.join(sorted(unknown))}", line)
            if self.plan.get("schema") == "lumora.project_plan.v4":
                anchor_id = next((source.get("id") for source in self.plan.get("source_mix", []) if source.get("job") == "anchor"), None)
                if anchor_id and anchor_id not in section_ids:
                    self.error("trace.anchor-missing", path, f"section must retain anchor source {anchor_id!r}", line)
        text = " ".join(parser.visible_text)
        for pattern in GENERIC_COPY:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                self.warning("copy.generic", path, f"review generic phrase {match.group(0)!r}")

    def check_css_urls(self, path: Path) -> None:
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", text, re.IGNORECASE):
            value = match.group(2).strip()
            if not value or value.startswith("data:"):
                continue
            line = text.count("\n", 0, match.start()) + 1
            self.check_url(path, "css", "url", value, line)

    def check_motion(self, text_files: list[Path]) -> None:
        aggregate = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in text_files)
        has_advanced_motion = bool(re.search(r"\b(?:gsap|ScrollTrigger|requestAnimationFrame|parallax|scroll-progress|data-reveal)\b|@keyframes", aggregate, re.IGNORECASE))
        has_reduced_motion = "prefers-reduced-motion" in aggregate
        if has_advanced_motion and not has_reduced_motion:
            self.error("motion.reduced", self.site_root, "advanced motion exists without a prefers-reduced-motion path")
        scrub_count = len(re.findall(r"\bscrub\s*:", aggregate, re.IGNORECASE))
        if scrub_count > 1:
            self.warning("motion.multiple-scrubs", self.site_root, f"found {scrub_count} scrubbed timelines; confirm only one is the dominant experience and the others remain subordinate")
        has_autoplay_state = bool(re.search(r"\bsetInterval\s*\(|\bautoplay\b", aggregate, re.IGNORECASE))
        has_drag_state = "pointerdown" in aggregate and bool(re.search(r"scrollBy|translateX|drag", aggregate, re.IGNORECASE))
        if scrub_count and has_autoplay_state and has_drag_state:
            self.warning("motion.competing-systems", self.site_root, "scrubbed scroll, autoplay state, and drag behavior all appear; review whether the page has multiple competing interaction centers")

        long_scroll_justification = str((self.plan.get("motion_plan") or {}).get("long_scroll_justification") or "").strip()
        for path in text_files:
            if path.suffix.lower() != ".css":
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for match in re.finditer(r"\b(?:min-)?height\s*:\s*([0-9]+(?:\.[0-9]+)?)\s*(?:d|s|l)?vh\b", text, re.IGNORECASE):
                if float(match.group(1)) < 240:
                    continue
                line = text.count("\n", 0, match.start()) + 1
                if not long_scroll_justification:
                    self.warning("motion.long-scroll", path, f"{match.group(1)}vh scroll track needs a beat-by-beat occupancy justification", line)

    def check_media_reuse(self) -> None:
        for src, count in self.image_usage.items():
            filename = Path(urlsplit(src).path).name.lower()
            if count <= 2 or any(token in filename for token in ("logo", "icon", "mark", "favicon")):
                continue
            self.warning("media.reuse", self.site_root, f"image {src!r} is used {count} times; prominent repeated reuse usually weakens the asset campaign")

    def run(self) -> list[Finding]:
        if not self.site_root.is_dir():
            self.error("site.missing", self.site_root, "site root does not exist")
            return self.findings
        self.load_plan()
        self.check_required_files()
        html_files = sorted(self.site_root.rglob("*.html"))
        if not html_files:
            self.error("html.none", self.site_root, "no HTML files found")
            return self.findings
        for path in html_files:
            parser = self.parse_html(path)
            self.check_html_metadata(path, parser)
            self.check_html_elements(path, parser)
        self.check_media_reuse()
        selected_ids = {source.get("id") for source in self.plan.get("source_mix", []) if source.get("id")}
        for missing in sorted(selected_ids - self.used_source_ids):
            self.error("trace.unused-source", self.plan_path, f"selected source {missing!r} is not used by any HTML section")
        for source in self.plan.get("source_mix", []):
            source_id = source.get("id")
            for section_id in source.get("implemented_sections") or []:
                if section_id not in self.section_sources:
                    self.error("trace.missing-section", self.plan_path, f"implemented section {section_id!r} for {source_id!r} does not exist")
                elif source_id not in self.section_sources[section_id]:
                    self.error("trace.section-mismatch", self.plan_path, f"section {section_id!r} does not declare source {source_id!r}")
        for mapping in self.plan.get("source_to_section_map") or []:
            section_id = mapping.get("section_id")
            if section_id not in self.section_sources:
                self.error("trace.plan-section", self.plan_path, f"planned section {section_id!r} does not exist")
                continue
            missing_sources = set(mapping.get("source_ids") or []) - self.section_sources[section_id]
            if missing_sources:
                self.error(
                    "trace.plan-source",
                    self.plan_path,
                    f"planned section {section_id!r} is missing source ids: {', '.join(sorted(missing_sources))}",
                )
        css_files = sorted(self.site_root.rglob("*.css"))
        js_files = sorted(self.site_root.rglob("*.js"))
        for path in css_files:
            self.check_css_urls(path)
        self.check_motion(css_files + js_files)
        return self.findings


def print_human(findings: list[Finding]) -> None:
    for finding in findings:
        location = finding.file + (f":{finding.line}" if finding.line else "")
        print(f"{finding.severity.upper():7} {finding.code:28} {location} - {finding.message}")
    errors = sum(1 for finding in findings if finding.severity == "error")
    warnings = sum(1 for finding in findings if finding.severity == "warning")
    print(f"Lumora audit: {errors} error(s), {warnings} warning(s)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", type=Path, required=True)
    parser.add_argument("--plan", type=Path, help="Defaults to <site-root>/lumora-plan.json")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    args = parser.parse_args()
    plan = args.plan or args.site_root / "lumora-plan.json"
    auditor = Auditor(args.site_root, plan, strict=args.strict)
    findings = auditor.run()
    errors = sum(1 for finding in findings if finding.severity == "error")
    warnings = sum(1 for finding in findings if finding.severity == "warning")
    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "findings": [asdict(item) for item in findings]}, indent=2))
    else:
        print_human(findings)
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
