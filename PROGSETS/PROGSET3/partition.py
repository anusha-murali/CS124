import random
import time
import sys
import numpy as np
import math


MAX_ITERATIONS = 25000


################################################################################
##                                                                            ##
##                            Utility Functions                               ##
##                                                                            ##
################################################################################


# Read an input file
def readInput(fileName):
    with open(fileName) as inFile:
        inputSet = inFile.readlines()
    inFile.close()
    inputSet = [num.strip('\n') for num in inputSet]
    inputSet = [int(num) for num in inputSet]
    return inputSet


# Generate a random sequence of -1's and +1'ss
def standardRep(n):
    sequence = []
    for i in range(n):
        sequence.append(random.choice([-1, 1]))
    return sequence


def randomResidue(numList, sequence):
    residue = 0

    for i in range(len(numList)):
        residue = residue + (numList[i]*sequence[i])

    if (residue < 0):
        return (-residue)
    
    return residue


# Generate a random parition of size n
def randPartition(n): 
    partition = [random.randint(0,n-1) for i in range(0,n)]
    return partition

# Generate a pre-partition as specified in the progset
def prePartition(numList, sequence):
    
    # Work off a copy of the input sequence
    P = list(sequence)
    A = []

    # Initialize the set A
    for i in range(0,len(numList)):
        A.append(0)

    # Generate the partition by adding to prePartion sequence
    for j in range(0,len(numList)):
        A[P[j]] = A[P[j]] + numList[j]

    return A
    

# Find a neighbor to a given solution
def randomNeighbor(numList):    
    # Return two random indices on the input set
    indexList = random.sample(range(0,len(numList)), 2)

    # We negate the first value
    numList[indexList[0]] = -numList[indexList[0]]

    # We negate the second value with probability 1/2
    if (random.random() < 0.5):
        numList[indexList[1]] = -numList[indexList[1]]

    return numList


# Cooling schedule for the Simulated Annealing heuristics
def T(i):
    return (pow(10, 10)) * (pow(0.8, math.floor(i/300)))


# This function is used to generate the statistics of the experimental results
# in a LaTeX tabular format
#
def generateResults1():

    algo_codes = [0, 1, 2, 3, 11, 12, 13]
    x_label = 0
    with open("results.tex", "w") as resultFile:
        resultFile.write("\\begin{tabular}{|c|c|c|c|c|c|}\hline \n")
        resultFile.write("Algorithm Code & Mean Residue & Mean Runtime & Min & Max & Std. Dev\\\\ \hline \n ")
        
        for algo in algo_codes:
            print("Currently working on algo ", algo)
            A = []
            AR = []
            for i in range(50):
                fileName = "INPUTS/t"+str(i)+".txt"
                startTime = time.time()
                
                if (algo == 0):
                    A.append(kk(readInput(fileName)))
                    x_label = 1
                elif (algo == 1):
                    A.append(repeatedRandom(readInput(fileName)))
                    x_label = 2
                elif (algo == 2):
                    A.append(hillClimbing(readInput(fileName)))
                    x_label = 3
                elif (algo == 3):
                    A.append(simulatedAnnealing(readInput(fileName)))
                    x_label = 4
                elif (algo == 11):
                    A.append(prePartRepeatedRandom(readInput(fileName)))
                    x_label = 5
                elif (algo == 12):
                    A.append(prePartHillClimbing(readInput(fileName)))
                    x_label = 6
                elif (algo == 13):
                    A.append(prePartSimulatedAnnealing(readInput(fileName)))
                    x_label = 7
                AR.append(time.time() - startTime)
            resultFile.write("%3i & %6.2f & %6.5f & %6i & %6i & %6.2f \\\\ \hline \n" % (algo,  statistics.mean(A), \
                                    statistics.mean(AR),  min(A), max(A), statistics.stdev(A)))

            # The following writes out the data from A into output files, which will be used by tikzpicture
            with open("../REPORT/"+str(algo) + "residue.txt", "w") as f1:
                f1.write("x y\n")
                for i in range(len(A)):
                    f1.write(str(x_label)+ " " + str(A[i])+"\n")
            f1.close()

            # The following writes out the data from AR into output files, which will be used by tikzpicture
            with open("../REPORT/"+str(algo) + "timing.txt", "w") as f1:
                f1.write("x y\n")
                for i in range(len(AR)):
                    f1.write(str(x_label)+ " " + str(AR[i])+"\n")
            f1.close()
  
        resultFile.write("\end{tabular}\n")
    resultFile.close()
        

# This function is used to generate the xperimental results
# in a LaTeX tabular format
#
def generateResults2():

    x_label = 0

    A0 = []
    A1 = []
    A2 = []
    A3 = []
    A11 = []
    A12 = []
    A13 = []

    with open("results2.tex", "w") as resultFile:
        resultFile.write("\\begin{tabular}{|c|c|c|c|c|c|c|c|}\hline \n")
        resultFile.write("Run & Algo 0 & Algo 1 & Algo 2 & Algo 3 & Algo 11 & Algo 12 & Algo 13\\\\ \hline \n ")

        for i in range(50):
            fileName = "INPUTS/t"+str(i)+".txt"
            print("Currently working on iteration ", i)
            A0.append(kk(readInput(fileName)))
            A1.append(repeatedRandom(readInput(fileName)))
            A2.append(hillClimbing(readInput(fileName)))
            A3.append(simulatedAnnealing(readInput(fileName)))
            A11.append(prePartRepeatedRandom(readInput(fileName)))
            A12.append(prePartHillClimbing(readInput(fileName)))
            A13.append(prePartSimulatedAnnealing(readInput(fileName)))
            resultFile.write("%2i & %3i & %6i & %6i & %6i & %6i & %6i & %6i \\\\ \hline \n" % \
                             (i+1, A0[i], A1[i], A2[i], A3[i], A11[i], A12[i], A13[i]))
        resultFile.write("%3i & %6i & %6i & %6i & %6i & %6i & %6i \\\\ \hline \n" % \
                             (statistics.mean(A0), statistics.mean(A1), statistics.mean(A2), \
                              statistics.mean(A3), statistics.mean(A11), statistics.mean(A12), \
                              statistics.mean(A13)))
        resultFile.write("\end{tabular}\n")
    resultFile.close()




################################################################################
##                                                                            ##
##                              Karmarkar-Karp                                ##
##                                                                            ##
################################################################################

def kk(numList):
    tempList = list(numList)

    while (len(tempList) > 1):
        n1 = max(tempList)
        index1 = tempList.index(n1)
        tempList[index1] = 0

        n2 = max(tempList)
        tempList[index1] = n1 - n2
        tempList.remove(n2)

    return tempList[0]



################################################################################
##                                                                            ##
##               Heuristics using Standard Representation                     ##
##                                                                            ##
################################################################################


def repeatedRandom(numList):
    # Generate a random sequence of -1's and 1's
    prevSequence = standardRep(len(numList))
    # Create a random set on the above random sequence
    bestResidue = randomResidue(numList, prevSequence)

    for i in range(1, MAX_ITERATIONS):
        # Generate a random sequence of -1's and 1's
        randSequence = standardRep(len(numList))
        newResidue = randomResidue(numList, randSequence)

        # If the newResidue is smaller, then update prevResidue
        if newResidue < bestResidue:
            bestResidue = newResidue

    return bestResidue


def hillClimbing(numList):
    # Generate a random sequence of -1's and 1's
    prevSequence = standardRep(len(numList))
    # Create a random set on the above random sequence
    bestResidue = randomResidue(numList, prevSequence)

    for i in range(1, MAX_ITERATIONS):
        # Generate a random neighbor
        randSequence = randomNeighbor(prevSequence)
        newResidue = randomResidue(numList, randSequence)

        # If the newResidue is smaller, then update prevResidue
        if newResidue < bestResidue:
            bestResidue = newResidue

    return bestResidue


def simulatedAnnealing(numList):
    # Generate a random sequence of -1's and 1's
    prevSequence = standardRep(len(numList))
    # Create a random set on the above random sequence
    bestResidue = randomResidue(numList, prevSequence)

    # randResidue = bestResidue

    for i in range(1, MAX_ITERATIONS):
        # Generate a random neighbor
        neighborSequence = randomNeighbor(prevSequence)
        newResidue = randomResidue(numList, neighborSequence)

        # If the newResidue is smaller, then update prevResidue
        if newResidue < bestResidue:
            prevSequence = neighborSequence
        elif (random.random() < math.exp(-(newResidue - bestResidue)/T(i))):
            prevSequence = neighborSequence

        newResidue = randomResidue(numList, prevSequence)
        
        if (newResidue < bestResidue):
            bestResidue = newResidue

    return bestResidue



################################################################################
##                                                                            ##
##              Heuristics using Pre-Partitioned Representation               ##
##                                                                            ##
################################################################################


def prePartRepeatedRandom(numList):
    # Generate a random partition
    prevSequence = randPartition(len(numList))
    # Create a prepartition and run KK on it
    bestResidue = kk(prePartition(numList, prevSequence))
    
    for i in range(1, MAX_ITERATIONS):
        # Generate a random partition
        randSequence = randPartition(len(numList))
        newResidue = kk(prePartition(numList, randSequence))

        # If the newResidue is smaller, then update prevResidue
        if newResidue < bestResidue:
            bestResidue = newResidue

    return bestResidue


def prePartHillClimbing(numList):
    # Generate a random partition
    prevSequence = randPartition(len(numList))
    # Create a prepartition and run KK on it
    bestResidue = kk(prePartition(numList, prevSequence))
    
    for i in range(1, MAX_ITERATIONS):
        # Generate a random partition
        randSequence = randomNeighbor(prevSequence)
        newResidue = kk(prePartition(numList, randSequence))

        # If the newResidue is smaller, then update prevResidue
        if newResidue < bestResidue:
            bestResidue = newResidue

    return bestResidue


def prePartSimulatedAnnealing(numList):
    # Generate a random sequence of -1's and 1's
    prevSequence = randPartition(len(numList))
    # Create a random set on the above random sequence
    bestResidue = kk(prePartition(numList, prevSequence))

    # randResidue = bestResidue

    for i in range(1, MAX_ITERATIONS):
        # Generate a random neighbor
        neighborSequence = randomNeighbor(prevSequence)
        newResidue = randomResidue(numList, neighborSequence)

        # If the newResidue is smaller, then update prevResidue
        if newResidue < bestResidue:
            prevSequence = neighborSequence
        elif (random.random() < math.exp(-(newResidue - bestResidue)/T(i))):
            prevSequence = neighborSequence

        newResidue = kk(prePartition(numList, prevSequence))
        
        if (newResidue < bestResidue):
            bestResidue = newResidue

    return bestResidue


################################################################################
##                                                                            ##
##                             Main Driver                                    ##
##                                                                            ##
################################################################################
#

# Obtain the input arguments
if len(sys.argv) > 1:
    flag = int(sys.argv[1])
    algo = int(sys.argv[2])
    fileName = sys.argv[3]
else:
    flag = 0
    algo = 0
    fileName = "INPUTS/t1.txt"


if (algo == 0):
    print(kk(readInput(fileName)))
elif (algo == 1):
    print(repeatedRandom(readInput(fileName)))
elif (algo == 2):
    print(hillClimbing(readInput(fileName)))
elif (algo == 3):
    print(simulatedAnnealing(readInput(fileName)))
elif (algo == 11):
    print(prePartRepeatedRandom(readInput(fileName)))
elif (algo == 12):
    print(prePartHillClimbing(readInput(fileName)))
elif (algo == 13):
    print(prePartSimulatedAnnealing(readInput(fileName)))



