#!/usr/bin/env python3
"""Refresh the compact NameThat UI search index from public structured data."""

from __future__ import annotations

import html as html_lib
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

BASE = "https://namethatui.com"
OUT = Path(__file__).resolve().parent.parent / "references" / "catalog.json"
USER_AGENT = "NameThatUISkill/1.0 (+https://namethatui.com/)"


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def main() -> int:
    sitemap = ET.fromstring(fetch(f"{BASE}/sitemap.xml"))
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = [node.text for node in sitemap.iter(f"{namespace}loc") if node.text]
    entries = []

    for url in urls:
        match = re.search(r"/(web|macos)/([^/?#]+)$", url)
        if not match:
            continue
        page = fetch(url)
        block = re.search(r'<script type="application/ld\+json">(.*?)</script>', page)
        if not block:
            print(f"warning: no structured data at {url}", file=sys.stderr)
            continue
        data = json.loads(html_lib.unescape(block.group(1)))
        entries.append(
            {
                "platform": match.group(1),
                "slug": match.group(2),
                "name": data["name"],
                "aliases": data.get("alternateName", []),
                "url": url,
            }
        )

    entries.sort(key=lambda item: (item["platform"], item["name"].casefold()))
    payload = {
        "source": BASE,
        "refreshed": date.today().isoformat(),
        "entry_count": len(entries),
        "entries": entries,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(entries)} entries to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

