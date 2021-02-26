package ProjectManagement;

import java.io.*;
import java.net.URL;
import java.util.LinkedList;

import PriorityQueue.MaxHeap;
import ProjectManagement.Job.status;
import Trie.Trie;

public class Scheduler_Driver extends Thread implements SchedulerInterface {


    public static void main(String[] args) throws IOException {
        Scheduler_Driver scheduler_driver = new Scheduler_Driver();
        scheduler_driver.execute();
    }

    public void execute() throws IOException {


        File file;
        URL url = Scheduler_Driver.class.getResource("INP");
        file = new File(url.getPath());

        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(file));
        } catch (FileNotFoundException e) {
            System.err.println("Input file Not found");
        }
        String st;
        while ((st = br.readLine()) != null) {
            String[] cmd = st.split(" ");
            if (cmd.length == 0) {
                System.err.println("Error parsing: " + st);
                return;
            }

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
                case "":
                    handle_empty_line();
                    break;
                case "ADD":
                    handle_add(cmd);
                    break;
                default:
                    System.err.println("Unknown command: " + cmd[0]);
            }
        }


        run_to_completion();

        print_stats();

    }


    Trie pTrie=new Trie<>();
    MaxHeap jHeap=new MaxHeap();
    LinkedList<User> uList=new LinkedList<User>();
    LinkedList<Job> finished=new LinkedList<Job>();
    LinkedList<Job> unfinished=new LinkedList<Job>();
    public int gtime;
    
    @Override
    public void run() {
        // till there are JOBS
        schedule();
    }


    @Override
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
			
	}
    }

    

    @Override
    public void handle_project(String[] cmd) {
    	Project p=new Project(cmd);
    	pTrie.insert(p.pName, p);
    	System.out.println("Creating project");
    }

    @Override
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
    	j.stat=status.REQUESTED;
    	
    }

    @Override
    public void handle_user(String name) {
    	User u=new User(name);
    	uList.add(u);
    	System.out.println("Creating user");
    }

    @Override
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

    @Override
    public void handle_empty_line() {
    	System.out.println("Running code");
    	System.out.println("Remaining jobs: "+jHeap.curSize);
    	Job job=(Job) jHeap.extractMax();
    	while (job!=null) {
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
			System.out.println("Execution cycle completed");
			finished.add(job);
			return;
		}
    	}

    @Override
    public void handle_add(String[] cmd) {
    	System.out.println("ADDING Budget");
    	Project proj=(Project)pTrie.search(cmd[1]).value;
    	proj.budget=proj.budget+Integer.parseInt(cmd[2]);
    	int i=0;
    	while(i<unfinished.size()) {
    		if(unfinished.get(i).project.budget >= unfinished.get(i).runtime) {
    			jHeap.insert(unfinished.get(i));
    			unfinished.remove(i);
    			i--;
    		}
    		i++;
    	}
    }

    @Override
    public void print_stats() {
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
    }

    @Override
    public void schedule() {
    	Job job=(Job) jHeap.extractMax();
				while (job!=null && job.project.budget < job.runtime) {
					job.ctime = 0;
					System.out.println("Executing: " + job.jName + " from: " + job.project.pName);
					System.out.println("Un-sufficient budget.");
					unfinished.add(job);
					job = (Job) jHeap.extractMax();
				}
				System.out.println("Executing: " + job.jName + " from: " + job.project.pName);
				job.stat = status.COMPLETED;
				gtime = gtime + job.runtime;
				job.ctime = gtime;
				job.project.budget = job.project.budget - job.runtime;
				System.out.println("Project: " + job.project.pName + " budget remaining: " + job.project.budget);
				System.out.println("Execution cycle completed");
				finished.add(job);
		}
    
}
