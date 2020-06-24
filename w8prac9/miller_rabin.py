# alex o

import random
import math

def miller_rabin_randomized_primality(n, k):
    # return true if it's probably prime
    # return false if composite

    if n == 2 or n == 3: # base cases
        return True

    if n % 2 == 0: # even number 
        return False

    s, t = 0, n-1 # initialisation 
    while t % 2 == 0:
        s += 1
        t = t >> 1 # divided by 2
 
    for _ in range(k):
        a = random.randrange(2,n-1) # 2 to n-2 inclusive 

        if pow(a,n-1,n) != 1:
            return False

        curr = pow(a, t, n)
        for i in range(1,s+1):
            prev = curr 
            curr = pow(curr,2,n) # repeated squaring
            flag = True if prev in (1,n-1) else False # check prev
            if curr == 1 and not flag:
                return False
                
    return True # prime
    
def repeated_squaring(num, power, modulo):
    ret, curr = 1, None
    
    while power > 0:
        curr = (num % modulo) if curr is None else pow(curr,2,modulo)
        if power % 2 == 1:
            ret = ret*curr % modulo
        power = power >> 1
    
    return ret