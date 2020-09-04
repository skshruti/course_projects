%{
    #include<stdio.h>
    #include<string.h>
    void push();
    char* pop();
    char* topelem();
    void pushi();
    int popi();
    int topelemi();
    void func(char* a);
    void calculate(char* a);
    int result=0;
    int yylex();
    FILE *fp;
%}

%token ID NEXT
%%

S   : E NEXT {fprintf(fp,"%s %d\n",topelem(), topelemi());} S
    | E {fprintf(fp,"%s %d\n",topelem(), topelemi());}
    | error NEXT {fprintf(fp,"\n");} S 
E    : E E '+' {func("+ "); calculate("+ ");}
    | E E '-' {func("- "); calculate("- ");}
    | E E '*' {func("* "); calculate("* ");}
    | E E '/' {func("/ "); calculate("/ ");}
    | ID    {push(); pushi(yylval);}
    ;

%%
#include"lex.yy.c"

char str[100][100];
int answer[100];
int i=0;
int j=0;

yyerror (char const *s){
        fprintf(fp,"invalid input");
}

void pushi(int a){
   answer[j]=a;
   j++;
}

void push()
{
   strcpy(str[i],yytext);
   i++;
}

int popi(){
    j--;
    return answer[j];
}
char* pop()
{   
    i--;
    return str[i];
}

int topelemi(){
    return answer[j-1];
}
char* topelem()
{
    return str[i-1];
}

void func(char* a)
{
    char temp[1000];
    char* expr1=pop();//5
    char* expr2=pop();//4
    bzero(temp,1000);
    strcat(temp,a);//+
    strcat(temp,expr2);
    strcat(temp," ");
    strcat(temp,expr1);
    strcpy(str[i],temp);
    i++;
}

void calculate(char* a)
{
    int expr1=popi();
    int expr2=popi();
    if(strcmp(a,"+ ")==0) answer[j]=expr2+expr1;
    if(strcmp(a,"- ")==0) answer[j]=expr2-expr1;
    if(strcmp(a,"* ")==0) answer[j]=expr2*expr1;
    if(strcmp(a,"/ ")==0) answer[j]=expr2/expr1;
    j++;
}

int main()
{
    FILE *f;
    f=fopen("postfix.txt","r");
    fp=fopen("result.txt","w");
    yyin=f;
    yyparse();
    fclose(f);
    fclose(fp);
    return 0;

}