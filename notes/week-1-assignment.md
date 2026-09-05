# Week 1 assignment

Due 2026-08-26, 23:59 IST. Last recorded submission 2026-08-18, 14:29 IST. All 10 questions, 1 point each — all shown correct on the portal.

## Q1 (1 point)

**Question**

A dataset was highly useful in 2024, but by 2026 the same dataset becomes irrelevant because the information has lost significance. Which "V" best describes this situation?

**Options**

- a) Validity
- b) Veracity
- c) Volatility
- d) Venue

**Answer:** **c) Volatility**

**Why:** [[week-1]] Lecture 1 defines Volatility as the rate of data loss and the stable lifetime of data — exactly "data that used to matter but has since lost significance."

**Trap:** Validity is accuracy/correctness for a given use, not loss of relevance over time; Veracity is about noise/trustworthiness, not aging-out.

---

## Q2 (1 point)

**Question**

Which of the following statements about Oozie is CORRECT?

**Options**

- a) Oozie is a distributed NoSQL database.
- b) Oozie is a workflow scheduler system for Hadoop jobs.
- c) Oozie is used to store data in HDFS.
- d) Oozie is a machine learning library for Spark.

**Answer:** **b**

**Why:** Lecture 3, Core ideas — Oozie is explicitly defined as the workflow scheduler that manages/coordinates Hadoop jobs.

**Trap:** Options a/c/d misassign Oozie's job to HBase/Cassandra (NoSQL), HDFS (storage), and MLlib (ML library) respectively.

---

## Q3 (1 point)

**Question**

Oozie can directly coordinate which of the following Hadoop ecosystem components?

**Options**

- a) Hive, Pig, Sqoop, and MapReduce
- b) HDFS, NameNode, DataNode, and YARN only
- c) Cassandra, MongoDB, and Redis only
- d) Spark MLlib and GraphX only

**Answer:** **a**

**Why:** Lecture 3 states Oozie "supports MapReduce, Pig, Hive, and Sqoop" as the jobs it coordinates.

**Trap:** b/c/d list components Oozie does not directly schedule (storage/resource internals, NoSQL stores, Spark libraries).

---

## Q4 (1 point)

**Question**

What is the primary purpose of Apache Flume in the Hadoop ecosystem?

**Options**

- a) Querying data stored in HDFS
- b) Collecting and transferring large amounts of log data
- c) Performing machine learning tasks
- d) Managing cluster resources

**Answer:** **b**

**Why:** Lecture 3 — Flume is "a distributed reliable available service for efficiently collecting, aggregating, moving large amounts of log data into HDFS," i.e., data ingestion.

**Trap:** a is Hive's job, c is MLlib's, d is YARN's.

---

## Q5 (1 point)

**Question**

What is the primary role of Apache ZooKeeper in a Hadoop ecosystem?

**Options**

- a) Distributed data storage
- b) Workflow scheduling
- c) Distributed coordination and synchronization
- d) SQL query processing

**Answer:** **c**

**Why:** Lecture 2 and 3 both define Zookeeper as the centralized coordination service — configuration, synchronization, naming, group services, leader election.

**Trap:** b is Oozie's role (near-twin covered in [[week-1]] near-twins table); a is HDFS/HBase, d is Hive.

---

## Q6 (1 point)

**Question**

Hive primarily operates on data stored in:

**Options**

- a) MongoDB
- b) Cassandra
- c) HDFS
- d) Redis

**Answer:** **c**

**Why:** Hive is a distributed data-management/SQL-query layer for Hadoop, running over MapReduce against data stored in HDFS.

**Trap:** MongoDB/Cassandra/Redis are separate NoSQL stores not part of the Hive-over-Hadoop path.

---

## Q7 (1 point)

**Question**

Which of the following best describes Apache Hive?

**Options**

- a) A distributed coordination service
- b) A workflow scheduler
- c) A data warehouse system built on Hadoop
- d) A NoSQL database

**Answer:** **c**

**Why:** Lecture 2/3 — Hive provides SQL-like queries (HiveSQL) over MapReduce/HDFS for data mining and analysis, i.e., a data-warehouse layer on Hadoop.

**Trap:** a=Zookeeper, b=Oozie, d=HBase/Cassandra — all near-twins from this week's notes.

---

## Q8 (1 point)

**Question**

Which Hadoop module stores metadata?

**Options**

- a) DataNode
- b) TaskTracker
- c) NameNode
- d) Reducer

**Answer:** **c**

**Why:** Lecture 3 — the NameNode holds filenames and block-location metadata; DataNodes hold the actual data blocks.

**Trap:** DataNode is the classic swapped-pair distractor (holds data, not metadata).

---

## Q9 (1 point)

**Question**

Which pair is correctly matched?

**Options**

- a) Hive – Stream Processing
- b) Kafka – Distributed Commit Log
- c) Sqoop – Graph Analytics
- d) GraphX – ETL Tool

**Answer:** **b**

**Why:** Kafka is described in Lecture 2 as an open-source distributed stream-processing framework built around a distributed commit-log abstraction that feeds Spark Streaming.

**Trap:** a/c/d all swap roles: Hive is SQL queries not streaming, Sqoop is RDBMS↔Hadoop transfer not graphs, GraphX is Spark's graph-analytics library not ETL.

---

## Q10 (1 point)

**Question**

Which of the following is the PRIMARY function of Apache ZooKeeper in a distributed Hadoop environment?

**Options**

- a) Storing large-scale data across cluster nodes
- b) Managing distributed coordination, synchronization, and configuration services
- c) Executing SQL-like queries on HDFS data
- d) Scheduling Hadoop workflows and jobs

**Answer:** **b**

**Why:** Same Zookeeper definition as Q5 — coordination/sync/config service, not storage, querying, or scheduling.

**Trap:** a=HDFS, c=Hive, d=Oozie.

---

## Patterns this week

- Heavy on **tool-identity** and **"which pair is correctly matched"** questions — pure vocabulary recall from the Hadoop ecosystem slide, no reasoning needed once you know each tool's one-liner.
- Zookeeper vs. Oozie is the recurring near-twin trap (coordination/config vs. workflow scheduling) — it showed up twice (Q5, Q10).
- NameNode vs. DataNode (metadata vs. actual blocks) is tested directly (Q8) — same swap as flagged in [[week-1]] near-twins table.
- One V-characteristics question (Q1) tests the *less obvious* V's (Volatility) rather than the core 3 V's — expect final-exam questions to reach beyond Volume/Velocity/Variety into Veracity/Value/Volatility/Validity.

## Tips for the final

- The Zookeeper/Oozie and NameNode/DataNode swaps are near-certain to reappear reworded — memorize the *function*, not the option letter.
- Don't just memorize "3 V's" — this assignment shows the extra V's (Volatility, Validity, Veracity) are fair game too.
- Tool one-liners (Hive=SQL warehouse, Pig=scripting ETL, Sqoop=RDBMS transfer, Flume=log ingestion, Kafka=distributed commit log/streaming, Oozie=workflow scheduler, Zookeeper=coordination) are the highest-leverage thing to drill from this week.
