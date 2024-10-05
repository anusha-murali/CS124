# Python3 program to find all subsets of
# given set. Any repeated subset is
# considered only once in the output


def printPowerSet(arr, n):

	# Function to find all subsets of given set.
	# Any repeated subset is considered only
	# once in the output
	_list = []

	# Run counter i from 000..0 to 111..1
	for i in range(2**n):
		subset = ""

		# consider each element in the set
		for j in range(n):

			# Check if jth bit in the i is set.
			# If the bit is set, we consider
			# jth element from set
			if (i & (1 << j)) != 0:
				subset += str(arr[j]) + "|"

		# if subset is encountered for the first time
		# If we use set<string>, we can directly insert
		if subset not in _list and len(subset) > 0:
			_list.append(subset)

	# consider every subset
	for subset in _list:

		# split the subset and print its elements
		arr = subset.split('|')
		for string in arr:
			print(string, end=" ")
		print()

def polarTransform(n):

    subSet = []
    pArray = []
    
##    for i in range(2**n):
##        subSet.append(i)

    subSet.append(1)
    subSet.append(1)
    subSet.append(0)
    subSet.append(1)

    pArray.append(subSet[0])
    
    for i in range(2**n):
        for j in range(n):
            if (i & (1 << j) != 0):
                w = subSet[i]
                if (i == 2):
                    print("w = ", w, "pArray = ", pArray)
                for k in pArray:
                    w = w + k
                pArray.append(w%2)
            
    return pArray
        


# Driver Code
if __name__ == '__main__':
	x = [1, 1, 0, 1]
	n = len(x)
	printPowerSet(x, n)

# This code is contributed by vibhu4agarwal
