#!/usr/bin/env python3
"""Render notes/week-N/notes.md to notes/week-N/notes.pdf (images + mermaid included).

Pipeline: markdown -> HTML (relative image paths kept) -> headless Chrome print-to-pdf.
Mermaid is rendered in the page by mermaid.js (cached in .skill-cache/mermaid.min.js,
fetched from jsdelivr on first run).

Usage (from project root):
  .venv/bin/python Skills/nptel-big-data-week/scripts/build_pdf.py --week N
Needs: `markdown` (pip), Google Chrome / Chromium.
"""
from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

try:
    import markdown
except ImportError:  # pragma: no cover
    markdown = None

ROOT = Path(__file__).resolve().parents[3]
MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "google-chrome",
    "chromium",
    "chromium-browser",
    "chrome",
]

CSS = """
@page { size: A4; margin: 14mm 13mm; }
body { font: 10.5pt/1.5 -apple-system, "Helvetica Neue", Arial, sans-serif; color: #1a1a1a; }
h1 { font-size: 21pt; border-bottom: 2px solid #333; padding-bottom: 4px; }
h2 { font-size: 15pt; margin-top: 1.4em; border-bottom: 1px solid #bbb; break-after: avoid; }
h3, h4 { break-after: avoid; }
img { max-width: 100%; max-height: 120mm; display: block; margin: 6px auto; break-inside: avoid; }
table { border-collapse: collapse; margin: 8px 0; break-inside: avoid; font-size: 9.5pt; }
th, td { border: 1px solid #999; padding: 3px 7px; vertical-align: top; }
th { background: #eee; }
code { font: 9pt Menlo, monospace; background: #f3f3f3; padding: 0 3px; border-radius: 3px; }
pre { background: #f6f6f6; padding: 8px; overflow-wrap: anywhere; white-space: pre-wrap; break-inside: avoid; }
pre.mermaid { background: none; text-align: center; white-space: pre; }
pre.mermaid svg { max-width: 100%; height: auto; }
blockquote { border-left: 3px solid #999; margin-left: 0; padding-left: 10px; color: #444; }
details { margin: 6px 0; }
"""


def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if os.path.isabs(c):
            if Path(c).exists():
                return c
        elif shutil.which(c):
            return shutil.which(c)
    return None


def get_mermaid() -> Path:
    cache = ROOT / ".skill-cache" / "mermaid.min.js"
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        print("fetching mermaid.js (one time) ...")
        urllib.request.urlretrieve(MERMAID_URL, cache)
    return cache


def md_to_html(md_text: str, base: Path, mermaid_js: Path | None) -> str:
    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists", "md_in_html"],
    )
    body = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        r'<pre class="mermaid">\1</pre>',
        body,
        flags=re.S,
    )
    script = ""
    if mermaid_js is not None:
        script = (
            f'<script src="{mermaid_js.as_uri()}"></script>'
            '<script>mermaid.initialize({startOnLoad:true,theme:"neutral",'
            'flowchart:{useMaxWidth:true}});</script>'
        )
    return (
        f'<!doctype html><html><head><meta charset="utf-8">'
        f'<base href="{base.as_uri()}/"><style>{CSS}</style></head>'
        f"<body>{body}{script}</body></html>"
    )


def build(week: int, chrome: str) -> Path:
    week_dir = ROOT / "notes" / f"week-{week}"
    md_path = week_dir / "notes.md"
    if not md_path.exists():
        raise SystemExit(f"missing {md_path}")
    md_text = md_path.read_text(encoding="utf-8")
    has_mermaid = "```mermaid" in md_text
    page = md_to_html(md_text, week_dir, get_mermaid() if has_mermaid else None)
    out_pdf = week_dir / "notes.pdf"
    with tempfile.TemporaryDirectory() as tmp:
        html_file = Path(tmp) / "notes.html"
        html_file.write_text(page, encoding="utf-8")
        cmd = [
            chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
            "--allow-file-access-from-files", "--no-pdf-header-footer",
            "--virtual-time-budget=30000",
            f"--user-data-dir={Path(tmp) / 'profile'}",
            f"--print-to-pdf={out_pdf}", html_file.as_uri(),
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=180)
    if not out_pdf.exists() or out_pdf.stat().st_size == 0:
        raise SystemExit("Chrome produced no PDF")
    return out_pdf


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, required=True, choices=range(1, 9))
    args = ap.parse_args()
    if markdown is None:
        print("Need `markdown`. Run: .venv/bin/pip install markdown", file=sys.stderr)
        return 1
    chrome = find_chrome()
    if not chrome:
        print("Need Google Chrome / Chromium installed for PDF rendering.", file=sys.stderr)
        return 1
    out = build(args.week, chrome)
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
