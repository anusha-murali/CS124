# Python3 program for Bellman-Ford's single source
# shortest path algorithm.

# Class to represent a graph
import numpy as np

class Graph:

	def __init__(self, vertices):
		self.V = vertices # No. of vertices
		self.graph = []

	# function to add an edge to graph
	def addEdge(self, u, v, w):
		self.graph.append([u, v, w])

	# utility function used to print the solution
	def printArr(self, dist):
		print("Vertex Distance from Source")
		for i in range(self.V):
			print("{0}\t\t{1}".format(i, dist[i]))

	# The main function that finds shortest distances from src to
	# all other vertices using Bellman-Ford algorithm. The function
	# also detects negative weight cycle
	def BellmanFord(self, src):

		# Step 1: Initialize distances from src to all other vertices
		# as INFINITE
		dist = [float("Inf")] * self.V
		dist[src] = 0

		# Step 2: Relax all edges |V| - 1 times. A simple shortest
		# path from src to any other vertex can have at-most |V| - 1
		# edges
		for _ in range(self.V - 1):
			# Update dist value and parent index of the adjacent vertices of
			# the picked vertex. Consider only those vertices which are still in
			# queue
			for u, v, w in self.graph:
				if dist[u] != float("Inf") and dist[u] + w < dist[v]:
					dist[v] = dist[u] + w

		# Step 3: check for negative-weight cycles. The above step
		# guarantees shortest distances if graph doesn't contain
		# negative weight cycle. If we get a shorter path, then there
		# is a cycle.

		for u, v, w in self.graph:
			if dist[u] != float("Inf") and dist[u] + w < dist[v]:
				print("Graph contains negative weight cycle")
				return

		# print all distance
		self.printArr(dist)


# Driver's code
if __name__ == '__main__':

##	g = Graph(4)
##
##	g.addEdge(0, 1, -10)
##	g.addEdge(0, 3, -10)
##	g.addEdge(1, 2, -20)
##	g.addEdge(2, 3, -30)

        g = Graph(6)
        g.addEdge(0, 1, -5)
        g.addEdge(2, 1, -2)
        g.addEdge(1, 3, -4)
        g.addEdge(1, 4, -5)
        g.addEdge(3, 4, -10)
        g.addEdge(3, 5, 1)
        
        g.BellmanFord(0)

