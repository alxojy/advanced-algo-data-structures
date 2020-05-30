# alex o

# fibonacci heap reference:
# Introduction to Algorithms by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest
# http://staff.ustc.edu.cn/~csli/graduate/algorithms/book6/chap21.htm
import math 

class Node:
    # represents a node in a binomial tree
    def __init__(self, key, payload=None):
        self.degree = 0
        self.key = key
        self.payload = payload # store information if any
        self.parent = None
        self.child = None # leftmost child
        self.left = None # left sibling
        self.right = None # right sibling
        self.mark = False # indicate if node is marked
    
    def get_siblings(self):
        siblings = []
        curr, visited = self, False
        while curr != self or not visited:
            if curr == self:
                visited = True
            
            siblings.append(curr)
            curr = curr.right
        
        return siblings

class FibonacciHeap:

    def __init__(self, size=256):
        self.min_head = None # pointer to the min element in the heap
        self.lookup = [None]*size
        self.n = 0 # store number of nodes

    def get_minimum(self):
        return self.min_head # return minimum node
    
    def ord_position(self, char):
        return ord(char)

    def insert(self, key, payload):
        # insert new node into heap - O(1)
        node = Node(key, payload) # create new node

        if self.min_head is None: # empty heap
            self.min_head = node
            self.min_head.left = self.min_head.right = self.min_head # link to itself

        else:
            # reassign pointers to point to the correct nodes
            node.left = self.min_head.left 
            node.right = self.min_head
            self.min_head.left.right = self.min_head.left = node

            if node.payload < self.min_head.payload: # reassign min pointer if necessary
                self.min_head = node
            elif node.payload == self.min_head.payload:
                self.min_head_reassignment(node)

        self.n += 1
    
    def min_head_reassignment(self, n):
        try:
            if len(self.min_head.key) > len(n.key):
                self.min_head = n
            elif ord(self.min_head.key) < ord(n.key):
                self.min_head = n
        except:
            pass

    def merge_heaps(self, h1, h2):
        # update pointers when merging - O(1)
        temp = h2.left
        h2.left = h1.min_head.left
        h1.min_head.left.right = h2
        h1.min_head.left = temp
        temp.right = h1.min_head

        return h1.min_head if h1.min_head.payload < h2.payload else h2 # return minimum value

    def remove(self, node):
        # this function removes the node from the root list
        node.left.right = node.right
        node.right.left = node.left

    def fib_link(self, tree1, tree2):
        # link 2 trees with same order (ie. B0 + B0 = B1)
        # tree1 root value > tree2 root value (tree2 will be parent of tree1)
        self.remove(tree1) # remove tree1 from root list
        
        tree1.right = tree1.left = tree1 # link to itself

        tree1.parent = tree2 # assign parent
        tree2.degree += 1
        tree1.mark = False

        if tree2.child is None:
            tree2.child = tree1 
            return 

        # reassign pointers
        tree1.right = tree2.child.right
        tree1.left = tree2.child
        tree2.child.right.left = tree2.child.right = tree1

    def extract_min(self):
        z = self.min_head
        if z is not None:
            if z.child is not None:
                for sibling in z.child.get_siblings(): # loop through child
                   sibling.parent = None # remove link to parent
                self.merge_heaps(self, z.child)

            self.remove(z)
            #self.lookup[self.ord_position(z.key)] = None

            if z == z.right:
                self.min_head = None
            else:
                self.min_head = z.right
                self.consolidate()
        
            self.n -= 1

        return z

    def consolidate(self):
        D = int(math.log(self.n, 2))+1 # highest degree + 1
        A = [None]*D # helper array
        
        for w in self.min_head.get_siblings():
            x = w
            d = x.degree
            next_node = w.right

            while A[d] is not None:
                y = A[d]
                if x.payload > y.payload:
                    x,y = y,x # swap
                
                elif x.payload == y.payload:
                    
                    try:
                        if len(x.key) > len(y.key):
                            x,y = y,x # swap
                        elif ord(x.key) > ord(y.key):
                            x,y = y,x # swap

                    except:
                        pass

                self.fib_link(y,x)
                A[d] = None
                d += 1

            A[d] = x

        self.min_head = None
        for i in range(D):
            if A[i] is not None:
                if self.min_head is None or A[i].payload < self.min_head.payload:
                    self.min_head = A[i]
                elif self.min_head.payload == A[i].payload:
                    self.min_head_reassignment(A[i])
    
class Huffman:
    # reference fro Huffman code: http://math.ubbcluj.ro/~tradu/TI/huffmancode.pdf. 

    def __init__(self, text, size=256):
        self.text = text
        self.dictionary = [0]*size # default size = 256 for 256 alphabets
        self.heap = FibonacciHeap() # min heap
        self.unique_chars = 0 # number of unique characters
        self.calculate_frequency() # calculate frequency of each char in text

    def ord_position(self, char):
        return ord(char)

    def get_character(self, pos):
        return chr(pos)

    def calculate_frequency(self):
         # calculate frequency of each char in text
        for char in self.text:
            self.dictionary[self.ord_position(char)] += 1

        self.make_heap()
    
    def make_heap(self):
        # create priority queue based on frequency of chars
        for i in range(len(self.dictionary)):
            if self.dictionary[i] > 0:
                self.heap.insert(self.get_character(i), self.dictionary[i]) # O(1) insert
                self.unique_chars += 1

        self.huffman()
        
    def huffman(self):
        # huffman coding using priority queue
        for i in range(1, self.unique_chars):
            first = self.heap.extract_min()
            second = self.heap.extract_min()
            
            self.encode(first, True)
            self.encode(second, False)

            new = (first.payload + second.payload, first.key + second.key) # add both frequencies
            self.heap.insert(first.key + second.key, first.payload + second.payload)
    
    def encode(self, elem, left):
        for char in elem.key:

            if type(self.dictionary[self.ord_position(char)]) == int:
                self.dictionary[self.ord_position(char)] = ''

            if left:
                self.dictionary[self.ord_position(char)] += '0'
            else:
                self.dictionary[self.ord_position(char)] += '1'

    def get_code(self, char):
        if type(self.dictionary[self.ord_position(char)]) != str:
            assert "encoding not found"

        return ''.join(reversed(self.dictionary[self.ord_position(char)]))
