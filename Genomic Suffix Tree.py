class Node(object):
    def __init__(self, value, ID):
        self.value = value
        self.children = {}
        self.ID = ID #Label nodes with ID
        
class Trie(object):
    def __init__(self):
        self.root = Node(None, 0) #Root is labeled 0
        
    def AddString(self, pattern, ID):
        current = self.root #Start at root
        for nt in pattern:
            if nt in current.children:
                current = current.children[nt]
            else:
                new_node = Node(nt, ID)
                current.children[nt] = new_node
                current = new_node
                ID += 1
        if None not in current.children:
            current.children[None] = None
        return ID    

    def Traverse(self, suffix, branch_ids, edges):
        current = self.root
        edge_temp = ''
        for nt in suffix:
            if nt in current.children:
                current = current.children[nt]
                if len(current.children) >= 2:
                    if current.ID in branch_ids:
                        edge_temp = ''
                    else:
                        edge_temp += nt
                        branch_ids.append(current.ID)
                        edges.append(edge_temp)
                        edge_temp = ''
                if len(current.children) == 1:
                    edge_temp += nt
        edges.append(edge_temp)
        edge_temp = ''
        return branch_ids, edges
        
def SuffixTree(genome):
    #Trie loading
    Tree = Trie()
    ID = 1 
    i = 0
    while i < len(genome):
        ID = Trie.AddString(Tree, genome[i:], ID)
        i += 1
    
    #Trie traversal
    branch_ids = []
    edges = []
    i = 0
    while i < len(genome):
        branch_ids, edges = Trie.Traverse(Tree, genome[i:], branch_ids, edges)
        i += 1
    edges.remove('')
    
    return sorted(edges)

genome = 'CTTGTTCGTAAA'
edges = SuffixTree(genome)
for edge in edges:
    print edge
