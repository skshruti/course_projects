package Trie;

public class Person {
	public String naam;
	public String pno;

    public Person(String name, String phone_number) {
    	naam=name;
    	pno=phone_number;
    }

    public String getName() {
        return this.naam;
    }
    
    public String toString() {
    	return ("[Name: " + this.naam+", Phone="+ this.pno+"]");
    }
}
