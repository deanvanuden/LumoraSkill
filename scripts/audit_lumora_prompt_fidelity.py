#!/usr/bin/env python3
"""Verify that a Lumora build has an explicit prompt-fidelity pass report.

This script cannot judge visual fidelity by itself. It enforces the evidence
contract that the agent must complete after reading the loaded prompt_text:

- every used data-prompt-id is covered by a fidelity section entry
- each covered prompt is marked pass, not partial/risk/fail
- the agent explicitly asserts that layout, components, motion, responsive
  behavior, media behavior, CTA placement, and verification requirements were
  compared against the loaded prompt_text

Use this as a hard gate next to manifest and visual asset audits.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROMPT_ID_RE = re.compile(r"""data-prompt-id\s*=\s*["']([^"']+)["']""")
SCAN_SUFFIXES = {".html", ".htm", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}
REQUIRED_CHECKS = {
    "layout",
    "component_structure",
    "motion",
    "responsive_behavior",
    "media_behavior",
    "cta_placement",
    "verification_requirements",
}


def fail(message: str) -> int:
    sys.stderr.write(f"ERROR: {message}\n")
    return 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", required=True, help="Generated Lumora site root.")
    parser.add_argument(
        "--manifest",
        help="Path to lumora-manifest.json. Defaults to <site-root>/lumora-manifest.json.",
    )
    parser.add_argument(
        "--report",
        help=(
            "Path to lumora-prompt-fidelity.json. Defaults to "
            "<site-root>/lumora-prompt-fidelity.json."
        ),
    )
    return parser.parse_args(argv)


def resolve_inside_repo(path: str | Path, label: str) -> Path:
    resolved = Path(path).resolve()
    allowed_roots = (ROOT.resolve(), Path.cwd().resolve())
    if not any(is_relative_to(resolved, root) for root in allowed_roots):
        raise ValueError(f"{label} must stay inside the skill root or current workspace")
    return resolved


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise FileNotFoundError(f"file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_ids(manifest: Any) -> set[str]:
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object")
    selected = manifest.get("selected_prompts", manifest.get("prompts"))
    if not isinstance(selected, list) or not selected:
        raise ValueError("manifest must contain non-empty selected_prompts list")
    ids: set[str] = set()
    for entry in selected:
        if not isinstance(entry, dict):
            raise ValueError("each selected prompt manifest entry must be an object")
        prompt_id = entry.get("id")
        if not isinstance(prompt_id, str) or not prompt_id:
            raise ValueError("selected prompt entry missing id")
        if prompt_id in ids:
            raise ValueError(f"duplicate prompt id in manifest: {prompt_id}")
        ids.add(prompt_id)
    return ids


def scan_prompt_ids(site_root: Path) -> set[str]:
    found: set[str] = set()
    for path in site_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        if any(part in {"node_modules", "dist", ".git"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        found.update(match.group(1) for match in PROMPT_ID_RE.finditer(text))
    return found


def normalize_checks(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    checks: set[str] = set()
    for item in value:
        if isinstance(item, str):
            checks.add(item.strip().lower())
    return checks


def as_bool(value: Any) -> bool:
    return value is True


def audit_report(report: Any, manifest_prompt_ids: set[str], used_prompt_ids: set[str]) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["prompt fidelity report must be a JSON object"]

    if str(report.get("audit_type", "")).lower() != "prompt_fidelity":
        errors.append("audit_type must be prompt_fidelity")
    if str(report.get("overall_status", "")).lower() != "pass":
        errors.append("overall_status must be pass")
    if not as_bool(report.get("all_sections_prompt_verbatim")):
        errors.append("all_sections_prompt_verbatim must be true")
    if not as_bool(report.get("no_partial_or_inspired_sections")):
        errors.append("no_partial_or_inspired_sections must be true")

    sections = report.get("sections")
    if not isinstance(sections, list) or not sections:
        return [*errors, "sections must be a non-empty list"]

    covered: set[str] = set()
    for index, section in enumerate(sections, start=1):
        label = f"sections[{index}]"
        if not isinstance(section, dict):
            errors.append(f"{label}: section entry must be an object")
            continue

        prompt_id = section.get("prompt_id")
        if not isinstance(prompt_id, str) or not prompt_id:
            errors.append(f"{label}: missing prompt_id")
            continue
        covered.add(prompt_id)

        status = str(section.get("status", "")).lower()
        if status != "pass":
            errors.append(f"{prompt_id}: status must be pass, got {status or 'missing'}")

        if prompt_id not in manifest_prompt_ids:
            errors.append(f"{prompt_id}: prompt_id is not present in manifest")

        files = section.get("implementation_files")
        if not isinstance(files, list) or not files or not all(isinstance(item, str) for item in files):
            errors.append(f"{prompt_id}: implementation_files must be a non-empty string list")

        checks = normalize_checks(section.get("prompt_requirements_checked"))
        missing_checks = REQUIRED_CHECKS - checks
        if missing_checks:
            errors.append(f"{prompt_id}: missing prompt_requirements_checked {sorted(missing_checks)}")

        for field in (
            "loaded_prompt_text_compared",
            "structure_layout_components_motion_1_to_1",
            "only_allowed_adaptations_used",
            "no_unlisted_prompt_deviations",
        ):
            if not as_bool(section.get(field)):
                errors.append(f"{prompt_id}: {field} must be true")

        summary = section.get("fidelity_summary")
        if not isinstance(summary, str) or len(summary.strip()) < 24:
            errors.append(f"{prompt_id}: fidelity_summary must explain the pass evidence")

        deviations = section.get("deviations")
        if deviations not in ([], None):
            errors.append(f"{prompt_id}: deviations must be empty for a pass report")

    required_coverage = used_prompt_ids or manifest_prompt_ids
    missing = required_coverage - covered
    if missing:
        errors.append(f"prompt ids missing from fidelity report: {sorted(missing)}")
    extra = covered - manifest_prompt_ids
    if extra:
        errors.append(f"fidelity report contains prompt ids absent from manifest: {sorted(extra)}")

    return errors


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        site_root = resolve_inside_repo(args.site_root, "site root")
        if not site_root.is_dir():
            raise FileNotFoundError(f"site root not found: {site_root}")
        manifest_path = resolve_inside_repo(
            args.manifest or site_root / "lumora-manifest.json", "manifest"
        )
        report_path = resolve_inside_repo(
            args.report or site_root / "lumora-prompt-fidelity.json", "prompt fidelity report"
        )

        manifest_prompt_ids = manifest_ids(load_json(manifest_path))
        used_prompt_ids = scan_prompt_ids(site_root)
        unknown_used = used_prompt_ids - manifest_prompt_ids
        if unknown_used:
            raise ValueError(f"data-prompt-id values missing from manifest: {sorted(unknown_used)}")

        errors = audit_report(load_json(report_path), manifest_prompt_ids, used_prompt_ids)
        if errors:
            for error in errors:
                sys.stderr.write(f"ERROR: {error}\n")
            return 1

    except Exception as exc:
        return fail(str(exc))

    print("Lumora prompt fidelity audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
