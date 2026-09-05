# Parsing an NPTEL assignment paste (Cmd+A / Cmd+C)

The portal paste is noisy. Reconstruct questions; do not keep chrome.

## Throw away

Course outline trees, “How does an NPTEL online course work?”, login, payment, week-0 ads, “Assignment submitted on…”, “Due on…”, “Score: 0/1”, “No, the answer is incorrect.”, “Yes, the answer is correct.”, unit= / lesson= URLs, reviewer emails.

Keep due date and total marks in one header line if present.

## A typical item looks like

```
3) Which of the following is used in Hadoop for distributed storage?  1 point
Hive
HDFS
YARN
Spark
Accepted Answers:
HDFS
```

or options jammed on one line: `Hive Introduction to HDFS Big Data YARN Spark`.

Rules:

- Numbered `N)` or `N.` starts a question. `1 point` / `2 points` is marks, not an option.
- `Accepted Answers:` / `Correct Answer:` is the portal key. Use it as a *claim to verify*, not as gospel if it contradicts this week's slides/notes.
- `Statement 1` / `Statement 2` stay together as one question.
- True/False may have no a/b/c/d; still label the answer True or False.
- If the user had already selected an option, that is **their** choice, not necessarily correct. Prefer `Accepted Answers` when present, then verify.

## If options are merged

Split on known tool names and obvious phrases. If a split is uncertain, keep the blob and say so under the question — do not invent a fourth option.

## Images in the assignment

Cmd+A copy usually **drops** figures. If the stem says “from the figure” and no figure is in the paste, write `Figure missing from paste` and solve from the text if possible; otherwise mark unsolved.
