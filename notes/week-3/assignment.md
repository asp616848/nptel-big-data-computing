# Week 3 assignment

Due 2026-09-09, 23:59 IST. Last recorded submission 2026-08-30, 16:21 IST. All 10 questions, 1 point each — no accepted answers shown on the portal paste, solved from [[week-3]] notes.

## Q1 (1 point)

**Question**

Which statement best explains Spark's fault tolerance mechanism?

**Options**

- a) Every RDD is replicated across all nodes.
- b) Every transformation result is written to HDFS.
- c) Spark tracks lineage and recomputes lost partitions.
- d) Spark checkpoints every operation by default.

**Answer:** **c**

**Why:** Lecture 10, "How lineage actually works" — Spark logs the coarse-grained transformations that built each RDD (its lineage); on partition loss it traces the log and recomputes only that partition, at no extra cost when nothing fails.

**Trap:** a/b describe HDFS-style redundancy (block replication / write-through), which is exactly what Spark avoids — that's the "not a backup copy" distinction the notes call out explicitly. d overstates: persistence is opt-in, not automatic.

---

## Q2 (1 point)

**Question**

Which operation below is an Action rather than a Transformation?

**Options**

- a) collect()
- b) join()
- c) map()
- d) filter()

**Answer:** **a**

**Why:** Lecture 9 Part B, "Basic actions" — `collect()` pulls the RDD back to the driver, triggering execution. `map`, `filter`, `join` are all lazy transformations that only build the DAG.

**Trap:** join/map/filter are the textbook transformation examples used throughout the notes precisely because they never run until an action like `collect()` forces them.

---

## Q3 (1 point)

**Question**

Which Spark component is responsible for splitting a DAG into stages?

**Options**

- a) SparkContext
- b) TaskScheduler
- c) DAGScheduler
- d) BlockManager

**Answer:** **c**

**Why:** Lecture 10, "Execution mechanics" — the DAG scheduler splits the DAG into stages of tasks and submits each stage once ready; the task scheduler then launches those tasks and retries stragglers/failures.

**Trap:** b (TaskScheduler) is the near-twin — it launches/retries tasks *within* a stage, but does not decide the stage boundaries. SparkContext is the entry point, not the scheduler; BlockManager isn't the component the notes name for this job (cache/task execution lives on the executor).

---

## Q4 (1 point)

**Question**

Why is reduceByKey() generally preferred over groupByKey() for aggregation?

**Options**

- a) It automatically sorts keys.
- b) It uses combiners on the map side.
- c) It creates fewer partitions.
- d) It avoids shuffling completely.

**Answer:** **b**

**Why:** Lecture 9 Part B, "Key-value pair RDDs" — `reduceByKey` "automatically applies a combiner on the map side," partially summing values before they cross the network, the same optimization idea as a MapReduce combiner. `groupByKey` ships every raw value.

**Trap:** d is wrong — reduceByKey still shuffles, just less data; a/c aren't properties either operation has (no sorting, no partition-count change) per the notes.

---

## Q5 (1 point)

**Question**

In Spark, which operation triggers actual execution of a DAG?

**Options**

- a) map()
- b) filter()
- c) join()
- d) count()

**Answer:** **d**

**Why:** Same transformation-vs-action split as Q2 — `count()` is the canonical action used throughout the Lecture 9 log-mining trace ("count is an action, so *this* is the point where Spark actually walks back through the chain and executes everything").

**Trap:** map/filter/join are all lazy transformations — none of them runs anything by itself.

---

## Q6 (1 point)

**Question**

Which statement about RDDs is FALSE?

**Options**

- a) RDDs are immutable.
- b) RDDs can be cached for reuse.
- c) RDDs automatically rebuild lost data using lineage.
- d) RDDs support direct modification of existing partitions.

**Answer:** **d**

**Why:** Lecture 9's RDD definition and the near-twin table both stress RDDs are *immutable* — created only by reading external data or applying coarse-grained transformations, never edited element-by-element/in place. a, b, c are all directly stated properties (immutable, cacheable, lineage-rebuilt).

**Trap:** "Direct modification of existing partitions" is the opposite of coarse-grained, immutable transformations — this is the false statement to pick.

---

## Q7 (1 point)

**Question**

Which feature helps Spark recover lost RDD partitions?

**Options**

- a) Replication
- b) Lineage
- c) Compression
- d) Scheduling

**Answer:** **b**

**Why:** Same mechanism as Q1 — lineage is the recorded transformation log Spark replays to recompute a lost partition.

**Trap:** a (Replication) is the HDFS-style mechanism the notes explicitly contrast lineage against; c/d aren't fault-tolerance mechanisms discussed in the notes at all.

---

## Q8 (1 point)

**Question**

SparkContext is:

**Options**

- a) Storage system
- b) Main entry point to Spark functionality
- c) Worker node
- d) Scheduler

**Answer:** **b**

**Why:** Lecture 9 Part B and Lecture 10 both define it identically: "A SparkContext ... is the entry point to all Spark functionality," created inside the driver program.

**Trap:** c/d confuse SparkContext with the Worker Nodes / DAGScheduler-TaskScheduler it talks to; a is not a role it has anywhere in the notes.

---

## Q9 (1 point)

**Question**

Which Spark component launches tasks on worker nodes and retries failed tasks?

**Options**

- a) SparkContext
- b) DAGScheduler
- c) BlockManager
- d) TaskScheduler

**Answer:** **d**

**Why:** Lecture 10, "Execution mechanics" — "the task scheduler then launches the actual tasks via the cluster manager and retries failed or straggling tasks." This is the mirror of Q3.

**Trap:** b (DAGScheduler) is the near-twin — it splits the DAG into stages but doesn't itself launch/retry individual tasks; that handoff to the task scheduler is exactly what the notes' near-twins section flags.

---

## Q10 (1 point)

**Question**

A Spark application performs multiple iterations over the same dataset. Which feature provides the greatest performance improvement?

**Options**

- a) HDFS replication
- b) Data compression
- c) Caching/Persistence of RDDs
- d) Increasing block size

**Answer:** **c**

**Why:** Lecture 9 Part B's PageRank walkthrough is the notes' explicit example: "because `links` and `ranks` are cached RDDs reused every iteration, PageRank is exactly the kind of iterative workload where Spark's in-memory model beats MapReduce" — same logic applies to k-means/logistic regression.

**Trap:** a/b/d are all storage-layer knobs (replication, compression, block size) that don't address the real cost of iterative work — re-reading/recomputing the same data every pass — which only in-memory caching removes.

---

## Patterns this week

- Heavy on the **Spark execution org chart**: SparkContext → DAGScheduler → TaskScheduler → Executors/Workers, tested from both directions (Q3 asks DAGScheduler's job, Q9 asks TaskScheduler's job) — know which one splits stages vs which one launches/retries tasks.
- **reduceByKey vs groupByKey** (Q4) is this week's headline near-twin, same map-side-combiner distinction flagged in the notes' near-twins table.
- **Lineage vs replication** shows up twice (Q1, Q7) as the core fault-tolerance concept — Spark recomputes via a transformation log, it does not keep redundant copies like HDFS.
- **Transformation vs action** recall (Q2, Q5) — pure vocabulary: map/filter/join never run anything; count/collect/take/save do.
- Q10 tests *applying* the caching concept to a scenario (iterative jobs) rather than just defining it — expect more "which real workload benefits from X" phrasing on the final.

## Tips for the final

- Memorize the *function* of each execution component, not just its name: DAGScheduler = stage-splitting, TaskScheduler = task launch/retry, SparkContext = entry point/driver-side handle. These get reworded and swapped as distractors constantly.
- Don't just memorize "lineage = fault tolerance" — be ready to explain *why* it's cheap (metadata only, no cost on the happy path) versus replication's constant storage/network overhead.
- reduceByKey's map-side combine is the single most-tested efficiency fact from Lecture 9/10 — drill it alongside the Week 2 MapReduce combiner concept, since NPTEL likes connecting the two weeks.
