import time
import numpy as np

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return np.mod(fib(n-1), 65536) + np.mod(fib(n-2), 65536)


##startTime = time.time()
##print(fib(39))
##print("%-14s:%.4f seconds" % ("Elapsed time",time.time() - startTime))

done = False
k = 39
while not done:
    startTime = time.time()
    print(fib(k))
    if (time.time() - startTime) > 60:
        print("k_max = ", k)
        done = True
        print("%-14s:%.4f seconds" % ("Elapsed time",time.time() - startTime))
    k = k + 1
        

