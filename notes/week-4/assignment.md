# Week 4 assignment

Due 2026-09-16, 23:59 IST. No `Accepted Answers` in the paste — solved from `notes/week-4/notes.md`.

## Q1 (1 point)

**Question**

Which Cassandra replication strategy is specifically designed for multi-datacenter deployments?

**Options**

- a) Simple Strategy
- b) Network Topology Strategy
- c) Random Partitioner
- d) Byte Ordered Partitioner

**Answer:** **b**

**Why:** Lec 13 (Data Placement Strategies) — Simple Strategy just uses a partitioner within one ring; Network Topology Strategy is the one that explicitly "requires multiple data center deployments," placing a fixed number of replicas per DC and walking the ring clockwise onto different racks.

**Trap:** Random Partitioner and Byte Ordered Partitioner are the two *partitioner* choices used inside Simple Strategy, not replication strategies themselves.

---

## Q2 (1 point)

**Question**

What is the primary purpose of Cassandra's Bloom Filter?

**Options**

- a) Store key-value pairs permanently
- b) Compress SSTables
- c) Quickly determine if a key may exist in an SSTable
- d) Replace indexing structures

**Answer:** **c**

**Why:** Lec 13 — the Bloom filter is checked before touching disk, to find which SSTable a key is likely in; it's a cheap existence pre-check, not storage itself.

**Trap:** It does not replace the index file — the notes explicitly list the SSTable's index file and the Bloom filter as two separate pieces working together.

---

## Q3 (1 point)

**Question**

Which statement about Bloom Filters is TRUE?

**Options**

- a) They may produce false negatives.
- b) They never produce false positives.
- c) They may produce false positives but never false negatives
- d) They guarantee exact membership testing.

**Answer:** **c**

**Why:** Lec 13's own definition: checking for existence can say "present" when a key isn't actually there (false positive, ~0.02% in the slide's example) but it never says "absent" for a key that is actually present (no false negatives).

**Trap:** (a) and (d) invert the guarantee; (b) is close but wrong direction — false positives *do* happen, just rarely.

---

## Q4 (1 point)

**Question**

In Cassandra, why are writes generally faster than reads?

**Options**

- a) Reads use only memory.
- b) Writes avoid disk operations entirely.
- c) Writes are append-oriented using Commit Logs and MemTables
- d) Reads bypass SSTables.

**Answer:** **c**

**Why:** Lec 13 — a write only needs to append to the commit log and update the in-memory Memtable (write-back) before acking; it doesn't need to touch an SSTable on the critical path. Reads, by contrast, may have to check Memtable, row cache, Bloom filter, key cache, and one or more SSTables (Lec 17's read path).

**Trap:** (b) overstates it — the commit log write *is* a disk operation, just a fast sequential append, not the slower flush/compaction path.

---

## Q5 (1 point)

**Question**

Which Cassandra consistency level is the FASTEST for writes?

**Options**

- a) ALL
- b) QUORUM
- c) ONE
- d) ANY

**Answer:** **d**

**Why:** Lec 14 — ANY lets any server (not even necessarily a replica) ack the write, so the coordinator can cache it and reply immediately; the notes list ANY explicitly as "fastest."

**Trap:** ONE is faster than ALL/QUORUM but still requires an actual replica to be updated, so it's slower than ANY.

---

## Q6 (1 point)

**Question**

According to CAP theorem, Cassandra primarily chooses:

**Options**

- a) Consistency and Availability
- b) Consistency and Partition Tolerance
- c) Availability and Partition Tolerance
- d) Atomicity and Durability

**Answer:** **c**

**Why:** Lec 14 — the CAP Theorem Fallout slide places Cassandra in the AP camp (Availability + Partition tolerance) with eventual/weak consistency, alongside Dynamo and Voldemort.

**Trap:** (b) is HBase/BigTable/Spanner's choice, not Cassandra's; (d) mixes in ACID terms that belong to RDBMS, not CAP.

---

## Q7 (1 point)

**Question**

Which property defines Eventual Consistency?

**Options**

- a) All replicas are instantly synchronized.
- b) Replicas converge if updates stop.
- c) Reads always return latest value.
- d) No stale reads are possible.

**Answer:** **b**

**Why:** Lec 14/15 — eventual consistency's defining guarantee is that "if all writes to a key stop, all its replicas will eventually converge"; while writes continue, reads can lag behind (the "moving wave" described in Lec 14).

**Trap:** (a), (c), (d) all describe strong/linearizable consistency, the opposite end of the spectrum from eventual consistency.

---

## Q8 (1 point)

**Question**

What happens if a ZooKeeper ensemble loses majority availability?

**Options**

- a) A new leader is elected immediately.
- b) Remaining node becomes leader.
- c) No leader can be elected.
- d) System switches to standalone mode.

**Answer:** **c**

**Why:** Lec 16, Part B — the worked example (3 nodes, 2 die) shows that with only a minority surviving, Zookeeper deliberately elects no leader at all, rather than risk a split-brain scenario; a leader is only elected/kept when a majority (2f+1 for f failures) is available.

**Trap:** (b) contradicts the majority rule — a single surviving node out of three is not enough to become leader.

---

## Q9 (1 point)

**Question**

Which ZooKeeper design goal ensures that all updates are processed in a globally agreed order?

**Options**

- a) Ordered
- b) Replicated
- c) Fast
- d) Atomic

**Answer:** **a**

**Why:** Lec 16, Part A lists Zookeeper's four design goals (Simple, Replicated, Ordered, Fast) separately; "Ordered" is specifically the one where "Zookeeper will timestamp each update with a number... reflects the order of the transaction."

**Trap:** Atomicity (from the guarantees list, not the design-goals list) is about an update being all-or-nothing, not about global ordering across updates.

---

## Q10 (1 point)

**Question**

What is the default type of znode in ZooKeeper?

**Options**

- a) Ephemeral
- b) Sequential
- c) Temporary
- d) Persistent

**Answer:** **d**

**Why:** Lec 16, Part A — the notes state persistent znodes are "the default type of znode," remaining until explicitly deleted, as opposed to ephemeral (tied to a session) or sequential (auto-numbered).

**Trap:** "Temporary" isn't one of the three znode types the lecture names at all (Persistent, Ephemeral, Sequential).

---

## Patterns this week

- Near-twin traps dominate: Bloom filter direction of false positives/negatives, ANY vs ONE vs ALL speed ordering, and Cassandra's AP vs HBase's CP CAP choice.
- "Why is X faster than Y" questions (writes vs reads) test whether you know the actual mechanism (commit log + Memtable append) rather than a vague "it's optimized" answer.
- Zookeeper questions lean on the majority/`2f+1` rule and the three named design goals (Simple, Replicated, Ordered, Fast) plus the three znode types — expect these to be mixed and matched.

## Tips for the final

- The CAP-choice question (Cassandra = AP) is a near-certain reword target — memorize the *reasoning* (partition tolerance is basically mandatory, so it's really a C-vs-A choice), not just "Cassandra = AP."
- Don't memorize option letters; "which is fastest" orderings (ANY < ONE < QUORUM < ALL) are worth knowing as a full ranking, not just the extremes.
- Znode types and Zookeeper's four design goals are easy to blur together (e.g. "Ordered" vs "Atomic") — keep straight which is a *design goal* vs a *guarantee*.
