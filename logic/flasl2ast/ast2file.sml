open AST;
val temp = HENCE
    ([COND (ATOM "temp1 temp2 temp3",NOT (ATOM "temp2")),
      OR (ATOM "temp3",AND (ATOM "temp4",ATOM "temp5"))],
     COND (ATOM "temp6",ATOM "temp7"));

fun p2str(p: Prop): string=
     case p of
     ATOM(s) => "ATOM \"" ^ s ^ "\""
    |NOT(p) => String.concatWith " " ["NOT","(",p2str(p),")"]
    |AND(p1, p2) => String.concatWith " " ["AND","(",p2str(p1),",",p2str(p2),")"]
    |OR(p1, p2) => String.concatWith " " ["OR","(",p2str(p1),",",p2str(p2),")"]
    |COND(p1, p2) => String.concatWith " " ["COND","(",p2str(p1),",",p2str(p2),")"]
    |BIC(p1, p2) => String.concatWith " " ["BIC","(",p2str(p1),",",p2str(p2),")"]
    |ITE(p1, p2, p3) => String.concatWith " " ["IF","(",p2str(p1),")","THEN","(",p2str(p2),")","ELSE","(",p2str(p3),")"]

fun plist2str(plist: Prop list): string =
     case plist of 
     [] => ""
    |x::[] => p2str(x)
    |x::xs => String.concatWith "," [p2str(x), plist2str(xs)];

fun ast2filefun(arg): string = 
     case arg of
    HENCE(plist, p) => "HENCE([" ^ plist2str(plist) ^ "]," ^ p2str(p) ^ ")";

fun ast2file (arg: Argument) = 
    let val os = TextIO.openOut "arg.sml"
    in
        TextIO.output(os,"val arg = ");
        TextIO.output(os,ast2filefun(arg));
        TextIO.closeOut os
    end;

