
def printParagraph(words, M):
    n = len(words)
    xSpace = [[0 for i in range(n)] for j in range(n)] # No of extra spaces at the end of each line
    lCost = [[0 for i in range(n)] for j in range(n)]  # Cost of line containing words from i to j 
    cost = [float('inf')]*(n+1) # Cost of an optimal arrangements of words 1,...,i
    pList = [0]*n

    # Base case
    cost[0] = 0

    # Compute the extra spaces for all the words from 0 to n-1
    # xSpace[i, j] denotes the extra space on a line containing words i through j
    for i in range(n):
        xSpace[i][i] = M - len(words[i])
        for j in range(i+1, n):
            xSpace[i][j] = xSpace[i][j-1] - len(words[j]) - 1

    # Compute the line costs
    for i in range(n):
        for j in range(n):
            if xSpace[i][j] < 0:
                #print("extraspace = ", xSpace[i][j])
                lCost[i][j] = (2**(-xSpace[i][j]) - (xSpace[i][j])**3 - 1) #float('inf')
               # print("linecost = ", lCost[i][j])
            elif (j == n-1 and xSpace[i][j] >= 0):
                lCost[i][j] = 0
            else:
                lCost[i][j] = (xSpace[i][j])**3

    #print("lcost[0][0] = ", lCost[0][0])
    
    # Compute the costs for each line
    for j in range(n):
        for i in range(0, j+1):
            thisCost = cost[i] + lCost[i][j]
            #print("cost[", i, "] = ", cost[i], "lCost[",i,"][",j,"]", lCost[i][j], "thisCost = ", thisCost)
            if (cost[j+1] > thisCost):
                cost[j+1] = thisCost
                pList[j] = i
##
##    print(xSpace)
##    print(lCost)
##    print(cost)

    return cost, pList


def printNeatly(words, j, pList):
    i = pList[j]
    lineNo = 0
    if (i != 0):
        lineNo = printNeatly(words, i-1, pList) + 1
    print(' '.join(words[i:(j+1)]))
    return lineNo
    

input_text = "Determine the minimal penalty, and corresponding optimal division of words into lines, for the text of this question, from the first `Determine' through the last `correctly.)', for the cases where M is 40 and M is 72. Words are divided only by spaces (and, in the pdf version, linebreaks) and each character that isn't a space (or a linebreak) counts as part of the length of a word, so the last word of the question has length eleven, which counts the period and the right parenthesis. (You can find the answer by whatever method you like, but we recommend coding your algorithm from the previous part. You don't need to submit code.) (The text of the problem may be easier to copy-paste from the tex source than from the pdf. If you copy-paste from the pdf, check that all the characters show up correctly.)"

input_text = "Determine the minimal penalty, and corresponding optimal division of words into lines, for the text of this question, from the first `Determine' through the last `correctly.)', for the cases where M is 40 and M is 72. Words are divided only by spaces (and, in the pdf version, linebreaks) and each character that isn't a space (or a linebreak) counts as part of the length of a word, so the last word of the question has length eleven, which counts the period and the right parenthesis. (You can find the answer by whatever method you like, but we recommend coding your algorithm from the previous part. You don't need to submit code.) (The text of the problem may be easier to copy-paste from the tex source than from the pdf. If you copy-paste from the pdf, check that all the characters show up correctly.)"

#input_text = "Anusha baby is very smart and beautiful."

#input_text = ""

words = input_text.split()

cost, pList = printParagraph(words, 40)

printNeatly(words, len(words)-1, pList)

print(cost[-1])
