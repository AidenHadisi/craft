---
name: craft-paper
description: Draft, edit, review, cite, and format academic research papers in LaTeX. Use when the user wants to write a paper, revise a draft, get a pre-submission review, fix citations, make figures or tables, or prepare a paper for a venue.
---

# Craft Paper

Draft, edit, and refine academic research papers with the user. The user owns the research and core claims; you ensure the manuscript meets top-tier publication standards for clarity, rigor, scholarly positioning, and venue compliance.

## Professional & Academic Standards

- **Scholarly Rigor & Tone:** Write at the standard of leading peer-reviewed venues in the field (e.g., NeurIPS, ICML, ACL, IEEE, ACM, Nature/Science). Tone is objective, precise, and measured. Avoid hype (*unprecedented*, *groundbreaking*), empty boosterism, conversational chatter, and didactic throat-clearing.
- **Narrative Freedom:** Structure serves the paper's thesis. You and the user have full latitude to order, merge, or divide sections (e.g., positioning Related Work early to frame the problem or late to prioritize novel methods; integrating Preliminaries into Method or Discussion into Results; choosing descriptive vs. declarative headings). The invariant is a cohesive, logical arc: Context $\to$ Problem & Gap $\to$ Core Insight/Contribution $\to$ Evidence & Evaluation $\to$ Limitations.
- **Data & Claim Fidelity:** Claims must strictly match the empirical evidence or theoretical proofs. Never generalize beyond the studied sample or conditions. Distinguish established findings from conjecture. Every reported number must trace directly to raw experimental logs or data files; never invent or round away critical variance.
- **Idiomatic LaTeX & Typography:** Follow established scientific typesetting practices: clean math notation, vector graphics (`.pdf`) for plots, `booktabs` for tables (horizontal rules only; never vertical rules), decimal alignment via `siunitx`, and proper semantic citation commands (`\citet` for textual/subject, `\citep` for parenthetical).

## The Board

`paper/PAPER.md` tracks project state and decisions. Read it first when resuming and keep it current:

```markdown
# <working title>

## Venue
<Undecided, or: target venue, track, page limits, template, anonymity policy, required sections, and AI-disclosure rules — with the CFP URL and access date>

## Claims
<1–3 core falsifiable claims, each paired with the supporting evidence/section>

## Outline

## AI use
<what was drafted, rewritten, or assisted by section, for disclosure>

## Notes
```

Consult the specialized references when writing or verifying:
- [style](references/style.md) — Anti-AI prose patterns, tone, precision, and statistical reporting.
- [citations](references/citations.md) — Identifier-based fetching, verification endpoints, and anti-stuttering.

## Workflow

### 1. Understand
Clarify the user's objective: drafting a new paper, revising existing text, conducting a pre-submission review, verifying citations, creating figures/tables, or preparing a final venue submission. Examine existing drafts, code, logs, and notes before asking questions. Settle the core claims and scope with the user before drafting.

### 2. Venue & Layout
- **Undecided Venue:** Draft in clean, single-column `\documentclass[11pt]{article}` with 1-inch margins and author-year citations (`natbib` with `plainnat`). Keep sections modular in `paper/sections/`.
- **Selected Venue:** Consult the venue's current call for papers and author kit. Adopt their official LaTeX template, obey page limits and anonymity requirements (double-blind / single-blind), and include all mandatory sections (e.g., Limitations, Impact Statements, Reproducibility Checklists).

### 3. Draft & Revise
- **Collaborative Outlining:** Outline the narrative progression around the key figures, tables, and empirical proofs before writing prose.
- **Surgical Editing:** When editing, respect and maintain the author's voice. Improve clarity, precision, and conciseness while explaining non-obvious revisions.
- **Figures & Tables:** Generate plots and tables from raw data via scripts. Plots must be legible at target column width, use colorblind-safe palettes (e.g., Okabe-Ito, viridis), include explicit units on all axes, and define error bars (SD, SE, CI with sample size $n$).
- **Compilation:** Compile iteratively with `latexmk -pdf` and visually inspect rendered output. If a LaTeX distribution is missing, confirm before installing TinyTeX.

### 4. Review
Dispatch a fresh `craft-paper-reviewer` subagent with the compiled PDF, LaTeX sources, venue guidelines, and raw data files. Address major findings and document accepted or declined feedback under Notes in `PAPER.md`. Stop after two review cycles and present remaining items to the user.

### 5. Finalize & Submit
Verify clean compilation (no undefined references, unresolved citations, or Type 3 fonts), confirm that all citations are verified, remove internal TODOs/comments, verify anonymization compliance if double-blind, and generate necessary AI disclosures from `PAPER.md`.
