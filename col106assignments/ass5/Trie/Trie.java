
package Trie;
import java.util.ArrayList;
import java.util.LinkedList;

public class Trie<T> implements TrieInterface {
	TrieNode root;
	public Trie(){
		this.root=new TrieNode();
		
	}
//	
//	public void updateNull(TrieNode tn) {
//		if(tn!=null) {
//			tn.value=null;
//			tn.array=null;
//			tn=null;
//		}
//    }
    

    public void printTrie(TrieNode trieNode) {
    	int i=0;
    	if(trieNode.value!=null) {
    		System.out.println(trieNode.getValue());
    	}
    	while(i<95) {
    		if(trieNode.array[i]!=null) {
    			printTrie(trieNode.array[i]);
    		}
    		i++;
    		
    	}
    }
    
    
    public boolean hasNoChild(TrieNode root) 
    { 
		for (int i = 0; i < 95; i++)
			if (root.array!=null && root.array[i] != null && root.array[i].array != null)
				return false;
		return true; 
    } 
    int k=0;
    @Override
    public boolean delete(String word) {
    	TrieNode tn=this.root;
    	int i=0;
    	k++;int c=0;
    	while( word!=null && i<word.length()) {
    		c=(int)(word.charAt(i));
	    	int index=c-32;
	    	if(tn.array==null) break;
	    	if(tn.array[index]!=null) {
	    		tn=tn.array[index];
	    		i++;
	    	}
	    	else {
	    		return false;}
    	}
    	if(tn.value==null) {
    		return false;}
    	return deleting(word);
    	
    }
    
    public boolean deleting(String word) {
    	TrieNode tn=this.root;
    	int i=0;
    	k++;
    	while( word!=null && i<word.length()) {
    		int c=(int)(word.charAt(i));
	    	int index=c-32;
	    	if(tn.array==null) break;
	    	if(tn.array[index]!=null) {
	    		tn=tn.array[index];
	    		i++;
	    	}
	    	else return false;
    	}
    		if(hasNoChild(tn)) {
    			tn.value = null;
    			tn.array = null;
	    		deleting(word.substring(0, word.length()-1));
	    		return true;
	    	}
	    	else {
	    		tn.value=null;
	    		return true;
	    	}
    }
    
    @Override
    public TrieNode<T> search(String word) {
    	TrieNode tn=this.root;
    	int i=0;
    	while( word!=null && i<word.length()) {
    		int c=(int)(word.charAt(i));
	    	int index=c-32;
	    	if(tn.array==null) break;
	    	if(tn.array[index]!=null) {
	    		tn=tn.array[index];
	    		i++;
	    	}
	    	else return null;
    	}
    	if(tn.value==null || tn==null) return null;
        return tn;
   
        
    }

    @Override
    public TrieNode<T> startsWith(String prefix) {
    	TrieNode tn=this.root;
    	int i=0;
    	while( prefix!=null && i<prefix.length()) {
    		int c=(int)(prefix.charAt(i));
	    	int index=c-32;
	    	if(tn.array[index]!=null) {
	    		tn=tn.array[index];
	    		i++;
	    	}
	    	else return null;
    	}
        return tn;
    	
    }
    
    @Override
    public boolean insert(String word, Object value) {
    TrieNode tn=this.root;
    	int i=0;
    	while( word!=null && i<word.length()) {
    		int c=(int)(word.charAt(i));
	    	int index=c-32;
	    	if(tn!=null && tn.array[index]==null)
	    		{
	    		tn.array[index]=new TrieNode();
	    		}
	    	tn=tn.array[index];
	    	i++;
    	}
    	if(tn!=null) {
    		tn.value=(T) value;
    		return true;
    	}
        return false;
    }

    @Override
    public void printLevel(int level) {
    	ArrayList<TrieNode> list=new ArrayList<TrieNode>();
    	TrieNode tn=this.root;
    	TrieNode tnp=null;
    	list.add(tn);
    	int i=1; 
    	while(i<=level-1) {
    		list.add(tnp);
    		int j=0;
    		int k=list.size();
    		while(j<k-1) {
    			TrieNode temp=list.get(j);
    			int index=0;
    			while(index<95) {
    				if(temp.array[index]!=null) {
    					list.add(temp.array[index]);
    				}
    				index++; 
    			}
    			j++;
    		}
    		ArrayList dellist=new ArrayList();
    		int lol=0;
    		while(list.get(lol)!=tnp) { dellist.add(list.get(lol)); lol++;}
    		list.removeAll(dellist);
    		list.remove(0);
    		i++;
    	}
    	//System.out.println(list.size());
    	//sort(list);
    	
    	int yas=0;
    	ArrayList<Character> newList=new ArrayList();
    	while(yas<list.size()) {
    		//S=S+" "+(character((TrieNode)list.get(yas)));
    		int ha=0;
    		while(ha<character(list.get(yas)).size())
    		{
    			newList.add(character(list.get(yas)).get(ha));
    			ha++;
    		}
    		yas++;
    	}
    	sort(newList);
    	String S=""+newList.get(0);
    	int x=1;
    	while(x<newList.size()) {
    		S=S+","+newList.get(x);
    		x++;
    	}
    	System.out.println("Level "+i+": "+S);
    }
    
    
    private ArrayList<Character> character(TrieNode trieNode) {
		if(trieNode!=null) {
			ArrayList<Character> list1=new ArrayList();
			
			int i=1;
			while(i<95) {

		    	if(trieNode.array==null) break;
				if(trieNode.array[i]!=null && (trieNode.array[i].array!=null || trieNode.array[i].value!=null)) list1.add((char)(i+32));
				i++;
			}
			int j=0;
			//String S="";
			//while(j<list1.size()) { S=S+list1.get(j); j++;}
			ArrayList<Character> nList=new ArrayList();
			while(j<list1.size()) { nList.add(list1.get(j)); j++;}
			return nList;
			}
		return null;
		}
	
    @Override
    public void print() {
    	System.out.println("-------------\n" + 
    			"Printing Trie");
    	LinkedList<TrieNode> list=new LinkedList<TrieNode>();
    	LinkedList<TrieNode> thisLevel = new LinkedList<TrieNode>();
    	
    	TrieNode tn=this.root;
    	TrieNode tnp=null;
    	list.add(tn);
    	int i=1; 
    	while(list.size() != 0) {
    		list.add(tnp);
    		int j=0;
    		int k=list.size();
    		while(list.getFirst() != null) {
    			TrieNode temp=list.remove();
    			thisLevel.add(temp);
    			int index=0;
    			while(index<95) {
    				if(temp.array!=null && temp.array[index]!=null) {
    					list.add(temp.array[index]);
    				}
    				index++; 
    			}
    			j++;
    		}
    		list.remove();
    	
    	//System.out.println(list.size());
    	//sort(list);
    	
    		int yas=0;
    		ArrayList<Character> newList=new ArrayList();
    		int size = thisLevel.size();
    		while(yas<size) {
    			//S=S+" "+(character((TrieNode)list.get(yas)));
    			int ha=0;
    			while(ha<character(thisLevel.get(0)).size())
    			{
    				newList.add(character(thisLevel.get(0)).get(ha));
    				
    				ha++;
   				}
    			thisLevel.remove();
    			yas++;
    		}
    		sort(newList);
    		String S="";
    		int x=0;
    		while(x<newList.size()) {
    			S=S+newList.get(x);
    			if(x < newList.size()-1) S+= ",";
    			x++;
    		}
    		System.out.println("Level "+i+": "+S);
    		i++;
    	}
    	System.out.println("-------------");
    }
    
    public void sort(ArrayList<Character> list) {
    	//ArrayList list=new ArrayList();
    	//list.add("a");
    	//list.add("B");
    	//list.add("j");
    	//list.add("c");
    	for (int i = 0; i < list.size(); i++) {
    	    for (int j = list.size() - 1; j > i; j--) {
    	        if (list.get(i)>list.get(j)) {
    	        	char tmp = list.get(i);
    	            list.set(i, list.get(j));
    	            list.set(j, tmp);
    	            }
    	    }
    	}
    }
}