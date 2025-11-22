jupyter-book build .
sed -i 's#!\[](img/cover.png)#<!-- ![](img/cover.png) -->#' 0_prelude.md
jupyter-book build . --builder=pdflatex
sed -i 's#<!-- !\[](img/cover.png) -->#![](img/cover.png)#' 0_prelude.md
pdfunite cover/cover.pdf cover/blank.pdf _build/latex/book.pdf how_phasors_work.pdf
