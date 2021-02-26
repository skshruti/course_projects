//package assignment3;
import java.lang.Math;

public class DoubleHashing_<K, T> implements MyHashTable_<K, T> {
	public int size;
	T[] hashTable;
	

	public DoubleHashing_(int size) {
		this.size=size;
		hashTable=((T[]) new Object[size]);
		
	}
	
	public T record;
	
	public static long djb2(String str, int hashtableSize) { 
	    long hash = 5381; 
	    for (int i = 0; i < str.length(); i++) { 
	        hash = ((hash << 5) + hash) + str.charAt(i); 
	    } 
	    return Math.abs(hash) % hashtableSize; 
	}
	public static long sdbm(String str, int hashtableSize) { 
	    long hash = 0; 
	    for (int i = 0; i < str.length(); i++) { 
	        hash = str.charAt(i) + (hash << 6) + (hash << 16) - hash; 
	    } 
	    return Math.abs(hash) % (hashtableSize - 1) + 1; 
	}
	
	public long h(K key,int i) {
		return (djb2(key.toString(),size) + i*sdbm(key.toString(),size))%size;
	}
	
	public int insert(K key, T obj) {
		int j=0;
		int index=(int) h(key, j);
		int count=1;
		while(hashTable[index]!=null) {
			index=(int) h(key, count);
			count++;
		}
		hashTable[index]=obj;
		return count;
	}

	
	public int update(K key, T obj) {
		int j=0;
		int index=(int) h(key, j);
		int count=1;
		while(hashTable[index]==null ||((Student) hashTable[index]).pair().toString().equals(key.toString())==false) {
			j++;
			index=(int) h(key, j);
			count++;
		}
		hashTable[index]=obj;
		return count;
	}


	public int delete(K key) {
			int j=0;
			int index=(int) h(key, j);
			int count=1; 
			while(hashTable[index]==null ||((Student) hashTable[index]).pair().toString().equals(key.toString())==false) {
				j++;
				index=(int) h(key, j);
				count++;
			}
			hashTable[index]=null;
			return count;
		
	}


	public boolean contains(K key) {
		int count=0;
		int index=(int) h(key, count);
		int findex=(int) h(key, count);
		if(hashTable[index]!=null && ((Student) hashTable[index]).pair().toString().equals(key.toString())) {
			return true;
		}
		else { 
			count++;
			index=(int) h(key, count);
			while(index!=findex){
			if(hashTable[index]!=null && ((Student) hashTable[index]).pair().toString().equals(key.toString())){
				return true;
			}
			else {
				count++;
				index=(int) h(key, count);
			}
				
		}
		}
		return false;
	}
		

	public T get(K key) throws NotFoundException {
			int j=0;
			int index=(int) h(key, j);
			while(hashTable[index]==null ||((Student) hashTable[index]).pair().toString().equals(key.toString())==false) {
				index=(int) h(key, ++j);
			}
			if(hashTable[index]!=null) {
				return (T)((Student)hashTable[index]).getData();
			}
			else {
				return null;
			}
		
	}

	public String address(K key) throws NotFoundException {

			int j=0;
			int index=(int) h(key, j);
			while(hashTable[index]==null || ((Student) hashTable[index]).pair().toString().equals(key.toString())==false) {
				j++;
				index=(int) h(key, j);
			}
			if(hashTable[index]!=null) {
				return (index+"");
			}
			else {
				return null;
			}
			
		
	}
	
}


