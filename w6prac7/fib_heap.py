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

    def __init__(self, size=26):
        self.min_head = None # pointer to the min element in the heap
        self.lookup = [None]*size
        self.n = 0 # store number of nodes

    def get_minimum(self):
        return self.min_head # return minimum node

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

        self.lookup[key] = node # insert into lookup table
        self.n += 1
    
    """def union(self, h1, h2):
        # used for merging 2 heaps of the same rank (ie. B0+B0=B1). O(1) complexity
        new_heap = FibonacciHeap() # create new heap
        return h1 if h1.min_head is None else h2 # check if one of the heaps is empty
        new_heap.min_head = self.merge_heaps(h1, h2)

        new_heap.n = h1.n + h2.n 
        return new_heap"""
    
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
                new_min = self.merge_heaps(self, z.child)

            self.remove(z)
            self.lookup[z.key] = None

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

                self.fib_link(y,x)
                A[d] = None
                d += 1

            A[d] = x

        self.min_head = None
        for i in range(D):
            if A[i] is not None:
                if self.min_head is None or A[i].payload < self.min_head.payload:
                    self.min_head = A[i]

    def decrease_key(self, key, new_value):
        key_node = self.lookup[key]
        if key_node is None:
            assert "node doesn't exist"
        if new_value > key_node.payload:
            assert "new value is more than current value for key"
        key_node.payload = new_value
        parent = key_node.parent

        if parent is not None and key_node.payload < parent.payload:
            self.cut(key_node, parent)
            self.cascading_cut(parent)

        if key_node.payload < self.min_head.payload:
            self.min_head = key_node

    def cut(self, x, y):
        # remove x from child list of y
        self.remove(x)
        if y.child == x and x.right != x: # reassign child
            y.child = x.right
        else:
            y.child = None
        y.degree -= 1
        x.right = x.left = x # link to itself
        x.parent = None
        x.mark = False
        self.merge_heaps(self, x) # add x to root list

    def cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if not y.mark:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    def delete(self, key):
        self.decrease_key(key, -math.inf)
        self.extract_min()

    def check(self):
        input("CHECKCHECKCHECKCHECKCHECKCHECK")
        print(self.lookup)
        print('min pointer', self.min_head.payload)
        for node in self.lookup:
            if node is not None:
                if node.key is not None:
                    print('key', node.key)
                if node.payload is not None:
                    print('payload', node.payload)
                if node.parent is not None:
                    print('parent', node.parent.key)
                if node.right is not None:
                    print('right', node.right.key)
                if node.left is not None:
                    print('left', node.left.key)
                if node.child is not None:
                    print('child', node.child.key)
                if node.mark is not None:
                    print('mark', node.mark)
                print("----------")
        
