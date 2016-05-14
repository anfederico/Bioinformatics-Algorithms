'''
Text file containg DNA sequences
For example...

>Seq_1
AGATGAGCACGTGCATTCTAAATAATCAAGCGCGATGTCCTACGTATAGTTGAGGTCTAC
GTACTATCAACCTACCCTTATGAATCGCTGTTCCATATCCAGAGGTCGTCTAGTGAACTC
TTAAGCAGGTTGCATGCCAAGATAGCGCCATACACGATGGTTTTCGGGTCGGCTCCGCGC
GGGTACACATATA
>Seq_2
CTGGCGGCAAAGCACCGAACCGTATACCGACGTGACGGTCGCATGCTTGATGCATTGCAC
GACAGAGGAGGAACTCCCTTTAGTGTAAGCACGAGCTCGACAGATAATTATAGATTTCTG
GCCTTTGACTATAACCCTTATGAATCGCTGTTCCATGGGCTCGCTCACAGAAGGTGTAGG
TGAACGTTGCGTGTGACGACGGGACGCAGGCCGCACGCCCCTACGTCGAGACACAGCTTA
GTCTACAAGTAGTTTGATGCATGTGTGGACTTGAGCCCCTTGGTAGGCTGTGTGGAAGGG
GGTTGATCATCGTTGTCATAATGCCGCGGAACAAACATATCCCCCATGTTCGGTCACCAA
>Seq_3
AGAAACCTCGTCGCCCCTCAGAATCACAGACCGAGGAGATGATAAATCCGTTAGTATAAA
CTCAGGTCTTACCCTTATGAATCGCTGTTCCATTACGCTGAGATTCTCTGCTCGAGAGAC
TGATTAATCCCTCCTTGTCTTTAACAAGATGCGCAGCCCTCGATTTACGCGGATTTACAC
>Seq_4
TTGCCATTGTCACCGGATCTACTATTTGATCCAGCATGGGGTTTCTTAATTCATTAAACA
ATATCCGGCTCTATCCCTCGGACGGCGTGAATGAACACTTTTGAGGGGACTTAATCCGAT
TTTTTATGGCCACTGACACCCTTATGAATCGCTGTTCCATCTTCATGGGCCGTTAGTATA
AACTCAGGTCTTTGCTCCACTTTGTTGTTGGTCTCTTTATTGATTTCCTACGCTGAGATT
GTGAGCTTGCTCGCTTGGAGCGAAAAA

'''

infile = open("strings.txt", "r")

temp_string = ""
strings = []
x = 0

#Load strings from text file
for string in infile:
    if string[0] != ">":    
        x = 1
        temp_string = temp_string + string
    if string[0] == ">":
        if x == 1:
            strings.append(temp_string)
        temp_string = ""
            

#Remove midstring line breaks
temp_strings = []
for string in strings:
    listing = list(string)
    for pos in range(0,len(listing)-1):
        if listing[pos] == "\n":
            listing[pos] = ""
        temp_string = "".join(listing)
    temp_strings.append(temp_string)
strings = temp_strings
ref = strings[0]
strings.remove(strings[0])

#Setup list for appending of all motifs
all_motifs = []

#Function for finding substrings between str and ref
def find_substrings(str, ref):
    motifs = []
    match = 0
    x = 0
    y = 1
    for j in range(0, 2):    
        while y < len(str):
            for i in range(0, len(str)):
                if str[i:i+len(ref[x:y])] == ref[x:y]:
                    match = 1
            if match == 1:
                if ref[x:y] != "\n":
                    motifs.append(ref[x:y])
                y += 1
                match = 0
            elif match == 0:
                x += 1
                y = x + 1
    return motifs

    
for seq in strings:
    all_motifs.append(find_substrings(seq, ref))

#Setup list for appending common motifs
common_motifs = []

for substring in all_motifs[0]:
    w = 0
    for part in all_motifs:
        w = 0
        for sub in part:
            if substring == sub:
                w = 1
    if w == 1:
        common_motifs.append(substring)
        
print max(common_motifs, key = len)

#Output looks something like this -> ACCCTTATGAATCGCTGTTCCAT
