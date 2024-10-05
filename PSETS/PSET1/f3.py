import time
import numpy as np


def fib(k):
    f = ([0], [1])
    mat = ([1, 1], [1, 0])

    for i in range(k):
        mat = np.linalg.matrix_power(mat, 2)

    f = np.dot(mat, f)
    
    return f[0][0]

startTime = time.time()
fib(pow(2,24))
print("%-14s:%.4f seconds" % ("Elapsed time",time.time() - startTime))



