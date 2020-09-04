type token =
  | EOL
  | EOF
  | NOVAR of (string)
  | VAR of (string)
  | QUERY
  | ONLYIF
  | LBRACK
  | COMMA
  | RBRACK
  | TERMINATOR
  | UNDEFINED
  | HALT

open Parsing;;
let _ = parse_error;;
# 2 "parser.mly"
open Backend
let errexp()=Printf.printf("invalid input\n");;
let dbase=ref [[]];;

# 23 "parser.ml"
let yytransl_const = [|
  257 (* EOL *);
    0 (* EOF *);
  260 (* QUERY *);
  261 (* ONLYIF *);
  262 (* LBRACK *);
  263 (* COMMA *);
  264 (* RBRACK *);
  265 (* TERMINATOR *);
  266 (* UNDEFINED *);
  267 (* HALT *);
    0|]

let yytransl_block = [|
  258 (* NOVAR *);
  259 (* VAR *);
    0|]

let yylhs = "\255\255\
\001\000\001\000\002\000\002\000\002\000\003\000\003\000\004\000\
\004\000\005\000\005\000\008\000\008\000\007\000\007\000\009\000\
\009\000\010\000\010\000\010\000\010\000\010\000\010\000\006\000\
\006\000\006\000\000\000"

let yylen = "\002\000\
\002\000\001\000\002\000\002\000\002\000\001\000\001\000\002\000\
\002\000\001\000\004\000\001\000\003\000\001\000\003\000\001\000\
\004\000\001\000\003\000\003\000\003\000\003\000\003\000\003\000\
\003\000\003\000\002\000"

let yydefred = "\000\000\
\000\000\000\000\002\000\000\000\016\000\000\000\000\000\027\000\
\000\000\000\000\000\000\000\000\007\000\000\000\000\000\008\000\
\009\000\000\000\005\000\001\000\003\000\004\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\024\000\025\000\
\000\000\026\000\000\000\000\000\011\000\000\000\017\000\000\000\
\015\000\000\000\020\000\019\000\013\000\021\000\023\000\022\000\
\000\000"

let yydgoto = "\002\000\
\008\000\009\000\010\000\011\000\026\000\013\000\017\000\027\000\
\028\000\029\000"

let yysindex = "\010\000\
\006\255\000\000\000\000\251\254\000\000\011\255\012\255\000\000\
\037\255\033\255\034\255\039\255\000\000\040\255\017\255\000\000\
\000\000\042\255\000\000\000\000\000\000\000\000\017\255\017\255\
\043\255\044\255\038\255\045\255\046\255\030\255\000\000\000\000\
\048\255\000\000\017\255\017\255\000\000\017\255\000\000\041\255\
\000\000\017\255\000\000\000\000\000\000\000\000\000\000\000\000\
\017\255"

let yyrindex = "\000\000\
\000\000\000\000\000\000\021\255\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\047\255\000\000\000\000\000\000\000\000\
\000\000\049\255\000\000\000\000\000\000\000\000\000\000\000\000\
\026\255\028\255\000\000\031\255\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\000\
\000\000"

let yygindex = "\000\000\
\000\000\000\000\000\000\000\000\255\255\000\000\023\000\245\255\
\001\000\236\255"

let yytablesize = 58
let yytable = "\012\000\
\015\000\014\000\032\000\034\000\016\000\003\000\018\000\004\000\
\005\000\006\000\001\000\031\000\004\000\005\000\044\000\046\000\
\007\000\048\000\004\000\025\000\019\000\046\000\033\000\043\000\
\045\000\010\000\047\000\010\000\010\000\010\000\018\000\040\000\
\005\000\016\000\016\000\012\000\012\000\020\000\018\000\018\000\
\033\000\021\000\022\000\023\000\024\000\037\000\049\000\033\000\
\030\000\035\000\036\000\038\000\041\000\039\000\042\000\006\000\
\000\000\014\000"

let yycheck = "\001\000\
\006\001\001\000\023\000\024\000\006\000\000\001\006\000\002\001\
\003\001\004\001\001\000\023\000\002\001\003\001\035\000\036\000\
\011\001\038\000\002\001\003\001\009\001\042\000\024\000\035\000\
\036\000\005\001\038\000\007\001\008\001\009\001\030\000\002\001\
\003\001\008\001\009\001\008\001\009\001\001\001\008\001\009\001\
\042\000\009\001\009\001\005\001\005\001\008\001\006\001\049\000\
\007\001\007\001\007\001\007\001\030\000\008\001\007\001\009\001\
\255\255\009\001"

let yynames_const = "\
  EOL\000\
  EOF\000\
  QUERY\000\
  ONLYIF\000\
  LBRACK\000\
  COMMA\000\
  RBRACK\000\
  TERMINATOR\000\
  UNDEFINED\000\
  HALT\000\
  "

let yynames_block = "\
  NOVAR\000\
  VAR\000\
  "

let yyact = [|
  (fun _ -> failwith "parser")
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'input) in
    Obj.repr(
# 21 "parser.mly"
            (_1)
# 135 "parser.ml"
               : Backend.term list))
; (fun __caml_parser_env ->
    Obj.repr(
# 22 "parser.mly"
        (errexp();[])
# 141 "parser.ml"
               : Backend.term list))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'store) in
    Obj.repr(
# 25 "parser.mly"
                   (dbase:=_1::!dbase;_1)
# 148 "parser.ml"
               : 'input))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 1 : 'answer) in
    Obj.repr(
# 26 "parser.mly"
                    (_1)
# 155 "parser.ml"
               : 'input))
; (fun __caml_parser_env ->
    Obj.repr(
# 27 "parser.mly"
                  (exit 0)
# 161 "parser.ml"
               : 'input))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : 'fact) in
    Obj.repr(
# 30 "parser.mly"
       (_1::[])
# 168 "parser.ml"
               : 'store))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : 'rule) in
    Obj.repr(
# 31 "parser.mly"
       (_1)
# 175 "parser.ml"
               : 'store))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'fact) in
    Obj.repr(
# 34 "parser.mly"
             (print_sol(check_fact(_2)(!dbase)); _2::[])
# 182 "parser.ml"
               : 'answer))
; (fun __caml_parser_env ->
    let _2 = (Parsing.peek_val __caml_parser_env 0 : 'query) in
    Obj.repr(
# 35 "parser.mly"
              (print_solutions(give_solutions(_2)(!dbase));print_newline(); _2)
# 189 "parser.ml"
               : 'answer))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : string) in
    Obj.repr(
# 38 "parser.mly"
        (create_term(_1)([]))
# 196 "parser.ml"
               : 'fact))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 3 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'factlist) in
    Obj.repr(
# 39 "parser.mly"
                               (create_term(_1)(_3))
# 204 "parser.ml"
               : 'fact))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : 'fact) in
    Obj.repr(
# 42 "parser.mly"
       (_1::[])
# 211 "parser.ml"
               : 'factlist))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'fact) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'factlist) in
    Obj.repr(
# 43 "parser.mly"
                      (_1::_3)
# 219 "parser.ml"
               : 'factlist))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : 'question) in
    Obj.repr(
# 46 "parser.mly"
           (_1::[])
# 226 "parser.ml"
               : 'query))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'question) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'query) in
    Obj.repr(
# 47 "parser.mly"
                       (_1::_3)
# 234 "parser.ml"
               : 'query))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : string) in
    Obj.repr(
# 50 "parser.mly"
      (create_var(_1))
# 241 "parser.ml"
               : 'question))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 3 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 1 : 'questionlist) in
    Obj.repr(
# 51 "parser.mly"
                                   (create_term(_1)(_3))
# 249 "parser.ml"
               : 'question))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 0 : 'question) in
    Obj.repr(
# 54 "parser.mly"
           (_1::[])
# 256 "parser.ml"
               : 'questionlist))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'questionlist) in
    Obj.repr(
# 55 "parser.mly"
                         ((create_var(_1))::_3)
# 264 "parser.ml"
               : 'questionlist))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : string) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'factlist) in
    Obj.repr(
# 56 "parser.mly"
                     (create_var(_1)::_3)
# 272 "parser.ml"
               : 'questionlist))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'fact) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'questionlist) in
    Obj.repr(
# 57 "parser.mly"
                          (_1::_3)
# 280 "parser.ml"
               : 'questionlist))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'question) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'questionlist) in
    Obj.repr(
# 58 "parser.mly"
                              (_1::_3)
# 288 "parser.ml"
               : 'questionlist))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'question) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'factlist) in
    Obj.repr(
# 59 "parser.mly"
                          (_1::_3)
# 296 "parser.ml"
               : 'questionlist))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'fact) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'factlist) in
    Obj.repr(
# 62 "parser.mly"
                       (_1::_3)
# 304 "parser.ml"
               : 'rule))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'fact) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'questionlist) in
    Obj.repr(
# 63 "parser.mly"
                           (_1::_3)
# 312 "parser.ml"
               : 'rule))
; (fun __caml_parser_env ->
    let _1 = (Parsing.peek_val __caml_parser_env 2 : 'question) in
    let _3 = (Parsing.peek_val __caml_parser_env 0 : 'questionlist) in
    Obj.repr(
# 64 "parser.mly"
                               (_1::_3)
# 320 "parser.ml"
               : 'rule))
(* Entry line *)
; (fun __caml_parser_env -> raise (Parsing.YYexit (Parsing.peek_val __caml_parser_env 0)))
|]
let yytables =
  { Parsing.actions=yyact;
    Parsing.transl_const=yytransl_const;
    Parsing.transl_block=yytransl_block;
    Parsing.lhs=yylhs;
    Parsing.len=yylen;
    Parsing.defred=yydefred;
    Parsing.dgoto=yydgoto;
    Parsing.sindex=yysindex;
    Parsing.rindex=yyrindex;
    Parsing.gindex=yygindex;
    Parsing.tablesize=yytablesize;
    Parsing.table=yytable;
    Parsing.check=yycheck;
    Parsing.error_function=parse_error;
    Parsing.names_const=yynames_const;
    Parsing.names_block=yynames_block }
let line (lexfun : Lexing.lexbuf -> token) (lexbuf : Lexing.lexbuf) =
   (Parsing.yyparse yytables 1 lexfun lexbuf : Backend.term list)
