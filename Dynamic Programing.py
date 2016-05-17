'''
This program will return the total number of pairs of cats in a population remaining after the n-th month if all cats live for m months
F[1] = 1 pair of baby cats (1 male + 1 female) 
Each pair of cats reaches maturity in one month and produces a single pair of offspring (1 male + 1 female) each subsequent month including the month of death
'''

n = 99 
m = 20

F = {}
F[0] = 0
F[1] = 1
F[2] = 1
born = {}
born[0] = 0
born[1] = 1
born[2] = 0

for x in ((3-m)-1,0):
    F[x]    = 0
    
###

def num_born(j):
    if j < 1:
        return 0
    elif j == 1:
        return 1
    elif j == 2:
        return 0
    else:
        born[j] = F[j-1] - born[j-1]
        return born[j]
    
def mort_fib(i):
    F[i] = (F[i-1]-num_born(i-m)) + (F[i-2]-num_born((i-m)-1))
    
for k in range (3,n+1):
    mort_fib(k)

print F[n]
