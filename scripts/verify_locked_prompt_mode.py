#!/usr/bin/env python3
"""Verify Lumora JSON prompt_text loading guarantees."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOADER = ROOT / "scripts" / "load_lumora_prompt.py"


def run_loader(library: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        [sys.executable, str(LOADER), "--library", str(library), *args],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix=".lumora-json-prompt-", dir=ROOT) as tmp:
        tmp_root = Path(tmp)
        library = tmp_root / "motionsites-prompt-library.json"
        prompt_text = (
            "# Stored Prompt\r\n"
            "\r\n"
            "Hero: {{COMPANY_NAME}}\t  \r\n"
            "  Preserve indentation and trailing spaces.  \n"
            "Final line without added wrapper"
        )
        other_text = "# Other Prompt\nThis must never be combined.\n"
        library.write_text(
            json.dumps(
                {
                    "prompts": [
                        {"id": "fixture", "title": "Fixture", "prompt_text": prompt_text},
                        {"id": "other", "title": "Other", "prompt_text": other_text},
                        {"id": "empty", "title": "Empty"},
                    ]
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        before_bytes = library.read_bytes()
        expected_bytes = prompt_text.encode("utf-8")
        expected_hash = hashlib.sha256(expected_bytes).hexdigest()

        loaded = run_loader(library, "--id", "fixture", "--sha256")
        require(loaded.returncode == 0, loaded.stderr.decode("utf-8", errors="replace"))
        require(loaded.stdout == expected_bytes, "prompt_text was not loaded byte-for-byte")
        require(
            loaded.stderr == f"SHA256:{expected_hash}\n".encode(),
            "SHA256 hash was missing or incorrect",
        )
        require(loaded.stdout == expected_bytes, "stdout contains wrapper text or changed bytes")
        require(b"{{COMPANY_NAME}}" in loaded.stdout, "placeholder was replaced")
        require(b"\r\n" in loaded.stdout and b"\t  \r\n" in loaded.stdout, "linebreaks or whitespace changed")
        require(other_text.encode("utf-8") not in loaded.stdout, "multiple prompts were combined")

        duplicate_id = run_loader(library, "--id", "fixture", "--id", "other")
        require(duplicate_id.returncode != 0, "multiple --id values were accepted")
        require(duplicate_id.stdout == b"", "multiple --id failure wrote to stdout")

        combined_id = run_loader(library, "--id", "fixture,other")
        require(combined_id.returncode != 0, "comma-combined id was accepted")
        require(combined_id.stdout == b"", "comma-combined id failure wrote to stdout")

        missing_text = run_loader(library, "--id", "empty")
        require(missing_text.returncode != 0, "entry without prompt_text was accepted")
        require(missing_text.stdout == b"", "missing prompt_text failure wrote to stdout")

        after_bytes = library.read_bytes()
        require(after_bytes == before_bytes, "prompt library was modified")

    print("Lumora JSON prompt_text verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
