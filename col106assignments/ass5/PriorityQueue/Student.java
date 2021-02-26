package PriorityQueue;

public class Student implements Comparable<Student> {
    public String name;
    public Integer marks;
   // public int number;

    public Student(String trim, int parseInt) {
    	name=trim;
    	marks=parseInt;
    }
    
    public String toString() {
    	return ("Student{name='"+this.name+"', marks="+this.marks+"}");
    }

    @Override
    public int compareTo(Student student) {
        if(this.marks>student.marks) return 1;
        else if(this.marks<student.marks) return -1;
        else return 0;
    }

    public String getName() {
        return name;
    }
    
    

	//public int number() {
		
		//return number;
	//}
    
    
}
