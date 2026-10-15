"""Sanity checks on PYQ/questions.json. Exit 1 if hard errors."""
import json, os, sys, collections
q = json.load(open(os.path.join(os.path.dirname(__file__), "..", "questions.json")))
err, warn = [], []
ids = collections.Counter(x["id"] for x in q)
for x in q:
    i = x["id"]
    if ids[i] > 1: err.append((i, "duplicate id"))
    if not x["question"].strip(): err.append((i, "empty question"))
    if len(x["options"]) < 2: warn.append((i, f"{len(x['options'])} options"))
    if not x["answer"]: err.append((i, "no answer"))
    ks = {o["k"] for o in x["options"]}
    if any(a not in ks for a in x["answer"]): err.append((i, "answer not in options"))
    if len(x["question"]) > 900: warn.append((i, "very long stem"))
    if any(len(o["text"]) > 250 for o in x["options"]): warn.append((i, "very long option"))
    if any(len(o["text"]) == 0 for o in x["options"]): err.append((i, "empty option"))
print("questions", len(q), "| errors", len(err), "| warnings", len(warn))
for e in err: print("ERR ", *e)
for w in warn: print("WARN", *w)
print("by year/week:")
c = collections.Counter((x["year"], x["week"]) for x in q)
for y in sorted({k[0] for k in c}):
    print(" ", y, " ".join(f"W{w}:{c[(y,w)]}" for w in range(9) if c[(y, w)]))
sys.exit(1 if err else 0)
