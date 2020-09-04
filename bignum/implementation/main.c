#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include"arbprecision.h"
// char** argv = malloc(2);
// argv[0] = "file.txt";
// argv[1] = "out.txt";
int main(int argc, char **argv){
	char **input;	
 	FILE *i;
 	char *o;
	// i = fopen("file.txt", "r");
	// o = "out.txt";
 	i=fopen(argv[1], "r");;
 	o=argv[2];
	if(i == NULL) {
      printf("Error opening file");
      return(-1);
   }
   char *string=NULL;
   size_t length=0;
   size_t line;
	freopen(o, "w+", stdout);
	while ((line=getline(&string, &length, i)) != -1) {
		input=getInp(string);
		if(strcmp(input[0], "ABS")==0){
			char *a;
			a=input[1];
			char *b;
			b=input[2];
			bignum b1=tobignum(a);
			bignum b2=tobignum(b);
			complex c1;
			c1.real=b1;
			c1.img=b2;
			print_complex(absc(c1));
			printf("\n");
			input=getInp(string);

		}	
		else{
			char *a;
			a=input[1];
			char *b;
			b=input[2];
			char *c;
			c=input[3];
			char *d;
			d=input[4];
			bignum b1=tobignum(a);
			bignum b2=tobignum(b);
			bignum b3=tobignum(c);
			bignum b4=tobignum(d);
			complex c1;
			complex c2;
			c1.real=b1;
			c1.img=b2;
			c2.real=b3;
			c2.img=b4;
			if(strcmp(input[0], "ADD")==0){
			//	fprintf(stdout, print_complex(addc(c1,c2)));
				print_complex(addc(c1,c2));
				printf("\n");
				input=getInp(string);
			}
			else if(strcmp(input[0], "SUB")==0){
	//			freopen(o, "w+", stdout);
				print_complex(subc(c1,c2));
				printf("\n");
				input=getInp(string);
			}
			else if(strcmp(input[0], "PROD")==0){
	//			freopen(o, "w+", stdout);
				print_complex(multc(c1,c2));
				printf("\n");
				input=getInp(string);
			}
			else printf("Command not Found\n");
		}

	}
	fclose(i);
	return 0;
}