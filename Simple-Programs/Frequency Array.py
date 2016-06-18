import copy

string = 'ATCGTGTAACCGGTGGGACGCCCGGCGAGGCTGATCTGTCTATGCTCATTTCAGACCACTCGTAGCGAGCCTGTTCGTC'
k = 2 #k-mer size

nts = ['A','C','G','T']
kmers_one = ['A','C','G','T']
kmers_two = []
while k > 1:
    kmers_two = []
    for str in kmers_one:
        for nt in nts:
            temp = copy.deepcopy(str)
            temp += nt
            kmers_two.append(temp)
    k -= 1
    kmers_one = copy.deepcopy(kmers_two)
    
kmer_dict = {}    
for kmer in kmers_one:
    kmer_dict[kmer] = 0

k = 2
i = 0
while i < len(string)-k+1:
    kmer_dict[string[i:i+k]] += 1
    i += 1

for kmer in kmers_one:
    print kmer_dict[kmer],
    
#Output -> 1 4 4 4 3 5 8 6 5 6 5 7 3 8 6 3
