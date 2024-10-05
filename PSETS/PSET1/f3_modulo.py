import time
import numpy as np


def fib(k):
    f = ([0], [1])
    mat = ([1, 1], [1, 0])
    
    for i in range(k):
        mat = (np.mod(np.linalg.matrix_power(mat, 2), 65536))
        
    f = np.mod(np.dot(mat, f), 65536)

    print("I am here")
    
##    for i in range(1, n+1):
##        f = np.mod(np.dot(mat, f), 65536)
        # f = np.mod(np.matmul(mat, f), pow(2, 16))

    return f[0][0]

startTime = time.time()
print(fib(40000000))
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


