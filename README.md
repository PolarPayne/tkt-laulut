# tkt-laulut
**This project is now complete, the final PDF is a little bit
different, since some small changes were required to be done
by hand.** If you see this repo useful for you, please do
use it.

Laulattaako? No hätä, käpistelijät auttavat.

* Step 0: Install python >=3.4 and texlive-full
* Step 1: run `make`
* Step 2: ???
* Step 3: Profit!

# Data
All lyrics and ordering and everythingelse is within
two csv files, `lyrics.csv` and `ordering.csv`.
These files are automatically downloaded from Google Sheets.

The first line of these files is the header, and is skipped.
It should also tell quite well what to put in to the column.

## File format
`TODO`

# Song format
* Seperate verses with a single empty line.
* Use `:,: ` to signify a repeated part of a song
    (see `drunken_sailor` and many others).
* `# ` can be used to signify foresinger or similiar
    (see `kalmarevisan`).
* Songs with lots of very similiar verses,
    don't write every verse completely
    (see `henkilokunta`, and `kun_mä_kuolen` and many others).
* Extra directions usually inside parentheses.

# LaTeX
* Be careful with non-ascii non-finnish characters,
    they'll probably break the build.
* Be careful with math characters,
    they need to be surrounded with `\(` `\)`.
* For italics use `\textit{Text to be italized.}`
    (and textbf similarly for bold).
  * Each line has to have their own commands (because LaTeX)...
