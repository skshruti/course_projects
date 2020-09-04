%{
open Backend
let errexp()=Printf.printf("invalid input\n");;
let dbase=ref [[]];;

%}

%token EOL EOF
%token <string> NOVAR
%token <string> VAR
%token QUERY ONLYIF
%token LBRACK COMMA RBRACK
%token TERMINATOR
%token UNDEFINED
%token HALT
%start line
%type <Backend.term list> line
%%

line:
	 input EOL {$1}
	|error {errexp();[]}

input:
	 store TERMINATOR {dbase:=$1::!dbase;$1}
	|answer TERMINATOR {$1}
	|HALT TERMINATOR {exit 0}

store:
	 fact {$1::[]}
	|rule {$1}

answer:
	 QUERY fact {print_sol(check_fact($2)(!dbase)); $2::[]}
	|QUERY query {print_solutions(give_solutions($2)(!dbase));print_newline(); $2}

fact: 
	 NOVAR {create_term($1)([])}
	|NOVAR LBRACK factlist RBRACK {create_term($1)($3)}

factlist:
	 fact {$1::[]}
	|fact COMMA factlist {$1::$3} 

query:
	 question {$1::[]}
	|question COMMA query {$1::$3}

question:
	 VAR {create_var($1)}
	|NOVAR LBRACK questionlist RBRACK {create_term($1)($3)}

questionlist:
	 question {$1::[]}
	|VAR COMMA questionlist {(create_var($1))::$3}
	|VAR COMMA factlist {create_var($1)::$3}
	|fact COMMA questionlist {$1::$3}
	|question COMMA questionlist {$1::$3}
	|question COMMA factlist {$1::$3}

rule:
	 fact ONLYIF factlist {$1::$3}
	|fact ONLYIF questionlist {$1::$3}
	|question ONLYIF questionlist {$1::$3}
