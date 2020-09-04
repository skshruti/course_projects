exception Unexpected_Error
exception NOT_UNIFIABLE
exception Invalid_signature

type variable= string
type symbol=string*int
type signature= symbol list
type term= V of variable|Node of symbol * (term list)
type substitution= (term* variable) list

let print_bool (b: bool)=match b with
| true -> print_string("true")
| false -> print_string("false");;

let print_list (l: string list)=
	print_string("[");
	for i=0 to (List.length l-1) do
	 print_string(List.nth l i);
	 print_string(";");
	done;
	print_string("]");;

let print_symbol (sym: string*int)=
	print_string("(");
	print_string(fst sym);
	print_string(",");
	print_int(snd sym);
	print_string(")");;

let rec print_term(t: term)= match t with
	 V(a)->print_string(a);
	 		print_string(";");
	|Node(sym, lt)->print_string("Node(");
					print_symbol(sym);
					print_string(",[");
					List.iter print_term lt; 
					print_string("];");;

let print_tuple (tup: term*variable)=
	print_string("(");
	print_term(fst tup);
	print_string("/");
	print_string(snd tup);
	print_string("),");;

let rec print_substitution(s: substitution)=
	print_string"{";
	List.iter print_tuple s;
	print_string"}";;



(*checks if the symbol name exists in the signature*)
let rec is_repeated (s: string)(l: signature)=match s,l with
	 s,[]->false
	|s,x::xs->if(s=fst x) then true else is_repeated(s)(xs);;

(*for each symbol, checks the arity and checks if the symbol name exists in the remaining list of symbols i.e., if the symbol name is repeated*)
let rec check_sig (s: signature)=
	let check_symbol (smb: symbol)= match smb with
	(a,b)->if(b<0) then false else true in
	match s with
	 []->true
	|x::xs->if(is_repeated(fst x)(xs)=false) then
				if(check_symbol(x)=true) then check_sig(xs)
				else false
			else false;;


(*if the symbol name exists in signature and the arity matches in the signature, then it is a valid symbol*)
let rec valid_symbol(sym: symbol)(s:signature)=
	let rec symbol_name (sym:symbol) (s: signature)=match sym, s with
	 _,[]->false
	|sym,x::xs->if(fst sym=fst x) then true
				else symbol_name(sym)(xs)
	in
	let rec symbol_arity (sym:symbol)(s: signature)=match sym, s with
	 _,[]->true
	|sym,x::xs->if(fst sym=fst x) then 
					begin
						if((snd sym)=(snd x)) then true
						else false
					end
				else symbol_arity(sym)(xs)
	in
	if(symbol_name(sym)(s)=true && symbol_arity(sym)(s)=true) then true
	else false;; 

(*returns false if at least one value is false in the list*)
let rec all_true(l: bool list)=match l with
	 []->true
	|true::xs->all_true(xs)
	|false::xs->false;;

(*returns true if at least one value is true in the list*)
let rec true_exist(l: bool list)=match l with
	 []->false
	|false::xs->true_exist(xs)
	|true::xs->true;;

(*applies the function on the term list, makes a list of validity of each term and returns false if even one term is not valid*)
let rec valid_term (t: term) (s: signature)=
	let rec valid(t: term)=
	match t with
	 V(var)->true
	|Node(sym, lt)->if(valid_symbol(sym)(s)=true) then
	 					if(List.length lt=snd sym) then 
	 						if(snd sym=0) then true
	 						else all_true(List.map valid lt)
	 					else false
	 				else false
	in
	valid(t);;

(*if signature is invalid, raises exception else checks for the symbol and iterates the same function over term list*)
let rec wfterm (t: term) (s: signature)=
	if(check_sig(s)=false) then (raise Invalid_signature) else 
	let rec iterList(lt: term list)(s: signature)=match lt with
	 []->true
	|x::xs->if(valid_term(x)(s)=true) then iterList(xs)(s)
			else false
	in
	 match t,s with
	 V(var),s->true
	|Node(sym,lt),s->if(valid_term(t)(s)=true) then iterList(lt)(s)
	 				else false;;

(*size of a node is 1+(its arity), so size of the tree would be some of arities of all nodes+1(the root node).
done by iterating the function over term list*)
let rec size(t: term)=
	let rec help (t:term)=
		let rec iterList(lt: term list)=match lt with
		 []->0
		|x::xs->help(x)+iterList(xs)
		in
		match t with
		 V(var)->0
		|Node(sym, lt)->snd sym+iterList(lt)
	in
	1+help(t);;

(*returns the maximum value in a list*)
let rec maxVal(l: int list)=
	let res=ref(List.nth l 0) in
		for i=0 to (List.length l-1) do
			if((List.nth l i)> !res) then res:=List.nth l i
		done;
	!res;;

(*returns 1+max([list of heights of each term]), the max is calculated using maXval function
done by iterating the function over term list*)
let rec ht(t: term)=
		let rec iterList(l: term list)=match l with
		 []->[0]
		|x::xs->ht(x)::iterList(xs)
		in
		match t with
		 V(var)->0
		|Node(sym, lt)->if(snd sym>0) then 1+maxVal(iterList(lt))
						else 0;;

(*traverses the whole term and when encountered a variable, appends it to the result*)
let rec varsHelp(t: term)=
		let rec iterList(l: term list)=match l with
		 []->[]
		|x::xs->varsHelp(x)@iterList(xs);
		in
		match t with
		 V(var)->[var]
		|Node(sym, lt)->iterList(lt);;

(*returns a new list containing the variables only once*)
let rec remove_repeated (l: variable list)=match l with
	 []->[]
	|x::xs->if(List.mem x xs) then remove_repeated(xs) 
			else x::remove_repeated(xs);;

(*returns the list after removing repeatition of values in the list obtained by varsHelp*)
let vars (t: term)=remove_repeated(varsHelp(t));;

(*returns the list of variables in a substitution*)
let rec list_of_vars(s: substitution)=match s with
	 []->[]
	|x::xs->snd x::list_of_vars(xs);;

(*returns the term by which the variable is to be substituted in a substitution.*)
let rec get_termV (s: substitution)(v: variable)=match s with
	 []->raise(Unexpected_Error)
	|x::xs->if(snd x=v) then fst x 
	 		else get_termV(xs)(v);;

(*if the variable of term exists in the substitution,(list obtained using list_of_vars),
the variable is substituted by corresponding term(obtained using get_termV)
else, the same variable is added to the result.
done by iterating the function over term list*)
let rec subst(t: term)(s: substitution)=
	let rec iterList(lt: term list)=match lt with
	  [] -> []
	| x::xs -> subst(x)(s)::iterList(xs)
	in
	match t,list_of_vars(s) with
	 V(a),l->if(List.mem a l) then get_termV(s)(a)
				else V(a) 
	|Node(sym, lt),v->Node(sym, iterList(lt));;	

(*gives the composition of s1 and s2 using subst*)
let rec composeHelp (s1: substitution)(s2: substitution)=
	match s1 with
	 []->[]
	|x::xs-> (subst(fst x)(s2),snd x)::composeHelp(xs)(s2);;

(*gives the resulting composition of any number of substitutions*)
let rec compose (l: substitution list)=
	match l with
	 []->[]
	|s::[]->s
	|x::y::xs->compose((composeHelp(x)(y))::xs);;

(*returns true if a term is V of variable else false*)
let is_var (t: term)=match t with
	 V(a)->true
	|Node(sym, lt)->false;;

(*given a substitution, removes reoccuring substitutions;
raises exception in case of conflicting substitutions;
raises exception in case of substitutions of type v->f(v);*)
let rec generalise (s: substitution)=match s with
	 []->[]
	|x::xs->if(List.mem (snd x) (vars(fst x))) then raise NOT_UNIFIABLE
			else
				if(List.mem (snd x) (list_of_vars xs)=false) then x::generalise(xs)
				else 
					if(get_termV(xs)(snd x)=(fst x)) then generalise(xs)
					else 
						if(is_var(fst x) || is_var(get_termV(xs)(snd x))) 
						then x::generalise(xs)
						else raise NOT_UNIFIABLE;; 

(*given a generalised substitution, returns the most general substitution*)
let rec finSubs(s: substitution)=match s with
	 []->[]
	|x::xs->if(is_var(fst x)) then 
				if(List.mem (snd x) (list_of_vars(xs))) then 
					match (fst x) with
					V(a)->(get_termV(xs)(snd x),a)::finSubs(xs)
					|Node(sym, lt)->x::finSubs(xs)
				else (subst(fst x)(xs),snd x)::finSubs(xs)
			else (subst(fst x)(xs),snd x)::finSubs(xs);;

(*returns a non generalised list of evey possible substitution needed to unify the terms*)
let rec unify_terms (t1: term)(t2: term)=
	let rec iterList(l1: term list)(l2: term list)=
		match l1, l2 with
		 [],[]->[]
		|[],x::xs->raise NOT_UNIFIABLE
		|x::xs,[]->raise NOT_UNIFIABLE
		|x::xs,y::ys->unify_terms(x)(y)@iterList(xs)(ys)
	in
	match t1, t2 with
	 V(a),V(b)->if(a=b) then []
	 			else [(V(a),b)]
	|Node(sym, lt),V(b)->[(Node(sym, lt),b)]
	|V(a),Node(sym, lt)->[(Node(sym, lt),a)]
	|Node(s1, lt1), Node(s2, lt2)-> if(s1=s2) 
										then iterList(lt1)(lt2)
								    else raise NOT_UNIFIABLE;;

(*returns the most general unifier*)
let mgu (t1: term)(t2: term)=finSubs(generalise(unify_terms(t1)(t2)));;

