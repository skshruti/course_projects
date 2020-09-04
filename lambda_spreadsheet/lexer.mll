{
open Parser
exception EOF;;
}

rule token = parse
	| '\n'	{EOL}
	| [' ' '\t' ] {token lexbuf}
	| ['0'-'9']* as flt {FLOAT(flt)}
	| '-'?('0'|['1'-'9']['0'-'9']*)'.'((['0'-'9']*['1'-'9']|'0'))? as flt {FLOAT(flt)}
	| '('	{LEFTPAR}
	| ')'	{RIGHTPAR}
	| '['	{LEFTBRACK}
	| ']'	{RIGHTBRACK}
	| ','	{COMMA}
	| ':'	{COLON}
	| ':''='	{ASSIGNOP}
	| "COUNT"	{COUNT}
	| "ROWCOUNT" {ROWCOUNT}
	| "COLCOUNT" {COLCOUNT}
	| "SUM" {SUM}
	| "ROWSUM" {ROWSUM}
	| "COLSUM" {COLSUM}
	| "AVG" {AVG}
	| "ROWAVG" {ROWAVG}
	| "COLAVG" {COLAVG}
	| "MIN" {MIN}
	| "ROWMIN" {ROWMIN}
	| "COLMIN" {COLMIN}
	| "MAX" {MAX}
	| "ROWMAX" {ROWMAX}
	| "COLMAX" {COLMAX}
	| "ADD" {ADD}
	| "SUBT" {SUBT}
	| "MULT" {MULT}
	| "DIV" {DIV}
	| '['['0'-'9']*','' '?['0'-'9']*']' as str {INDEX(str)}
	| '('' '?'['['0'-'9']*','' '?['0'-'9']*']'' '?':'' '?'['['0'-'9']*','' '?['0'-'9']*']'' '?')' as str {RANGE(str)}
	| ';' {TERMINATOR}
	| eof {raise EOF}


