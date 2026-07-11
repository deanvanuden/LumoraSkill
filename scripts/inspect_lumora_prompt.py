#!/usr/bin/env python3
"""Inspect a full Lumora prompt or focused source excerpts by exact prompt id."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIBRARY = ROOT / "references" / "motionsites-prompt-library.json"


FOCUS_TERMS: dict[str, tuple[str, ...]] = {
    "layout": ("layout", "structure", "section", "hero", "grid", "composition", "spacing", "position", "sticky", "pin"),
    "visual": ("visual", "style", "color", "palette", "background", "typography", "font", "surface", "border", "shadow", "texture"),
    "media": ("image", "photo", "video", "asset", "canvas", "webgl", "three", "3d", "gallery", "poster"),
    "motion": ("animation", "transition", "motion", "scroll", "gsap", "scrolltrigger", "parallax", "scrub", "reveal", "hover"),
    "interaction": ("interaction", "button", "menu", "tab", "accordion", "carousel", "slider", "form", "toggle", "drag", "selector"),
    "responsive": ("responsive", "mobile", "tablet", "breakpoint", "media query", "reduced motion", "accessibility", "touch"),
    "conversion": ("cta", "call to action", "pricing", "purchase", "checkout", "booking", "contact", "signup", "form"),
}


@dataclass(frozen=True)
class Section:
    heading: str
    body: str


def load_prompt(library_path: Path, prompt_id: str) -> dict[str, Any]:
    payload = json.loads(library_path.read_text(encoding="utf-8"))
    matches = [item for item in payload.get("prompts", []) if item.get("id") == prompt_id]
    if len(matches) != 1:
        raise LookupError(f"expected exactly one prompt with id {prompt_id!r}")
    prompt = matches[0]
    if not isinstance(prompt.get("prompt_text"), str) or not prompt["prompt_text"]:
        raise LookupError(f"prompt {prompt_id!r} has no available prompt_text")
    return prompt


def split_sections(text: str) -> list[Section]:
    lines = text.splitlines(keepends=True)
    sections: list[Section] = []
    heading = "Opening"
    body: list[str] = []

    for line in lines:
        stripped = line.strip()
        markdown_heading = re.match(r"^#{1,5}\s+(.+)$", stripped)
        upper_heading = bool(
            stripped.endswith(":")
            and 1 <= len(stripped.rstrip(":").split()) <= 10
            and stripped.rstrip(":").upper() == stripped.rstrip(":")
        )
        if markdown_heading or upper_heading:
            if body and "".join(body).strip():
                sections.append(Section(heading=heading, body="".join(body).strip()))
            heading = (markdown_heading.group(1) if markdown_heading else stripped.rstrip(":"))[:180]
            body = []
        else:
            body.append(line)

    if body and "".join(body).strip():
        sections.append(Section(heading=heading, body="".join(body).strip()))
    return sections


def focus_words(focuses: list[str]) -> tuple[str, ...]:
    words: list[str] = []
    for focus in focuses:
        if focus not in FOCUS_TERMS:
            valid = ", ".join(sorted(FOCUS_TERMS))
            raise ValueError(f"unknown focus {focus!r}; choose from {valid}")
        words.extend(FOCUS_TERMS[focus])
    return tuple(dict.fromkeys(words))


def section_score(section: Section, words: tuple[str, ...]) -> int:
    heading = section.heading.lower()
    body = section.body.lower()
    return sum(8 * heading.count(word) + min(5, body.count(word)) for word in words)


def context_windows(text: str, words: tuple[str, ...], max_windows: int = 6) -> list[Section]:
    lower = text.lower()
    positions = sorted({lower.find(word) for word in words if lower.find(word) >= 0})
    windows: list[Section] = []
    used_ends: list[int] = []
    for index, position in enumerate(positions):
        start = max(0, position - 600)
        end = min(len(text), position + 1500)
        if any(start < used_end for used_end in used_ends):
            continue
        windows.append(Section(heading=f"Context {index + 1}", body=text[start:end].strip()))
        used_ends.append(end)
        if len(windows) >= max_windows:
            break
    return windows


def focused_excerpt(text: str, focuses: list[str], max_chars: int) -> list[Section]:
    words = focus_words(focuses)
    ranked = sorted(split_sections(text), key=lambda section: section_score(section, words), reverse=True)
    selected = [section for section in ranked if section_score(section, words) > 0]
    if not selected:
        selected = context_windows(text, words)

    output: list[Section] = []
    used = 0
    for section in selected:
        allowance = max_chars - used
        if allowance <= 300:
            break
        body = section.body[: max(0, allowance - len(section.heading) - 20)].rstrip()
        if not body:
            continue
        output.append(Section(section.heading, body))
        used += len(section.heading) + len(body) + 20
    return output


def parse_focus(value: str) -> list[str]:
    focuses = [part.strip().lower() for part in value.split(",") if part.strip()]
    if not focuses:
        raise ValueError("--focus requires at least one focus name")
    return focuses


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True, help="Exact source prompt id")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--full", action="store_true", help="Write the exact prompt body to stdout")
    mode.add_argument("--focus", help="Comma-separated focuses such as layout,visual,media,motion,responsive")
    parser.add_argument("--max-chars", type=int, default=12000, help="Maximum focused output size")
    parser.add_argument("--library", type=Path, default=DEFAULT_LIBRARY)
    args = parser.parse_args()

    try:
        prompt = load_prompt(args.library.resolve(), args.id)
        text = prompt["prompt_text"]
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if args.full:
            sys.stdout.buffer.write(text.encode("utf-8"))
            sys.stdout.buffer.flush()
            sys.stderr.write(f"\nSOURCE:{args.id} SHA256:{digest}\n")
            return 0

        focuses = parse_focus(args.focus)
        excerpts = focused_excerpt(text, focuses, max(1000, args.max_chars))
        print(f"# Lumora source: {prompt.get('title') or args.id}")
        print()
        print(f"- id: `{args.id}`")
        print(f"- category: `{prompt.get('ui_category') or (prompt.get('metadata') or {}).get('category') or ''}`")
        print(f"- prompt_sha256: `{digest}`")
        print(f"- focus: `{', '.join(focuses)}`")
        for section in excerpts:
            print()
            print(f"## {section.heading}")
            print()
            print(section.body)
        return 0
    except Exception as exc:
        sys.stderr.write(f"ERROR: {exc}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
