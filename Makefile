all: laulukirja.pdf

.PHONY: clean
clean:
	git clean -fx

laulukirja.pdf: laulukirja.tex laulut.tex
	pdflatex laulukirja.tex && \
	pdflatex laulukirja.tex && \
	pdflatex laulukirja.tex

laulut.tex: to_latex.py ordering.csv lyrics.csv
	python3 to_latex.py ordering.csv lyrics.csv > laulut.tex

.PHONY: ordering.csv
ordering.csv:
	curl "https://docs.google.com/spreadsheets/d/\
	1D0C7BTZ5212Xf6xvW4ijLj7wICh74baMRTxJCnrqivY/pub?gid=0&single=true&output=csv" \
	> ordering.csv

.PHONY: lyrics.csv
lyrics.csv:
	curl "https://docs.google.com/spreadsheets/d/\
	1D0C7BTZ5212Xf6xvW4ijLj7wICh74baMRTxJCnrqivY/pub?gid=300077251&single=true&output=csv" \
	> lyrics.csv
