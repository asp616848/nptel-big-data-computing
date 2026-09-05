# Week 2 assignment

Due date: 2026-09-02, 23:59 IST (closed). 10 questions, 1 point each.

## Q1 (1 point)

**Question**

Which HDFS component is primarily responsible for monitoring replica counts and initiating re-replication when a block becomes under-replicated?

**Options**

- a) DataNode
- b) Client
- c) NameNode
- d) Secondary NameNode

**Answer:** **c) NameNode**

**Why:** The NameNode tracks block-to-DataNode mappings and replication state; per `notes/week-2/notes.md` Lec 4, it detects under-replication via missing heartbeats and restarts the replication process to restore the configured factor.

**Trap:** DataNode only stores and serves blocks — it doesn't decide replication counts, it just executes what the NameNode instructs.

---

## Q2 (1 point)

**Question**

What is the primary purpose of introducing the HDFS Federation?

**Options**

- a) Increase replication factor
- b) Increase namespace scalability
- c) Reduce block size
- d) Eliminate DataNodes

**Answer:** **b) Increase namespace scalability**

**Why:** Lec 4 of `notes/week-2/notes.md` names namespace scalability as Federation's headline benefit (plus performance/isolation), achieved by splitting one NameNode's namespace into multiple independent NameNode+block-pool pairs.

**Trap:** Federation doesn't touch replication factor or block size — those are separate tuning parameters (`dfs.replication`, `dfs.block.size`).

---

## Q3 (1 point)

**Question**

Which of the following is directly affected by the number of HDFS blocks?

**Options**

- a) NameNode memory usage
- b) Number of Map tasks
- c) Both A and B
- d) Neither A and B

**Answer:** **c) Both A and B**

**Why:** Lec 4 notes: more blocks per file → more NameNode metadata to hold in memory, and at least one map task is typically needed per block, so both scale together with block count.

**Trap:** Picking just one of A/B misses that the lecture explicitly ties block count to both memory pressure *and* task count in the same trade-off discussion.

---

## Q4 (1 point)

**Question**

What is the default value of the parameter `dfs.replication`?

**Options**

- a) 1
- b) 2
- c) 3
- d) 4

**Answer:** **c) 3**

**Why:** Directly stated in Lec 4: default replication factor is 3, configured via `dfs.replication`.

---

## Q5 (1 point)

**Question**

(Portal repeats the Q4 stem text, but the options describe DataNode failure handling — treating it as intended: "How does the NameNode respond when it detects a DataNode failure?")

**Options**

- a) Ignores the failure
- b) Deletes all blocks immediately
- c) Marks the DataNode and initiates re-replication if needed
- d) Restarts the DataNode automatically

**Answer:** **c) Marks the DataNode and initiates re-replication if needed**

**Why:** Lec 4's fault-tolerance section: a DataNode missing heartbeats is marked down, stops receiving new I/O, and the NameNode re-replicates any blocks that fell below the replication factor.

**Trap:** The NameNode cannot restart a DataNode remotely (d) — recovery is via re-replication onto other live nodes, not reviving the failed one.

---

## Q6 (1 point)

**Question**

Which statement about Reduce tasks is TRUE?

**Options**

- a) A key can be processed by multiple Reducers.
- b) Each key is assigned to exactly one Reducer.
- c) Reducers execute before Mappers.
- d) Reducers never use partitioning.

**Answer:** **b) Each key is assigned to exactly one Reducer.**

**Why:** Lec 6's Reduce/partitioning section: every key routes to exactly one reduce task (commonly via hash partitioning, `hash(key) % num_reduce_tasks`) so all values for that key land together for correct aggregation.

**Trap:** (a) directly contradicts the "each key → one reducer" rule; (c) reverses the map→shuffle→reduce order; (d) partitioning is exactly the mechanism that assigns keys to reducers.

---

## Q7 (1 point)

**Question**

What is the primary role of a Partitioner in MapReduce?

**Options**

- a) Sort records within a Reducer
- b) Decide which Reducer receives a key-value pair
- c) Combine Mapper outputs locally
- d) Replicate data blocks across HDFS

**Answer:** **b) Decide which Reducer receives a key-value pair**

**Why:** Lec 6 notes hash partitioning as `reduce_task_number = hash(key) % number_of_reduce_tasks` — the partitioner's job is routing each key to its designated reducer.

**Trap:** (a) sorting-within-reducer and (c) local combining are related but separate shuffle-stage activities, not the partitioner's defining role.

---

## Q8 (1 point)

**Question**

Which YARN component is responsible for detecting task failures for a specific job?

**Options**

- a) Resource Manager (RM)
- b) Node Manager (NM)
- c) Application Master (AM)
- d) DataNode

**Answer:** **c) Application Master (AM)**

**Why:** Lec 7's YARN section: the Application Master is scoped to one job and negotiates containers plus detects/handles that job's task failures, distinct from the cluster-wide Resource Manager.

**Trap:** RM schedules cluster-wide but doesn't track per-job task failures; that's delegated to each job's own AM.

---

## Q9 (1 point)

**Question**

Which statement about the Reduce function is TRUE?

**Options**

- a) It accepts an intermediate key and a set of values.
- b) It processes only one value at a time.
- c) It cannot aggregate values.
- d) It always produces multiple output values.

**Answer:** **a) It accepts an intermediate key and a set of values.**

**Why:** Lec 6 core ideas: reduce takes an intermediate key and an iterator over all values for that key, then aggregates (e.g., sums) them — matching option (a) exactly.

**Trap:** (d) is backwards — the lecture states reduce typically produces 0 or 1 output values per invocation, not "always multiple."

---

## Q10 (1 point)

**Question**

In the Reverse Web-Link Graph application, the Mapper emits:

**Options**

- a) (source, target)
- b) (target, source)
- c) (URL, 1)
- d) (target, count)

**Answer:** **b) (target, source)**

**Why:** Lec 7 worked example: for edge (source, target), map emits `<target, source>` so reduce can group all sources per target into `<target, list(source)>` — the whole point of "reversing" the link direction.

**Trap:** (a) is the un-reversed direction (that would just replay the original graph); (c) is the URL-access-frequency pattern from a different application in the same lecture.

---

## Patterns this week

- Straight component-identity questions dominate (NameNode vs DataNode vs RM vs NM vs AM) — know exactly which layer (HDFS vs YARN) each name belongs to.
- Several questions test "who does X when Y fails" — NameNode's heartbeat-driven re-replication, AM's per-job failure detection. NPTEL likes turning fault-tolerance mechanics into MCQs.
- Reduce/Partitioner questions test the "one key → one reducer" invariant from multiple angles (statement-true/false, role-of-component, and default-behavior framing).
- The Reverse Web-Link Graph direction-flip (target,source) is a recurring trap — expect it reworded with a different application (e.g., inverted index's (word, docID)) on the final.

## Tips for the final

- Expect "which component does X" stems to reappear with RM/NM/AM/NameNode/DataNode/JobTracker/TaskTracker shuffled into new combinations — learn the *role*, not the sentence.
- Don't memorize option letters; this set's "c" and "b" answers will land on different letters when reworded.
- Revisit the "one key → one reducer" and "map/reduce direction-flip" ideas — both showed up twice in Week 2's own quiz pattern already (Q6/Q7 and Q10), so they're high-value for the exam.
