#!/usr/bin/env python3
"""Load one Lumora prompt_text from the bundled JSON library.

Stdout is reserved for the exact prompt_text bytes only.
Diagnostics, including optional hashes, go to stderr.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LIBRARY = ROOT / "references" / "motionsites-prompt-library.json"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--id",
        dest="ids",
        action="append",
        required=True,
        help="Exact JSON prompt entry id to load. Only one --id is allowed.",
    )
    parser.add_argument(
        "--sha256",
        action="store_true",
        help="Write SHA256:<hash> to stderr after loading.",
    )
    parser.add_argument(
        "--library",
        default=str(DEFAULT_LIBRARY),
        help="Prompt library JSON path. Defaults to references/motionsites-prompt-library.json.",
    )
    return parser.parse_args(argv)


def fail(message: str) -> int:
    sys.stderr.write(f"ERROR: {message}\n")
    return 1


def validate_exact_id(ids: list[str]) -> str:
    if len(ids) != 1:
        raise ValueError("exactly one --id value is required")

    prompt_id = ids[0]
    if not prompt_id:
        raise ValueError("prompt id must not be empty")
    if prompt_id in {".", ".."}:
        raise ValueError("prompt id must be an exact library id")
    if "/" in prompt_id or "\\" in prompt_id or "," in prompt_id:
        raise ValueError("prompt id must not contain path separators or comma-separated ids")
    return prompt_id


def load_library(path: Path) -> dict[str, Any]:
    resolved = path.resolve()
    root = ROOT.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError("library path must stay inside the LumoraSkill repository") from exc

    if not resolved.is_file():
        raise FileNotFoundError(f"prompt library not found: {resolved}")
    return json.loads(resolved.read_text(encoding="utf-8"))


def prompt_text_for_id(library: dict[str, Any], prompt_id: str) -> str:
    matches = [item for item in library.get("prompts", []) if isinstance(item, dict) and item.get("id") == prompt_id]
    if len(matches) != 1:
        raise LookupError(f"expected exactly one prompt entry for id: {prompt_id}")

    prompt_text = matches[0].get("prompt_text")
    if not isinstance(prompt_text, str) or not prompt_text:
        raise LookupError(f"prompt entry has no prompt_text: {prompt_id}")
    return prompt_text


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        prompt_id = validate_exact_id(args.ids)
        library = load_library(Path(args.library))
        data = prompt_text_for_id(library, prompt_id).encode("utf-8")
    except Exception as exc:
        return fail(str(exc))

    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()

    if args.sha256:
        digest = hashlib.sha256(data).hexdigest()
        sys.stderr.write(f"SHA256:{digest}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
