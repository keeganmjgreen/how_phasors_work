# Build static HTML and PDF (Jupyter Book V1):
source .venv-jb1/bin/activate
jupyter-book build .
sed -i 's#!\[](img/cover.png)#<!-- ![](img/cover.png) -->#' 0_prelude.md
jupyter-book build . --builder=pdflatex
sed -i 's#<!-- !\[](img/cover.png) -->#![](img/cover.png)#' 0_prelude.md
pdfunite cover/cover.pdf cover/blank.pdf _build/latex/book.pdf how_phasors_work.pdf
