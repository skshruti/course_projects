In this README file, I have only explained those methods which I was supposed to implement.
The starter code which was provided to us is not explained.

Node.java

The methods getPriority() and getValue() were completed which return the priority and value of the node respectively.


Queue.java

Queue(int capacity): Queue and capacity were initialised inside this.

size(): Returns the current size of the queue.

isEmpty() and isFull(): These methods returned Boolean type true or false if the queue was empty or full respectively. If currentSize was 0, isEmpty returned true and isFull returned True if the value of currentSize is equal to capacity.

Enqueue(Node<V> node): If the queue is full, then this function would do nothing. If it is not empty then node would be assigned to the first element and if not empty, node would be assigned to the element to which rear is pointing. The value of rear would be increased by 1 and currentSize would also increment by 1.

Dequeue(): The value inside the first element would be removed and all the subsequent elements would shift towards the left by 1 step so as to decrease the value of rear and CurrentSize by 1 and the node which is dequeued will be returned.


PriorityQueue.java

PriorityQueue(int capacity): Queue and capacity were initialised inside this.

size(): Returns the current size of the queue.

isEmpty() and isFull(): These methods returned Boolean type true or false if the queue was empty or full respectively. If currentSize was 0, isEmpty returned true and isFull returned True if the value of currentSize is equal to capacity.

Enqueue(Node<V> node): if the queue is full, then this function would do nothing. if it is not full, node would be assigned to the element to which rear is pointing. the value of rear would be increased by 1 and currentSize would also increment by 1.

Dequeue(): i is the pointer variable. It starts from the front and compares the priority of queue[f] to queue[i] and if priority of queue[i] is less than queue[f], it assigns i to f and keeps doing the same till it traverses the whole queue. hence, finally we get the queue[f] which has the least priority. Now since, one item is dequeued, rear is decreased by 1 and the currentSize too and all the elements following queue[f] are shifted towards the left by 1. the item which is dequeued is returned finally.

add(int priority, V value): A newNode is created with the priority and value and the newNode is enqueued to queue.

removeMin: The dequeue function is executed.


Buyer.java

First of all, the Buyer Constructor method was completed.

buy(): While the catalog is empty, the thread is asked to wait using the await() method. If not empty, a node is dequeued from the catalog, consumed message is diplayed along with the priority of the node dequeued and the other threads are signalled using the signalAll() method.


Seller.java

First of all, the Seller Constructor method was completed.

sell(): While the catalog is full, the thread is asked to wait using the await() method. If the inventory is not empty, a node is dequeued from the inventory and the same node is enqueued in the catalog and the other threads are signalled using the signalAll() method.


Assignment2Driver.java

Firstly, each element of the list is enqueued in the inventory using a while loop.

A for loop is created and objects of Seller are made till the the required number(=a_driver.numSellers) of objects is created. 
Another for loop is created and objects of Buyer are made till the the required number(=a_driver.numBuyers) of objects is created. 
A threadSellers array is created which contains the threads of all the sellers. 
A threadBuyers array is created which contains the threads of all the buyers. 
All the elements of both the arrays are started.





