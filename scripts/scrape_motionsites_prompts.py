#!/usr/bin/env python3
"""Scrape MotionSites prompt metadata and prompt bodies into Lumora.

This maintains the bundled licensed MotionSites prompt library for Lumora.
It uses the same public Supabase metadata table and get-prompt Edge Function
that the MotionSites web app uses. Premium prompt bodies require an
authenticated MotionSites access token.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUPABASE_URL = "https://xgdzyqfalbibzelpdpvr.supabase.co"
ANON_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhnZHp5cWZhbGJpYnplbHBkcHZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE4MzUwMDYsImV4cCI6MjA4NzQxMTAwNn0."
    "u8lH5Y14xx2WxrNEBp8ngkJlijIYHJASq_gOzTaINZY"
)


def request_json(
    method: str,
    url: str,
    *,
    token: str | None = None,
    body: dict[str, Any] | None = None,
    timeout: int = 60,
) -> Any:
    headers = {
        "apikey": ANON_KEY,
        "Authorization": f"Bearer {token or ANON_KEY}",
        "Accept": "application/json",
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        return {
            "_http_error": exc.code,
            "_details": details,
        }


def fetch_metadata() -> list[dict[str, Any]]:
    query = urllib.parse.urlencode(
        {
            "select": "id,title,category,sort_order,type,types,created_at,page_type,row_span,is_free,image_preview_url,video_preview_url",
            "order": "sort_order.asc",
        }
    )
    data = request_json("GET", f"{SUPABASE_URL}/rest/v1/prompts?{query}")
    if not isinstance(data, list):
        raise RuntimeError(f"Could not fetch prompt metadata: {data!r}")
    return data


def fetch_prompt_body(prompt_id: str, token: str | None) -> dict[str, Any]:
    data = request_json(
        "POST",
        f"{SUPABASE_URL}/functions/v1/get-prompt",
        token=token,
        body={"prompt_id": prompt_id},
    )
    if not isinstance(data, dict):
        return {"status": "error", "error": f"Unexpected response: {data!r}"}
    if data.get("_http_error"):
        return {"status": "error", "error": data}
    if data.get("prompt_text"):
        result = {
            "status": "ok",
            "prompt_text": data.get("prompt_text"),
        }
        if isinstance(data.get("sections"), list):
            result["sections"] = data["sections"]
        if isinstance(data.get("section_names"), list):
            result["section_names"] = data["section_names"]
        return result
    code = data.get("code") or "missing"
    return {"status": str(code), "response": data}


def load_existing(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"prompts": []}
    return json.loads(path.read_text(encoding="utf-8"))


def merge_records(existing: dict[str, Any], metadata: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for item in existing.get("prompts", []):
        if isinstance(item, dict) and item.get("id"):
            records[str(item["id"])] = item
    for item in metadata:
        records.setdefault(str(item["id"]), {})
        records[str(item["id"])].update({"metadata": item, "id": item["id"], "title": item.get("title")})
    return records


def parse_args(argv: list[str]) -> argparse.Namespace:
    default_output = Path(__file__).resolve().parents[1] / "references" / "motionsites-prompt-library.json"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=default_output)
    parser.add_argument("--token", default=os.environ.get("MOTIONSITES_ACCESS_TOKEN"))
    parser.add_argument("--only-missing", action="store_true", help="Do not refetch records that already have prompt_text.")
    parser.add_argument("--limit", type=int, default=0, help="Limit prompt fetch count for testing.")
    parser.add_argument("--sleep", type=float, default=0.05, help="Seconds between prompt-body requests.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    metadata = fetch_metadata()
    existing = load_existing(args.output)
    records = merge_records(existing, metadata)

    ids = [str(item["id"]) for item in metadata]
    if args.only_missing:
        ids = [prompt_id for prompt_id in ids if not records.get(prompt_id, {}).get("prompt_text")]
    if args.limit > 0:
        ids = ids[: args.limit]

    counts: dict[str, int] = {}
    fetched = 0
    for index, prompt_id in enumerate(ids, start=1):
        body = fetch_prompt_body(prompt_id, args.token)
        status = body.pop("status", "error")
        counts[status] = counts.get(status, 0) + 1
        record = records[prompt_id]
        record["fetch_status"] = status
        record["fetched_at"] = datetime.now(timezone.utc).isoformat()
        if status == "ok":
            record.update(body)
        else:
            record["fetch_error"] = body
        fetched += 1
        if fetched % 25 == 0 or fetched == len(ids):
            print(f"Fetched {fetched}/{len(ids)} prompt bodies...", flush=True)
        if args.sleep:
            time.sleep(args.sleep)

    output = {
        "source": "MotionSites bundled licensed prompt library",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "metadata_count": len(metadata),
        "body_fetch_count": fetched,
        "counts": counts,
        "prompts": [records[prompt_id] for prompt_id in sorted(records, key=lambda key: (records[key].get("metadata", {}).get("sort_order") is None, records[key].get("metadata", {}).get("sort_order", 999999), records[key].get("title") or key))],
    }
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({"output": str(args.output), "metadata_count": len(metadata), "body_fetch_count": fetched, "counts": counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
