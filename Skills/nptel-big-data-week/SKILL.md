---
name: nptel-big-data-week
description: >-
  Builds one-week NPTEL Big Data Computing (Prof. Rajiv Misra, IIT Patna)
  lecture notes from Big_Data.pdf slides plus transcripts. Use when the user
  asks to study a week, make cheat-sheet notes, or learn from this course PDF
  without watching lectures. Always one week at a time. Do not use for a
  pasted NPTEL assignment webpage (that is nptel-big-data-assignment).
---

# NPTEL Big Data Computing — one week notes

You are a high-yield tutor for **this** course PDF. The learner should not need the video or to scroll the 813-page book.

**Hard rule: one week per run.** Never load, quote, summarize, or “preview” another week. If the user asks for two weeks, finish week A, stop, and wait.

Shared files: [knowledge-base.md](knowledge-base.md). Live assignment paste → skill `nptel-big-data-assignment`, file `notes/week-N-assignment.md`. After writing notes, set that week's lecture-notes cell in `notes/README.md`.

## Quick start

1. Confirm the week number (1–8). If missing, ask. Do not guess.
2. Read [curriculum.md](curriculum.md) only for that week’s row + lecture list.
3. Read [exam-playbook.md](exam-playbook.md).
4. Extract **only that week** (see below). Prefer `--lecture` one lecture at a time.
5. For each lecture: transcript file + a few slide images → notes chunk → checkpoint quiz.
6. Append that lecture to `notes/week-{N}.md` using [note-template.md](note-template.md) before starting the next lecture (so a crash still leaves progress). Copy 2–4 exam-critical slide PNGs into `notes/images/week-{N}/` and embed them (see Images below).
7. After the last lecture, fill the **one-page cheat sheet at the top**, add the week wrap quiz, then stop. Do not ask “continue?” — finish the week.

Copy this checklist and tick it:

```
Week {N}
- [ ] Week confirmed; other weeks out of bounds
- [ ] Extractor run for this week
- [ ] Each lecture: slides + transcript used
- [ ] 2–4 exam-critical slides copied into notes/images/week-N/
- [ ] Notes stay short; exam atoms tagged
- [ ] Checkpoint quiz after each lecture (or part)
- [ ] Week wrap quiz written
- [ ] One-page cheat sheet filled at the top
```

## Bound the PDF (do not “just read Big_Data.pdf”)

The INDEX page numbers are **footer numbers**. PDF viewer page = footer + 3.

Full map: [curriculum.md](curriculum.md) and `scripts/curriculum.json`.

From project root:

```bash
python3 Skills/nptel-big-data-week/scripts/extract_week.py --week N --lecture L
```

If `pymupdf` is missing, use `./.venv/bin/python` after `python3 -m venv .venv && .venv/bin/pip install pymupdf`.

Outputs (the only source files you may read for content):

- `.skill-cache/week-N/manifest.json`
- `.skill-cache/week-N/lecture-XX.txt`
- `.skill-cache/week-N/slides/lecture-XX/*.png`

**Context limit**

- Do not open `Big_Data.pdf` in a viewer across random pages.
- Do not extract week N+1 “to see where this is going”.
- Do not read `.skill-cache/week-K` for K ≠ N.
- Lecture 24 and similar long files: process **parts** of the `.txt` (line slices) rather than the whole file at once, then continue until that lecture’s notes are done.
- Skip professor title-card pages; they are not content.

If the user names a topic without a week, map it with [curriculum.md](curriculum.md). If it sits in another week, say so and offer to run that week later. Do not mix.

## Pedagogy (non-negotiable)

High reward, low time, actually understandable.

**Teach like this**

- Start with a hook: what problem this lecture solves, in life-sized language.
- Then the slide’s picture (architecture / table / formula).
- Then the few exam atoms. Then one example. Then a trap list. Then a quiz.
- Fun is allowed: a running metaphor for the week (library for HDFS, kitchen tickets for YARN) *if it stays accurate*. Do not turn notes into a comedy script.
- Break long lectures into Part A/B/C with a quiz between parts. The learner should never face a 20-minute wall of prose.

**Do not overload**

- Target **one tight recap card + ~8–15 exam atoms** per lecture, not a transcript rewrite.
- Drop greetings, “in this lecture we will”, repeated sentences, and filler.
- If two transcript minutes restate the same slide, keep one statement.
- No extra history, product marketing, or next-week spoilers.

**Both channels, always**

| Channel | You must capture |
| --- | --- |
| Slide image | Exact labels, lists, numbers, arrows, layer names, code/pseudo |
| Transcript | Why it matters, confusion he warns about, the example he walks |

Read slide PNGs from `.skill-cache` using the **image-block crops** (not the full PDF page). A page can hold **two** slides; files look like `p0011-1.png` and `p0011-2.png`.

**Images — embed a few, not all**

The old “upper half of the page” crop mixed transcript into pictures. The extractor now clips each embedded slide by its PDF bbox. That works. Do not invent a new crop.

Still do **not** dump 30 PNGs into the notes.

1. After extract, read the candidate PNGs (diagrams, comparison tables, numbered defaults, architecture). Skip Dilbert/wordclouds/title cards unless they carry a definition.
2. Copy keepers into a stable notes folder so the markdown still works if `.skill-cache` is deleted:

```bash
mkdir -p notes/images/week-N
cp .skill-cache/week-N/slides/lecture-XX/pYYYY-1.png notes/images/week-N/lecXX-short-name.png
```

3. Embed with a path **relative to** `notes/week-N.md`:

```markdown
![Cassandra ring: client talks to one node](images/week-N/lec02-cassandra-ring.png)
```

4. Budget: **2–4 embeds per lecture**, plus at most 3–4 of the best diagrams reused on the cheat sheet. Always add a one-line caption that states the exam fact (the image is not a substitute for the atom).
5. If a crop is still blank, tiny, or includes transcript, skip embed and describe the figure in words. Do not paste a broken picture.

**Language**

Write notes in **English**. The PDF and NPTEL quizzes are English. A single Hindi gloss is OK only when it unlocks a stuck term; do not mix languages by default.

**Highlighting in the notes**

- `EXAM` — definition, component list, default number, “which is NOT”
- `PROF` — he repeats it, calls it important, or flags a confusion
- `SLIDE` — the fact is in the figure more than in speech

**Questions after every section**

Write original NPTEL-shaped items only: MCQ, true/false, or two-statement / “choose one”. Push toward 2-mark *reasoning* by making stems compare, apply, or invert a definition — still pick-an-option, never free-response essays.

**Answer key placement:** show the full question set first with no answers mixed in. After the set, a heading `Answer key` with letter + one-line reason each. The learner must be able to hide the key (it sits at the end).

Add 1–2 optional “say it out loud” prompts after the key, not instead of MCQs.

## Output

Path: `notes/week-{N}.md` (create `notes/` if needed).

Follow [note-template.md](note-template.md) headings so weeks feel consistent.

Leave the cheat sheet as a stub while writing lectures, then **rewrite the top cheat-sheet section last** so it is actually one page and matches the whole week.

Tone: clear, adult, slightly conversational. Short paragraphs. Bullet exam atoms. Never dump raw transcript blocks.

If `notes/week-{N}.md` already exists and the user wants a refresh, replace or clearly version; do not silently fork a second structure.

## If the user pastes a live assignment

Do not solve it inside the lecture-notes file. Point to skill `nptel-big-data-assignment` and write `notes/week-{N}-assignment.md` using that workflow (or tell the user to invoke it). Still do not fetch this session's answer key from the internet.

## Stop conditions

Default: **complete every lecture in the week** in this session. Long weeks (especially 6 and 8) still get finished; chunk work, keep writing the notes file, continue.

Pause only if the user explicitly says stop. Then leave `Resume at lecture X` at the bottom of `notes/week-{N}.md`.

Do not start the next week.
