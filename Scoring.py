k = 4
list = ['CAGT', 'GTGT', 'TACC', 'ATCA', 'TCCA']

def score(list,k):
    AA = [0] * k
    CC = [0] * k
    GG = [0] * k
    TT = [0] * k
    x = 0
    y = 0
    consensus = ''
    
    for kmer in list:
        for i in range(0,len(kmer)):
            if kmer[i] == "A":
                AA[i] += 1
            elif kmer[i] == "C":
                CC[i] += 1
            elif kmer[i] == "G":
                GG[i] += 1
            elif kmer[i] == "T":
                TT[i] += 1
                
    for i in range(0,k):
        if AA[i] == max(AA[i],CC[i],GG[i],TT[i]):
            consensus = consensus + "A"
        elif CC[i] == max(AA[i],CC[i],GG[i],TT[i]):
            consensus = consensus + "C"
        elif GG[i] == max(AA[i],CC[i],GG[i],TT[i]):
            consensus = consensus + "G"
        elif TT[i] == max(AA[i],CC[i],GG[i],TT[i]):
            consensus = consensus + "T"
    
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
    
print score(list,k)

#Outpit -> 11
