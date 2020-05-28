from numpy import binary_repr

class EliasOmega:
    
    def __init__(self, code):
        self.code = self.dec_to_bin(code) # binary 
        self.elias_omega = ""
    
    def dec_to_bin(self, i):
        return binary_repr(i, width=None)
        #return "{0:b}".format(i)

    def encode(self):
        if self.code == '1': # base case = 1
            return '1'

        return '0' + self.encode_aux(True)

    def encode_aux(self, flag):
        if len(self.code)-1 > 0:
            if self.code[0] == '1' and not flag:
                self.code = '0' + self.code[1:]
            self.elias_omega = self.code + self.elias_omega
            self.code = self.dec_to_bin(len(self.code)-1)
            self.encode_aux(False)
            
        return self.elias_omega
    
    def decode(self):
        return self.decode_aux(self.code, 0)

    def decode_aux(self, code, n):
        if code[n] == '0':
            n = self.bin_to_dec('0'+ code[1:n])
            self.decode_aux(code, n+1)
        else:
            return code[n:]

    def bin_to_dec(self, n):
        return int(n, 2)

print(EliasOmega(5).decode())