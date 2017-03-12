#!/usr/bin/python3

chars_per_page = 7

lines = [line for line in open("story.txt", 'r')]
text = " ".join(lines)

binarystrings = ["{0:0>7}".format(int(str(bin(ord(char)))[2:] )) for char in text]

def applygradient(text, left):
	t = ""
	start = 60 if left else 20
	end   = 20 if left else 60
	for (i, c) in enumerate(text):
		pc = i / len(text)
		value = start + (end - start) * pc
		t += "{\\color{black!%d}%c}" % (int(value), c)
	return t

j = 0

while len(binarystrings):
	pagestring = ""
	for i in range(chars_per_page):
		pagestring += binarystrings[0]
		binarystrings = binarystrings[1:]
		if not len(binarystrings):
			break
	name = "binary%d.tex" % j
	f = open(name, 'w')
	f.write(applygradient(pagestring, (j % 2) == 0))
	f.close()
	j += 1
