# Contributing

Thank you for helping fellow NPTEL learners. Every week you add or fix makes this repo more useful.

## Ways to contribute

| You can… | How |
| --- | --- |
| Add notes for week 2–8 | Use the `nptel-big-data-week` skill or follow the templates in `Skills/nptel-big-data-week/` |
| Add assignment solutions | Paste from the NPTEL portal + use `nptel-big-data-assignment` |
| Fix a wrong answer | Edit `notes/week-N-assignment.md` with **Answer**, **Why**, and cite the slide/lecture |
| Improve notes | Typos, clearer explanations, better near-twin rows, missing diagrams |
| Improve skills | Edit `Skills/*/SKILL.md` or the extractor in `Skills/nptel-big-data-week/scripts/` |

## Before you open a PR

1. **One week per change** when possible — easier to review.
2. **Don't mix weeks** in a single notes file.
3. **Verify assignment answers** against that week's slides in `Big_Data.pdf`, not random web sources.
4. If the portal's "Accepted Answers" disagrees with the slides, document both (see existing assignment files).
5. Copy 2–4 exam-critical slide PNGs into `notes/images/week-N/` when adding lecture notes.
6. Update the table in [`notes/README.md`](notes/README.md).

## File conventions

### Lecture notes — `notes/week-N.md`

Follow [`Skills/nptel-big-data-week/note-template.md`](Skills/nptel-big-data-week/note-template.md):

- One-page cheat sheet at the top
- Per-lecture sections with checkpoint quizzes
- Week wrap quiz at the end
- Embed images from `notes/images/week-N/` only

### Assignments — `notes/week-N-assignment.md`

Follow [`Skills/nptel-big-data-assignment/assignment-template.md`](Skills/nptel-big-data-assignment/assignment-template.md):

- Clean question stem + options
- **Answer** then **Why** (1–3 sentences)
- `## Patterns this week` and `## Tips for the final` at the end

### Images

Name slides descriptively: `lec04-namenode-blocks.png`, not `p0042-1.png`.

## Pull request workflow

```bash
git checkout -b week-3-notes
# … make your changes …
git add notes/week-3.md notes/images/week-3/ notes/README.md
git commit -m "Add week 3 lecture notes"
git push origin week-3-notes
```

Open a PR on GitHub with:

- Which week(s) you touched
- Whether you used the Cursor skill or wrote manually
- Anything you're unsure about (conflicting portal answers, etc.)

## Using the skills to contribute

If you have Cursor set up (see [README.md](README.md#using-the-cursor-ai-skills-optional)):

```text
"Use nptel-big-data-week. Build notes for week 4."
```

```text
"Use nptel-big-data-assignment. Week 4. [paste]"
```

Review the agent's output, fix anything off, then PR.

## Code of conduct

Be helpful and accurate. No posting live exam questions during an active exam window. Credit fixes in PR descriptions — we all learn from each other.

---

Questions? Open a [GitHub issue](https://github.com/asp616848/nptel-big-data-computing/issues).
