{
open Parser
exception EOF;;
}

rule token = parse
	| '\n'	{EOL}
	| [' ' '\t' ] {token lexbuf}
	| "halt" {HALT}
	| "?-" {QUERY}
	| ":-" {ONLYIF}
	| '(' {LBRACK}
	| ')' {RBRACK}
	| ',' {COMMA}
	| ['0'-'9']['0'-'9']* as str{NOVAR(str)}
	| ['a'-'z']['a'-'z''_''A'-'Z''0'-'9']* as str{NOVAR(str)}
	| ['A'-'Z']['a'-'z''_''A'-'Z']* as str{VAR(str)}
	| '.' {TERMINATOR}
	| eof {EOF}


