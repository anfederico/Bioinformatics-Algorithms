#Simple scoring method (+1 match / -1 mismatch)
def score(vwu):
    if vwu[0] == vwu[1] and vwu[0] == vwu[2]:
        return 1
    else:
        return -1

def MultipleAlignment(v, w, u):
    #Initialize 3D scoring matrix
    s = [[[0 for j in range(len(w)+1)] for i in range(len(v)+1)] for k in range(len(u)+1)]
    backtrack = [[[0 for j in range(len(w)+1)] for i in range(len(v)+1)] for k in range(len(u)+1)]

    #3D scoring / s[k][i][j]
    for k in range(1,len(u)+1):    
        for i in range(1,len(v)+1):
            for j in range(1,len(w)+1):
     
                values = [
                         s[k][i-1][j],    #0
                         s[k][i][j-1],    #1
                         s[k-1][i][j],    #2
                         s[k][i-1][j-1],  #3
                         s[k-1][i-1][j],  #4
                         s[k-1][i][j-1],  #5
                         s[k-1][i-1][j-1]+score(u[k-1]+v[i-1]+w[j-1])  #6
                         ]
                         
                s[k][i][j] = max(values)   
                backtrack[k][i][j] = values.index(s[k][i][j])
    
    #Backtracking and output
    i = len(v)
    j = len(w)
    k = len(u)
    V = ''
    W = ''
    U = ''
    while i+j+k != 0:
        if i*j*k == 0:
            if i == 0:
                V += '-'
            else:
                V += v[i-1]
                i -= 1
            if j == 0:
                W += '-'
            else:
                W += w[j-1]
                j -= 1
            if k == 0:
                U += '-'
            else:
                U += u[k-1]
                k -= 1  
    
        elif backtrack[k][i][j] == 0:
            V += v[i-1] 
            W += '-'
            U += '-'
            i = i-1
        elif backtrack[k][i][j] == 1:
            V += '-' 
            W += w[j-1] 
            U += '-'
            j = j-1
        elif backtrack[k][i][j] == 2:
            V += '-' 
            W += '-' 
            U += u[k-1]
            k = k-1           
        elif backtrack[k][i][j] == 3:
            V += v[i-1] 
            W += w[j-1]
            U += '-'
            i = i-1
            j = j-1
        elif backtrack[k][i][j] == 4:
            V += v[i-1] 
            W += '-'
            U += u[k-1]
            i = i-1
            k = k-1    
        elif backtrack[k][i][j] == 5:
            V += '-' 
            W += w[j-1]
            U += u[k-1]
            j = j-1
            k = k-1        
        elif backtrack[k][i][j] == 6:
            V += v[i-1] 
            W += w[j-1]
            U += u[k-1]
            i = i-1
            j = j-1
            k = k-1       
    
    return int(s[len(u)][len(v)][len(w)]), V[::-1], W[::-1], U[::-1]
    
score, V, W, U = MultipleAlignment('ACGATACGT', 'CCCATTAAGT', 'GACTATAGAA')            

print 'Score: ' + str(score)
print V
print W
print U
