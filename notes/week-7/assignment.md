# Week 7 assignment

Answers below match the answers given in the paste, each checked against `notes/week-7/notes.md`.

## Q1 (1 point)

**Question**

Random Forest is best described as:

**Options**

- a) A single deep decision tree
- b) A clustering algorithm
- c) A neural network ensemble
- d) A bagging of de-correlated decision trees

**Answer:** **d**

**Why:** Lec 28 slide: "Random Forest algorithm is a bagging of de-correlated decision trees" (bootstrap samples + a random subset of features at each split).

---

## Q2 (1 point)

**Question**

What is the main purpose of Bagging?

**Options**

- a) Increase bias
- b) Reduce prediction variance
- c) Reduce dataset size
- d) Increase overfitting

**Answer:** **b**

**Why:** Lec 28 — bagging (bootstrap aggregation) averages many models, so noisy parts cancel; "bagging works because it reduces the variance of the predictions" (bias–variance trade-off).

---

## Q3 (1 point)

**Question**

Bootstrap in Bagging refers to:

**Options**

- a) Sampling with replacement
- b) Feature scaling
- c) Gradient computation
- d) Data normalization

**Answer:** **a**

**Why:** Lec 28 — a bootstrap dataset is a same-size replica of the data made by random sampling **with replacement** (rows may repeat or be missing).

---

## Q4 (1 point)

**Question**

In Random Forest, at each split:

**Options**

- a) All features are always evaluated
- b) Random subset of features is selected
- c) Features are ignored
- d) Only one feature exists

**Answer:** **b**

**Why:** Lec 28 — select m out of p input variables at random as split candidates (m = √p classification, p/3 regression); this is what makes the trees de-correlated.

**Trap:** (a) describes an ordinary decision tree.

---

## Q5 (1 point)

**Question**

Random Forest can naturally support parallel processing because:

**Options**

- a) Trees are built independently
- b) Trees share memory
- c) Trees use one processor
- d) Trees require sequential execution

**Answer:** **a**

**Why:** Lec 28 — each tree is trained on its own bootstrap sample independent of the others, so forests train in a distributed environment with a high degree of parallelism.

**Trap:** (d) describes boosting, where each tree depends on the previous one.

---

## Q6 (1 point)

**Question**

Boosting combines:

**Options**

- a) Strong classifiers only
- b) Weak classifiers into a strong ensemble
- c) Clusters into datasets
- d) Databases into warehouses

**Answer:** **b**

**Why:** Lec 29 slide: "Boosting is a method for combining outputs of many weak classifiers to produce a powerful ensemble."

---

## Q7 (1 point)

**Question**

Gradient Boosting builds models:

**Options**

- a) In a single step
- b) Iteratively
- c) Randomly
- d) Without training

**Answer:** **b**

**Why:** Lec 29 — the complex model is built iteratively; each step fits a simple tree to the current residuals (or gradients) and adds it to the ensemble.

---

## Q8 (1 point)

**Question**

In Gradient Boosted Trees, the base learners are usually:

**Options**

- a) Decision Trees
- b) Neural Networks
- c) K-Means Clusters
- d) Support Vectors

**Answer:** **a**

**Why:** Lec 29 — f(x) = h₁(x) + … + h_M(x) where each h_m is a decision tree.

**Trap:** (b) the lecture contrasts boosting with neural networks, which start from a very complex model.

---

## Q9 (1 point)

**Question**

Cross-validation is mainly used to:

**Options**

- a) Increase dataset size
- b) Assess model quality and select best parameters
- c) Reduce number of features
- d) Perform clustering

**Answer:** **b**

**Why:** Lec 29 — cross-validation "helps to assess the quality of a machine learning model and to find the best model among the family of models" (Spark: `CrossValidator` + `ParamGridBuilder`, e.g. maxDepth 1–8, 10 folds).

---

## Q10 (1 point)

**Question**

Recommended learning rate for Gradient Boosting is:

**Options**

- a) Greater than 1
- b) Equal to 5
- c) Less than or equal to 0.1
- d) Equal to 10

**Answer:** **c**

**Why:** Lec 29 GBT algorithm slide: v (regularization / learning rate) recommended ≤ 0.1; small steps, like gradient descent, need more iterations but give a better model.

---

## Patterns this week

- Straight definitions: random forest = bagging of de-correlated trees; boosting = weak into strong; bootstrap = with replacement.
- "Why" questions: parallelism (independent trees), bagging purpose (variance), CV purpose (quality + parameter selection).
- Single-number recall: learning rate ≤ 0.1.
- Wrong options are near-twins from the other ensemble family (sequential vs independent) or other ML areas (clustering, neural networks).

## Tips for the final

- Likely rewordings: "which method reduces variance", "which ensemble builds trees sequentially", "m for classification is √p", "entropy of a pure node is 0", "PLANET builds one tree level per MapReduce step".
- Also expect Lec 27 items (information gain, pure vs impure, ID3) since the assignment only touched Lec 28–29.
- Do not memorise option letters; learn the contrast bagging/random forest (independent, parallel, variance) vs boosting (sequential, weak learners, learning rate).
