functor FlasllexLrValsFun(structure Token : TOKEN)
 : sig structure ParserData : PARSER_DATA
       structure Tokens : Flasllex_TOKENS
   end
 = 
struct
structure ParserData=
struct
structure Header = 
struct
(* 
Start = THEREFORE Prop | Proplist THEREFORE Prop
Proplist = Prop | Proplist
Prop = Exp FULLSTOP
Exp = NOT Exp 
    | Exp AND Exp
    | Exp OR Exp 
    | IF Exp THEN Exp 
    | Exp IF Exp 
    | Exp IFF Exp 
    | IF Exp THEN Exp ELSE Exp 
    | LPAR Exp RPAR 
    | QUOTE Stringlist QUOTE 
Stringlist = Term
    | Term Stringlist 
Term = ID 
*)

end
structure LrTable = Token.LrTable
structure Token = Token
local open LrTable in 
val table=let val actionRows =
"\
\\001\000\001\000\055\000\013\000\055\000\000\000\
\\001\000\001\000\020\000\000\000\
\\001\000\001\000\020\000\013\000\053\000\000\000\
\\001\000\002\000\043\000\005\000\043\000\009\000\043\000\010\000\043\000\
\\011\000\043\000\013\000\043\000\000\000\
\\001\000\002\000\010\000\005\000\009\000\009\000\041\000\011\000\007\000\
\\013\000\006\000\000\000\
\\001\000\002\000\010\000\005\000\009\000\009\000\008\000\010\000\040\000\
\\011\000\007\000\013\000\006\000\000\000\
\\001\000\002\000\010\000\005\000\009\000\011\000\007\000\013\000\006\000\000\000\
\\001\000\003\000\044\000\004\000\044\000\005\000\044\000\006\000\044\000\
\\007\000\044\000\008\000\044\000\012\000\044\000\014\000\044\000\000\000\
\\001\000\003\000\045\000\004\000\045\000\005\000\045\000\006\000\045\000\
\\007\000\045\000\008\000\045\000\012\000\045\000\014\000\045\000\000\000\
\\001\000\003\000\046\000\004\000\046\000\005\000\046\000\006\000\046\000\
\\007\000\046\000\008\000\046\000\012\000\046\000\014\000\046\000\000\000\
\\001\000\003\000\051\000\004\000\051\000\005\000\051\000\006\000\051\000\
\\007\000\051\000\008\000\051\000\012\000\051\000\014\000\051\000\000\000\
\\001\000\003\000\052\000\004\000\052\000\005\000\052\000\006\000\052\000\
\\007\000\052\000\008\000\052\000\012\000\052\000\014\000\052\000\000\000\
\\001\000\003\000\017\000\004\000\016\000\005\000\015\000\006\000\014\000\
\\007\000\047\000\008\000\035\000\012\000\047\000\014\000\047\000\000\000\
\\001\000\003\000\017\000\004\000\016\000\005\000\015\000\006\000\014\000\
\\007\000\048\000\008\000\048\000\012\000\048\000\014\000\048\000\000\000\
\\001\000\003\000\017\000\004\000\016\000\005\000\015\000\006\000\014\000\
\\007\000\049\000\008\000\049\000\012\000\049\000\014\000\049\000\000\000\
\\001\000\003\000\017\000\004\000\016\000\005\000\015\000\006\000\014\000\
\\007\000\050\000\008\000\050\000\012\000\050\000\014\000\050\000\000\000\
\\001\000\003\000\017\000\004\000\016\000\005\000\015\000\006\000\014\000\
\\007\000\033\000\000\000\
\\001\000\003\000\017\000\004\000\016\000\005\000\015\000\006\000\014\000\
\\012\000\032\000\000\000\
\\001\000\003\000\017\000\004\000\016\000\005\000\015\000\006\000\014\000\
\\014\000\013\000\000\000\
\\001\000\009\000\042\000\000\000\
\\001\000\009\000\011\000\000\000\
\\001\000\010\000\000\000\000\000\
\\001\000\010\000\038\000\000\000\
\\001\000\010\000\039\000\000\000\
\\001\000\013\000\054\000\000\000\
\\001\000\013\000\031\000\000\000\
\"
val actionRowNumbers =
"\005\000\020\000\004\000\018\000\
\\001\000\006\000\006\000\006\000\
\\006\000\006\000\019\000\003\000\
\\006\000\006\000\006\000\006\000\
\\002\000\025\000\000\000\017\000\
\\022\000\016\000\007\000\023\000\
\\014\000\013\000\009\000\008\000\
\\024\000\011\000\010\000\006\000\
\\012\000\006\000\015\000\021\000"
val gotoT =
"\
\\001\000\035\000\002\000\003\000\003\000\002\000\004\000\001\000\000\000\
\\000\000\
\\002\000\003\000\003\000\002\000\004\000\010\000\000\000\
\\000\000\
\\005\000\017\000\006\000\016\000\000\000\
\\002\000\019\000\000\000\
\\002\000\003\000\003\000\020\000\000\000\
\\002\000\021\000\000\000\
\\002\000\022\000\000\000\
\\002\000\003\000\003\000\023\000\000\000\
\\000\000\
\\000\000\
\\002\000\024\000\000\000\
\\002\000\025\000\000\000\
\\002\000\026\000\000\000\
\\002\000\027\000\000\000\
\\005\000\028\000\006\000\016\000\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\000\000\
\\002\000\032\000\000\000\
\\000\000\
\\002\000\034\000\000\000\
\\000\000\
\\000\000\
\"
val numstates = 36
val numrules = 18
val s = ref "" and index = ref 0
val string_to_int = fn () => 
let val i = !index
in index := i+2; Char.ord(String.sub(!s,i)) + Char.ord(String.sub(!s,i+1)) * 256
end
val string_to_list = fn s' =>
    let val len = String.size s'
        fun f () =
           if !index < len then string_to_int() :: f()
           else nil
   in index := 0; s := s'; f ()
   end
val string_to_pairlist = fn (conv_key,conv_entry) =>
     let fun f () =
         case string_to_int()
         of 0 => EMPTY
          | n => PAIR(conv_key (n-1),conv_entry (string_to_int()),f())
     in f
     end
val string_to_pairlist_default = fn (conv_key,conv_entry) =>
    let val conv_row = string_to_pairlist(conv_key,conv_entry)
    in fn () =>
       let val default = conv_entry(string_to_int())
           val row = conv_row()
       in (row,default)
       end
   end
val string_to_table = fn (convert_row,s') =>
    let val len = String.size s'
        fun f ()=
           if !index < len then convert_row() :: f()
           else nil
     in (s := s'; index := 0; f ())
     end
local
  val memo = Array.array(numstates+numrules,ERROR)
  val _ =let fun g i=(Array.update(memo,i,REDUCE(i-numstates)); g(i+1))
       fun f i =
            if i=numstates then g i
            else (Array.update(memo,i,SHIFT (STATE i)); f (i+1))
          in f 0 handle General.Subscript => ()
          end
in
val entry_to_action = fn 0 => ACCEPT | 1 => ERROR | j => Array.sub(memo,(j-2))
end
val gotoT=Array.fromList(string_to_table(string_to_pairlist(NT,STATE),gotoT))
val actionRows=string_to_table(string_to_pairlist_default(T,entry_to_action),actionRows)
val actionRowNumbers = string_to_list actionRowNumbers
val actionT = let val actionRowLookUp=
let val a=Array.fromList(actionRows) in fn i=>Array.sub(a,i) end
in Array.fromList(List.map actionRowLookUp actionRowNumbers)
end
in LrTable.mkLrTable {actions=actionT,gotos=gotoT,numRules=numrules,
numStates=numstates,initialState=STATE 0}
end
end
local open Header in
type pos = int
type arg = unit
structure MlyValue = 
struct
datatype svalue = VOID | ntVOID of unit ->  unit
 | ID of unit ->  (string) | Term of unit ->  (string)
 | Stringlist of unit ->  (string list)
 | Proplist of unit ->  (AST.Prop list) | Prop of unit ->  (AST.Prop)
 | Exp of unit ->  (AST.Prop) | Start of unit ->  (AST.Argument)
end
type svalue = MlyValue.svalue
type result = AST.Argument
end
structure EC=
struct
open LrTable
infix 5 $$
fun x $$ y = y::x
val is_keyword =
fn _ => false
val preferred_change : (term list * term list) list = 
nil
val noShift = 
fn (T 9) => true | _ => false
val showTerminal =
fn (T 0) => "ID"
  | (T 1) => "NOT"
  | (T 2) => "AND"
  | (T 3) => "OR"
  | (T 4) => "IF"
  | (T 5) => "IFF"
  | (T 6) => "THEN"
  | (T 7) => "ELSE"
  | (T 8) => "THEREFORE"
  | (T 9) => "EOF"
  | (T 10) => "LPAR"
  | (T 11) => "RPAR"
  | (T 12) => "QUOTE"
  | (T 13) => "FULLSTOP"
  | _ => "bogus-term"
local open Header in
val errtermvalue=
fn _ => MlyValue.VOID
end
val terms : term list = nil
 $$ (T 13) $$ (T 12) $$ (T 11) $$ (T 10) $$ (T 9) $$ (T 8) $$ (T 7)
 $$ (T 6) $$ (T 5) $$ (T 4) $$ (T 3) $$ (T 2) $$ (T 1)end
structure Actions =
struct 
exception mlyAction of int
local open Header in
val actions = 
fn (i392,defaultPos,stack,
    (()):arg) =>
case (i392,stack)
of  ( 0, ( ( _, ( MlyValue.Prop Prop1, _, Prop1right)) :: ( _, ( _, 
THEREFORE1left, _)) :: rest671)) => let val  result = MlyValue.Start
 (fn _ => let val  (Prop as Prop1) = Prop1 ()
 in (AST.HENCE([], Prop))
end)
 in ( LrTable.NT 0, ( result, THEREFORE1left, Prop1right), rest671)

end
|  ( 1, ( ( _, ( MlyValue.Prop Prop1, _, Prop1right)) :: _ :: ( _, ( 
MlyValue.Proplist Proplist1, Proplist1left, _)) :: rest671)) => let
 val  result = MlyValue.Start (fn _ => let val  (Proplist as Proplist1
) = Proplist1 ()
 val  (Prop as Prop1) = Prop1 ()
 in (AST.HENCE(Proplist, Prop))
end)
 in ( LrTable.NT 0, ( result, Proplist1left, Prop1right), rest671)
end
|  ( 2, ( rest671)) => let val  result = MlyValue.Start (fn _ => (
raise Fail("oops")))
 in ( LrTable.NT 0, ( result, defaultPos, defaultPos), rest671)
end
|  ( 3, ( ( _, ( MlyValue.Prop Prop1, Prop1left, Prop1right)) :: 
rest671)) => let val  result = MlyValue.Proplist (fn _ => let val  (
Prop as Prop1) = Prop1 ()
 in (Prop :: [])
end)
 in ( LrTable.NT 3, ( result, Prop1left, Prop1right), rest671)
end
|  ( 4, ( ( _, ( MlyValue.Proplist Proplist1, _, Proplist1right)) :: (
 _, ( MlyValue.Prop Prop1, Prop1left, _)) :: rest671)) => let val  
result = MlyValue.Proplist (fn _ => let val  (Prop as Prop1) = Prop1
 ()
 val  (Proplist as Proplist1) = Proplist1 ()
 in (Prop :: Proplist)
end)
 in ( LrTable.NT 3, ( result, Prop1left, Proplist1right), rest671)
end
|  ( 5, ( ( _, ( _, _, FULLSTOP1right)) :: ( _, ( MlyValue.Exp Exp1, 
Exp1left, _)) :: rest671)) => let val  result = MlyValue.Prop (fn _ =>
 let val  (Exp as Exp1) = Exp1 ()
 in (Exp)
end)
 in ( LrTable.NT 2, ( result, Exp1left, FULLSTOP1right), rest671)
end
|  ( 6, ( ( _, ( MlyValue.Exp Exp1, _, Exp1right)) :: ( _, ( _, 
NOT1left, _)) :: rest671)) => let val  result = MlyValue.Exp (fn _ =>
 let val  Exp1 = Exp1 ()
 in (AST.NOT(Exp1))
end)
 in ( LrTable.NT 1, ( result, NOT1left, Exp1right), rest671)
end
|  ( 7, ( ( _, ( MlyValue.Exp Exp2, _, Exp2right)) :: _ :: ( _, ( 
MlyValue.Exp Exp1, Exp1left, _)) :: rest671)) => let val  result = 
MlyValue.Exp (fn _ => let val  Exp1 = Exp1 ()
 val  Exp2 = Exp2 ()
 in (AST.AND(Exp1, Exp2))
end)
 in ( LrTable.NT 1, ( result, Exp1left, Exp2right), rest671)
end
|  ( 8, ( ( _, ( MlyValue.Exp Exp2, _, Exp2right)) :: _ :: ( _, ( 
MlyValue.Exp Exp1, Exp1left, _)) :: rest671)) => let val  result = 
MlyValue.Exp (fn _ => let val  Exp1 = Exp1 ()
 val  Exp2 = Exp2 ()
 in (AST.OR(Exp1, Exp2))
end)
 in ( LrTable.NT 1, ( result, Exp1left, Exp2right), rest671)
end
|  ( 9, ( ( _, ( MlyValue.Exp Exp2, _, Exp2right)) :: _ :: ( _, ( 
MlyValue.Exp Exp1, _, _)) :: ( _, ( _, IF1left, _)) :: rest671)) =>
 let val  result = MlyValue.Exp (fn _ => let val  Exp1 = Exp1 ()
 val  Exp2 = Exp2 ()
 in (AST.COND(Exp1, Exp2))
end)
 in ( LrTable.NT 1, ( result, IF1left, Exp2right), rest671)
end
|  ( 10, ( ( _, ( MlyValue.Exp Exp2, _, Exp2right)) :: _ :: ( _, ( 
MlyValue.Exp Exp1, Exp1left, _)) :: rest671)) => let val  result = 
MlyValue.Exp (fn _ => let val  Exp1 = Exp1 ()
 val  Exp2 = Exp2 ()
 in (AST.COND(Exp2, Exp1))
end)
 in ( LrTable.NT 1, ( result, Exp1left, Exp2right), rest671)
end
|  ( 11, ( ( _, ( MlyValue.Exp Exp2, _, Exp2right)) :: _ :: ( _, ( 
MlyValue.Exp Exp1, Exp1left, _)) :: rest671)) => let val  result = 
MlyValue.Exp (fn _ => let val  Exp1 = Exp1 ()
 val  Exp2 = Exp2 ()
 in (AST.BIC(Exp1, Exp2))
end)
 in ( LrTable.NT 1, ( result, Exp1left, Exp2right), rest671)
end
|  ( 12, ( ( _, ( MlyValue.Exp Exp3, _, Exp3right)) :: _ :: ( _, ( 
MlyValue.Exp Exp2, _, _)) :: _ :: ( _, ( MlyValue.Exp Exp1, _, _)) :: 
( _, ( _, IF1left, _)) :: rest671)) => let val  result = MlyValue.Exp
 (fn _ => let val  Exp1 = Exp1 ()
 val  Exp2 = Exp2 ()
 val  Exp3 = Exp3 ()
 in (AST.ITE(Exp1, Exp2, Exp3))
end)
 in ( LrTable.NT 1, ( result, IF1left, Exp3right), rest671)
end
|  ( 13, ( ( _, ( _, _, RPAR1right)) :: ( _, ( MlyValue.Exp Exp1, _, _
)) :: ( _, ( _, LPAR1left, _)) :: rest671)) => let val  result = 
MlyValue.Exp (fn _ => let val  (Exp as Exp1) = Exp1 ()
 in (Exp)
end)
 in ( LrTable.NT 1, ( result, LPAR1left, RPAR1right), rest671)
end
|  ( 14, ( ( _, ( _, _, QUOTE2right)) :: ( _, ( MlyValue.Stringlist 
Stringlist1, _, _)) :: ( _, ( _, QUOTE1left, _)) :: rest671)) => let
 val  result = MlyValue.Exp (fn _ => let val  (Stringlist as 
Stringlist1) = Stringlist1 ()
 in (AST.ATOM(String.concatWith " " Stringlist))
end)
 in ( LrTable.NT 1, ( result, QUOTE1left, QUOTE2right), rest671)
end
|  ( 15, ( ( _, ( MlyValue.Term Term1, Term1left, Term1right)) :: 
rest671)) => let val  result = MlyValue.Stringlist (fn _ => let val  (
Term as Term1) = Term1 ()
 in (Term :: [])
end)
 in ( LrTable.NT 4, ( result, Term1left, Term1right), rest671)
end
|  ( 16, ( ( _, ( MlyValue.Stringlist Stringlist1, _, Stringlist1right
)) :: ( _, ( MlyValue.Term Term1, Term1left, _)) :: rest671)) => let
 val  result = MlyValue.Stringlist (fn _ => let val  (Term as Term1) =
 Term1 ()
 val  (Stringlist as Stringlist1) = Stringlist1 ()
 in (Term :: Stringlist)
end)
 in ( LrTable.NT 4, ( result, Term1left, Stringlist1right), rest671)

end
|  ( 17, ( ( _, ( MlyValue.ID ID1, ID1left, ID1right)) :: rest671)) =>
 let val  result = MlyValue.Term (fn _ => let val  (ID as ID1) = ID1
 ()
 in (ID)
end)
 in ( LrTable.NT 5, ( result, ID1left, ID1right), rest671)
end
| _ => raise (mlyAction i392)
end
val void = MlyValue.VOID
val extract = fn a => (fn MlyValue.Start x => x
| _ => let exception ParseInternal
	in raise ParseInternal end) a ()
end
end
structure Tokens : Flasllex_TOKENS =
struct
type svalue = ParserData.svalue
type ('a,'b) token = ('a,'b) Token.token
fun ID (i,p1,p2) = Token.TOKEN (ParserData.LrTable.T 0,(
ParserData.MlyValue.ID (fn () => i),p1,p2))
fun NOT (p1,p2) = Token.TOKEN (ParserData.LrTable.T 1,(
ParserData.MlyValue.VOID,p1,p2))
fun AND (p1,p2) = Token.TOKEN (ParserData.LrTable.T 2,(
ParserData.MlyValue.VOID,p1,p2))
fun OR (p1,p2) = Token.TOKEN (ParserData.LrTable.T 3,(
ParserData.MlyValue.VOID,p1,p2))
fun IF (p1,p2) = Token.TOKEN (ParserData.LrTable.T 4,(
ParserData.MlyValue.VOID,p1,p2))
fun IFF (p1,p2) = Token.TOKEN (ParserData.LrTable.T 5,(
ParserData.MlyValue.VOID,p1,p2))
fun THEN (p1,p2) = Token.TOKEN (ParserData.LrTable.T 6,(
ParserData.MlyValue.VOID,p1,p2))
fun ELSE (p1,p2) = Token.TOKEN (ParserData.LrTable.T 7,(
ParserData.MlyValue.VOID,p1,p2))
fun THEREFORE (p1,p2) = Token.TOKEN (ParserData.LrTable.T 8,(
ParserData.MlyValue.VOID,p1,p2))
fun EOF (p1,p2) = Token.TOKEN (ParserData.LrTable.T 9,(
ParserData.MlyValue.VOID,p1,p2))
fun LPAR (p1,p2) = Token.TOKEN (ParserData.LrTable.T 10,(
ParserData.MlyValue.VOID,p1,p2))
fun RPAR (p1,p2) = Token.TOKEN (ParserData.LrTable.T 11,(
ParserData.MlyValue.VOID,p1,p2))
fun QUOTE (p1,p2) = Token.TOKEN (ParserData.LrTable.T 12,(
ParserData.MlyValue.VOID,p1,p2))
fun FULLSTOP (p1,p2) = Token.TOKEN (ParserData.LrTable.T 13,(
ParserData.MlyValue.VOID,p1,p2))
end
end
