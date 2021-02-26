
public class triangle extends Shape implements TriangleInterface, Comparable<triangle>{
	PointInterface[] points;
	EdgeInterface[] edges;
	int count;
	boolean visited;
	triangle(PointInterface[] arr){
		this.points=arr;
		PointInterface[] e1 = new PointInterface[] {arr[0], arr[1]};
		EdgeInterface edge1=new edge(e1);
		PointInterface[] e2 = new PointInterface[] {arr[1], arr[2]};
		EdgeInterface edge2=new edge(e2);
		PointInterface[] e3 = new PointInterface[] {arr[2], arr[0]};
		EdgeInterface edge3=new edge(e3);
		EdgeInterface[] earr=new EdgeInterface[] {edge1, edge2, edge3};
		this.edges=earr;
		this.count=-1;
		this.visited=false;
	} 
	@Override
	public PointInterface[] triangle_coord() {
		return this.points;
	}
	@Override
	public int compareTo(triangle o) {
		if(this.toString().compareTo(o.toString())>0) return 1;
		else if(this.toString().compareTo(o.toString())<0) return -1;
		else return 0;
	}
	
	public String toString() {
		String s="";
		point p1=(point) this.triangle_coord()[0];
		point p2=(point) this.triangle_coord()[1];
		point p3=(point) this.triangle_coord()[2];
		if(p1.compareTo(p2)<=0 && p2.compareTo(p3)<=0 ) s=p1.toString()+";"+p2.toString()+";"+p3.toString();
		else if(p1.compareTo(p3)<=0 && p3.compareTo(p2)<=0 ) s=p1.toString()+";"+p3.toString()+";"+p2.toString();
		else if(p2.compareTo(p1)<=0 && p1.compareTo(p3)<=0 ) s=p2.toString()+";"+p1.toString()+";"+p3.toString();
		else if(p2.compareTo(p3)<=0 && p3.compareTo(p1)<=0 ) s=p2.toString()+";"+p3.toString()+";"+p1.toString();
		else if(p3.compareTo(p1)<=0 && p1.compareTo(p2)<=0 ) s=p3.toString()+";"+p1.toString()+";"+p2.toString();
		else if(p3.compareTo(p2)<=0 && p2.compareTo(p1)<=0 ) s=p3.toString()+";"+p2.toString()+";"+p1.toString();
		return s;
	}

}
