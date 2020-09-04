%{
open Backend

let errexp()=Printf.printf("invalid input\n");;
%}

%token EOL
%token <string> FLOAT
%token LEFTPAR RIGHTPAR
%token LEFTBRACK RIGHTBRACK
%token COMMA COLON
%token ASSIGNOP
%token <string> INDEX
%token <string> RANGE
%token TERMINATOR
%token COUNT ROWCOUNT COLCOUNT SUM ROWSUM COLSUM AVG ROWAVG COLAVG MIN ROWMIN COLMIN MAX ROWMAX COLMAX
%token ADD SUBT MULT DIV
%token UNDEFINED

%start main            
%type <unit> main
%%
main:
	expr EOL {()}
	|error {errexp(); exit 0}
;
expr:
 	 INDEX ASSIGNOP COUNT RANGE TERMINATOR {full_count (sh)($4)($1)}
 	|INDEX ASSIGNOP ROWCOUNT RANGE TERMINATOR {row_count (sh)($4)($1)}
 	|INDEX ASSIGNOP COLCOUNT RANGE TERMINATOR {col_count(sh)($4)($1)}
 	|INDEX ASSIGNOP SUM RANGE TERMINATOR {full_sum (sh)($4)($1)}
 	|INDEX ASSIGNOP ROWSUM RANGE TERMINATOR {row_sum (sh)($4)($1)}
 	|INDEX ASSIGNOP COLSUM RANGE TERMINATOR {col_sum (sh)($4)($1)}
 	|INDEX ASSIGNOP AVG RANGE TERMINATOR {full_avg (sh)($4)($1)}
 	|INDEX ASSIGNOP ROWAVG RANGE TERMINATOR {row_avg (sh)($4)($1)}
 	|INDEX ASSIGNOP COLAVG RANGE TERMINATOR {col_avg (sh)($4)($1)}
 	|INDEX ASSIGNOP MIN RANGE TERMINATOR {full_min (sh)($4)($1)}
 	|INDEX ASSIGNOP ROWMIN RANGE TERMINATOR {row_min (sh)($4)($1)}
 	|INDEX ASSIGNOP COLMIN RANGE TERMINATOR {col_min (sh)($4)($1)}
 	|INDEX ASSIGNOP MAX RANGE TERMINATOR {full_max (sh)($4)($1)}
 	|INDEX ASSIGNOP ROWMAX RANGE TERMINATOR {row_max (sh)($4)($1)}
 	|INDEX ASSIGNOP COLMAX RANGE TERMINATOR {col_max (sh)($4)($1)}
	|INDEX ASSIGNOP ADD RANGE RANGE TERMINATOR {add_range (sh)($4)($5)($1)}
	|INDEX ASSIGNOP SUBT RANGE RANGE TERMINATOR {subt_range (sh)($4)($5)($1)}
	|INDEX ASSIGNOP MULT RANGE RANGE TERMINATOR {mult_range (sh)($4)($5)($1)}
	|INDEX ASSIGNOP DIV RANGE RANGE TERMINATOR {div_range (sh)($4)($5)($1)}
	|INDEX ASSIGNOP ADD FLOAT RANGE TERMINATOR {add_const (sh)($5)(float_of_string $4)($1)}
	|INDEX ASSIGNOP SUBT FLOAT RANGE TERMINATOR {subt_const (sh)($5)(float_of_string $4)($1)}
	|INDEX ASSIGNOP MULT FLOAT RANGE TERMINATOR {mult_const (sh)($5)(float_of_string $4)($1)}
	|INDEX ASSIGNOP DIV FLOAT RANGE TERMINATOR {div_const (sh)($5)(float_of_string $4)($1)}
	|INDEX ASSIGNOP ADD RANGE FLOAT TERMINATOR {add_const (sh)($4)(float_of_string $5)($1)}
	|INDEX ASSIGNOP SUBT RANGE FLOAT TERMINATOR {subt_const (sh)($4)(float_of_string $5)($1)}
	|INDEX ASSIGNOP MULT RANGE FLOAT TERMINATOR {mult_const (sh)($4)(float_of_string $5)($1)}
	|INDEX ASSIGNOP DIV RANGE FLOAT TERMINATOR {div_const (sh)($4)(float_of_string $5)($1)}
	|INDEX ASSIGNOP ADD INDEX RANGE TERMINATOR {add_index (sh)($5)($4)($1)}
	|INDEX ASSIGNOP SUBT INDEX RANGE TERMINATOR {subt_index (sh)($5)($4)($1)}
	|INDEX ASSIGNOP MULT INDEX RANGE TERMINATOR {mult_index (sh)($5)($4)($1)}
	|INDEX ASSIGNOP DIV INDEX RANGE TERMINATOR {div_index (sh)($5)($4)($1)}
	|INDEX ASSIGNOP ADD RANGE INDEX TERMINATOR {add_index (sh)($4)($5)($1)}
	|INDEX ASSIGNOP SUBT RANGE INDEX TERMINATOR {subt_index (sh)($4)($5)($1)}
	|INDEX ASSIGNOP MULT RANGE INDEX TERMINATOR {mult_index (sh)($4)($5)($1)}
	|INDEX ASSIGNOP DIV RANGE INDEX TERMINATOR {div_index (sh)($4)($5)($1)}
;
