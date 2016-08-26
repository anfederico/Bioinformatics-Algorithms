import collections
from random import randint
from copy import deepcopy

infile = open('PairedReads.txt', 'r')
DNA = []
for line in infile:
    DNA.append(line.strip('\n'))
infile.close()
    
k = 30 #Read length
d = 100 #Distance between pairs    

def prefix(kmer_pair):
    pref = ''
    f = (len(kmer_pair)-1)/2
    pref += (kmer_pair[:f-1])
    pref += '|'
    pref += (kmer_pair[f+1:len(kmer_pair)-1])
    return pref
    
def suffix(kmer_pair):
    suff = ''
    f = (len(kmer_pair)-1)/2
    suff += (kmer_pair[1:f])
    suff += '|'
    suff += (kmer_pair[len(kmer_pair)-f+1:])
    return suff

def AssembleGenome(DNA, k, d):
    #Represent every k-mer in Patterns as an isolated edge between its prefix and suffix
    edges = [] # edged = [kmer : [prefix(kmer), suffix(kmer)]]
    for kmer in DNA:
        edges.append(kmer)
        edges.append([prefix(kmer),suffix(kmer)])
    
    #Find prefixes/suffixes
    prefixes = []
    suffixes = []
    i = 0
    while i < len(edges):
        prefixes.append(edges[i+1][0])
        suffixes.append(edges[i+1][1])
        i += 2
    
    #Sort pairs    
    pairs = {}
    i = 0
    while i < len(prefixes):
        pairs.setdefault(prefixes[i],[])
        pairs[prefixes[i]].append(suffixes[i])
        i += 1
    pairs = collections.OrderedDict(sorted(pairs.items()))
    
    #Assign strings to unique IDs
    numbers = {}
    rev_numbers = {}
    i = 0
    for pair in pairs:
        numbers[pair] = str(i)
        rev_numbers[str(i)] = pair
        i += 1
        
    for pair in pairs:
        for end in pairs[pair]:
            numbers.setdefault(end, 'empty')
        if numbers[end] == 'empty':
            numbers[end] = str(i)
            rev_numbers[str(i)] = end
            i += 1
    
    adj_list = {}
    circuit_max = 0
    for start in pairs:
        for end in pairs[start]:
            adj_list.setdefault(numbers[start], [])
            adj_list[numbers[start]].append(numbers[end])
            circuit_max += 1
         
    #Reduced adjacency list to keep track of traveled edges   
    red_adj_list = {}            
    red_adj_list = deepcopy(adj_list)
    
    #Find start and end node
    start = {}
    for one in red_adj_list:
        start.setdefault(one, 0)
        start[one] += len(red_adj_list[one])
    end = {}
    for one in red_adj_list:
        for two in red_adj_list[one]:
            end.setdefault(two, 0)
            end[two] += 1
    for one in end:
        try: 
            if start[one] != end[one]:
                if start[one] > end[one]:
                    start_node = one
                if start[one] < end[one]:
                    end_node = one
        except KeyError:
            end_node = one
    for one in start:
        try:
            if end[one] != start[one]:
                if end[one] < start[one]:
                    start_node = one
                if end[one] > start:
                    end_node = one  
        except KeyError:
            start_node = one
            
    #Set end
    red_adj_list[end_node] = []
    
    #Starting node (if graph is directed/ubalanced)
    start = start_node
    curr_vrtx = start_node
    
    path = []
    path.append(curr_vrtx)
    stack = []
    circuit = []
    while len(circuit) != circuit_max:
    
        if red_adj_list[curr_vrtx] != []: #If neighbors exist
            stack.append(curr_vrtx)
            pick = randint(0,len(red_adj_list[curr_vrtx])-1)
            temp = deepcopy(curr_vrtx)
            curr_vrtx = red_adj_list[temp][pick]
            red_adj_list[temp].remove(curr_vrtx)
            
        else:
            circuit.append(curr_vrtx)
            curr_vrtx = stack[len(stack)-1]
            stack.pop()
        
    #Match IDs to strings
    circuit = [start] + circuit[::-1]
    corr_order = []
    for vrtx in circuit:
        corr_order.append(rev_numbers[vrtx])
    
    #Formatting
    a = []
    b = []
    for kmer in corr_order:
        a.append(kmer[:k-1])
        b.append(kmer[k:])
    prefixstring = ''
    for kmer in a:
        prefixstring += kmer[0]
    suffixstring = ''
    for kmer in b:
        suffixstring += kmer[0]
    genome = ''
    genome += prefixstring[0:k+d]
    genome += suffixstring
    genome += b[len(b)-1][1:]
    
    return genome
            
print AssembleGenome(DNA, k, d)
