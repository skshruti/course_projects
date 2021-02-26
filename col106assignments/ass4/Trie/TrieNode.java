package Trie;
import Util.NodeInterface;


public class TrieNode<T> implements NodeInterface<T> {
	public T value;
	public TrieNode[] array;
	public TrieNode parent;
	
	TrieNode(){
		this.array=new TrieNode[95];
	}
    @Override
    public T getValue() {
        return this.value;
    }


}