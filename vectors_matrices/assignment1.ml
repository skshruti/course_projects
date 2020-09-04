type vector = float list
type matrix = float list list

exception InvalidInput
exception UnequalVectorSize
exception UnequalMatrixShape
exception IncompatibleMatrixShape
exception SingularMatrix

let rec head(v:vector): float = match v with
			[]-> raise(InvalidInput)
		| x::xs->x;;
let rec tail(v:vector): vector = match v with
			[]-> raise(InvalidInput)
		| x::xs->xs;;
let rec vdim (v:vector): int = match v with
			[] -> 0
		| x::xs-> 1+vdim(xs);; 
let rec mkzerov (n:int): vector = match n with
			0 -> []
		|   x -> 0.0::(mkzerov(n-1));; 
let rec elem(v:vector)(i:int): float = 
		if i>vdim(v) then 
		raise(InvalidInput) else
		match v,i with
			 [],_-> raise(InvalidInput)
		| x::xs,1->x
		| x::xs,_->elem(xs)(i-1);;
let rec iszerov(v:vector): bool = match v with
			[]->true
		| x::xs->if(x<>0.0) then false else (iszerov(xs));;
let rec addv (v1:vector) (v2:vector): vector =
    	if vdim(v1)<>vdim(v2) then 
    	raise(UnequalVectorSize) else
    	match v1,v2 with
			[],[]->[]
		| x::xs,y::ys->(x+.y)::(addv(xs)(ys));;
let rec scalarmultv (c:float) (v:vector): vector = match c,v with
			_, []->[]
		| c,x::xs->(c*.x)::scalarmultv(c)(xs);;
let rec dotprodv (v1:vector) (v2:vector): float =
		if vdim(v1)<>vdim(v2) then 
    	raise(UnequalVectorSize) else
    	match v1,v2 with
			[],[]->0.0
		| x::xs,y::ys->(x*.y)+.(dotprodv(xs)(ys));;



let rec headm(m:matrix): vector = match m with
			[]-> raise(InvalidInput)
		| x::xs->x;;
let rec tailm(m:matrix): matrix = match m with
			[]-> raise(InvalidInput)
		| x::xs->xs;;
let rec geti(m:matrix)(i:int): vector = match m,i with
			 [],_-> raise(InvalidInput)
		| x::xs,1->x
		| x::xs,_->geti(xs)(i-1);;
let rec nrow(m:matrix): int = match m with
			[] -> 0
		| x::xs-> 1+nrow(xs);; 
let rec mdim (m:matrix): int*int = match m with 
        	[]->(0,0)
        | x::xs->(nrow(x::xs),vdim(x));;
let rec mkzerom (m_:int) (n_:int): matrix = match m_,n_ with
			0,n_->[mkzerov(n_)]
		| m_,n_->mkzerov(n_)::mkzerom(m_-1)(n_);;  
let rec iszerom (m:matrix): bool = match m with 
				 []->true
		|	[x::xs]->iszerov(x::xs)
		| x::xs -> if(iszerov(x)<>true) then false else iszerom(xs);; 
let rec mkunitv(i: int)(m: int)= match i, m with
                 _,0->[]
		|        1,_->1.0::mkunitv(0)(m-1)
		|		 0,1->0.0::[]
        |        0,m->0.0::mkunitv(0)(m-1)
		|       i,m ->0.0::mkunitv(i-1)(m-1);;
let rec help1(m:int)(j:int): matrix=
		if j==m then [mkunitv(j)(m)]
        else mkunitv(j)(m)::help1(m)(j+1);;
let rec mkunitm (m_:int): matrix = help1(m_)(1);;
let rec isunitv(v: vector)(i: int)(count: int): bool=
			if (count>vdim(v)) then true
		else if (elem(v)(count)<>0.0 && elem(v)(count)<>1.0)then false
		else if (elem(v)(count)==0.0 && count==i) then false
		else isunitv(v)(i)(count+1);;
let rec help5(m: matrix)(i: int): bool=
			if i>nrow(m) then true
		else if isunitv(geti(m)(i))(i)(1) == false then false 
		else help5(m)(i+1);;
let rec isunitm(m_:matrix): bool = help5(m_)(1);;
let rec addm (m1:matrix) (m2:matrix): matrix = 
			 if mdim(m1)<>mdim(m2) then 
    	raise(UnequalMatrixShape) else
    	match m1,m2 with
			[],[]->[]
		| x::xs,y::ys->(addv(x)(y))::(addm(xs)(ys));; 
let rec scalarmultm (c:float) (m:matrix): matrix = match c, m with
			_,[]->[]
		| _,x::xs -> scalarmultv(c)(x)::scalarmultm(c)(xs);;
let rec getcolumn(m: matrix)(i: int): vector= match m, i with
			_,0->[]
		| [],_ ->[] 
		| x::xs,i -> elem(x)(i)::getcolumn(xs)(i);; 
let rec help2(v: vector)(i: int)(m: matrix): vector= match v,i,m with
			_,_,[]->[]
		| v, i, x::xs->
			if i==vdim(x) then [dotprodv(v)(getcolumn(m)(i))]
		else dotprodv(v)(getcolumn(m)(i))::help2(v)(i+1)(m);;
let rec multvm(v: vector)(m: matrix): vector=
		if vdim(v)<>nrow(m) then
		raise(IncompatibleMatrixShape) else
		match v, m with
			[],_->[]
		| _,[] -> []
		| v, m -> help2(v)(1)(m);;
let rec multm (m1:matrix) (m2:matrix): matrix = match m1, m2 with
			[],_->[]
		|   _,[]->[]
		| x::xs, m2->multvm(x)(m2)::multm(xs)(m2);; 
let rec help3 (m: matrix)(i: int): matrix= match m, i with
			[],_->[]
		| x::xs,i->
			if i==vdim(x) then [getcolumn(m)(i)]
		else getcolumn(m)(i)::help3(m)(i+1);;
let rec transm (m:matrix): matrix = help3(m)(1);;
let rec exclude(v: vector)(i: int)(j: int): vector= 
		if i>vdim(v) then
		raise (IncompatibleMatrixShape) else
			if j>vdim(v) then []
        else if j==i && i==vdim(v) then []
		else if j==i then elem(v)(j+1)::exclude(v)(i)(j+2)
		else elem(v)(j)::exclude(v)(i)(j+1);;
let rec cofact(m: matrix)(r: int)(c :int)(count: int)(var: int): matrix= 
        if var=0 then [] 
		else if count==r then cofact(tailm(m))(r)(c)(count+1)(var-1)
        else exclude(headm(m))(c)(1)::cofact(tailm(m))(r)(c)(count+1)(var-1);;
let signi(i: int): float=
		if i mod 2==0 then -1.0
		else 1.0;;
let rec help4(m: matrix)(i: int)=
            if i>vdim(headm(m)) then 0.0 
            else if vdim(headm(m))==1 && nrow(m)==1 then head(headm(m))
            else
                (elem(headm(m))(i)*.signi(i)*.help4(cofact(m)(1)(i)(1)(vdim(headm(m))))(1))+.help4(m)(i+1);;
let rec detm (m:matrix): float = help4(m)(1);;
let sign(i: int)(j: int): float=
		if (i+j) mod 2==0 then 1.0
		else -1.0;;
let rec minorvec(m: matrix)(i: int)(j: int): vector= 
			if(headm(m))==[] then []
		else if j>vdim(headm(m)) then []
		else (sign(i)(j))*.detm(cofact(m)(i)(j)(1)(vdim(headm(m))))::minorvec(m)(i)(j+1);;
let rec minors(m: matrix)(i:int): matrix=
		if i>vdim(headm(m)) then [] else
		match m,i with
			[],_->[]
		| m,_->minorvec(m)(i)(1)::minors(m)(i+1);;
let rec invm (m:matrix): matrix = 
		if detm(m)==0.0 then
		raise(SingularMatrix) else
	 	scalarmultm(1.0/.detm(m))(transm(minors(m)(1)));;



let rec mkonev (n:int): vector = match n with
			0 -> []
		|   x -> 1.0::(mkzerov(n-1));; 
let mkmatrix(v1: vector)(v2: vector): matrix=
			v1::[v2];;
let rec crossprodv (v1:vector) (v2:vector): vector =
		if vdim(v1)==vdim(v2) then
		minorvec(mkonev(vdim(v1))::mkmatrix(v1)(v2))(1)(1)
		else raise(UnequalVectorSize);;
