def BWTConstruction(Text):
    #Find cyclic suffixes
    Suffixes = []
    i = 0
    while i < len(Text):
        Suffixes.append(Text[i:]+Text[:i])
        i += 1

    #Construct BWT from last char of sorted cyclic suffixes
    BWT = ''    
    Suffixes = sorted(Suffixes)
    for suffix in Suffixes:
        BWT += suffix[len(suffix)-1]

    return BWT

def BWTReconstruction(BWT):
    #Sort BWT to find FirstColumn
    BWT_list = []
    for nt in BWT:
        BWT_list.append(nt)
    BWT_list = sorted(BWT_list)

    #Assign IDs to nts
    FirstColumn = []
    LastColumn = []
    Index = {'A':1, 'C':1, 'G':1, 'T':1, '$':1}
    for nt in BWT_list:
        FirstColumn.append(nt+str(Index[nt]))
        Index[nt] += 1
    Index = {'A':1, 'C':1, 'G':1, 'T':1, '$':1}
    for nt in BWT:
        LastColumn.append(nt+str(Index[nt]))
        Index[nt] += 1
    
    #Reconstruct
    Invert = []
    Length = len(FirstColumn)-1
    Find = '$1'
    while len(Invert) < Length:
        for i in range(len(LastColumn)):
            if LastColumn[i] == Find:
                Invert.append(FirstColumn[i])
                Find = FirstColumn[i]
    
    #Formatting
    Text = ''
    for char in Invert:
        Text += char[0]
    Text += '$'

    return Text

def Compress(text):
    #Run-length encoding
    i = 1
    k = 1
    S = text[0]
    TextCompressed = ''
    TextCompressedList = []
    while i < len(text):
        if text[i] == S:
            k += 1
            S = text[i]
            i += 1
        else:
            TextCompressed += str(k)+S
            TextCompressedList.append((k,S))
            k = 1
            S = text[i]
            i += 1
    TextCompressedList.append((k,S))        
    TextCompressed += str(k)+S   
    
    return TextCompressed, TextCompressedList
    
def Decompress(CompressedTextList):
    #Run-length decoding
    TextDecompressed = ''
    for pair in CompressedTextList:
        TextDecompressed += pair[0]*pair[1]

    return TextDecompressed

'''==============[Demonstration]=============='''

#Short string of nts with a small CpG island to display utility        
Text = 'ATTATCCCTCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCCGCGCTTATATACGCCTGGTCA$'
print 'Original Text'
print Text

#A BWT naturally converts CpGs into repeating C's and G's
#Very useful for run-length encoding a full genome
BWT =  BWTConstruction(Text)
print 'Constructed BWT'
print BWT

#Run-length encoding
BWTCompressed, BWTCompressedList = Compress(BWT)
print 'Compressed BWT'
print BWTCompressed

#Run-length decoding
BWTDecompressed = Decompress(BWTCompressedList)
print 'Decompressed BWT'
print BWTDecompressed

#Inverse BWT
TextReconstructed = BWTReconstruction(BWT)
print 'Reconstructed Text'
print TextReconstructed

'''
Output

Original Text
ATTATCCCTCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCCGCGCTTATATACGCCTGGTCA$
Constructed BWT
ACTTTT$TTGCGGAGGGGGGGGGGGGGTCGCCGCCCCCCCCCCCCCCCCCCTGAATTGACCCA
Compressed BWT
1A1C4T1$2T1G1C2G1A13G1T1C1G2C1G18C1T1G2A2T1G1A3C1A
Decompressed BWT
ACTTTT$TTGCGGAGGGGGGGGGGGGGTCGCCGCCCCCCCCCCCCCCCCCCTGAATTGACCCA
Reconstructed Text
ATTATCCCTCGCGCGCGCGCGCGCGCGCGCGCGCGCGCGCCGCGCTTATATACGCCTGGTCA$

'''
