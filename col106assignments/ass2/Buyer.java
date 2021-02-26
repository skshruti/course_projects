import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;

public class Buyer<V> extends BuyerBase<V> {
	public int  capacity;
	public Buyer (int sleepTime, int catalogSize, Lock lock, Condition full, Condition empty, PriorityQueue<V> catalog, int iteration) throws InterruptedException {
        //TODO Complete the Buyer Constructor method
        // ...
    	setSleepTime(sleepTime);
    	this.capacity=catalogSize;
    	setIteration(iteration);
    	this.lock = lock;
    	this.catalog=catalog;
    	this.full = full;
    	this.empty = empty;
    	//full.await();
    	//full.notify();
    	//full.notifyAll();
    	//empty.await();
    	//empty.notify();
    	//empty.notifyAll();
    }
	
    public void buy() throws InterruptedException {
    	lock.lock();
    	
	try {
            //TODO Complete the try block for consume method
            // ...
		while(catalog.size()==0) {
			empty.await();
		}
			Node<V> n = (Node<V>) catalog.removeMin();
		    System.out.print("Consumed "); // DO NOT REMOVE (For Automated Testing)
		    n.show(); // DO NOT REMOVE (For Automated Testing)
		    full.signalAll();
		
	} catch (Exception e) {
            e.printStackTrace();
	} finally {
            //TODO Complete this block
		lock.unlock();
	}
    }
}
