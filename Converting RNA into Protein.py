#Text filed containing codon/protein pairs
infile = open("codons.txt", "r")

#Load Dictionary
codons = {}
for line in infile:
    if line [5] == "t":
        codons[line[0:3]] = " Stop"
    else:
        codons[line[0:3]] = line[4]

RNA = "AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGAUGA"
Protein = ""

x = 0
y = 3

while y < len(RNA):
    Protein = Protein + codons[RNA[x:y]]
    x += 3
    y += 3

print Protein
