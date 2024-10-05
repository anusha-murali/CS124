import sys
sys.set_int_max_str_digits(10000000)
import time

def fib(n):
    f = [0, 1]

    for i in range(2, n+1):
        f.append(f[i-1] + f[i-2])
    return f[n]


startTime = time.time()
print(fib(40))
#print(fib(pow(2,10)))
print("%-14s:%.4f seconds" % ("Elapsed time",time.time() - startTime))

##print("2^31 = ",pow(2,31))
##
##for i in range(1,50):
##    if (fib(i) >= pow(2, 31)):
##        print("i = ", i, "F = ", fib(i))
##    
