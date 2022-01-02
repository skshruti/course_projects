In this assignment I have done following things: 
->Raising appropriate exceptions for the argument. Done by the checkArgument function.
->Substitution of terms and predicates. Done by substTerm and subsPred.

TESTCASES:

#1
val subs = [(VAR("x"), FUN("g",[VAR("x")])),(VAR("p"), CONST("c")),(VAR("q"), CONST("d"))]
val t = FUN("g",[VAR("x"),VAR("y"),CONST("k")])
val fh = FUN("h",[VAR("p"),VAR("q")])
val pred = ALL(VAR("p"),ATOM("b",[fh,t]))
subsPred (subs,pred);
Testing cases:
->A bound variable should not be substituted.
->Term list and predicates are getting correctly substituted.
->Only the variables that are in subs are getting substituted and others are not changed.

#2
val subs = [(CONST("x"), FUN("g",[VAR("x")])),(VAR("p"), CONST("c")),(VAR("q"), CONST("d"))]
val t = FUN("g",[VAR("x"),VAR("y"),CONST("k")])
val pred = ATOM("b",[t])
subsPred (subs,pred);
Testing cases:
->If Substitution list says to substitute a constant, then exception should be raised.

