all: laulukirja.pdf

.PHONY: clean
clean:
	git clean -fx

laulukirja.pdf: bits laulukirja.tex laulut.tex
	pdflatex laulukirja.tex && \
	pdflatex laulukirja.tex && \
	pdflatex laulukirja.tex

laulut.tex: to_latex.py ordering.csv lyrics.csv 
	python3 to_latex.py ordering.csv lyrics.csv > laulut.tex

.PHONY: ordering.csv lyrics.csv
ordering.csv lyrics.csv:
	./get_songs.sh

.PHONY: bits
bits:
	cd footer && ./story2binary.py && touch binary.tex