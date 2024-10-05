import time
import numpy as np

def fib(n):
    f = [0, 1]

    for i in range(2, n+1):
        f.append(np.mod(f[i-1], 65536) + np.mod(f[i-2], 65536))
    return f[n]


startTime = time.time()
print(fib(67108864))
print("%-14s:%.4f seconds" % ("Elapsed time",time.time() - startTime))


    
##done = False
##k = 39
##while not done:
##    startTime = time.time()
##    print(fib(k))
##    if (time.time() - startTime) > 60:
##        print("k_max = ", k)
##        done = True
##        print("%-14s:%.4f seconds" % ("Elapsed time",time.time() - startTime))
##    k = k + 1
