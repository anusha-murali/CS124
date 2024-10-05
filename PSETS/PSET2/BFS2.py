# Python3 Program to print BFS traversal
# from a given source vertex. BFS(int s)
# traverses vertices reachable from s.

from collections import defaultdict

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.visited = []

    def BFS(self, s):
        queue = []

        queue.append(s)
        self.visited.append(s)

        
        while queue:
            s = queue.pop(0)
            #print(s, end=" ")

            for i in self.graph[s]:
                print("(",s,",",i,")")
                if i not in self.visited:
                    queue.append(i)
                    self.visited.append(s)
            #print(self.visited)

g = Graph()

g.addEdge(0, 1)
g.addEdge(0, 2)
g.addEdge(1, 0)
g.addEdge(2, 0)
##g.addEdge(1, 2)
##g.addEdge(2, 0)
##g.addEdge(2, 3)
##g.addEdge(3, 3)

g.BFS(0)
