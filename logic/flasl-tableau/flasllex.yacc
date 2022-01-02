(* 
Start = THEREFORE Prop | Proplist THEREFORE Prop
Proplist = Prop | Proplist
Prop = Exp FULLSTOP
Exp = NOT Exp 
    | Exp AND Exp
    | Exp OR Exp 
    | IF Exp THEN Exp 
    | Exp IF Exp 
    | Exp IFF Exp 
    | IF Exp THEN Exp ELSE Exp 
    | LPAR Exp RPAR 
    | QUOTE Stringlist QUOTE 
Stringlist = Term
    | Term Stringlist 
Term = ID 
*)
%%
%name Flasllex
%pos int
%term 
    ID of string | NOT | AND | OR | IF | IFF | THEN | ELSE | THEREFORE | EOF | LPAR | RPAR | QUOTE | FULLSTOP
%nonterm 
    Start of AST.Argument
    | Exp of AST.Prop
    | Prop of AST.Prop
    | Proplist of AST.Prop list
    | Stringlist of string list
    | Term of string
%start Start
%keyword 
%eop EOF 
%noshift EOF
%nodefault 
%verbose 

%right IFF IF THEN ELSE
%left AND OR
%nonassoc NOT
(*%left THEREFORE IF THEN ELSE IFF OR AND NOT*)
%%
Start: THEREFORE Prop (AST.HENCE([], Prop))
    | Proplist THEREFORE Prop (AST.HENCE(Proplist, Prop))
    | (raise Fail("oops"))
Proplist: Prop (Prop :: [])
    | Prop Proplist (Prop :: Proplist)
Prop: Exp FULLSTOP (Exp)
Exp : NOT Exp (AST.NOT(Exp1))
    | Exp AND Exp (AST.AND(Exp1, Exp2))
    | Exp OR Exp (AST.OR(Exp1, Exp2))
    | IF Exp THEN Exp (AST.COND(Exp1, Exp2))
    | Exp IF Exp (AST.COND(Exp2, Exp1))
    | Exp IFF Exp (AST.BIC(Exp1, Exp2))
    | IF Exp THEN Exp ELSE Exp (AST.ITE(Exp1, Exp2, Exp3))
    | LPAR Exp RPAR (Exp)
    | QUOTE Stringlist QUOTE (AST.ATOM(String.concatWith " " Stringlist))
Stringlist: Term (Term :: [])
    | Term Stringlist (Term :: Stringlist)
Term: ID (ID)