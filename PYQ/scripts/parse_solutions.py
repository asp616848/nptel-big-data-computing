"""Parse NPTEL 'solution document' style PDFs (2021, 2022, 2023, 2024, 2025 weeks 1-8).

Line based. Question starts must be sequential (1,2,3..) within a week, which keeps
numbered lines inside code/explanations from being mistaken for questions.
Usage: parse_solutions.py <pdf> <year> <out.json> [first_page] [last_page]
"""
import json
import re
import sys

import fitz

ZW = dict.fromkeys(map(ord, "​‌‍﻿"), None)

WEEK_RES = [
    re.compile(r"\(Week-?\s*(\d)\)"),
    re.compile(r"^Week\s*-?\s*(\d)\s*(?:[:\-].*)?$", re.I),
    re.compile(r"^Assignme\w*\s*-?\s*(\d)\s*$", re.I),
]
QSTART = re.compile(r"^(?:Q\.?\s*(\d{1,2})\s*[\.\):]?|(\d{1,2})\s*[\.\)])\s*(.*)$")
OPT = re.compile(r"^\(?([A-Ha-h])[\.\)]\s+(.*)$|^\(?([A-Ha-h])[\.\)]$")
ANS = re.compile(
    r"^(?:Correct\s+Answer|Answer|Ans|Solution|The correct answer is)\s*[:\-]?\s*(.*)$", re.I
)
EXPL = re.compile(r"^(?:Explanation|Detailed Solution)\s*[:\-]?\s*(.*)$", re.I)
JUNKL = re.compile(
    r"^(\d+/\d+|https?://\S+|\d+/\d+/\d+.*|Big Data Computing - .*|Quiz Assignment.*Solutions.*|"
    r"_{5,}|NPTEL.*|Assignment\s*\d.*Solution.*)$"
)


def clean(s):
    return re.sub(r"\s+", " ", s.translate(ZW).replace("\xa0", " ")).strip()


def load_lines(pdf, first=None, last=None):
    doc = fitz.open(pdf)
    out = []
    for pn, page in enumerate(doc, 1):
        if first and pn < first:
            continue
        if last and pn > last:
            break
        for raw in page.get_text().split("\n"):
            out.append((pn, raw))
    # merge lone bullet glyph lines with the following line
    merged = []
    i = 0
    while i < len(out):
        pn, raw = out[i]
        t = clean(raw)
        if t in ("•", "●", "○", "▪", "◦", "o", "-") and i + 1 < len(out):
            merged.append((pn, "• " + clean(out[i + 1][1])))
            i += 2
            continue
        merged.append((pn, raw))
        i += 1
    return merged


def parse(pdf, year, first=None, last=None):
    lines = load_lines(pdf, first, last)
    week = None
    qonly = sum(1 for _, r in lines if re.match(r"^\s*Q\.?\s*\d", r)) >= 20
    qs = []
    cur = None
    last_no = 0
    mode = None  # stem / opt / ans / expl
    for pn, raw in lines:
        t = clean(raw)
        if not t:
            continue
        wk = None
        for r in WEEK_RES:
            m = r.search(t) if r.pattern.startswith("\\(") else r.match(t)
            if m:
                wk = int(m.group(1))
                break
        if wk is not None and not t.endswith("?") and (len(t) < 40 or "Solutions" in t):
            week = wk
            last_no = 0
            cur = None
            continue
        if JUNKL.match(t):
            continue
        m = QSTART.match(t)
        if m and qonly and not re.match(r"^Q", t):
            m = None
        if m and int(m.group(1) or m.group(2)) == last_no + 1 and not (mode in ("opt",) and OPT.match(t)):
            # avoid treating "1." option-ish lines; real question starts only
            last_no += 1
            cur = {"year": year, "week": week, "qno": last_no, "page": pn, "stem": [m.group(3)], "opts": [],
                   "ans": [], "expl": [], "bullets": [], "raw": [t]}
            qs.append(cur)
            mode = "stem"
            continue
        if cur is None:
            continue
        cur["raw"].append(t)
        a = ANS.match(t)
        if a and mode in ("stem", "opt", "ans") and (cur["opts"] or cur["bullets"] or True):
            mode = "ans"
            if a.group(1):
                cur["ans"].append(a.group(1))
            continue
        e = EXPL.match(t)
        if e and mode in ("ans", "opt", "stem"):
            mode = "expl"
            if e.group(1):
                cur["expl"].append(e.group(1))
            continue
        if mode == "expl":
            cur["expl"].append(t)
            continue
        if mode == "ans":
            # continuation of answer text (wrapped) until blank/explanation
            cur["ans"].append(t)
            continue
        if t.startswith("• "):
            mode = "opt"
            cur["bullets"].append([t[2:]])
            continue
        o = OPT.match(t)
        if o and (mode in ("stem", "opt")):
            letter = (o.group(1) or o.group(3)).upper()
            exp = chr(ord("A") + len(cur["opts"]))
            if letter == exp:
                mode = "opt"
                cur["opts"].append([letter, [o.group(2) or ""]])
                continue
        if mode == "opt":
            if cur["bullets"]:
                cur["bullets"][-1].append(t)
            elif cur["opts"]:
                cur["opts"][-1][1].append(t)
            else:
                cur["stem"].append(t)
        else:
            cur["stem"].append(t)
    return finish(qs)


def finish(qs):
    res = []
    for q in qs:
        flags = []
        if q["bullets"] and not q["opts"]:
            opts = [clean(" ".join(b)) for b in q["bullets"]]
        else:
            opts = [clean(" ".join(o[1])) for o in q["opts"]]
        stem = clean(" ".join(q["stem"]))
        ans_raw = clean(" ".join(q["ans"]))
        letters = []
        if opts:
            # answer may be: "C) text", "C", "(c) text", "B. text", "A, C", or bare text
            am = re.match(r"^\(?([A-Ha-h])(?:[\.\)]|\b)\s*(.*)$", ans_raw)
            multi = re.match(r"^((?:[A-Ha-h]\s*[,&and ]+\s*)+[A-Ha-h])\b", ans_raw)
            if multi:
                letters = sorted(set(re.findall(r"[A-Ha-h]", multi.group(1).upper())))
            elif am and ord(am.group(1).upper()) - 65 < len(opts) and (
                am.group(2) == "" or opts[ord(am.group(1).upper()) - 65].lower().startswith(am.group(2).lower()[:15])
                or len(am.group(2)) > 0
            ):
                letters = [am.group(1).upper()]
            else:
                for i, o in enumerate(opts):
                    if ans_raw and clean(o).lower() == ans_raw.lower():
                        letters.append(chr(65 + i))
                if not letters:
                    for i, o in enumerate(opts):
                        if ans_raw and (o.lower().startswith(ans_raw.lower()[:25]) or ans_raw.lower().startswith(o.lower()[:25])):
                            letters.append(chr(65 + i))
                            break
            if not letters:
                ex = " ".join(q["expl"])
                inf = re.findall(r"\b([A-H])\s+is\s+correct", ex)
                if inf:
                    letters = sorted(set(inf))
                    flags.append("answer-from-explanation")
            if not letters:
                flags.append("answer-unresolved")
        else:
            flags.append("no-options")
        if len(opts) not in (2, 3, 4, 5, 6):
            flags.append("odd-option-count")
        res.append({
            "year": q["year"], "week": q["week"], "qno": q["qno"], "page": q["page"], "stem": stem,
            "options": opts, "answer_letters": letters, "answer_raw": ans_raw,
            "explanation": clean(" ".join(q["expl"])), "flags": flags, "raw": q["raw"],
        })
    return res


if __name__ == "__main__":
    pdf, year, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    fp = int(sys.argv[4]) if len(sys.argv) > 4 else None
    lp = int(sys.argv[5]) if len(sys.argv) > 5 else None
    r = parse(pdf, year, fp, lp)
    json.dump(r, open(out, "w"), indent=1, ensure_ascii=False)
    from collections import Counter
    print(len(r), "questions; per week:", dict(sorted(Counter(x["week"] for x in r).items(), key=lambda kv: (kv[0] is None, kv[0]))))
    print("flagged:", sum(1 for x in r if x["flags"]))
