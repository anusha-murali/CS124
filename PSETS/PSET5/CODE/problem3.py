##import numpy as np
import scipy.special
import math

def computeP(n, m, k, theta):
    p = 0.0
    for i in range(theta):
        #p = p + math.comb(k*n, i)*((1/m)**i)*(1-1/m)**(k*n-i)
        p = p + scipy.special.binom(k*n, i)*((1/m)**i)*(1-1/m)**(k*n-i)

    return 1 - p
    


def computeP2(n, m, k, theta):
    p = 0.0
    for i in range(theta):
        a = k*n-i
        b = (1-1/m)**a
        c = (1/m)**i
        d = math.comb(k*n, i)
        e = d*c*b
        if (e > 10**(-6)):
            p = p + d*c*b

    return 1 - p 


def computeP3(n, m, k, theta):

    p = math.comb(k*n, theta)*(1/(m**theta))

    return p


N = [1000, 10000, 100000]

##print("Following users computeP")
##for i in range(len(N)):
##    p = computeP(N[i], 8*N[i], 5, 16)
##    print("p = ", p, "E(X) = ", p*N[i])
##    

##print("Following users computeP2")
##for i in range(len(N)):
##    p = computeP2(N[i], 8*N[i], 5, 16)
##    print("p = ", p, "E(X) = ", p*N[i]*8)


##print(" ")
##print("Following users computeP3")
##for i in range(len(N)):
##    p = computeP3(N[i], 8*N[i], 5, 16)
##    print("p = ", p, "E(X) = ", p*N[i])


def prob3(n, k, theta):
    m = 8*n
    p = 0.0*10**(-15)
    for i in range(theta):
        a = math.comb(k*n, i)
        b = pow(1/m, i)
        c = pow((1-1/m), (k*n-i))
        x = a*b*c
        if (x > 10**(-20)):
            p = p + x
            # print(p)
    return (1-p)

for i in range(len(N)):
    p = prob3(N[i], 5, 16)
    print("p = ", p, "E(X) = ", p*N[i]*8)
    

def prob32(n, k, theta):
    m = 8*n
    p = 0.0
    a = math.comb(n*k, 16)
    b = pow(1/m, 15)
    return (a*b)


def prob33(n, k):
    m = 8*n
    a = math.exp(1)*n*k
    b = 16*m
    c = pow(a/b, 16)
    return (m*c)

print("Loose upperbound")

for i in range(len(N)):
    p = prob33(N[i], 5)
    print("p = ", p, "E(X) = ", p*N[i]*8)
    
