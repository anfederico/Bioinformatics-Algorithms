from random import randint

DNA = []
infile = open('DNA.txt','r')
for line in infile:
    DNA.append(line.strip('\n'))

k = 15 #Length of k-mer
size = len(DNA)

#Returns the most probable kmer
def ProfileMostProb(string, k, a, c, g, t):
    KmersProb = []
    Probs = []
    for i in range(0,len(string)-k+1):
        kmer = string[i:i+k]
        prob = 1
        pos = 0
        for nt in kmer:
            if nt == 'A':
                prob = prob*a[pos]
            elif nt == 'C':
                prob = prob*c[pos]
            elif nt == 'G':
                prob = prob*g[pos]
            elif nt == 'T':
                prob = prob*t[pos]
            pos += 1    
        KmersProb.append({kmer:prob})
        Probs.append(prob)
    for pair in KmersProb:
        for kmer in pair:
            if pair[kmer] == max(Probs):
                return kmer
                
#Scores a set of kmers based on consensus scoring method
def Score(list, k):
    AA = [0]*k
    CC = [0]*k
    GG = [0]*k
    TT = [0]*k
    consensus = ''
    for kmer in list:
        for i in range(0,len(kmer)):
            if kmer[i] == 'A':
                AA[i] += 1
            elif kmer[i] == 'C':
                CC[i] += 1
            elif kmer[i] == 'G':
                GG[i] += 1
            elif kmer[i] == 'T':
                TT[i] += 1
    for i in range(0,k):
        if AA[i] == max(AA[i],CC[i],GG[i],TT[i]):
            consensus = consensus + 'A'
        elif CC[i] == max(AA[i],CC[i],GG[i],TT[i]):
            consensus = consensus + 'C'
        elif GG[i] == max(AA[i],CC[i],GG[i],TT[i]):
            consensus = consensus + 'G'
        elif TT[i] == max(AA[i],CC[i],GG[i],TT[i]):
            consensus = consensus + 'T'
    score = 0
    pos = 0
    for nt in consensus:
        for kmer in list:
            if kmer[pos] == nt:
                pass
            else:
                score += 1
        pos += 1
    return score

def GibbsMotifSampler(DNA, k, size):

    DNA_Ordered = {}
    numbers = 1
    for seq in DNA:
        DNA_Ordered[numbers] = seq
        numbers += 1
    
    #Pseudocounts
    A = [float(1)]*k
    C = [float(1)]*k
    G = [float(1)]*k
    T = [float(1)]*k
        
    #Probabilities
    a = [float(0)]*k
    c = [float(0)]*k
    g = [float(0)]*k
    t = [float(0)]*k
    Total = [float(0)]*k
    
    #Randomly select k-mers
    RandomKmers = []
    number = 1
    for seq in DNA:
        i = randint(0,len(seq)-k)
        RandomKmers.append({seq[i:i+k]:number})
        number += 1
    
    BestKmers = []
    for pair in RandomKmers:
        for kmer in pair:
            BestKmers.append(kmer)
    BestScore = Score(BestKmers,k)
    
    runs = 0
    while runs < 100:
        GoodKmers = []
        number = 1
        for seq in DNA:
            i = randint(0,len(seq)-k)
            GoodKmers.append({seq[i:i+k]:number})
            number += 1
    
        count = 0
        while count < 10:
            
            #Random roll
            roll = randint(1,size)
    
            #Adjust Frequencies
            A = [float(1)]*k
            C = [float(1)]*k
            G = [float(1)]*k
            T = [float(1)]*k
            for pair in GoodKmers:
                for kmer in pair:
                    if pair[kmer] != roll:
                        pos = 0
                        for nt in kmer:
                            if nt == 'A':
                                A[pos] += 1
                            elif nt == 'C':
                                C[pos] += 1
                            elif nt == 'G':
                                G[pos] += 1
                            elif nt == 'T':
                                T[pos] += 1
                            pos += 1  
    
            #Reprofile
            Total = [float(0)]*k
            for i in range(0,k):
                Total[i] = A[i]+C[i]+G[i]+T[i]
                a[i] = A[i]/Total[i]
                c[i] = C[i]/Total[i]
                g[i] = G[i]/Total[i]
                t[i] = T[i]/Total[i]
        
            for pair in GoodKmers:
                for kmer in pair:
                    if pair[kmer] == roll:
                        del pair[kmer]
                        pair[ProfileMostProb(DNA_Ordered[roll], k, a, c, g, t)] = roll
            Challenger = []
            for pair in GoodKmers:
                for kmer in pair:
                    Challenger.append(kmer)
            
            if Score(Challenger,k) < BestScore:
                BestKmers = Challenger
                BestScore = Score(BestKmers,k)
            
            count += 1    
        runs += 1
    
    return BestKmers
    
BestKmers = GibbsMotifSampler(DNA, k, size)       

#Formatting
for kmer in BestKmers:
    print kmer
print 'Score: ' + str(Score(BestKmers,k))
