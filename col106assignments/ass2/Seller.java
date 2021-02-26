import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;

public class Seller<V> extends SellerBase<V> {
	
    private int capacity;

	public Seller (int sleepTime, int catalogSize, Lock lock, Condition full, Condition empty, PriorityQueue<V> catalog, Queue<V> inventory) throws InterruptedException {
        //TODO Complete the constructor method by initializing the attributes
        // ...
    	setSleepTime(sleepTime);
    	this.capacity=catalogSize;
    	this.inventory=inventory;
    	//lock.lock();
    	this.catalog=catalog;
    	this.lock = lock;
    	this.full = full;
    	this.empty = empty;
    	//full.await();
    	//full.notify();
    	//full.notifyAll();
    	//empty.await();
    	//empty.notify();
    	//empty.notifyAll();
    	
    }
    
    public void sell() throws InterruptedException {
    	
    	lock.lock();
	try {
            //TODO Complete the try block for produce method
            // ...
		while(catalog.size()==capacity) {
			full.await();
		}
		if(!inventory.isEmpty()) {
			Node<V> item = (Node<V>) inventory.dequeue();
			catalog.enqueue(item);
			empty.signalAll();
		}
		
		
	} catch(Exception e) {
            e.printStackTrace();
	} finally {
            //TODO Complete this block
		lock.unlock();
	}		
    }
}
