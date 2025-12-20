# Build static PDF (Jupyter Book V1):
source .venv-jb1/bin/activate
git revert --no-edit 4bbbb54550655d4a5d7a9193ee4c04d1719cd2b8
jupyter-book build . --builder=pdflatex
pdfunite cover/cover.pdf cover/blank.pdf _build/latex/book.pdf how_phasors_work.pdf
git reset
git reset --keep HEAD~1
