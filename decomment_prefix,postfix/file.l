%{
/* Definition section */
%}
DIGIT [0-9]

/* Rule Section */
%%
(-)?{DIGIT}+			 {yylval=atoi(yytext); 
				 return ID;}
\n				 return NEXT;
["*-/+"]		 return yytext[0];
.      ;
<<EOF>> 	yyterminate();
%%