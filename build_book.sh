jupyter-book build .
jupyter-book build . --builder=pdflatex
pdfunite cover/cover.pdf cover/blank.pdf _build/latex/book.pdf how_phasors_work.pdf
