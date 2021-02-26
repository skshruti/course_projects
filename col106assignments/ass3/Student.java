//package assignment3;

public class Student implements Student_ {
	public String fname;
	public String lname;
	public String hostel;
	public String department;
	public String cgpa;
	
	
	public Student(String fname, String lname, String hostel, String department, String cgpa) {
		this.fname = fname;
		this.lname = lname;
		this.hostel= hostel;
		this.department=department;
		this.cgpa = cgpa;
	}
	
	public Pair<String, String> pair(){
		Pair<String, String> pair=new Pair<>(fname, lname);
		return pair;
	}
	
	public String getData() {
		return (fname+" "+lname+" "+hostel+" "+department+" "+cgpa);
	}
	
	public String fname() {
		return this.fname;
	}

	public String lname() {
		return this.lname;
	}

	public String hostel() {
		return this.hostel;
	}

	public String department() {
		return this.department;
	}

	public String cgpa() {
		return this.cgpa;
	}
	


}
