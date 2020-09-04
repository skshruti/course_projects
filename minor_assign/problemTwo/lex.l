%{

%}

%%
a*	{yylval=yyleng;return A;}
b*	{yylval=yyleng;return B;}
(a*b*)?[^ab\n]+ {return RANDOM;}
a*b*a+ {return RANDOM;}
\n	{yyterminate();}
%%

int yywrap(){}

