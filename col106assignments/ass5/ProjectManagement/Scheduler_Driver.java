package ProjectManagement;


import java.io.*;
import java.net.URL;
import java.util.ArrayList;
import java.util.LinkedList;

import PriorityQueue.MaxHeap;
import ProjectManagement.Job.status;
import Trie.Trie;

public class Scheduler_Driver extends Thread implements SchedulerInterface {


    public static void main(String[] args) throws IOException {
//

        Scheduler_Driver scheduler_driver = new Scheduler_Driver();
        File file;
        if (args.length == 0) {
            URL url = Scheduler_Driver.class.getResource("INP");
            file = new File(url.getPath());
        } else {
            file = new File(args[0]);
        }

        scheduler_driver.execute(file);
    }

    public void execute(File commandFile) throws IOException {


        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(commandFile));

            String st;
            while ((st = br.readLine()) != null) {
                String[] cmd = st.split(" ");
                if (cmd.length == 0) {
                    System.err.println("Error parsing: " + st);
                    return;
                }
                String project_name, user_name;
                Integer start_time, end_time;

                long qstart_time, qend_time;

                switch (cmd[0]) {
                    case "PROJECT":
                        handle_project(cmd);
                        break;
                    case "JOB":
                        handle_job(cmd);
                        break;
                    case "USER":
                        handle_user(cmd[1]);
                        break;
                    case "QUERY":
                        handle_query(cmd[1]);
                        break;
                    case "": // HANDLE EMPTY LINE
                        handle_empty_line();
                        break;
                    case "ADD":
                        handle_add(cmd);
                        break;
                    //--------- New Queries
                    case "NEW_PROJECT":
                    case "NEW_USER":
                    case "NEW_PROJECTUSER":
                    case "NEW_PRIORITY":
                        timed_report(cmd);
                        break;
                    case "NEW_TOP":
                        qstart_time = System.nanoTime();
                        timed_top_consumer(Integer.parseInt(cmd[1]));
                        qend_time = System.nanoTime();
                        System.out.println("Time elapsed (ns): " + (qend_time - qstart_time));
                        break;
                    case "NEW_FLUSH":
                        //qstart_time = System.nanoTime();
                        timed_flush( Integer.parseInt(cmd[1]));
                        //qend_time = System.nanoTime();
                        //System.out.println("Time elapsed (ns): " + (qend_time - qstart_time));
                        break;
                    default:
                        System.err.println("Unknown command: " + cmd[0]);
                }

            }


            run_to_completion();
            print_stats();

        } catch (FileNotFoundException e) {
            System.err.println("Input file Not found. " + commandFile.getAbsolutePath());
        } catch (NullPointerException ne) {
            ne.printStackTrace();

        }
    }

    @Override
    public ArrayList<JobReport_> timed_report(String[] cmd) {
        long qstart_time, qend_time;
        ArrayList<JobReport_> res = null;
        switch (cmd[0]) {
            case "NEW_PROJECT":
                qstart_time = System.nanoTime();
                res = handle_new_project(cmd);
                qend_time = System.nanoTime();
               // System.out.println(res);
                System.out.println("Time elapsed (ns): " + (qend_time - qstart_time));
                break;
            case "NEW_USER":
                qstart_time = System.nanoTime();
                res = handle_new_user(cmd);
                qend_time = System.nanoTime();
               // System.out.println(res);
                System.out.println("Time elapsed (ns): " + (qend_time - qstart_time));

                break;
            case "NEW_PROJECTUSER":
                qstart_time = System.nanoTime();
                res = handle_new_projectuser(cmd);
                qend_time = System.nanoTime();
               // System.out.println(res);
                System.out.println("Time elapsed (ns): " + (qend_time - qstart_time));
                break;
            case "NEW_PRIORITY":
                qstart_time = System.nanoTime();
                res = handle_new_priority(cmd[1]);
                qend_time = System.nanoTime();
               // System.out.println(res);
                System.out.println("Time elapsed (ns): " + (qend_time - qstart_time));
                break;
        }

        return res;
    }
    Trie pTrie=new Trie<>();
    MaxHeap jHeap=new MaxHeap();
    LinkedList<User> uList=new LinkedList<User>();
    LinkedList<Job> finished=new LinkedList<Job>();
    LinkedList<Job> unfinished=new LinkedList<Job>();
    ArrayList<JobReport_> allJobs=new ArrayList<JobReport_>();
    ArrayList<UserReport_> allUser=new ArrayList<UserReport_>();
    public int gtime;
    public int aNumber=0;
    //public int consumed=0;

    @Override
    public ArrayList<UserReport_> timed_top_consumer(int top) {
    	//System.out.println("Top query");
    	ArrayList<UserReport_> arrUser=new ArrayList<UserReport_>();
    	int i=0;
    	while(i<uList.size()) {
    		if(uList.get(i).cons>=top) arrUser.add(uList.get(i));
    		i++;
    	}
//    	int l=0;
//    	while(l<arrUser.size()) System.out.println(arrUser.get(l++).toString());
    	sort(arrUser);
//    	int k=0;
//    	while(k<arrUser.size()) System.out.println(arrUser.get(k++).toString());
        return arrUser;
    }



    @Override
    public void timed_flush(int waittime) {
    	//System.out.println("Flush query");
    	int index=0;
    	//int no=0;
    	int abhi=gtime;
    	LinkedList<Job> flushed=new LinkedList<Job>();
    	while(index<jHeap.curSize)
    	{
    		//System.out.println(gtime);
			//System.out.println(((Job)(jHeap.heap[index].value)).jName+((Job)(jHeap.heap[index].value)).atime);
    		if((abhi-((Job)(jHeap.heap[index].value)).atime)>=waittime){
    			flushed.add((Job) jHeap.heap[index].value);
    			execute_a_job((Job)(jHeap.heap[index].value));
    			//no++;
    			
    			index--;
    			//jHeap.remove((Job)(jHeap.heap[index].value));
    		}
    		index++;
    	}
    	
//    	for(int j=0; j<flushed.size(); j++) {
//    		//System.out.println("heyyyy");
//    		System.out.println("Flushed: "+flushed.get(j).toString2());
//    	}
    }
    
    

    private ArrayList<JobReport_> handle_new_priority(String s) {
    	//System.out.println("Priority query");
    	ArrayList<JobReport_> arrJob=new ArrayList<JobReport_>();
    	int k=0;
    	while(k<unfinished.size()) {
    			if(Integer.parseInt(unfinished.get(k).getPrior())>=Integer.parseInt(s)){
    				arrJob.add(unfinished.get(k));
    			}
    			k++;
    	}
    	int i=0;
    	while(i<jHeap.curSize) {
    			if(Integer.parseInt(((Job) jHeap.heap[i].value).getPrior())>=Integer.parseInt(s)){
    				arrJob.add((Job) jHeap.heap[i].value);
    			}
    			i++;
    	}	
    	
        return arrJob;
    }

    private ArrayList<JobReport_> handle_new_projectuser(String[] cmd) {
    	//System.out.println("Project User query");
    	ArrayList<JobReport_> unJobs=new ArrayList<JobReport_>();
    	ArrayList<JobReport_> arrJob=new ArrayList<JobReport_>();
    	int i=0;
    	//System.out.println("okay");
    	while(i<allJobs.size()) {
    		//System.out.println("okay");
    		if (allJobs.get(i).user().compareTo(cmd[2])==0 && allJobs.get(i).project_name().compareTo(cmd[1])==0 && allJobs.get(i).arrival_time()>=Integer.parseInt(cmd[3]) && (allJobs.get(i).arrival_time()<=Integer.parseInt(cmd[4]))) {
				if (unfinished.contains(allJobs.get(i)))
					unJobs.add(allJobs.get(i));
				else
					arrJob.add(allJobs.get(i));
				}
    		i++;
    	}
    	arrJob.addAll(unJobs);
    	//int k=0;
    	//while(k<arrJob.size()) System.out.println(arrJob.get(k++).toString2());
        return arrJob;
    }

    private ArrayList<JobReport_> handle_new_user(String[] cmd) {
    	//System.out.println("User query");
    	ArrayList<JobReport_> arrJob=new ArrayList<JobReport_>();
    	int i=0;
    	while(i<allJobs.size()) {
    		if(allJobs.get(i).user().compareTo(cmd[1])==0) {
    			if(allJobs.get(i).arrival_time()>=Integer.parseInt(cmd[2]) && (allJobs.get(i).arrival_time()<=Integer.parseInt(cmd[3]))){
    				arrJob.add(allJobs.get(i));
    			}
    			
    		}
    		i++;
    	}	
    	//int k=0;
    //	while(k<arrJob.size()) System.out.println(arrJob.get(k++).toString2());
        return arrJob;
    }

    private ArrayList<JobReport_> handle_new_project(String[] cmd) {
    	//System.out.println("Project query");
    	ArrayList<JobReport_> arrJob=new ArrayList<JobReport_>();
    	int i=0;
    	while(i<allJobs.size()) {
    		//System.out.println("okay");
    		//if(allJobs.get(i).arrival_time()==0) System.out.println("umm");
    		if(allJobs.get(i).project_name().compareTo(cmd[1])==0) {
    			if(allJobs.get(i).arrival_time()>=Integer.parseInt(cmd[2]) && (allJobs.get(i).arrival_time()<=Integer.parseInt(cmd[3]))){
    				arrJob.add(allJobs.get(i));
    			}
    			
    		}
    		i++;
    	}	
   // 	int k=0;
    //	while(k<arrJob.size()) System.out.println(arrJob.get(k++).toString2());
        return arrJob;
    }




    public void schedule() {
        execute_a_job();
    }

    private void execute_a_job() {
		handle_empty_line();
		
	}

	public void run_to_completion() {
    	while (jHeap.heap[0]!=null) {
    		System.out.println("Running code");
        	System.out.println("Remaining jobs: "+jHeap.curSize);
        	Job job=(Job) jHeap.extractMax();
        	while (job.project.budget < job.runtime)
				{
				job.ctime=0;
				System.out.println("Executing: "+job.jName+" from: "+job.project.pName);
				System.out.println("Un-sufficient budget.");
				unfinished.add(job);
				job = (Job) jHeap.extractMax();
				}
			System.out.println("Executing: "+job.jName+" from: "+job.project.pName);
			job.stat = status.COMPLETED;
			gtime = gtime + job.runtime;
			job.ctime = gtime;
			job.project.budget = job.project.budget - job.runtime;
			System.out.println("Project: "+job.project.pName+" budget remaining: "+job.project.budget);
			System.out.println("System execution completed");
			finished.add(job);
			//set consumed;
	    	job.user.cons+=job.runtime;
			
	}
    }

    public void print_stats() {
    	//Timer time=new Timer();
    	//time.start();
    	//long qstart_time = System.nanoTime();
    	System.out.println("--------------STATS---------------");
    	System.out.println("Total jobs done: "+finished.size());
    	int i=0;
    	while(i<finished.size()) {
    		System.out.println(finished.get(i).toString());
    		i++;
    	}
    	System.out.println("------------------------");
    	System.out.println("Unfinished jobs: ");
    	int j=0;
    	while(j<unfinished.size()) {
    		System.out.println(unfinished.get(j).toString());
    		j++;
    	}
    	System.out.println("Total unfinished jobs: "+unfinished.size());
    	System.out.println("--------------STATS DONE---------------");
    	//long qend_time = System.nanoTime();
    	//System.out.println("Time elapsed (ns): " + (qend_time - qstart_time));
    	//time.since();
    	//time.report("print");
    }

    public void handle_add(String[] cmd) {
    	System.out.println("ADDING Budget");
    	if (pTrie.search(cmd[1])!=null) {
			Project proj = (Project) pTrie.search(cmd[1]).value;
			proj.budget = proj.budget + Integer.parseInt(cmd[2]);
			int i = 0;
			while (i < unfinished.size()) {
				if (unfinished.get(i).project.budget >= unfinished.get(i).runtime) {
					jHeap.insert(unfinished.get(i));
					unfinished.remove(i);
					i--;
				}
				i++;
			} 
		}

    }

    public void handle_empty_line() {
    	System.out.println("Running code");
    	System.out.println("Remaining jobs: "+jHeap.curSize);
//    	int k=0;
//    	while(k<jHeap.curSize) System.out.println("ins"+((Job) jHeap.heap[k++].value).toString2());
    	Job job=(Job) jHeap.extractMax();
    	//System.out.println("fuckk");
    	//if(job==null) System.out.println("fuckk");
    	while (job!=null) {
			while (job.project.budget < job.runtime)
				{
				job.ctime=0;
				System.out.println("Executing: "+job.jName+" from: "+job.project.pName);
				System.out.println("Un-sufficient budget.");
				unfinished.add(job);
//				int m=0;
//		    	while(m<jHeap.curSize) System.out.println("ins"+((Job) jHeap.heap[m++].value).toString2());
				job = (Job) jHeap.extractMax();
				}
			System.out.println("Executing: "+job.jName+" from: "+job.project.pName);
			job.stat = status.COMPLETED;
			gtime = gtime + job.runtime;
			job.ctime = gtime;
			
			job.project.budget = job.project.budget - job.runtime;
			System.out.println("Project: "+job.project.pName+" budget remaining: "+job.project.budget);
//			int m=0;
//	    	while(m<jHeap.curSize) System.out.println("ins"+((Job) jHeap.heap[m++].value).toString2());
			System.out.println("Execution cycle completed");
			finished.add(job);
			//set consumed;
			job.user.cons+=job.runtime;
			return;
		}
    }


    public void handle_query(String key) {
    	System.out.println("Querying");
    	int i=0;
    	while(i<jHeap.curSize) {
    		if(jHeap.heap[i]!=null && ((Job)jHeap.heap[i].value).jName.compareTo(key)==0) {
    			
    			if(((Job)jHeap.heap[i].value).stat==status.REQUESTED) {
    				System.out.println(key+": NOT FINISHED");
    				return;
    			}
    			else System.out.println(key+": COMPLETED");
    			return;
    		}
    		i++;
    		
    	}
    	int k=0;
    	while(k<finished.size()) {
    		if(finished.get(k).jName.compareTo(key)==0) {
    			System.out.println(key+": COMPLETED");
    			return;
    		}
    		k++;
    	}
    	int j=0;
    	while(j<unfinished.size()) {
    		if(unfinished.get(j).jName.compareTo(key)==0) {
    			System.out.println(key+": NOT FINISHED");
				return;
    		}
    		j++;
    	}
    	System.out.println(key+": NO SUCH JOB");

    }

    public void handle_user(String name) {
    	User u=new User(name);
    	uList.add(u);
    	allUser.add(u);
    	System.out.println("Creating user");
    }

    public void handle_job(String[] cmd) {
    	System.out.println("Creating job");
    	Job j=new Job(cmd);
    	if(pTrie.search(cmd[2])==null) {
    		System.out.println("No such project exists. "+cmd[2]);
    		return;
    	}
    	else {
    		Project proj=(Project) (pTrie.search(cmd[2])).value;
    		j.project=proj;
    	}
    	
    	
		int index=0;
		while(index<uList.size()) {
			if(uList.get(index).uName.compareTo(cmd[3])==0) {
				User user=(User) uList.get(index);
				j.user=user;
				break;
			}
			index++;
			if(index==uList.size()) {
				System.out.println("No such user exists: "+cmd[3]); 
				return;
			}
		}
    	jHeap.insert(j);
    	j.number=aNumber++;
    	allJobs.add(j);
    	j.stat=status.REQUESTED;
    	int jAtime=gtime;
    	j.atime=jAtime;
    	//System.out.println(j.jName+"  "+j.atime); 
    	
    	
    }
    


    public void handle_project(String[] cmd) {
    	Project p=new Project(cmd);
    	pTrie.insert(p.pName, p);
    	System.out.println("Creating project");
    }

    public void execute_a_job(Job job) {
    	if(job.project.budget < job.runtime)
		{
		job.ctime=0;
		//System.out.println("Executing: "+job.jName+" from: "+job.project.pName);
		//System.out.println("Un-sufficient budget.");
		unfinished.add(job);
		}
    	else{
    	//System.out.println("Executing: "+job.jName+" from: "+job.project.pName);
		job.stat = status.COMPLETED;
		gtime = gtime + job.runtime;
		job.ctime = gtime;
		job.project.budget = job.project.budget - job.runtime;
		//System.out.println("Project: "+job.project.pName+" budget remaining: "+job.project.budget);
		//System.out.println("Execution cycle completed");
		finished.add(job);
		job.user.cons+=job.runtime;
		jHeap.remove(job);
//		int k=0;
//    	System.out.println("yup");
//    	while(k<jHeap.curSize) System.out.println("ins"+((Job)jHeap.heap[k++].value).toString2());
		}
    }
    
    public ArrayList<UserReport_> sort(ArrayList<UserReport_> list) {
    	if(list.size()==0 )  return null;
    	else if(list.size()==1 ) return list;
    	else {	int mid=list.size()/2;
    		ArrayList<UserReport_> left=new ArrayList<UserReport_>();
    		ArrayList<UserReport_> right=new ArrayList<UserReport_>();
    		for(int i=0;i<mid;i++) left.add(list.get(i));
    		for(int i=mid;i<list.size();i++) right.add(list.get(i));
    		sort(left);
    		sort(right);
    		merge(left,right,list);
    		return list;
    	}
    }
    
    public void merge(ArrayList<UserReport_> lhalf, ArrayList<UserReport_> rhalf, ArrayList<UserReport_> full){
    	int lcount=0, rcount=0, count=0;
    	while(lcount<lhalf.size() && rcount<rhalf.size()) {
    		if(lhalf.get(lcount).compareTo2(rhalf.get(rcount))>0) {
    			full.set(count, lhalf.get(lcount));
    			lcount++;
//    			int k=0;
//    			while(k<=count) System.out.println(full.get(k++).toString());
//    			System.out.println("hi");
    		}
    		else if( lhalf.get(lcount).compareTo2(rhalf.get(rcount))<=0){
    			full.set(count, rhalf.get(rcount));
    			rcount++;
//    			int k=0;
//    			while(k<=count) System.out.println(full.get(k++).toString());
//    			System.out.println("hi");
    		}
    		count++;
    	}
    	
    	ArrayList<UserReport_> rest;
        int restIndex;
        if (lcount >= lhalf.size()) {
            // The left ArrayList has been use up...
            rest = rhalf;
            restIndex = rcount;
        } else {
            // The right ArrayList has been used up...
            rest = lhalf;
            restIndex = lcount;
        }
 
        // Copy the rest of whichever ArrayList (left or right) was not used up.
        for (int i=restIndex; i<rest.size(); i++) {
           full.set(count, rest.get(i));
            count++;
        }
    
    }
   
}
