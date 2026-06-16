#!/usr/bin/env python3
"""Audit Lumora media slots and brand color discipline.

This script does not replace browser QA. It catches repeatable failures that are
easy to miss during implementation:

- tiny source images stretched into large hero/card slots
- duplicated prominent media
- missing focal-point crop metadata
- generated images that claim to depict exact real-world people/places/products
- saturated off-brand colors left in source files after token mapping
"""

from __future__ import annotations

import argparse
import colorsys
import json
import re
import struct
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCAN_SUFFIXES = {".css", ".html", ".htm", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}
RASTER_SUFFIXES = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
NON_PROMINENT_TYPES = {"icon", "logo", "texture", "pattern"}
DEFAULT_MIN_SCALE = 1.5

HEX_RE = re.compile(r"(?<![A-Za-z0-9_-])#([0-9A-Fa-f]{3,8})(?![A-Za-z0-9_-])")


def fail(message: str) -> int:
    sys.stderr.write(f"ERROR: {message}\n")
    return 1


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-root", required=True, help="Generated Lumora site root.")
    parser.add_argument(
        "--media-plan",
        help="Path to lumora-media-plan.json. Defaults to <site-root>/lumora-media-plan.json.",
    )
    parser.add_argument(
        "--min-scale",
        type=float,
        default=DEFAULT_MIN_SCALE,
        help="Required asset pixel scale versus target render size for prominent raster media.",
    )
    parser.add_argument(
        "--no-color-audit",
        action="store_true",
        help="Skip saturated off-brand color scanning.",
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


def normalize_hex(value: str) -> tuple[int, int, int, float] | None:
    text = value.strip().lstrip("#")
    if len(text) == 3:
        text = "".join(ch * 2 for ch in text)
    elif len(text) == 4:
        text = "".join(ch * 2 for ch in text)
    if len(text) not in {6, 8}:
        return None
    try:
        red = int(text[0:2], 16)
        green = int(text[2:4], 16)
        blue = int(text[4:6], 16)
        alpha = int(text[6:8], 16) / 255 if len(text) == 8 else 1.0
    except ValueError:
        return None
    return red, green, blue, alpha


def hex_to_hls(value: str) -> tuple[float, float, float, float] | None:
    rgba = normalize_hex(value)
    if rgba is None:
        return None
    red, green, blue, alpha = rgba
    hue, lightness, saturation = colorsys.rgb_to_hls(red / 255, green / 255, blue / 255)
    return hue * 360, lightness, saturation, alpha


def color_distance(a: tuple[int, int, int, float], b: tuple[int, int, int, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def hue_distance(a: float, b: float) -> float:
    diff = abs(a - b) % 360
    return min(diff, 360 - diff)


def parse_aspect_ratio(value: Any) -> float | None:
    if isinstance(value, (int, float)) and value > 0:
        return float(value)
    if not isinstance(value, str):
        return None
    text = value.strip().lower()
    if ":" in text:
        left, right = text.split(":", 1)
        try:
            width = float(left)
            height = float(right)
        except ValueError:
            return None
        return width / height if height > 0 else None
    try:
        parsed = float(text)
    except ValueError:
        return None
    return parsed if parsed > 0 else None


def read_image_size(path: Path) -> tuple[int, int]:
    suffix = path.suffix.lower()
    with path.open("rb") as handle:
        header = handle.read(32)
        if suffix == ".png" and header.startswith(b"\x89PNG\r\n\x1a\n"):
            return struct.unpack(">II", header[16:24])
        if suffix == ".gif" and header[:6] in {b"GIF87a", b"GIF89a"}:
            return struct.unpack("<HH", header[6:10])
        if suffix in {".jpg", ".jpeg"}:
            return read_jpeg_size(path)
        if suffix == ".webp" and header.startswith(b"RIFF") and header[8:12] == b"WEBP":
            return read_webp_size(path)
    raise ValueError(f"unsupported or unreadable image format: {path}")


def read_jpeg_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            raise ValueError(f"invalid JPEG: {path}")
        while True:
            marker_start = handle.read(1)
            if marker_start != b"\xff":
                raise ValueError(f"invalid JPEG marker stream: {path}")
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            if marker in {b"\xd8", b"\xd9"}:
                continue
            length_bytes = handle.read(2)
            if len(length_bytes) != 2:
                raise ValueError(f"truncated JPEG: {path}")
            length = struct.unpack(">H", length_bytes)[0]
            if marker in {
                b"\xc0",
                b"\xc1",
                b"\xc2",
                b"\xc3",
                b"\xc5",
                b"\xc6",
                b"\xc7",
                b"\xc9",
                b"\xca",
                b"\xcb",
                b"\xcd",
                b"\xce",
                b"\xcf",
            }:
                data = handle.read(5)
                if len(data) != 5:
                    raise ValueError(f"truncated JPEG SOF segment: {path}")
                height, width = struct.unpack(">HH", data[1:5])
                return width, height
            handle.seek(length - 2, 1)


def read_webp_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 30 or not (data.startswith(b"RIFF") and data[8:12] == b"WEBP"):
        raise ValueError(f"invalid WEBP: {path}")
    chunk = data[12:16]
    if chunk == b"VP8X":
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return width, height
    if chunk == b"VP8 ":
        start = data.find(b"\x9d\x01\x2a")
        if start == -1 or start + 10 > len(data):
            raise ValueError(f"cannot locate VP8 size: {path}")
        width, height = struct.unpack("<HH", data[start + 3 : start + 7])
        return width & 0x3FFF, height & 0x3FFF
    if chunk == b"VP8L":
        if len(data) < 25:
            raise ValueError(f"truncated VP8L image: {path}")
        bits = int.from_bytes(data[21:25], "little")
        width = (bits & 0x3FFF) + 1
        height = ((bits >> 14) & 0x3FFF) + 1
        return width, height
    raise ValueError(f"unsupported WEBP chunk: {path}")


def media_slots(plan: Any) -> list[dict[str, Any]]:
    if isinstance(plan, list):
        slots = plan
    elif isinstance(plan, dict):
        slots = plan.get("media_slots", plan.get("slots"))
    else:
        raise ValueError("media plan must be an object or list")
    if not isinstance(slots, list) or not slots:
        raise ValueError("media plan must contain a non-empty media_slots list")
    for slot in slots:
        if not isinstance(slot, dict):
            raise ValueError("each media slot must be an object")
    return slots


def resolve_asset(site_root: Path, src: str) -> Path:
    if src.startswith(("http://", "https://", "data:")):
        raise ValueError(f"media src must be a local built asset, got remote/data URI: {src}")
    raw = src[1:] if src.startswith("/") else src
    return (site_root / raw).resolve()


def audit_media(site_root: Path, plan: Any, min_scale: float) -> list[str]:
    errors: list[str] = []
    seen: dict[str, list[str]] = {}

    for index, slot in enumerate(media_slots(plan), start=1):
        label = str(slot.get("id") or f"slot-{index}")
        src = slot.get("src")
        source_type = str(slot.get("source_type", "")).lower()
        role = str(slot.get("role", "")).lower()

        for field in ("id", "prompt_id", "section_id", "role", "src", "target_width", "target_height", "aspect_ratio", "fit", "focal_point", "source_type"):
            if slot.get(field) in (None, ""):
                errors.append(f"{label}: missing required field {field}")

        if not isinstance(src, str) or not src:
            continue

        try:
            asset = resolve_asset(site_root, src)
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            continue

        if not asset.is_file():
            errors.append(f"{label}: asset not found: {src}")
            continue

        skip_prominence = source_type in NON_PROMINENT_TYPES or role in NON_PROMINENT_TYPES
        if not skip_prominence and not slot.get("allow_reuse"):
            seen.setdefault(str(asset), []).append(label)

        focal = str(slot.get("focal_point", "")).strip()
        if not skip_prominence and not focal:
            errors.append(f"{label}: missing focal_point for prominent media")

        if source_type == "generated":
            represents_real = bool(
                slot.get("represents_real_person_place_product")
                or slot.get("represents_real_company_place")
                or slot.get("represents_real_person")
                or slot.get("represents_real_product")
            )
            approved = bool(slot.get("user_approved_real_representation"))
            if represents_real and not approved:
                errors.append(
                    f"{label}: generated asset claims exact real-world representation without user approval"
                )

        if asset.suffix.lower() not in RASTER_SUFFIXES:
            if not skip_prominence:
                errors.append(f"{label}: prominent media must be raster, got {asset.suffix or 'no suffix'}")
            continue

        try:
            width, height = read_image_size(asset)
        except Exception as exc:
            errors.append(f"{label}: cannot read image dimensions for {src}: {exc}")
            continue

        try:
            target_width = float(slot.get("target_width"))
            target_height = float(slot.get("target_height"))
        except (TypeError, ValueError):
            errors.append(f"{label}: target_width and target_height must be numeric")
            continue

        if target_width <= 0 or target_height <= 0:
            errors.append(f"{label}: target_width and target_height must be positive")
            continue

        slot_min_scale = float(slot.get("min_scale") or min_scale)
        if not skip_prominence:
            required_width = target_width * slot_min_scale
            required_height = target_height * slot_min_scale
            if width < required_width or height < required_height:
                errors.append(
                    f"{label}: {src} is {width}x{height}, below {slot_min_scale:.2f}x target "
                    f"{int(target_width)}x{int(target_height)}"
                )

        expected_ratio = parse_aspect_ratio(slot.get("aspect_ratio"))
        if expected_ratio:
            actual_ratio = width / height
            mismatch = abs(actual_ratio - expected_ratio) / expected_ratio
            if not skip_prominence and mismatch > 0.45 and str(slot.get("fit")).lower() == "cover":
                errors.append(
                    f"{label}: asset ratio {actual_ratio:.2f} is far from slot ratio {expected_ratio:.2f}; "
                    "create a better slot-specific crop or generated asset"
                )

    for asset, labels in seen.items():
        if len(labels) > 1:
            errors.append(
                f"prominent media reused without allow_reuse: {Path(asset).name} in {', '.join(labels)}"
            )

    return errors


def collect_brand_colors(plan: Any) -> tuple[list[str], list[str]]:
    if not isinstance(plan, dict):
        return [], []
    palette = plan.get("brand_palette") or plan.get("brand_tokens") or {}
    if not isinstance(palette, dict):
        return [], []

    brand: list[str] = []
    allowed: list[str] = []
    for key, value in palette.items():
        target = allowed if "allowed" in str(key).lower() or "exception" in str(key).lower() else brand
        if isinstance(value, str) and value.startswith("#"):
            target.append(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item.startswith("#"):
                    target.append(item)
    return brand, allowed


def scan_files_for_colors(site_root: Path) -> list[tuple[Path, str]]:
    found: list[tuple[Path, str]] = []
    for path in site_root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        if any(part in {"node_modules", "dist", ".git"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in HEX_RE.finditer(text):
            found.append((path, f"#{match.group(1)}"))
    return found


def is_allowed_color(color: str, brand: list[str], allowed: list[str]) -> bool:
    parsed = normalize_hex(color)
    hls = hex_to_hls(color)
    if parsed is None or hls is None:
        return True
    hue, lightness, saturation, alpha = hls
    if alpha < 0.18:
        return True
    if lightness < 0.08 or lightness > 0.94 or saturation < 0.12:
        return True

    allowed_rgba = [normalize_hex(item) for item in [*brand, *allowed]]
    allowed_rgba = [item for item in allowed_rgba if item is not None]
    if any(color_distance(parsed, item) <= 42 for item in allowed_rgba):
        return True

    brand_hues = [hex_to_hls(item) for item in brand]
    brand_hues = [item[0] for item in brand_hues if item is not None and item[2] >= 0.18]
    if brand_hues and any(hue_distance(hue, brand_hue) <= 22 for brand_hue in brand_hues):
        return True

    return False


def audit_colors(site_root: Path, plan: Any) -> list[str]:
    brand, allowed = collect_brand_colors(plan)
    if not brand:
        return ["brand_palette is missing source-backed brand colors; color audit cannot verify cohesion"]

    errors: list[str] = []
    offenders: dict[str, set[str]] = {}
    for path, color in scan_files_for_colors(site_root):
        if not is_allowed_color(color, brand, allowed):
            rel = str(path.relative_to(site_root))
            offenders.setdefault(color.lower(), set()).add(rel)

    for color, files in sorted(offenders.items()):
        shown = ", ".join(sorted(files)[:4])
        suffix = "" if len(files) <= 4 else f", +{len(files) - 4} more"
        errors.append(f"off-brand saturated color {color} in {shown}{suffix}")
    return errors


def main(argv: list[str]) -> int:
    try:
        args = parse_args(argv)
        site_root = resolve_inside_repo(args.site_root, "site root")
        if not site_root.is_dir():
            raise FileNotFoundError(f"site root not found: {site_root}")
        media_plan = resolve_inside_repo(
            args.media_plan or site_root / "lumora-media-plan.json", "media plan"
        )
        plan = load_json(media_plan)

        errors = audit_media(site_root, plan, args.min_scale)
        if not args.no_color_audit:
            errors.extend(audit_colors(site_root, plan))
        if errors:
            for error in errors:
                sys.stderr.write(f"ERROR: {error}\n")
            return 1

    except Exception as exc:
        return fail(str(exc))

    print("Lumora visual asset audit passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
