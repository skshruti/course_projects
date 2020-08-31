open Stack;;
open List;;

exception VAR_NOT_FOUND
exception INVALID_OPERATION
exception EMPTY_STACK

type opcode=INT of int|CLOS of string*control| ID of string| BOOL of bool| APP| ADD| SUB| MULT| DIV| IF| COMPARE
	and closure=table*expression
		and expression=Var of string
				 | Int of int
				 | Bool of bool
				 | Add of (expression*expression)
				 | Mult of (expression*expression)
				 | Sub of (expression*expression)
				 | Div of (expression*expression)
				 | Abs of (string*expression)
				 | App of (expression*expression)
				 | If of (expression*expression*expression)
				 | Compare of expression
			and stack=answer list
				and table=(string*answer) list
					and control=opcode list
						and dump=(stack*table*control) list
							and answer=I of int
									| B of bool
									| VClos of (table*string*control)

let rec print_closure (c)=match snd c with
	Var(x)->print_string(x);
	|Int(a)->print_int(a);
	|Bool(true)->print_string("true");
	|Bool(false)->print_string("false");
	|Add(e1,e2)->print_string("add:(");print_closure(fst c,e1);print_string(",");print_closure(fst c,e2);print_string(")")
	|Mult(e1,e2)->print_string("mult:(");print_closure(fst c,e1);print_string(",");print_closure(fst c,e2);print_string(")")
	|Sub(e1,e2)->print_string("div:(");print_closure(fst c,e1);print_string(",");print_closure(fst c,e2);print_string(")")
	|Div(e1,e2)->print_string("sub:(");print_closure(fst c,e1);print_string(",");print_closure(fst c,e2);print_string(")")
	|Abs(x,e2)->print_string("abs:(");print_string(x);print_string(",");print_closure(fst c,e2);print_string(")")
	|App(e1,e2)->print_string("app:(");print_closure(fst c,e1);print_string(",");print_closure(fst c,e2);print_string(")")
	|If(e1,e2,e3)->print_string("IfThenElse")
	|Compare(e)->print_string("compare with 0:(");print_closure(fst c,e);print_string(")");;

let print_answer (a)=match a with
		     I(x)->print_int(x); print_string"\n"
		|B(true)->print_string("true");
		|B(false)->print_string("false");
		|VClos(cl)->raise EMPTY_STACK;;

let print_tuple (t)=
	print_string("(");
	print_string(fst t);
	print_string(",");
	print_answer(snd t);
	print_string(")");;

let print_table (t)=
	print_string"[";
	List.iter print_tuple t;
	print_string"];\n";;

let popFrom (s: stack)=
	 match s with
	 x::xs->x,xs
	|[]->raise EMPTY_STACK;;

let rec lookup (s: string)(t: table)=
		match t with
		    []->raise VAR_NOT_FOUND
		|x::xs->if(fst x=s) then snd x else lookup s xs;;  

let rec compile (e: expression)= 
		match e with
		 Var(x)->[ID(x)]
 	|Int(a)->[INT(a)]
 	|Bool(b)->[BOOL(b)]
	|Add(e1,e2)->compile(e1)@compile(e2)@[ADD]
	|Mult(e1,e2)->compile(e1)@compile(e2)@[MULT]
	|Sub(e1,e2)->compile(e1)@compile(e2)@[SUB]
	|Div(e1,e2)->compile(e1)@compile(e2)@[DIV]
	|Abs(x,e2)->[CLOS(x,compile(e2))]
	|App(e1,e2)->compile(e1)@compile(e2)@[APP]
	|If(e1,e2,e3)->compile(e3)@compile(e2)@compile(e1)@[IF]
	|Compare(e)->compile(e)@[COMPARE];;

let add(s: stack)(c: control)=
	 match s,c with
	 I(a)::I(b)::xs, ADD::c'->I(a+b)::xs,c'
	|_->raise INVALID_OPERATION;;

let sub(s: stack)(c: control)=
	 match s,c with
	 I(a)::I(b)::xs, SUB::c'->I(b-a)::xs,c'
	|_->raise INVALID_OPERATION;;

let mult(s: stack)(c: control)=
	 match s,c with
	 I(a)::I(b)::xs, MULT::c'->I(a*b)::xs,c'
	|_->raise INVALID_OPERATION;;

let div(s: stack)(c: control)=
	 match s,c with
	 I(a)::I(b)::xs, DIV::c'->I(b/a)::xs,c'
	|_->raise INVALID_OPERATION;;

let rec secd (s:stack) (e:table) (c:control) (d:dump)=
	match c, d with
	 [],[]->List.hd s
	|[],(s',e',c')::d'->secd ((List.hd s)::s') e' c' d'
	|INT(i)::xs,d->secd (I(i)::s) e xs d
	|ID(str)::xs,d->secd (lookup(str)(e)::s) e xs d
	|BOOL(b)::xs,d->secd (B(b)::s) e xs d
	|ADD::xs,d->let s',c' = add(s)(ADD::xs) in
					secd s' e c' d
	|MULT::xs,d->let s',c' = mult(s)(MULT::xs) in
					secd s' e c' d
	|SUB::xs,d->let s',c' = sub(s)(SUB::xs) in
					secd s' e c' d
	|DIV::xs,d->let s',c' = div(s)(DIV::xs) in
					secd s' e c' d
	|CLOS(str,c')::xs,d->secd (VClos(e,str,c')::s) e xs d
	|COMPARE::xs,d->let (e1,s2)=popFrom s in
				 (match e1 with
				 	 I(a)->if(a>0) then secd (I(1)::s2) e xs d
							else if(a<0) then secd (I(-1)::s2) e xs d
							else secd (I(0)::s2) e xs d
					|_->raise INVALID_OPERATION)
	|APP::xs,d->(let (e2,s2)=popFrom s in let (e1,s1)=popFrom s2 in
				 match e1, e2 with
				 VClos(t',s',c'),e2->secd [] ((s',e2)::t') c' ((s1,e,xs)::d)
				|_->raise INVALID_OPERATION;)
	|IF::xs,d->let (e1,s2)=popFrom s in
				 (match e1 with
				 				 B(true)->(match s2 with
				 				 				e2::e3::s'->secd (e2::s') e xs d
				 				 				|_->raise INVALID_OPERATION)
				 				|B(false)->(match s2 with
				 								e2::e3::s'->secd (e3::s') e xs d
				 								|_->raise INVALID_OPERATION)
				 				|_->raise INVALID_OPERATION);;
