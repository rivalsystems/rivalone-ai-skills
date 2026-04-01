#!/usr/bin/env python3
"""Validate skills/catalog/catalog.json against files on disk. Stdlib only."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = REPO_ROOT / "skills" / "catalog"
INDEX_PATH = CATALOG_DIR / "catalog.json"

REQUIRED_IDS = frozenset(
    {"auth-basics", "connection", "market-data", "orders", "errors-troubleshooting"}
)


def main() -> int:
    if not INDEX_PATH.is_file():
        print(f"error: missing {INDEX_PATH}", file=sys.stderr)
        return 1

    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    bundles = data.get("bundles")
    if not isinstance(bundles, list):
        print("error: catalog.json: 'bundles' must be a list", file=sys.stderr)
        return 1

    seen: set[str] = set()
    errors = 0

    for i, b in enumerate(bundles):
        if not isinstance(b, dict):
            print(f"error: bundles[{i}] must be an object", file=sys.stderr)
            errors += 1
            continue
        bid = b.get("id")
        path = b.get("path")
        if not isinstance(bid, str) or not bid.strip():
            print(f"error: bundles[{i}]: missing string id", file=sys.stderr)
            errors += 1
            continue
        if bid in seen:
            print(f"error: duplicate bundle id {bid!r}", file=sys.stderr)
            errors += 1
        seen.add(bid)
        if not isinstance(path, str) or not path.strip():
            print(f"error: bundle {bid!r}: missing path", file=sys.stderr)
            errors += 1
            continue
        fpath = (CATALOG_DIR / path).resolve()
        if not str(fpath).startswith(str(CATALOG_DIR.resolve())):
            print(f"error: bundle {bid!r}: path escapes catalog dir", file=sys.stderr)
            errors += 1
            continue
        if not fpath.is_file():
            print(f"error: bundle {bid!r}: missing file {path}", file=sys.stderr)
            errors += 1

    missing_ids = REQUIRED_IDS - seen
    if missing_ids:
        for mid in sorted(missing_ids):
            print(f"error: required bundle id missing: {mid}", file=sys.stderr)
        errors += len(missing_ids)

    if errors:
        print(f"validate_catalog: {errors} error(s)", file=sys.stderr)
        return 1

    print(f"validate_catalog: ok ({len(bundles)} bundles)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
