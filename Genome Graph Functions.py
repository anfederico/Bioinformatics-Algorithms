
print ChromosomeToCycle('(+1 -2 -3 +4)') #Output -> (1 2 4 3 6 5 7 8)
def ChromosomeToCycle(Chromosome):
    chr_for = []
    active = 0
    temp = ''
    for char in Chromosome:
        if char == ' ' or char == ')':
            active = 2
        if active == 1:
            temp += char
        if char == '+' or char == '-':
            active = 1
            if char == '-':
                temp += '-'
        if active == 2:
            chr_for.append(int(temp))
            temp = ' '
            active = 0    
    
    P_und = []
    P_cyc = []
    for num in chr_for:
        if num > 0:
            P_cyc.append(2*num-1)
            P_cyc.append(2*num)
        elif num < 0:
            P_cyc.append(2*(-1*num))
            P_cyc.append(2*(-1*num)-1)
    
    cycle = '('
    for num in P_cyc:
        cycle += str(num) + ' '
    cycle = cycle.strip(' ')
    cycle += ')'
    return cycle       


print CycleToChromosome('(1 2 4 3 6 5 7 8)') #Output -> (+1 -2 -3 +4)
def CycleToChromosome(Cycle):
    cyc_for = []
    active = 0
    temp = ''
    for char in Cycle:
        if active == 1:
            if char == ' ' or char == ')':
                active = 2
        if active == 1:
            temp += char
        if active == 0:
            if char == '(' or char == ' ':
                active = 1
        if active == 2:
            cyc_for.append(int(temp))
            temp = ' '
            active = 1

    chrom_unf = []    
    for i in range(1,len(cyc_for)/2+1):
        if cyc_for[2*i-2] < cyc_for[2*i-1]:
            chrom_unf.append('+' + str(cyc_for[2*i-1]/2))
        else:
            chrom_unf.append('-' + str(cyc_for[2*i-2]/2))
        
    chrom_for = '('
    for num in chrom_unf:
        chrom_for += num + ' '
    chrom_for = chrom_for.strip(' ')
    chrom_for += ')'
    return chrom_for
  
  
print ColoredEdges('(+1 -2 -3)(-4 +5 -6)') #Output -> [(2, 4), (3, 6), (5, 1), (7, 9), (10, 12), (11, 8)]
def ColoredEdges(Genome):
    genomes = []
    genome_temp = ''
    for char in Genome:
        if char == ')':
            genome_temp +=char
            genomes.append(genome_temp)
            genome_temp = ''
        if char != ')':
            genome_temp +=  char

    nodes = []     
    for chrom in genomes:
        nodes.append(ChromosomeToCycle(chrom))
    nodes_lst = []    
    for chrom in nodes:
        nodes_tmp = []
        active = 0
        temp = ''
        for char in chrom:
            if active == 1:
                if char == ' ' or char == ')':
                    active = 2
            if active == 1:
                temp += char
            if active == 0:
                if char == '(' or char == ' ':
                    active = 1
            if active == 2:
                nodes_tmp.append(int(temp))
                temp = ' '
                active = 1
        nodes_lst.append(nodes_tmp)

    colored_edges = []
    for chrom in nodes_lst:
        j = 1
        while j < len(chrom)-2:
            colored_edges.append((chrom[j],chrom[j+1]))
            j += 2
        colored_edges.append((chrom[len(chrom)-1], chrom[0]))   
    return colored_edges


print GraphToGenome([(2, 4), (3, 6), (5, 1), (7, 9), (10, 12), (11, 8)]) #Output -> (+1 -2 -3)(-4 +5 -6)
def GraphToGenome(Graph):
    edges = []
    for pair in Graph:
        if pair[0] % 2 == 0:
            x = pair[0]/2
        else:
            x = ((pair[0]+1)/2)*-1
        if pair[1] % 2 == 0:
            y = pair[1]/2
        else:
            y = ((pair[1]+1)/2)*-1
        edges.append((x,y))
        
    chromosomes = []
    while len(edges) != 0:
        start = edges[0][0]
        end = edges[0][1]
        edges.remove((start,end))
        chromosome = [start]
    
        cyc_end = start*-1
        while end != cyc_end:
            end = end*-1
            for pair in edges:
                if pair[0] == end:
                    start = pair[0]
                    end = pair[1]
                    break        
            edges.remove((start,end))
            chromosome.append(start)
        chromosomes += [chromosome]
    
    genome_temp = ''
    for chromosome_temp in chromosomes:
        genome_temp += '('
        for char in chromosome_temp:
            if char > 0:
                genome_temp += '+' + str(char) + ' '
            else:
                genome_temp += str(char) + ' '
        genome_temp = genome_temp.strip(' ')
        genome_temp += ')'
    return genome_temp
