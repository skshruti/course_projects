open Str;;
open List;;

type elemType=None
			| Some of float
type index = string
type range = string
type sheet = elemType array array

exception InvalidInput
exception Empty 
exception Empty_cell

(*To access values of indices and ranges*)
let rec elem(v:string list)(i:int) = 
		match v,i with
			 [],_-> raise(Empty)
		| x::xs,1->x
		| x::xs,_->elem(xs)(i-1);;

let sepleft (i: index)=split_delim (regexp "[[]") i
let rowarr (i: string)=let temp=elem(sepleft(i))(2) in 
		split_delim (regexp "[,]") temp;;
let row (i: index)=let intv=
					let temp=rowarr (i: string) in elem(temp)(1)
						in int_of_string intv;;
let colarr (i: string)=let temp=elem(rowarr(i))(2) in
		split_delim (regexp "[]]") temp;;
let col (i: index)=let intv=
					let temp=colarr (i: string) in elem(temp)(1)
						in int_of_string intv;;


let seplr (r: range)=split_delim (regexp "[(]") r
let firsti (r: string)=let temp=elem(seplr(r))(2) in 
		split_delim (regexp "[:]") temp;;
let indOne (r: range)=let temp=firsti (r: string) in elem(temp)(1);;
let seci (r: string)=let temp=elem(firsti(r))(2) in
		split_delim (regexp "[)]") temp;;
let indTwo (r: range)=let temp=seci (r: string) in elem(temp)(1);;
let r1 (r: range)=let temp=indOne(r) in row(temp);;
let c1 (r: range)=let temp=indOne(r) in col(temp);;
let r2 (r: range)=let temp=indTwo(r) in row(temp);;
let c2 (r: range)=let temp=indTwo(r) in col(temp);;

let is_some (a: elemType)=match a with
	 None->false
	|Some v->true;;

let is_none (a: elemType)=match a with
	 None->true
	|Some v->false;;

let print_elem (a)= match a with
  None -> print_string("None;")
| Some v -> print_float(v); print_string(";");;

let print_array (v: elemType array)=
	print_string("[|");
	Array.iter print_elem v;
	print_string("|];");;

let print_sheet (s: sheet)=
	print_string("[|");
	Array.iter print_array s;
	print_string("|]");;

let value (a: elemType)= match a with
	 None->raise(Empty_cell)
	|Some v->v;;

let full_count (s: sheet)(r: range)(i: index)=
	let res= ref 0 in
		for i=r1(r) to r2(r) do
			for j=c1(r) to c2(r) do
				if(is_some(s.(i).(j))=true) then res:=!res+1
				else res:=!res;
			done;
		done;
	s.(row(i)).(col(i))<-Some (float_of_int !res);
	print_sheet(s);
	print_string("\n");
	s;;

let row_count (s: sheet)(r: range)(i: index)=
	let nrow= ref(row(i)) in
		for k=r1(r) to r2(r) do
			let res= ref 0 in
			for j=c1(r) to c2(r) do
				if(is_some(s.(k).(j))=true) then res:=!res+1
				else res:=!res;
			done;
			s.(!nrow).(col(i))<-Some (float_of_int !res);
			nrow:=!nrow+1;
		done;
	print_sheet(s);
	print_string("\n");
	s;;

let col_count (s: sheet)(r: range)(i: index)=
	let ncol=ref(col(i)) in
		for k=c1(r) to c2(r) do
			let res= ref 0 in
			for j=r1(r) to r2(r) do
				if(is_some(s.(j).(k))=true) then res:=!res+1
				else res:=!res;
			done;
			s.(row(i)).(!ncol)<-Some (float_of_int !res);
			ncol:=!ncol+1;
		done;
	print_sheet(s);
	print_string("\n");
	s;;



let full_sum (s: sheet)(r: range)(i: index)=
	let res= ref 0. in
		for k=r1(r) to r2(r) do
			for j=c1(r) to c2(r) do
				res:=!res+.value(s.(k).(j))
			done;
		done;
	s.(row(i)).(col(i))<-Some !res;
	print_sheet(s);
	print_string("\n");
	s;;

let row_sum (s: sheet)(r: range)(i: index)=
	let nrow=ref(row(i)) in
		for k=r1(r) to r2(r) do
			let res= ref 0. in
			for j=c1(r) to c2(r) do
				res:=!res+.value(s.(k).(j))
			done;
			s.(!nrow).(col(i))<-Some !res;
			nrow:=!nrow+1;
		done;
	print_sheet(s);
	print_string("\n");
	s;;

let col_sum (s: sheet)(r: range)(i: index)=
	let ncol=ref(col(i)) in
		for k=c1(r) to c2(r) do
			let res= ref 0. in
			for j=r1(r) to r2(r) do
				res:=!res+.value(s.(j).(k))
			done;
			s.(row(i)).(!ncol)<-Some !res;
			ncol:=!ncol+1;
		done;
	print_sheet(s);
	print_string("\n");
	s;;




let full_avg (s: sheet)(r: range)(i: index)=
	let count= ref 0. and
     	avg= ref 0. and
	 	res= ref 0. in
		for k=r1(r) to r2(r) do
			for j=c1(r) to c2(r) do
				begin
				res:=!res+.value(s.(k).(j));
				count:=!count+.1.;
				end
			done;
		done;
	avg:= !res/. !count;
	s.(row(i)).(col(i))<-Some !avg;
	print_sheet(s);
	print_string("\n");
	s;;

let row_avg (s: sheet)(r: range)(i: index)=
	let nrow=ref(row(i)) in
		for k=r1(r) to r2(r) do
			let res= ref 0. and 
			 count=ref 0. and
			 avg=ref 0. in
			for j=c1(r) to c2(r) do
					begin 
					res:=!res+.value(s.(k).(j));
					count:=!count+.1.;
					end
			done;
			avg:=!res/. !count;
			s.(!nrow).(col(i))<-Some !avg;
			nrow:=!nrow+1;
		done;
	print_sheet(s);
	print_string("\n");
	s;;

let col_avg (s: sheet)(r: range)(i: index)=
	let ncol=ref(col(i)) in
		for k=c1(r) to c2(r) do
			let res= ref 0. and 
			 count=ref 0. and
			 avg=ref 0. in
			for j=r1(r) to r2(r) do
					begin 
					res:=!res+.value(s.(j).(k));
					count:=!count+.1.;
					end
			done;
			avg:=!res/. !count;
			s.(row(i)).(!ncol)<-Some !avg;
			ncol:=!ncol+1;
		done;
	print_sheet(s);
	print_string("\n");
	s;;




let full_min (s: sheet)(r: range)(i: index)=
	let res=ref(value(s.(r1(r)).(c1(r)))) in
		for k=r1(r) to r2(r) do
			for j=c1(r) to c2(r) do
				if(value(s.(k).(j))< !res) then res:=value(s.(k).(j))
			done;
		done;
	s.(row(i)).(col(i))<-Some !res;
	print_sheet(s);
	print_string("\n");
	s;;

let row_min (s: sheet)(r: range)(i: index)=
	let nrow=ref(row(i)) in
		for k=r1(r) to r2(r) do
			let res= ref(value(s.(k).(c1(r)))) in
			for j=c1(r) to c2(r) do
				if(value(s.(k).(j))< !res) then res:=value(s.(k).(j))
			done;
			s.(!nrow).(col(i))<-Some !res;
			nrow:=!nrow+1;
		done;
	print_sheet(s);
	print_string("\n");
	s;;

let col_min (s: sheet)(r: range)(i: index)=
	let ncol=ref(col(i)) in
		for k=c1(r) to c2(r) do
			let res= ref(value(s.(r1(r)).(k))) in
			for j=r1(r) to r2(r) do
				if(value(s.(j).(k))< !res) then res:=value(s.(j).(k))
			done;
			s.(row(i)).(!ncol)<-Some !res;
			ncol:=!ncol+1;
		done;
	print_sheet(s);
	print_string("\n");
	s;;



let full_max (s: sheet)(r: range)(i: index)=
	let res=ref(value(s.(r1(r)).(c1(r)))) in
		for k=r1(r) to r2(r) do
			for j=c1(r) to c2(r) do
				if(value(s.(k).(j))> !res) then res:=value(s.(k).(j))
			done;
		done;
	s.(row(i)).(col(i))<-Some !res;
	print_sheet(s);
	print_string("\n");
	s;;

let row_max (s: sheet)(r: range)(i: index)=
	let nrow=ref(row(i)) in
		for k=r1(r) to r2(r) do
			let res= ref(value(s.(k).(c1(r)))) in
			for j=c1(r) to c2(r) do
				if(value(s.(k).(j))> !res) then res:=value(s.(k).(j))
			done;
			s.(!nrow).(col(i))<-Some !res;
			nrow:=!nrow+1;
		done;
	print_sheet(s);
	print_string("\n");
	s;;

let col_max (s: sheet)(r: range)(i: index)=
	let ncol=ref(col(i)) in
		for k=c1(r) to c2(r) do
			let res= ref(value(s.(r1(r)).(k))) in
			for j=r1(r) to r2(r) do
				if(value(s.(j).(k))> !res) then res:=value(s.(j).(k))
			done;
			s.(row(i)).(!ncol)<-Some !res;
			ncol:=!ncol+1;
		done;
	print_sheet(s);
	print_string("\n");
	s;;



let add_const (s: sheet)(r: range)(f: float)(i: index)=
	let nrow=ref(row(i)) in
		for k=r1(r) to r2(r) do
			for j=c1(r) to c2(r) do
				s.(!nrow).(col(i))<-Some (value(s.(k).(j))+.f);
				nrow:=!nrow+1;
			done;
		done;
	print_sheet(s);
	print_string("\n");
	s;;

let subt_const (s: sheet)(r: range)(f: float)(i: index)=
	let nrow=ref(row(i)) in
		for k=r1(r) to r2(r) do
			for j=c1(r) to c2(r) do
				s.(!nrow).(col(i))<-Some (value(s.(k).(j))-.f);
				nrow:=!nrow+1;
			done;
		done;
	print_sheet(s);
	print_string("\n");
	s;;


let mult_const (s: sheet)(r: range)(f: float)(i: index)=
	let nrow=ref(row(i)) in
		for k=r1(r) to r2(r) do
			for j=c1(r) to c2(r) do
				s.(!nrow).(col(i))<-Some (value(s.(k).(j))*.f);
				nrow:=!nrow+1;
			done;
		done;
	print_sheet(s);
	print_string("\n");
	s;;

let div_const (s: sheet)(r: range)(f: float)(i: index)=
	let nrow=ref(row(i)) in
		for k=r1(r) to r2(r) do
			for j=c1(r) to c2(r) do
				s.(!nrow).(col(i))<-Some (value(s.(k).(j))/.f);
				nrow:=!nrow+1;
			done;
		done;
	print_sheet(s);
	print_string("\n");
	s;;




let add_range (s: sheet)(rone: range)(rtwo: range)(i: index)=
	let p=ref(r1(rone)) and
		m=ref(row(i)) in
	for k=r1(rtwo) to r2(rtwo) do
		let q=ref(c1(rone)) in
		for j=c1(rtwo) to c2(rtwo) do
			s.(!m).(col(i))<-Some (value(s.(k).(j))+.value(s.(!p).(!q)));
			q:= !q+1;
			m:= !m+1
		done;
		p:= !p+1;
	done;
	print_sheet(s);
	print_string("\n");
	s;;

let subt_range (s: sheet)(rone: range)(rtwo: range)(i: index)=
	let p=ref(r1(rone)) and
		m=ref(row(i)) in
	for k=r1(rtwo) to r2(rtwo) do
		let q=ref(c1(rone)) in
		for j=c1(rtwo) to c2(rtwo) do
			s.(!m).(col(i))<-Some (value(s.(!p).(!q))-.value(s.(k).(j)));
			q:= !q+1;
			m:= !m+1
		done;
		p:= !p+1;
	done;
	print_sheet(s);
	print_string("\n");
	s;;

let mult_range (s: sheet)(rone: range)(rtwo: range)(i: index)=
	let p=ref(r1(rone)) and
		m=ref(row(i)) in
	for k=r1(rtwo) to r2(rtwo) do
		let q=ref(c1(rone)) in
		for j=c1(rtwo) to c2(rtwo) do
			s.(!m).(col(i))<-Some (value(s.(k).(j))*.value(s.(!p).(!q)));
			q:= !q+1;
			m:= !m+1
		done;
		p:= !p+1;
	done;
	print_sheet(s);
	print_string("\n");
	s;;

let div_range (s: sheet)(rone: range)(rtwo: range)(i: index)=
	let p=ref(r1(rone)) and
		m=ref(row(i)) in
	for k=r1(rtwo) to r2(rtwo) do
		let q=ref(c1(rone)) in
		for j=c1(rtwo) to c2(rtwo) do
			s.(!m).(col(i))<-Some (value(s.(!p).(!q))/.value(s.(k).(j)));
			q:= !q+1;
			m:= !m+1
		done;
		p:= !p+1;
	done;
	print_sheet(s);
	print_string("\n");
	s;;



let add_index (s: sheet)(r: range)(inpi: index)(i: index)=
	let cons=ref(value(s.(row(inpi)).(col(inpi)))) and
		nrow=ref(row(i)) in
	for k=r1(r) to r2(r) do
		for j=c1(r) to c2(r) do
			s.(!nrow).(col(i))<-Some (value(s.(k).(j))+. !cons);
			nrow:=!nrow+1;
		done;
	done;
	print_sheet(s);
	print_string("\n");
	s;;

let subt_index (s: sheet)(r: range)(inpi: index)(i: index)=
	let cons=ref(value(s.(row(inpi)).(col(inpi)))) and
		nrow=ref(row(i)) in
	for k=r1(r) to r2(r) do
		for j=c1(r) to c2(r) do
			s.(!nrow).(col(i))<-Some (value(s.(k).(j))-. !cons);
			nrow:=!nrow+1;
		done;
	done;
	print_sheet(s);
	print_string("\n");
	s;;

let mult_index (s: sheet)(r: range)(inpi: index)(i: index)=
	let cons=ref(value(s.(row(inpi)).(col(inpi)))) and
		nrow=ref(row(i)) in
	for k=r1(r) to r2(r) do
		for j=c1(r) to c2(r) do
			s.(!nrow).(col(i))<-Some (value(s.(k).(j))*. !cons);
			nrow:=!nrow+1;
		done;
	done;
	print_sheet(s);
	print_string("\n");
	s;;

let div_index (s: sheet)(r: range)(inpi: index)(i: index)=
	let cons=ref(value(s.(row(inpi)).(col(inpi)))) and
		nrow=ref(row(i)) in
	for k=r1(r) to r2(r) do
		for j=c1(r) to c2(r) do
			s.(!nrow).(col(i))<-Some (value(s.(k).(j))/. !cons);
			nrow:=!nrow+1;
		done;
	done;
	print_sheet(s);
	print_string("\n");
	s;;

let sh=Array.make_matrix (int_of_string(Sys.argv.(2))) (int_of_string(Sys.argv.(3))) (None) ;;