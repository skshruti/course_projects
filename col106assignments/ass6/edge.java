
public class edge extends Shape implements EdgeInterface, Comparable<edge>{
	//[(x1,y1,z1),(x2,y2,z2)]
	// 2 points for an edge which can be in any order
	PointInterface[] arr;
	edge(PointInterface[] arr){
		this.arr=arr;
	}
	
	public float power(float m, int n) {
        if (n != 0)
            return (m * power(m, n - 1));
        else
            return 1;
    }
	public PointInterface[] edgeEndPoints() {
		// TODO Auto-generated method stub
		return this.arr;
	}

	public float min(float a, float b) {
		if(a<=b) return a;
		else return b;
	}
	
	public float max(float a, float b) {
		if(a>b) return a;
		else return b;
	}
	
	public float eLength() {
		float xd=(this.arr[1].getX()-this.arr[0].getX());
		float yd=(this.arr[1].getY()-this.arr[0].getY());
		float zd=(this.arr[1].getZ()-this.arr[0].getZ());
		float result=power(xd,2)+power(yd,2)+power(zd,2);
		return result;
	}
	
	public String toString() {
		return ("[("+this.arr[0].getX()+","+this.arr[0].getY()+","+this.arr[0].getZ()+"),("+this.arr[1].getX()+","+this.arr[1].getY()+","+this.arr[1].getZ()+")]");
	}
	
	
	
	public int compareTo(edge edge) {
			PointInterface[] arr1 = this.arr;
			PointInterface[] arr2 = edge.arr;
			float minx1 = min(arr1[0].getX(), arr1[1].getX());
			float miny1 = min(arr1[0].getY(), arr1[1].getY());
			float minz1 = min(arr1[0].getZ(), arr1[1].getZ());
			float minx2 = min(arr2[0].getX(), arr2[1].getX());
			float miny2 = min(arr2[0].getY(), arr2[1].getY());
			float minz2 = min(arr2[0].getZ(), arr2[1].getZ());
			float maxx1 = max(arr1[0].getX(), arr1[1].getX());
			float maxy1 = max(arr1[0].getY(), arr1[1].getY());
			float maxz1 = max(arr1[0].getZ(), arr1[1].getZ());
			float maxx2 = max(arr2[0].getX(), arr2[1].getX());
			float maxy2 = max(arr2[0].getY(), arr2[1].getY());
			float maxz2 = max(arr2[0].getZ(), arr2[1].getZ());
			if (minx1 > minx2)
				return 1;
			else if (minx1 < minx2)
				return -1;
			else {
				if (maxx1 > maxx2)
					return 1;
				else if (maxx1 < maxx2)
					return -1;
				else {
					if (miny1 > miny2)
						return 1;
					else if (miny1 < miny2)
						return -1;
					else {
						if (maxy1 > maxy2)
							return 1;
						else if (maxy1 < maxy2)
							return -1;
						else {
							if (minz1 > minz2)
								return 1;
							else if (minz1 < minz2)
								return -1;
							else {
								if (maxz1 > maxz2)
									return 1;
								else if (maxz1 < maxz2)
									return -1;
								else
									return 0;
							}
						}
					}
				}
			}
		
		
	}
} 
