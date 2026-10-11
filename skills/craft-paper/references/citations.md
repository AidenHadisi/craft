# Citations

Typed BibTeX is wrong about half the time even with web search, and fabricated references now get papers desk-rejected and authors banned from arXiv. Every entry is fetched by identifier and checked.

## What to cite

- Any specific method, finding, dataset, software, figure, or claim not considered common knowledge.
- Quote verbatim text directly; do not lightly reword without attribution.
- Reusing your own text: methods boilerplate is acceptable if disclosed; never recycle results.
- Self-cite only when directly relevant, not to inflate metrics.

## What not to cite: Textbook math and standard statistics

- **Do not cite standard textbook math or century-old statistical tests.** Metrics taught in undergraduate curricula—such as Spearman rank correlation (1904), Pearson correlation, Student's $t$-test, Cohen's kappa (1960), Brier score (1950), Bayes' theorem, or Euclidean distance—do not need citations in computer science and AI papers. Citing them looks pedantic and signals AI drafting.
- **When to cite statistical methods:** Cite a statistical work only when discussing a specific, non-obvious methodological paradox (e.g., Feinstein & Cicchetti on the high-prevalence kappa paradox), a recently proposed test, or a domain-specific mathematical extension.

## Preprints and published versions

- Cite the peer-reviewed version once it exists.
- For a preprint, the year is the v1 year. Give the ID as `arXiv:YYMM.NNNNN`, with a version if you quote it.
- NeurIPS proceedings have no DOI: use the proceedings URL. ICLR papers live on OpenReview.

## Datasets, software, and AI tools

- Cite datasets and software as works, with a persistent identifier and the exact version. Read the repository's `CITATION.cff` if it has one. For Zenodo, cite the version DOI, not the concept DOI.
- An LLM is cited only when it is an object of study, as software: "OpenAI. (2023). *ChatGPT* (Mar 14 version) [Large language model]". AI help with the writing is disclosed in the paper's acknowledgments or dedicated AI disclosure section per venue policy, not cited as a reference.

## Citation frequency and placement

- **Cite on first mention, then refer by name.** Cite a paper, dataset, method, or software tool when it is first introduced (usually in the Introduction, Background, or Study Design) and in Related Work. Refer to it by name thereafter (e.g., "Ragas", "in \texttt{ragas}", "on RAGTruth").
- **Never re-cite on every mention.** Repeating parenthetical citations (`(Es et al., 2024)`, `(Niu et al., 2024)`) across subsequent paragraphs, results sections, discussion, table captions, or limitations is "citation stuttering". It clutters prose and signals automated drafting.
- **Re-cite only for distinct claims.** Only re-cite later in the text when attributing a specific, distinct finding or direct quote to that publication.
- **Tool name vs. author name:** When citing a software tool or dataset whose project name is better known than its lead author, attach parenthetical `\citep{key}` to the tool name (`Ragas \citep{ragas2024}`), rather than making `\citet{key}` the sentence subject (`\citet{ragas2024}` renders as "Es et al. (2024)", which can confuse readers who recognize the tool, not the author).

## Styles

| Style | Used by | LaTeX |
|---|---|---|
| natbib author-year | NeurIPS, ICLR, ICML, ACL/EMNLP/NAACL, TMLR | `natbib` with the venue `.bst` |
| IEEE numeric | IEEE journals and conferences, ICSE, MSR | `IEEEtran` |
| ACM numeric | ACM venues | `acmart` |
| APA 7 | psychology, education, social sciences, some HCI | `biblatex-apa` or `apacite` |
| Chicago author-date | social sciences, history | `biblatex-chicago` |
| Vancouver | biomedicine | varies |
| Springer | LNCS and Springer journals | `splncs04` |
| Undecided venue | — | `natbib` with `plainnat` |

- `\citet{key}` → "Devlin et al. (2019)", for a citation that is part of the sentence.
- `\citep{key}` → "(Devlin et al., 2019)", for a parenthetical citation.
- In numeric styles, do not make "[3]" the subject: "as shown in [3]", not "[3] shows".
- Protect capitals in BibTeX titles with braces: `{BERT}`, `{ImageNet}`, `{Bayesian}`. Styles lowercase everything else.
- DOIs as `https://doi.org/10.xxxx/...`.

## Finding and fetching

The model proposes which work supports a claim. It never types title, authors, venue, year, or DOI.

1. **Find candidates.** Follow the references and citations of papers already verified, or search. Use `craft-researcher` for broad related-work searches.
2. **Resolve each candidate to an identifier** (DOI, arXiv ID, PMID, ACL Anthology ID):
   ```bash
   # Semantic Scholar title match; a fabricated title returns 404 "Title match not found"
   curl "https://api.semanticscholar.org/graph/v1/paper/search/match?query=Attention+Is+All+You+Need&fields=title,year,authors,venue,externalIds"
   # Crossref bibliographic search
   curl "https://api.crossref.org/works?query.bibliographic=Attention+Is+All+You+Need+Vaswani+2017&rows=5&select=DOI,title,author,issued,container-title&mailto=<email>"
   ```
3. **Fetch the entry by identifier:**
   ```bash
   curl -LH "Accept: application/x-bibtex" https://doi.org/<doi>
   curl -LH "Accept: application/x-bibtex" https://doi.org/10.48550/arXiv.<id>   # arXiv: correct v1 year
   curl -L "https://export.arxiv.org/api/query?id_list=<id>"                      # journal_ref and published DOI
   ```
   ACL Anthology papers have a `.bib` link on their page.
4. **Confirm with a second source.** Title, first author, year (±1 across preprint and published), and venue must agree between two independent sources. If identity fields disagree, reject the entry rather than patching it.
5. **Swap preprints for the published version** when one exists: check arXiv `journal_ref`/`doi` and Semantic Scholar `venue`/`externalIds.DOI`.
6. **Check for retraction.**
   ```bash
   curl "https://api.crossref.org/works/<doi>?mailto=<email>"   # look for "updated-by"
   ```
   Cite a retracted work only when discussing the retraction.
7. **Confirm the source says what you cite it for.** Read the abstract or the relevant passage:
   ```bash
   curl "https://api.semanticscholar.org/graph/v1/snippet/search?query=<claim>&paperIds=ARXIV:<id>&limit=3"
   ```
   If the claim is specific (a number, a comparison) and you only have the abstract, flag it for the user.
8. **Escalate what you cannot verify.** Mark it in the text (`\textbf{[UNVERIFIED]}`) and tell the user. Theses, books, reports, blogs, and translated titles often fail automated checks while being real.

## Known traps

- **arXiv's own BibTeX export** (`arxiv.org/bibtex/<id>`) gives the latest revision's year. Use the `10.48550` DOI instead.
- **Crossref title search** can return re-deposited copies of famous papers under unrelated DOIs. Never accept a title-only match. Add `mailto=<email>` to every request.
- **OpenAlex** has merged unrelated records under one ID. Never use it as the only source.
- **Semantic Scholar** rate-limits requests without a key. If `S2_API_KEY` is set, send it as the `x-api-key` header.
- **arXiv API** allows one request every three seconds.
- **DBLP**'s search API blocks scripts; its SPARQL endpoint (`https://sparql.dblp.org/`) works.

Back off and retry on HTTP 429.
