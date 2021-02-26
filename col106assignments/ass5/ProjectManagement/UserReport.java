package ProjectManagement;

public class UserReport extends User implements UserReport_{
	int cons=0;
	UserReport(String name) {
		super(name);
		// TODO Auto-generated constructor stub
	}
	 public String user()    { return this.uName; }

	    public int consumed() { 
	    	return this.cons;
	    	}
	    public String toString() {
	    	return("User "+this.uName+" Usage "+this.cons);
	    }
	    
	    public int compareTo2(UserReport that) {
	    	if(this.consumed()>that.consumed()) return 1;
	    	else if(this.consumed()<that.consumed()) return -1;
	    	else if(this.consumed()==that.consumed()) {
	    		return 0;
	    	}
	    	return 0;
	    }
}
