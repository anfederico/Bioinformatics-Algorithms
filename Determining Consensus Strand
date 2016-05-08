'''
Text file containing ID and Sequence (one line each)
Simple example...(sequences can be much longer)

>Seq_1
ATCCAGCTGTCCGACCCT
>Seq_2
GGGCAACTTTCCGACTTT
>Seq_3
ATGGATCTATCGGACTCT
>Seq_4
AAGCAACCATCGGACTTT
>Seq_5
TTGGAACTCTGGTACTCT
>Seq_6
ATGCCATTTCCGATCACA
>Seq_7
ATGGCACTACTGGGTCCA

'''

infile = open("in.txt", "r")

A = 0
C = 0
G = 0
T = 0

x = 0
y = 0

consensus = ""
a = ""
c = ""
g = ""
t = ""

lines = []

start = 0
z = -1

for line in infile:
    if line[0] == ">":
        lines.append(line)
        start = 1
        z += 2
    else:
        if start == 1:
            lines.append(line)
            start = 0
        elif start == 0:
            lines[z] = lines[z] + line
            
    
while x < (len(lines[1])-1):
    while y < len(lines):
        if lines[y][0] != ">":
            if lines[y][x] == "A":
                A += 1
            elif lines[y][x] == "C":
                C += 1
            elif lines[y][x] == "G":
                G += 1    
            elif lines[y][x] == "T":
                T += 1
            y += 1
        else:
            y += 1
            
    if A == max(A,C,G,T):
        consensus = consensus + "A"
    elif C == max(A,C,G,T):
        consensus = consensus + "C"
    elif G == max(A,C,G,T):
        consensus = consensus + "G"
    elif T == max(A,C,G,T):
        consensus = consensus + "T"

    a = a + " " + str(A)
    c = c + " " + str(C)
    g = g + " " + str(G)
    t = t + " " + str(T)
           
    x += 1
    y = 0
    A = 0
    C = 0
    G = 0
    T = 0

print("Consensus: "+ consensus + "\n")

topofmatrix = "   "
for base in consensus:
    topofmatrix = topofmatrix + base + " "
print(topofmatrix + "\n")
print("A:" + a)
print("C:" + c)
print("G:" + g)
print("T:" + t)

infile.close()

'''
Output

Consensus: ATGCAACTATCGGACTCT

   A T G C A A C T A T C G G A C T C T 

A: 5 1 0 0 5 5 0 0 3 0 0 0 1 5 0 1 0 2
C: 0 0 1 4 2 0 6 1 1 2 5 2 0 0 6 2 5 0
G: 1 1 6 3 0 1 0 0 1 0 1 5 5 1 0 0 0 0
T: 1 5 0 0 0 1 1 6 2 5 1 0 1 1 1 4 2 5

'''
