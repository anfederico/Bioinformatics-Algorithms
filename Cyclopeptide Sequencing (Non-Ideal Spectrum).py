from copy import deepcopy
import heapq
import operator

#Non-ideal experimental spectrum
spec_strn = '456 783 658 508 156 361 426 1177 593 554 1137 245 1493 1390 1280 114 797 97 981 606 740 721 496 817 1232 753 583 1242 342 584 1293 1379 211 147 338 137 1356 1436 1048 867 469 1080 1076 359 996 512 887 527 1356 314 696 720 997 1248 1282 1248 1008 757 485 200 1362 261 103 1346 1024 1132 1396 622 773 892 676 772 559 622 415 626 1280 1037 417 626 270 114 1379 835 934 867 1122 497 398 1151 1394 910 710 1155 312 1095 939 360 137 813 1406 680 920 382 99 1078 1269 1181 371 114 900 871 284 852 245 964 1111 445 156 1209 871 1223 966 213 213 251 1269 1179 470 87 131 1134 1337 1133 529 715 573 57 601 1018 413 736 985 0 1067 224 1234 909 316 1337 1023 778 475 1379 259 641 356 224'

#Reorganize through listing
spec_list = []
spec_temp = ''
for char in spec_strn:
    if char != ' ':
        spec_temp += char
    else:
        spec_list.append(int(spec_temp))
        spec_temp = ''
    
sort_spec_list = deepcopy(sorted(spec_list))

#============== FIND CONVOLUTION ==============#

def find_convo(sort_spec_list, m):
    
    #Create matrix
    matrix = []
    for number in sort_spec_list:
        matrix.append(number)
        matrix.append([0]*len(sort_spec_list))
    
    #Traverse and fill
    k = 1  
    i = 3
    while i < len(sort_spec_list)*2:
        j = 0
        k += 1
        while j < k-1:
            matrix[i][j] = matrix[i-1]-sort_spec_list[j]
            j += 1
        i += 2
    
    #Specify elements
    elements = []
    i = 3
    while i < len(sort_spec_list)*2:
        for element in matrix[i]:
            if element != 0:
                elements.append(element)
        i += 2    
    
    #Element frequency
    multi = {}
    for element in sorted(elements):
        if element >= 57 and element <= 200:
            multi.setdefault(element,0)
            multi[element] += 1

    numbers = []
    for element in multi:
        numbers.append(multi[element]) 
    minimum = min(heapq.nlargest(m, numbers))
    
    output = []
    for element in multi:    
        if multi[element] >= minimum:
            #print str(element) + ': (' + str(multi[element]) + ')'
            output.append(str(element))
    
    return output
    
m = 18 #Number of high frequency peptides present in convolution
freq_eles = find_convo(sort_spec_list, m)

#Give each mass an arbitrary ASCII character
lookup_num2char= {}
lookup_char2num = {}
i = 65
for element in freq_eles:
    if i == 91:
        i = 97
    lookup_num2char[element] = chr(i)
    lookup_char2num[chr(i)] = element
    i += 1

sort_spec_list_temp = []
for char in sort_spec_list:
    sort_spec_list_temp.append(str(char))
sort_spec_list = deepcopy(sort_spec_list_temp)

#============== FIND LINEAR SPECTRUM ==============#

def lin_spec(protein):
    proteins = []
    sizes = ['0']
    proteins.append(protein)
    
    n = len(protein)
    
    for window in range(1,n):
        for i in range(0,n-window+1):
            proteins.append(protein[i:i+window])
        
    for string in proteins:
        total = 0
        for amino_acid in string:
            total += int(lookup_char2num[amino_acid])
        sizes.append(str(total))
    
    return sizes
    
#============== FIND CYCLO SPECTRUM ==============#

def cyclo_spec(protein):
    proteins2 = []
    sizes2 = ['0']
    proteins2.append(protein)
    cyclic_protein = protein*2
    
    n = len(protein)
    
    for window in range(1,n):
        for i in range(0,n):
            proteins2.append(cyclic_protein[i:i+window])
        
    for string in proteins2:
        total = 0
        for amino_acid in string:
            total += int(lookup_char2num[amino_acid])
        sizes2.append(str(total))
        
    return sizes2
    
#==================== FIND MASS ====================#

def find_mass(spectrum):
    temp_list = []
    for str in spectrum:
        temp_list.append(int(str))
    temp_list = sorted(temp_list)
    return temp_list[len(temp_list)-1]

#================= LINEAR SCORING =================#

def score(expe, spec):
    temp_spec = deepcopy(spec)
    score = 0
    for exp_aa in expe:
        present = 0
        for spec_aa in temp_spec:
            if exp_aa == spec_aa:
                present = 1
        if present == 1:
            score += 1
            temp_spec.remove(exp_aa)
    return score 

#===================== BEGIN ====================#

#Correct mass to check for
corr_mass = find_mass(sort_spec_list)

combos = [] #Store potential peptides
for amino_acid in lookup_char2num:
    combos.append(amino_acid)
    
#Recursive method for building and scoring peptides
leaders = {} #Store lead scoring peptides
i = 0
rounds = 1
while len(combos) != 0:
    
    #Expand and score
    temp_combos = {}
    scores = []
    for string in combos:
        for amino_acid in lookup_char2num:     

            new_combo = string+amino_acid
            new_spec = lin_spec(new_combo)
            new_score = score(new_spec, sort_spec_list)            
                
            if find_mass(new_spec) < corr_mass:
                
                    scores.append(new_score)
                    temp_combos[new_combo] = new_score
            
            elif find_mass(new_spec) == corr_mass:
                leaders[new_combo] = score(cyclo_spec(new_combo), sort_spec_list)
                
    
    if len(scores) == 0:
        break
    
    #Trim and push forward   
    if rounds >= 5:
        maxi = deepcopy(min(heapq.nlargest(3, scores)))
    if rounds < 5:
        maxi = deepcopy(min(heapq.nlargest(25, scores)))

    combos = []
    counter = 0
    for string in temp_combos:
        
        if temp_combos[string] >= maxi:

            combos.append(string)
            counter += 1
        
        if rounds >= 5:
            if counter == 100:
                break
    rounds += 1

#Best scoring peptides with correct mass
max_scores = []
for protein in leaders:
    max_scores.append(leaders[protein])

#Select best of the best
tops = []    
for protein in leaders:
    if leaders[protein] == max(max_scores):
        string = ''
        for amino_acid in protein:
            string += lookup_char2num[amino_acid] + '-'
        tops.append(string.strip('-'))
            
for top in tops:
    print top

'''
Output
87-137-147-114-99-57-156-103-97-114-131-114-137
137-147-114-99-57-156-103-97-114-131-114-137-87
87-137-114-131-114-97-103-156-57-99-114-147-137
147-114-99-57-156-103-97-114-131-114-137-87-137
137-114-131-114-97-103-156-57-99-114-147-137-87
114-131-114-97-103-156-57-99-114-147-137-87-137
'''
