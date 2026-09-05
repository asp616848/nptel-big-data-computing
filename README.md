# NPTEL Big Data Computing — Study Hub

[![NPTEL](https://img.shields.io/badge/NPTEL-Big%20Data%20Computing-blue)](https://onlinecourses.nptel.ac.in/noc26_cs55/preview)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**High-yield lecture notes, weekly assignment solutions, and Cursor AI skills** for the NPTEL course **Big Data Computing** (Prof. Rajiv Misra, IIT Patna).

Study a full week **without watching every lecture or scrolling the 813-page PDF**. Built for exam prep and weekly NPTEL assignments.

---

## If this helped you — star the repo

If these notes saved you time, **please [star this repository](https://github.com/asp616848/nptel-big-data-computing)** so other learners can find it. Stars help the project show up in search and keep it maintained.

**Contributions welcome** — see [CONTRIBUTING.md](CONTRIBUTING.md). Add notes for a new week, fix an answer, improve a diagram, or help with the Cursor skills.

---

## What's inside

| Path | What it is |
| --- | --- |
| [`notes/`](notes/) | Week-by-week lecture notes + assignment packs |
| [`notes/README.md`](notes/README.md) | Progress tracker — which weeks are done |
| [`Big_Data.pdf`](Big_Data.pdf) | Official course slide book (813 pages) |
| [`Skills/nptel-big-data-week/`](Skills/nptel-big-data-week/) | Cursor skill to **generate** lecture notes for one week |
| [`Skills/nptel-big-data-assignment/`](Skills/nptel-big-data-assignment/) | Cursor skill to turn a pasted NPTEL assignment into Q + solutions |

### Coverage

| Week | Topic | Notes | Assignment |
| --- | --- | :---: | :---: |
| 1 | Introduction to Big Data | ✅ | ✅ |
| 2 | Enabling Technologies / Hadoop | — | — |
| 3 | Big Data Platforms (Spark + KV) | — | — |
| 4 | Storage platforms | — | — |
| 5 | Streaming / fast data | — | — |
| 6 | ML applications | — | — |
| 7 | ML with Spark | — | — |
| 8 | Graph processing | — | — |

*Weeks 2–8 are open for [contributions](CONTRIBUTING.md).*

---

## Quick start — just read the notes

**No setup required.** Clone or download and open the markdown files.

```bash
git clone https://github.com/asp616848/nptel-big-data-computing.git
cd nptel-big-data-computing
```

1. Open [`notes/README.md`](notes/README.md) to see what's ready.
2. Read [`notes/week-1.md`](notes/week-1.md) — start with the **one-page cheat sheet** at the top.
3. After each lecture section, try the **checkpoint quiz** (answers are collapsed below).
4. Before the weekly NPTEL quiz, skim the cheat sheet + **near-twins table** (common wrong answers).
5. For assignment practice, open [`notes/week-1-assignment.md`](notes/week-1-assignment.md).

### How each week's notes are structured

Every `notes/week-N.md` follows the same shape:

1. **One-page cheat sheet** — 7 things to remember, near-twins, key numbers, exam diagrams.
2. **Week map** — which lectures matter for the exam.
3. **Per-lecture sections** — hook → concepts → slide crops → checkpoint quiz.
4. **Week wrap quiz** — mixed review at the end.

Budget about **60–90 minutes per week** if you only read the notes (no video).

---

## Using the Cursor AI skills (optional)

The skills automate note generation from `Big_Data.pdf`. You need [Cursor](https://cursor.com) and this repo cloned locally.

### 1. Install the skills

Copy (or symlink) both skill folders into your Cursor skills directory:

```bash
# Personal skills (available in every project)
mkdir -p ~/.cursor/skills
cp -R Skills/nptel-big-data-week ~/.cursor/skills/
cp -R Skills/nptel-big-data-assignment ~/.cursor/skills/
```

Or, for **project-only** skills, put them in `.cursor/skills/` inside this repo.

### 2. Set up Python (for PDF extraction)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Generate lecture notes for a week

In Cursor chat, ask something like:

> *"Use the nptel-big-data-week skill. Build notes for week 2."*

The skill will:

- Extract only that week's slides/text from `Big_Data.pdf`
- Write `notes/week-N.md` using the course templates
- Copy exam-critical diagrams into `notes/images/week-N/`
- Update the tracker in `notes/README.md`

**Rule:** one week per run — don't ask for multiple weeks at once.

Manual extract (if you want to preview slides before the agent runs):

```bash
python3 Skills/nptel-big-data-week/scripts/extract_week.py --week 2
# or one lecture:
python3 Skills/nptel-big-data-week/scripts/extract_week.py --week 2 --lecture 4
```

Output lands in `.skill-cache/week-N/` (gitignored; safe to delete and regenerate).

### 4. Solve a weekly NPTEL assignment

When the assignment opens on the NPTEL portal:

1. Open the assignment page in your browser.
2. **Cmd+A / Ctrl+A** → **Cmd+C / Ctrl+C** to copy the whole page.
3. In Cursor chat:

> *"Use nptel-big-data-assignment. Week 3. Here's the paste: …"*

The skill writes `notes/week-N-assignment.md` with **Answer + Why** for each question and updates the tracker.

See also: [`Skills/nptel-big-data-assignment/paste-guide.md`](Skills/nptel-big-data-assignment/paste-guide.md).

---

## Repo layout

```
.
├── README.md                 ← you are here
├── CONTRIBUTING.md           ← how to add weeks / fix answers
├── Big_Data.pdf              ← course slide book
├── requirements.txt          ← pymupdf for the extractor
├── notes/
│   ├── README.md             ← week completion table
│   ├── week-N.md             ← lecture notes + cheat sheet
│   ├── week-N-assignment.md  ← NPTEL assignment Q + solutions
│   └── images/week-N/        ← embedded slide crops
└── Skills/
    ├── nptel-big-data-week/       ← lecture-notes skill + extractor
    └── nptel-big-data-assignment/ ← assignment skill
```

---

## Course info

- **Course:** [Big Data Computing](https://onlinecourses.nptel.ac.in/noc26_cs55/preview) — NPTEL
- **Instructor:** Prof. Rajiv Misra, IIT Patna
- **Book:** `Big_Data.pdf` in this repo (footer page numbers + 3 = PDF viewer page)

---

## Disclaimer

- Notes and assignment write-ups are **community study aids**, not official NPTEL material.
- `Big_Data.pdf` is the course slide book; **enroll on NPTEL** for videos, exams, and certificates.
- Assignment answers can change when NPTEL shuffles options — always verify against that week's slides.
- Use these materials for learning. Don't share live exam keys during an active attempt.

---

## License

Notes, skills, and scripts in this repo: [MIT License](LICENSE).

Course slides (`Big_Data.pdf`) remain property of NPTEL / IIT Patna; included here for enrolled learners' convenience.

---

**Star ⭐ · [Contribute](CONTRIBUTING.md) · Share with classmates**
