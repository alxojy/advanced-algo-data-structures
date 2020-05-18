# Binomial heap implementation reference: 
# Cormen et al., Introduction to Algorithms (Chapter 19)
# http://www.cs.toronto.edu/~anikolov/CSC265F16/binomial-heaps.pdf
import math 

class Node:
    # represents a node in a binomial tree
    def __init__(self, key, payload=None):
        self.degree = 0
        self.key = key
        self.payload = payload # store information if any
        self.parent = None
        self.child = None # leftmost child
        self.sibling = None # right sibling

class BinomialHeap:

    def __init__(self):
        self.head = None
        self.lookup = [None]*26

    def get_minimum(self):
        # returns the minimum node in the heap and the node before it (mainly for extract_min())
        min_node, min_val = None, math.inf # arbitrary large number for inf
        
        curr_head, prev = self.head, None # initialise pointer & previous node
        # check first value
        if curr_head.payload <= min_val:
            min_node = curr_head
            min_val = curr_head.payload

        # loop through all roots and check if it's the min value
        while curr_head is not None:
            if curr_head.sibling is not None and curr_head.sibling.payload <= min_val:
                min_val = curr_head.sibling.payload
                min_node = curr_head.sibling
                prev = curr_head
            curr_head = curr_head.sibling

        return min_node, prev # return node that is minimum and the previous node

    def insert(self, key, payload):
        # perform insertion into heap 
        new_node = Node(key, payload)
        if self.head is None: # empty heap
            self.head = new_node
            self.lookup[key] = new_node
            return 
        # create new heap with only 1 element
        new_node = Node(key, payload)
        self.lookup[key] = new_node
        new_heap = BinomialHeap()
        new_heap.head = new_node
        self.head = self.union(self, new_heap) # merge both heaps

    def tree_merge(self, tree1, tree2):
        # merge two trees of the same rank (ie. B0 + B0 = B1)
        tree1.parent = tree2
        tree1.sibling = tree2.child
        tree2.child = tree1
        tree2.degree += 1

    def heap_merge(self, h1, h2):
        # merges 2 binomial heaps into a single linked list in monotically increasing order
        new_heap = BinomialHeap() # create new heap
        # selects which head to point to for the new heap
        if h1.head.degree > h2.head.degree:
            new_heap.head = h2.head
            curr2 = h2.head.sibling
            curr1 = h1.head
        
        else:
            new_heap.head = h1.head
            curr1 = h1.head.sibling
            curr2 = h2.head

        new_head = new_heap.head

        # loop through both heaps to add into the linked list
        while curr1 is not None and curr2 is not None:
            if curr1.degree > curr2.degree:
                new_head.sibling = curr2
                new_head = new_head.sibling
                curr2 = curr2.sibling

            else:
                new_head.sibling = curr1
                new_head = new_head.sibling
                curr1 = curr1.sibling
        
        # handle case with unequal number of trees in both heaps
        pointer = curr2 if curr1 is None else curr1
        if pointer is not None:
            new_head.sibling = pointer
        
        return new_heap # return new heap

    def union(self, h1, h2):
        # this function unites h1 and h2 and ensures that there is only 1 of each order of trees in the new heap
        new_heap = self.heap_merge(h1, h2) 
        curr_head = new_heap.head # current root

        if curr_head is None: # empty heap
            return new_heap

        prev = None
        next_head = curr_head.sibling
        while next_head is not None:
            # no need to merge trees. move to next root
            if (curr_head.degree != next_head.degree) or (next_head.sibling is not None and next_head.sibling.degree == curr_head.degree):
                prev = curr_head
                curr_head = next_head
            
            else:
                if curr_head.payload <= next_head.payload: # case 3 - remove next tree from linked list and link it to current tree
                    curr_head.sibling = next_head.sibling
                    self.tree_merge(next_head, curr_head)
                
                else:
                    if prev is None: # case 4 - remove current tree from linked list and link it to next tree
                        new_heap.head = next_head
                    else:
                        prev.sibling = next_head
                        
                    self.tree_merge(curr_head, next_head)
                    curr_head = next_head
                
            next_head = curr_head.sibling
        
        return new_heap.head
    
    def extract_min(self):
        # extract minimum value from heap
        min_node, prev_node = self.get_minimum() # get min node and the node before min

        if prev_node is not None:
            prev_node.sibling = min_node.sibling # extract root of heap with min node 
        else:
            self.head = min_node.sibling

        min_node_child = min_node.child
        min_val = min_node.payload # minimum value to return
        self.lookup[min_node.key], min_node = None, None
        
        h2 = BinomialHeap() # create new heap
        if min_node_child is not None: # there are children below min node
            h2.head = self.extract_min_aux(min_node_child)

        # check if any of the heaps are empty
        if self.head is None:
            self.head = h2.head
        elif h2.head is None:
            pass
        else:
            self.head = self.union(self, h2) # merge both heaps
        
        return min_val # return minimum value
    
    def extract_min_aux(self, node):
        # reverse the linked list so that it is sorted in increasing order
        if node.sibling is None or node is None:
            return node

        new = self.extract_min_aux(node.sibling)
        new.parent, node.parent = None, None # remove reference to parent 
        node.sibling.sibling = node
        node.sibling = None

        return new
    
    def decrease_key(self, key, new_val):
        node = self.lookup[key]
        if node is None:
            assert "key doesn't exist"

        if new_val > node.payload:
            assert "new value > current value of key"
        
        node.payload = new_val # reassign new value
        curr = node # current node

        while curr.parent is not None and curr.payload < curr.parent.payload:
            # swap payload, key and value in lookup table
            curr.payload, curr.parent.payload = curr.parent.payload, curr.payload
            curr.key, curr.parent.key = curr.parent.key, curr.key
            self.lookup[curr.key], self.lookup[curr.parent.key] = self.lookup[curr.parent.key], self.lookup[curr.key]
            curr = curr.parent # go up to parent

    def delete(self, key):
        self.decrease_key(key, -math.inf)
        self.extract_min()

    def check(self):
        input('-----CHECK-----CHECK-----')
        print(self.lookup)
        for node in self.lookup:
            if node is not None:
                if node.key is not None:
                    print('key', node.key)
                if node.payload is not None:
                    print('payload', node.payload)
                if node.parent is not None:
                    print('parent', node.parent.key)
                if node.sibling is not None:
                    print('sibling', node.sibling.key)
                if node.child is not None:
                    print('child', node.child.key)
                print("----------")
                
"""
b = BinomialHeap()
b.insert(11, 0)
b.insert(12, 40)
b.insert(10,-5)
b.insert(0, 5)
b.insert(1,20)
b.insert(2,15)
b.insert(3,70)
b.insert(4,10)
b.insert(5,1)
b.insert(6,8)
b.insert(7,15)
b.insert(8,18)
b.insert(9,19)
print(b.head.key)
print(b.head.child.key)
print(b.head.child.child.key)
print(b.head.child.child.child.key)
print(b.head.child.child.sibling.key)
print(b.head.child.sibling.key)
print(b.head.child.sibling.child.key)
print(b.head.child.sibling.sibling.key)
"""