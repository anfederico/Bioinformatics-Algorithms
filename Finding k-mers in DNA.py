DNA = 'TCACGCAGCATCACGCAGCATGCTTCCGAGTGTAAAGGCCTGCTTCCGAGTGTAAAGGCCTGCTTCCGAGTCACGCAGCAAATCGATCCCTGCTTCCGAGAATCGATCCCAATCGATCCCTGCTTCCGAGTGCTTCCGAG'
k = 3
kmers = {} 

for i in range(0,len(DNA)-k):
    kmers[DNA[i:k+i]] = 0
        
for kmer in kmers:
    for i in range(0,len(DNA)):
        if kmer == DNA[i:len(kmer)+i]:
            kmers[kmer] += 1

import operator        
max_count = kmers[max(kmers.iteritems(), key=operator.itemgetter(1))[0]]
print "Count: " + str(max_count)
print "k-mers:",

for kmer in kmers:
    if kmers[kmer] == max_count:
        print kmer,
'''
Output
Count: 9
k-mers: CGA TCC
'''
