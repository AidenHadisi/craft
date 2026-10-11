# Venues

Snapshot as of October 2026. Venues change their rules every year — read the current call for papers and author instructions before relying on any row here, and record the URL and date in `PAPER.md`.

## Undecided venue

Use `\documentclass[11pt]{article}` with 1 in margins and `natbib` with `plainnat`. When switching to the official template, the sections and `refs.bib` carry over; resize figures to the new widths and recheck the page count.

## Snapshot

| Venue | Columns | Limit | Template | Review | Notes |
|---|---|---|---|---|---|
| NeurIPS 2026 | 1 | 9 pages, +1 camera-ready | `neurips_2026.sty` (only template accepted; has workshop options) | double-blind | 16-item paper checklist mandatory; references, checklist, appendix do not count |
| ICLR 2027 | 1 | 9 pages, 10 at rebuttal and camera-ready | ICLR style | double-blind, open review | LLM use must be disclosed; significant use needs its own section |
| ICML 2026 | 2 | 8 pages, +1 camera-ready | `icml2026.sty`, LaTeX only, US Letter | double-blind | Impact statement required; format checker |
| TMLR | 1 | none | TMLR style file | double-blind, open review | Judged on claims supported by evidence and audience interest, not novelty; Reproducibility Certification available |
| ACL / ARR | 2 | long 8, short 4, +1 final | ACL style, A4 | double-blind | Limitations section mandatory; Responsible NLP checklist; captions below figures and tables |
| ICSE 2027 | 2 | 10 + 2 pages of references only | `IEEEtran` conference | double-anonymous | Open-science policy; fabricated references desk-rejected |
| MSR 2027 | 2 | 10 + 2 (short 4 + 1) | `IEEEtran` conference | double-anonymous | Data availability statement; archival repository; use a different title on arXiv |
| IEEE Software | typeset by IEEE | ≤ 4,200 words (each figure or table counts 250), ≤ 15 references, abstract ≤ 150 words | Word or LaTeX | single-anonymous by default | Three actionable insights for practitioners; editable source at final |
| ACM venues | `sigconf` 2, `acmsmall` 1 | per venue | `acmart` (`review`, `anonymous` options) | per venue | CCS concepts and keywords required; `\Description` alt text on figures; TAPS needs LaTeX source |
| Springer LNCS | 1 | per conference | `llncs` | per conference | One corresponding author; source files required |
| Elsevier | varies | per journal | `elsarticle` | per journal | Source in one flat folder at production |
| arXiv | any | none | any | moderated | TeX source preferred (gets an HTML version); CS review and position papers must already be peer-reviewed; 2 new submissions per month |

Workshops set their own limits in each call; most use the parent conference's template with a workshop option.

## Front matter

- **Title:** title case; plain text in the submission form.
- **Authors:** ordered by field custom — contribution order in ML, SE, and the sciences; often alphabetical in mathematics and theory. AI tools are never authors.
- **Affiliations, ORCID, corresponding author, equal contribution:** use the template's commands (`\icmlaffiliation`, `\icmlcorrespondingauthor`, `\icmlEqualContribution`; `acmart` `\affiliation`, `\orcid`, `\authornote`; `llncs` `\inst`, `\orcidID`; `IEEEtran` `\IEEEauthorblockN`, `\IEEEauthorblockA`). Never hand-format.
- **Keywords:** ACM `\ccsdesc` + `\keywords`; IEEE `IEEEkeywords` ("Index Terms"); LNCS `\keywords` inside the abstract; NeurIPS, ICLR, TMLR collect them in the submission form.
- **Preprints:** never say "under review at X". Use the template's preprint option (NeurIPS `preprint`, TMLR `preprint`).

## Captions

Table captions above, figure captions below at NeurIPS, ICLR, TMLR, ICML, IEEE, and LNCS. ACL puts captions below both; APA puts the number and title above both.

## AI-use disclosure

| Venue | Where | What |
|---|---|---|
| ICLR | in the paper and the submission form; a separate LLM-usage section for significant use | any use |
| NeurIPS | experimental setup, only when an LLM is part of the method | writing help is exempt; position track allows copy-editing only, with attestation |
| ICML | encouraged, no fixed place | — |
| ACL / ARR | Responsible NLP checklist item and Acknowledgements; rebuttals too | pure polishing exempt |
| ICSE, MSR, CAIN 2027 | Acknowledgements (calls quote older ACM text) | — |
| ACM (May 2026) | Methods, when AI is part of the research | writing help no longer requires disclosure |
| IEEE | Acknowledgements: tool, sections, level of use | do not use AI to edit references |
| Springer (incl. Empirical SE) | Methods | AI may not write results or discussion on its own |
| Elsevier | separate declaration | fixed template sentence |
| Science | cover letter plus Methods or Acknowledgements | — |

When the venue's call and the publisher disagree, follow the stricter one.

## Double-blind

- No author names, affiliations, acknowledgments, or grant numbers.
- Your own prior work cited in the third person ("Smith et al. show"); work under review elsewhere as "Anonymous" with an anonymized copy in the supplement.
- Code and data through an anonymizing proxy (anonymous.4open.science), on a frozen branch. No link shorteners or tracking hosts. Strip names and licenses from submitted code.
- Clear the PDF metadata (`\hypersetup{pdfauthor={}}`; the template's anonymous mode usually handles it).

## Before submitting

- Compiles cleanly with `latexmk -pdf`; no undefined references or citations in the log.
- Within the page limit by the venue's counting rules.
- Correct template, paper size, and options (anonymous or review mode).
- Every required section and checklist present, with section pointers where asked.
- AI use disclosed where the venue asks.
- No `[UNVERIFIED]` citation markers left.
- No placeholders, TODOs, comments meant for the author, or chatbot text in the PDF.
- No hidden or white text and no instructions aimed at AI reviewers anywhere, including metadata.
- Fonts embedded (`pdffonts paper.pdf` shows no "no" in the emb column, no Type 3).
- Artifacts archived with a DOI, README with exact run steps, license.
- Journals: a one-page cover letter (problem, findings, fit; not under review elsewhere; all authors approve).

## Camera-ready

Restore acknowledgments and funding; add competing interests and lay summary where required; replace arXiv citations with published versions; de-anonymize links; use the extra page. Authors may be reordered but not added or removed at most venues.

## Rebuttal

Read the venue's limits first (ARR: 5,000 characters per response, any link means desk rejection; NeurIPS: 10,000 characters, no links or files). Open with a general response to shared concerns. Quote each concern and answer it with evidence and a section pointer. Fix factual misunderstandings first. Concede valid points with specific, checkable changes. When a criticism matches a known invalid pattern ("not novel" with no reference), say so neutrally. Disclose AI drafting where required.
