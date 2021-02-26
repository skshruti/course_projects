package ProjectManagement;

import java.util.LinkedList;

public class User implements Comparable<User> {
	public String uName;
	

	
	User(String name){
		this.uName=name;
		
	}
    @Override
    public int compareTo(User user) {
    	if(this.uName.compareTo(user.uName)>0) return 1;
    	else if(this.uName.compareTo(user.uName)>0) return -1;
    	else return 0;
    }
    
}
