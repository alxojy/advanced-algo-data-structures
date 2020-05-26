import random
import math

def miller_rabin_randomized_primality(n, k):
    # return true if it's composite
    # return false if probably prime
    if n % 2 == 0:
        return "Composite1"

    s, t = 0, n-1
    while t % 2 == 0:
        s += 1
        t = t >> 1 # divided by 2

    for _ in range(k):
        a = random.randint(2,n-1)
        if pow(a,n-1,n) != 1:
            return "Composite2"
        
        for i in range(1,s+1):
            if pow(a, int(pow(2,i)*t), n) == 1 and pow(a, int(pow(2,(i-1))*t), n) != (1 or -1):
                return "Probably prime"
        
    return "Probably prime"

print(miller_rabin_randomized_primality(11,8))
