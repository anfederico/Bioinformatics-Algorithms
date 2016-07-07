import copy

def GenerateKmers(k):
    nts  = ['A','C','G','T']
    kmers = ['A','C','G','T']
    count = 0
    while count < k-1:
        kmers_temp = []
        for kmer in kmers:
            for nt in nts:
                kmers_temp.append(kmer+nt)
        kmers = copy.deepcopy(kmers_temp)
        count += 1
    return kmers    

def HammingDistance(genome, pattern):
    mismatch = 0
    i = 0
    while i < len(genome):
        if genome[i] != pattern[i]:
            mismatch += 1
        i += 1
    return mismatch

def ReverseComplement(DNAin):
    y = len(DNAin) - 1
    DNAout = ''
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
    return DNAout
    
genome = 'ACGTTGCATGTCGCATGAGCTAGCTTTGATGAGGATGAGCTTTGGAGCGCCCAAACTGCATGAGAGCT'
k = 5 #Length of k-mer
d = 2 #Max mismatches allowed

kmers = GenerateKmers(k)
most_frequent = {}

#Compute number of appearances of k-mer and its reverse compliment throughout genome
for kmer in kmers:
    j = 0
    while j < len(genome)-len(kmer)+1:
        kmer_rev = ReverseComplement(kmer)
        if HammingDistance(genome[j:j+len(kmer)],kmer) <= d:
            most_frequent.setdefault((kmer, kmer_rev),0)
            most_frequent[(kmer, kmer_rev)] += 1 
        
        if HammingDistance(genome[j:j+len(kmer_rev)],kmer_rev) <= d:
            most_frequent.setdefault((kmer, kmer_rev),0)
            most_frequent[(kmer, kmer_rev)] += 1 
        
        j += 1

#Find maximum values
output_ordered = [] 
values = []
for kmer in most_frequent:
    values.append(most_frequent[kmer])
for kmer in most_frequent:
    if most_frequent[kmer] == max(values):
        output_ordered.append(kmer)

#Seperate copies of (kmer/kmer_rev) and (kmer_rev/kmer)       
seperate = {}       
for pair in sorted(output_ordered):
    for kmer in pair:
        seperate[kmer] = 0

for kmer in seperate:
    print kmer,
    
#Output -> TGCTC GAGCA
