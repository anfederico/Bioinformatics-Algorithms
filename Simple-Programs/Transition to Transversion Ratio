'''
Text file containing two strings to be compared
>String_1
CGCGAATTAAGTAACTATCACACAAGTCACGTAGACCTAATAGCACTCCAGCGCTGCAGC
GACCATATAATCGTGACGGCGAAGGACCCCTGCGCTTTAAGGTTTTCACGTTCCTTACAT
>String_2
CGCGAACTAAGCAGCCATCATACAGGTCTCTAGGACCTGACCGCGCTTAAACTCTGCAGC
GACTACATAATCGCCGTGACAAAGGACCCCTGCATTCTAACGTCTTCACGTACTTTATAT

'''

infile = open('s1s2.txt', 'r')
s1 = ''
s2 = ''
switch = 0
for line in infile:
    if line[0] == '>':
        switch += 1    
    if line[0] != '>':
        if switch == 1:
            s1 = s1 + line.rstrip('\n')
        if switch == 2:
            s2 = s2 + line.rstrip('\n')
    
list = {'G' : 'Pyr', 'A' : 'Pyr', 'C' : 'Pur', 'T' : 'Pur'}

transi = 0.00000
transv = 0.00000

for pos in range(0,len(s1)):
    if s1[pos] != s2[pos]:
        if list[s1[pos]] == list[s2[pos]]:
            transi += 1
        elif list[s1[pos]] != list[s2[pos]]:
            transv += 1
        
print (transi/transv)

#Output -> 2.77777777778
