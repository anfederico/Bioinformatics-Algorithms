
'''
Text file containing codon/protein pairs (per line)
For example...
TTT F      CTT L      ATT I      GTT V
TTC F      CTC L      ATC I      GTC V
TTA L      CTA L      ATA I      GTA V
TTG L      CTG L      ATG M      GTG V
TCT S      CCT P      ACT T      GCT A
TCC S      CCC P      ACC T      GCC A
TCA S      CCA P      ACA T      GCA A
TCG S      CCG P      ACG T      GCG A
TAT Y      CAT H      AAT N      GAT D
TAC Y      CAC H      AAC N      GAC D
TAA Stop   CAA Q      AAA K      GAA E
TAG Stop   CAG Q      AAG K      GAG E
TGT C      CGT R      AGT S      GGT G
TGC C      CGC R      AGC S      GGC G
TGA Stop   CGA R      AGA R      GGA G
TGG W      CGG R      AGG R      GGG G

Text file containing pre-RNA and splice sites
>RNA_1
ATGGTCTACATAGCTGACAAACAGCACGTAGCAATCGGTCGAATCTCGAGAGGCATATGGTCACATGATCGGTCGAGCGTGTTTCAAAGTTTGCGCCTAG
>Intron_1
ATCGGTCGAA
>Intron_2
ATCGGTCGAGCGTGT

'''

RNA = open("splicing.txt", "r")
SPLICE = open("introns.txt", "w")

#Seperate the introns
x = 0
y = 0
for line in RNA:
    if y != 2:
        if line[0] == ">":
            y += 1
    if y == 2:
        SPLICE.write(line)
        
SPLICE.close()
RNA.close()

#Create mRNA (pre-RNA at this point) string
RNA = open("splicing.txt", "r")
mRNA = ""
for line in RNA:
    if x != 2:
        if line[0] == ">":
            x += 1
        else:
            mRNA = mRNA + line

#Remove internal line breaks
mRNA_listy = list(mRNA)
for pos in range(0,len(mRNA_listy)-1):
    if mRNA_listy[pos] == "\n":
        mRNA_listy[pos] = ""
mRNA = "".join(mRNA_listy)

#Load introns into list
SPLICE = open("introns.txt", "r")
introns = []
for line in SPLICE:
    if line[0] != '>':
        introns.append(line.rstrip('\n'))

#Splice those introns out to get your mRNA
for intron in introns:
    a = 0
    b = len(intron)
    while b < len(mRNA):
        if mRNA[a:b] == intron:
            mRNA = mRNA[:a] + mRNA[b:]
            a += 1
            b += 1
        else:
            a += 1
            b += 1

#Text file containing codon/protein pairs
infile = open("DNA_Codon_Table.txt", "r")

#Load dictionary
codons = {}
for line in infile:
    codons[line[0:3]] = line[4]

#Convert mRNA into Protein
Protein = ""
x = 0
y = 3
while y < len(mRNA):
    Protein = Protein + codons[mRNA[x:y]]
    x += 3
    y += 3

print Protein

#Output -> MVYIADKQHVASREAYGHMFKVCA


