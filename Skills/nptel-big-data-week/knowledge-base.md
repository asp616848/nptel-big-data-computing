# Knowledge base (this course folder)

Both week-notes and week-assignment skills write here. One week at a time. English. Paths are from the project root.

Each week is a **self-contained folder**. Do not scatter that week's notes, assignment, or images across the `notes/` root.

```
notes/README.md                      ← index; update when a week folder is added
notes/week-{N}/notes.md              ← lecture notes + cheat sheet (notes skill)
notes/week-{N}/assignment.md         ← official weekly assignment Q + solutions (assignment skill)
notes/week-{N}/images/               ← embedded slide crops used by that week's notes.md
.skill-cache/week-{N}/               ← regenerable extract; not the knowledge base
```

| File | Owner skill | When |
| --- | --- | --- |
| `notes/week-N/notes.md` | `nptel-big-data-week` | Study the lectures |
| `notes/week-N/assignment.md` | `nptel-big-data-assignment` | After the user pastes that week's NPTEL assignment page |

Cross-links:

- Assignment write-up may cite `notes/week-N/notes.md` headings and lecture numbers from `Skills/nptel-big-data-week/curriculum.md`.
- Lecture notes must **not** copy the live assignment questions (those belong in the assignment file).
- Neither file may pull in another week's content. Do not read `notes/week-K/` for K ≠ N.

When updating `notes/README.md`, keep a short table: week, notes yes/no, assignment yes/no. Link into the week's folder.
