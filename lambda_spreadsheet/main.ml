open Backend;;
open List;;
open Array;;

let rec mkarr l (k:int) n = if (k=n) then [] else match l with
            [] -> []
            | e::l -> match e with 
                    ""| " " -> None :: mkarr (l) (k+1) (n)
                    | h -> Some(float_of_string h) :: mkarr (l) (k+1) (n);;

let _ =
            try
              let in_stream = open_in Sys.argv.(1); in
                  for i=0 to (int_of_string(Sys.argv.(2))-1) do
                    let line = input_line in_stream in
                    let split = Str.split_delim (Str.regexp ",") in
                    let values = split line in
                    let temp = mkarr (values) (0) (int_of_string(Sys.argv.(3))) ;in
                      sh.(i)<-(Array.of_list temp);
                  done;
                  close_in in_stream;
            with e ->
              Printf.printf "File not found!";
              raise e

              let parse =
                try
                let lexbuf = Lexing.from_channel stdin in
                
                while true do
                  Parser.main Lexer.token lexbuf;
                    flush stdout
                done
              with Lexer.EOF ->
                exit 0;;
        
