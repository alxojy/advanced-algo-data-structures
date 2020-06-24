# alex o

from bitarray import bitarray

class EliasOmega:
    
    def __init__(self, code=0):
        self.code = self.dec_to_bin(code, bitarray()) # binary 
        self.elias_omega = bitarray()

    def bitarray_length(self, bitarr):
        info = bitarray.buffer_info(bitarr)
        return (info[1]*8) - info[3]

    def dec_to_bin(self, num, bitarr):
        if num == 0:
            return 

        self.dec_to_bin(num >> 1, bitarr)

        bitarr.append(num & 1)
        return bitarr

    def encode(self):
        if self.bitarray_length(self.code) == 1: # base case = 1
            return bitarray(1)

        return bitarray('0') + self.encode_aux(True)

    def encode_aux(self, flag):
        if self.bitarray_length(self.code)-1 > 0:
            if self.code[0] == 1 and not flag:
                self.code[0] = 0
            self.elias_omega = self.code + self.elias_omega
            self.code = self.dec_to_bin(len(self.code)-1, bitarray())
            self.encode_aux(False)

        return self.elias_omega
    
    def decode(self, code, start=0):
        # return int and length of elias encoding
        if not code[start]:
            i, length = 1, 2
            while not code[start+i]:
                temp = self.bin_to_dec(bitarray('1')+code[start+i+1:start+i+length])
                i += length
                length = temp+1

            return self.bin_to_dec(code[start+i:start+i+length]), i+length

        else:
            return 1, 1

    def bin_to_dec(self, n):
        return int(n.to01(), 2)
        