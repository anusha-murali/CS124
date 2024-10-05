
def sumOverSubsetsNOT_DP(a, n):
    sos = [0]*(1 << n)
    DP = [[0]*1000]*1000

    for i in range(1 << n):
        for j in range(n):
            if (i & (1 << j)):
                if (j == 0):
                    DP[i][j] = a[i] + a[i ^ (1 << j)]
                else:
                    DP[i][j] = DP[i][j-1] + DP[i ^ (1 << j)][j-1]
            else:
                if (j == 0):
                    DP[i][j] = a[i]
                else:
                    DP[i][j] = DP[i][j-1]
        sos[i] = DP[i][n-1]
    for i in range(1 << n):
        print(sos[i], end = " ")


def sumOverSubsetsWorking(a, n):
    sos = [0]*(1 << n)
    DP = [[0 for i in range(n)] for j in range(1 << n)]

    for i in range (1 << n):
        for j in range (n):
            if (i & ( 1 << j)):
                if (j == 0):
                    DP[i][j] = a[i] + a[i^1]
                else:
                    DP[i][j] = DP[i][j-1] + DP[i^(1 << j)][j-1]
            else:
                if (j == 0):
                    DP[i][j] = a[i]
                else:
                    DP[i][j] = DP[i][j-1]
        sos[i] = DP[i][n-1]

    for i in range (1 << n):
        print(sos[i], end = " ")

    print(DP)




def sumOverSubsetsWorking2(a, n):
    P = [0]*(1 << n)
    table = [[0 for i in range(n)] for j in range(1 << n)]

    for i in range (1 << n):
        for j in range (n):
            if (i & ( 1 << j)):
                if (j == 0):
                    table[i][j] = a[i] + a[i^1]
                else:
                    table[i][j] = table[i][j-1] + table[i^(1 << j)][j-1]
            else:
                if (j == 0):
                    table[i][j] = a[i]
                else:
                    table[i][j] = table[i][j-1]
        P[i] = table[i][n-1]

    for i in range (1 << n):
        print(P[i], end = " ")
        

def sumOverSubsets(A, n):
    P = [0]*(1 << n)
    table = [[0 for i in range(n)] for j in range(1 << n)]

    for x in range (1 << n):
        for i in range (n):
            if (x & ( 1 << i)):
                if (i == 0):
                    table[x][i] = A[x] + A[x^1]
                else:
                    table[x][i] = table[x][i-1] + table[x^(1 << i)][i-1]
            else:
                if (i == 0):
                    table[x][i] = A[x]
                else:
                    table[x][i] = table[x][i-1]
        P[x] = table[x][n-1]%2

    for i in range (1 << n):
        print(P[i], end = " ")
        

def another(a, n):
    f = [0]*(4)
    for i in range(1<<n):
        f[i] = a[i];
    for i in range(n):
      for mask in range(1<<n):
        if (mask & (1 << i)):
          f[i] += f[mask ^ (1 << i)];
          f[i] = f[i]%2
    return f

def another2(a, n):
    f = [0]*(4)
    for i in range(1<<n):
        f[i] = a[i];
    for i in range(n):
      for mask in range(1<<n):
        if (mask & (1 << i)):
          f[i] -= f[mask ^ (1 << i)];
          f[i] = f[i]%2
    return f


def reverse(A, n):
    P = [0]*(1 << n)
    table = [[0 for i in range(n)] for j in range(1 << n)]

    for x in range (1 << n):
        for i in range (n):
            if (x & ( 1 << i)):
                if (i == 0):
                    table[x][i] = A[x] + A[x^1]
                else:
                    table[x][i] = table[x][i-1] + table[x^(1 << i)][i-1]
            else:
                if (i == 0):
                    table[x][i] = A[x]
                else:
                    table[x][i] = table[x][i-1]
        P[x] = table[x][n-1]%2

    for i in range (1 << n):
        print(P[i], end = " ")


# Driver Code
if __name__ == '__main__':
	a = [5, 7, 1, 9] 
	a = [1, 1, 0, 1]
	a = [1, 0, 1, 1]
	# a = [1, 2, 1, 3]
	
##	a = [7, 11, 13, 16]
##	a = [7, 18, 20, 47]
	n = 2
	sumOverSubsets(a, n)
