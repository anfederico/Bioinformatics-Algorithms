from copy import deepcopy

infile = open('AA_MassTablet', 'r')
aa = {}
for line in infile:
    aa[line[0]] = line[2:].strip('\n')
infile.close()

#Ideal experimental spectrum
SpectrumIdealTemp = '0 71 97 99 101 101 113 114 129 131 163 186 202 202 211 227 228 230 230 234 260 287 299 301 324 329 331 331 359 365 374 388 400 413 430 430 445 460 462 464 487 501 510 514 517 531 558 561 561 576 593 611 615 616 630 632 673 675 689 690 694 712 729 744 744 747 774 788 791 795 804 818 841 843 845 860 875 875 892 905 917 931 940 946 974 974 976 981 1004 1006 1018 1045 1071 1075 1075 1077 1078 1094 1103 1103 1119 1142 1174 1176 1191 1192 1204 1204 1206 1208 1234 1305'
SpectrumIdeal = SpectrumIdealTemp.split()

def LinearSpectrum(peptide):
    #Find the linear spectrum of the peptide
    peptides = []
    sizes = ['0']
    peptides.append(peptide)
    n = len(peptide)
    for window in range(1,n):
        for i in range(0,n-window+1):
            peptides.append(peptide[i:i+window])
    for string in peptides:
        total = 0
        for aminoacid in string:
            total += int(aa[aminoacid])
        sizes.append(str(total))
    return sizes
    
def CheckCompatibility(SpectrumCheck, SpectrumIdeal):
    #Check compatibility with the ideal spectrum
    temp = deepcopy(SpectrumIdeal)
    compatibility = True
    for SpecProt in SpectrumCheck:
        present = 0
        for SpecNum in temp:
            if SpecProt == SpecNum:
                present = 1
        if present == 1:
            temp.remove(SpecProt)
        if present == 0:
            compatibility = False
            return compatibility
    return compatibility

def FindMass(spectrum):
    temp = []
    for num in spectrum:
        temp.append(int(num))
    temp = sorted(temp)
    return temp[len(temp)-1]

def IdealSequencing(SpectrumIdeal):
    #Find correct mass of the ideal spectrum
    CorrectMass = FindMass(SpectrumIdeal)
    
    Combos = [] #Store potential peptides
    Correct = [] #Store correct peptides
    for letter in aa:
        Combos.append(letter)

    #Recursive method for building and checking peptides
    while len(Combos) != 0:
        for string in Combos:
            for aminoacid in aa: 
                if CheckCompatibility(LinearSpectrum(string+aminoacid), SpectrumIdeal) == True:
                    
                    #If compatible thus far, and mass is correct, add to correct pile
                    if FindMass(LinearSpectrum(string+aminoacid)) == CorrectMass:
                        Correct.append(string+aminoacid)
                    
                    #If compatible thus far, but mass is too small, retry with another amino acid appended next round 
                    elif FindMass(LinearSpectrum(string+aminoacid)) < CorrectMass:
                        Combos.append(string+aminoacid)
            
            Combos.remove(string)  

    #Selects unique peptides
    unique = {}
    for peptide in Correct:
        string = ''
        for aminoacid in peptide:
            if aminoacid == 'L' or aminoacid == 'I':
                string += '(L/I)'
            else:
                string += aminoacid
        unique[string] = 1
    return unique
        
Peptides = IdealSequencing(SpectrumIdeal)     

for peptide in Peptides:
        print peptide
