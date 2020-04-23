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

def find_substrings(pat):
    """
    :return: longest substrings in pat without '?'. ie. du??de?, returns [(0,1),(4,5)] aka {du,de}
    """
    substrings = []
    start = -1
    end = -1

    for i in range(len(pat)):
        if (i == 0 and pat[0] != '?') or (pat[i-1] == '?' and pat[i] != '?'):
            start = i
        if (i == len(pat)-1 and pat[i] != '?') or (i < len(pat)-1 and pat[i+1] == '?' and pat[i] != '?'):
            end = i
            substrings.append((start, end))
    
    return substrings

def wildcard(pat, txt):
    substrings = find_substrings(pat)

    z_arrays = [] # store z array for all the substrings
    matches = [] # store matches

    if substrings == []: # all wildcards
        for i in range(len(txt)-len(pat)+1):
            matches.append(i+1)

    else:
        for substr in substrings:
            s = ""
            for i in range(substr[0],substr[1]+1):
                s += pat[i] # generate substring

            z = z_algorithm(s + '$' + txt) # run z algo
            z_arrays.append(z)

        for i in range(len(txt)-len(pat)+1):
            for j in range(len(substrings)): # loop through all longest substrings without ?
                start, end = substrings[j][0], substrings[j][1] # start, end positions of substring
                substr_len = end-start+1 # length of substring

                if z_arrays[j][i+substr_len+start+1] != substr_len: # substring of txt doesn't match with substring in pat
                    break
                elif j+1 == len(substrings): # all substrings match
                    matches.append(i+1)
        
    return matches

if __name__ == "__main__":
    txtfile = open(sys.argv[1], "r")
    patfile = open(sys.argv[2], "r")

    txt = txtfile.read().strip()
    pat = patfile.read().strip()

    w = open('output_wildcard_matching.txt','w')
    result = wildcard(pat, txt)
    for line in result:
        w.write(str(line) + "\n")

    txtfile.close()
    patfile.close()
    w.close()