#!/usr/bin/env python3
"""Disabled legacy archetype selector for Lumora."""

from __future__ import annotations

import sys


MESSAGE = (
    "select_lumora_archetypes.py is disabled for Lumora. "
    "Select existing entries from references/motionsites-prompt-library.json "
    "by role, and use load_lumora_prompt.py --id <prompt-id> for exact prompt_text inspection."
)


def main() -> int:
    sys.stderr.write(MESSAGE + "\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
