'''=================[SETUP]================='''
import copy
import operator

'''
Matrix_Species.txt
0 295 300 524 1077 1080 978 941 940
295 0 314 487 1071 1088 1010 963 966
300 314 0 472 1085 1088 1025 965 956
524 487 472 0 1101 1099 1021 962 965
1076 1070 1085 1101 0 818 1053 1057 1054
1082 1088 1088 1098 818 0 1070 1085 1080
976 1011 1025 1021 1053 1070 0 963 961
941 963 965 962 1057 1085 963 0 16
940 966 956 965 1054 1080 961 16 0
'''

infile = open('Matrix_Species.txt', 'r')

#Setup starting matrix D and fill it in
n = 9 #size of matrx
m = 9 #start numbering unkown ancestors
D = {}
species = ['Cow', 'Pig', 'Horse', 'Mouse', 'Dog', 'Cat', 'Turkey', 'Civet', 'Human']
for i in species:
    D[i] = {}
    for j in species:
        D[i][j] = 0  
i = 0
for line in infile:
    j = 0
    temp = ''
    for char in line:
        if char != ' ':
            temp += char
        else:
            D[species[i]][species[j]] = float(temp)
            temp = ''
            j += 1
    D[species[i]][species[j]] = float(temp.strip('\n'))
    i += 1        

'''=================[FUNCTIONS]================='''

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
    
'''=================[BEGIN]================='''

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
    
'''
Output
9->12:454
9->Civet:9
9->Human:7
10->11:163
10->Cat:414
10->Dog:403
11->10:163
11->12:22
11->Turkey:488
12->11:22
12->13:250
12->9:454
13->12:250
13->14:85
13->Mouse:253
14->13:85
14->15:10
14->Horse:148
15->14:10
15->Cow:146
15->Pig:148
Cat->10:414
Civet->9:9
Cow->15:146
Dog->10:403
Horse->14:148
Human->9:7
Mouse->13:253
Pig->15:148
Turkey->11:488
'''
