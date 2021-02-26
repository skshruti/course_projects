import LinkedList.LinkedList;
import LinkedList.Node;
import RedBlack.RBTree;
import RedBlack.RedBlackNode;

public class Shape implements ShapeInterface
{	
	RBTree<String, triangle> allTri=new RBTree<String, triangle>();
	RBTree<edge, triangle> allEdges=new RBTree<edge, triangle>();
	RBTree<point, edge> allPoiEdg=new RBTree<point, edge>();
	LinkedList<triangle> allTriangle=new LinkedList<triangle>();
	
	
	//INPUT [x1,y1,z1,x2,y2,z2,x3,y3,z3]
	 public boolean ADD_TRIANGLE(float [] triangle_coord){
		 if((triangle_coord[3]-triangle_coord[0])/(triangle_coord[6]-triangle_coord[0])==
				 (triangle_coord[4]-triangle_coord[1])/(triangle_coord[7]-triangle_coord[1]) && 
				 (triangle_coord[4]-triangle_coord[1])/(triangle_coord[7]-triangle_coord[1])==
				 	(triangle_coord[5]-triangle_coord[2])/(triangle_coord[8]-triangle_coord[2]))
		 return false;
		 else {
			 PointInterface p1=new point(triangle_coord[0],triangle_coord[1],triangle_coord[2]);
			 PointInterface p2=new point(triangle_coord[3],triangle_coord[4],triangle_coord[5]);
			 PointInterface p3=new point(triangle_coord[6],triangle_coord[7],triangle_coord[8]);
			 PointInterface[] setPoints=new PointInterface[] {p1, p2, p3};
			 TriangleInterface newT=new triangle(setPoints);
			 allEdges.insert((edge) ((triangle) newT).edges[0],(triangle) newT);
			 allEdges.insert( (edge) ((triangle) newT).edges[1],(triangle) newT);
			 allEdges.insert((edge) ((triangle) newT).edges[2],(triangle) newT);
			 allPoiEdg.insert((point) p1, (edge) ((triangle) newT).edges[0]);
			 allPoiEdg.insert((point) p1, (edge) ((triangle) newT).edges[2]);
			 allPoiEdg.insert((point) p2, (edge) ((triangle) newT).edges[0]);
			 allPoiEdg.insert((point) p2, (edge) ((triangle) newT).edges[1]);
			 allPoiEdg.insert((point) p3, (edge) ((triangle) newT).edges[1]);
			 allPoiEdg.insert((point) p3, (edge) ((triangle) newT).edges[2]);
//			 printPreorder(allPoiEdg.root) ;
			 allTri.insert(newT.toString(),(triangle) newT);
			 allTriangle.add((triangle) newT);
//			 System.out.println(allTri.size);
			 return true;
		 }
		 }

	 public int TYPE_MESH(){
		if(allEdges.root.key!=null) {
			LinkedList<RedBlackNode<edge, triangle>> nList=new LinkedList<RedBlackNode<edge, triangle>>();
			int result=1;
			nList.add(allEdges.root);
			RedBlackNode<edge, triangle> n=new RedBlackNode<edge, triangle>();
			n=nList.get(0); 
			while(n!=null ) {
				if(n==null) {break;}
				if((int)n.getValues().size()>2) {
				//	System.out.println(3); 
					return 3;}
				else if((int)n.getValues().size()==1) {
					result=2;
					nList.remove();
				} 
				else {
					nList.remove();
				}
				
				if(n.left!=null && n.left.key!=null) {
					nList.add(n.left);
				}
				if(n.right!=null && n.right.key!=null) {
					nList.add(n.right);
				}
				n=nList.get(0); 
			}
			return result;
		}
		else return 0;
		}
 
	 public int COUNT_CONNECTED_COMPONENTS(){
		 LinkedList<LinkedList<triangle>> list=new LinkedList<LinkedList<triangle>>();
		 int index=0;
		 allTriangle.get(index).count=list.size();
		 LinkedList<triangle> headList=new LinkedList<triangle>();
		 list.add(headList);
		 headList.add(allTriangle.get(index));
		 while(index<allTriangle.size()) {
			 int i=0;
			 while (i<list.size()) {
				 int j=0;
				while (j < list.get(i).size()) {
					if (shareEdge(allTriangle.get(index), list.get(i).get(j)) && allTriangle.get(index).count==-1) {
						list.get(i).add(allTriangle.get(index));
						allTriangle.get(index).count=i;
						break;
						}
					if(allTriangle.get(index).count!=-1) j=list.get(i).size();
						j++;
					} 
				if(allTriangle.get(index).count!=-1) i=list.size();
					i++;
			 	}
			 if(allTriangle.get(index).count==-1) {
				 allTriangle.get(index).count=list.size();
				 LinkedList<triangle> nList=new LinkedList<triangle>();
				 list.add(nList);
				 nList.add(allTriangle.get(index));
			 }
			 index++;
		 }
	//	 System.out.println(list.size());
		 int i=0;
		 while(i<list.size()) {
			// System.out.println(list.get(i).size());
			 int j=0;
			 while(j<list.get(i).size()) {
				 list.get(i).get(j).count=-1;
				 j++;
				// System.out.println(list.get(i).get(j++));
			 }
			 i++;
		 }
//		 System.out.println(list.size());
		 return list.size();
		 }
	
/*	 public void printPreorder(RedBlackNode node) 
	    { 
	        if (node == null) 
	            return; 
	       if(node.getValues()!=null) {
	    	   System.out.print(node.getValues().size() + " "); 
	    	   int index=0;
	    	   while(index<node.getValues().size()) {
	  			System.out.println(node.getValues().get(index++)+"hi");
	  			 
	  		 }
	       }
	       if(node.left!=null) {
	    	   System.out.println("left");
	    	   printPreorder(node.left); 
	       }
	       if(node.right!=null) {
	    	   System.out.println("right");
	    	   printPreorder(node.right); 
	       }
	    }
*/
	 
	 public EdgeInterface[] BOUNDARY_EDGES(){
		 LinkedList<edge> list=new LinkedList<edge>();
			if(allEdges.root.key!=null) {
				LinkedList<RedBlackNode<edge, triangle>> nList=new LinkedList<RedBlackNode<edge, triangle>>();
				nList.add(allEdges.root);
				RedBlackNode<edge, triangle> n=new RedBlackNode<edge, triangle>();
				n=nList.get(0); 
				while(n!=null ) {
					if((int)n.getValues().size()==1 && n.key!=null) {
						list.add(n.key);
					}
					nList.remove();
					if(n.left!=null && n.left.key!=null) { 
						nList.add(n.left);
					}
					if(n.right!=null && n.right.key!=null ) {
						nList.add(n.right);
					}
					n=nList.get(0);
				}
				if(list.size()==0) return null;
				EdgeInterface[] array = new EdgeInterface[list.size()];
				
				int hi=0;
				while(hi<list.size()) {
					array[hi]=list.get(hi);
//					System.out.println(array[hi]);
					hi++;
				}
				sort(array);
				int hii=0;
				while(hii<list.size()) {
					System.out.println(array[hii]);
					hii++;
				}
				
				return array;
			}
			else return null;
		 }

	 @SuppressWarnings("unchecked")
	public boolean shareEdge(triangle t1, triangle t2) {
			 if(((Comparable<edge>) t1.edges[0]).compareTo((edge) t2.edges[0])==0) return true;
			 else if(((Comparable<edge>) t1.edges[0]).compareTo((edge) t2.edges[1])==0) return true;
			 else if(((Comparable<edge>) t1.edges[0]).compareTo((edge) t2.edges[2])==0) return true;
			 else if(((Comparable<edge>) t1.edges[1]).compareTo((edge) t2.edges[0])==0) return true;
			 else if(((Comparable<edge>) t1.edges[1]).compareTo((edge) t2.edges[1])==0) return true;
			 else if(((Comparable<edge>) t1.edges[1]).compareTo((edge) t2.edges[2])==0) return true;
			 else if(((Comparable<edge>) t1.edges[2]).compareTo((edge) t2.edges[0])==0) return true;
			 else if(((Comparable<edge>) t1.edges[2]).compareTo((edge) t2.edges[1])==0) return true;
			 else if(((Comparable<edge>) t1.edges[2]).compareTo((edge) t2.edges[2])==0) return true;
			 else return false;
		 }

	//INPUT [x1,y1,z1,x2,y2,z2,x3,y3,z3]
	 public TriangleInterface [] NEIGHBORS_OF_TRIANGLE(float [] triangle_coord){
		 LinkedList<triangle> list=new LinkedList<triangle>();
		 PointInterface p1=new point(triangle_coord[0],triangle_coord[1],triangle_coord[2]);
		 PointInterface p2=new point(triangle_coord[3],triangle_coord[4],triangle_coord[5]);
		 PointInterface p3=new point(triangle_coord[6],triangle_coord[7],triangle_coord[8]);
		 PointInterface[] setPoints=new PointInterface[] {p1, p2, p3};
		 TriangleInterface newT=new triangle(setPoints);
		 RedBlackNode<String, triangle> node=allTri.search(newT.toString());
		 if(node==null) return null;
		 triangle tri=node.getValue();
		 int index=0;
		 while(index<allTriangle.size()) {
			 if(tri.compareTo(allTriangle.get(index))!=0) {
				 if(shareEdge(tri, allTriangle.get(index))) list.add(allTriangle.get(index));
			 }
			 index++;
		 }
		 TriangleInterface [] arr=new TriangleInterface[list.size()]; 
		 int hi=0;
			while(hi<list.size()) {
				arr[hi]=list.get(hi);
				System.out.println(arr[hi]);
				hi++;
			}
		 return arr;
		 }

	 
	//INPUT [x1,y1,z1,x2,y2,z2,x3,y3,z3]
	 public EdgeInterface [] EDGE_NEIGHBOR_TRIANGLE(float [] triangle_coord){
		 PointInterface p1=new point(triangle_coord[0],triangle_coord[1],triangle_coord[2]);
		 PointInterface p2=new point(triangle_coord[3],triangle_coord[4],triangle_coord[5]);
		 PointInterface p3=new point(triangle_coord[6],triangle_coord[7],triangle_coord[8]);
		 PointInterface[] setPoints=new PointInterface[] {p1, p2, p3};
		 TriangleInterface newT=new triangle(setPoints);
		 RedBlackNode<String, triangle> node=allTri.search(newT.toString());
		 if(node==null) return null;
		 int hi=0;
			while(hi<node.getValue().edges.length) System.out.println(node.getValue().edges[hi++]);
		 return node.getValue().edges;
		 }

	//INPUT [x1,y1,z1,x2,y2,z2,x3,y3,z3]
	 public PointInterface [] VERTEX_NEIGHBOR_TRIANGLE(float [] triangle_coord){
		 PointInterface p1=new point(triangle_coord[0],triangle_coord[1],triangle_coord[2]);
		 PointInterface p2=new point(triangle_coord[3],triangle_coord[4],triangle_coord[5]);
		 PointInterface p3=new point(triangle_coord[6],triangle_coord[7],triangle_coord[8]);
		 PointInterface[] setPoints=new PointInterface[] {p1, p2, p3};
		 TriangleInterface newT=new triangle(setPoints);
		 RedBlackNode<String, triangle> node=allTri.search(newT.toString());
		 if(node==null) return null;
		 int hi=0;
			while(hi<node.getValue().points.length) System.out.println(node.getValue().points[hi++]);
		 return node.getValue().points;
	 }
	 
	 @SuppressWarnings("unchecked")
	public boolean shareVertex(triangle t1, triangle t2) {
		 if( ((Comparable<point>) t1.points[0]).compareTo( (point) t2.points[0])==0) return true;
		 else if(((Comparable<point>) t1.points[0]).compareTo((point) t2.points[1])==0) return true;
		 else if(((Comparable<point>) t1.points[0]).compareTo((point) t2.points[2])==0) return true;
		 else if(((Comparable<point>) t1.points[1]).compareTo((point) t2.points[0])==0) return true;
		 else if(((Comparable<point>) t1.points[1]).compareTo((point) t2.points[1])==0) return true;
		 else if(((Comparable<point>) t1.points[1]).compareTo((point) t2.points[2])==0) return true;
		 else if(((Comparable<point>) t1.points[2]).compareTo((point) t2.points[0])==0) return true;
		 else if(((Comparable<point>) t1.points[2]).compareTo((point) t2.points[1])==0) return true;
		 else if(((Comparable<point>) t1.points[2]).compareTo((point) t2.points[2])==0) return true;
		 else return false;
	 } 

	//INPUT [x1,y1,z1,x2,y2,z2,x3,y3,z3]
	 public TriangleInterface [] EXTENDED_NEIGHBOR_TRIANGLE(float [] triangle_coord){
		 LinkedList<triangle> list=new LinkedList<triangle>();
		 PointInterface p1=new point(triangle_coord[0],triangle_coord[1],triangle_coord[2]);
		 PointInterface p2=new point(triangle_coord[3],triangle_coord[4],triangle_coord[5]);
		 PointInterface p3=new point(triangle_coord[6],triangle_coord[7],triangle_coord[8]);
		 PointInterface[] setPoints=new PointInterface[] {p1, p2, p3};
		 TriangleInterface newT=new triangle(setPoints);
		 RedBlackNode<String, triangle> node=allTri.search(newT.toString());
		 if(node==null) return null;
		 triangle tri=node.getValue();
		 int index=0;
		 while(index<allTriangle.size()) {
			 if(tri.compareTo(allTriangle.get(index))!=0) {
				 if(shareVertex(tri, allTriangle.get(index))) list.add(allTriangle.get(index));
			 }
			 index++;
		 }
		 TriangleInterface [] arr=new TriangleInterface[list.size()]; 
		 int hi=0;
			while(hi<list.size()) {
				arr[hi]=list.get(hi);
				System.out.println(arr[hi]);
				hi++;
			}
		 return arr;
		 }


	//INPUT [x,y,z]
	 @SuppressWarnings("unchecked")
	public TriangleInterface [] INCIDENT_TRIANGLES(float [] point_coordinates){
		 LinkedList<triangle> list=new LinkedList<triangle>();
		 PointInterface p=new point(point_coordinates[0],point_coordinates[1],point_coordinates[2]);
		 int index=0;
		 while(index<allTriangle.size()) {
			 if(((Comparable<point>) allTriangle.get(index).points[0]).compareTo((point) p)==0 ||
					 ((Comparable<point>) allTriangle.get(index).points[1]).compareTo((point) p)==0 || 
					 	((Comparable<point>) allTriangle.get(index).points[2]).compareTo((point) p)==0) {
				list.add(allTriangle.get(index));
			 }
			 index++;
		 }
		 TriangleInterface [] arr=new TriangleInterface[list.size()]; 
		 int hi=0;
			while(hi<list.size()) {
				arr[hi]=list.get(hi);
				System.out.println(arr[hi]);
				hi++;
			}
		 return arr;
		 }


	// INPUT [x,y,z]
	 public PointInterface [] NEIGHBORS_OF_POINT(float [] point_coordinates){
		 LinkedList<point> list=new LinkedList<point>();
		 PointInterface p=new point(point_coordinates[0],point_coordinates[1],point_coordinates[2]);
		 RedBlackNode<point, edge> node=allPoiEdg.search((point) p);
		 if(node==null) return null;
		 int index=0;
		 while(index<node.getValues().size()) {
			 if(((point) node.getValues().get(index).edgeEndPoints()[0]).compareTo((point) p)==0)
				 list.add((point) node.getValues().get(index++).edgeEndPoints()[1]);
			 else
				 list.add((point) node.getValues().get(index++).edgeEndPoints()[0]);
		 }
		 PointInterface [] arr=new PointInterface[list.size()]; 
		 int hi=0;
			while(hi<list.size()) {
				arr[hi]=list.get(hi);
				System.out.println(arr[hi]);
				hi++;
			}
		 return arr;
		 }

	// INPUT[x,y,z]
	 public EdgeInterface [] EDGE_NEIGHBORS_OF_POINT(float [] point_coordinates){
		 LinkedList<edge> list=new LinkedList<edge>();
		 PointInterface p=new point(point_coordinates[0],point_coordinates[1],point_coordinates[2]);
		 RedBlackNode<point, edge> node=allPoiEdg.search((point) p);
		 if(node==null) return null;
		 int index=0;
		 while(index<node.getValues().size()) {
			 list.add(node.getValues().get(index++));
		 }
		 EdgeInterface [] arr=new EdgeInterface[list.size()]; 
		 int hi=0;
			while(hi<list.size()) {
				arr[hi]=list.get(hi);
				System.out.println(arr[hi]);
				hi++;
			}
		 return arr;
		 }


	// INPUT[x,y,z]
	 @SuppressWarnings("unchecked")
	public TriangleInterface [] FACE_NEIGHBORS_OF_POINT(float [] point_coordinates){
		 LinkedList<triangle> list=new LinkedList<triangle>();
		 PointInterface p=new point(point_coordinates[0],point_coordinates[1],point_coordinates[2]);
		 int index=0;
		 while(index<allTriangle.size()) {
			 if(((Comparable<point>) allTriangle.get(index).points[0]).compareTo((point) p)==0 ||
					 ((Comparable<point>) allTriangle.get(index).points[1]).compareTo((point) p)==0 || 
					 	((Comparable<point>) allTriangle.get(index).points[2]).compareTo((point) p)==0) {
				list.add(allTriangle.get(index));
			 }
			 index++;
		 }
		 TriangleInterface [] arr=new TriangleInterface[list.size()]; 
		 int hi=0;
			while(hi<list.size()) {
				arr[hi]=list.get(hi);
				System.out.println(arr[hi]);
				hi++;
			}
		 return arr;
		 }



	// INPUT // [xa1,ya1,za1,xa2,ya2,za2,xa3,ya3,za3 , xb1,yb1,zb1,xb2,yb2,zb2,xb3,yb3,zb3]   where xa1,ya1,za1,xa2,ya2,za2,xa3,ya3,za3 are 3 coordinates of first triangle and xb1,yb1,zb1,xb2,yb2,zb2,xb3,yb3,zb3 are coordinates of second triangle as given in specificaition.

	 public boolean IS_CONNECTED(float [] triangle_coord_1, float [] triangle_coord_2){
		 PointInterface p11=new point(triangle_coord_1[0],triangle_coord_1[1],triangle_coord_1[2]);
		 PointInterface p12=new point(triangle_coord_1[3],triangle_coord_1[4],triangle_coord_1[5]);
		 PointInterface p13=new point(triangle_coord_1[6],triangle_coord_1[7],triangle_coord_1[8]);
		 PointInterface[] setPoints1=new PointInterface[] {p11, p12, p13};
		 TriangleInterface T1=new triangle(setPoints1);
		 PointInterface p21=new point(triangle_coord_2[0],triangle_coord_2[1],triangle_coord_2[2]);
		 PointInterface p22=new point(triangle_coord_2[3],triangle_coord_2[4],triangle_coord_2[5]);
		 PointInterface p23=new point(triangle_coord_2[6],triangle_coord_2[7],triangle_coord_2[8]);
		 PointInterface[] setPoints2=new PointInterface[] {p21, p22, p23};
		 TriangleInterface T2=new triangle(setPoints2);
		 CONNECTED_COMPONENTS();
		 LinkedList<LinkedList<triangle>> list=CONNECTED_COMPONENTS();
//		 System.out.println(list.size());
		 int i=0;
		 while(i<list.size()) {
		//	 System.out.println(list.get(i).size());
			 int j=0;
			 while(j<list.get(i).size()) {
		//		 System.out.println(list.get(i).get(j++));
				 j++;
			 }
			 i++;
		 }
		 int index=0;
		 while(index<list.size()) {
			 if(list.get(index).contains((triangle) T1) && list.get(index).contains((triangle) T2)) return true;
			 index++;
		 }
		 return false;
		 }


	// INPUT [x1,y1,z1,x2,y2,z2] // where (x1,y1,z1) refers to first end point of edge and  (x2,y2,z2) refers to the second.
	 @SuppressWarnings("unchecked")
	public TriangleInterface [] TRIANGLE_NEIGHBOR_OF_EDGE(float [] edge_coordinates){
		 LinkedList<triangle> list=new LinkedList<triangle>();
		 PointInterface p1=new point(edge_coordinates[0],edge_coordinates[1],edge_coordinates[2]);
		 PointInterface p2=new point(edge_coordinates[3],edge_coordinates[4],edge_coordinates[5]);
		 PointInterface[] setPoints=new PointInterface[] {p1, p2};
		 EdgeInterface edge=new edge(setPoints);int index=0;
		 while(index<allTriangle.size()) {
			 if(((Comparable<edge>) allTriangle.get(index).edges[0]).compareTo((edge) edge)==0 ||
					 ((Comparable<edge>) allTriangle.get(index).edges[1]).compareTo((edge) edge)==0 || 
							 ((Comparable<edge>) allTriangle.get(index).edges[2]).compareTo((edge) edge)==0) {
				list.add(allTriangle.get(index));
			 }
			 index++;
		 }
		 TriangleInterface [] arr=new TriangleInterface[list.size()]; 
		 int hi=0;
			while(hi<list.size()) {
				arr[hi]=list.get(hi);
				System.out.println(arr[hi]);
				hi++;
			}
		 return arr;
		 }


	 public int MAXIMUM_DIAMETER(){
		 LinkedList<LinkedList<triangle>> list=CONNECTED_COMPONENTS();
		 int index=0;
		 int finIndex=0;
		 while(index<list.size()) {
			 if(list.get(index).size()>list.get(finIndex).size()) {
				 finIndex=index;
				 index++;
			 }
			 index++;
		 }
		 triangle t=null;
		 int dia=0;
		 LinkedList<triangle> finList=list.get(finIndex);
//		 System.out.println(finList.size());
		 int i=0;
		 while(i<finList.size()) {
			 int count=0;
			 LinkedList<triangle> nList=new LinkedList<triangle>();
			 nList.add(finList.get(0));
			 finList.get(0).visited=true;
	//		 System.out.println(nList.get(0));
			 nList.add(t);
	//		 System.out.println(nList.get(1));
			 while(nList.get(0)!=null) {
				 int k=0;
				 while(k<finList.size()) {
					 if(!finList.get(k).visited && shareEdge(finList.get(k), nList.get(0))) {
						 finList.get(k).visited=true;
						 nList.add(finList.get(k)); 
						 k++;
						 }
					 k++;
				 }
	//			 int hi=0;
		//		 while(hi<nList.size()) System.out.println(nList.get(hi++));
				 nList.remove();
				 if(nList.get(0)==null) {
//					 System.out.println("hi");
					 nList.add(t);
					 nList.remove();
					 count++;
				 }
			 }
			 if(count-1>dia) dia=count-1;
			 i++;
		 }
//		 System.out.println(dia);
		 return dia;
		 }
	 
	 

	 public LinkedList<LinkedList<triangle>> CONNECTED_COMPONENTS(){
		 LinkedList<LinkedList<triangle>> list=new LinkedList<LinkedList<triangle>>();
		 int index=0;
		 allTriangle.get(index).count=list.size();
		 LinkedList<triangle> headList=new LinkedList<triangle>();
		 list.add(headList);
		 headList.add(allTriangle.get(index));
		 while(index<allTriangle.size()) {
			 int i=0;
			 while (i<list.size()) {
				 int j=0;
				while (j < list.get(i).size()) {
					if (shareEdge(allTriangle.get(index), list.get(i).get(j)) && allTriangle.get(index).count==-1) {
						list.get(i).add(allTriangle.get(index));
						allTriangle.get(index).count=i;
						break;
					}
					j++;
				} 
				i++;
			 }
			 if(allTriangle.get(index).count==-1) {
				 allTriangle.get(index).count=list.size();
				 LinkedList<triangle> nList=new LinkedList<triangle>();
				 list.add(nList);
				 nList.add(allTriangle.get(index));
			 }
			 index++;
		 }
		 int i=0;
		 while(i<list.size()) {
	//		 System.out.println(list.get(i).size());
			 int j=0;
			 while(j<list.get(i).size()) {
				 list.get(i).get(j).count=-1; j++;
//				 System.out.println(list.get(i).get(j++));
			 }
			 i++;
		 }
		 return list;
		 }

	public PointInterface [] CENTROID (){
		LinkedList<LinkedList<triangle>> okay=CONNECTED_COMPONENTS();
		LinkedList<float[]> arr=new LinkedList<float[]>();
		int index=0;
		while(index<okay.size()) {
			float sx=0;float sy=0;float sz=0;
			int j=0;
			while(j<okay.get(index).size()) {
				sx= sx+okay.get(index).get(j).points[0].getX();
				sx= sx+okay.get(index).get(j).points[1].getX();
				sx= sx+okay.get(index).get(j).points[2].getX();
				sy= sy+okay.get(index).get(j).points[0].getY();
				sy= sy+okay.get(index).get(j).points[1].getY();
				sy= sy+okay.get(index).get(j).points[2].getY();
				sz= sz+okay.get(index).get(j).points[0].getZ();
				sz= sz+okay.get(index).get(j).points[1].getZ();
				sz= sz+okay.get(index).get(j).points[2].getZ();
				j++;
			}
			float[] num=new float[] {sx/(3*j), sy/(3*j), sz/(3*j)};
			arr.add(num);
			index++;
		}
		PointInterface [] result=new PointInterface[arr.size()]; 
		 int hi=0;
			while(hi<arr.size()) {
				PointInterface p=new point(arr.get(hi)[0],arr.get(hi)[1],arr.get(hi)[2]);
				result[hi]=p;
	//			System.out.println(result[hi]);
				hi++;
			}
		return result;
		
	}
	
	public LinkedList<triangle> findcomponent(float [] point_coordinates){
		PointInterface p=new point(point_coordinates[0],point_coordinates[1],point_coordinates[2]);
		LinkedList<LinkedList<triangle>> list=CONNECTED_COMPONENTS();
		int i=0;
		while(i<list.size()) {
			int j=0;
			while(j<list.get(i).size()) {
				if(((point) list.get(i).get(j).points[0]).compareTo((point) p)==0 || ((point) list.get(i).get(j).points[1]).compareTo((point) p)==0 || ((point) list.get(i).get(j).points[2]).compareTo((point) p)==0) {
					LinkedList<triangle> component=list.get(i);
					return component;
				}
				j++;
			}
			i++;
		}
		return null;
	}
	// INPUT [x,y,z]
	public PointInterface CENTROID_OF_COMPONENT (float [] point_coordinates){
		LinkedList<triangle> okay=findcomponent(point_coordinates);
		if(okay!=null) {
			int index=0;
			float sx=0;float sy=0;float sz=0;
			while(index<okay.size()) {				
					sx= sx+okay.get(index).points[0].getX();
					sx= sx+okay.get(index).points[1].getX();
					sx= sx+okay.get(index).points[2].getX();
					sy= sy+okay.get(index).points[0].getY();
					sy= sy+okay.get(index).points[1].getY();
					sy= sy+okay.get(index).points[2].getY();
					sz= sz+okay.get(index).points[0].getZ();
					sz= sz+okay.get(index).points[1].getZ();
					sz= sz+okay.get(index).points[2].getZ();
					index++;
			}
			float[] num=new float[] {sx/(3*index), sy/(3*index), sz/(3*index)};
			PointInterface p=new point(num[0],num[1],num[2]);
//			System.out.print(p);
			return p;
		}
		return null;
	}
	
	public float power(float m, int n) {
        if (n != 0)
            return (m * power(m, n - 1));
        else
            return 1;
    }

	public float distance(point p1, point p2) {
		float xd=(p1.getX()-p2.getX());
		float yd=(p1.getY()-p2.getY());
		float zd=(p1.getZ()-p2.getZ());
		float result=power(xd,2)+power(yd,2)+power(zd,2);
		return result;
	}
	
	public 	PointInterface [] CLOSEST_COMPONENTS(){
		LinkedList<LinkedList<triangle>> list=CONNECTED_COMPONENTS();
		LinkedList<LinkedList<point>> points=new LinkedList<LinkedList<point>>();
		int index=0;
		while(index<list.size()) {
			LinkedList<point> l=new LinkedList<point>();
			int j=0;
			while(j<list.get(index).size()) {
				if(!l.contains((point) list.get(index).get(j).points[0])) {
					l.add((point) list.get(index).get(j).points[0]);
				}
				if(!l.contains((point) list.get(index).get(j).points[1])) {
					l.add((point) list.get(index).get(j).points[1]);
				}
				if(!l.contains((point) list.get(index).get(j).points[2])) {
					l.add((point) list.get(index).get(j).points[2]);
				}
				j++;
			}
			points.add(l);
			index++;
		} 
		if (points.size()>1) {
			float min=distance(points.get(0).get(0), points.get(1).get(0));
			PointInterface [] result=new PointInterface [] {points.get(0).get(0), points.get(1).get(0)};
			int i=0;
			while(i<points.size()) {
				int j=i+1;
				while(j<points.size()) {
					int hi=0;
					while(hi<points.get(i).size()) {
						int hey=0;
						while(hey<points.get(j).size()) {
							if(distance(points.get(i).get(hi), points.get(j).get(hey))<min) {
								min=distance(points.get(i).get(hi), points.get(j).get(hey));
								result[0]=points.get(i).get(hi);
								result[1]=points.get(j).get(hey);
								hey++;
							}
							hey++;
						}
						hi++;
					}
					j++;
				}
				i++;
			}
//			int hi=0;
	//		while(hi<result.length) {
		//		System.out.println(result[hi]);
			//	hi++;
	//		}
			return result;
		}
		else return null;
	
	}
	
/*	public EdgeInterface [] bubblesort(EdgeInterface [] list) {
		System.out.println(list.length);
		if (list.length==0) return null;
		else {
			int i=0;
			while(i<list.length) {
				int j=i+1;
				System.out.println(list.length);
				System.out.println(j);
				if(j<list.length) System.out.println("yo");
				while(j<list.length) {
					System.out.println(list[i]);
					if(((edge) list[j]).eLength()<((edge) list[i]).eLength()) {
						edge temp=(edge) list[i];
						list[i]=list[j];
						list[j]=temp;
						j++;
					}
					j++;
				}
				i++;
			}
			return list;
		}
	}
*/

	public EdgeInterface [] sort(EdgeInterface [] list) {
    	if(list.length==0 )  return null;
    	else if(list.length==1 ) return list;
    	else {	
    //		System.out.println("heyo");
    		int mid=list.length/2;
    		EdgeInterface [] left=new EdgeInterface [mid];
    		EdgeInterface [] right=new EdgeInterface [list.length-mid];
    		for(int i=0;i<mid;i++) {
    		//	System.out.println("okay");
    			left[i]=list[i];
    		}
    		for(int i=mid;i<list.length;i++) right[i-mid]=list[i];
    		sort(left);
    		sort(right);
    		merge(left,right,list);
    		return list;
    	}
    }
	

	 public void merge(EdgeInterface [] lhalf, EdgeInterface [] rhalf, EdgeInterface [] full){
	    	int lcount=0, rcount=0, count=0;
	    	while(lcount<lhalf.length && rcount<rhalf.length) {
	    		if(((edge) lhalf[lcount]).eLength()<=((edge) rhalf[rcount]).eLength()) {
	    			full[count]= lhalf[lcount];
	    			lcount++;
	    		}
	    		else if( ((edge) lhalf[lcount]).eLength()>((edge) rhalf[rcount]).eLength()){
	    			full[count]= rhalf[rcount];
	    			rcount++;
	    		}
	    		count++;
	    	}
	    	
	    	EdgeInterface [] rest;
	        int restIndex;
	        if (lcount >= lhalf.length) {
	            rest = rhalf;
	            restIndex = rcount;
	        } else {
	            rest = lhalf;
	            restIndex = lcount;
	        }
	        for (int i=restIndex; i<rest.length; i++) {
	           full[count]= rest[i];
	            count++;
	        }
	    
	    }



}

