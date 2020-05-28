# alex o

import sys

def boyer_moore(pat, txt):
    # initialise array to store starting indexes of match
    ret = []

    if len(pat) > len(txt) or len(pat) == 0: # edge cases
        return ret 

    # pat preprocessing
    bc = bad_character(pat)
    gs = good_prefix(pat)
    mp = matched_suffix(pat)

    prev_i, prev_mismatch = len(txt), len(txt) # stop & resume pointers
    i = len(txt)-len(pat) # start from right 
    flag = False # flag used for galil

    while i > -1:
        count = 0 
        # left to right comparisons
        while count < len(pat) and pat[count] == txt[i+count]:
            count += 1
         
            # galil's optimization - jump over from previous i to previous mismatch to compare
            if flag and i+count == prev_i: 
                count += prev_mismatch - prev_i

        if flag:
            flag = False
 
        # full match case
        if count >= len(pat): 
            count = len(pat) # if matched suffix rule used, count reinitialise to len(pat)
            ret.append(i+1) # store match. index starts from 1
            i -= len(pat) - mp[len(pat)-2]
        
        # consider bad character & good prefix rules
        else:
            bad_shift = bc_shift(bc, txt, i, count, pat) # bad character shift
            g_shift = gpms_shift(count, pat, mp, gs)

            # galil 
            if g_shift > bad_shift or (bad_shift == g_shift and count > 0):
                flag = True 
                prev_i = i 
                prev_mismatch = i+count     

            i -= max(bad_shift, g_shift) 
    
    return ret

def bc_shift(bc, txt, i, count, pat):
    # determine the number of shifts using bad character rule
    if bc[ord(txt[i+count])-32] is None: # char not in pat
        bad_shift = len(pat) - count
    else:
        bad_shift = max(1, bc[ord(txt[i+count])-32][count]-count)

    return bad_shift

def gpms_shift(count, pat, mp, gs):
    # determine the number of shifts using good prefix/ matched suffix rule
    if gs[count] == 0: # matched suffix rule
        g_shift = len(pat) - mp[count-1]
    else:
        g_shift = gs[count] # good prefix rule
    
    return g_shift

def bad_character(pat):
    NO_ASCII_CHARS = 96
    # initialise bad character table
    bc = [None]*NO_ASCII_CHARS
    n = len(pat)

    for j in range(n):
        if bc[ord(pat[j])-32] is None:
            # initialise row if char doesnt exist yet
            bc[ord(pat[j])-32] = [n]*n
            bc = bad_char_row(bc, ord(pat[j])-32, j, n)
        else:
            # char already exist from previous comparisons
            bc = bad_char_row(bc, ord(pat[j])-32, j, n)
    
    return bc

# helper function for bad character table
def bad_char_row(bc, row, j, n):
    bc[row][j] = j
    k = j-1
    while k > -1 and bc[row][k] == n:
        bc[row][k] = bc[row][k+1] 
        k -= 1
    
    return bc

def good_prefix(pat):
    """
    Substring matched is present in rhs of pat. 
    :returns: the good prefix array
    """
    n = len(pat)
    z = z_algorithm(pat)
    gs = [0]*(n+1)

    for j in range(len(pat)-1,0,-1):
        i = z[j]-n-1    
        gs[i] = j
    return gs

def matched_suffix(pat):
    """
    k+1 is the mismatched position. ranges below are inclusive of the highest value
    matched_suffix[k] is the length of the longest prefix of pat[0...k] that is identical
    to the suffix of pat[len(pat)-k...len(pat)-1]
    """
    z = z_algorithm(reverse(pat))

    for i in range(len(pat)-1,-1,-1):
        if z[i] + i != len(pat) and i+1 < len(pat):
            z[i] = z[i+1]
    
    z.reverse()
    return z

# reverse the string
def reverse(str):
    ret = ''
    for i in str:
        ret = i + ret
    return ret

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

if __name__ == "__main__":
    txtfile = open(sys.argv[1], "r")
    patfile = open(sys.argv[2], "r")

    txt = txtfile.read().strip()
    pat = patfile.read().strip()

    w = open('output_mirrored_boyermoore.txt','w')
    result = boyer_moore(pat, txt)
    for line in result:
        w.write(str(line) + "\n")

    txtfile.close()
    patfile.close()
    w.close()


