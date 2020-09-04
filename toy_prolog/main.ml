open Backend;;

let main()=begin
	try 
		let lexbuf=Lexing.from_channel stdin in
		while (true) do 
			Parser.line Lexer.token lexbuf
		done;
	with Lexer.EOF -> exit 0
end;;
main();
        
