hasType(Gamma, X, T):-lookup(Gamma, X, T).


hasType(Gamma, N, tint) :- number(N).

hasType(Gamma, false, tbool).
hasType(Gamma, true, tbool).

hasType(Gamma, add(E1, E2), T):-
    hasType(Gamma, E1, tint),hasType(Gamma, E2, tint),hasType(Gamma,E1,T).
hasType(Gamma, sub(E1, E2), T):-
    hasType(Gamma, E1, tint),hasType(Gamma, E2, tint),hasType(Gamma,E1,T).
hasType(Gamma, mult(E1, E2), T):-
    hasType(Gamma, E1, tint),hasType(Gamma, E2, tint),hasType(Gamma,E1,T).
hasType(Gamma, div(E1, E2), T):-
    hasType(Gamma, E1, tint),hasType(Gamma, E2, tint),hasType(Gamma,E1,T).

hasType(Gamma, lt(E1, E2), T):-
    hasType(Gamma, E1, tint),hasType(Gamma, E2, tint),hasType(Gamma,true,T).
hasType(Gamma, ltet(E1, E2), T):-
    hasType(Gamma, E1, tint),hasType(Gamma, E2, tint),hasType(Gamma,true,T).
hasType(Gamma, gt(E1, E2), T):-
    hasType(Gamma, E1, tint),hasType(Gamma, E2, tint),hasType(Gamma,true,T).
hasType(Gamma, gtet(E1, E2), T):-
    hasType(Gamma, E1, tint),hasType(Gamma, E2, tint),hasType(Gamma,true,T).
hasType(Gamma, eq(E1, E2), T):-
    (   hasType(Gamma, E1, T1), hasType(Gamma, E2, T1)
    ->  hasType(Gamma, true, T)).

hasType(Gamma, and(B1, B2), T):-
    hasType(Gamma, B1, tbool),hasType(Gamma, B2, tbool),hasType(Gamma,B1,T).
hasType(Gamma, or(B1, B2), T):-
    hasType(Gamma, B1, tbool),hasType(Gamma, B2, tbool),hasType(Gamma,B1,T).
hasType(Gamma, not(B), T):-hasType(Gamma, B, tbool), hasType(Gamma,B,T).

hasType(Gamma, if(E1, E2, E3), T):-
    hasType(Gamma,E1,tbool),hasType(Gamma,E2,T), hasType(Gamma,E3,T).

hasType(Gamma, Elist, T):-
    (   Elist=[]
    ->  append([],[],T)
    ;   Elist=[E]
    ->  hasType(Gamma, E, T)
    ;   Elist=[Ehead|Etail]
    ->  hasType(Gamma, Ehead, Thead), hasType(Gamma, Etail, Ttail),
        append([Thead], Ttail, T)).

hasType(Gamma, def(D, Scope), T):-
    typeElaborates(Gamma, D, Gamma2),
    hasType(Gamma2, Scope, T).

hasType(Gamma, abs(X,E,TX), T):-
    append([[X,TX]], Gamma, Gamma1),
    hasType(Gamma1, E, T2),
    makeArrow(TX, T2, T).

hasType(Gamma, app(E1,E2), T):-
    hasType(Gamma, E1, arrow(T1, T)).

typeDef(Gamma, let(X,E), T):-hasType(Gamma, E, T).

typeElaborates(Gamma, D, Gamma2):-
    (   D=let(X,E)
    ->  hasType(Gamma, E, T),
        append([[X,T]], Gamma, Gamma2)
    ;   D=seq(let(X1,E1), let(X2,E2))
    ->  typeDef(Gamma, let(X1,E1), T1),
        append([[X1,T1]], Gamma, Gamma1),
        typeDef(Gamma1, let(X2,E2), T2),
        append([[X2,T2]], Gamma1, Gamma2))
    ;   D=par(let(X1,E1), let(X2,E2))
    ->  typeDef(Gamma, let(X1,E1), T1),
        append([[X1,T1]], Gamma, Gamma1),
        typeDef(Gamma, let(X2,E2), T2),
        append([[X2,T2]], Gamma1, Gamma2)
    ;   D=local(let(X1,E1), let(X2,E2))
    ->  typeDef(Gamma, let(X1,E1), T1),
        append([[X1,T1]], Gamma, Gamma1),
        typeDef(Gamma1, let(X2,E2), T2),
        append([[X2,T2]], Gamma1, Gamma2).

lookup([[X,T]|Gamma2], X, T):-!.
lookup([[Y,T1]|Gamma2], X, T):-
    (   Y=X, T1\=T
    ->  fail
    ;   lookup(Gamma2, X, T)).

makeArrow(T1, T2, arrow(T1, T2)).

gamma([]).
