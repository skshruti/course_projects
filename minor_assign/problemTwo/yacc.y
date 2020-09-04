%{
#include<stdio.h>
#include<string.h>
int counta=0;
int countb=0;
int test=0;
int isEqual();
int yylex();
%}

%token A B RANDOM

%%
S: E {if(test==0){
		printf("Is the string of type aa...bb...? TRUE\n");
		if(isEqual()==1) printf("Are a and b of equal numbers? TRUE\n");
		else printf("Are a and b of equal numbers? FALSE\n");}
	else printf("Is the string of type aa...bb...? FALSE\n");}
E: RANDOM {test=1;};
 | A {counta=counta+yylval;} B {countb=countb+yylval;}
 ;

%%

#include"lex.yy.c"

yyerror (char const *s){
}


int isEqual(){
	if(counta==countb) return 1;
	else return 0;
}

int main(){
	yyparse();
	printf(“problemTwo successfully compiles and runs\n”);
	return 0;
}