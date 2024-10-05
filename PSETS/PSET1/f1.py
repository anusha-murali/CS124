import time

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

startTime = time.time()
print(fib(40))
print("%-14s:%.4f seconds" % ("Elapsed time",time.time() - startTime))
