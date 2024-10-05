// CS124 Spring 2024 PROGSET1
// Implementation of Prim's algorithm using Min Heap 
// February 14, 2024
//
#include <math.h>
#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <unistd.h>


// Each element in our Min Heap consists of two pieces of information, source vertex no and
// the edge weight
struct MinHeapElement {
  int v;
  float edgeWeight;
};

// We implement the priority queue using a Min Heap, which can be dynamically allocated as needed.
// The PQ consists of MinHeapElements, which have NOT yet been added to the MST being built
//
struct MinHeap {
  struct MinHeapElement **pq;  // Elements as a PQ 
  int capacity; // Maximum capacity of the Min Heap (= |V|)
  int size;     // Current size of the Min Heap
  int *index;   // Index of a given vertex
};

// This function creates a new Min Heap element
//
struct MinHeapElement* createMinHeapElement(int v, float edgeWeight)
{
  struct MinHeapElement* minHeapElement;

  minHeapElement = (struct MinHeapElement*)malloc(sizeof(struct MinHeapElement));
  minHeapElement->v = v;
  minHeapElement->edgeWeight = edgeWeight;

  return minHeapElement;
}

// This function creates the Min Heap by allcating enough space for building
// a priority queue of at most |V| elements.
// 
struct MinHeap* initMinHeap(int noOfVertices)
{
  struct MinHeap* minHeap;

  minHeap = (struct MinHeap*)malloc(sizeof(struct MinHeap));
  minHeap->index = (int *)malloc(noOfVertices*sizeof(int));
  minHeap->size = noOfVertices;
  minHeap->capacity = noOfVertices;
  minHeap->pq = (struct MinHeapElement**)malloc(noOfVertices*sizeof(struct MinHeapElement*));

  return minHeap;
}

// Return the index of the parent of node at index i
int parentNode(int i) 
{
  return (i - 1)/2;
}

// Return the left child of node at index i
int leftChild(int i) 
{
  return (2*i + 1);
}

// Return the right child of node at index i
int rightChild(int i) 
{
  return (2*i + 2);
}

// This function re-organizes the heap to maintain the Min Heap property at
// the given index.
// 
void minHeapify(struct MinHeap *minHeap, int index)
{
  int left = leftChild(index);
  int right = rightChild(index);
  int smallest = index;

  // If the left child is smaller than the element at index, then 
  // it is the smallest
  if (left < minHeap->size && 
      minHeap->pq[left]->edgeWeight < minHeap->pq[smallest]->edgeWeight)
    smallest = left;

  // If the right child is smaller than the element at index, then
  // it is the smallest
  if (right < minHeap->size && 
      minHeap->pq[right]->edgeWeight < minHeap->pq[smallest]->edgeWeight)
    smallest = right;

  // If the current element is not the smallest, then we swap it with the smallest.
  // This will preserve the Min Heap property of the heap. We have to recursively
  // minHeapify until we reach the root node, so that all the subtrees along the
  // path will be minHeapified.
  //
  if (smallest != index) 
  {
    struct MinHeapElement *smallestNode;
    struct MinHeapElement *temp;

    smallestNode = minHeap->pq[smallest];
    struct MinHeapElement* indexNode = minHeap->pq[index];

    // Swap indexes
    minHeap->index[smallestNode->v] = index;
    minHeap->index[indexNode->v] = smallest;

    // Swap nodes
    temp = minHeap->pq[smallest];
    minHeap->pq[smallest] = minHeap->pq[index];
    minHeap->pq[index] = temp;

    // Recursively minHeapify
    minHeapify(minHeap, smallest);
  }
}


// This function extracts the element with the smallest weight. Once
// extracted, the remaining heap will be min-heapified.
//
struct MinHeapElement* extractMin(struct MinHeap* minHeap)
{
  struct MinHeapElement *heapRoot;
  struct MinHeapElement *lastElement;

  if (!minHeap || minHeap->size == 0)
    return NULL;

  // Remember the root of the Min Heap
  heapRoot = minHeap->pq[0];

  lastElement =  minHeap->pq[minHeap->size - 1];
  
  // Update the root value with the last element
  minHeap->pq[0] = lastElement;

  // Update indexes of the last element
  minHeap->index[heapRoot->v] = minHeap->size - 1;
  minHeap->index[lastElement->v] = 0;

  // Now, remove the last element by decreasing the heap size
  minHeap->size = minHeap->size - 1;

  // Call minHeapify to maintain the Min Heap property
  minHeapify(minHeap, 0);

  return heapRoot;
}

// This function decreases edgeWeight of a given vertex v. 
//
void decreaseKey(struct MinHeap* minHeap, int v, float edgeWeight)
{
  struct MinHeapElement *temp;

  // Get the index of v in Min Heap PQ
  int i = minHeap->index[v];

  // Update the node's edgeWeight
  minHeap->pq[i]->edgeWeight = edgeWeight;

  // Swap with the parent, if the node's edge weight is smaller than
  // that of the parent. Do this until reaching the root
  while ((i > 0) && minHeap->pq[i]->edgeWeight < minHeap->pq[(i-1)/2]->edgeWeight) 
  {
    // This node's weight is smaller than the parent's weight.
    // So, swap this node with its immediate parent
    minHeap->index[minHeap->pq[i]->v] = (i-1)/2;
    minHeap->index[minHeap->pq[(i-1)/2]->v] = i;

    temp = minHeap->pq[i];
    minHeap->pq[i] = minHeap->pq[(i-1)/2];
    minHeap->pq[(i-1)/2] = temp;

    // Traverse up the tree by updating the parent's index
    i = (i-1)/2;
  }
}

// This function returns true if the given vertex is 
// in the Min Heap and false otherwise. If the vertex is still
// in the Min Heap, then it is eligible to be included in the MST.
bool isInMinHeap(struct MinHeap* minHeap, int v)
{
  if (minHeap->index[v] < minHeap->size) 
    return true;

  return false;
}

// This is a debugging routine to print the Min Heap
//
void printMinHeap(struct MinHeap *minHeap)
{
  for (int i = 0; i < minHeap->size; i++)
    printf("%2.3f ", minHeap->pq[i]->edgeWeight);
  printf("\n");
}

// This function frees the Min Heap
//
void freeMinHeap(struct MinHeap *minHeap) {
    if (!minHeap)
        return;
    free(minHeap->pq);
    free(minHeap);
}   

// We represent our graph using an adjacency list, which
// is a linked list hanging off of a vertex. Each element in the 
// adjacency list contains two pieces of information: the destination
// vertex and the edge weight.
//
struct adjListElement 
{
  int destV;
  float weight;
  struct adjListElement* next;
};

// We represent our graph using an adjacency list, which is a 
// linked list hanging off of a vertex. The linked list consists of
// adjListElements defined above
//
struct adjacencyList 
{
  struct adjListElement *head; 
};

// This function allocates memory for a new adjacency list element
// and returns it
//
struct adjListElement* createAdjListElement(int destV, float weight)
{
  struct adjListElement *newElement;

  newElement = (struct adjListElement*)malloc( sizeof(struct adjListElement));
  newElement->destV = destV;
  newElement->weight = weight;
  newElement->next = NULL;
  return newElement;
}

// We represent our graph using adjacency lists. There is one adjacency
// list for each vertex, so there are V number of adjacency lists in G.
// V corresponds to the number of vertices in G.
//
struct Graph 
{       
  struct adjacencyList *adjListArray;
  int V;
};

// This function creates a fully connected and weighted graph with
// V vertices. It allocates memory for V adjacency lists, one for 
// each of the V vertices. This graph will be the input to the Prim's 
// MST algorithm defined above.
//
struct Graph *createConnectedGraph(int noOfVertices)
{
  struct Graph *G;

  G = (struct Graph*)malloc(sizeof(struct Graph));
  G->V = noOfVertices;  // Graph has V vertices

  // Allocate memory for V adjacency lists
  G->adjListArray = (struct adjacencyList*)malloc(noOfVertices*sizeof(struct adjacencyList));

  // Start with empty lists
  for (int i = 0; i < noOfVertices; ++i)
    G->adjListArray[i].head = NULL;

  return G;
}

// This function adds an edge to the undirected graph, G.
// Since G is undirected, we add two edges between any two
// vertices src and dest: one in the direction of src --> dest
// and another in the direction of dest --> src.
// 
void addEdge(struct Graph* G, int src, int dest, float weight)
{
  struct adjListElement *newElement;

  // Create a new element to be added to the Adjacency List
  // hanging off of the 'src' vertex.
  // Add this element to the front of the list and make this
  // element the head of the Adjacency List.
  // This adds an edge from 'src' to 'dest' vertices. 
  newElement = createAdjListElement(dest, weight);
  newElement->next = G->adjListArray[src].head;
  G->adjListArray[src].head = newElement;

  // Create a new element to be added to the Adjacency List
  // hanging off of the 'dest' vertex.
  // Add this element to the front of the list and make this
  // element the head of the Adjacency List.
  // This adds an edge from 'dest' to 'src' vertices.
  newElement = createAdjListElement(src, weight);
  newElement->next = G->adjListArray[dest].head;
  G->adjListArray[dest].head = newElement;
}

// This function prints the MST by tracing all the edges
// between the vertices stored in the parent PQ
void printMST(int parent[], int N, float edgeWeight[])
{
  for (int i = 1; i < N; ++i)
  printf("%d - %d: %2.3f\n", parent[i], i, edgeWeight[i]);
}

// This function computes the weight of the MST
float edgeWeightOfMST(float edgeWeight[], int V)
{
  float totalWeight = 0.0;

  for (int i = 1; i < V; i++)
    totalWeight = totalWeight + edgeWeight[i];

  return (totalWeight);
    
}

// This function creates an MST using the Prim's algorithm for the input
// graph, G and returns its weight. At a high level, we do the 
// following tasks:
// (1) Initialize the edge weights to all vertices as INFINITY.
// (2) Insert the source vertex (weight = 0) in to the Priority Queue (PQ)
// (3) Using the cut property, find the smallest from the PQ and add it to 
//     MST, if it's not alread there and update its parent.
// (4) Min-heapify the remaining elements in PQ. Continue until there is
//     no more elements in PQ.
// (5) Compute the average weight of the MST found and return it.
//
float weightOfMST(struct Graph* G, int flag)
{
  int N = G->V;         // The number of vertices in graph
  float edgeWeight[N]; // Edge weights used to build the Min Heap
  int parent[N];        // Except for the root, we maintain the parent for every vertex
  float total_weight = 0.0;
  struct MinHeap *minHeap;

  // First allocate a Min Heap with sufficient space to maintain the edges
  minHeap = initMinHeap(N);

  // Now initialize the Min Heap such that all the edge weights are INFINITE
  // except for the source vertex, which willl be intialized to 0. Also we initialize
  // the parent of the vertices as -1. 
  for (int i = 1; i < N; i++) 
  {
    edgeWeight[i] = INFINITY;
    parent[i] = -1;
    minHeap->pq[i] = createMinHeapElement(i, edgeWeight[i]);
    minHeap->index[i] = i;
  }

  edgeWeight[0] = 0.0;   // This will be at the front of the PQ
  minHeap->pq[0] = createMinHeapElement(0, edgeWeight[0]);
  minHeap->index[0] = 0;

  // Until the Priority Queue (Min Heap) becomes empty, we extract the
  // minimum using the cut property and add the edge to the growing MST
  while (minHeap->size > 0) 
  {
    struct MinHeapElement *minHeapElement;  // An element on the PQ
    struct adjListElement *adjElement;      // An element on the Adjacency List

    // Get the vertex at the root of the Min Heap. This has the minimum
    // edge weight
    minHeapElement = extractMin(minHeap);

    // Get the vertex no of the above minimum element
    int curV = minHeapElement->v; 

    // Get the first element in the adjacency list of the current vertex, curV.
    adjElement = G->adjListArray[curV].head;

    // Now go through all the adjacent vertices of curV and update their
    // edge weights accordingly
    while (adjElement != NULL) 
    {
      int adjV = adjElement->destV;  // Get an adjacent vertex of curV

      // if adjV is not yet part of the growing MST and if its true edge weight is
      // smaller than the current weight in the edgeWeight PQ, then update this
      // adjV with the actual edge weight, as well as the parent PQ.
      // Since this edge is now included in the growing MST, we add it to total_weight.
      if (isInMinHeap(minHeap, adjV) && adjElement->weight < edgeWeight[adjV]) 
      {
        edgeWeight[adjV] = adjElement->weight;
	parent[adjV] = curV;
	decreaseKey(minHeap, adjV, edgeWeight[adjV]);
        total_weight = total_weight + edgeWeight[adjV];
      }
      // Get the next element in the adjacency list
      adjElement = adjElement->next;
    }
  }

  if (flag == 5)  // For debugging - verbose output
  {
    // The following piece of code identifies a candidate k(n)
    // for edge pruning
    float max_weight = 0.0;
    for (int i = 0; i < N; i++)
      if (edgeWeight[i] > max_weight)
         max_weight = edgeWeight[i];
    printf("Max weight for n = %d is %3.3f\n", N, max_weight);
 
    printf("%s", "MST: \n");
    printMST(parent, N, edgeWeight);
  }

  // Free all the memory allocated for Min Heap
  freeMinHeap(minHeap);

  return edgeWeightOfMST(edgeWeight, N);
}


// Find expected weights of MSTs where weight of each edge is
// a real number chosen uniformly at random on [0, 1].
// Input - n: Number of vertices, numTrials
// Output - Expected weight of the MST on n vertices
//
float expectedWeightZeroD(int n, int numTrials, int flag)
{
  struct Graph *graph;
  float total_weight = 0.0;

  for (int k = 0; k < numTrials; k++)
  {
    // if (n < 1024)
    //  sleep(1);

    // Allocate a graph with |V| = n
    graph = createConnectedGraph(n);

    for (int i = 0; i < n; i++)
      for (int j = i+1; j < n; j++)
      {
        // Add edges between the n vertices with random real weights in the
        // range of [0, 1]
        float weight = ((float)rand()) / RAND_MAX; //drand48();
        // 
        // For n < 1024, we can blindly add all (n choose 2) edges, as the runtime
        // on my MacBook is < 0.01 sec. However, when n > 1024, I only add edges that
        // exceed a weight of 256/n, as the expected weight is order of magnitude
        // smaller than 256/n. Therefore, any weight > 256/n seems to have 
        // negligible effect on the expected edge of the MST, as Prim's algorithm
        // doesn't even look at these edges, which are burried deep under the
        // Min Heap.
        //
        if (n < 1024)
          addEdge(graph, i, j, weight);
        else
        {
          if (weight < ((float)256)/((float)n))
            addEdge(graph, i, j, weight);
        }
      }
    
    // Run Prim's algorithm on the above graph and compute the weight of the MST
    total_weight = total_weight + weightOfMST(graph, flag);
  }
  return (total_weight/numTrials);
}

// This function computes the Euclidean distance between
// two points (x1, y1) and (x2, y2)
float distanceTwoD(float x1, float y1, float x2, float y2)
{
  return sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2));
}


// Find expected weights of MSTs where the vertices are found
// within a unit square. The edge weight is the Euclidean distance
// between the vertices.
// Input - n: Number of vertices, numTrials
// Output - Expected weight of the MST on n vertices
//
float expectedWeightTwoD(int n, int numTrials, int flag)
{
  struct Graph *graph;
  float total_weight = 0.0;
  float x[n], y[n];

  for (int k = 0; k < numTrials; k++)
  {
    // if (n < 1024)
    //  sleep(1);

    // Allocate a graph with |V| = n
    graph = createConnectedGraph(n);

    // Randomly generate n points
    for (int i = 0; i < n; i++)
    {
       x[i] = ((float)rand()) / RAND_MAX;
       y[i] = ((float)rand()) / RAND_MAX;
    }

    for (int i = 0; i < n; i++)
      for (int j = i+1; j < n; j++)
      {
        // Add edges between the n vertices. Their edge weights are
        // Euclidean distance between the points (x_i, y_i) and (x_j, y_j)
        float weight = distanceTwoD(x[i], y[i], x[j], y[j]);

        // For n < 1024, we can blindly add all (n choose 2) edges, as the runtime
        // on my MacBook is < 0.01 sec. However, when n > 1024, I only add edges that
        // exceed a weight of 2048/n, as the expected weight is order of magnitude
        // smaller than 2048/n. Therefore, any weight > 2048/n seems to have
        // negligible effect on the expected edge of the MST, as Prim's algorithm
        // doesn't even look at these edges, which are burried deep under the
        // Min Heap.
        //
        if (n < 1024)
          addEdge(graph, i, j, weight);
        else
        {
          if (weight < ((float)2048)/((float)n))
            addEdge(graph, i, j, weight);
        }
      }
    
    // Run Prim's algorithm on the above graph and compute the weight of the MST
    total_weight = total_weight + weightOfMST(graph, flag);
  }

  return (total_weight/numTrials);
}

// This function computes the Euclidean distance between
// two points (x1, y1, z1) and (x2, y2, z2)
float distanceThreeD(float x1, float y1, float z1, float x2, float y2, float z2)
{
  return sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2) + (z1 - z2)*(z1 - z2));
} 

// Find expected weights of MSTs where the vertices are found
// within a unit cube. The edge weight is the Euclidean distance
// between two vertices.
// Input - n: Number of vertices, numTrials
// Output - Expected weight of the MST on n vertices
//
float expectedWeightThreeD(int n, int numTrials, int flag)
{
  struct Graph *graph;
  float total_weight = 0.0;
  float x[n], y[n], z[n];

  for (int k = 0; k < numTrials; k++)
  {
    //if (n < 1024)
    //  sleep(1);

    // Allocate a graph with |V| = n
    graph = createConnectedGraph(n);

    // Randomly generate n points
    for (int i = 0; i < n; i++)
    {
       x[i] = ((float)rand()) / RAND_MAX;
       y[i] = ((float)rand()) / RAND_MAX;
       z[i] = ((float)rand()) / RAND_MAX;
    }

    for (int i = 0; i < n; i++)
      for (int j = i+1; j < n; j++)
      {
        // Add edges between the n vertices. Their edge weights are
        // Euclidean distance between the points (x_i, y_i, z_i) and (x_j, y_j, z_j)
        float weight = distanceThreeD(x[i], y[i], z[i], x[j], y[j], z[j]);

        // For n < 1024, we can blindly add all (n choose 2) edges, as the runtime
        // on my MacBook is < 0.01 sec. However, when n > 1024, I only add edges that
        // exceed a weight of 8192/n, as the expected weight is order of magnitude
        // smaller than 8192/n. Therefore, any weight > 8192/n seems to have
        // negligible effect on the expected edge of the MST, as Prim's algorithm
        // doesn't even look at these edges, which are burried deep under the
        // Min Heap.
        //
        if (n < 1024)
          addEdge(graph, i, j, weight);
        else
        {
          if (weight < ((float)8192)/((float)n))
            addEdge(graph, i, j, weight);
        }
      }

    // Run Prim's algorithm on the above graph and compute the MST's weight
    total_weight = total_weight + weightOfMST(graph, flag);
  }

  return (total_weight/numTrials);
}

// This function computes the Euclidean distance between
// two points (w1, x1, y1, z1) and (w2, x2, y2, z2)
float distanceFourD(float w1, float x1, float y1, float z1, 
                      float w2, float x2, float y2, float z2)
{ 
  return sqrt((w1 - w2)*(w1 - w2) + (x1 - x2)*(x1 - x2) 
              + (y1 - y2)*(y1 - y2) + (z1 - z2)*(z1 - z2));
}  

// Find expected weights of MSTs where the vertices are found
// within a hypercube. The edge weight is the Euclidean distance
// between two vertices.
// Input - n: Number of vertices, numTrials
// Output - Expected weight of the MST on n vertices
//
float expectedWeightFourD(int n, long numTrials, int flag)
{   
  struct Graph *graph;
  float total_weight = 0.0;
  float w[n], x[n], y[n], z[n];

  for (long k = 0; k < numTrials; k++)
  { 
    // if (n < 1024)
    //  sleep(1);

    // Allocate a graph with |V| = n
    graph = createConnectedGraph(n);
    
    // Randomly generate n points
    for (int i = 0; i < n; i++)
    {
       w[i] = ((float)rand()) / RAND_MAX;
       x[i] = ((float)rand()) / RAND_MAX;
       y[i] = ((float)rand()) / RAND_MAX;
       z[i] = ((float)rand()) / RAND_MAX;
    }   
    
    for (int i = 0; i < n; i++)
      for (int j = i+1; j < n; j++)
      {       
        // Add edges between the n vertices. Their edge weights are
        // Euclidean distance between the points (w_i, x_i, y_i, z_i) and (w_j, x_j, y_j, z_j)
        float weight = distanceFourD(w[i], x[i], y[i], z[i], w[j], x[j], y[j], z[j]);

        // We find that edge weights above certain values of k(n) are not being used
        // in building the MST. Therefore, we can avoid adding those edges to the graph.
        // This reduces the size of the memory usage and also improves the performance              
        if (n < 1024)
          addEdge(graph, i, j, weight);
        else if (n < 131072)
        {
          if (weight < ((float)8192)/((float)n))
            addEdge(graph, i, j, weight);
        }
        else
        {
          if (weight < ((float)32768)/((float)n))
            addEdge(graph, i, j, weight);
        }
      }

    // Run Prim's algorithm on the above graph and compute the weight of the MST
    total_weight = total_weight + weightOfMST(graph, flag);
  }     
              
  return (total_weight/numTrials);
}             
              
// The following functon runs the experiment for dimension = 0 
// for all n from 2^7 to 2^18, and computes the average MST weight
// over numTrials.
// Use flag = 5 to invoke this function.
//
void experimentZeroD(int numTrials)
{
  int numPoints = 64;
  int dimension = 0;
  int flag = 0;
  float weight = 0.0; 
  float time_taken;
  clock_t t;

  printf("Experiments 0 D\n");
  printf("---------------\n");

  for (int i = 0; i < 12; i++)
  {
    // Start with numpoints = 128
    numPoints = numPoints*2;
    
    t = clock();
    weight = expectedWeightZeroD(numPoints, numTrials, flag);
    t = clock() - t;
    time_taken = ((float)t)/CLOCKS_PER_SEC; // in seconds
    time_taken = time_taken/numTrials;

    printf("%2.10f %d %d %d t = %f\n", 
             weight,
             numPoints, 
             numTrials, 
             dimension,
             time_taken);
  }
}

// The following functon runs the experiment for dimension = 2
// for all n from 2^7 to 2^18, and computes the average MST weight
// over numTrials.
// Use flag = 5 to invoke this function.
//
void experimentTwoD(int numTrials)
{             
  int numPoints = 64;
  int dimension = 0;
  int flag = 0;
  float weight = 0.0;
  float time_taken;
  clock_t t;
  
  printf("Experiments 2 D\n");
  printf("---------------\n");
  
  for (int i = 0; i < 12; i++)
  {   
    // Start with numpoints = 128
    numPoints = numPoints*2;
  
    t = clock();
    weight = expectedWeightTwoD(numPoints, numTrials, flag);
    t = clock() - t;
    time_taken = ((float)t)/CLOCKS_PER_SEC; // in seconds
    time_taken = time_taken/numTrials;

    printf("%2.10f %d %d %d t = %f\n",
             weight,
             numPoints,
             numTrials,
             dimension,
             time_taken);            
  }           
}

// The following functon runs the experiment for dimension = 3
// for all n from 2^7 to 2^18, and computes the average MST weight
// over numTrials.
// Use flag = 5 to invoke this function.
//
void experimentThreeD(int numTrials)
{             
  int numPoints = 64;
  int dimension = 0;
  int flag = 0;
  float weight = 0.0;
  float time_taken;
  clock_t t;
    
  printf("Experiments 3 D\n");
  printf("---------------\n");
 
  for (int i = 0; i < 12; i++)
  {   
    // Start with numpoints = 128
    numPoints = numPoints*2;
  
    t = clock();
    weight = expectedWeightThreeD(numPoints, numTrials, flag);
    t = clock() - t;
    time_taken = ((float)t)/CLOCKS_PER_SEC; // in seconds
    time_taken = time_taken/numTrials;
             
    printf("%2.10f %d %d %d t = %f\n",
             weight,
             numPoints,
             numTrials,
             dimension,
             time_taken);            
  }           
}

// The following functon runs the experiment for dimension = 4
// for all n from 2^7 to 2^18, and computes the average MST weight
// over numTrials.
// Use flag = 5 to invoke this function.
//
void experimentFourD(int numTrials)
{             
  int numPoints = 64;
  int dimension = 0;
  int flag = 0;
  float weight = 0.0;
  float time_taken;
  clock_t t;
    
  printf("Experiments 4 D\n");
  printf("---------------\n");
 
  for (int i = 0; i < 12; i++)
  {   
    // Start with numpoints = 128
    numPoints = numPoints*2;
             
    t = clock();
    weight = expectedWeightFourD(numPoints, numTrials, flag);
    t = clock() - t;
    time_taken = ((float)t)/CLOCKS_PER_SEC; // in seconds
    time_taken = time_taken/numTrials;
             
    printf("%2.10f %d %d %d t = %f\n",
             weight,
             numPoints,
             numTrials,
             dimension,
             time_taken);
  }           
}


// Main program for PROGSET1
//
int main(int argc, char *argv[])
{
  if (argc != 5)
  {
    printf("Incorrect number of arguments passed.\n");
    printf("Usage: ./randmst flag numpoints numtrials dimension\n");
    return 1;
  }
  else
  {
    srand(time(0));

    clock_t t;
    int flag = atoi(argv[1]);
    int numPoints = atoi(argv[2]);
    int numTrials = atoi(argv[3]);
    int dimension = atoi(argv[4]); 

    t = clock();

    if (flag == 0)
    {
      if (dimension == 0)  // For autograder (outputs according to the PSET specs)
        printf("%2.10f %d %d %d\n", 
              expectedWeightZeroD(numPoints, numTrials, flag), 
              numPoints, 
              numTrials, 
              dimension); 
      else if (dimension == 2)
        printf("%2.10f %d %d %d\n",
              expectedWeightTwoD(numPoints, numTrials, flag),
              numPoints,
              numTrials,
              dimension);
      else if (dimension == 3)
        printf("%2.10f %d %d %d\n",
              expectedWeightThreeD(numPoints, numTrials, flag),
              numPoints,
              numTrials,
              dimension);
      else if (dimension == 4)
        printf("%2.10f %d %d %d\n",
              expectedWeightFourD(numPoints, numTrials, flag),
              numPoints,
              numTrials,
              dimension);
    }
    else if (flag == 5) // For my own debugging. Experiments can be run for individual dimension
    {
      if (dimension == 0)
        printf("%2.10f %d %d %d\n",
              expectedWeightZeroD(numPoints, numTrials, flag), 
              numPoints,
              numTrials, 
              dimension);
      else if (dimension == 2)
        printf("%2.10f %d %d %d\n",
              expectedWeightTwoD(numPoints, numTrials, flag),
              numPoints,
              numTrials, 
              dimension);
      else if (dimension == 3)
        printf("%2.10f %d %d %d\n",
              expectedWeightThreeD(numPoints, numTrials, flag),
              numPoints,
              numTrials,
              dimension);
      else if (dimension == 4)
        printf("%2.10f %d %d %d\n",
              expectedWeightFourD(numPoints, numTrials, flag),
              numPoints,
              numTrials,
              dimension);
      else
        printf("Not supported\n");

      t = clock() - t;
      float time_taken = ((float)t)/CLOCKS_PER_SEC; // in seconds
      printf("For n = %d, time taken = %f seconds\n", numPoints, time_taken);
    }
    else if (flag == 3) // My experiments: Experiments will be run for all dimensions
    { 
      float time_taken;
      t = clock();

      experimentZeroD(numTrials);
      t = clock() - t;
      time_taken = ((float)t)/CLOCKS_PER_SEC; // in seconds
      printf("Time taken = %f seconds\n", time_taken);

      experimentTwoD(numTrials); 
      t = clock() - t;
      time_taken = ((float)t)/CLOCKS_PER_SEC; // in seconds
      printf("Time taken = %f seconds\n", time_taken);
 
      experimentThreeD(numTrials); 
      t = clock() - t;
      time_taken = ((float)t)/CLOCKS_PER_SEC; // in seconds
      printf("Time taken = %f seconds\n", time_taken);

      experimentFourD(numTrials); 
      t = clock() - t;
      time_taken = ((float)t)/CLOCKS_PER_SEC; // in seconds
      printf("Time taken = %f seconds\n", time_taken);
    }
  }

  return 0;
}

