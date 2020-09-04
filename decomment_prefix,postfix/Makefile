all:
	(lex lex.l; gcc -o decomment lex.yy.c; lex file.l; yacc file.y; gcc -o conversion y.tab.c -ll -ly)
