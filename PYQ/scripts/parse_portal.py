"""Parse NPTEL portal printouts (question + options + 'Accepted Answers:').

Used for: 2019 files (all weeks), and the Week-0 portion of the 2023/2024/2025 files.
Usage: parse_portal.py <pdf> <year> <out.json> [max_pages]
"""
import json
import re
import sys

import fitz

JUNK = re.compile(
    r"^(Score: ?\d+|Powered by|Previous Page|End|Funded by|©.*|Check Answers.*|"
    r"\d+/\d+|https?://\S+|\d+/\d+/\d+, .*|Big Data Computing - .*|\d+ points?|"
    r"The due date.*|As per our records.*|assignment\.|Due (on|date).*|Your last recorded.*|"
    r"Assignment not submitted|Answer Submitted\.?|Your score is.*)$"
)
RESULT = re.compile(r"^(Yes|No), the answer is (correct|incorrect)\.?$")
HEAD = re.compile(r"^(?:Week[- ]?\d+\s*:\s*)?Assignment[- ]?(\d)$")
NUM = re.compile(r"^\d+\)$")


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def blocks_of(doc, max_pages, xmin):
    out = []
    for pn, page in enumerate(doc):
        if max_pages and pn >= max_pages:
            break
        for b in sorted(page.get_text("blocks"), key=lambda b: (round(b[1]), b[0])):
            if b[6] != 0 or b[0] < xmin:
                continue
            out.append((pn + 1, b[0], b[1], b[4]))
    return out


def parse(pdf, year, max_pages=None, xmin=140):
    doc = fitz.open(pdf)
    items = []  # (page, x0, text) one per line group
    week = None
    for pn, x0, y0, text in blocks_of(doc, max_pages, xmin):
        lines = [l for l in text.split("\n")]
        # drop number markers and junk lines
        for i, l in enumerate(lines):
            n = norm(l)
            if not n:
                continue
            if HEAD.match(n):
                items.append(("HEAD", int(HEAD.match(n).group(1)), pn))
                continue
            if NUM.match(n) or JUNK.match(n) or "nptel.iitm.ac.in" in n or "@" in n and "." in n and " " not in n:
                continue
            if n in ("Announcements", "Course", "Ask a Question", "Progress", "FAQ"):
                continue
            if n == "Accepted Answers:":
                items.append(("ACC", pn, x0))
                continue
            if RESULT.match(n):
                items.append(("RES", n, pn))
                continue
            items.append(("TXT", l, x0, pn, i == 0, y0))
    qs = []
    buf = []  # list of blocks: [x0, [lines]]
    state = "Q"
    cur = None
    week = None
    cnt = {}

    def add_line(l, x0, newblock):
        if newblock or not buf:
            buf.append([x0, [norm(l)]])
        else:
            buf[-1][1].append(norm(l))

    for it in items:
        k = it[0]
        if k == "HEAD":
            week = it[1]
            continue
        if k == "RES":
            state = "RES"
            continue
        if k == "ACC":
            state = "ANS"
            cur = {"content": [list(b) for b in buf], "ans": [], "week": week}
            buf.clear()
            qs.append(cur)
            continue
        _, l, x0, pn, first, y0 = it
        if state == "ANS":
            nl = norm(l)
            # answer line iff it matches an option line of the current question
            opts = [norm(" ".join(b[1])) for b in cur["content"]]
            if any(nl == o or (nl and o.startswith(nl)) or (nl and nl in o and len(nl) > 12) for o in opts) and (
                not cur["ans"] or True
            ):
                cur["ans"].append(nl)
                continue
            state = "Q"
        add_line(l, x0, first)
    # split each into stem/options
    res = []
    for q in qs:
        cont = q["content"]
        blocks = [(b[0], norm(" ".join(b[1]))) for b in cont]
        ans = q["ans"]
        # locate answered option blocks
        idxs = []
        for i, (x, t) in enumerate(blocks):
            if any(a == t or t.startswith(a) or (len(a) > 12 and a in t) for a in ans):
                idxs.append(i)
        flag = []
        if not idxs:
            flag.append("answer-not-matched")
            res.append({"year": year, "week": q["week"], "stem": " ".join(t for _, t in blocks), "options": [],
                        "answers_text": ans, "flags": flag})
            continue
        ox = min(blocks[i][0] for i in idxs)
        j = len(blocks)
        while j > 0 and abs(blocks[j - 1][0] - ox) <= 2.5:
            j -= 1
        stem = " ".join(t for _, t in blocks[:j]).strip()
        options = [t for _, t in blocks[j:]]
        res.append({"year": year, "week": q["week"], "stem": stem, "options": options, "answers_text": ans,
                    "flags": flag})
    return res


if __name__ == "__main__":
    pdf, year, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    mp = int(sys.argv[4]) if len(sys.argv) > 4 else None
    r = parse(pdf, year, mp)
    json.dump(r, open(out, "w"), indent=1, ensure_ascii=False)
    print(len(r), "questions;", sum(1 for x in r if x["flags"]), "flagged")
