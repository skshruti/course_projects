
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;


public class Assignment3 {
	public static void main(String[] args) throws Exception {
		MyHashTable_<Pair<String, String>, Student> hTable=null;
		if(args[1].equals("DH")) {
			hTable=new DoubleHashing_<Pair<String, String>, Student>(Integer.parseInt(args[0]));
		}
		else if(args[1].equals("SCBST")) {
			hTable=new SeparateChaining_<Pair<String, String>, Student>(Integer.parseInt(args[0]));
		}
		
		BufferedReader reader;
	    reader = new BufferedReader(new FileReader(args[2]));
        String  line = reader.readLine();
	    while (line != null) {
		String[] tokens = line.split(" ");
	    if(tokens.length!=0) {
		if(tokens[0].equalsIgnoreCase("insert")) {
	    	String fname=tokens[1]; 
	    	String lname=tokens[2]; 
	    	String hostel=tokens[3]; 
	    	String department=tokens[4]; 
	    	String cgpa=tokens[5] ;
	    	//System.out.print(S);
	    	Student S= new Student(fname, lname, hostel, department, cgpa);
	    	//System.out.print(S);
	    	Pair<String, String> pair=new Pair<>(fname, lname);
	    	System.out.println(hTable.insert(pair, S));
	    	}
	    
	    else if(tokens[0].equalsIgnoreCase("update")) {
	    	String fname=tokens[1]; 
	    	String lname=tokens[2]; 
	    	String hostel=tokens[3]; 
	    	String department=tokens[4]; 
	    	String cgpa=tokens[5] ; 
	    	if(!hTable.contains(new Pair<String,String>(fname,lname))) {
	    		System.out.println("E");
	    	}
	    	else{
	    		Student S= new Student(fname, lname, hostel, department, cgpa);
	    	Pair<String, String> pair=new Pair<>(fname, lname);
	    	System.out.println(hTable.update(pair, S));
	    	}
	    	}
	    else if(tokens[0].equalsIgnoreCase("delete")) {
	    	String fname=tokens[1]; 
	    	String lname=tokens[2]; 
	    	Pair<String, String> pair=new Pair<>(fname, lname);
	    	if(!hTable.contains(pair)) {
	    		System.out.println("E");
	    	}
	    	else {
	    		System.out.println(hTable.delete(pair));
	    	}
	    }
	    else if(tokens[0].equalsIgnoreCase("contains")) {
	    	String fname=tokens[1]; 
	    	String lname=tokens[2]; 
	    	Pair<String, String> pair=new Pair<>(fname, lname);
	    	if(hTable.contains(pair))System.out.println("T");
	    	else System.out.println("F");
	    }
	    else if(tokens[0].equalsIgnoreCase("get")) {
	    	String fname=tokens[1]; 
	    	String lname=tokens[2]; 
	    	Pair<String, String> pair=new Pair<>(fname, lname);
	    	if(!hTable.contains(pair))System.out.println("E");
	    	else 
	    	System.out.println(hTable.get(pair));
	    }
	    else if(tokens[0].equalsIgnoreCase("address")) {
	    	String fname=tokens[1]; 
	    	String lname=tokens[2]; 
	    	Pair<String, String> pair=new Pair<>(fname, lname);
	    	if(!hTable.contains(pair))System.out.println("E");
	    	else 
	    	System.out.println(hTable.address(pair));
	    }
	    line = reader.readLine();
	    }
	    }
	  	
	
	}
}
