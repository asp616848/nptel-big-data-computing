# How NPTEL actually tests this course

Course: **Big Data Computing**, Prof. Rajiv Misra, IIT Patna, 8 weeks.

Use this file to shape notes and quizzes. Do **not** paste leaked answer keys into the learner's notes. Write original questions from *this week's* slides + transcript.

## What scores the certificate

Typical recent pattern (sessions vary; check the current portal):

- **Weekly assignment** each week: MCQs, usually about 10 questions, 1 mark each.
- **Proctored exam**: about **60 MCQs, 100 marks**, often 20+20+20 questions with 1 / 2 / 2 marks. **No negative marking** in the 2025 forenoon paper reported by learners.
- Certificate mixes assignment average + exam. Weekly quizzes still matter, and the exam reuses their *ideas*.

## What the questions look like

NPTEL for this course is not a coding exam. It is a **vocabulary + architecture + distinction** exam.

Recurring shapes:

1. **One-line definition.** “Variety refers to ___.” Options are volume / speed / types-and-formats / correctness.
2. **Tool identity.** “Which Hadoop component is used for distributed storage?” Hive / **HDFS** / YARN / Spark.
3. **Which is NOT.** “Which is not a NoSQL database?” HBase / **SQL Server** / Cassandra.
4. **Two-statement true/false.** Two sentences about Volatility vs Viscosity (or similar V's). Often *both false* because the definitions were swapped.
5. **Role of a component.** YARN allocates resources and schedules. Sqoop bulk-transfers Hadoop ↔ RDBMS. Flume collects log streams. MLlib is Spark's distributed ML library.
6. **Who stores what.** NameNode: filenames + block locations. Reading an already-known block from a DataNode does not need the NameNode.
7. **What you would change in WordCount.** 3-word phrases → change **map()** only (reduce still sums counts).
8. **Tiny numerical.** Default HDFS block size; how many blocks and replicas for a given file size. Rare, but it shows up even on the final.
9. **Architecture pictures turned into words.** HDFS Federation = multiple NameNodes with independent namespaces. CAP: pick which two you keep. Spark Streaming = micro-batches, not one-tuple-at-a-time unless the lecture says otherwise.

## How questions are picked

- Almost always **from the slides' exact nouns**, not from outside blogs.
- Professor asides in the transcript become T/F traps when he says “this is *not* X, people confuse it with Y”.
- Comparison slides (MR1 vs YARN, RDD vs DataFrame, Sqoop vs Flume, HBase vs Cassandra, window types) are gold.
- Numbers, default values, and component lists on a slide are copied nearly verbatim.
- Final exam often **rewords** weekly assignment stems rather than inventing new topics. Studying weekly MCQ *patterns* is high leverage. Memorizing last year's option letter (A/B/C/D) is low leverage because options shuffle.

## What “full marks” study actually is

For each lecture, the learner must be able to:

- Give the slide definition of every bold term.
- Name the components on any architecture diagram and one job each.
- Distinguish near-twins (the “which is NOT” / swapped-statement questions).
- Work one toy example that was on the slides (WordCount, k-means map/reduce, PageRank iteration, a CQL snippet, a window).
- Recall any default number the slide stated.

If a paragraph in the transcript does not help those five, it does not belong in the notes.

## Agent rules for practice questions

- After every lecture (or part): 5–8 items, exam format only (MCQ, T/F, two-statement). Make several of them *reasoning* still inside that format: swapped definitions, “which component would fail”, “what changes in the example”.
- After the week: 10–12 mixed items like Assignment-N.
- **Never interleave answers with questions.** Full set, then `Answer key` with letter + one-line reason.
- Never say “the 2023 assignment answer is B”. Teach so any wording still works.
- If the user pastes this week's live assignment, help them *reason*, do not farm an answer key.
