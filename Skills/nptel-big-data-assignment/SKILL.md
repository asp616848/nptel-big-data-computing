---
name: nptel-big-data-assignment
description: >-
  Turns a Cmd+A / Cmd+C paste of the NPTEL Big Data Computing weekly
  assignment webpage into a short questions-and-solutions markdown file
  for one week. Use when the user pastes assignment HTML/text, asks to
  save this week's quiz, or wants solutions for the live NPTEL assignment.
---

# NPTEL Big Data Computing — one week assignment

**New file, same knowledge base as the lecture-notes skill.** Do not regenerate lecture notes here.

Hard rule: **one week**. Week number comes from the user prompt. If missing, ask. Do not infer from leftover files of another week.

## Quick start

1. Confirm week N (1–8).
2. Read [paste-guide.md](paste-guide.md), then [assignment-template.md](assignment-template.md).
3. Read `Skills/nptel-big-data-week/knowledge-base.md` and that week's lecture list in `Skills/nptel-big-data-week/curriculum.md` only.
4. If `notes/week-{N}.md` exists, use it to justify answers. If it does not, reason from the paste plus (only if needed) `.skill-cache/week-{N}/` or a single-lecture extract for week N. Never open another week.
5. Write `notes/week-{N}-assignment.md`.
6. Update the table in `notes/README.md`.
7. Stop.

```
Week {N} assignment
- [ ] Week confirmed
- [ ] Paste parsed; chrome stripped
- [ ] Every question has Answer + short Why
- [ ] Portal “Accepted Answers” verified against this week’s ideas
- [ ] End notes: patterns + tips only
- [ ] notes/README.md ticked
```

## Output shape

Path: `notes/week-{N}-assignment.md`

To the point. One question after another. **Not** a second copy of the lecture notes.

- Clean stem + options.
- **Answer** first (letter or True/False).
- **Why** in 1–3 sentences, tied to a lecture idea / notes heading.
- **Trap** only when an option is a near-twin.
- After the last question: `## Patterns this week` and `## Tips for the final` (see template). That is the only discursive part.

Do not embed lecture slide images unless the assignment itself is about a figure that you actually have.

## Answers vs the portal

- If the paste includes `Accepted Answers`, start from that, then **check** it against this week's notes/slides. If they disagree, keep both: `Portal says X; notes/slides imply Y because …` and recommend Y only with a clear reason.
- If there is no accepted answer, solve it. Do not search the internet for this session's key.
- Do not copy last year's option letters. Options shuffle.

## Knowledge base

Lecture notes stay in `notes/week-{N}.md` (other skill). This file is the assignment layer. Cross-link, do not merge the two documents into one.

See `Skills/nptel-big-data-week/knowledge-base.md`.

## Tone

English, dense, exam-useful. No pep talk, no restating all four options as prose.
