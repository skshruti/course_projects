// This class implements the Queue
public class Queue<V> implements QueueInterface<V>{

    //TODO Complete the Queue implementation
    private NodeBase<V>[] queue;
    private int capacity, currentSize, front=0, rear=0;
	
    public Queue(int capacity) {    
    	this.capacity=capacity;
    	queue = new NodeBase[capacity];
    	
    }
    
    public int size() {
    	return currentSize;
    }

    public boolean isEmpty() {
    	if(currentSize==0) {
    		return true;
    	}
    	else {
    		return false;
    	}
    }
	
    public boolean isFull() {
    	if(currentSize==capacity) {
    		return true;
    	}
    	else {
    		return false;
    	}
    }

    public void enqueue(Node<V> node) {
    	if(!isFull()) {
    	if(! isEmpty()) {
    		queue[rear]=node;
    	}
    	else {
    		queue[front]=node;
    	}
    	rear=(rear+1)%capacity;
    	currentSize++;
    	}
    	
    }

    public NodeBase<V> dequeue() {
    	if(!isEmpty()) {
    	NodeBase<V> temp= queue[front];
    	rear--;
    	int j=front;
    	while(j<currentSize) {
    		queue[j%capacity]=queue[(j+1)%capacity];
    		j++;
    	}
    	currentSize--;
    	return temp;
    	}
    	return null;
    }
    

}

