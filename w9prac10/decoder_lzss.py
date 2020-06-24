# alex o

from elias_omega import *
from huffman import *
from z_algorithm import z_algo
import sys

class Node:
    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

class BST:
    # bst used for huffman
    def __init__(self):
        self.root = Node()

    def insert(self, huffman, ascii_code, binarr):
        node = self.root
        for i in range(huffman[0],huffman[1]-1):
            if not binarr[i]:
                if node.left is None:
                    new_node = Node()
                    node.left = new_node
                node = node.left
            else:
                if node.right is None:
                    new_node = Node()
                    node.right = new_node
                node = node.right

        new_node = Node(ascii_code)
        if not binarr[huffman[1]-1]:
            node.left = new_node
        else:
            node.right = new_node

    def search(self, binarr, start=0):
        node = self.root
        i = 0
        while node.value is None:
            if not binarr[start+i]:
                node = node.left
            else:
                node = node.right
            i += 1
            
        return node, i

class Decoder:

    def __init__(self, filename):
        self.binary = bitarray()
        self.filename = filename
        self.bst = BST()
        self.elias = EliasOmega()
        self.byte_to_bin() # get bitstr 
        self.build_bst()

    def byte_to_bin(self):
        r = open(self.filename,'rb')

        y = [x for x in r.read()]

        for i in y:
            bitrep = self.elias.dec_to_bin(i,bitarray())
            if bitrep is not None:
                if self.elias.bitarray_length(bitrep) < 8:
                    self.binary += bitarray('0'*(8-len(bitrep)))+bitrep
                else:
                    self.binary += bitrep
            else:
                self.binary += bitarray('0'*8)
        
    def build_bst(self):
        # used for header
        unique_chars = self.elias.decode(self.binary) # get number of unique chars
        start = unique_chars[1]
        for i in range(unique_chars[0]):
            ascii_code = (start, start+7) # pointers for start and end. end exclusive
            start += 7
            elias_len = self.elias.decode(self.binary,start)
            start += elias_len[1]
            huffman = (start, start+elias_len[0]) # pointers. end exclusive
            start += elias_len[0]
            self.bst.insert(huffman, ascii_code, self.binary)
        
        self.lzss_decoder(start)
    
    def lzss_decoder(self, start):
        num_of_formats = self.elias.decode(self.binary,start)
        start += num_of_formats[1]
        ret_str = ''
        for i in range(num_of_formats[0]):
            if self.binary[start]:
                start += 1
                ascii_code, huffman_len = self.bst.search(self.binary,start)
                ret_str += chr(int(self.binary[ascii_code.value[0]:ascii_code.value[1]].to01(),2))
                start += huffman_len
            elif not self.binary[start]:
                start += 1
                length1, elias_len1 = self.elias.decode(self.binary,start)
                start += elias_len1
                length2, elias_len2 = self.elias.decode(self.binary,start)
                start += elias_len2
                begin = len(ret_str)-length1
                for j in range(length2):
                    ret_str += ret_str[begin+j]

        out = open('output_decoder_lzss.txt','w')
        out.write(ret_str)
        out.close()

if __name__ == "__main__":
    Decoder(sys.argv[1])
