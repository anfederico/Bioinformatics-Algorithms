#Setup DNA Codon Table
infile = open("DNA_Codon_Table.txt", "r")

codons = {}
for line in infile:
    codons[line[0:3]] = line[4]

#Find reverse compliment
DNAin = "AGCCATGTAGCTAACTCAGGTTACATGGGGATGACCCCGCGACTTGGATTAGAGTCTCTTTTGGAATAAGCCTGAATGATCCGAGTAGCATCTCAG"
DNAout = ""

y = len(DNAin) - 1

while y > -1:
    if DNAin[y] == "A":
        DNAout = DNAout + "T"
    elif DNAin[y] == "T":
        DNAout = DNAout + "A"
    elif DNAin[y] == "C":
        DNAout = DNAout + "G"
    elif DNAin[y] == "G":
        DNAout = DNAout + "C"
    y = y - 1

DNA_f = DNAin
DNA_r = DNAout

Proteins = []
Protein = ""

#Start with forward
x = 0
y = 3
z = 0
w = 0

while y < len(DNA_f):
    if codons[DNA_f[x:y]] == "/":
        if w == 1:
            break
    if codons[DNA_f[x:y]] == "M":
        z = 1
        w = 1
    if z == 1:
        Protein = Protein + codons[DNA_f[x:y]]
    x += 3
    y += 3
Proteins.append(Protein)
Protein = ""

x = 1
y = 4
z = 0
w = 0

while y < len(DNA_f):
    if codons[DNA_f[x:y]] == "/":
        if w == 1:
            break
    if codons[DNA_f[x:y]] == "M":
        z = 1
        w = 1
    if z == 1:
        Protein = Protein + codons[DNA_f[x:y]]
    x += 3
    y += 3
Proteins.append(Protein) 
Protein = ""

x = 2
y = 5
z = 0
w = 0

while y < len(DNA_f):
    if codons[DNA_f[x:y]] == "/":
        if w == 1:
            break
    if codons[DNA_f[x:y]] == "M":
        z = 1
        w = 1
    if z == 1:
        Protein = Protein + codons[DNA_f[x:y]]
    x += 3
    y += 3
Proteins.append(Protein)   
Protein = ""
    
#Now with reverse
x = 0
y = 3
z = 0
w = 0

while y < len(DNA_r):
    if codons[DNA_r[x:y]] == "/":
        if w == 1:
            break
    if codons[DNA_r[x:y]] == "M":
        z = 1
        w = 1
    if z == 1:
        Protein = Protein + codons[DNA_r[x:y]]
    x += 3
    y += 3
Proteins.append(Protein)
Protein = ""
    
x = 1
y = 4
z = 0
w = 0

while y < len(DNA_r):
    if codons[DNA_r[x:y]] == "/":
        if w == 1:
            break
    if codons[DNA_r[x:y]] == "M":
        z = 1
        w = 1
    if z == 1:
        Protein = Protein + codons[DNA_r[x:y]]
    x += 3
    y += 3
Proteins.append(Protein)  
Protein = ""

x = 2
y = 5
z = 0
w = 0

while y < len(DNA_r):
    if codons[DNA_r[x:y]] == "/":
        if w == 1:
            break
    if codons[DNA_r[x:y]] == "M":
        z = 1
        w = 1
    if z == 1:
        Protein = Protein + codons[DNA_r[x:y]]
    x += 3
    y += 3
Proteins.append(Protein)  

print Proteins    

#Output -> ['MGMTPRLGLESLLE', 'M', '', 'M', 'M', 'MLLGSFRLIPKETLIQVAGSSPCNLS']
