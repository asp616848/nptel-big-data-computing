# Week 6 assignment

Answers below match the answers given in the paste, each checked against `notes/week-6/notes.md`.

## Q1 (1 point)

**Question**

Cluster analysis is primarily a:

**Options**

- a) Supervised learning technique
- b) Reinforcement learning technique
- c) Unsupervised learning technique
- d) Deep learning technique

**Answer:** **c**

**Why:** Lec 23/25 — clustering data has no target label, so cluster analysis and association analysis are the unsupervised techniques (notes: Lec 23 "Supervised vs unsupervised").

**Trap:** (a) classification and regression are the supervised ones.

---

## Q2 (1 point)

**Question**

What is the main goal of cluster analysis?

**Options**

- a) Predict future values
- b) Organize similar items into groups
- c) Classify labeled data
- d) Reduce storage space

**Answer:** **b**

**Why:** Lec 23/25 — the slide definition: "organize similar items in your dataset into groups" (segmentation).

**Trap:** (a) is regression/predictive analytics, (c) is classification.

---

## Q3 (1 point)

**Question**

Which similarity measure calculates straight-line distance between two points?

**Options**

- a) Manhattan Distance
- b) Cosine Similarity
- c) Euclidean Distance
- d) Hamming Distance

**Answer:** **c**

**Why:** Lec 25 similarity-measures slide: Euclidean = distance along a straight line between A and B.

**Trap:** Manhattan only moves along the axes (horizontal/vertical path); Hamming is not on the slide.

---

## Q4 (1 point)

**Question**

Which similarity measure is based on the angle between vectors?

**Options**

- a) Euclidean Distance
- b) Manhattan Distance
- c) Cosine Similarity
- d) Jaccard Distance

**Answer:** **c**

**Why:** Lec 25 — cosine similarity is the cosine of the angle between two vectors (normalised dot product), good for sparse document vectors.

---

## Q5 (1 point)

**Question**

What is a common application of cluster analysis?

**Options**

- a) Customer segmentation
- b) Sorting algorithms
- c) Compiler optimization
- d) CPU scheduling

**Answer:** **a**

**Why:** Lec 23/25 — customer segmentation is the headline application (also crime hotspots, weather patterns, news grouping).

---

## Q6 (1 point)

**Question**

Which algorithm is most commonly associated with cluster analysis?

**Options**

- a) Decision Tree
- b) Naïve Bayes
- c) K-Means
- d) Logistic Regression

**Answer:** **c**

**Why:** Lec 25/26 — K-means is the classical clustering algorithm taught this week; decision tree, Naïve Bayes and logistic regression are classification methods.

---

## Q7 (1 point)

**Question**

What is the first step of the K-Means algorithm?

**Options**

- a) Compute accuracy
- b) Select initial centroids
- c) Normalize output
- d) Remove outliers

**Answer:** **b**

**Why:** Lec 25 — select K initial centroids, then iterate (assign to closest centroid, recompute centroids as means).

---

## Q8 (1 point)

**Question**

Which metric is commonly used to evaluate K-Means clustering quality?

**Options**

- a) Accuracy
- b) Recall
- c) WSSE
- d) Precision

**Answer:** **c**

**Why:** Lec 25 — WSSE (within-cluster sum of squared error) is the sum of squared distances from each sample to its centroid. Accuracy/precision/recall need labels, which clustering does not have.

**Trap:** (a), (b), (d) are classification metrics from Lec 24.

---

## Q9 (1 point)

**Question**

If WSSE decreases, it generally indicates:

**Options**

- a) Better cluster compactness
- b) Worse clustering
- c) More classification errors
- d) Data loss

**Answer:** **a**

**Why:** Lec 25 — lower WSSE means samples sit closer to their centroids, i.e. more compact clusters. Slide caution: lower WSSE is numerically better, not automatically "more correct", and a bigger K always lowers it.

---

## Q10 (1 point)

**Question**

K-Means stops iterating when:

**Options**

- a) No changes occur in centroids
- b) Accuracy becomes 100%
- c) Dataset becomes empty
- d) Number of features decreases

**Answer:** **a**

**Why:** Lec 25 stopping criteria — no change in centroids (so no sample changes cluster), or relaxed: fewer than a threshold (e.g. 1%) of samples change clusters.

**Trap:** (b) clustering has no labels, so no accuracy.

---

## Patterns this week

- Straight definitions: unsupervised, goal of clustering, which measure is Euclidean vs cosine.
- Tool identity: K-Means is the clustering algorithm; WSSE is its quality metric.
- Algorithm-step recall: first step = select initial centroids; stop = centroids stop changing.
- Options that belong to supervised learning (accuracy, recall, precision, decision tree) appear as distractors.

## Tips for the final

- Likely rewordings: "which technique is unsupervised", "which measure uses the angle", "WSSE increases/decreases means…", "which parameter is chosen by the elbow method" (K).
- Do not memorise option letters; they shuffle. Memorise the slide nouns: centroid, WSSE, elbow, Euclidean/Manhattan/cosine.
- Also expect Lec 24 ideas on the final: overfitting vs underfitting, validation vs test, precision vs recall, and Lec 26's map = classify, reduce = recenter.
