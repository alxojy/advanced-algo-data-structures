# alex o

import sys
from elias_omega import *
from huffman import *
from z_algorithm import z_algo
from bitarray import bitarray

class LZSS:

    def __init__(self, window, buffer, text):
        self.window = window
        self.buffer = buffer
        self.text = text
        self.huffman = Huffman(self.text, 128)
        self.byte_array = bytearray()
    
    def encode_header(self):
        byte = EliasOmega(self.huffman.unique_chars).encode() # number of unique characters
        for i in range(len(self.huffman.dictionary)):
            if self.huffman.dictionary[i] is not None:
                ascii_code = EliasOmega(i).dec_to_bin(i,bitarray())
                ascii_len = EliasOmega().bitarray_length(ascii_code)
                if ascii_len < 7:
                    ascii_code = bitarray('0'*(7-ascii_len))+ascii_code
                byte += ascii_code+EliasOmega(len(self.huffman.dictionary[i])).encode()+self.huffman.get_code(i)
        return byte

    def encode_data(self):
        i, max_val = 0, 1
        byte = bitarray('1') + self.huffman.get_code_char(self.text[0])

        separator, count = 1, 1
        while separator < len(self.text):
            match = z_algo(self.text, max(0, separator-self.window), separator, min(len(self.text)-1, separator+self.buffer-1))

            if match[1] < 3 or match[1] == -math.inf:
                byte += bitarray('1') + self.huffman.get_code_char(self.text[separator])
                separator += 1
            
            else:
                byte += bitarray('0') + EliasOmega(match[0]).encode() + EliasOmega(match[1]).encode()
                separator += match[1]

            count += 1

        byte = EliasOmega(count).encode() + byte
        return byte

    def encode(self):
        output = self.encode_header() + self.encode_data()
        out = bytearray()
        for i in range(0,len(output),8):
            if i > 0:
                out.append(int(output[i-8:i].to01(),2))

        remain_str = output[i::]
        remain = EliasOmega().bitarray_length(remain_str)      
        if remain > 0:
            out.append(int(remain_str.to01()+('0'*(8-remain)),2))

        output_file = open('output_encoder_lzss.bin','wb')
        output_file.write(out)
        output_file.close()

if __name__ == "__main__":
    filename = sys.argv[1]
    window = int(sys.argv[2])
    buffer = int(sys.argv[3])
    read_file = open(filename,'r')
    lines = read_file.read()
    LZSS(window,buffer,lines).encode()