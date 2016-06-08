from copy import deepcopy
infile = open('AA_Mass_Table.txt', 'r')

aa = {}
for line in infile:
    aa[line[0]] = line[2:].strip('\n')

#Ideal experimental spectrum
spec_strn = '0 71 97 99 101 101 113 114 129 131 163 186 202 202 211 227 228 230 230 234 260 287 299 301 324 329 331 331 359 365 374 388 400 413 430 430 445 460 462 464 487 501 510 514 517 531 558 561 561 576 593 611 615 616 630 632 673 675 689 690 694 712 729 744 744 747 774 788 791 795 804 818 841 843 845 860 875 875 892 905 917 931 940 946 974 974 976 981 1004 1006 1018 1045 1071 1075 1075 1077 1078 1094 1103 1103 1119 1142 1174 1176 1191 1192 1204 1204 1206 1208 1234 1305 '

#Reorganize through listing
spec_ideal = []
spec_temp = ''
for char in spec_strn:
    if char != ' ':
        spec_temp += char
    else:
        spec_ideal.append(spec_temp)
        spec_temp = ''

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
            total += int(aa[amino_acid])
        sizes.append(str(total))
    
    return sizes
    
#=============== CHECK COMPATABILITY ===============#

def check_compat(protein_spec, spec_ideal):
    temp = deepcopy(spec_ideal)
    compat = True
    for num_prot in protein_spec:
        present = 0
        for num_spec in temp:
            if num_prot == num_spec:
                present = 1
        if present == 1:
            temp.remove(num_prot)
        if present == 0:
            compat = False
            return compat
    return compat
            
#==================== FIND MASS ====================#

def find_mass(spectrum):
    temp_list = []
    for str in spectrum:
        temp_list.append(int(str))
    temp_list = sorted(temp_list)
    return temp_list[len(temp_list)-1]

#Correct mass to check for
corr_mass = find_mass(spec_ideal)

combos = [] #Store potential peptides
correct = [] #Store correct peptides
for letter in aa:
    combos.append(letter)

#Recursive method for building and checking peptides
i = 0
while len(combos) != 0:
    for string in combos:
        for amino_acid in aa: 
            if check_compat(lin_spec(string+amino_acid), spec_ideal) == True:
                if find_mass(lin_spec(string+amino_acid)) == corr_mass:
                    correct.append(string+amino_acid)
                elif find_mass(lin_spec(string+amino_acid)) < corr_mass:
                    combos.append(string+amino_acid)
        combos.remove(string)  

#Weeds out unique peptides
unique_dict = {}
for protein in correct:
    string = ''
    for amino_acid in protein:
        if amino_acid == 'L' or amino_acid == 'I':
            string += '(L/I)'
        else:
            string += amino_acid
    unique_dict[string] = 1

for protein in unique_dict:
    print protein
    
'''
Output
MVETTW(L/I)NPYA
(L/I)WTTEVMAYPN
TEVMAYPN(L/I)WT
MAYPN(L/I)WTTEV
WTTEVMAYPN(L/I)
TTEVMAYPN(L/I)W
YPN(L/I)WTTEVMA
(L/I)NPYAMVETTW
AYPN(L/I)WTTEVM
ETTW(L/I)NPYAMV
N(L/I)WTTEVMAYP
VETTW(L/I)NPYAM
W(L/I)NPYAMVETT
PYAMVETTW(L/I)N
VMAYPN(L/I)WTTE
YAMVETTW(L/I)NP
NPYAMVETTW(L/I)
TW(L/I)NPYAMVET
PN(L/I)WTTEVMAY
AMVETTW(L/I)NPY
TTW(L/I)NPYAMVE
EVMAYPN(L/I)WTT
'''
