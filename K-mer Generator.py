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

print GenerateKmers(4)

#Output ->['AAAA', 'AAAC', 'AAAG', 'AAAT',...,'TTTA', 'TTTC', 'TTTG', 'TTTT']
