---
name: craft-paper
description: Draft, edit, review, cite, and format academic research papers in LaTeX. Use when the user wants to write a paper, revise a draft, get a pre-submission review, fix citations, make figures or tables, or prepare a paper for a venue.
---

# Craft Paper

For agent dispatch and tool availability, follow [host compatibility](../../references/host-compatibility.md).

Draft, edit, and refine academic research papers with the user. The user owns the research and core claims; you ensure the manuscript meets top-tier publication standards for clarity, rigor, scholarly positioning, and venue compliance.

## Professional & Academic Standards

- **Scholarly Rigor & Tone:** Write at the standard of leading peer-reviewed venues in the field (e.g., NeurIPS, ICML, ACL, IEEE, ACM, Nature/Science). Tone is objective, precise, and restrained. Avoid hype (*unprecedented*, *groundbreaking*), empty boosterism, conversational chatter, and didactic throat-clearing.
- **Narrative Freedom:** Structure serves the paper's thesis. You and the user have full latitude to order, merge, or divide sections (e.g., positioning Related Work early to frame the problem or late to prioritize novel methods; integrating Preliminaries into Method or Discussion into Results; choosing descriptive vs. declarative headings).
- **Data & Claim Fidelity:** Claims must strictly match the empirical evidence or theoretical proofs. Never generalize beyond the studied sample or conditions. Distinguish established findings from conjecture. Every reported number must trace directly to raw experimental logs or data files; never invent or round away critical variance.
- **Idiomatic LaTeX & Typography:** Follow established scientific typesetting practices: clean math notation, vector graphics (`.pdf`) for plots, `booktabs` for tables (horizontal rules only; never vertical rules), decimal alignment via `siunitx`, and proper semantic citation commands (`\citet` for textual/subject, `\citep` for parenthetical).

## The Board

`paper/PAPER.md` tracks project state and decisions. Read it first when resuming and keep it current:

```markdown
# <working title>

## Venue
<Undecided, or: target venue, track, page limits, template, anonymity policy, required sections, and AI-disclosure rules — with the CFP URL and access date. Paper type and reporting guideline, if one applies.>

## Claims
<1–3 core falsifiable claims, one sentence each, with a pointer to the supporting section, figure, or data file>

## Outline

## AI use
<what was drafted, rewritten, or assisted by section, for disclosure>

## Notes
<open decisions and accepted or declined review items; not a changelog>
```

Consult the specialized references when writing or verifying:
- [style](references/style.md) — Anti-AI prose patterns, tone, precision, and statistical reporting.
- [citations](references/citations.md) — Identifier-based fetching, verification endpoints, and anti-stuttering.

## Workflow

### 1. Understand
Clarify the user's objective: drafting a new paper, revising existing text, conducting a pre-submission review, verifying citations, creating figures/tables, or preparing a final venue submission. Examine existing drafts, code, logs, and notes before asking questions. Settle the core claims and scope with the user before drafting.

Name the paper type (e.g., empirical study, clinical trial, systematic review, theory, humanities argument, position paper, software or dataset paper). When a reporting guideline applies (CONSORT, PRISMA, STROBE, and others on the EQUATOR Network), fetch its current version rather than recalling it.

### 2. Venue & Layout
- **Undecided Venue:** Draft in clean, single-column `\documentclass[11pt]{article}` with 1.5-inch side margins (about 80 characters per line) and author-year citations (`natbib` with `plainnat`).
- **Selected Venue:** Consult the venue's current call for papers and author kit. Adopt their official LaTeX template, obey page limits and anonymity requirements (double-blind / single-blind), and include all mandatory sections (e.g., Limitations, Impact Statements, Reproducibility Checklists).
- **Project Layout:** `paper/` holds `main.tex`, `sections/`, `refs.bib`, `figures/`, `scripts/`, `generated/`, `PAPER.md`, and a `latexmkrc` containing `$pdf_mode = 1; $aux_dir = '.build';` so build files stay out of the tree; add `.build/` to `.gitignore`. `latexmk` is the build, so never wrap it in a script. When figures or tables are generated from data, a short `Makefile` maps data and scripts to outputs, then calls `latexmk`.

### 3. Draft & Revise
- **Collaborative Outlining:** Outline the narrative progression around the key figures, tables, and empirical proofs before writing prose. Write the final abstract and title once results are stable.
- **Surgical Editing:** When editing, respect and maintain the author's voice. Improve clarity, precision, and conciseness while explaining non-obvious revisions.
- **Figures & Tables:** Scripts in `paper/scripts/` read the analysis outputs and generate figures and, for empirical papers, `generated/numbers.tex` with one macro per reported result; prose and tables use these macros, never typed numbers. Analysis code never writes paper artifacts. Size each figure at its final width in the paper's body font (8–9 pt) and embed fonts as TrueType (`pdf.fonttype=42` in matplotlib). Use colorblind-safe palettes (e.g., Okabe-Ito, viridis), explicit units on all axes, and defined error bars (SD, SE, CI with sample size $n$). A figure caption opens with the finding it supports, then explains how to read it.
- **Compilation:** Compile iteratively with `latexmk`, then render pages to PNG (`pdftoppm -r 110 -png`, or PyMuPDF via `uv run --with pymupdf`) and look at them; PDF text extraction hides overlaps, clipping, and font mismatches. Fix layout problems at their cause, never with `\resizebox`, negative `\vspace`, or `[H]`. If a LaTeX distribution is missing, confirm before installing TinyTeX.

### 4. Review
Dispatch a fresh `craft-paper-reviewer` subagent with the rendered page images, LaTeX sources, venue guidelines or reporting checklist, and raw data files. Address major findings and document accepted or declined feedback under Notes in `PAPER.md`. Stop after two review cycles and present remaining items to the user.

### 5. Finalize & Submit
Verify clean compilation (no undefined references, unresolved citations, or Type 3 fonts), confirm that all citations are verified, remove internal TODOs/comments, verify anonymization compliance if double-blind, and generate necessary AI disclosures from `PAPER.md`. For arXiv, copy `main.bbl` from `.build/` into `paper/` and package with `arxiv_latex_cleaner`, which strips comments and unused files.
