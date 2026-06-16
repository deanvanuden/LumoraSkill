#!/usr/bin/env python3
"""Verify that a Lumora build has hash-backed selected prompt evidence.

This script cannot prove visual fidelity by itself. It enforces the non-negotiable
evidence gate: every claimed data-prompt-id must point to a real library entry and
the build manifest must include the exact SHA256 of that entry's prompt_text.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIBRARY = ROOT / "references" / "motionsites-prompt-library.json"
PROMPT_ID_RE = re.compile(r"""data-prompt-id\s*=\s*["']([^"']+)["']""")
SCAN_SUFFIXES = {".html", ".htm", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}


def fail(message: str) -> int:
    sys.stderr.write(f"ERROR: {message}\n")
    return 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to lumora-manifest.json for the generated site.",
    )
    parser.add_argument(
        "--output-root",
        help="Generated site root to scan for data-prompt-id attributes.",
    )
    parser.add_argument(
        "--library",
        default=str(DEFAULT_LIBRARY),
        help="Prompt library JSON path. Defaults to references/motionsites-prompt-library.json.",
    )
    return parser.parse_args(argv)


def resolve_inside_repo(path: str | Path, label: str) -> Path:
    resolved = Path(path).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} must stay inside the LumoraSkill repository") from exc
    return resolved


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def library_entries(path: Path) -> dict[str, dict[str, Any]]:
    data = load_json(path)
    prompts = data.get("prompts")
    if not isinstance(prompts, list):
        raise ValueError("prompt library must contain a prompts list")

    entries: dict[str, dict[str, Any]] = {}
    for item in prompts:
        if not isinstance(item, dict):
            continue
        prompt_id = item.get("id")
        if not isinstance(prompt_id, str) or not prompt_id:
            continue
        if prompt_id in entries:
            raise ValueError(f"duplicate prompt id in library: {prompt_id}")
        entries[prompt_id] = item
    return entries


def manifest_entries(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object")
    entries = data.get("selected_prompts", data.get("prompts"))
    if not isinstance(entries, list) or not entries:
        raise ValueError("manifest must contain non-empty selected_prompts list")
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("each selected prompt manifest entry must be an object")
    return entries


def scan_prompt_ids(output_root: Path) -> set[str]:
    if not output_root.is_dir():
        raise FileNotFoundError(f"output root not found: {output_root}")

    found: set[str] = set()
    for path in output_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        if "node_modules" in path.parts or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        found.update(match.group(1) for match in PROMPT_ID_RE.finditer(text))
    return found


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        manifest_path = resolve_inside_repo(args.manifest, "manifest")
        library_path = resolve_inside_repo(args.library, "library")
        entries = library_entries(library_path)
        manifest = load_json(manifest_path)
        selected = manifest_entries(manifest)

        seen: set[str] = set()
        manifest_ids: set[str] = set()
        for entry in selected:
            prompt_id = entry.get("id")
            sha256 = entry.get("sha256")
            loaded = entry.get("loaded", True)

            if not isinstance(prompt_id, str) or not prompt_id:
                raise ValueError("selected prompt entry missing id")
            if prompt_id in seen:
                raise ValueError(f"duplicate prompt id in manifest: {prompt_id}")
            seen.add(prompt_id)
            manifest_ids.add(prompt_id)

            if loaded is not True:
                raise ValueError(f"manifest entry must mark loaded=true: {prompt_id}")
            if prompt_id not in entries:
                raise ValueError(f"manifest id is not in library: {prompt_id}")
            prompt_text = entries[prompt_id].get("prompt_text")
            if not isinstance(prompt_text, str) or not prompt_text:
                raise ValueError(f"library entry has no prompt_text: {prompt_id}")
            actual_hash = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
            if sha256 != actual_hash:
                raise ValueError(
                    f"sha256 mismatch for {prompt_id}: expected {actual_hash}, got {sha256!r}"
                )

        if args.output_root:
            output_root = resolve_inside_repo(args.output_root, "output root")
            used_ids = scan_prompt_ids(output_root)
            if not used_ids:
                raise ValueError("no data-prompt-id attributes found in output root")
            unknown = used_ids - manifest_ids
            if unknown:
                raise ValueError(f"data-prompt-id values missing from manifest: {sorted(unknown)}")
            unused = manifest_ids - used_ids
            if unused:
                raise ValueError(f"manifest ids not found in output root: {sorted(unused)}")

    except Exception as exc:
        return fail(str(exc))

    print("Lumora manifest verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
