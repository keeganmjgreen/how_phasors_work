# How Phasors Work

An electrical engineering book about phasors and applying AC circuit analysis to the electrical grid.

[Web](https://keeganmjgreen.github.io/how_phasors_work) | [PDF](https://raw.githubusercontent.com/keeganmjgreen/how_phasors_work/refs/heads/main/how_phasors_work.pdf)

![](img/pdf_fanout.png)

## Chapters

- [Introduction](https://keeganmjgreen.github.io/how_phasors_work/introduction/)<br>Basics of DC versus AC power and resistive versus reactive loads.

- [What is a Phasor?](https://keeganmjgreen.github.io/how_phasors_work/what-is-a-phasor/)<br>Relationship between sinusoids and phasors. Deriving the concept of phasors. Formal phasor transformation and notation.

- [Life With and Without Phasors: Example Circuit Analysis](https://keeganmjgreen.github.io/how_phasors_work/life-with-and-without-phasors/)<br>Seeing the benefits of phasors in practice over differential equations and the Laplace transform.

- [Complex Power and the Power Factor](https://keeganmjgreen.github.io/how_phasors_work/complex-power-and-the-power-factor/)<br>Deriving complex power and the power triangle from time-domain instantaneous power. Power factor and power factor correction.

- [Three-Phase Power](https://keeganmjgreen.github.io/how_phasors_work/three-phase-power/)<br>Motivation for three-phase power. Wye versus delta configurations. Three-phase power in the grid.

- [Grid Modeling](https://keeganmjgreen.github.io/how_phasors_work/grid-modeling/)<br>Bus injection model. Power flow, optimal power flow, economic dispatch, and unit commitment problems.

This book is a work in progress. Existing chapters will be revised, and new chapters will be added. Readers are encouraged to provide feedback in [Issues](https://github.com/keeganmjgreen/how_phasors_work/issues).

---

© 2025&ndash;2026 Keegan Green. Written without AI.

## Development

When authoring locally, preview the HTML version of the book using `uvx jupyter-book start`. Alternatively, run the "Start Jupyter Book (Web)" task in VS Code. Then, open the resulting URL (likely http://localhost:3000).

Build the final PDF version of the book using `source build_pdf.sh`. Alternatively, run the "Build PDF" task in VS Code. This converts the source files (`.ipynb`, `.md`) to `how_phasors_work.pdf` using Jupyter Book, MyST, and LaTeX.
