"""Parse this repo's own notes/week-N/assignment.md files (2026 session) into draft JSON.
Usage: parse_assignments.py <out.json>   (run from the repo root)
"""
import glob, json, re, sys

def clean(s):
    s = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()

rows = []
for path in sorted(glob.glob("notes/week-*/assignment.md")):
    week = int(re.search(r"week-(\d+)", path).group(1))
    text = open(path).read()
    head = text.split("\n## Q", 1)[0]
    solved = bool(re.search(r"No `?Accepted Answers`? in the paste|no accepted answers shown", head, re.I))
    for blk in re.split(r"\n(?=## Q\d+)", text)[1:]:
        m = re.match(r"## Q(\d+)", blk)
        qno = int(m.group(1))
        body = blk.split("\n---", 1)[0]
        qtxt = re.search(r"\*\*Question\*\*\s*\n(.*?)\n\*\*Options\*\*", body, re.S).group(1)
        opts_txt = re.search(r"\*\*Options\*\*\s*\n(.*?)\n\*\*Answer:\*\*", body, re.S).group(1)
        opts = []
        for line in opts_txt.split("\n"):
            mo = re.match(r"^- ([a-h])\)\s*(.*)$", line.strip())
            if mo:
                opts.append(mo.group(2))
            elif line.strip() and opts:
                opts[-1] += " " + line.strip()
        ans = re.search(r"\*\*Answer:\*\*\s*\*\*([a-h](?:\s*(?:,|and)\s*[a-h])*)\b", body)
        letters = sorted(set(re.findall(r"[a-h]", ans.group(1)))) if ans else []
        why = re.search(r"\*\*Why:\*\*\s*(.*?)(?=\n\*\*Trap:\*\*|\Z)", body, re.S)
        trap = re.search(r"\*\*Trap:\*\*\s*(.*)", body, re.S)
        expl = clean(why.group(1)) if why else ""
        if trap:
            expl += " Trap: " + clean(trap.group(1))
        rows.append({
            "year": 2026, "week": week, "qno": qno, "page": None, "path": path,
            "stem": clean(qtxt), "options": [clean(o) for o in opts],
            "answer_letters": [l.upper() for l in letters], "answer_raw": ans.group(1) if ans else "",
            "explanation": expl, "flags": ["answer-solved"] if solved else [],
        })
json.dump(rows, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
print(len(rows), "questions;", sum(1 for r in rows if not r["answer_letters"] or len(r["options"]) < 2), "problems")
