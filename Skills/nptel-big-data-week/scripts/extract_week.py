#!/usr/bin/env python3
"""Extract one week (or one lecture) from Big_Data.pdf using footer page numbers.

Footer numbers are the printed page numbers in the PDF. PDF page index is
footer + 3 (cover image + two index pages).

Writes a cache the agent can read without opening the rest of the book:
  .skill-cache/week-N/manifest.json
  .skill-cache/week-N/lecture-XX.txt
  .skill-cache/week-N/slides/lecture-XX/pNNNN.png
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CURRICULUM = Path(__file__).resolve().parent / "curriculum.json"

try:
    import fitz
except ImportError:
    fitz = None


def footer_to_pdf(footer: int, offset: int) -> int:
    """1-based PDF page number."""
    return footer + offset


def lecture_ranges(week: dict, offset: int, last_content_footer: int) -> list[dict]:
    lectures = week["lectures"]
    out = []
    for i, lec in enumerate(lectures):
        f0 = lec["footer"]
        f1 = lectures[i + 1]["footer"] - 1 if i + 1 < len(lectures) else week["footer_end"]
        f1 = min(f1, last_content_footer)
        out.append(
            {
                "n": lec["n"],
                "title": lec["title"],
                "footer_start": f0,
                "footer_end": f1,
                "pdf_start": footer_to_pdf(f0, offset),
                "pdf_end": footer_to_pdf(f1, offset),
            }
        )
    return out


def extract_text(page) -> str:
    return page.get_text("text") or ""


def looks_like_title_page(text: str) -> bool:
    t = text.strip()
    if "Prof. Rajiv Misra" in t and "Big Data Computing" in t and len(t) < 450:
        return True
    return False


def slide_rects(page) -> list:
    """Real embedded slide photos. Do not use a hardcoded crop — Y position varies."""
    rects = []
    for block in page.get_text("dict").get("blocks", []):
        if block.get("type") != 1:
            continue
        r = fitz.Rect(block["bbox"])
        if r.width < 180 or r.height < 80:
            continue
        rects.append(r)
    return rects


def render_slide(page, rect, zoom: float = 1.7):
    clip = fitz.Rect(rect)
    clip += (-2, -2, 2, 2)
    clip &= page.rect
    return page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=int, required=True, choices=range(1, 9))
    parser.add_argument("--lecture", type=int, default=None, help="Optional lecture number (1-34)")
    parser.add_argument("--pdf", type=str, default=None)
    parser.add_argument("--out", type=str, default=None)
    parser.add_argument("--no-images", action="store_true")
    args = parser.parse_args()

    data = json.loads(CURRICULUM.read_text())
    week = data["weeks"][str(args.week)]
    offset = data["footer_to_pdf_offset"]
    last_footer = data["last_content_footer"]
    ranges = lecture_ranges(week, offset, last_footer)

    if args.lecture is not None:
        ranges = [r for r in ranges if r["n"] == args.lecture]
        if not ranges:
            print(f"Lecture {args.lecture} is not in week {args.week}", file=sys.stderr)
            print("This week has:", [r["n"] for r in lecture_ranges(week, offset, last_footer)], file=sys.stderr)
            return 2

    pdf_path = Path(args.pdf) if args.pdf else ROOT / data["pdf_relative"]
    out_dir = Path(args.out) if args.out else ROOT / ".skill-cache" / f"week-{args.week}"
    out_dir.mkdir(parents=True, exist_ok=True)

    if fitz is None:
        print("Need pymupdf. From the project root run:", file=sys.stderr)
        print("  python3 -m venv .venv && .venv/bin/pip install pymupdf", file=sys.stderr)
        return 1

    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    doc = fitz.open(pdf_path)
    written = []
    for r in ranges:
        # Clamp to document
        pdf_start = max(1, r["pdf_start"])
        pdf_end = min(doc.page_count, r["pdf_end"])
        chunks = [
            f"# Lecture {r['n']}: {r['title']}",
            f"footer_pages: {r['footer_start']}-{r['footer_end']}",
            f"pdf_pages: {pdf_start}-{pdf_end}",
            "",
        ]
        slide_dir = out_dir / "slides" / f"lecture-{r['n']:02d}"
        if not args.no_images:
            if slide_dir.exists():
                shutil.rmtree(slide_dir)
            slide_dir.mkdir(parents=True, exist_ok=True)

        saved_slides = []
        for pdf_page in range(pdf_start, pdf_end + 1):
            page = doc[pdf_page - 1]
            text = extract_text(page)
            chunks.append(f"----- pdf {pdf_page} | footer {pdf_page - offset} -----")
            chunks.append(text.strip())
            chunks.append("")
            if args.no_images or looks_like_title_page(text):
                continue
            rects = slide_rects(page)
            for idx, rect in enumerate(rects):
                pix = render_slide(page, rect)
                suffix = "" if len(rects) == 1 else f"-{idx + 1}"
                img_path = slide_dir / f"p{pdf_page:04d}{suffix}.png"
                pix.save(str(img_path))
                saved_slides.append(
                    {
                        "file": str(img_path.relative_to(out_dir)),
                        "pdf_page": pdf_page,
                        "index": idx,
                        "bbox": [round(rect.x0, 1), round(rect.y0, 1), round(rect.x1, 1), round(rect.y1, 1)],
                    }
                )

        txt_name = f"lecture-{r['n']:02d}.txt"
        (out_dir / txt_name).write_text("\n".join(chunks), encoding="utf-8")
        rec = dict(r)
        rec.update({"text_file": txt_name, "slides": saved_slides, "pdf_start": pdf_start, "pdf_end": pdf_end})
        written.append(rec)
        print(f"lecture {r['n']}: pdf {pdf_start}-{pdf_end} -> {txt_name} ({len(saved_slides)} slides)")

    manifest_path = out_dir / "manifest.json"
    previous = []
    if args.lecture is not None and manifest_path.exists():
        try:
            previous = json.loads(manifest_path.read_text()).get("lectures") or []
        except json.JSONDecodeError:
            previous = []
    merged = {item["n"]: item for item in previous if item.get("n") not in {x["n"] for x in written}}
    for item in written:
        merged[item["n"]] = item
    lectures_out = [merged[k] for k in sorted(merged)]

    manifest = {
        "week": args.week,
        "title": week["title"],
        "footer_start": week["footer_start"],
        "footer_end": week["footer_end"],
        "pdf_start": footer_to_pdf(week["footer_start"], offset),
        "pdf_end": footer_to_pdf(week["footer_end"], offset),
        "lectures": lectures_out,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote {manifest_path}")
    print("CONTEXT LIMIT: only read files in this folder. Do not open other weeks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
