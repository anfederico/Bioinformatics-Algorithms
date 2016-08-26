k = 4
list = ['CAGT', 'GTGT', 'TACC', 'ATCA', 'TCCA']

def score(list,k):
    AA = [0.0] * k
    CC = [0.0] * k
    GG = [0.0] * k
    TT = [0.0] * k
    
    aa = [0.0] * k
    cc = [0.0] * k
    gg = [0.0] * k
    tt = [0.0] * k
    TTotal = [0.0] * k
    
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
        TTotal[i] = AA[i]+CC[i]+GG[i]+TT[i]
        aa[i] = AA[i]/TTotal[i]
        cc[i] = CC[i]/TTotal[i]
        gg[i] = GG[i]/TTotal[i]
        tt[i] = TT[i]/TTotal[i]

    from math import log
    score = 0
    for i in range(0,k):
        if aa[i] == 0.0:
            score += 0
        else:
            score += (aa[i]*log(aa[i],2))
    
        if cc[i] == 0.0:
            score += 0
        else:
            score += (cc[i]*log(cc[i],2))
    
        if gg[i] == 0.0:
            score += 0
        else:
            score += (gg[i]*log(gg[i],2))
        
        if tt[i] == 0.0:
            score += 0
        else:
            score += (tt[i]*log(tt[i],2))
    
    return score*-1.

print score(list,k)

#Output -> 5.93673487912
