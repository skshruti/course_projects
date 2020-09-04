typedef struct bignums{
	char dig[1000];
	int sign;
	int noDig;
}bignum;

typedef struct complexs{
	bignum real;
	bignum img;
}complex;

bignum tobignum(char *string);
int print_bignum(bignum b);
int max(int a, int b);
bignum add(bignum a, bignum b);
bignum zero_bignum();
int compare_bignum(bignum a, bignum b);
bignum sub(bignum a, bignum b);
bignum shift_left(bignum b, int i);
bignum ntp(bignum a);
int print_complex(complex c);
complex addc(complex c1, complex c2);
int floatcarry=0;
int floatborrow=0;
bignum adddec(bignum a, bignum b);
int compare_dec(bignum a, bignum b);
char **getInp(char *);
bignum helper(bignum a);
bignum leadingzero(bignum b);

bignum tobignum(char *string){
	bignum result;
	result.noDig=0;
 	for (int i=0; i<1000; i++) result.dig[i] = (char) 0;
	result.sign=1;
    if(string[0]=='-') result.sign=-1;
	int i=0;
	while(i<(int) strlen(string)){
//		printf("nodig %d", result.noDig);
		result.dig[i]=string[i];
		result.noDig++;
		i++;
	}
	if(string[0]=='-') result.noDig--;
//	printf("\n%s %d\n", string, result.noDig);
	return result;
}

complex tocomplex(char *string){
	char **array=malloc(64 * sizeof(char *));
	char *parsed=strtok(string, " ,()\n");
	int position=0;
	while(parsed!=NULL){
		array[position]=parsed;
		position++;
		parsed=strtok(NULL, " ,()\n");

	}
	array[position]=NULL;
	complex c;
	c.real=tobignum(array[0]);
	c.img=tobignum(array[1]);
	return c;
}

int print_bignum(bignum b){
	b=leadingzero(b);
	int i=0;
	if(b.sign==-1) printf("-");
	int limit=b.noDig;
	if (b.dig[0]=='-') {
	    limit++;
	    i++;
	}
	while(i<limit){
		printf("%c", b.dig[i]);
		i++;
	};
	return 0;
}

bignum helper(bignum a){
		int j=0;
		while(j<a.noDig){
			a.dig[j]=a.dig[j+1];
		    j++;
		}
		a.noDig--;
		return a;
}

bignum leadingzero(bignum a){
	if(a.dig[0]=='-'){
		int j=0;
		while(j<a.noDig){
			a.dig[j]=a.dig[j+1];
		    j++;
		}
	}
	while(a.dig[0]=='0' && a.noDig>1){
		a=helper(a);
	}
	return a;
}

int max(int a, int b){
	if (a>b) return a;
	else return b;
}

int is_float(bignum a){
	int i=0;
	int limit=a.noDig;
	if (a.sign==-1 || a.dig[0]=='-') limit++;
	while(i<a.noDig){
		if(a.dig[i]=='.') return 1;
		i++;
	}
	return 0;
}

bignum float_to_int(bignum a){
	if(is_float(a)==1){
	    ntp(a);
		int i=0;
		while(a.dig[i]!='.') i++;
		int j=i;
		int limit=a.noDig;
	    if (a.sign==-1 || a.dig[0]=='-') limit++;
		while(j<a.noDig){
		    a.dig[j]=a.dig[j+1];
		    j++;
		}
		a.noDig--;
	}
	return a;
}

bignum floatre(bignum a){
	if(is_float(a)==1){
		bignum result;
		for (int i=0; i<1000; i++) result.dig[i] = (char) 0;
		result.sign=a.sign;
		result.noDig=0;
		int limit=0;
		while(a.dig[limit]!='.') limit++;
		int j=0;
		while(j<limit){
		    result.dig[j]=a.dig[j];
		    j++;
		    result.noDig++;
		}
		if(a.dig[0]=='-') result.noDig--;
		return result;
	}
	return a;
}

bignum floatimg(bignum a){
	if(is_float(a)==1){
		bignum result;
		for (int i=0; i<1000; i++) result.dig[i] = (char) 0;
		result.sign=+1;
		result.noDig=0;
		int i=0;
		while(a.dig[i]!='.') i++;
		i++;
		int j=0;
		int limit=a.noDig;
	    if (a.sign==-1 || a.dig[0]=='-') limit++;
		while(i<limit){
		    result.dig[j]=a.dig[i];
		    i++;
		    j++;
		    result.noDig++;
		}
		if(result.noDig==0) return zero_bignum();
		return result;
	}
	return zero_bignum();
}

bignum int_to_float(bignum a, int i){
	int counter=a.noDig;
	if (a.dig[0]=='-') counter++;
	while(i>0){
		a.dig[counter]=a.dig[counter-1];
		counter--;
		i--;
	}
	a.dig[counter]='.';
	a.noDig++;
	return a;
}

int countdec(bignum a){
	if(is_float(a)==1){
		if(a.dig[0]=='-'){
			int j=0;
			while(j<a.noDig){
				a.dig[j]=a.dig[j+1];
			    j++;
			}
		}
		int i=0;
		while(a.dig[i]!='.') i++;
		return a.noDig-i-1;
	}
	return 0;
}

bignum ntp(bignum a){
	if(a.dig[0]=='-'){
		int j=0;
		while(j<a.noDig){
			a.dig[j]=a.dig[j+1];
		    j++;
		}
	}
	return a;
}

bignum adddec(bignum a, bignum b){
	if(a.noDig<b.noDig){
		int i=a.noDig;
		while(i<b.noDig){
			a.dig[i]='0';
			a.noDig++;
			i++;
		}
	}
	if(b.noDig<a.noDig){
		int i=b.noDig;
		while(i<a.noDig){
			b.dig[i]='0';
			b.noDig++;
			i++;
		}
	}
		int carry=0;
		bignum result;
		for (int i=0; i<1000; i++) result.dig[i] = (char) 0;
		result.sign=+1;
		result.noDig=0;
		int i=a.noDig-1;
		int j=b.noDig-1;
		int k=b.noDig-1;
    		while(i>-1 && j>-1){
    			result.noDig++;
    			result.dig[k]=(char)((((a.dig[i]-'0')+(b.dig[j]-'0')+carry)%10)+48);
    			carry=((a.dig[i]-'0')+(b.dig[j]-'0')+carry)/10;
    			i--;
    			j--;
    			k--;
    		}
    	floatcarry=carry;
	return result;
}



bignum addint(bignum a, bignum b, int carry){
	if(a.sign==b.sign){
		bignum result;
		for (int i=0; i<1000; i++) result.dig[i] = (char) 0;
		if(a.sign==+1) result.sign=+1;
		else result.sign=-1;
		result.noDig=0;
		if(a.sign==-1){
				int i=0;
				while(i<b.noDig){
				    b.dig[i]=b.dig[i+1];
				    i++;
				}
				int j=0;
				while(j<a.noDig){
				    a.dig[j]=a.dig[j+1];
				    j++;
				}
				result.sign=-1;
			}
		int i=a.noDig-1;
		int j=b.noDig-1;
		int k=max(a.noDig, b.noDig);
    		while(i>-1 && j>-1){
    			result.noDig++;
    			result.dig[k]=(char)((((a.dig[i]-'0')+(b.dig[j]-'0')+carry)%10)+48);
    			carry=((a.dig[i]-'0')+(b.dig[j]-'0')+carry)/10;
    			i--;
    			j--;
    			k--;
    		}
		if(i<=-1 && j>-1){
			while(j>-1){
				result.noDig++;
				result.dig[k]=(char)((((b.dig[j]-'0')+carry)%10)+48);
				carry=((b.dig[j]-'0')+carry)/10;
				j--;
				k--;
			}
		};
		if(j<=-1 && i>-1){
			while(i>-1){
				result.noDig++;
				result.dig[k]=(char)((((a.dig[i]-'0')+carry)%10)+48);
				carry=((a.dig[i]-'0')+carry)/10;
				i--;
				k--;
			}
		};
		if(carry!=0){
		    result.dig[0]=(char)(carry+48);
		    result.noDig++;
		}
		else{
		    int i=0;
		    while(i<result.noDig){
		        result.dig[i]=result.dig[i+1];
		        i++;
		    }
		}
	return result;
  }
     else if(a.sign==-1){
     	return add(b,a);
     } 
	 else {
	 	b.sign=+1;
	 	int i=0;
		while(i<b.noDig){
			b.dig[i]=b.dig[i+1];
			i++;
		}
	 	return sub(a,b);
	 }
}

 bignum add(bignum a, bignum b){
	if(is_float(a)==1 || is_float(b)==1){
 		if(a.sign!=b.sign){
			if(b.sign==-1){
				b.sign=+1;
				int i=0;
				while(i<b.noDig){
				    b.dig[i]=b.dig[i+1];
				    i++;
				}
				return sub(a,b);
			}
			else{
				a.sign=+1;
				int i=0;
				while(i<a.noDig){
				    a.dig[i]=a.dig[i+1];
				    i++;
				}
				return sub(b,a);
			}
		}
		if(a.sign==-1){
			b.sign=+1;
			int i=0;
			while(i<b.noDig){
		    	b.dig[i]=b.dig[i+1];
			    i++;
			}
			a.sign=+1;
			int j=0;
			while(j<a.noDig){
			    a.dig[j]=a.dig[j+1];
				j++;
			}
			bignum final=add(a,b);
			final.sign=-1;
			return final;

		}

 		bignum areal=floatre(a);
 		bignum aimg=floatimg(a);
 		bignum breal=floatre(b);
 		bignum bimg=floatimg(b);
 		bignum sumimg=adddec(aimg, bimg);
 		bignum sumre=addint(areal, breal, floatcarry);
 		bignum sum=sumre;
 		int i=sumre.noDig;
 		sum.dig[i]='.';
 		i++;
 		sum.noDig++;
 		int j=0;
 		while(j<sumimg.noDig){
 			sum.dig[i]=sumimg.dig[j];
 			i++;
 			j++;
 			sum.noDig++;
 		}
 		return sum;
 	}
 	else return addint(a, b, 0);
 }

bignum zero_bignum(){
	bignum a;
	a.dig[0]=(char)(48);
	a.sign=+1;
	a.noDig=1;
	return a;
}

int compare_bignum(bignum a, bignum b)
{
	if(is_float(a)==1 || is_float(b)==1){
		if(compare_bignum(floatre(a), floatimg(b))!=0) {
		//	printf("hi%d",);
			return compare_bignum(floatre(a), floatre(b));
		}
		else return compare_dec(floatimg(a), floatimg(b));
	}
	int i;			
	if ((a.sign == -1) && (b.sign == +1)) return(-1);
	if ((a.sign == +1) && (b.sign == -1)) return(+1);

	if(a.sign==-1){
		if (b.noDig > a.noDig) return (+1);
		if (a.noDig > b.noDig) return (-1);
		for (i = 0; i<=a.noDig; i++) {
			if (a.dig[i] > b.dig[i]) return(-1);
			if (b.dig[i] > a.dig[i]) return(+1);
		}
	}
	else{
		if (b.noDig > a.noDig) return (-1);
		if (a.noDig > b.noDig) return (+1);
		for (i = 0; i<=a.noDig-1; i++) {
			if (a.dig[i] > b.dig[i]) return(+1);
			if (b.dig[i] > a.dig[i]) return(-1);
		}
	}
	return(0);
}

int compare_dec(bignum a, bignum b){
	if(a.noDig<b.noDig){
		int i=a.noDig;
		while(i<b.noDig){
			a.dig[i]='0';
			a.noDig++;
			i++;
		}
	}
	if(b.noDig<a.noDig){
		int i=b.noDig;
		while(i<a.noDig){
			b.dig[i]='0';
			b.noDig++;
			i++;
		}
	}
	int i;	
	for (i = 0; i<=a.noDig-1; i++) {
		if (a.dig[i] > b.dig[i]) return(+1);	
		if (b.dig[i] > a.dig[i]) return(-1);
	}
	
	return(0);

}
bignum subdec(bignum a, bignum b){
	if(a.noDig<b.noDig){
		int i=a.noDig;
		while(i<b.noDig){
			a.dig[i]='0';
			a.noDig++;
			i++;
		}
	}
	if(b.noDig<a.noDig){
		int i=b.noDig;
		while(i<a.noDig){
			b.dig[i]='0';
			b.noDig++;
			i++;
		}
	}
	int borrow=0;
	bignum result;
	for (int i=0; i<1000; i++) result.dig[i] = (char) 0;
	result.sign=+1;
	int k=b.noDig-1;
	result.noDig=0;
	int v;
	int i=a.noDig-1;
    while(i>-1){
    //	printf("a=%c\n", a.dig[i]);
    //	printf("b=%c\n", b.dig[i]);
    	result.noDig++;
    	v=((a.dig[i]-'0')-borrow-(b.dig[i]-'0'));
    	if(a.dig[i]>0) borrow=0;
    	if(v<0){
    		v=v+10;
    		borrow=1;
    		}
   		result.dig[k]=(char)((v%10)+48);
   	//	printf("res=%c\n", result.dig[k]);
  		i--;
    	k--;
    }
    floatborrow=borrow;
    return result;
}

bignum subint(bignum a, bignum b, int borrow){
	if(compare_bignum(a,b)==0) {
	    return zero_bignum();
	}
	if(a.sign!=b.sign){
		if(b.sign==-1){
			b.sign=+1;
			int i=0;
			while(i<b.noDig){
			    b.dig[i]=b.dig[i+1];
			    i++;
			}
			return add(a,b);
		}
		else{
			a.sign=+1;
			int i=0;
			while(i<a.noDig){
			    a.dig[i]=a.dig[i+1];
			    i++;
			}
			bignum final;
			final=add(a,b);
			final.sign=-1;
			return final;
		}
	}
	else{
		if(a.sign==+1 && compare_bignum(a,b)<0) {
			bignum final;
			final=sub(b,a);
			final.sign=-1;
			return final;
		}
		else{
			bignum result;
			for (int i=0; i<1000; i++) result.dig[i] = (char) 0;
			result.sign=+1;
			int k=max(a.noDig, b.noDig)-1;
			if(a.sign==-1){
				int i=0;
				while(i<b.noDig){
				    b.dig[i]=b.dig[i+1];
				    i++;
				}
				int j=0;
				while(j<a.noDig){
				    a.dig[j]=a.dig[j+1];
				    j++;
				}
				if(compare_bignum(a,b)<0) result.sign=-1;
				if(compare_bignum(a,b)>0){
				    bignum c;
				    c=b;
				    b=a;
				    a=c;
				}
			}
			result.noDig=0;
			int v;
			int i=a.noDig-1;
			int j=b.noDig-1;
    		while(i>-1 && j>-1){
    			result.noDig++;
    			v=((a.dig[i]-'0')-borrow-(b.dig[j]-'0'));
    			if(a.dig[i]>0) borrow=0;
    			if(v<0){
    				v=v+10;
    				borrow=1;
    			}
    			result.dig[k]=(char)((v%10)+48);
    			i--;
    			j--;
    			k--;
    		}
			if(j<=-1 && i>-1){
				while(i>-1){
					result.noDig++;
	    			v=((a.dig[i]-'0')-borrow);
	    			if(a.dig[i]>0) borrow=0;
	    			if(v<0){
	    				v=v+10;
	    				borrow=1;
	    			}
	    			result.dig[k]=(char)((v%10)+48);
	    			i--;
	    			k--;
				}
			};
    		return result;
		}
	}

}

bignum sub(bignum a, bignum b){
 	if(is_float(a)==1 || is_float(b)==1){
 		if(a.sign!=b.sign){
			if(b.sign==-1){
				b.sign=+1;
				int i=0;
				while(i<b.noDig){
				    b.dig[i]=b.dig[i+1];
				    i++;
				}
				return add(a,b);
			}
			else{
				a.sign=+1;
				int i=0;
				while(i<a.noDig){
				    a.dig[i]=a.dig[i+1];
				    i++;
				}
				bignum final;
				final=add(a,b);
				final.sign=-1;
				return final;
			}
		}
		if(a.sign==-1){
			b.sign=+1;
			int i=0;
			while(i<b.noDig){
		    	b.dig[i]=b.dig[i+1];
			    i++;
			}
			a.sign=+1;
			int j=0;
			while(j<a.noDig){
			    a.dig[j]=a.dig[j+1];
				j++;
			}
			// printf("\na");
			// p
			return sub(b,a);

		}

 		if(compare_bignum(a,b)<0) {
 			bignum res=sub(b,a);
 			res.sign=-1;
 			return res;
 		}
 		bignum areal=floatre(a);
 		bignum aimg=floatimg(a);
 		bignum breal=floatre(b);
 		bignum bimg=floatimg(b);
 		bignum sumimg=subdec(aimg, bimg);
 		// print_bignum(a);
 		// print_bignum(b);
 		
 		// printf("\nsubdec\n");
 		// print_bignum(aimg);
 		// print_bignum(bimg);
 		
 		bignum sumre=subint(areal, breal, floatborrow);
 		bignum sum=sumre;
 		int i=sumre.noDig;
 		sum.dig[i]='.';
 		i++;
 		sum.noDig++;
 		int j=0;
 		while(j<sumimg.noDig){
 			sum.dig[i]=sumimg.dig[j];
 			i++;
 			j++;
 			sum.noDig++;
 		}
 		return sum;
 	}
 	else return subint(a, b, 0);
 }

bignum shift_left(bignum b, int i){
	int k=b.noDig;
	int counter=0;
	while(counter<i){
		b.dig[b.noDig]=(char)(48);
		b.noDig++;
		counter++;
	}
	return b;
}

bignum multint(bignum a, int b){
	bignum result;
	for (int i=0; i<1000; i++) result.dig[i] = (char) 0;
	result.noDig=0;
	result.sign=+1;
	int k=a.noDig;
	int carry=0;
	int i=a.noDig-1;
	while(i>-1){
    	result.noDig++;
    	result.dig[k]=(char)(((((a.dig[i]-'0')*b)+carry)%10)+48);
    	carry=(((a.dig[i]-'0')*b)+carry)/10;
    	i--;
    	k--;
    }
    if(carry!=0){
		    result.dig[0]=(char)(carry+48);
		    result.noDig++;
	}
	else{
		int i=0;
	    while(i<result.noDig){
    		result.dig[i]=result.dig[i+1];
    		i++;
		}
	}
    return result;
}

bignum mult(bignum a, bignum b){
	int decf=countdec(a)+countdec(b);
	a=float_to_int(a);
	b=float_to_int(b);	
	if(b.dig[0]=='-'){
		int i=0;
		while(i<b.noDig){
		b.dig[i]=b.dig[i+1];
		i++;
		}
	}
	if(a.dig[0]=='-'){
		int j=0;
		while(j<a.noDig){
			a.dig[j]=a.dig[j+1];
		    j++;
		}
	}
	bignum sum=multint(a, b.dig[b.noDig-1]-'0');
	sum.sign=+1;
	int i=b.noDig-2;
	int shift=1;
	while(shift<b.noDig){
		int d=b.dig[i]-'0';
		bignum tosum=multint(a, d);
		tosum=shift_left(tosum, shift);
		sum=add(sum, tosum);
		shift++;
		i--;
	}
	if(a.sign!=b.sign) sum.sign=-1;
	if(decf>0) sum=int_to_float(sum, decf);
	return sum;
}

int print_complex(complex c){
	printf("(");
	print_bignum(c.real);
	printf(",");
//	if(c.img.sign==+1) printf("+");
	print_bignum(c.img);
	printf(")");
	return 0;
}

complex addc(complex c1, complex c2){
	bignum realre=add(c1.real, c2.real);
	bignum imgre=add(c1.img, c2.img);
	complex result;
	result.real=realre;
	result.img=imgre;
	return result;
}

complex subc(complex c1, complex c2){
	bignum realre=sub(c1.real, c2.real);
	bignum imgre=sub(c1.img, c2.img);
	complex result;
	result.real=realre;
	result.img=imgre;
	return result;
}

complex multc(complex c1, complex c2){
	bignum realre=sub(mult(c1.real,c2.real), mult(c1.img,c2.img));
	bignum imgre=add(mult(c1.real,c2.img), mult(c1.img,c2.real));
	complex result;
	result.real=realre;
	result.img=imgre;
	return result;
}

complex absc(complex c){
	complex result;
	result.img=zero_bignum();
	result.real=add(mult(c.real,c.real),mult(c.img,c.img));
	return result;
}


#define seperate "(), \n"
char **getInp(char *input){
	char **array=malloc(64 * sizeof(char *));
	char *parsed=strtok(input, seperate);
	int position=0;
	while(parsed!=NULL){
		array[position]=parsed;
		position++;
		parsed=strtok(NULL, seperate);
	}
	array[position]=NULL;
	return array;
}
