package LinkedList;

public class Node<E> {
	public E data; 
    Node<E> next; 
    public Node(E d) { 
        data = d;
        next = null;
    } 
    public Node() { 
        data = null;
        next = null;
    } 
}
