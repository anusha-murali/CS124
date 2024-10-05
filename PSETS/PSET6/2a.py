import random

def probN(N):
    m = N
    count = 0
    countN = 0
    while (m > 1):
        m = random.randint(1,N)
        count = count + 1
        if (m == N):
            countN = countN + 1

    return (count, countN)
