open Str;;
open List;;

exception VAR_NOT_FOUND
exception INVALID_OPERATION

type closure=table*expression
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
			and table=(string*answer) list
				and answer=I of int
						| B of bool
						| Clos of closure

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
		|Clos(cl)->print_closure(cl);;

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

let rec lookup (s: string)(t: table)=

		match t with
		    []->raise VAR_NOT_FOUND
		|x::xs->if(fst x=s) then snd x else lookup s xs;;  

let rec kri (cl: closure) (s: closure list)=
		match cl, s with
		 (t,Int(i)),s->I(i)
		|(t,Var(x)),[]->(match lookup(x)(t) with
						 I(a)->I(a)
						|B(b)->B(b)
						|Clos(t',e')->kri (t',e') [];)
		|(t,Var(x)),s->(match lookup(x)(t) with
						 I(a)->I(a)
						|B(b)->B(b)
						|Clos(t',e')->kri (t',e') s;)
		|(t,Bool(x)),s->B(x)
		|(t,Abs(x,e)),[]->Clos(t,Abs(x,e))
		|(t,Abs(x,e)),(c'::xs)->kri ((x,Clos(c'))::t,e) xs
		|(t,Add(e1,e2)),s->(let v1=kri (t,e1) s
									and v2=kri (t,e2) s in
									match v1, v2 with
									 I(a1),I(a2)->I(a1+a2)
									|_->raise INVALID_OPERATION )
		|(t,Mult(e1,e2)),s->(let v1=kri (t,e1) s
									and v2=kri (t,e2) s in
									match v1, v2 with
									 I(a1),I(a2)->I(a1*a2)
									|_->raise INVALID_OPERATION )
		|(t,Sub(e1,e2)),s->(let v1=kri (t,e1) s
									and v2=kri (t,e2) s in
									match v1, v2 with
									 I(a1),I(a2)->I(a1-a2)
									|_->raise INVALID_OPERATION )
		|(t,Div(e1,e2)),s->(let v1=kri (t,e1) s
									and v2=kri (t,e2) s in
									match v1, v2 with
									 I(a1),I(a2)->I(a1/a2)
									|_->raise INVALID_OPERATION )
		|(t,Compare(e)),s->(let v=kri (t,e) s in
									match v with
									 I(a)->if(a>0) then I(1)
									 		else if(a<0) then I(-1)
									 		else I(0)
									|_->raise INVALID_OPERATION )
		|(t,App(e1,e2)),s->kri (t,e1) ((t,e2)::s)
		|(t,If(e1,e2,e3)),s->match (kri (t,e1) (s)) with
								 B(true)->kri (t,e2) s
								|B(false)->kri (t,e3) s
								|_->raise INVALID_OPERATION;;

