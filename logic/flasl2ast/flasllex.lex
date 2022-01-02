open Tokens
type pos = int
val linenum = ref 1
val charsAbove = ref 1
type lexresult= (svalue,pos) token
fun eof () = Tokens.EOF(0,0)
(*  *)
fun init() = ()
%%

%header (functor FlasllexLexFun(structure Tokens: Flasllex_TOKENS)); 
alpha=[0-9A-Za-z-];
text=[^\"\.\(\)\ \127\000-\031];
ws = [\ \t];

%%
\n       => (linenum := !linenum + 1; charsAbove := yypos; lex());
{ws}+    => (lex());
"("     => (LPAR(!linenum, yypos - !charsAbove));
")"     => (RPAR(!linenum, yypos - !charsAbove));
"\""    => (QUOTE(!linenum, yypos - !charsAbove));
\.     => (FULLSTOP(!linenum, yypos - !charsAbove));
"NOT"    => (NOT(!linenum, yypos - !charsAbove));
"AND"    => (AND(!linenum, yypos - !charsAbove));
"OR"    => (OR(!linenum, yypos - !charsAbove));
"IF"    => (IF(!linenum, yypos - !charsAbove));
"THEN"    => (THEN(!linenum, yypos - !charsAbove));
"IFF"    => (IFF(!linenum, yypos - !charsAbove));
"ELSE"    => (ELSE(!linenum, yypos - !charsAbove));
"THEREFORE"    => (THEREFORE(!linenum, yypos - !charsAbove));
{text}+    => (ID(yytext, !linenum, yypos - !charsAbove));
.        => (raise Fail("ScanError at char "^Int.toString(yypos - !charsAbove)^" in line "^Int.toString(!linenum)); lex());