# Curriculum map (this PDF)

Source of truth: the book's INDEX (PDF pages 2–3). **Page No. is the footer number, not the PDF viewer page.**

Formula used by `scripts/extract_week.py`:

```
pdf_page (1-based) = footer_page + 3
```

That offset is the cover image plus two index pages. Lecture 1 footer 1 starts at PDF page 4.

Do not re-derive the whole index by reading the PDF. Use this file + the extractor.

Official NPTEL week titles are broader umbrellas. For notes, follow **this book's lecture list**.

| Week | Book lectures | Footer pages | PDF pages | NPTEL umbrella title |
| --- | --- | --- | --- | --- |
| 1 | 1–3 | 1–78 | 4–81 | Introduction to Big Data |
| 2 | 4–8 | 79–162 | 82–165 | Enabling Technologies / Hadoop |
| 3 | 9–12 | 163–255 | 166–258 | Big Data Platforms (Spark + KV) |
| 4 | 13–17 | 256–359 | 259–362 | Storage platforms |
| 5 | 18–22 | 360–472 | 363–475 | Streaming / fast data |
| 6 | 23–26 | 473–595 | 476–598 | ML applications |
| 7 | 27–29 | 596–694 | 599–697 | ML with Spark (trees / predictive) |
| 8 | 30–34 | 695–809 | 698–812 | Graph processing |

Last teaching footer is 809 (PDF 812). PDF 813 is a “not for sale” page. Ignore it.

## Lectures

### Week 1
1. Introduction to Big Data — footer 1
2. Big Data Enabling Technologies — footer 31
3. Hadoop Stack for Big Data — footer 51

### Week 2
4. Hadoop Distributed File System (HDFS) — footer 79
5. Hadoop MapReduce 1.0 — footer 107
6. Hadoop MapReduce 2.0 (Part-I) — footer 113
7. Hadoop MapReduce 2.0 (Part-II) — footer 129
8. MapReduce Examples — footer 139

### Week 3
9. Parallel Programming with Spark — footer 163
10. Introduction to Spark — footer 201
11. Spark Built-in Libraries — footer 230
12. Design of Key-Value Stores — footer 239

### Week 4
13. Data Placement Strategies — footer 256
14. CAP Theorem — footer 269
15. Consistency Solutions — footer 283
16. Design of Zookeeper — footer 293
17. CQL (Cassandra Query Language) — footer 339

### Week 5
18. Design of HBase — footer 360
19. Spark Streaming and Sliding Window Analytics (Part-I) — footer 381
20. Spark Streaming and Sliding Window Analytics (Part-II) — footer 405
21. Sliding Window Analytics — footer 430
22. Introduction to Kafka — footer 447

### Week 6
23. Big Data Machine Learning (Part-I) — footer 473
24. Big Data Machine Learning (Part-II) — footer 495
25. K-means using MapReduce — footer 563
26. Parallel K-means cluster analysis — footer 586

### Week 7
27. Decision Trees for Big Data Analytics — footer 596
28. Big Data Predictive Analytics (Part-I) — footer 635
29. Big Data Predictive Analytics (Part-II) — footer 658

### Week 8
30. Parameter Servers — footer 695
31. PageRank Algorithm in Big Data — footer 716
32. Spark GraphX & Graph Analytics (Part-I) — footer 732
33. Spark GraphX & Graph Analytics (Part-II) — footer 761
34. Case Study: Flight Data Analysis using Spark GraphX — footer 795

## How a lecture is laid out in the PDF

Most lectures open on a short title card that contains:

```
Big Data Computing
Prof. Rajiv Misra
Department of Computer Science
andEngineering,IIT Patna
```

Later lectures often add `Lecture NN` and the title on that same card. A few lectures (12, 24, 33, 34) do **not** use a clean title card. Always bound lectures by the footer map, not by searching for the professor line.

Teaching pages typically have:

1. A **slide image** in the upper half (diagrams, tables, definitions, architecture).
2. The **spoken transcript** under it.
3. Markers like `Refer slide time: (0:16)` or `(Refer Slide Time: 13:08)`.
4. The **footer page number** at the bottom.

Transcripts are oral and messy. Slides carry the exact terms NPTEL copies into quizzes. Both are required.

## Deliberate non-goals

- Do not load another week's cache or PDF range “for background”.
- Do not OCR or dump the entire 813-page file into context.
- Week 6 lecture 24 is long. Split it into learning parts; still stay inside week 6.
