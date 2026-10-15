"""2024 doc has no uniform answer line; infer letters from the explanation text."""
import json, re, sys
def letters_from(raw_lines, n):
    txt = "\n".join(raw_lines)
    found = []
    # "Option b: ... - Correct" / "option c: 3 - Correct"
    for m in re.finditer(r"[Oo]ption\s*([A-Da-d])\b[^\n]*", txt):
        seg = m.group(0)
        nxt = txt[m.end():m.end() + 40]
        if re.search(r"(?<![Ii]n)\b[Cc]orrect\b", seg + nxt.split("Option")[0][:40]) and not re.search(r"[Ii]ncorrect", seg + nxt[:15]):
            found.append(m.group(1).upper())
    for m in re.finditer(r"^\(?([A-Da-d])[\.\)]?\s*[:\-–]?\s*(Correct|correct)\b", txt, re.M):
        found.append(m.group(1).upper())
    for m in re.finditer(r"^\(?([A-Da-d])[\.\)]\s*Correct\b", txt, re.M):
        found.append(m.group(1).upper())
    m = re.search(r"correct answer is:?\s*\(?([A-Da-d])\b", txt)
    if m: found.append(m.group(1).upper())
    return sorted(set(found))
if __name__ == "__main__":
    f = sys.argv[1]
    r = json.load(open(f))
    for x in r:
        L = letters_from(x["raw"], len(x["options"]))
        x["resolved"] = L
    json.dump(r, open(f, "w"), indent=1, ensure_ascii=False)
    ok = [x for x in r if len(x["resolved"]) == 1]
    print(len(ok), "of", len(r), "resolved uniquely")
