"""Assemble PYQ/questions.json from the per-file parser drafts + manual overrides.

Run order (see PYQ/README.md):
  parse_portal.py / parse_solutions.py / resolve_2024.py  -> drafts in $DRAFTS
  build_bank.py                                           -> PYQ/questions.json
  build_outputs.py                                        -> PYQ/index.html, PYQ/bank.md
"""
import difflib
import json
import os
import re
import sys

DRAFTS = os.environ.get("PYQ_DRAFTS", "/tmp/pyq_drafts")
OUT = os.path.join(os.path.dirname(__file__), "..", "questions.json")

SRC = {
    "2019a": "2019_A-0-2,5-8_solu.pdf",
    "2019b": "2019_A-4.pdf",
    "2021": "2021_A-0 to 8_solu.pdf",
    "2022": "2022_A-1 to 8_solu.pdf",
    "2023": "2023_A-0 to 8_solu.pdf",
    "2024": "2024_A-0 to 8_solu.pdf",
    "2025": "2025_A-0 to 8_solu.pdf",
}


def norm(s):
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()


def key(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def load(name):
    return json.load(open(os.path.join(DRAFTS, name + ".json")))


# ---------------------------------------------------------------- 2019 portal fixes
TF = ["True", "False"]
STMT4 = ["Only statement 1 is true", "Only statement 2 is true", "Both statements are true", "Both statements are false"]


def fix_2019a(r):
    """Patch questions the printed PDF cut at page breaks. Index = position in the parser draft."""
    P = {}
    P[0] = dict(stem="Which of the following is a characteristic of Big Data?", options=r[0]["options"][1:])
    P[2] = dict(stem="The following three conditions must be satisfied to solve the critical section problem ____________",
                options=["Mutual exclusion, progress and bounded waiting", "Mutual exclusion only", "Progress only", "All of the mentioned"],
                answers_text=["All of the mentioned"], flags=["options-reconstructed"])
    P[3] = dict(stem="Mutual exclusion implies that :",
                options=[
                    "If a process is executing in its critical section, then no other process must be executing in their critical sections",
                    "If a process is executing in its critical section, then other processes must be executing in their critical sections",
                    "If a process is executing in its critical section, then all the resources of the system must be blocked until it finishes execution",
                    "None of the mentioned"],
                answers_text=["If a process is executing in its critical section, then no other process must be executing in their critical sections"])
    P[4] = dict(stem="In the memory hierarchy, as the speed of operation increases the memory size also increases.", options=TF,
                answers_text=["False"])
    P[9] = dict(options=STMT4, answers_text=["Both statements are false"], flags=["options-reconstructed"])
    P[10] = dict(stem="What are the main components of Hadoop Ecosystem?")
    P[24] = dict(stem="Point out the correct statement in context of YARN:",
                 options=["YARN extends the power of Hadoop to incumbent and new technologies found within the data center",
                          "YARN is highly scalable", "YARN enhances a Hadoop compute cluster in many ways", "All of the mentioned"])
    P[32] = dict(options=["As many filesystems as the number of region servers", "One filesystem per column family",
                          "A single filesystem available to all region servers", "One filesystem per table."],
                 answers_text=["A single filesystem available to all region servers"], flags=["options-from-2021-twin"])
    P[39] = dict(stem="Identify the correct statement in context of Regressive model of Machine Learning.",
                 options=["Regressive model predicts a numeric value instead of category",
                          "Regressive model organizes similar item in your dataset into groups",
                          "Regressive model comes up with a set of rules to capture associations between items or events",
                          "None of the Mentioned"],
                 answers_text=["Regressive model predicts a numeric value instead of category"])
    P[42] = dict(flags=["has-figure"])
    P[49] = dict(flags=["has-figure"])
    P[52] = dict(stem="Boosting any algorithm takes into consideration the weak learners. Which of the following is the main reason behind using weak learners? Reason I - To prevent overfitting. Reason II - To prevent underfitting.",
                 options=["Both the Reasons", "Reason I", "Reason II", "None of the reasons"], answers_text=["Reason I"])
    P[57] = dict(stem="What is the PageRank score of vertex B after the second iteration? (Without damping factor) Hint: the basic PageRank formula is PR(t+1)(u) = sum over v of PR(t)(v) / C(v), where PR(t+1)(u) is the page rank of node u under consideration, PR(t)(v) is the previous page rank of node v pointing to node u, and C(v) is the outgoing degree of vertex v.",
                 options=["1/6", "1.5/12", "2.5/12", "1/3"], answers_text=["1/6"], flags=["stem-restored-from-2021-twin"])
    P[38] = dict(
        stem="Consider the following dataset Customers (Name, Date, AmountSpent): Alice 2016-05-01 50; Bob 2016-05-04 29; Bob 2016-05-01 25; Alice 2016-05-04 55; Alice 2016-05-03 45; Bob 2016-05-06 27. Using the Customers table calculate the moving average for the following pseudo code using spark streaming fundamentals: val wSpec1 = Window.partitionBy(\"name\").orderBy(\"date\").rowsBetween(-1, 1); customers.withColumn(\"movingAvg\", avg(customers(\"amountSpent\")).over(wSpec1)).show()",
        options=["MovingAvg column (rows in the order Alice 05-01, Bob 05-04, Bob 05-01, Alice 05-04, Alice 05-03, Bob 05-06): 50, 29, 54, 105, 150, 81",
                 "MovingAvg column (same row order as option A): 47.5, 27, 27, 50, 50, 28",
                 "MovingAvg column holds the previous row's amount: Alice 05-01 Null, 05-03 50, 05-04 45; Bob 05-01 Null, 05-04 25, 05-06 29",
                 "(option D is a table image that is cut off in the source PDF)"],
        answers_text=["MovingAvg column (same row order as option A): 47.5, 27, 27, 50, 50, 28"],
        flags=["table-options-reconstructed", "answer-solved"])
    DROP = {21}  # stem / options / answer lost at the page break in the source PDF
    out = []
    for i, x in enumerate(r):
        if i in DROP:
            continue
        x = dict(x)
        x.update(P.get(i, {}))
        if not x["options"] and x["stem"].rstrip().endswith("True False"):
            x["stem"] = x["stem"].rstrip()[: -len("True False")].strip()
            x["options"] = TF
        out.append(x)
    return out


def tf_fix(r):
    for x in r:
        if not x["options"] and x["stem"].rstrip().endswith("True False"):
            x["stem"] = x["stem"].rstrip()[: -len("True False")].strip()
            x["options"] = TF
    return r


IMAGES = {
    "2019-W6-Q4": ["confusion-matrix.png"], "2021-W6-Q7": ["confusion-matrix.png"], "2022-W6-Q5": ["confusion-matrix.png"],
    "2019-W8-Q3": ["pagerank-graph.png"], "2021-W8-Q8": ["pagerank-graph.png"], "2022-W8-Q4": ["pagerank-graph.png"],
    "2019-W7-Q3": ["attribute-table.png"], "2019-W4-Q4": ["temperature-table.png"],
}

OVERRIDES = {
    # source accepted-answer is the 4-line query of option B (same as the 2021/2022 twin)
    "2019-W4-Q4": dict(answer=["B"]),
    "2021-W5-Q11": dict(
        question="Consider the following dataset Customers (Name, Date, AmountSpent in Rs.): Alice 2020-05-01 50; Bob 2020-05-04 29; Bob 2020-05-01 25; Alice 2020-05-04 55; Alice 2020-05-03 45; Bob 2020-05-06 27. Using the following pseudo code, find the rank of each customer visiting the supermarket: val wSpec3 = Window.partitionBy(\"name\").orderBy(\"date\"); customers.withColumn(\"rank\", rank().over(wSpec3)).show()",
        options=[
            "Rank column (rows in the order Alice 05-01, Bob 05-04, Bob 05-01, Alice 05-04, Alice 05-03, Bob 05-06): 1, 1, 1, 2, 2, 2",
            "Rank column holds the previous visit's amount instead: Alice 05-01 Null, 05-03 50, 05-04 45; Bob 05-01 Null, 05-04 25, 05-06 29",
            "Rank column (same row order as option A): 3, 3, 2, 2, 2, 1",
            "Alice 05-01 = 1, 05-03 = 2, 05-04 = 3; Bob 05-01 = 1, 05-04 = 2, 05-06 = 3"],
        flags=["table-options-reconstructed", "has-figure"]),
}


def portal_fix_2025(r):
    r = [dict(x) for x in r]
    # Q5 prints the Q4 stem twice; reconstructed from its options.
    for x in r:
        if x["stem"].startswith("What is the default block size") and not x["options"]:
            x["stem"] = "What is the default block size in HDFS (as of Hadoop 2.x)?"
            x["options"] = ["64 KB", "128 MB", "256 MB", "1 GB"]
            x["answers_text"] = ["128 MB"]
    # the one whose stem came back empty: its options are NameNode/JobTracker/DataNode/TaskTracker
    for x in r:
        if not x["stem"].strip() and "DataNode" in x["options"]:
            x["stem"] = "Which component of HDFS stores the actual data blocks? (the printed stem repeats the block-size question)"
            x["flags"] = x.get("flags", []) + ["stem-reconstructed"]
    return r


def strip_email(r):
    for x in r:
        x["stem"] = re.sub(r"^\S+@\S+\s+", "", x["stem"]).strip()
    return r


# ---------------------------------------------------------------- 2021 week 0 (no answer key printed)
def week0_2021(w0_2023):
    qs = []
    for x in w0_2023:
        y = dict(x)
        y["flags"] = list(x.get("flags", [])) + ["answer-from-2023-twin"]
        qs.append(y)
    # position 9 ("fork") in 2023 is followed by the two extra 2021 questions
    qs.append(dict(week=0, stem="Which of the following page replacement algorithms suffers from Belady's anomaly?",
                   options=["FIFO", "LRU", "Optimal Page Replacement", "Both LRU and FIFO"], answers_text=["FIFO"],
                   flags=["answer-solved"]))
    qs.append(dict(week=0, stem="Suppose the numbers 7, 5, 1, 8, 3, 6, 0, 9, 4, 2 are inserted in that order into an initially empty binary search tree. The binary search tree uses the usual ordering on natural numbers. What is the in-order traversal sequence of the resultant tree ?",
                   options=["7 5 1 0 3 2 4 6 8 9", "0 2 4 3 1 6 5 9 8 7", "0 1 2 3 4 5 6 7 8 9", "9 8 6 4 2 3 0 1 5 7"],
                   answers_text=["0 1 2 3 4 5 6 7 8 9"], flags=["answer-solved"]))
    for q in qs:
        q["year"] = 2021
    return qs


# ---------------------------------------------------------------- 2024 answer key (solved by reading the explanations)
A2024 = {
    1: "B B C B B A D C B B", 2: "A B B C C C BC D C B", 3: "B B C C C A B B A C", 4: "C B C D B C C C C C",
    5: "B D A B A D C C D C", 6: "D B D B C B C C D D", 7: "B C B B B B C C C C", 8: "B B C B B D B B A C",
}
CUT = re.compile(
    r"\s+(?:Ans\b|And-|Answer:|(?:Option|option)\s+[A-Da-d]\b|[a-dA-D][\.\)]\s*(?:Correct|Incorrect)|[a-dA-D]\)\s+[A-Z]|S1:\s)")
NOTE_2024 = {(2, 7): "Source explanation marks both B and C as correct."}


def fix_2024(r):
    out = []
    for x in r:
        x = dict(x)
        opts = [norm(o) for o in x["options"]]
        m = CUT.search(opts[-1])
        if m:
            opts[-1] = opts[-1][: m.start()].strip()
        x["options"] = opts
        key_ = A2024[x["week"]].split()[x["qno"] - 1]
        x["answer_letters"] = list(key_)
        x["flags"] = [f for f in x.get("flags", []) if f != "answer-unresolved"] + ["answer-inferred-from-explanation"]
        if (x["week"], x["qno"]) in NOTE_2024:
            x["flags"].append("source-lists-two-correct")
        out.append(x)
    return out


A2025_FIX = {(6, 1): "B", (6, 4): "C", (7, 3): "C"}


# ---------------------------------------------------------------- topics
WEEK_TOPIC = {0: "Prerequisites", 1: "Intro to Big Data", 2: "Hadoop / HDFS / MapReduce", 3: "Spark & key-value stores",
              4: "Storage: CAP, Cassandra, ZooKeeper", 5: "Streaming: HBase, Kafka, Spark Streaming",
              6: "ML basics: regression, k-means", 7: "ML with Spark: trees & ensembles", 8: "Graph processing"}
KW = [
    ("HDFS", r"\bhdfs\b|namenode|datanode|block size|replication"), ("MapReduce", r"mapreduce|map\(\)|reduce\(\)|reducer|mapper|combiner|partitioner"),
    ("YARN", r"\byarn\b|resource ?manager|node ?manager"), ("Spark", r"\bspark\b|\brdd|dataframe|dstream"),
    ("Kafka", r"kafka"), ("HBase", r"hbase|region"), ("Cassandra", r"cassandra|cql|snitch|gossip|tombstone|hinted"),
    ("ZooKeeper", r"zookeeper|znode"), ("CAP", r"\bcap\b|consistency|partition tolerance"), ("Hive/Pig/Sqoop/Flume", r"\bhive\b|\bpig\b|sqoop|flume|impala|mahout"),
    ("GraphX/PageRank", r"graphx|pagerank|graph"), ("ML", r"k-means|random forest|boosting|bagging|decision tree|regression|classification|cross-validation|overfit|cosine|distance|clustering|gradient"),
    ("Databases/OS/Networks", r"super key|bcnf|3nf|b\+|acid|ipv4|\bttl\b|\barp\b|fork\(\)|belady|binary search tree|smtp|critical section|network service|process-to-process"),
]


def topics(q):
    t = {WEEK_TOPIC[q["week"]]}
    text = (q["question"] + " " + " ".join(o["text"] for o in q["options"])).lower()
    for name, rx in KW:
        if re.search(rx, text):
            t.add(name)
    return sorted(t)


# ---------------------------------------------------------------- assemble
def to_letters(x):
    opts = x["options"]
    if "answer_letters" in x and x["answer_letters"]:
        return x["answer_letters"]
    L = []
    for a in x.get("answers_text", []):
        a = norm(a)
        hit = None
        for i, o in enumerate(opts):
            if norm(o) == a:
                hit = i
                break
        if hit is None:
            for i, o in enumerate(opts):
                if norm(o).startswith(a[:30]) or a.startswith(norm(o)[:30]):
                    hit = i
                    break
        if hit is not None:
            L.append(chr(65 + hit))
    return sorted(set(L))


def main():
    sets = []  # (year, srckey, list of raw question dicts)
    a = fix_2019a(load("2019a"))
    sets.append((2019, "2019a", a))
    sets.append((2019, "2019b", tf_fix(load("2019b"))))
    w23 = strip_email(load("2023w0"))
    sets.append((2021, "2021", week0_2021(w23) + load("2021s")))
    sets.append((2022, "2022", load("2022s")))
    sets.append((2023, "2023", w23 + load("2023s")))
    sets.append((2024, "2024", strip_email(load("2024w0")) + fix_2024(load("2024s"))))
    sets.append((2025, "2025", portal_fix_2025(load("2025w0")) + load("2025s")))
    sets.append((2026, "2026", load("2026")))  # this repo's notes/week-N/assignment.md

    bank = []
    for year, sk, rows in sets:
        counters = {}
        for x in rows:
            x = dict(x)
            wk = x["week"]
            counters[wk] = counters.get(wk, 0) + 1
            qno = x.get("qno") or counters[wk]
            if sk == "2025" and (wk, qno) in A2025_FIX:
                x["answer_letters"] = [A2025_FIX[(wk, qno)]]
            letters = to_letters(x)
            opts = [{"k": chr(65 + i), "text": norm(o)} for i, o in enumerate(x["options"])]
            flags = list(x.get("flags", []))
            if not letters:
                flags.append("answer-unresolved")
            if len(letters) > 1:
                flags.append("multi-answer")
            q = {
                "id": f"{year}-W{wk}-Q{qno}",
                "year": year, "week": wk, "qno": qno,
                "type": "MSQ" if len(letters) > 1 else "MCQ",
                "question": norm(x["stem"]),
                "options": opts, "answer": letters,
                "explanation": x.get("explanation", "") or "",
                "source": {"file": x.get("path") or SRC[sk], "page": x.get("page")},
                "flags": sorted(set(flags)),
            }
            ov = OVERRIDES.get(q["id"])
            if ov:
                if "options" in ov:
                    q["options"] = [{"k": chr(65 + i), "text": t} for i, t in enumerate(ov["options"])]
                if "question" in ov:
                    q["question"] = ov["question"]
                if "answer" in ov:
                    q["answer"] = ov["answer"]
                    q["type"] = "MSQ" if len(ov["answer"]) > 1 else "MCQ"
                    q["flags"] = [f for f in q["flags"] if f != "multi-answer"]
                q["flags"] = sorted(set(q["flags"]) | set(ov.get("flags", [])))
            if q["id"] in IMAGES:
                q["images"] = ["images/" + n for n in IMAGES[q["id"]]]
            q["topics"] = topics(q)
            bank.append(q)

    # unique ids (2019 has two source files for different weeks, so collisions are not expected)
    seen = {}
    for q in bank:
        if q["id"] in seen:
            q["id"] += "b"
        seen[q["id"]] = 1

    # duplicates across years
    for i, q in enumerate(bank):
        q["_k"] = key(q["question"])
    groups = []
    for i, q in enumerate(bank):
        placed = False
        for g in groups:
            r = bank[g[0]]
            if q["_k"] == r["_k"] or (
                min(len(q["_k"]), len(r["_k"])) > 25
                and difflib.SequenceMatcher(None, q["_k"], r["_k"]).quick_ratio() > 0.9
                and difflib.SequenceMatcher(None, q["_k"], r["_k"]).ratio() > 0.9
            ):
                ok = True
                ao = {key(o["text"]) for o in q["options"]}
                bo = {key(o["text"]) for o in r["options"]}
                if ao and bo and len(ao & bo) / max(len(ao), len(bo)) < 0.5:
                    ok = False
                if ok:
                    g.append(i)
                    placed = True
                    break
        if not placed:
            groups.append([i])
    # stems that differ too much for the fuzzy match but are the same question
    FORCE = [("2019-W4-Q4", "2021-W4-Q10")]
    idx = {q["id"]: i for i, q in enumerate(bank)}
    for a, b in FORCE:
        ga = next(g for g in groups if idx[a] in g)
        gb = next(g for g in groups if idx[b] in g)
        if ga is not gb:
            gb.extend(ga)
            groups.remove(ga)
    # collapse repeats: one record per unique question, listing every appearance
    def quality(q):
        return (len([f for f in q["flags"] if f != "multi-answer"]), -q["year"])
    merged = []
    for g in groups:
        members = [bank[i] for i in g]
        canon = dict(min(members, key=quality))
        apps = sorted(({"id": m["id"], "year": m["year"], "week": m["week"], "qno": m["qno"]} for m in members),
                      key=lambda a: (a["year"], a["week"], a["qno"]))
        canon["appearances"] = apps
        canon["repeat"] = len(apps)
        canon["years"] = sorted({a["year"] for a in apps})
        canon["weeks"] = sorted({a["week"] for a in apps})
        canon["topics"] = sorted(set().union(*[set(m["topics"]) for m in members]))
        canon["flags"] = sorted(set(canon["flags"]))
        if not canon["explanation"]:
            canon["explanation"] = next((m["explanation"] for m in members if m["explanation"]), "")
        imgs = []
        for m in members:
            for im in m.get("images", []):
                if im not in imgs:
                    imgs.append(im)
        if imgs:
            canon["images"] = imgs
        canon.pop("_k", None)
        canon.pop("group", None)
        canon.pop("also_in", None)
        merged.append(canon)
    total_raw = len(bank)
    bank = merged
    bank.sort(key=lambda q: (q["week"], q["year"], q["qno"]))
    json.dump(bank, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(total_raw, "raw questions ->", len(bank), "unique;", sum(1 for q in bank if q["repeat"] > 1), "repeated")
    from collections import Counter
    print("raw per year:", sorted(Counter(a["year"] for q in bank for a in q["appearances"]).items()))
    print("unresolved:", [q["id"] for q in bank if "answer-unresolved" in q["flags"]])


if __name__ == "__main__":
    main()
