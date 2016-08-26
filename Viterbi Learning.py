infile = open('TransitionMatrix.txt', 'r')
TransitionMatrix = []
for line in infile:
    TransitionMatrix.append(line.strip('\n').split('\t'))
infile.close()

infile = open('EmissionMatrix.txt', 'r')
EmissionMatrix = []
for line in infile:
    EmissionMatrix.append(line.strip('\n').split('\t'))
infile.close()

string = 'zzxzzxyxzyyyyxzxxxyxyxzzzxyxxyyxxxyxyyxzyzxyyyzyzxyyzzxzxzyzyyzxyxyxyzzxyzzxxxzyyyzzyxzzxxyzzyxyzyxx'
alphabet = 'x y z'.split() #Observation space
states = 'A B C D'.split() #State space

TM = {} #Setup transition matrix
i = 0
for state1 in states:
    TM[state1] = {}
    j = 1
    for state2 in states:
        TM[state1][state2] = float(TransitionMatrix[i][j])
        j += 1
    i += 1   
    
EM = {} #Setup emission matrix
i = 0
for state in states:
    EM[state] = {}
    j = 1
    for letter in alphabet:
        EM[state][letter] = float(EmissionMatrix[i][j])
        j += 1
    i += 1  

def Viterbi(string, alphabet, states, TM, EM):

    Pi = 1 #Probability of initial state set to equally likely = 1/|states|

    T1 = {} #Scoring matrix
    T2 = {} #Backtracking matrix
    for state in states:
        T1[state] = [0]*len(string)
        T2[state] = [0]*len(string)

    #Initalize scores at source
    for state in states:
        T1[state][0] = Pi*EM[state][string[0]]

    #Fill in remaining scores through dynamic programming    
    i = 1    
    while i < len(string):
        for j in states:
            values = []
            K = []
            for k in states:
                values.append(T1[k][i-1]*TM[k][j]*EM[j][string[i]])
                K.append((T1[k][i-1]*TM[k][j]*EM[j][string[i]], k))
            
            #Choose max weight of possible edges (k->j)
            T1[j][i] = max(values)
            #Remember which edge was chosen for backtracking
            for k in K:
                if k[0] == max(values):
                    T2[j][i] = k[1]
        i += 1

    #Find maximum sink value and begin most probable path
    values = []
    K = []
    for state in T1:
        values.append(T1[state][len(string)-1])
    for state in T1:
        if T1[state][len(string)-1] == max(values):
            path = state
            last = state

    #Backtracking
    i = len(string)-1    
    while i > 0:
        for state in states:
            if T2[last][i] == state:
                last = state
                path += last
                i -= 1
                break
            
    return path[::-1]

def EstimateParameters(string, alphabet, path, states):
    
    #Count TM instances
    TM_counts = {}
    i = 0
    while i < len(path)-1:
        TM_counts.setdefault(path[i], {})
        TM_counts[path[i]].setdefault(path[i+1], 0)
        TM_counts[path[i]][path[i+1]] += 1
        i += 1
        
    #Count EM instances
    EM_counts = {}
    i = 0
    while i < len(path):
        EM_counts.setdefault(path[i], {})
        EM_counts[path[i]].setdefault(string[i], 0)
        EM_counts[path[i]][string[i]] += 1
        i += 1 
     
    #Calculate TM matrix 
    TM_matrix = {}
    for state in states:
        TM_matrix.setdefault(state,{})
        total = 0.0
        for column in states:
            try:
                total += TM_counts[state][column]
            except KeyError:
                pass
        if total == 0:
            for column in states:
                TM_matrix[state][column] = 1.0/len(states)
        else:
            for column in states:
                try:
                    TM_matrix[state][column] = TM_counts[state][column]/total
                except KeyError:
                    TM_matrix[state][column] = 0
    
    #Calculate EM matrix 
    EM_matrix = {}
    for state in states:
        EM_matrix.setdefault(state,{})
        total = 0.0
        for column in alphabet:
            try:
                total += EM_counts[state][column]
            except KeyError:
                pass
        if total == 0:
            for column in alphabet:
                EM_matrix[state][column] = 1.0/len(alphabet)
        else:
            for column in alphabet:
                try:
                    EM_matrix[state][column] = EM_counts[state][column]/total
                except KeyError:
                    EM_matrix[state][column] = 0
    
    return TM_matrix, EM_matrix

#Viterbi Learning
iteration = 0
while iteration < 100:
    
    #Find the hidden path using parameters
    path = Viterbi(string, alphabet, states, TM, EM)
    
    #Estimate new parameters based on the hidden path
    TM, EM = EstimateParameters(string, alphabet, path, states)
    
    iteration += 1

#Excluded from this point is the code necessary to format/output the final TM/EM
