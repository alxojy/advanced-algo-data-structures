# Megan Ooi Jie Yi
# 30101670

import sys

def z_algorithm(str):
    # initialise z array
    z = [None]*len(str)
    # initialise first position of z array
    z[0] = len(str)
    
    L, R = 0, 0
    for i in range(1,z[0]):
        # case 1 - no z box
        if i > R:
            count = 0
            while (i + count) < z[0] and str[i+count] == str[count]:
                count += 1
            if count > 0:
                L,R = i,i+count-1
            z[i] = count

        # case 2 - in z box
        else:
            remain, k = R-i+1, i-L

            # case 2a 
            if z[k] < remain:
                z[i] = z[k]
            
            # case 2b
            elif z[k] > remain:
                z[i] = remain

            # case 2c
            else:
                # compare str[remain] onwards
                count = 0
                while (R+1+count) < z[0] and str[R+1+count] == str[R-i+1+count]:
                    count += 1
                if count > 0:
                    L, R = i, i+remain+count-1
                z[i] = remain+count
    
    return z

def sp_arr(pat):
    # generate spix array
    z = z_algorithm(pat)
    ASCII = 96
    sp = [-1]*ASCII 
    sp[ord(pat[0])-32] = [0]*len(pat)

    for j in range(len(pat)-1,0,-1):
        i = j+z[j]-1
        x = ord(pat[z[j]])-32 # character position
 
        if sp[x] == -1: # initialise array if character doesn't exist yet
            sp[x] = [-1]*len(pat)
            
        sp[x][i] = z[j]

    return sp

def kmp(pat, txt):
    matches = [] # store matches
    
    if pat == "" or len(pat) > len(txt):
        return matches
    
    sp = sp_arr(pat) # preprocess

    i = 0
    count = 0
    while i <= len(txt)-len(pat):
        while count < len(pat) and pat[count] == txt[i+count]:
            count += 1
        
        if count == len(pat): # full match
            matches.append(i+1) # indexes start from 1
            shift = count - spix_val(sp, txt, count, i) # shift pat by this amount
            count = start_count(spix_val(sp, txt, count, i)) # index to start comparing from

        elif count > 0:
            shift = count - spix_val(sp, txt, count, i) # shift pat by this amount
            count = start_count(spix_val(sp, txt, count, i)) # index to start comparing from
            
        else:
            shift = 1
        
        i += shift

    return matches

def start_count(val):
    # returns index to start comparing pat
    if val >= 0:
        count = val+1
    else:
        count = 0

    return count
    
def spix_val(sp, txt, count, i):
    if i+count < len(txt): # edge case, pat match till end of txt 
        # returns 
        if sp[ord(txt[i+count])-32] == -1:
            ret = -1
        else:
            ret = sp[ord(txt[i+count])-32][count-1]
    else:
        ret = -1

    return ret

if __name__ == "__main__":
    txtfile = open(sys.argv[1], "r")
    patfile = open(sys.argv[2], "r")

    txt = txtfile.read().strip()
    pat = patfile.read().strip()

    w = open('output_kmp.txt','w')
    result = kmp(pat, txt)
    for line in result:
        w.write(str(line) + "\n")

    txtfile.close()
    patfile.close()
    w.close()