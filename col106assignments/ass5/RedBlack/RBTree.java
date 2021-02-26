package RedBlack;

public class RBTree<T extends Comparable, E> implements RBTreeInterface<T, E>  {
	RedBlackNode root;
	RBTree(){
		this.root=new RedBlackNode();
		
	}
	public void ll(RedBlackNode x, RedBlackNode y, RedBlackNode z) {
		z.left=y.right;
		z.parent=y;
		y.parent=z.parent;
		y.right=z;
		z.parent=y;
	}
	
	public void lr(RedBlackNode x, RedBlackNode y, RedBlackNode z) {
		x.parent=z;
		z.left=x;
		y.right=x.left;
		y.parent=x;
		x.left=y;
		ll(y, x, z);
	}
	
	public void rr(RedBlackNode x, RedBlackNode y, RedBlackNode z) {
		z.right=y.left;
		z.parent=y;
		y.parent=z.parent;
		y.left=z;
		z.parent=y;
	}
	
	public void rl(RedBlackNode x, RedBlackNode y, RedBlackNode z) {
		x.parent=z;
		z.right=x;
		y.left=x.right;
		y.parent=x;
		x.right=y;
		rr(y, x, z);
	}
	
	public void restructure(RedBlackNode x, RedBlackNode y, RedBlackNode z) {
		if(z.left==y && y.left==x) ll(x, y, z);
		else if(z.left==y && y.right==x) lr(x,y,z);
		else if(z.right==y && y.right==x) rr(x,y,z);
		else if(z.right==y && y.left==x) rl(x,y,z);
	}
	
	public RedBlackNode uncle(RedBlackNode x) {
		if(x.parent.parent.left==x.parent) return x.parent.parent.right;
		else return x.parent.parent.left;
		
	}
	
	public void dothis(RedBlackNode x) {
		if(x==root) { x.color="black"; return;}
		else 
			while(x!=root) {
				if(x.parent.color!="black") {
					if(uncle(x).color=="red") {
						x.parent.color="black";
						uncle(x).color="black";
						x.parent.parent.color="red";
						x=x.parent.parent;
					}
					else restructure(x, x.parent, x.parent.parent);
				}
				else {
					return;
				}
			}
		
	}
	
	
	
	
    @Override
    public void insert(T key, E value) {
    	if(root.key==null) {
    		root = new RedBlackNode<T,E>(key, value);
    		root.color = "black";
    		
    		return;
    	}
    	else {
        	RedBlackNode papa = null;
        	RedBlackNode p = root;
    		while(p.left!=null) {
    			if(p.key.compareTo(key) == 0) {
    				
    				p.vlist.add(value);
    				
    				return;
    			}
    			else if(p.key.compareTo(key)>0) {
    				papa = p;
    				p=p.left;
    			}
    			else {
    				papa = p;
    				p=p.right;
    			}
    			}
		
        	p = new RedBlackNode<T,E>(key, value);
        	p.parent = papa;
        	if(papa.key.compareTo(key) > 0) papa.left = p;
        	else papa.right = p;
        	
        	
    	}
    
    }

    @Override
    public RedBlackNode<T, E> search(T key) {
    	if(root.key==null) {
    		return null;
    	}
    	else if(root.key.compareTo(key)==0) {
    		return root; 
    	}
    	else {
    		RedBlackNode p = root;
    		while(p.key!=null)
		    	if(p.key.compareTo(key)==0) return p; 
		    	else if(p.key.compareTo(key)>0) p=p.left;
		    	else p=p.right;
    	}
		return null;
    
    
    }
}