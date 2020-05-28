# alex o
import heapq

class Node:

    def __init__(self, frequency, payload=None):
        self.frequency = frequency
        self.payload = payload
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.frequency < other.frequency
    
    def insert_left(self, node):
        self.left = node
    
    def insert_right(self, node):
        self.right = node
    
    def get_item(self):
        return self.payload
    
    def get_left(self):
        return self.left
    
    def get_right(self):
        return self.right
    

class Huffman:
    # reference fro Huffman code: http://math.ubbcluj.ro/~tradu/TI/huffmancode.pdf. 

    def __init__(self, text, size=256):
        self.text = text
        self.dictionary = [0]*size # default size = 26 for 26 alphabets
        self.heap = [] # min heap
        self.unique_chars = 0 # number of unique characters
        self.encoded = [None]*256 # stores encoding for each char
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
                heapq.heappush(self.heap, Node(self.dictionary[i], self.get_character(i))) # push (frequency, char ord position)
                self.unique_chars += 1

        self.check()
        self.huffman()
        
    def huffman(self):
        # huffman coding using priority queue
        for i in range(1, self.unique_chars):
            first = heapq.heappop(self.heap)
            second = heapq.heappop(self.heap)

            new = Node(first.frequency + second.frequency) # add both frequencies
            new.left, new.right = first, second
            heapq.heappush(self.heap,new)
    
    def traverse(self):
        if self.heap[0] is None: # no root, heap empty
            return None

        self.traverse_aux(self.heap[0], "") # call helper function
        return self.encoded
    
    def traverse_aux(self, node, code):
        if node.left is None and node.right is None and node.payload is not None:
            self.encoded[self.ord_position(node.payload)] = code
            return 

        self.traverse_aux(node.left, code + '0')
        self.traverse_aux(node.right, code + '1')