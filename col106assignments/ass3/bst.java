//package assignment3;

public class bst {
	bst right;
	bst left;
	bst up;
	Student data;
	
	bst(Student obj) {
		this.data=obj;
		this.right=null;
		this.left=null;
		this.up = null;
	} 
	

	public int insertbst(Student obj) {
		 if(this.data.fname().compareToIgnoreCase(obj.fname())>0) {
			if(this.left == null) {
				bst d = new bst(obj);
				this.left =d;
				this.left.up=this;return 1;
			} 
			else return 1+this.left.insertbst(obj);
			//count++;
		}
		else {
			if(this.right == null) {
				bst d = new bst(obj);
				this.right =d;
				this.right.up = this;return 1;
				} 
			else return 1+this.right.insertbst(obj);
			//count++;
		}
		
		//System.out.print(67);
		//return count;
	}
	
	public int updatebst(Student obj) {
		//int count=0;
		if(this.data.fname().equals(obj.fname())) {
			this.data=(Student) obj;
			return 1;
		}
		else if(this.data.fname().compareToIgnoreCase(obj.fname())>0) {
			return 1+this.left.updatebst(obj);
			
		}
		else {
			return 1+this.right.updatebst(obj);
			
		}
		
	}
	
	public int deletebst(Pair pair) {
		int count=0;
		if((this.data.fname().equals(pair.first))) {
			if(this.left==null && this.right==null) {
				if(this.up.right == this) {
					this.up.right = null;
				}
				else {
					this.up.left =null;
				}
				count++;
			}
			else if(this.left==null) {
				if(this.up.right == this) {
					this.up.right = this.right;
				}
				else {
					this.up.left = this.right;
				}
				count++;
			}
			else if(this.right==null) {
				if(this.up.right == this) {
					this.up.right = this.left;
				}
				else {
					this.up.left = this.left;
				}
				count++;
			}
			else {
				bst minbst=this.right;
				Pair p=this.right.data.pair();
				
					while(minbst.left!=null) {
						minbst=minbst.left;
						p=minbst.data.pair();
						count++;
				
				this.data=minbst.data;
				count=count+this.right.deletebst(p);
				}
			}
		}
		else if(this.data.fname().compareToIgnoreCase(pair.first)>0) {
			count++;
			count =count+this.left.deletebst(pair);
		}
		else {
			count++;
			count =count+this.right.deletebst(pair);
		}
		return count;
	}
	
	public boolean containsbst(String key) {
	
			if((this.data.fname()+this.data.lname()).equals(key)) {
				return true;
			}
			else if((this.data.fname()+this.data.lname()).compareToIgnoreCase(key)>0) {
				if(this.left == null) return false;
				return this.left.containsbst(key);
			}
			else{
				if(this.right == null)return false;
				return this.right.containsbst(key);
			
		}
		//return false;
	}
	
	public String getbst(String key) {
			if(this.data!=null && (this.data.fname()+this.data.lname()).equals(key)) {
				return this.data.getData();
			}
			else if(this.left!=null && (this.data.fname()+this.data.lname()).compareToIgnoreCase(key)>0 ) {
				return this.left.getbst(key);
			}
			else if(this.right!=null && (this.data.fname()+this.data.lname()).compareToIgnoreCase(key)<0){
				return this.right.getbst(key);
			}
			else {
				return null;
			}
		
	}
	
	public String addressbst(String key) {
		//String result="-";
		if((this.data.fname()+this.data.lname()).equals(key)) {
			return "";	
		}
		else if((this.data.fname()+this.data.lname()).compareToIgnoreCase(key)>0) {
			return "L"+this.left.addressbst(key);
			
		}
		else{
			return "R"+this.right.addressbst(key);
			
		}
	//return result;
}
	
}
