package ProjectManagement;

import java.util.LinkedList;

public class User implements Comparable<User>, UserReport_ {
	public String uName;
	int cons;
	
	User(String name){
		this.uName=name;
		
	}
    @Override
    public int compareTo(User user) {
    	if(this.uName.compareTo(user.uName)>0) return 1;
    	else if(this.uName.compareTo(user.uName)>0) return -1;
    	else return 0;
    }
    
    public String user()    { return this.uName; }

    public int consumed() { return this.cons; }

    public String toString() {
    	return("User "+this.uName+" Usage "+this.cons);
    }

	
	@Override
	public int compareTo2(UserReport_ userReport_) {
		if(this.consumed()>userReport_.consumed()) return 1;
    	else if(this.consumed()<userReport_.consumed()) return -1;
    	else if(this.consumed()==userReport_.consumed()) {
    		return 0;
    	}
    	return 0;
	}
}
