"""
author: alex o
"""

def z_algorithm(str):
    n = len(str)
    # initialise z array
    z = [None]*n
    # initialise first position of z array
    z[0] = n
    
    L = 0
    R = 0
    for i in range(1,len(str)):
        
        # case 1 - no z box
        if i > R:
            count = 0
            while (i + count) < z[0] and str[i+count] == str[count]:
                count += 1
            if count > 0:
                L = i
                R = i+count-1
            z[i] = count
        else:
            remain = R-i+1
            k = i-L

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
                while (i+remain+count) < z[0] and str[R+1+count] == str[R-i+1+count]:
                    count += 1
                if count > 0:
                    L = i
                    R = i+remain+count-1
                z[i] = remain+count

    return z
