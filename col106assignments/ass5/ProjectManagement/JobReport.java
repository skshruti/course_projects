package ProjectManagement;

public class JobReport extends Job implements JobReport_ {
	 JobReport(String[] array) {
		super(array);
		// TODO Auto-generated constructor stub
	}

	public String user() { return this.user.uName; }

	    public String project_name()  { return this.project.pName; }

	    public int budget()  { return this.project.budget; }

	    public int arrival_time()  { return this.atime; }

	    public int completion_time() { return this.ctime; }
	    
	    public String toString2() {
	    	String compTime=null;
	    	if(this.ctime!=0) compTime=""+this.ctime; 
	    	return("Job{id="+this.number+", user='"+this.user.uName+"', project='"+this.project.pName+"', jobstatus="+this.stat+", execution_time="+this.runtime+", end_time="+compTime+", priority="+this.getPrior()+", name='"+this.jName+"'}" );
	    }
}
