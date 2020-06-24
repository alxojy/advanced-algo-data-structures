# alex o

import math

def z_algo(string, start, separator, end):
    window, buffer = separator-start, end-separator+1
    z = [None]*(window+(2*buffer)) # initialise z array
    z[0] = window+(2*buffer) # initialise first position of z array
    max_val, max_index = -math.inf, 0 # max match length and index 
    
    L, R = 0, 0
    for i in range(1,z[0]):
        
        off, off1 = 0, 0
        if i + separator > end:
            off = window+buffer
            
        if i > R: # case 1 - no z box
            count = 0
            while (i + count) < z[0] and string[separator+i+count-off] == string[separator+count-off1]:
                if i+separator+count-off >= end:
                    off = window+i+1
                
                if separator+count-off1 >= end:
                    off1 = window+1
                count += 1
                
            if count > 0:
                L,R = i,i+count-1
                
            z[i] = count    

        # case 2 - in z box
        else:
            remain, k = R-i+1, i-L
            
            if z[k] < remain: # case 2a 
                z[i] = z[k]
            
            elif z[k] > remain: # case 2b
                z[i] = remain
            
            else: # case 2c
                # compare str[remain] onwards
                count = 0
                while (R+1+count) < z[0] and string[R+1+count+separator-off] == string[R-i+1+count+separator-off1]:
                    if R+1+separator+count-off >= end:
                        off = window+i+1
                
                    if R-i+1+separator+count-off1 >= end:
                        off1 = window+1
                    count += 1

                if count > 0:
                    L, R = i, i+remain+count-1

                z[i] = remain+count

        if buffer+window > i >= buffer:
            if z[i] >= max_val:
                max_val, max_index = min(buffer,z[i]), window+buffer-i
    
    return max_index, max_val
    