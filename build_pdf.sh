gsed -i 's/:width: 100%/:width: 156.25%/' *.ipynb
gsed -i 's/:width: 100%/:width: 156.25%/' *.md
gsed -i 's/:width: 64%/:width: 100%/' *.ipynb
gsed -i 's/:width: 64%/:width: 100%/' *.md
gsed -i 's/<!-- LATEX_ONLY_EMPTY_PARAGRAPH -->/\&nbsp; <!-- LATEX_ONLY_EMPTY_PARAGRAPH -->/' *.ipynb
gsed -i 's/<!-- LATEX_ONLY_EMPTY_PARAGRAPH -->/\&nbsp; <!-- LATEX_ONLY_EMPTY_PARAGRAPH -->/' *.md

uv run jupyter book build --pdf

gsed -i 's/:width: 100%/:width: 64%/' *.ipynb
gsed -i 's/:width: 100%/:width: 64%/' *.md
gsed -i 's/:width: 156.25%/:width: 100%/' *.ipynb
gsed -i 's/:width: 156.25%/:width: 100%/' *.md
gsed -i 's/\&nbsp; <!-- LATEX_ONLY_EMPTY_PARAGRAPH -->/<!-- LATEX_ONLY_EMPTY_PARAGRAPH -->/' *.ipynb
gsed -i 's/\&nbsp; <!-- LATEX_ONLY_EMPTY_PARAGRAPH -->/<!-- LATEX_ONLY_EMPTY_PARAGRAPH -->/' *.md

cp _build/exports/introduction.pdf how_phasors_work.pdf

pdftoppm -f 1 -l 1 -png how_phasors_work.pdf > img/pdf_page_1.png
pdftoppm -f 17 -l 17 -png how_phasors_work.pdf > img/pdf_page_2.png
pdftoppm -f 51 -l 51 -png how_phasors_work.pdf > img/pdf_page_3.png
