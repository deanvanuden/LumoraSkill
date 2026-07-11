#!/usr/bin/env python3
"""Validate a Lumora website for traceability and GitHub Pages delivery."""

from __future__ import annotations

import argparse
import json
import re
import sys
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

    def load_plan(self) -> None:
        if not self.plan_path.is_file():
            self.error("plan.missing", self.plan_path, "lumora-plan.json is required")
            return
        try:
            self.plan = json.loads(self.plan_path.read_text(encoding="utf-8"))
        except Exception as exc:
            self.error("plan.invalid-json", self.plan_path, f"cannot parse plan: {exc}")
            return
        if self.plan.get("schema") != "lumora.project_plan.v3":
            self.error("plan.schema", self.plan_path, "expected schema lumora.project_plan.v3")

        direction = self.plan.get("creative_direction") or {}
        required_direction = {
            "creative_thesis": "creative thesis",
            "signature_motif": "signature motif",
            "company_specificity_test": "company specificity test",
        }
        for key, label in required_direction.items():
            if not str(direction.get(key) or "").strip():
                self.error(f"plan.{key}", self.plan_path, f"fill the {label} before delivery")
        if direction.get("status") != "locked":
            self.warning("plan.direction-status", self.plan_path, "set creative_direction.status to 'locked' after the direction is approved")

        source_library = json.loads(SOURCE_LIBRARY.read_text(encoding="utf-8"))
        valid_sources = {
            item.get("id"): item.get("prompt_sha256")
            for item in source_library.get("prompts", [])
            if item.get("id") and item.get("prompt_text")
        }
        source_mix = self.plan.get("source_mix") or []
        if len(source_mix) < 3:
            self.error("plan.source-count", self.plan_path, "use at least three distinct prompt donors")
        seen_ids: set[str] = set()
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
            if len(contributions) < 2:
                self.error("plan.source-contributions", self.plan_path, f"{prompt_id!r} needs at least two implemented contributions")
            if not source.get("implemented_sections"):
                self.error("plan.source-sections", self.plan_path, f"{prompt_id!r} needs at least one implemented section")

        media = self.plan.get("media_plan") or {}
        if media.get("required_roles") and not media.get("slots"):
            self.error("plan.media-slots", self.plan_path, "define the media slots before delivery")
        motion = self.plan.get("motion_plan") or {}
        if not str(motion.get("desktop_implementation") or "").strip():
            self.error("plan.motion-desktop", self.plan_path, "describe the desktop signature motion implementation")
        if not str(motion.get("mobile_recomposition") or "").strip():
            self.error("plan.motion-mobile", self.plan_path, "describe the mobile motion recomposition")

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
