P = [6,2,9,5,1,4,1,3]
D = [2,3,1,1,5,7,1,7,1,4,1,3,3,9,3,8,7,6,1,4,9,1,3,8,4,3,8,6,4,1] 

p = 1249

P = [6, 2]
D = [3,9,7,9,8,5,3,5,6,2,9,5,1,4,1,3]

p = 11

def printD(D, k):
    n = len(D)
    for i in range(n-k+1, -1, -1):
        print(D[i], end="")

def HP(P, p):
    ans = 0
    for i in range(len(P)):
        ans = (ans + (P[i]*(10**i))%p)%p
    return ans

def HK(k, p):
    return (10**k)%p

def HDK(D, k, p):
    ans = 0
    n = len(D)
    for i in range(k):
        ans = (ans + (D[n-k+i]*(10**i))%p)%p
    return ans

#def HDI(D, i, k, p):
    
    
def fp(P, D, p):
    n = len(D)
    k = len(P)
    hp = HP(P, p)
    hdk = HDK(D, k, p)

    for i in range(n-k, -1, -1):
        tempD = D[i:i+k]
        if (HDK(tempD, k, p) == hp):
            print("i = ", i, end = " ")
            print(tempD)
    


def findP(P, seed, p):
    k = 7
    a = seed[0]
    b = seed[len(seed)-1]
    front = 0
    for i in range(100):
        front = seed[i]
        back = (front*10**(k) - 9*P)%p
        seed.append(back)
    return seed
        
