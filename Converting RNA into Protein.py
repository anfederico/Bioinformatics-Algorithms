'''
Text file containing codon/protein pairs (per line)
For example...

UUU F      CUU L      AUU I      GUU V
UUC F      CUC L      AUC I      GUC V
UUA L      CUA L      AUA I      GUA V
UUG L      CUG L      AUG M      GUG V
UCU S      CCU P      ACU T      GCU A
UCC S      CCC P      ACC T      GCC A
UCA S      CCA P      ACA T      GCA A
UCG S      CCG P      ACG T      GCG A
UAU Y      CAU H      AAU N      GAU D
UAC Y      CAC H      AAC N      GAC D
UAA Stop   CAA Q      AAA K      GAA E
UAG Stop   CAG Q      AAG K      GAG E
UGU C      CGU R      AGU S      GGU G
UGC C      CGC R      AGC S      GGC G
UGA Stop   CGA R      AGA R      GGA G
UGG W      CGG R      AGG R      GGG G

'''

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

infile.close()

#Output looks something like this -> MAMAPRTEINSTRING Stop
