# Ukkonen code implementation heavily references the Ukkonen algorithm in Esso Ukkonen's paper.
# https://www.cs.helsinki.fi/u/ukkonen/SuffixT1withFigs.pdf

# notes: Edge representation = ((start, end), next_node)
# start = start index
# end = end index
# next_node = the node the edge is pointing to

class Node:
    """
    This class represents a node in the tree. The node can be an internal node or a leaf.
    If it is a leaf, it'll be initialised with a not null value for the leaf.
    """

    def __init__(self, leaf=None, suffix_link=None, size=26):
        self.edges = [None]*size # default size = 26 for 26 alphabets
        self.suffix_link = suffix_link # suffix link to another node
        self.leaf = leaf # store information if node is a leaf

    def add_edge(self, index, edge):
        self.edges[index] = edge # index represents the ord of the alphabet

    def get_edge(self, index):
        return self.edges[index]

    def get_suffix_link(self):
        return self.suffix_link # returns another node that is the suffix link

    def add_suffix_link(self, link):
        self.suffix_link = link # add a suffix link (another node) to the node

class End:
    """ 
    Global end
    Trick 4: once a leaf, always a leaf
    """
    def __init__(self):
        self.val = -1 # start from -1 to be inclusive of the final value

    def increment(self):
        self.val += 1

    def get_global_end(self):
        return self.val

class SuffixTree:

    def __init__(self, text):
        self.text = text # text to build suffix tree
        self.root = Node() # root node
        self.e = End() # global end

    def ord_position(self, index):
        # lowercase characters
        return ord(self.text[index]) - 97

    def length(self, start, end):
        # return the length of the edge
        return end - start + 1

    def get_end(self, val):
        try:
            ret = val.get_global_end() # global end
        except: 
            ret = val
        return ret
    
    def build_tree(self):
        # this function is responsible for building the suffix tree

        active_node = self.root # initialise active node
        j = 0 # left pointer

        for i in range(len(self.text)):
            self.e.increment() # increment global end. once a leaf always a leaf
            (active_node, j) = self.update(active_node, (j, i))
            (active_node, j) = self.canonize(active_node, (j, i))
        
        # checking
        self.check(self.root)
        print(self.e.get_global_end())
        return self.root

    def update(self, node, val):
        # deals with rule 2 insertions on existing nodes
        # if test_and_split is true, this means that the current phase is a showstopper and it will not enter the while loop
        # return: active node and left pointer

        left, end = val[0], val[1]
        print("update", left, end)

        prev = self.root # previous node
        (end_point, r) = self.test_and_split(node, (left, end-1), end)

        while not end_point:
            # rule 2 - edge does not exist. add edge to existing node
            r.add_edge(self.ord_position(end),((end, self.e), Node(True, self.root)))

            if prev != self.root:
                # add suffix link if there were previous rule 2 in iteration i (i in build_tree())
                prev.add_suffix_link(r)
            prev = r

            (node, left) = self.canonize(node.get_suffix_link(), (left, end-1))
            (end_point, r) = self.test_and_split(node, (left, end-1), end)

        if prev != self.root:
            prev.add_suffix_link(node)
        
        return (node, left)

    def test_and_split(self, node, val, char):
        # tests if there's an edge/ the next character on the edge matches the letter in iteration i (i in build_tree())
        # splits the edge if character does not match in the middle of the edge
        # return bool and active node. bool = True when encounter rule 3. else, bool = False

        left, end = val[0], val[1]
        print("test", left, end)

        if left <= end:
            edge = node.get_edge(self.ord_position(left))
            start, end2, node2 = edge[0][0], edge[0][1], edge[1]

            pointer = start+self.length(left, end)
            # rule 3 - showstopper
            # char in the middle of the edge match
            if self.text[pointer] == self.text[char]:
                return (True, node)
            
            else:
                # rule 2 - split the edge
                split_node = Node(False)
                node.add_edge(self.ord_position(left),((start, pointer-1), split_node))
                split_node.add_edge(self.ord_position(pointer),((pointer, end2), node2))
                return (False, split_node)
        
        else:
            # parent of root (node) is None
            if node is None:
                return (True, self.root)
            # rule 2 - edge does not exist
            elif node.get_edge(self.ord_position(char)) is None:
                return (False, node)
            # rule 3 - showstopper
            # edge exists
            else:
                return (True, node)
    
    def canonize(self, node, val):
        # skip/count trick
        # traverse till the node is explicit (edge from the node is a leaf)

        left, end = val[0], val[1]
        print("canon", left, end)

        # edge case
        if node is None:
            if self.length(left, end) <= 0: 
                return (None, left) # terminal position
            else:
                left += 1
                node = self.root # reset the node to be the root

        if end < left:
            return (node, left)
        
        edge = node.get_edge(self.ord_position(left))
        ((start, end2), node2) = edge
        end2 = self.get_end(end2)

        while end2-start <= end-left: # while the edge length is larger than the active length

            left += end2-start+1 # increase the pointer to refer to the next char after the edge
            node = node2 # move onto the next node

            if left <= end:
                ((start, end2), node2) = node.get_edge(self.ord_position(left))
                end2 = self.get_end(end2)

        return (node, left)

    def values(self, i):
        # print values for checking
        print(i, self.active_node, self.active_edge, self.active_length, self.remainder)
    
    def check(self, node):
        # traverse tree
        if node is None:
            return
        else:
            for i in range(len(node.edges)):
                if node.edges[i] is not None:
                    print(node, node.get_suffix_link(), node.edges[i][0][0], node.edges[i][0][1], node.edges[i][1])
                    self.check(node.edges[i][1])

# function calls to test
#SuffixTree('abcabxabcyab').build_tree() # success
#SuffixTree('mississippi').build_tree() # success
#SuffixTree('dedododeeodoeodooedeeododooodoede').build_tree() # success
#SuffixTree('abcabxabcyab').build_tree()


