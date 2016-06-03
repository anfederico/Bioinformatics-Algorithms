#Nucleotide alphabet
NT = {'A':'a','C':'b','G':'c','T':'d'}
input = {}
k = 3 #length of k-mers

#Creates all possible k-mers from k=1 to k=9 in a dictionary paired with abcdef values for alphabetic ordering
input = {}
def combos(n):
    for a in NT:
        if n > 1:
            for b in NT:
                if n > 2:
                    for c in NT:
                        if  n > 3:
                            for d in NT:
                                if n > 4:
                                    for e in NT:
                                        if n > 5:
                                            for f in NT:
                                                if n > 6:
                                                    for g in NT:
                                                        if n > 7:
                                                            for h in NT:
                                                                if n > 8:
                                                                    for i in NT:
                                                                        if n > 9:
                                                                            pass
                                    
                                                                        else:
                                                                            input[a+b+c+d+e+f+g+h+i] = NT[a]+NT[b]+NT[c]+NT[d]+NT[e]+NT[f]+NT[g]+NT[h]+NT[i]                                            
                                                                else:
                                                                    input[a+b+c+d+e+f+g+h] = NT[a]+NT[b]+NT[c]+NT[d]+NT[e]+NT[f]+NT[g]+NT[h]                                         
                                                        else:
                                                            input[a+b+c+d+e+f+g] = NT[a]+NT[b]+NT[c]+NT[d]+NT[e]+NT[f]+NT[g]
                                                else:
                                                    input[a+b+c+d+e+f] = NT[a]+NT[b]+NT[c]+NT[d]+NT[e]+NT[f]
                                        else:
                                            input[a+b+c+d+e] = NT[a]+NT[b]+NT[c]+NT[d]+NT[e]
                                else:
                                    input[a+b+c+d] = NT[a]+NT[b]+NT[c]+NT[d] 
                        else:
                            input[a+b+c] = NT[a]+NT[b]+NT[c]          
                else:
                    input[a+b] = NT[a]+NT[b]
        else:
            input[a] = NT[a]
    
    import operator
    return sorted(input.items(), key=operator.itemgetter(1))

#Call to k-mer generating function
print combos(k)

#Output - > [('AAA', 'aaa'), ('AAC', 'aab'), ('AAG', 'aac'), ('AAT', 'aad'), ('ACA', 'aba'), ('ACC', 'abb'), ('ACG', 'abc'), ('ACT', 'abd'), ('AGA', 'aca'), ('AGC', 'acb'), ('AGG', 'acc'), ('AGT', 'acd'), ('ATA', 'ada'), ('ATC', 'adb'), ('ATG', 'adc'), ('ATT', 'add'), ('CAA', 'baa'), ('CAC', 'bab'), ('CAG', 'bac'), ('CAT', 'bad'), ('CCA', 'bba'), ('CCC', 'bbb'), ('CCG', 'bbc'), ('CCT', 'bbd'), ('CGA', 'bca'), ('CGC', 'bcb'), ('CGG', 'bcc'), ('CGT', 'bcd'), ('CTA', 'bda'), ('CTC', 'bdb'), ('CTG', 'bdc'), ('CTT', 'bdd'), ('GAA', 'caa'), ('GAC', 'cab'), ('GAG', 'cac'), ('GAT', 'cad'), ('GCA', 'cba'), ('GCC', 'cbb'), ('GCG', 'cbc'), ('GCT', 'cbd'), ('GGA', 'cca'), ('GGC', 'ccb'), ('GGG', 'ccc'), ('GGT', 'ccd'), ('GTA', 'cda'), ('GTC', 'cdb'), ('GTG', 'cdc'), ('GTT', 'cdd'), ('TAA', 'daa'), ('TAC', 'dab'), ('TAG', 'dac'), ('TAT', 'dad'), ('TCA', 'dba'), ('TCC', 'dbb'), ('TCG', 'dbc'), ('TCT', 'dbd'), ('TGA', 'dca'), ('TGC', 'dcb'), ('TGG', 'dcc'), ('TGT', 'dcd'), ('TTA', 'dda'), ('TTC', 'ddb'), ('TTG', 'ddc'), ('TTT', 'ddd')]
