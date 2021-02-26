//package assignment3;

public class Pair<A, B> {

	String first;
	String second;
	Pair(String A, String B){
		this.first=A;
		this.second=B;
	}
	public String toString(){
		return (this.first+this.second);
	}
}
