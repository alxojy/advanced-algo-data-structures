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
    z = z_algorithm(pat)
    sp = [0]*len(pat)

    for j in range(len(pat)-1,0,-1):
        i = j+z[j]-1
        sp[i] = z[j]

    return sp

def kmp(pat, txt):
    matches = []
    sp = sp_arr(pat)

    i = 0
    while i <= len(txt)-len(pat):
        count = 0
        while count < len(pat) and pat[count] == txt[i+count] :
            count += 1
        
        if count == len(pat):
            matches.append(i)
            i += count - sp[count-1]

        elif count - sp[count] > 0:
            i += count - sp[count-1]

        else:
            i += 1
                  
    return matches

patfile = open('pattern-collection.txt','r')
reffile = open('reference.txt','r')
reftxt = reffile.read().strip()
reffile.close()
w = open('file-match-1.txt','w')
i = 0
for line in patfile:
    #if i == 1:
    w.write(str(kmp(line.strip(), reftxt)))
    w.write("\n")
    #i += 1
patfile.close()
w.close()