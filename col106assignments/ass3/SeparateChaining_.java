//package assignment3;

public class SeparateChaining_<K, T> implements MyHashTable_<K, T>{
	bst[] hashTable;
	public int size;
	SeparateChaining_(int size) {
		this.size=size;
		hashTable=(bst[]) new bst[size];
		
	}
	
	public static long djb2(String str, int hashtableSize) { 
	    long hash = 5381; 
	    for (int i = 0; i < str.length(); i++) { 
	        hash = ((hash << 5) + hash) + str.charAt(i); 
	    } 
	    return Math.abs(hash) % hashtableSize; 
	}
	public long h(K key) {
		return (djb2(key.toString(),size))%size;
	}
	
	public int insert(K key, T obj) {
		int index=(int) h(key);
		if(hashTable[index]==null) {
			bst b = new bst((Student)obj);
			hashTable[index] = b;
			return 1;
		}
		else {
			return 1+hashTable[index].insertbst((Student)obj);
		}
			
	}

	public int update(K key, T obj) {
		int index=(int) h(key);
		return hashTable[index].updatebst((Student) obj);
		
	} 


	public int delete(K key) {
		int index=(int) h(key);
		Pair temp = (Pair)key;
		if(hashTable[index].data.fname().equalsIgnoreCase(temp.first)){
			int count = 0;
			if(hashTable[index].left==null&&hashTable[index].right == null) {hashTable[index]=null;return count++;}
			else if(hashTable[index].left == null) {hashTable[index] = hashTable[index].right;return 2;}
			else if(hashTable[index].right == null) {hashTable[index] = hashTable[index].left;return 2;}
			else{
				
				bst minbst=hashTable[index].right;
				if(minbst.left == null){hashTable[index].data = minbst.data;hashTable[index].right = hashTable[index].right.right;}
				else{while(minbst.left!=null) {
					minbst=minbst.left;
					count++;
				}
				hashTable[index].data=minbst.data;
				minbst.up.left = minbst.right;
				
			}
			return count;
		}	
	}
		else return hashTable[index].deletebst(temp);	
		//return 0;
	}

	public boolean contains(K key) {
		int index=(int) h(key);
		return hashTable[index].containsbst(key.toString());	
		
	}

	public T get(K key) throws NotFoundException {
		int index=(int) h(key);
		return (T)hashTable[index].getbst(key.toString());	
		
	}

	public String address(K key) throws NotFoundException {
		int index=(int) h(key);
		return Integer.toString(index)+"-"+hashTable[index].addressbst(key.toString());
	}

}
