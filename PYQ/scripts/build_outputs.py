"""questions.json -> index.html (single offline file) and bank.md (printable)."""
import json, os
HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..")
Q = json.load(open(os.path.join(ROOT, "questions.json")))

data = json.dumps(Q, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = open(os.path.join(HERE, "template.html")).read().replace("/*DATA*/", data)
open(os.path.join(ROOT, "index.html"), "w").write(html)

W = {0: "Prerequisites", 1: "Introduction to Big Data", 2: "Hadoop / HDFS / MapReduce", 3: "Spark & key-value stores",
     4: "Storage: CAP, Cassandra, ZooKeeper", 5: "Streaming: HBase, Kafka, Spark Streaming", 6: "ML basics",
     7: "ML with Spark: trees & ensembles", 8: "Graph processing"}
out = ["# Big Data Computing: Previous-Year Question Bank", "",
       f"{len(Q)} unique questions from NPTEL assignments 2019, 2021-2025 (repeats merged; `asked Nx` shows how often one came up). Open `index.html` for filters and practice mode.",
       "Answers marked `*` were not in the source key and were solved or inferred (see flags in the HTML).", ""]
cur = None
for q in Q:
    if q["week"] != cur:
        cur = q["week"]
        out += [f"## Week {q['week']} · {W[q['week']]}", ""]
    star = "*" if any(f in q["flags"] for f in ("answer-solved", "answer-from-2023-twin", "answer-inferred-from-explanation", "answer-from-explanation")) else ""
    seen = ", ".join(f"{a['year']} W{a['week']}" for a in q["appearances"])
    out.append(f"**{q['id']}** ({q['type']}, asked {q['repeat']}x: {seen}) {q['question']}")
    out.append("")
    for im in q.get("images", []):
        out.append(f"![figure]({im})")
        out.append("")
    for o in q["options"]:
        out.append(f"- {o['k']}. {o['text']}")
    out.append("")
    out.append(f"**Answer{star}:** {', '.join(q['answer'])}" + "")
    if q["explanation"]:
        out.append(f"\n> {q['explanation']}")
    out.append("")
open(os.path.join(ROOT, "bank.md"), "w").write("\n".join(out))
print("index.html", round(len(html) / 1024), "KB; bank.md", len(out), "lines")
