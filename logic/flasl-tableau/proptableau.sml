open AST;
fun checkOccurence(l,e) = 
     case l of
      [] => false
     |x::xs => if x=e then true else checkOccurence(xs,e);

fun checkValidity(l): bool = 
     case l of
      [] => true
     |x::xs => if checkOccurence(xs,NOT(x)) then false else checkValidity(xs);

fun plist2str(plist: Prop list, atomsfound: Prop list): bool * Prop list=
     case plist of 
     [] => (checkValidity(atomsfound),atomsfound)
    |x::[] => (case x of
             ATOM(s) => (checkOccurence(atomsfound,NOT(ATOM(s))),atomsfound@[ATOM(s)])
            |NOT(ATOM(s)) => (checkOccurence(atomsfound,ATOM(s)),atomsfound@[NOT(ATOM(s))])
            |NOT(NOT(p)) => (case plist2str([p],atomsfound) of
                            (a,b) => (a,b))
            |AND(p1, p2) => (case plist2str(p1::[p2],atomsfound) of
                            (a,b) => (a,b))
            |NOT(AND(p1,p2)) => (case (plist2str([NOT(p1)],atomsfound), plist2str([NOT(p2)],atomsfound)) of
                            ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |OR(p1, p2) => (case (plist2str([p1],atomsfound), plist2str([p2],atomsfound)) of
                            ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |NOT(OR(p1, p2)) => (case plist2str(NOT(p1)::[NOT(p2)],atomsfound) of
                            (a,b) => (a,b))
            |COND(p1, p2) => (case (plist2str([NOT(p1)],atomsfound), plist2str([p2],atomsfound)) of
                            ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |NOT(COND(p1, p2)) => (case plist2str(p1::[NOT(p2)],atomsfound) of
                            (a,b) => (a,b))
            |BIC(p1, p2) => (case (plist2str(p1::[p2],atomsfound), plist2str(NOT(p1)::[NOT(p2)],atomsfound)) of
                            ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |NOT(BIC(p1, p2)) => (case (plist2str(p1::[NOT(p2)],atomsfound), plist2str(NOT(p1)::[p2],atomsfound)) of
                            ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |ITE(p1, p2, p3) => (case (plist2str(p1::[p2],atomsfound), plist2str(NOT(p1)::[p3],atomsfound)) of
                            ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |NOT(ITE(p1, p2, p3)) => (case (plist2str([NOT(AND(p1,p2))],atomsfound), plist2str([NOT(AND(NOT(p1),p3))],atomsfound)) of
                            ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
    )
    |x::xs => (case x of
             ATOM(s) => (if checkOccurence(atomsfound,NOT(ATOM(s)))=false then plist2str(xs,atomsfound@[ATOM(s)])
                        else (true, atomsfound@[ATOM(s)]))
            |NOT(ATOM(s)) => (if checkOccurence(atomsfound,ATOM(s))=false then plist2str(xs,atomsfound@[NOT(ATOM(s))])
                        else (true, atomsfound@[NOT(ATOM(s))]))
            |NOT(NOT(p)) => (case plist2str(p::xs,atomsfound) of
                        (a,b) => (a,b))
            |AND(p1, p2) => (case plist2str(p1::p2::xs,atomsfound) of
                        (a,b) => (a,b))
            |NOT(AND(p1,p2)) => (case (plist2str(NOT(p1)::xs,atomsfound), plist2str(NOT(p2)::xs,atomsfound)) of
                        ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |OR(p1, p2) => (case (plist2str(p1::xs,atomsfound), plist2str(p2::xs,atomsfound)) of
                        ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |NOT(OR(p1, p2)) => (case plist2str(NOT(p1)::NOT(p2)::xs,atomsfound) of
                        (a,b) => (a,b))
            |COND(p1, p2) => (case (plist2str(NOT(p1)::xs,atomsfound), plist2str(p2::xs,atomsfound)) of
                        ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |NOT(COND(p1, p2)) => (case plist2str(p1::NOT(p2)::xs,atomsfound) of
                        (a,b) => (a,b))
            |BIC(p1, p2) => (case (plist2str(p1::p2::xs,atomsfound), plist2str(NOT(p1)::NOT(p2)::xs,atomsfound)) of
                        ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |NOT(BIC(p1, p2)) => (case (plist2str(p1::NOT(p2)::xs,atomsfound), plist2str(NOT(p1)::p2::xs,atomsfound)) of
                        ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |ITE(p1, p2, p3) => (case (plist2str(p1::p2::xs,atomsfound), plist2str(NOT(p1)::p3::xs,atomsfound)) of
                        ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
            |NOT(ITE(p1, p2, p3)) => (case (plist2str(NOT(AND(p1,p2))::xs,atomsfound), plist2str(NOT(AND(NOT(p1),p3))::xs,atomsfound)) of
                            ((a,b),(c,d))=>(if a=false then (a,b) else (c,d)))
    )

fun ast2flaslfun(arg: Argument): bool*Prop list = 
     case arg of
    HENCE(plist, p) => plist2str(NOT(p)::plist,[]);

fun printList(b,os) =
    case b of
    [] => TextIO.output(os,"")
    |ATOM(s)::xs => (TextIO.output(os,s);
                    TextIO.output(os,"-> True\n");
                    printList(xs,os))
    |NOT(ATOM(s))::xs => (TextIO.output(os,s);
                    TextIO.output(os,"-> False\n");
                    printList(xs,os));


fun writeTofile(result: bool*Prop list, filename: string) = 
    let val os = TextIO.openOut filename
    in
        (case result of
        (a,b)=>if a=true then TextIO.output(os,"Valid\n") 
                else (TextIO.output(os,"Invalid\n");
                        printList(b,os));
                TextIO.closeOut os)
    end;
(*    case result of
    (a,l) => if a=true then TextIO.output(os,"Valid\n")
                else TextIO.output(os,"Invalid\n");
    TextIO.closeOut os;*)

