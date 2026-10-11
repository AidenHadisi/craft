# Figures, tables, and statistics

## Geometry

Design each figure at its final size and include it at full width, so 8 pt in the figure is 8 pt on the page.

| Template | Column width | Text width | Body font |
|---|---|---|---|
| Undecided (`article`, 1 in margins) | — | 6.5 in | Computer Modern 11 pt |
| NeurIPS / ICLR | — | 5.5 in | Times 10 pt |
| TMLR | — | 6.5 in | Computer Modern Bright 10 pt |
| ICML | 3.25 in | 6.75 in | Times 10 pt |
| ACM `sigconf` | 3.33 in | 7.0 in | Libertine 9 pt |
| IEEEtran | 3.5 in | 7.16 in | Times 10 pt |
| ACL | 3.03 in | 6.30 in | Times 11 pt |

- Height follows content: about 0.4 in per category row plus 0.5 in for axes.
- Text in figures 7–9 pt at print size, never below 6 pt. Same font family as the body.
- Lines at least 0.5 pt.
- Vector PDF for plots; PNG at 300 dpi or more for raster images; JPEG only for photos.
- Fonts embedded as TrueType or Type 1, never Type 3.

## Figures

- One message per figure; the caption says what to see.
- Position on a common scale beats length, which beats angle, area, and color. For results: dot or point-range plots to compare models; lines only for an ordered x-axis; strip, box, or violin plots for distributions over seeds; heatmaps for confusion and agreement matrices; ROC and precision-recall curves with the AUC and its CI in the legend.
- With ten or fewer runs, plot every run as a point plus the mean and CI. For paired designs, plot the paired differences with their CI.
- Small multiples instead of more than about four overlaid series.
- Bars start at zero. Dot and line plots may be truncated to the meaningful range. One y-axis, no 3D graphics, no pie charts. Mark log scales in the axis label.
- Label every axis with units. No title inside the graphic; the caption is the title.
- Error bars always say what they are (SD, SE, or CI), how they were computed, and n.
- Each model or condition keeps the same color and marker in every figure.
- ACM wants `\Description{…}` alt text on every non-decorative figure.

## Color

- Categorical, Okabe-Ito: `#0072B2 #D55E00 #009E73 #CC79A7 #E69F00 #56B4E9 #F0E442 #000000`. Yellow and light blue only for fills. At most about five categorical colors.
- Sequential: viridis or cividis. Diverging: RdBu centered on a meaningful zero. Never jet or rainbow.
- Never color alone: add markers or line styles, prefer direct labels over a legend. The figure must survive grayscale.

## Matplotlib style

matplotlib 3.10.1 or later (3.10.0 crashes embedding some fonts in PDF).

```python
import matplotlib as mpl

COLUMN_WIDTH_IN = 3.25  # from the geometry table
OKABE_ITO = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#F0E442", "#000000"]

mpl.rcParams.update({
    "figure.figsize": (COLUMN_WIDTH_IN, 2.0),
    "figure.dpi": 100,                     # width × dpi must be an integer or the size drifts
    "figure.constrained_layout.use": True,
    "savefig.bbox": "standard",            # "tight" changes the final size
    "font.family": "serif",
    "font.serif": ["Times New Roman"],     # match the body font
    "font.size": 8, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.linewidth": 0.6, "lines.linewidth": 1.2, "lines.markersize": 4,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False,
    "axes.prop_cycle": mpl.cycler(color=OKABE_ITO),
    "image.cmap": "viridis",
    "pdf.fonttype": 42, "ps.fonttype": 42, # TrueType, never Type 3
})
```

Save as PDF, include with `\includegraphics[width=\columnwidth]{…}`, compile, and look at the rendered page.

## Tables

- Only three rules: `\toprule`, `\midrule`, `\bottomrule` (booktabs). Never vertical rules or double rules. Use `\cmidrule` under grouped headers and extra space between row groups.
- Units in the header (`Acc. (\%)`), never in the cells.
- Align numbers on the decimal point with `siunitx` `S` columns, rounded as [style](style.md) describes.
- Bold the best result only when its paired-difference CI against the runner-up excludes zero; otherwise bold all tied entries. Say what bold means in the caption.
- Captions self-contained: what is shown, n, what ± means, what bold means.
- Full-width tables in two-column layouts use `table*`.

```latex
\usepackage{booktabs,siunitx}
\sisetup{uncertainty-mode = separate}  % prints 84.7 ± 2.1 instead of 84.7(21)

\begin{table}[t]
  \caption{Agreement with human labels ($n = 1200$). Mean $\pm$ 95\% CI over 5 seeds.}
  \label{tab:judges}
  \centering
  \begin{tabular}{l S[table-format=2.1(2)] S[table-format=1.2]}
    \toprule
    Judge & {Acc. (\%)} & {$\kappa$} \\
    \midrule
    A & 84.7(21) & 0.71 \\
    B & 81.2(19) & 0.64 \\
    \bottomrule
  \end{tabular}
\end{table}
```

## Statistical reporting

- **Sources of variation:** name what was randomized (initialization, data order, sampling, prompts, test items). For closed API models, the test items may be the only source.
- **Runs:** fewer than five seeds is a red flag; bootstrap CIs need about ten runs to be reliable. Re-scoring the same checkpoint is not a new seed.
- **Best-of-N:** never report the best run, prompt, or seed without saying so. Say whether each number is a maximum, a mean, or a single run.
- **Intervals:** every headline number has an interval and the method behind it (t-interval, bootstrap with resample count, Clopper–Pearson for accuracy).
- **Comparisons:** compare models on the same items with paired differences, reporting the difference and its CI. Cluster standard errors when items come in groups.
- **Power:** decide the minimum effect you need to detect before running, not after.
- **Benchmark suites:** report the interquartile mean with stratified-bootstrap CIs and release per-run scores (rliable).
- **Effect sizes with CIs.** A p-value is not an effect size.
- **Tests:** name the test and check its assumptions. Paired t-test when the distribution is known; permutation or bootstrap for small data; McNemar for paired binary outcomes; Wilcoxon or sign test otherwise. No t-test on F1 or BLEU; do not treat cross-validation folds as independent.
- **Multiple comparisons:** correct across datasets or models (Holm or Benjamini–Hochberg).
- **Agreement:** say what was rated, by how many raters, on how many items, and how disagreements were resolved. Cohen's κ for two raters (weighted for ordinal labels), Fleiss' κ or Krippendorff's α for more. Report prevalence and raw percent agreement alongside κ, with a CI. Never compute several measures and report the best.
- **Release** raw per-run and per-item results, not only aggregates.
