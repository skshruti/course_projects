package ProjectManagement;

import PriorityQueue.MaxHeap;
import ProjectManagement.Project;



public class Job implements Comparable<Job> {
	public String jName;
	public Project project;
	public User user;
	public int runtime;
	public int ctime;
	public int etime;
	public enum status{REQUESTED, COMPLETED}
	public status stat;
    //public int number;
	

	Job(String[] array){
		this.jName=array[1];
		this.runtime=Integer.parseInt(array[4]);
	}
    @Override
    public int compareTo(Job job) {
    	int tprior=Integer.parseInt(this.getPrior());
    	int jprior=Integer.parseInt(job.getPrior());
    	if(tprior>jprior) return 1;
        else if(tprior<jprior) return -1;
        else return 0;
    }
    
//    public void setPrior(int i) {
//    	this.number=i;
//    }
//    
    public String getPrior() {
    	return this.project.priority;
    }
    
    public String toString() {
    	String compTime=null;
    	if(this.ctime!=0) compTime=""+this.ctime; 
    	return("Job{user='"+this.user.uName+"', project='"+this.project.pName+"', jobstatus="+this.stat+", execution_time="+this.runtime+", end_time="+compTime+", name='"+this.jName+"'}" );
    }
}