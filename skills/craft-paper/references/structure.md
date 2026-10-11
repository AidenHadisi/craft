# Paper structure

## Core principles

- **One central contribution:** Express the core contribution consistently across title, abstract, introduction, and conclusion.
- **Falsifiable claims:** Frame 1–3 explicit claims supported directly by experiments or proofs.
- **Logic over chronology:** Order sections by argumentative progression, never the historical sequence of how the work was done.
- **Reader attention budget:** Invest disproportionate care in title, abstract, introduction, and figures.

## Section order by paper type

| Type | Order | Notes |
|---|---|---|
| Method (ML / CS) | Abstract; Introduction (contributions + Fig. 1); Background; Method; Experimental Setup; Results + Ablations; Related Work; Discussion & Limitations; Conclusion | Method begins by page 2. Put Related Work before Method only if the problem formulation requires extensive positioning. |
| Empirical / Benchmark Audit | Introduction (RQs + contributions); Background on audited artifact; Study Design; Results by RQ; Impact / Re-ranking; Discussion; Threats to Validity; Data Availability | Prioritize construct validity: does the benchmark measure what it claims to measure? |
| Replication Study | Summary; Introduction; Scope & Original Claims; Methodology (reused vs. reimplemented, compute); Results per claim; New findings; Discussion | Define "replicate" vs. "reproduce" explicitly. Distinguish direct from conceptual replication. |
| Workshop / Short Paper | Introduction (≤0.5 page, one claim); Setup; Results; Compact Related Work; Limitations | Single focused point; do not compress a long paper into mini-sections. |
| Survey / Synthesis | Introduction; Conceptual Taxonomy (ideally a figure); Thematic synthesis sections; Open challenges; Conclusion | Group thematically; never write a sequential paper-by-paper summary. |
| Theory | Introduction (informal theorem statements); Preliminaries; Core Results; Proof sketches; Full proofs in appendix | State all assumptions explicitly before theorems. |
| Position Paper | Plain statement of position in Title/Intro; Core arguments; Alternative views; Actionable implications | Address strong counter-arguments directly. |

## Section guidelines

### Title
Topic, then method or outcome (under ~15 words). Include distinctive system/dataset names when relevant. Avoid cute puns that obscure the topic, undefined acronyms, or noncommittal phrasing ("Towards...").

### Abstract
Five concise moves (typically 150–250 words; check venue limits):
1. Accepted context or problem space.
2. Specific open gap and why it is hard.
3. What this paper proposes or conducts.
4. Primary quantitative results with scale and metrics.
5. Concrete takeaway for the field.

No citations, raw equations, or undefined abbreviations.

### Introduction
1 to 1.5 pages. Move logically through:
1. The concrete problem and why it matters.
2. Why existing solutions fall short (positioning against the closest 1–3 works).
3. The proposed approach and the key insight.
4. Main empirical finding and primary limitation.
5. Contributions list.

Avoid generic openers ("In recent years...") and boilerplate section roadmaps ("The remainder of this paper is structured...").

### Contributions
2–4 concise bullets written with active verbs (*demonstrate*, *propose*, *release*). Each bullet must state a falsifiable claim or concrete artifact and link to the section with evidence (§X).

### Background vs. Related Work
Keep them distinct:
- **Background:** Core concepts, problem formalization, and notation needed to understand the method.
- **Related Work:** Thematic grouping of alternative approaches. Contrast their mechanisms and assumptions with your own to show the exact gap filled. Never relegate all related work to an appendix.

### Method
Begin with high-level intuition and an overview figure before introducing formal notation. Define inputs, outputs, and parameters for each component. Interleave technical descriptions with the rationale behind design choices. Reserve rejected alternatives for the appendix.

### Experimental Setup
Establish experimental credibility:
- Research questions motivating each experiment.
- Competitive, fairly tuned baselines (tuned with the same rigor as the proposed method).
- Dataset descriptions, splits, and selection criteria.
- Evaluation metrics, number of runs/seeds, and compute resources.
- If using LLMs (e.g., as evaluators), specify model versions, prompt templates, decoding parameters, and human alignment validation.

### Results
Organize subsections by research question or declarative finding ("Prompt caching cuts latency by 60%"), not chronological runs or tables. Connect text directly to figures and tables. Report negative results and ablation breakdowns with the same clarity as wins.

### Discussion & Limitations
Interpret results, explain unexpected outcomes, and relate findings back to the broader problem. Organize limitations by validity threats where appropriate:
- **Construct:** Does the measurement reflect the true construct?
- **Internal:** Are there confounding variables or leakage?
- **External:** To what settings, populations, or distributions does this generalize?
- **Statistical:** Are sample sizes, power, and tests appropriate?

Include the most significant vulnerabilities. Avoid dressing up planned future work as limitations.

### Conclusion & Back Matter
- **Conclusion:** Recapitulate the core finding and open questions in 2–3 sentences without repeating the abstract.
- **Back matter:** Acknowledgments, data/code availability (with persistent DOI, e.g., Zenodo), reproducibility checklist, and author contributions (CRediT format).

## Drafting habits

- Write the one-sentence contribution before drafting sections.
- Outline with one sentence per intended paragraph before generating prose.
- Draft a rough compass abstract early; rewrite it from scratch once results are finalized.
- Write the introduction twice: once to guide drafting, once after results are fixed.
- Revise by cutting filler and tightening claims against evidence.
