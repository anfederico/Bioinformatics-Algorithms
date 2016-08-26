import copy
import operator

infile = open('Matrix.txt', 'r')
n = 9 #Size of matrix
m = 9 #Start numbering unkown ancestors
species = ['Cow', 'Pig', 'Horse', 'Mouse', 'Dog', 'Cat', 'Turkey', 'Civet', 'Human']

#Setup starting matrix D and fill it in
D = {}
for i in species:
    D[i] = {}
    for j in species:
        D[i][j] = 0  
i = 0
for line in infile:
    j = 0
    for number in line.split():
        D[species[i]][species[j]] = int(number)
        j += 1
    i += 1        
infile.close()    

#Use to visualize matrix D/D*
def Visualize(D):
    temp = '    '
    for cluster in D:
        temp += str(cluster) + '       '
    print temp    
    for line in D:
        print D[line]

#Transform matrix D to D* and find closest neighbors Ni and Nj         
def TransformMatrix(D):    
    #Find Total Distance
    TotalDistance = {}
    for i in D:
        total = 0
        for j in D:
            total += D[i][j]
        TotalDistance[i] = total
    
    #Create D*
    Dstar = {}
    for i in D:
        Dstar[i] = {}
        for j in D:
            Dstar[i][j] = 0 
    for i in D:
        for j in D:
            if i == j:
                Dstar[i][j] = 0
            else:
                Dstar[i][j] = (n-2)*D[i][j]-TotalDistance[i]-TotalDistance[j]
    
    #Find minimum neighbors
    Dstar_values = []
    for i in Dstar:
        for j in Dstar:
            if i != j:
                Dstar_values.append([Dstar[i][j],[i,j]])
    Ni = min(Dstar_values)[1][0]
    Nj = min(Dstar_values)[1][1]
    return Ni, Nj, Dstar, TotalDistance            

#Remove Ni and Nj from matrix D
def RemoveClusters(D,Ni,Nj):
    del D[Ni]
    del D[Nj]
    for i in D:
        del D[i][Ni]
        del D[i][Nj]
    return D

#Add unkown ancestor m to matrix D    
def AddCluster(D,D_temp,m,Ni,Nj):
    D[m] = {}
    for k in D:
        if k != m:
            D[m][k] = (0.5)*(D_temp[k][Ni]+D_temp[k][Nj]-D_temp[Ni][Nj])
    for k in D:
        if k != m:
            D[k][m] = (0.5)*(D_temp[k][Ni]+D_temp[k][Nj]-D_temp[Ni][Nj])
        if k == m:
            D[m][m] = 0
    return D            

#Add new edges m->Ni and m->Nj to adjacency list
def MakeLimbs(D_temp,m,Ni,Nj,TotalDistance):
    delta = (TotalDistance[Ni]-TotalDistance[Nj])/(n-2)
    LimbLength_Ni = (0.5)*(D_temp[Ni][Nj]+delta)
    LimbLength_Nj = (0.5)*(D_temp[Ni][Nj]-delta)
    adj_list.append([m, str(m) + '->' + str(Ni) + ':' + str(int(LimbLength_Ni))])
    adj_list.append([Ni, str(Ni) + '->' + str(m) + ':' + str(int(LimbLength_Ni))])
    adj_list.append([m, str(m) + '->' + str(Nj) + ':' + str(int(LimbLength_Nj))])
    adj_list.append([Nj, str(Nj) + '->' + str(m) + ':' + str(int(LimbLength_Nj))])

#Neighbor Joining    
adj_list = []    
while n != 2:
    Ni, Nj, Dstar, TotalDistance = TransformMatrix(D)
    D_temp = copy.deepcopy(D)
    RemoveClusters(D,Ni,Nj)
    D = AddCluster(D,D_temp,m,Ni,Nj)
    MakeLimbs(D_temp,m,Ni,Nj,TotalDistance)
    m += 1
    n -= 1
    
if n == 2:
    for Mi in D:
        for Mj in D:
            if Mi != Mj:
                adj_list.append([Mi, str(Mi) + '->' + str(Mj) + ':' + str(int(D[Mi][Mj]))])
                
#Print adjacency list
for edge in sorted(adj_list):
    print edge[1]
