# PYQ: previous-year question bank

460 unique questions (590 asked in total) from the NPTEL *Big Data Computing* assignments of 2019, 2021, 2022, 2023, 2024 and 2025, plus the 2026 session from this repo's own `notes/week-N/assignment.md`.
Source PDFs (2019-2025): [Shivammittal13ai/Big-Data-Computing_NPTEL-2025](https://github.com/Shivammittal13ai/Big-Data-Computing_NPTEL-2025/tree/main/Assignments).

| File | What |
| --- | --- |
| `index.html` | Interactive bank. One file, works offline: just open it. |
| `bank.md` | Same content as a printable, greppable markdown file, grouped by week. |
| `questions.json` | Source of truth. One record per unique question. |
| `images/` | Figures that the questions refer to. |
| `scripts/` | Extraction and build pipeline (`run_all.sh` rebuilds everything). |

## Using `index.html`

- Filter by **year**, **week**, **topic**, **type** (MCQ / MSQ), or search the text. Filters combine.
- A question that came back in several years appears **once**. `asked 3x: 2019 W7, 2021 W7, 2022 W7` shows where; the year filter matches any of those years. Sort by *most repeated first* to see what the paper-setters like.
- **Browse** shows the answers. **Practice** hides them: click an option (MSQ: tick several, then *Check answer*). Saved questions and your right/wrong history stay in your browser's localStorage.
- *Needs review only* lists questions whose answer or text was solved, inferred or reconstructed by us (see below).

## Record format

```json
{ "id": "2023-W7-Q6", "week": 7, "year": 2023, "qno": 6, "type": "MCQ",
  "question": "...", "options": [{"k": "A", "text": "..."}], "answer": ["C"],
  "explanation": "",               // only when the source PDF had one
  "appearances": [{"id": "2019-W7-Q1", "year": 2019, "week": 7, "qno": 1}],
  "repeat": 4, "years": [2019, 2021, 2022, 2023], "weeks": [7],
  "topics": ["ML with Spark: trees & ensembles"], "flags": [], "images": [], "source": {"file": "...", "page": 54} }
```

`id` is the copy that is shown (the one with the fewest flags, latest year on a tie). Where several copies of a question exist, their answers were compared: all 92 repeated questions agree, which is a good check on the parsers.

## How the answers were obtained

| Years | Source layout | Answer |
| --- | --- | --- |
| 2019, Week 0 of 2023/24/25 | NPTEL portal printout | `Accepted Answers` line |
| 2021, 2022, 2023, 2025 (W1-8) | solution documents | the printed answer line |
| 2024 (W1-8) | solution document with no answer line | **read from the explanation text** (flag `answer-inferred-from-explanation`) |
| 2021 Week 0 | question paper only, no key | taken from the identical 2023 question, plus 2 solved by us |
| 2026 | `notes/week-N/assignment.md` | the answer in that file; weeks 3-5 had no key in the portal paste and were solved from the notes (flag `answer-solved`). The file's *Why* and *Trap* lines are kept as the explanation |

## Known gaps and judgement calls

- 2019 has no Assignment 3 in the source repo; 2022 has no Week 0.
- 2019 W2 Q3 is dropped: the printout lost its stem and options at a page break.
- A few 2019 questions were cut by page breaks; their options or stem were reconstructed (flags `options-reconstructed`, `options-from-2021-twin`, `stem-restored-from-2021-twin`). 2019 W5 Q10 (moving average) had its option tables as images; they were rewritten as text and the answer solved by us.
- 2021 W5 Q11 has the same kind of table options, rewritten as text.
- 2025 W0 Q5 prints the stem of Q4 twice; its stem was reconstructed from the options.
- 2024 W2 Q7: the source explanation marks both B and C as correct, so both are stored (MSQ).
- Four figures are included as images (`images/`): confusion matrix, PageRank graph, attribute table, temperature table.
- The manual patches live in `scripts/build_bank.py` (`fix_2019a`, `OVERRIDES`, `A2024`, ...). They are keyed to the parser output, so re-running against a changed source needs them re-checked.
