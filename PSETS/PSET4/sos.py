def sumOverSubsets(A, n):
    P = [0]*(1 << n)

    for i in range(1 << n):
        P[i] = A[i]

    for i in range(n):
        for mask in range(1<<n):
            if (mask & (1<<i)):
                P[mask] = P[mask] + P[mask^(1<<i)]
    

    for i in range (1 << n):
        print(P[i]%2, end = " ")

        # Driver Code
if __name__ == '__main__':

	#a = [1, 1, 0, 1]
	a = [1, 0, 1, 1]
##	# a = [1, 2, 1, 3]
##	
##	a = [7, 11, 13, 16]
##	a = [7, 18, 20, 47]
##	# a = [1, 1, 1, 0]
	n = 2
	sumOverSubsets(a, n)
