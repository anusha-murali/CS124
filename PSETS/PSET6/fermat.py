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


def fermatPrime(n):

    a = random.randrange(3, n)
    while (n%a == 0):
        a = random.randrange(3, n)

    if (modPower(a, n-1, n) == 1):
        return True

    print("Fermat witness for compositeness is = ",a)
    return False


