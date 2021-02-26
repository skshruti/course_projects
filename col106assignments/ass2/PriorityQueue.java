
public class PriorityQueue<V> implements QueueInterface<V>{

    private NodeBase<V>[] queue;
    private int capacity, currentSize, front=0, rear=0;
	
    //TODO Complete the Priority Queue implementation
    // You may create other member variables/ methods if required.
    public PriorityQueue(int capacity) {    
    	this.capacity=capacity;
    	queue = new NodeBase[capacity];
    }

    public int size() {
    	return currentSize;
    }

    public boolean isEmpty() {
    	if(currentSize == 0) {
    		return true;
    	}
    	else {
    		return false;
    	}
    }
	
    public boolean isFull() {
    	if(currentSize == capacity) {
    		return true;
    	}
    	else {
    		return false;
    	}
    }

    public void enqueue(Node<V> node) {
    	if(!isFull()) {
    		queue[rear]=node;
    	rear=rear+1;
    	currentSize++;
    	}
    }

    // In case of priority queue, the dequeue() should 
    // always remove the element with minimum priority value
    public NodeBase<V> dequeue() {
    	if(!isEmpty()) {
    	int i=front;
    	int f=i;
    	int leastPri=queue[i].getPriority();
    	while(i<currentSize) {
    		if(queue[i].getPriority()<leastPri) {
    			leastPri=queue[i].getPriority();
    			f=i;
    		}
    		i=(i+1);
    	}
    	NodeBase<V> temp= queue[f];
    	rear--;
    	int j=f;
    	if((f+1)!=currentSize) {
    		while(j<currentSize) {
        		queue[j%capacity]=queue[(j+1)%capacity];
        		j++;
        	}
    	}
    	currentSize--;
    	return temp;
    	}
    	return null;
    }

    public void display () {
	if (this.isEmpty()) {
            System.out.println("Queue is empty");
	}
	for(int i=0; i<currentSize; i++) {
            queue[i+1].show();
	}
    }
		

	public void add(int priority, V value) {
		Node<V> newNode= new Node<V>(priority, value);
		this.enqueue(newNode);
	}

	public NodeBase<V> removeMin() {
		NodeBase<V> temp=this.dequeue();
		return temp;
	}
}

