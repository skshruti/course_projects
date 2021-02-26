package PriorityQueue;


public class MaxHeap<T extends Comparable> implements PriorityQueueInterface<T> {
	public Node<T>[] heap;
	int size=10000;
	
	public MaxHeap(){
		//heap= new T[size];
		heap= ((Node<T>[]) new Node[size]);
	}
	
	public int getParent(int i) { return (i-1)/2;};
	public int getLChild(int i) {return (2*i)+1;};
	public int getRChild(int i) {return (2*i)+2;};
	public int curSize=0;
	
	
	//public Student max(Student a,Student b) {
		//if(b.compareTo(a)>=0)
		//return b;
		//else return a;
		
	//}
	 
    @Override
    public void insert(T element) {
    	Node<T> node=new Node(element, curSize);
    	heap[curSize]=node;
    	int i=curSize;
    	if(heap[i].value==null) System.out.println("heap[i]");
    	if(heap[getParent(i)].value==null) System.out.println("heap[getParent(i)]");
    	while(heap[i].value.compareTo(heap[getParent(i)].value)>0) {
    		Node<T> temp=heap[i];
    		heap[i]=heap[getParent(i)];
    		heap[getParent(i)]=temp;
			i=getParent(i);
			
    	}
    	curSize++;
    	//int k=0;
    	//while(k<curSize) System.out.println("ins"+heap[k++].value);
    }
    
    @Override
   public T extractMax()
    {	
		//int k=0;
    	//while(k<curSize) System.out.println("ins"+heap[k++].value);
    	if (heap[0]!=null) {
    		Node<T> temp = heap[0];
			heap[0] = heap[curSize - 1];
			heap[curSize - 1] = null;
			curSize--;
			int i = 0;
			while (heap[getLChild(i)] != null || heap[getRChild(i)] != null) {
				if (( heap[getLChild(i)] != null && (heap[i].value.compareTo(heap[getLChild(i)].value) < 0)
						||(heap[getRChild(i)] != null && (heap[i].value).compareTo(heap[getRChild(i)].value) < 0))){
					if (heap[getRChild(i)] != null && (heap[getRChild(i)].value).compareTo(heap[getLChild(i)].value) > 0) {
						
						Node<T> temp2=heap[i];
			    		heap[i]=heap[getRChild(i)];
			    		heap[getRChild(i)]=temp2;
						i = getRChild(i);
					} else if (heap[getRChild(i)] != null && heap[getLChild(i)] != null && (heap[getRChild(i)].value).compareTo(heap[getLChild(i)].value) < 0) {
						
						Node<T> temp2=heap[i];
			    		heap[i]=heap[getLChild(i)];
			    		heap[getLChild(i)]=temp2;
			    		i = getLChild(i);
			    		
					} else {
						
						if (heap[getRChild(i)] != null && (heap[getRChild(i)]).number>(heap[getLChild(i)]).number) {
							Node<T> temp2 = heap[i];
							heap[i] = heap[getLChild(i)];
							heap[getLChild(i)] = temp2;
							i = getLChild(i);
						}
						else if(heap[getRChild(i)] != null && (heap[getRChild(i)]).number<(heap[getLChild(i)]).number){
							//System.out.println("heyy");
							//System.out.println("nonoononoooo"+heap[4].value.toString());
							Node<T> temp2 = heap[i];
							heap[i] = heap[getRChild(i)];
							heap[getRChild(i)] = temp2;
							i = getRChild(i);
						}
						else if(heap[getRChild(i)] == null && (heap[i].value.compareTo(heap[getLChild(i)].value) < 0)){
							Node<T> temp2 = heap[i];
							heap[i] = heap[getLChild(i)];
							heap[getLChild(i)] = temp2;
							i = getLChild(i);
						}
						else if(heap[getRChild(i)] == null && (heap[i]).number>(heap[getLChild(i)]).number) {
							Node<T> temp2 = heap[i];
							heap[i] = heap[getLChild(i)];
							heap[getLChild(i)] = temp2;
							i = getLChild(i);
						}
						else i=getLChild(i);
					}
				}
				else if ((heap[getLChild(i)] != null && (heap[i].value).compareTo( heap[getLChild(i)].value) == 0) && (heap[getRChild(i)] != null && (heap[i].value).compareTo(heap[getRChild(i)].value) == 0)) {
					if((heap[i]).number>(heap[getLChild(i)]).number && (heap[i]).number>(heap[getRChild(i)]).number){
						if((heap[getLChild(i)]).number<(heap[getRChild(i)]).number) {
							Node<T> temp2=heap[i];
				    		heap[i]=heap[getLChild(i)];
				    		heap[getLChild(i)]=temp2;
				    		
				    		i=getLChild(i);
						}
						else {
							Node<T> temp2=heap[i];
				    		heap[i]=heap[getRChild(i)];
				    		heap[getRChild(i)]=temp2;
				    		i=getRChild(i);
						}
					}
					else if((heap[i]).number>(heap[getLChild(i)]).number){
						Node<T> temp2=heap[i];
			    		heap[i]=heap[getLChild(i)];
			    		heap[getLChild(i)]=temp2;
			    		i=getLChild(i);
					}
					else if((heap[i]).number>(heap[getRChild(i)]).number){
						
							Node<T> temp2=heap[i];
				    		heap[i]=heap[getRChild(i)];
				    		heap[getRChild(i)]=temp2;
				    		i=getRChild(i);
					}
					else return temp.value;
				} //else if(heap[i]==null) { System.out.println("ha"); return temp.value;}
				//else if(heap[getLChild(i)]==null) { System.out.println("haha"); return temp.value;}
				else if (heap[getRChild(i)] != null && (heap[i].value).compareTo(heap[getLChild(i)].value) == 0) {
					if((heap[i].value).compareTo(heap[getRChild(i)].value) > 0){
						if((heap[i]).number>(heap[getLChild(i)]).number){
					Node<T> temp2=heap[i];
		    		heap[i]=heap[getLChild(i)];
		    		heap[getLChild(i)]=temp2;
					i = getLChild(i);}
					}
					else {
						Node<T> temp2=heap[i];
			    		heap[i]=heap[getRChild(i)];
			    		heap[getRChild(i)]=temp2;
			    		i=getRChild(i);
					}
				} else if (heap[getRChild(i)] != null && (heap[i].value).compareTo(heap[getRChild(i)].value) == 0) {
					if((heap[i].value).compareTo(heap[getLChild(i)].value) > 0){
						if((heap[i]).number>(heap[getRChild(i)]).number){
					Node<T> temp2=heap[i];
		    		heap[i]=heap[getRChild(i)];
		    		heap[getRChild(i)]=temp2;
					i = getRChild(i);}
					}
					else {
						Node<T> temp2=heap[i];
			    		heap[i]=heap[getLChild(i)];
			    		heap[getLChild(i)]=temp2;
			    		i=getLChild(i);
					}
				}
					else if(heap[getRChild(i)] == null) {
						if(heap[getLChild(i)] != null && (heap[i].value).compareTo(heap[getLChild(i)].value) == 0) {
							if((heap[i]).number>(heap[getLChild(i)]).number){
								Node<T> temp2=heap[i];
					    		heap[i]=heap[getLChild(i)];
					    		heap[getLChild(i)]=temp2;
								i = getLChild(i);}
							else {
								return temp.value;
							}
						}
						else if(heap[getLChild(i)] != null && (heap[i].value).compareTo(heap[getLChild(i)].value) < 0) {
							Node<T> temp2=heap[i];
				    		heap[i]=heap[getLChild(i)];
				    		heap[getLChild(i)]=temp2;
							i = getLChild(i);
						}
						else return temp.value;
				} else return temp.value;
					
			}
			//int k=0;
	    	//while(k<curSize) System.out.println("curHeap"+heap[k++]);
			return temp.value;
			
		}
    	return null;
    }

}