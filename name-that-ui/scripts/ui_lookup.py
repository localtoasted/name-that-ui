#!/usr/bin/env python3
"""Fuzzy-search the bundled NameThat UI catalog without dependencies."""

from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "references" / "catalog.json"
STOP = {"a", "an", "and", "at", "for", "in", "is", "it", "of", "on", "that", "the", "this", "to", "with"}


def tokens(value: str) -> set[str]:
    return {word for word in re.findall(r"[a-z0-9]+", value.casefold()) if word not in STOP}


def score(query: str, entry: dict) -> float:
    choices = [entry["name"], entry["slug"].replace("-", " "), *entry.get("aliases", [])]
    q_tokens = tokens(query)
    best = 0.0
    for choice in choices:
        c_tokens = tokens(choice)
        overlap = len(q_tokens & c_tokens) / max(1, len(q_tokens | c_tokens))
        sequence = difflib.SequenceMatcher(None, query.casefold(), choice.casefold()).ratio()
        phrase_bonus = 0.25 if query.casefold() in choice.casefold() or choice.casefold() in query.casefold() else 0.0
        best = max(best, overlap * 0.65 + sequence * 0.35 + phrase_bonus)
    return round(min(1.0, best), 4)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="plain-English UI description or component name")
    parser.add_argument("--platform", choices=("web", "macos"))
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    candidates = [entry for entry in catalog["entries"] if not args.platform or entry["platform"] == args.platform]
    results = []
    for entry in candidates:
        item = dict(entry)
        item["score"] = score(args.query, entry)
        results.append(item)
    results.sort(key=lambda item: (-item["score"], item["name"].casefold()))
    results = results[: max(1, args.limit)]

    if args.as_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0

    for index, item in enumerate(results, 1):
        print(f'{index}. {item["name"]} [{item["platform"]}]  score={item["score"]:.3f}')
        if item.get("aliases"):
            print(f'   aliases: {", ".join(item["aliases"][:6])}')
        print(f'   {item["url"]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
