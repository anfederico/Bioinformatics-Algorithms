'''
Text file containg protein IDs
For example...

Q640N1
Q8PV50
P0AAM4
Q8CE94
P49286

'''

#Get primary structure and store as sring
import urllib2
def find_protein(protein_id):
    give_protein = ""
    return_protein = ""

    for line in urllib2.urlopen("http://www.uniprot.org/uniprot/%s.fasta" % protein_id):
        if line[0] != ">":
            give_protein = give_protein + line
    
    for char in give_protein:
        if char != "\n":    
            return_protein = return_protein + char

    print protein_id
    return return_protein


#Finding the positions of N-glycosylation motif -> N{P}[ST]{P}
def find_motif(protein):    
    a = 0
    b = 1
    c = 2
    d = 3

    positions = []

    for i in range(0, len(protein)-4):
        if protein[a] == "N":
            if protein[b] != "P":
                if (protein[c] == "S") or (protein[c] == "T"): 
                    if protein[d] != "P":
                        positions.append(i+1)
                        a += 1
                        b += 1
                        c += 1
                        d += 1
                    else:
                        a += 1
                        b += 1
                        c += 1
                        d += 1
                else:
                    a += 1
                    b += 1
                    c += 1
                    d += 1
            else:
                a += 1
                b += 1
                c += 1
                d += 1
        else:
            a += 1
            b += 1
            c += 1
            d += 1
                
    pos = ""
    for num in positions:
        pos = pos + str(num) + " "
    print pos
            
infile = open("in.txt", "r")

listy = []

for line in infile:
    listy.append(line.strip())

for line in listy:
    find_motif(find_protein(line))

infile.close()

'''
Output

Q640N1
471 519 913 1030 
Q8PV50
188 195 
P0AAM4
Q8CE94
369 
P49286
4 130 

'''
