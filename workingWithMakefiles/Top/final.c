#include <stdio.h>
extern evenodd();
extern cube();
extern add32();
extern max();

int main(){
	int a;
	printf("Enter a number: ");
	scanf("%d", &a);
	int b,c,d,e;
	b=eo(a);
	c=cube(a);
	d=add32(a);
	e=max(a);
	printf("if even then 1 else 0: %d\n cube of the no is: %d\n after adding 32, the no becomes: %d\n if less than 50 return no else 50: %d\n", b, c, d, e);
	return 0;
}

