package ProjectManagement;
import Trie.Trie;;

public class Project {
	public String pName;
	public String priority;
	public int budget;
	
	
	
	Project(String[] cmd){
		this.pName=cmd[1];
		this.budget=Integer.parseInt(cmd[3]);
		this.priority=cmd[2];
		
	}
	
	
}
