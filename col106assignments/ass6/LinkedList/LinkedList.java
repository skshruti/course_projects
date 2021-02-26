package LinkedList;

public class LinkedList<E> {
	public Node<E> head;
	public Node<E> tail;
	int size;
    
    public LinkedList(){
        head = null;
        size=0;
        tail=null;
    }
    
    public boolean contains(E e) {
    	int i=0;
    	while(i<this.size()) {
    		if(this.get(i)!=null) 
    		{if(((Comparable) this.get(i)).compareTo((Comparable)e)==0) return true;}
    		i++;
    	}
    	return false;
    }

	public void add(E e) {
		Node<E> n=new Node<E>(e);
		if(head!=null) {
		tail.next=n;
		tail=tail.next;
		size++;
		return;
		}
		head=n; tail=n; size++;
	} 

	public E get(int i) {
		int index=0;
		Node n=this.head;
		while(index<i) {
			n=n.next;
			index++;
		}
		if(n==null) return null;
		return (E) n.data;
	}
    
    public int size() {
    	return this.size;
    }
    
    public void remove() {
    	if(head.next!=null) {
	    	head=head.next;
	    	this.size--;
    	}
    	else {
    		this.head=null;
    		this.size=0;
    	}
    	//return temp;
    }
}
