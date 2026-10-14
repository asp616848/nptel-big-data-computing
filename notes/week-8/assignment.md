# Week 8 assignment

Answers below match the answers given in the paste, each checked against `notes/week-8/notes.md`.

## Q1 (1 point)

**Question**

What is the main goal of GraphX?

**Options**

- a) Database management
- b) Unify data-parallel and graph-parallel analytics
- c) Replace Spark SQL
- d) Replace HDFS

**Answer:** **b**

**Why:** Lec 32/34 — GraphX is a distributed framework that unifies graph-parallel and data-parallel computation so the whole analytics pipeline runs in one system (tables and graphs as views of the same data).

---

## Q2 (1 point)

**Question**

Which phase is NOT part of the Graph-Parallel Pattern?

**Options**

- a) Gather
- b) Apply
- c) Scatter
- d) Shuffle Sort

**Answer:** **d**

**Why:** Lec 32 — the graph-parallel pattern is Gather (collect from neighbours), Apply (compute the new value), Scatter (send to neighbours). Shuffle Sort belongs to MapReduce.

---

## Q3 (1 point)

**Question**

Which GraphX operator joins vertices and edges together?

**Options**

- a) `mapV()`
- b) `subgraph()`
- c) `triplets`
- d) `reverse()`

**Answer:** **c**

**Why:** Lec 33 — the `triplets` operator joins vertices and edges: an edge plus both its end vertices.

**Trap:** `subgraph` filters, `reverse` flips edge direction, `mapV` transforms vertex properties.

---

## Q4 (1 point)

**Question**

In GraphX, a Property Graph consists of:

**Options**

- a) Only vertices
- b) Only edges
- c) Vertices and edges with properties
- d) Tables only

**Answer:** **c**

**Why:** Lec 33 — a property graph is a vertex property table (ID + property) and an edge property table (source ID, destination ID, property).

---

## Q5 (1 point)

**Question**

Which graph algorithm is commonly used to identify influential vertices?

**Options**

- a) K-Means
- b) PageRank
- c) Apriori
- d) Frequent Pattern Growth

**Answer:** **b**

**Why:** Lec 31/32/34 — PageRank scores vertices by the links pointing to them (links from many pages and from high-rank pages); the flight case study uses it to list the most influential airports.

---

## Q6 (1 point)

**Question**

Triangle Counting is mainly used for:

**Options**

- a) Sorting vertices
- b) Community detection
- c) Data compression
- d) Replication

**Answer:** **b**

**Why:** Lec 32/33 — counting triangles through a vertex measures the cohesiveness of its community: more triangles = a stronger community, fewer = weaker.

---

## Q7 (1 point)

**Question**

Which optimization reduces communication by avoiding unnecessary joins?

**Options**

- a) Join Elimination
- b) Data Duplication
- c) Replication Factor
- d) Hash Partitioning

**Answer:** **a**

**Why:** Lec 33 — join elimination identifies and bypasses the join for unused triplet fields (PageRank reads only the source attribute), giving about a 2× reduction in communication.

---

## Q8 (1 point)

**Question**

Which GraphX feature helps accelerate joins and construct subgraphs efficiently?

**Options**

- a) Bloom Filters
- b) Indexing and Bitmaps
- c) Commit Logs
- d) MemTables

**Answer:** **b**

**Why:** Lec 33 "Additional Query Optimizations" — indexing and bitmaps accelerate joins across graphs and efficiently construct subgraphs.

**Trap:** (c) and (d) are not GraphX features.

---

## Q9 (1 point)

**Question**

Which statement best describes GraphX?

**Options**

- a) Graph-only processing framework
- b) Batch-only processing framework
- c) Unified analytics framework for graph and data processing
- d) SQL replacement system

**Answer:** **c**

**Why:** Lec 32/34 — tables and graphs are composable views of the same physical data; GraphX unifies data-parallel and graph-parallel processing in one system.

---

## Q10 (1 point)

**Question**

Which GraphX optimization reuses routing tables, edge adjacency information, and indices across graphs and subgraphs?

**Options**

- a) Substantial Index and Data Reuse
- b) Active Edge Indexing
- c) Join Elimination
- d) Pregel Messaging

**Answer:** **a**

**Why:** Lec 33 — "Substantial index and data reuse: reuse routing tables across graphs and sub-graphs; reuse edge adjacency information and indices."

**Trap:** (b) active-edge indexing avoids scanning all edges each iteration; it is a different optimisation.

---

## Patterns this week

- Almost all questions come from Lec 32–33 (GraphX): goal, graph-parallel pattern, property graph, triplets, and the named optimisations.
- "Which is NOT" (Shuffle Sort) and "which operator" (triplets) style stems; the distractors come from MapReduce, NoSQL storage or other ML areas.
- Three look-alike optimisation names (join elimination, indexing and bitmaps, index and data reuse) each have a one-line job; the quiz swaps them.
- Algorithm-to-purpose pairs: PageRank → influential vertices, triangle counting → community cohesiveness.

## Tips for the final

- Likely rewordings: "which phase is part of graph-parallel pattern", "which operator returns edge with both vertices", "which optimisation reuses routing tables".
- Also expect Lec 30–31 items not covered by this assignment: pull vs push, SSP bounded staleness, PageRank damping factor 0.85 and initial 1/N, MapReduce PageRank re-shuffles the whole graph, Pregel supersteps.
- Do not memorise option letters; memorise each optimisation's job and the gather/apply/scatter order.
