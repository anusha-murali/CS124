##/*
##A binary heap is a Binary Tree with following properties:
##1) It’s a complete tree (All levels are completely filled except possibly the last level and the last level has all keys as left as
##possible). This property of Binary Heap makes them suitable to be stored in an array.
##
##2) A Binary Heap is either Min Heap or Max Heap. In a Min Binary Heap, the key at root must be minimum among all keys present in Binary
##Heap. The same property must be recursively true for all nodes in Binary Tree. Max Binary Heap is similar to MinHeap.
##
##Given some queries and your task is to implement the three methods insertKey,  deleteKey,  and extractMin on a Binary Min Heap and call
##them as per the query given below:
##1) 1  x  (a query of this type means to insert an element in the min heap with value x )
##2) 2  x  (a query of this type means to remove an element at position x from the min heap)
##3) 3  (a query like this removes the min element from the min heap and prints it ).
##
##Input:
##The first line of the input contains an integer 'T' denoting the number of test cases. Then T test cases follow. First line of each test
##case contains an integer Q denoting the number of queries. The second line of each test case contains Q queries seperated by space.
##
##Output:
##The output for each test case will  be space separated integers having -1  if the heap is empty else the min element of the heap.
##
##Your Task:
##You are required to complete the 3 methods insertKey() which takes one argument the value to be inserted , deleteKey() which takes one 
##argument the position from where element is to be deleted and extractMin() which returns the minimum element in the heap.
##
##Constraints:
##1 <= T <= 100
##1 <= Q <= 100
##1 <= x <= 100
##
##Example:
##Input:
##2
##7
##1 4 1 2 3 1 6 2 0 3 3
##5
##1 8 1 9 2 1 3 3
##
##Output:
##2 6 - 1
##8 -1
## 
##
##Explanation:
##Testcase 1:
##In the first test case for query 
##1 4      the heap will have  {4}  
##1 2      the heap will be {2 4}
##3         removes min element from heap ie 2 and prints it now heap is {4} 
##1 6      inserts 6 to heap now heap is {4 6}
##2 0      delete element at position 0 of heap now heap is {6}
##3         remove min element from heap ie 6 and prints it  now the heap is empty {}
##3         since heap is empty thus no min element exist so -1 is printed .
##*/


int MinHeap ::  extractMin()
{
    if(heap_size<=0) return -1;
    if(heap_size==1){
        heap_size--;
        return harr[0];
    }
    int root=harr[0];
    harr[0] = harr[heap_size-1];
    heap_size--;
    MinHeapify(0);
    return root;
}



void MinHeap :: deleteKey(int i)
{
    if(i>=heap_size) return;
    decreaseKey(i, INT_MIN);
    extractMin();
}



void MinHeap ::insertKey(int k)
{
  if(heap_size == capacity) return;
  heap_size++;
  int i=heap_size -1;
  harr[i] = k;
  
  while(i!=0 && harr[parent(i)] > harr[i] ){
      swap(harr[i] , harr[parent(i)]);
      i=parent(i);
  }
  
}



void MinHeap::decreaseKey(int i, int new_val)
{
    harr[i] = new_val;
    while (i != 0 && harr[parent(i)] > harr[i])
    {
       swap(harr[i], harr[parent(i)]);
       i = parent(i);
    }
}



void MinHeap::MinHeapify(int i)
{
    int l = left(i);
    int r = right(i);
    int smallest = i;
    if (l < heap_size && harr[l] < harr[i])
        smallest = l;
    if (r < heap_size && harr[r] < harr[smallest])
        smallest = r;
    if (smallest != i)
    {
        swap(harr[i], harr[smallest]);
        MinHeapify(smallest);
    }
}
