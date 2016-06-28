
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
