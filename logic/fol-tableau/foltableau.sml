use "structFOL.sml";
open structFOL;

fun checkArity(l: (string*int) list,s: string) : int = 
     case l of
      [] => ~1
     |(a,b)::xs => if a=s then b else checkArity(xs,s);

fun checkOccurence(l,e) = 
     case l of
      [] => false
     |x::xs => if x=e then true else checkOccurence(xs,e);

fun delete (item, list: string list) = List.filter(fn x => x <> item) list

fun printList(l : string list) =
     case l of
    [] => print("\n")
    |x::xs => (print(x);
         print(" ");
         printList(xs));

fun getVar(l: term list, sl: string list): string list = 
     case l of
    [] => sl
    |VAR(x)::xs => if checkOccurence(sl,x) then getVar(xs, sl) else getVar(xs, x::sl)
    |CONST(x)::xs => getVar(xs, sl)
    |FUN(s,tl)::xs => getVar(xs, getVar(tl, sl));

fun checkValidityTermList(tl: term list, arities: (string*int) list): bool* (string*int) list =
     case tl of
     [] => (true,arities)
    |VAR(s)::xs => checkValidityTermList(xs,arities)
    |CONST(s)::xs => checkValidityTermList(xs,arities)
    |FUN(s,tl)::xs => if checkArity(arities,s)= ~1 then 
                    (case checkValidityTermList(tl,(s,length tl)::arities) of
                        (a,b) => checkValidityTermList(xs,b))
                      else if checkArity(arities,s)=length tl then 
                    (case checkValidityTermList(tl,arities) of
                        (a,b) => checkValidityTermList(xs,b))
                      else raise NotWFT;

fun checkValidityPred(pred: Pred, arities: (string*int) list, fvars: string list): bool* (string*int) list* string list = 
     case pred of 
     FF => raise NotWFA
    |ATOM(s,tl) => if checkArity(arities,s)= ~1 then 
                (case checkValidityTermList(tl,(s,length tl)::arities) of
                    (a,b) => (true, b, getVar(tl,[])@fvars))
                   else if checkArity(arities,s)=length tl then 
                (case checkValidityTermList(tl,arities) of
                    (a,b) => (true, b, getVar(tl,[])@fvars))
                   else raise NotWFP
    |NOT(p) => checkValidityPred(p,arities,fvars)
    |AND(p1,p2) => (case checkValidityPred(p1, arities,fvars) of 
                    (a,b,c) => checkValidityPred(p2, b,c))
    |OR(p1,p2) => (case checkValidityPred(p1, arities,fvars) of 
                    (a,b,c) => checkValidityPred(p2, b,c))
    |COND(p1,p2) => (case checkValidityPred(p1, arities,fvars) of 
                    (a,b,c) => checkValidityPred(p2, b,c))
    |BIC(p1,p2) => (case checkValidityPred(p1, arities,fvars) of 
                    (a,b,c) => checkValidityPred(p2, b,c))
    |ITE(p1,p2,p3) => (case checkValidityPred(p1, arities,fvars) of 
                    (a,b,e) => (case checkValidityPred(p2, b,e) of 
                                (c,d,f) => checkValidityPred(p3, d,f)))
    |ALL(t,p) => (case t of 
                 VAR(s) => (case checkValidityPred(p,arities,[]) of
                                (a,b,c) => (a,b,delete(s,c)))
                |CONST(s) => raise NotVAR
                |FUN(s,tl) => raise NotVAR)
    |EX(t,p) => (case t of 
                 VAR(s) => (case checkValidityPred(p,arities,[]) of
                                (a,b,c) => (a,b,delete(s,c)@fvars))
                |CONST(s) => raise NotVAR
                |FUN(s,tl) => raise NotVAR);

fun checkValidityPredList(pl: Pred list, arities: (string*int) list, fvars: string list): bool* (string*int) list* string list =
     case pl of
     [] => (true,arities,fvars)
    |p::xs => case checkValidityPred(p,arities,fvars) of
                (a,b,c)=>checkValidityPredList(xs,b,c);

fun arg2predlist(arg: Argument): Pred list = 
     case arg of
    HENCE(plist, p) => NOT(p)::plist;

fun checkArgument(arg: Argument): bool =
     case checkValidityPredList(arg2predlist(arg),[],[]) of
      (a,b,c) => (printList(c);
          if length c = 0 then true else raise NotClosed);

fun makeSubsArg(x: (term * term) list, l: term list, res: ((term * term) list * term) list) =
     case l of
     [] => res
    |xs::ys => makeSubsArg(x,ys,(x,xs)::res)



fun substTerm(x: (term * term) list, t: term): term =
     case x of 
     [] => t
    |(VAR(s),st)::xs => (case t of
                         VAR(v) => if v=s then substTerm(xs,st) else substTerm(xs,VAR(v))
                        |FUN(p,tl) => (let val arglist = makeSubsArg([(VAR(s),st)],tl,[]) in
                                        substTerm(xs,FUN(p,map substTerm arglist)) end)
                        |_ => t)
    |_ => raise NotUnifiable;

fun delSubs(x: (term * term) list, v: string): (term * term) list = 
     case x of
     [] => []
    |(t1,t2)::ys => (case t1 of
                     VAR(var) => if var=v then delSubs(ys,v) else (t1,t2)::delSubs(ys,v)
                    |_ => raise NotUnifiable);


fun subsPred(x: (term * term) list, pred: Pred): Pred =
     case pred of 
     FF => FF
    |ATOM(s,tl) => (let val arglist = makeSubsArg(x,tl,[]) in
                        ATOM(s,map substTerm arglist) end)
    |NOT(p) => NOT(subsPred(x, p))
    |AND(p1,p2) => AND(subsPred(x, p1),subsPred(x, p2))
    |OR(p1,p2) => OR(subsPred(x, p1),subsPred(x, p2))
    |COND(p1,p2) => COND(subsPred(x, p1),subsPred(x, p2))
    |BIC(p1,p2) => BIC(subsPred(x, p1),subsPred(x, p2))
    |ITE(p1,p2,p3) => ITE(subsPred(x, p1),subsPred(x, p2),subsPred(x, p3))
    |ALL(t,p) => (case t of 
                 VAR(s) => ALL(t,subsPred(delSubs(x,s), p))
                |CONST(s) => raise NotVAR
                |FUN(s,tl) => raise NotVAR)
    |EX(t,p) => (case t of 
                 VAR(s) => EX(t,subsPred(delSubs(x,s), p))
                |CONST(s) => raise NotVAR
                |FUN(s,tl) => raise NotVAR);
