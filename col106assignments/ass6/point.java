
public class point implements PointInterface, Comparable<point>{
	float x;
	float y;
	float z;
	point(float x, float y, float z){
		this.x=x;
		this.y=y;
		this.z=z;
	}
	@Override
	public float getX() {
		// TODO Auto-generated method stub
		return this.x;
	}

	@Override 
	public float getY() {
		// TODO Auto-generated method stub
		return this.y;
	}

	@Override
	public float getZ() {
		// TODO Auto-generated method stub
		return this.z;
	}

	@Override
	public float[] getXYZcoordinate() {
		// TODO Auto-generated method stub
		float[] arr = new float[2];
		arr[0]=this.x;
		arr[1]=this.y;
		arr[2]=this.z;
		return arr;
	}
	@Override
	public int compareTo(point o) {
		if(this.getX()>o.getX()) return 1;
		else if(this.getX()<o.getX()) return -1;
		else if(this.getX()==o.getX()) {
			if(this.getY()>o.getY()) return 1;
			else if(this.getY()<o.getY()) return -1;
			else if(this.getY()==o.getY()) {
				if(this.getZ()>o.getZ()) return 1;
				else if(this.getZ()<o.getZ()) return -1;
				else if(this.getZ()==o.getZ()) return 0;
			}
		}
		return 0;
	}
	
	public String toString() {
		return ("("+this.getX()+", "+this.getY()+" ,"+this.getZ()+")");
	}
	
}
