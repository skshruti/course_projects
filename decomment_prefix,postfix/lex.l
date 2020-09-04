%{
#include<stdio.h> 
#include<string.h> 
void comment();
void literal();
void uncomment();
int count=1;
int lineno=0;
%}

%% 
\/\*[^*/]*[^*]*[^/]*\*\/ {comment(yytext);
	/*this is a comment*/}; 
\/\*[^*/]*[^*]*[^/]* {uncomment(yytext);
	/*this is an unterminated comment*/};
[^'/*']\"[^"""]*([^\\](\\\\)*\\\")*[^"""]*(\/\*[^*/]*[^/]*[^*]*\*\/)?[^"""]* {
	literal(yytext);
	ECHO;
	/*this handles unterminated string literals and prints them without any changes*/}
[^'/*']\'[^''']*([^\\](\\\\)*\\\')*[^''']*(\/\*[^*/]*[^/]*[^*]*\*\/)?[^''']* {
	literal(yytext);
	ECHO;
	/*this handles unterminated character literals and prints them without any changes*/}
[^'/*']\"[^"""]*([^\\](\\\\)*\\\")*[^"""]*(\/\*[^*/]*[^/]*[^*]*\*\/)?[^"""]*\"[^'/*'] {
	literal(yytext);
	ECHO;
	/*this handles string literals and does not replace comments within with a space*/}
[^'/*']\'[^''']*([^\\](\\\\)*\\\')*[^''']*(\/\*[^*/]*[^/]*[^*]*\*\/)?[^''']*\'[^'/*'] {
	literal(yytext);
	ECHO;
	/*this handles character literals and does not replace comments within with a space*/
	/*these regular expressions handle all the specifications provided in the assignment*/}
. {ECHO;
}
\n {
	count++;
	printf("\n");
}
%% 

int yywrap(){} 

void literal(char *str){
	/*this increments the count of lines whenever a new line is encountered*/
	int i=0;
	while(i<strlen(str)){
		if(str[i]=='\n') {
			count++;
		}
		i++;
	}
	return;
}

void uncomment(char *str){
	/*stores the line when comment started in lineno and prints it in case of unterminated comment*/
	lineno=count;
	printf(" ");
	int i=0;
	while(i<strlen(str)){
		if(str[i]=='\n') {
			printf("\n");
			count++;
		}
		i++;
	}
	fprintf( stderr, "Error: line %d: unterminated comment\n",lineno);
	return;
}

void comment(char *str){
	/*replaces comments with a space and required number of new lines*/
	lineno=count;
	printf(" ");
	int i=0;
	while(i<strlen(str)){
		if(str[i]=='\n') {
			printf("\n");
			count++;
		}
		i++;
	}
	return;
}

int main(){
	yylex();
	return 0; 
} 