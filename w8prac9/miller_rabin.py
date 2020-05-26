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
        
        for i in range(1,s+1):
            
            flag = True if pow(a, pow(2,i-1)*t, n) in (1,n-1) else False # check prev

            if pow(a, pow(2,i)*t, n) == 1 and not flag:
                return False
        
    return True # prime

