import random

# Compute (u^v) % p
def modPower(u, v, p):
    answer = 1
    u = u % p
    while (v > 0):
        if (v & 1):
            answer = (answer *u)%p;
        v = v >> 1
        u = (u * u) % p
    return answer


def MR(n, d):
    # Select a random number from [2..n-2]
    a = 2 + random.randint(1, n-4)

    # Compute a^d % n
    m = modPower(a, d, n);

    print("a = ", m)
    
    if (m == 1 or m == n -1):
        return True;

    while (d != n-1):
        m = (m*m)%n
        d = d*2
        if (m == 1):
            return False
        elif (m == n-1):
            return True

    return False;
    


# If this function returns false, n is definitely a composite.
# If it returns true, n is PROBABLY a prime. We use the parameter k
# increase the probability that n is a prime.
def isPrime(n, k):
    if n == 2 or n == 3:
        return True;

    # Find d such that n-1 = d*2^s
    d = n-1
    count = 0
    while (d%2 == 0):
        d = d // 2;
        count = count + 1
    print("n = ", n, "i = ",  count, " u = ", d)

    # Perform Miller-Rabin primality test k times to improve accuracy
    for i in range(k):
        if (MR(n, d) == False):
            return False;

    return True;
