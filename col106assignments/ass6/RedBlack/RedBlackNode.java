package RedBlack;
import LinkedList.LinkedList;
import Util.RBNodeInterface;


public class RedBlackNode<T extends Comparable, E> implements RBNodeInterface<E> {
	public String color;
	public T key;
	public LinkedList<E> vlist;
	public RedBlackNode right;
	public RedBlackNode left;
	public RedBlackNode parent;
	
	RedBlackNode(T k, E e) { 
		this.right= new RedBlackNode();
		this.left=new RedBlackNode();
		this.parent = null;
		this.vlist=new LinkedList();
		vlist.add(e);
		this.key = k;
		this.color = "red";
	}
	
	
	public RedBlackNode() {
		this.right=null;
		this.left=null;
		this.parent = null;
		this.vlist	=	null;
		this.key = null;
		this.color = "black";
	} 

    @Override
    public E getValue() {
        return this.vlist.get(0);
    }

 
    public LinkedList<E> getValues() {
        return this.vlist;
    }
    
    
}
