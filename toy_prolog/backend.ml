open Str;;
open List;;

exception Unexpected_Error
exception NOT_UNIFIABLE
exception Invalid_signature
exception GOAL_NOT_FOUND

type variable=string
type symbol=string*int
type signature= symbol list
type term=V of variable|Node of symbol * (term list)
type rule= term list
type substitution=(term* variable) list

type database= term list list

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

let print_boolList (l: bool list)=
	print_string("[");
	for i=0 to (List.length l-1) do
	 print_bool(List.nth l i);
	 print_string(";");
	done;
	print_string("]");;

let print_symbol (sym: string*int)=
	print_string(fst sym);;

let rec print_term(t: term)= match t with
	 V(a)->print_string(a);
	 		print_string(";");
	|Node(sym, lt)->print_symbol(sym);
					if(lt!=[]) then begin
					print_string(":[");
					List.iter print_term lt; 
					print_string("]")
					end;
					print_string(";");;

let print_termlist (lt: term list)=
	print_string"[";
	List.iter print_term lt;
	print_string"];\n";;

let print_tuple (tup: term*variable)=
	print_string("(");
	print_string(snd tup);
	print_string("=");
	print_term(fst tup);
	print_string("),");;

let print_substitution (s: substitution)=
	print_string"{";
	List.iter print_tuple s;
	print_string"}";;

let print_subsList (s: substitution list)=
	print_string"[";
	List.iter print_substitution s;
	print_string"];";;

let print_database (db: database)=
	print_string"{";
	List.iter print_termlist db;
	print_string"}";;

let print_sol (s: string)=
	let some=ref "" in
	print_string(s);
	print_string("Enter ';' to continue");
	some:=read_line();;

let rec print_solutions (s: substitution list)=
	let some=ref "" in
	if(List.length s==0) then
		begin
			print_string("No possible solutions.Enter ';' to continue"); 
			some:=read_line()
		end
	else
	begin
	print_substitution(List.hd s);
	print_string("\nEnter 1 to get more solutions else enter 0: \n");
	let ans=read_int() in
		if ans=1 then 
			if(List.length s=1) then 
				begin
					print_string("Sorry, no more solutions.Enter ';' to continue"); 
					some:=read_line()
				end
			else print_solutions(List.tl s)
		else begin
			print_string("Enter ';' to continue"); some:=read_line() end
	end;;

let seplr (s:string)=split_delim (regexp "[(]") s;;
let seprr (s:string)=let temp=(List.nth (seplr(s)) 1) in split_delim (regexp "[)]") temp;;
let content (s:string)=List.nth (seprr(s)) 0;;

let create_term (s: string)(lt: term list)=Node((s,List.length lt),lt);; 
let create_var (s: string)=V(s);;


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

(*applies the substitution on a list of terms*)
let rec substTl(t: term list)(s: substitution)=match t with
	 []->[]
	|x::xs->subst(x)(s)::substTl(xs)(s);;

(*returns true if a term is V of variable else false*)
let is_var (t: term)=match t with
	 V(a)->true
	|Node(sym, lt)->false;;

(*checks if the term contains a variable*)
let rec var_exist (t: term)=
	let rec iterList(l: term list)=match l with
	 []->false
	|x::xs->if(is_var(x)=false) then iterList(xs) else true
	in
	match t with
	 V(_)->true
	|Node(sym, lt)->iterList(lt);;

(*given a substitution, removes reoccuring substitutions;
raises exception in case of conflicting substitutions;
raises exception in case of substitutions of type v->f(v);*)
let rec generalise (s: substitution)=
	match s with
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
let rec finSubs(s: substitution)=
	match s with
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

(*finds all possible solutions of a term if it does not depend on any other fact*)
let rec answer_query (t: term)(db: database)=
	 match db with
	 []->[]
	|x::xs->try 
				if((List.length x)=1) then mgu(t)(List.hd x)::answer_query(t)(xs)
				else answer_query(t)(xs)
		   with NOT_UNIFIABLE->answer_query(t)(xs);;

(*returns root node of the term*)
let get_root (t: term)=match t with
	 V(a)->a
	|Node(sym, lt)->fst sym;;

(*returns everything except the root node of the term*)
let get_tree (t: term)=match t with
	 V(a)->[]
	|Node(sym, lt)->lt;;

(*finds the dependencies of the term by iterating over the database*)
let rec find_goal(t: term)(db: database)=
	let result=ref [] in
	for i=0 to (List.length db-1) do
	try
		let substWith=mgu(t)(List.hd (List.nth db i)) in
		result:=substTl(List.tl (List.nth db i))(substWith)::(!result)
	with
	| _ -> print_string""
	done;
	!result;;

(*returns false if the term depends on other facts, returns true if is independent*)
let rec is_fact(t: term)(db: database)=
	let temp=ref "true" in
	for i=0 to (List.length db-1) do
		if((List.length (List.nth db i))!=0) then
		begin
		if(get_root(t)=get_root(List.hd (List.nth db i)) && ((List.length (List.nth db i))>1)) then temp:="false"
		end
	done;
	if(!temp="false") then false
	else true;;

(*returns true if all the values are true in a list*)
let rec all_true(l: bool list)=match l with
	 []->true
	|true::xs->all_true(xs)
	|false::xs->false;;

(*checks the existence of a term if it is independent*)
let rec term_exist (t: term)(db: database)=
	let test=ref "no\n" in
		if((get_tree(t)!=[]) && (is_var(List.hd (get_tree(t))))=true) then test:="yes\n"
		else
		for i=0 to (List.length db-1) do
		if(test=ref "no\n") then begin
			if((List.length (List.nth db i))==0) then 
				test:="no\n"
			else 
			if((List.length (List.nth db i))==1) then 
				begin
				if(t=List.hd (List.nth db i)) then 
					test:="yes\n";
				end
			else
				if(t=List.hd (List.nth db i)) then
					for j=1 to (List.length (List.nth db i)-1) do
						if(term_exist(List.nth (List.nth db i) j)(db)="no\n") then test:="no\n"
						else test:="yes\n"
					done
		end
		done;
	!test;;


let addPossSol (s: substitution list)(lt: term list)(v: variable)=
	let res=ref [[]] in
	for i=0 to (List.length s-1) do
		for j=0 to (List.length lt-1) do
			res:=((List.nth lt j,v)::(List.nth s i))::(!res)
		done
	done;
	!res;;


(*returns the list of all the possible solutions that have to be checked for other dependencies*)
let rec answer_queries(t: term list)(db: database)=
	let res=ref (answer_query(List.hd t)(db)) in
	for i=1 to (List.length t-1) do
		let variables=ref (vars(List.nth t i)) in
		for j=0 to (List.length !variables-1) do
		let tempVar=ref (List.nth !variables j) in
			if((List.length !res==0) || (List.mem (!tempVar) (list_of_vars (List.hd  !res)))==false) then
				let getTerms(s:substitution)=get_termV s !tempVar in
				res:=addPossSol(!res)(List.map getTerms (answer_query(List.nth t i)(db)))(!tempVar)
		done
	done;
	!res;;

(*checks the existence of a term which is dependent on other facts*)
let rec solve_for(t: term)(db: database)(s: substitution)=
	let result=ref false in
	let goalList=ref (find_goal(t)(db)) in
	let i=ref 0 in
	let temp(t: term)=solve_for(t)(db)(s) in
	if(is_fact(t)(db)=true) then 
		if(term_exist(t)(db)="yes\n") then result:=true;
	while((result=ref false) && (!i<(List.length !goalList))) do
		let refList=ref (substTl(List.nth !goalList !i)(s)) in
		if(all_true (List.map temp !refList)=true) then result:=true;
		i:=!i+1
	done;
	!result;;

let rec multQueries(t: term list)(db: database)(lt: substitution list)=
	match lt with
	 []->[]
	|x::xs->let check_term(t: term)=solve_for(subst(t)(x))(db)(x) in
			if(List.length x==0) then multQueries(t)(db)(xs)
			else
				if(all_true (List.map check_term t)=true) then x::multQueries(t)(db)(xs)
				else multQueries(t)(db)(xs)

let addSubs (lt: substitution list)(s: substitution list)=
	let result=ref (lt) in
	for i=0 to (List.length s-1) do
		if((List.mem (List.nth s i) lt)=false) then result:=((List.nth s i)::!result);
	done;
	!result;;
(*returns all the solutions that satisfy all the subgoals for the relevant goal of a term using backtracking*)
let backtrack (t: term)(db: database)=
	let rec helper(t: term)(db: database)(lt: substitution list)=
	match lt with
	 []->[]
	|x::xs->if(solve_for(subst(t)(x))(db)(x)=true) then x::helper(t)(db)(xs)
			else helper(t)(db)(xs) in
	let goalList=ref (find_goal(t)(db)) in
	let result=ref [] in
	let i=ref 0 in
	while((!i<(List.length !goalList))) do
		result:=addSubs(!result)(helper(t)(db)(answer_queries(List.nth !goalList !i)(db)));
		i:=!i+1
	done;
	!result;;

(*the actual function which calls the corresponding function to check the existence of a term based on whether
it is dependent or independent*)
let check_fact (t: term)(db: database)=
	if(is_fact(t)(db)=true) then 
		begin
		if(term_exist(t)(db)="yes\n") then "true.\n"
		else "false.\n"
	end
	else 
		begin
		if(List.mem true (List.map var_exist (List.hd (find_goal(t)(db))))) then 
			begin
			if(List.length (backtrack(t)(db))==0) then "false.\n"
			else "true.\n"
			end
		else
			if(solve_for(t)(db)([])=true) then "true.\n"
			else "false.\n" 
		end;;

(*the actual function which calls the corresponding function to provide solutions for a term based on whether
it is dependent or independent*)
let give_solutions (t: term list)(db: database)=
	if(List.length t==1) then
		let temp=ref (List.hd t) in
		if(is_fact(!temp)(db)=true) then 
			answer_query(!temp)(db)
		else 
			backtrack(!temp)(db)
	else
		multQueries(t)(db)(answer_queries(t)(db));;

	


