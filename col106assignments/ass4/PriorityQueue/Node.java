package PriorityQueue;

public class Node<T> {
	public T value;
	public int number;
	
	Node(T element,int num){
		this.value=element;
		this.number=num;
	}
	public void setPrior(int i) {
    	this.number=i;
    }
}
