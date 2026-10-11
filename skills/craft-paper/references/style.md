# Style

The target venue's author instructions override anything here.

## Sentences and paragraphs

- **Direct structure:** State each paragraph's core point in its first sentence. Keep subject and main verb close together.
- **Focus on the subject, not the field:** Write about the phenomenon rather than the research activity ("Benchmark accuracy saturates within months", not "In recent years, researchers have focused on evaluation").
- **State facts directly:** Avoid announcing what a section will do ("This section discusses...") when you can state the question or finding directly.
- **Specific open questions:** Replace boilerplate ("more research is needed") with the precise unanswered problem.
- **Explain unfamiliar terms:** Gloss domain jargon concisely and define abbreviations on first use.

## Tense by section

| Content | Tense | Example |
|---|---|---|
| Prior work | past or present perfect | "Smith (2022) found"; "several studies have used" |
| Established facts | present | "Attention scales quadratically with length" |
| Your method and results | past | "We sampled 500 prompts"; "accuracy fell to 61%" |
| Interpretation and conclusions | present | "These results indicate" |
| Figures, tables, paper structure | present | "Table 2 shows"; "Section 3 describes" |

Never use future tense for the paper outline.

## Voice

Active voice with "we" is the default in most fields ("I" for a solo author; never "the author"). Use passive voice when the object or outcome is the primary focus and the actor is irrelevant.

## Claims and hedging

- Hedge intentionally, not reflexively. Replace vague qualifiers (*somewhat*, *fairly*, *relatively*) with explicit conditions, bounds, or confidence intervals.
- Every booster (*clearly*, *strongly*, *substantially*) requires a test, metric, or citation in the same sentence.
- Reserve "significant" strictly for statistical significance.
- Clearly separate findings from conjecture; label speculation explicitly ("We hypothesize...").
- Avoid suggestive anthropomorphic capability labels ("reasoning", "understanding", "human-level") unless formally operationalized and measured.

## Terms and abbreviations

- Define each key term at first use, then use that exact term consistently throughout the paper.
- Abbreviate only standard terms or those used three or more times. Redefine in the main text even if introduced in the abstract. Avoid abbreviations in headings.
- Do not invent acronyms for minor components or baselines.

## Numbers and statistics in prose

- Numerals for 10 and above and for any quantity with a unit; spell out numbers below 10 or when starting a sentence.
- Space between number and unit ("25 kg", "10 %" in SI; "10%" in APA). Match venue convention consistently.
- Uncertainty to at most two significant digits, estimate rounded to match: `84.7 ± 2.1`, never `84.732 ± 2.1`.
- Exact p-values (e.g., `p = .028`), with `p < .001` as the lower floor.
- Report tests as `t(32) = 2.94, p = .006, d = 0.81, 95% CI [0.60, 1.02]`. Statistical symbols italic, Greek letters upright.
- Fewer than 4 numbers belong in a sentence; 4–20 go in a table; larger sets belong in a figure.

## Math in prose

- Define every symbol at first use. Integrate formulas grammatically into the surrounding sentence.
- Use plain words rather than logical quantifiers (∀, ∃, ⇒) in prose; never begin a sentence with a math symbol.

## Precision and tone

- **No anthropomorphizing:** Models encode representations, optimize losses, or predict tokens; they do not "know", "believe", "decide", or "struggle". Do not personify studies ("we find", not "the study finds").
- **Literal and measured:** Avoid metaphors, scare quotes, and ungrounded novelty adjectives (*groundbreaking*, *unprecedented*, *revolutionary*). Let empirical results demonstrate value.
- **Direct verbs:** Use *is*, *has*, *measures*, *indicates*; avoid filler verbs like *serves as*, *stands as*, *represents*, *boasts*.

## Signs of AI prose

Fix the underlying structural pattern, not merely the vocabulary:

1. **Inflated significance:** Proclaiming "pivotal shifts" or "transformative leaps" → state the concrete empirical delta.
2. **Trailing participial clauses:** "..., highlighting the importance of X" / "..., underscoring the need for Y" → split into an evidence-backed sentence or delete.
3. **Contrastive boilerplate:** "Not only X, but also Y", "X is not simply A, it is B" → state the direct affirmative claim.
4. **Zero-tradeoff claims:** "without sacrificing accuracy" → report the actual empirical cost.
5. **Forced triads:** Reflexive sets of three adjectives or parallel clauses → state only the actual items.
6. **Formulaic connectives:** Overusing "Additionally", "Furthermore", "Moreover", "Notably" at sentence starts → rely on logical continuity.
7. **Empty summary closers:** "Overall, these findings underscore..." → conclude with the specific technical finding.
8. **Vague attribution:** "Studies have shown" without citation → cite exact work.
9. **Overgeneralization:** Expanding sample observations into universal present-tense truths → retain sample bounds and past tense.
10. **Bold-label bullet syndrome:** Fragmenting narrative prose into `**Label:** description` lists → write coherent paragraphs.
11. **Punctuation mannerisms:** Excessive em dashes or uniform punctuation → use standard varied punctuation.
12. **Uniform sentence length:** Identically metered sentences → vary sentence rhythm and length.
13. **Didactic throat-clearing:** "It is important to note that", "It is worth mentioning" → delete and state the point.
14. **Generic ungrounded prose:** Paragraphs devoid of numbers, citations, or falsifiable claims → ground with data or cut.
15. **Conversational residue:** "Certainly!", conversational transitions, or model cutoff disclaimers.

## Flagged words

A flagged word is not strictly banned, but treat it as a warning. Replace with direct technical wording unless it is the only accurate term:

- **Scientific buzzwords:** delve, underscore, showcase, meticulous, intricate, pivotal, realm, commendable, groundbreaking, unparalleled, unveil, unravel, multifaceted, interplay, nuanced, invaluable, noteworthy, burgeoning, foster, bolster, harness, elucidate, encapsulate, pave the way, shed light, garner, amidst, transformative, revolutionize, seamless, uncharted, unlock, elevate, empower, profound, poised, tapestry, testament, landscape, navigate, resonate, paramount.
- **Overused academic padding:** comprehensive, crucial, enhance, insights, notably, particularly, robust, key, essential, leverage, utilize, facilitate, ensure, novel, innovative, promising, remarkable, compelling, holistic.
- **Conversational and meta-commentary:** "this matters", "why X matters", "what comes next", "looking ahead", "adds another layer", "in practice", "arguably the most", "genuinely", "quietly", "meaningful", "thoughtful", "deliberate", "measured", "in a world where", "plays a crucial role", "in the realm of", "deep dive", "evolving landscape".

## Field differences

| Field | Voice | Conventions |
|---|---|---|
| ML / CS | active "we" | IEEE uses "Fig. 1" even at sentence start; report variance and seeds. |
| Psychology / Social Science (APA 7) | active ("I" solo, "we" coauthors) | Bias-free language; exact p without leading zeros (e.g., `p = .02`). |
| Biomedical (AMA) | active preferred | Capital italic *P*; 95% CI; "patients", not "cases". |
| Physical Sciences | active "we" | Strict SI units and nomenclature. |
