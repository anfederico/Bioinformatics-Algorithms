from copy import deepcopy
import heapq
import operator

#Non-ideal experimental spectrum
SpectrumNonIdealTemp = '456 783 658 508 156 361 426 1177 593 554 1137 245 1493 1390 1280 114 797 97 981 606 740 721 496 817 1232 753 583 1242 342 584 1293 1379 211 147 338 137 1356 1436 1048 867 469 1080 1076 359 996 512 887 527 1356 314 696 720 997 1248 1282 1248 1008 757 485 200 1362 261 103 1346 1024 1132 1396 622 773 892 676 772 559 622 415 626 1280 1037 417 626 270 114 1379 835 934 867 1122 497 398 1151 1394 910 710 1155 312 1095 939 360 137 813 1406 680 920 382 99 1078 1269 1181 371 114 900 871 284 852 245 964 1111 445 156 1209 871 1223 966 213 213 251 1269 1179 470 87 131 1134 1337 1133 529 715 573 57 601 1018 413 736 985 0 1067 224 1234 909 316 1337 1023 778 475 1379 259 641 356 224'
SpectrumNonIdealTemp = SpectrumNonIdealTemp.split()
SpectrumNonIdeal = []
for number in SpectrumNonIdealTemp:
    SpectrumNonIdeal.append(int(number))
SpectrumNonIdeal = sorted(SpectrumNonIdeal)

m = 18 #Number of high frequency peptides present in convolution    
MinMass = 57 #Minimum mass of possible amino acid
MaxMass = 200 #Maximum mass of possible amino acid
Boundary = 5 #How many rounds in before Upper Score cutoff is enforced
LowerScore = 3 #Lower Score cutoff
UpperScore = 25 #Upper Score cutoff

def FindConvolution(SpectrumNonIdeal, m, MinMass, MaxMass):
    #Find convolution of the peptide
    matrix = []
    for number in SpectrumNonIdeal:
        matrix.append(number)
        matrix.append([0]*len(SpectrumNonIdeal))
    k = 1  
    i = 3
    while i < len(SpectrumNonIdeal)*2:
        j = 0
        k += 1
        while j < k-1:
            matrix[i][j] = matrix[i-1]-SpectrumNonIdeal[j]
            j += 1
        i += 2
    elements = []
    i = 3
    while i < len(SpectrumNonIdeal)*2:
        for element in matrix[i]:
            if element != 0:
                elements.append(element)
        i += 2    
    frequency = {}
    for element in sorted(elements):
        if element >= MinMass and element <= MaxMass:
            frequency.setdefault(element,0)
            frequency[element] += 1
    numbers = []
    for element in frequency:
        numbers.append(frequency[element]) 
    minimum = min(heapq.nlargest(m, numbers))
    output = []
    for element in frequency:    
        if frequency[element] >= minimum:
            output.append(str(element))
    return output

def LinearSpectrum(peptide, CharToNum):
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
            total += int(CharToNum[aminoacid])
        sizes.append(str(total))
    return sizes

def CycloSpectrum(peptide, CharToNum):
    #Find the cyclo spectrum of the peptide
    peptides = []
    sizes = ['0']
    peptides.append(peptide)
    cyclic_protein = peptide*2
    n = len(peptide)
    for window in range(1,n):
        for i in range(0,n):
            peptides.append(cyclic_protein[i:i+window])
    for string in peptides:
        total = 0
        for aminoacid in string:
            total += int(CharToNum[aminoacid])
        sizes.append(str(total))
    return sizes

def FindMass(spectrum):
    temp = []
    for num in spectrum:
        temp.append(int(num))
    temp = sorted(temp)
    return temp[len(temp)-1]

def Score(Experimental, Reference):
    temp = deepcopy(Reference)
    score = 0
    for Expaa in Experimental:
        present = 0
        for Refaa in temp:
            if Expaa == Refaa:
                present = 1
        if present == 1:
            score += 1
            temp.remove(Expaa)
    return score 

def NonIdealSequencing(SpectrumNonIdeal, m,  MinMass, MaxMass, Boundary, LowerScore, UpperScore):
    #Give each mass an arbitrary ASCII character
    Frequency = FindConvolution(SpectrumNonIdeal, m, MinMass, MaxMass)
    NumToChar= {}
    CharToNum = {}
    i = 65
    for element in Frequency:
        if i == 91:
            i = 97
        NumToChar[element] = chr(i)
        CharToNum[chr(i)] = element
        i += 1
    
    #Convert integers to strings
    temp = []
    for char in SpectrumNonIdeal:
        temp.append(str(char))
    SpectrumNonIdeal = deepcopy(temp)

    #Find correct mass of the non-ideal spectrum
    CorrectMass = FindMass(SpectrumNonIdeal)
    
    combos = [] #Store potential peptides
    leaders = {} #Store lead scoring peptides
    for aminoacid in CharToNum:
        combos.append(aminoacid)
        
    #Recursive method for building and scoring peptides
    rounds = 1
    while len(combos) != 0:
        #Expand and score
        CombosTemp = {}
        Scores = []
        for string in combos:
            for aminoacid in CharToNum:     
                NewCombo = string+aminoacid
                NewSpec = LinearSpectrum(NewCombo, CharToNum)
                NewScore = Score(NewSpec, SpectrumNonIdeal)            
                
                #If mass is too small, retry with another amino acid appended next round    
                if FindMass(NewSpec) < CorrectMass:
                        Scores.append(NewScore)
                        CombosTemp[NewCombo] = NewScore
                
                #If mass is correct, score it
                elif FindMass(NewSpec) == CorrectMass:
                    leaders[NewCombo] = Score(CycloSpectrum(NewCombo, CharToNum), SpectrumNonIdeal)
                    
        if len(Scores) == 0:
            break
        
        #Trim and push forward   
        if rounds >= Boundary:
            maximum = deepcopy(min(heapq.nlargest(LowerScore, Scores)))
        if rounds < Boundary:
            maximum = deepcopy(min(heapq.nlargest(UpperScore, Scores)))
        combos = []
        counter = 0
        for string in CombosTemp:
            if CombosTemp[string] >= maximum:
                combos.append(string)
                counter += 1
            if rounds >= Boundary:
                if counter == 100: #Limit recursion
                    break
        rounds += 1
    
    #Best scoring peptides with correct mass
    LeadingScores = []
    for protein in leaders:
        LeadingScores.append(leaders[protein])
    
    #Select best of the best
    TopScores = []    
    for protein in leaders:
        if leaders[protein] == max(LeadingScores):
            string = ''
            for amino_acid in protein:
                string += CharToNum[amino_acid] + '-'
            TopScores.append(string.strip('-'))
    return TopScores    

Peptides = NonIdealSequencing(SpectrumNonIdeal, m, MinMass, MaxMass, Boundary, LowerScore, UpperScore)

for peptide in Peptides:
        print peptide
