.PHONY: install
install:
	latexmk -pdf presentation.tex
	latexmk -c presentation.tex

.PHONY: watch
watch:
	latexmk -pvc presentation.tex

.PHONY: clean
clean:
	latexmk -C presentation.tex
	rm *.snm
	rm *.nav
	rm *.bbl

.PHONY: bibtool
bibtool:
	bibtool -R -r keep_bibtex -r field -r improve -r sort_fld -s references.bib -o references.bib

.PHONY: zip
zip:
	zip beamer-template -x *.git* -r .
