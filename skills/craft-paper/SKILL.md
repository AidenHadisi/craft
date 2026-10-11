---
name: craft-paper
description: Draft, edit, review, cite, and format academic research papers in LaTeX. Use when the user wants to write a paper, revise a draft, get a pre-submission review, fix citations, make figures or tables, or prepare a paper for a venue.
---

# Craft Paper

Write and revise research papers with the user. The user owns the claims; you make them clear, correct, and ready for the venue.

`paper/PAPER.md` is the board. Read it first when resuming and keep it current:

```markdown
# <working title>

## Venue
<Undecided, or: venue and track, page limit, template, anonymity, required sections, AI-disclosure rule — with the call-for-papers URL and the date you read it>

## Claims
<1–3 claims a reader could check and prove wrong, each with the evidence behind it>

## Outline

## AI use
<what you drafted or changed, by section>

## Notes
```

Read the reference that matches the work before doing it:

- [structure](references/structure.md) — outlining, drafting, or restructuring; section order by paper type and what each section must do
- [style](references/style.md) — any prose you write or edit
- [citations](references/citations.md) — adding, fixing, or checking references
- [figures](references/figures.md) — figures, tables, and reporting statistics
- [venues](references/venues.md) — choosing or switching a venue, anonymizing, AI disclosure, submission, camera-ready, rebuttals

## 1. Understand

Find out what the user wants: a new draft, an edit, a review, citations, figures, or venue formatting. Read their draft, results, code, and notes before asking anything.

For a new paper, settle the paper type and the claims with the user, and the venue if they know it. Do not draft until they approve the claims.

## 2. Venue

Until the user picks a venue, write in a plain single-column `article` with author-year citations, and leave venue-specific parts for later.

Once they pick one, read its current call for papers and author instructions. Never rely on memory; the rules change every year. Move `main.tex` onto the official LaTeX template, record the rules under Venue, and fit the paper to its page limit and required sections.

## 3. Write

For a new draft, outline around the figures and tables first and get the user's approval. Then write in evidence order: results, method, discussion, related work, introduction, and the abstract last. One file per section in `paper/sections/`.

For an edit, change only what needs changing and keep the author's voice. Say what you changed and why.

After each round of changes, compile with `latexmk -pdf` and look at the rendered pages. If LaTeX is missing, ask before installing TinyTeX.

## Rules

- **Numbers come from the user's data.** Every number traces to their results files or logs. If it is not there, ask; never estimate.
- **Citations are fetched, never written from memory.** Fetch each entry by identifier and confirm it with a second source, as [citations](references/citations.md) describes. If you cannot verify a reference, mark it in the text and tell the user.
- **Cite on introduction and in related work; avoid citation stuttering.** Cite each dataset, tool, or prior work when first introduced and in Related Work. Refer to it by name thereafter—never repeat parenthetical citations `(Author et al., Year)` every time the system or dataset is named.
- **Claims match the evidence.** Keep results from this study in the past tense instead of turning them into general truths. Label speculation as speculation.
- **Figures and tables come from the data.** Generate them by script and look at them rendered.
- **Write plainly.** Check every draft against the signs of AI prose in [style](references/style.md) — fix the patterns, and replace flagged words unless they are the right word.

## 4. Review

Dispatch a fresh `craft-paper-reviewer` with the compiled PDF, the LaTeX source, the Venue section, and the paths to the results data. Fix what it finds and record anything you decline under Notes. After a significant revision, dispatch a fresh reviewer. Stop after two rounds and show the user what remains.

## 5. Submit

Work through the submission checklist in [venues](references/venues.md), writing any AI disclosure from the AI use section.
