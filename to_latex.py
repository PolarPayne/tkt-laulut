#!/usr/bin/python3
from os import listdir
from os.path import isfile, join
from io import StringIO
from collections import OrderedDict
from sys import stderr
import re
import csv

# indentation and spacing
SONG_NUMBER_SEP = "\\hspace{2pt}"
SONGTITLE_INDENT = "20pt"
SONGTITLE_PRE_SKIP = "\\vspace{5pt}"
SONGTITLE_POST_SKIP = "\\[6pt]"
VERSE_SKIP = "10pt"
PURKKA_INDENT = "10pt"

index_blacklist = [line.strip() for line in open("index_blacklist.txt", "r")]

def index_hack(name):
    """Hack indexing to work with åäö."""
    prefix = name
    prefix = re.sub("[åÅ]", "zza", prefix, re.U)
    prefix = re.sub("[äÄ]", "zzb", prefix, re.U)
    prefix = re.sub("[öÖ]", "zzc", prefix, re.U)
    return prefix + "@" + name

def melody_hack(s):
    s = s.replace("säv. ", r"säv.\ ")
    s = s.replace("san. ", r"san.\ ")
    return s

def line_hack(line, is_line=True):
    """Replace problematic characters with latex commands."""
    if line is None:
        return line
    line = line.replace("#", "\\#")
    line = line.replace("%", "\\%")
    line = line.replace("&", "\\&")
    line = line.replace("|", "\\|")
    #line = line.replace("@", "\\@")
    line = line.replace("$", "\\$")
    line = line.replace("€", "\\euro{}")
    line = line.replace("+", "\\texttt{+}")
    line = line.replace(";,;", ":,:")
    line = line.replace(";:;", ":,:")
    line = line.replace(";.;", ":,:")
    line = line.replace(":;:", ":,:")
    line = line.replace(" :,:", "~:,:")
    line = line.replace("...", " \dots{} ")
    line = line.replace("\"", "''")
    #line = line.replace("~", "\\textasciitilde{}")
    line = line.replace("______", "\\underline{\hspace{12mm}}")
    line = line.replace("_____", "\\underline{\hspace{10mm}}")
    line = line.replace("____", "\\underline{\hspace{8mm}}")
    line = line.replace("___", "\\underline{\hspace{6mm}}")
    line = line.replace("__", "\\underline{\hspace{4mm}}")
    line = line.replace("_", "\\_")
    line = re.sub(r'\[?x(\d)\]?',r'$[\\times{}\1]$',line)

    if not is_line:
        return line

    # place :,: and # modifiers before line start
    if line.startswith(":,:"):
        line = "\\hspace{0pt-\\widthof{:,: }}" + line
    if line.startswith("\\# :,:"):
        line = "\\hspace{0pt-\\widthof{\\# }-\\widthof{:,: }}" + line
    elif line.startswith("\\# "):
        line = "\\hspace{0pt-\\widthof{\\# }}" + line
    elif line.startswith("A: "):
        line = "\\hspace{0pt-\\widthof{A: }}" + line
    elif line.startswith("B: "):
        line = "\\hspace{0pt-\\widthof{B: }}" + line
    elif line.startswith(r"\( \leftrightarrow \)"):
        line = r"\hspace{0pt-\widthof{\(\leftrightarrow\) }}$\leftrightarrow$"
        return line
    elif line.startswith(r"\( \updownarrow \)"):
        line = r"\hspace{0pt-\widthof{\(\updownarrow\) }}$\updownarrow$"
        return line
    elif line.startswith(r"\( \circlearrowleft \)"):
        line = r"\hspace{0pt-\widthof{\(\circlearrowleft\) }}$\circlearrowleft$"
        return line
    elif line.startswith(r"\( \searrow\swarrow \)"):
        line = r"\hspace{0pt-\widthof{\(\searrow\swarrow\) }}$\searrow\swarrow$"
        return line
    if line:
        line += "\\\\"
    return line


def generate_song(data):
    out = []

    title = line_hack(data["title"], False)
    melody = line_hack(data["melody"], False)
    lyrics = data["lyrics"]
    index = line_hack(str(data["number"]), False)

    # strip empty verses from song
    while len(lyrics) > 1 and not lyrics[-1][0]:
        lyrics = lyrics[:-1]

    out.append("%")
    out.append("% " + title)
    out.append("%")
    # set the section name to show in header
    out.append(("\\sectionmark{{{0}}}%").format(index))

    # wrap title and first verse in the same minipage to prevent pagebreak between them
    out.append("\\noindent\\strut\\hspace{{{0}}}\\begin{{minipage}}{{\\linewidth-{0}}}"
        .format(PURKKA_INDENT))
    out.append(SONGTITLE_PRE_SKIP)

    # song number offset by correct amount
    out.append("\\hspace{{{2}-\\widthof{{\\large\\bf {0}.{1}}}}}{{\\large\\bf {0}.{1}}}"
        .format(index, SONG_NUMBER_SEP, SONGTITLE_INDENT))

    # song title in parbox for line wrapping
    t = "\\parbox[t]{{0.85\\linewidth}}{{\\raggedright {{\\large\\bf {}}}".format(title)
    if melody is not None:
        t += "\\\\[2pt]\\small\\emph{{{0}}}\\{1}}}".format(melody_hack(melody), SONGTITLE_POST_SKIP)
    else:
        t += "\\{0}}}".format(SONGTITLE_POST_SKIP) # close \leftline\parbox
    out.append(t)

    # add index entry for title and any alternate titles
    for name in [title] + data["alternate_titles"]:
        if not (title in index_blacklist and name in index_blacklist):
           out.append("\\index{{{}}}".format(index_hack(name)))

    first = True

    for verse in lyrics:
        # start a new minipage if not the first verse
        if not first:
            out.append("\\noindent\\strut\\hspace{{{0}}}\\begin{{minipage}}{{\\linewidth-{0}}}"
                .format(PURKKA_INDENT))
        else:
            first = False

        # wrap lines in verse block
        out.append("\\begin{verse}")
        for line in verse:
            out.append("\t" + line_hack(line))
        out.append("\\end{verse}")

        # close minipage and add verse spacing
        out.append("\\end{minipage}\\\\[" + VERSE_SKIP + "]")

    if (data["story"]):
        out.append(
"""\\noindent\\strut
\\begin{{minipage}}{{\\linewidth}}
\\emph{{\\noindent {0} }}\\\\
\\end{{minipage}}""".format(line_hack(data["story"]), PURKKA_INDENT))

    return "\n".join(out)


def category_break(i):
    break_string = ""
    if i != '1':
        break_string += "\\input{category/break.tex}\n"
    break_string += "\\input{category/page%c.tex}\n" % i
    return break_string


def main(order_file, songs_file):
    order = OrderedDict()

    with open(order_file, "r", newline="") as f:
        f.readline()
        for row in csv.reader(f):
            for i, a in enumerate(row):
                row[i] = a.strip()

            if len(row[4]):
                alts = []
                for i in csv.reader(StringIO(row[4])):
                    for j in i:
                        alts.append(j)
            else:
                alts = []

            if row[5] in order:
                print("There is already a song with id: \"{}\".".format(row[5]), file=stderr)
                continue

            order[row[5]] = {
                "number": row[0] if len(row[0]) else None,
                "title": row[3],
                "melody": row[9],
                "alts": alts,
                "story": row[12],
                "category": row[7]
            }

    lyrics = {}
    with open(songs_file, "r", newline="") as f:
        f.readline()
        for row in csv.reader(f):
            lines = row[1].split("\n")
            lines = [i.strip() for i in lines]
            lines = "\n".join(lines)
            lines = lines.split("\n\n")
            lines[:] = [i.split("\n") for i in lines]
            lyrics[row[0].strip()] = lines

    count = 0
    data = []

    for i, d in order.items():
        if i not in lyrics:
            print("\"{}\" doesn't have lyrics.".format(i), file=stderr)
            exit(1)
            continue

        if d["number"] is None:
            number = count
        else:
            number = d["number"]
        count += 1

        title = d["title"]
        melody = "(" + d["melody"] + ")" if len(d["melody"]) else None

        data.append({
            "title": d["title"],
            "alternate_titles": d["alts"],
            "number": number,
            "melody": melody,
            "lyrics": lyrics[i],
            "story": d["story"],
            "category": d["category"]
        })

    category = None

    for i in data:
        song_category = i["category"]
        if not category or (song_category[0] != category[0]):
            category = song_category
            print(category_break(song_category[0]))
        print(generate_song(i))

if __name__ == "__main__":
    from sys import argv
    main(argv[1], argv[2])
