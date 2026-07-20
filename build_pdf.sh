gsed -i 's|!\[\](img/cover.jpg)|<!-- ![](img/cover.jpg) -->|' 0_prelude.md
gsed -i 's/:width: 100%/:width: 156.25%/' *.ipynb
gsed -i 's/:width: 100%/:width: 156.25%/' *.md
gsed -i 's/:width: 64%/:width: 100%/' *.ipynb
gsed -i 's/:width: 64%/:width: 100%/' *.md

uv run jupyter book build --pdf

gsed -i 's|<!-- !\[\](img/cover.jpg) -->|![](img/cover.jpg)|' 0_prelude.md
gsed -i 's/:width: 100%/:width: 64%/' *.ipynb
gsed -i 's/:width: 100%/:width: 64%/' *.md
gsed -i 's/:width: 156.25%/:width: 100%/' *.ipynb
gsed -i 's/:width: 156.25%/:width: 100%/' *.md

cp _build/exports/prelude.pdf how_phasors_work.pdf
