open AST;
structure Flasllex = struct 
structure FlasllexLrVals = FlasllexLrValsFun(structure Token = LrParser.Token) 
structure FlasllexLex = FlasllexLexFun(structure Tokens = FlasllexLrVals.Tokens); 
structure FlasllexParser =
    Join(structure LrParser = LrParser
        structure ParserData = FlasllexLrVals.ParserData 
        structure Lex = FlasllexLex)
val invoke = fn lexstream => 
    let val print_error = fn (str,pos,line) =>
        TextIO.output(TextIO.stdOut,
        "***Flasllex Parser Error at line number " ^ Int.toString(line) ^ " character position " ^ (Int.toString pos)
        ^ "***\n" ^ str^ "\n")
    in FlasllexParser.parse(0,lexstream,print_error,()) end
fun newLexer fcn =
    let val lexer = FlasllexParser.makeLexer fcn
        val _ = FlasllexLex.UserDeclarations.init() 
    in lexer
    end
fun stringToLexer str = 
    let val done = ref false
    in newLexer (fn n => if (!done) then "" else (done := true; str))
    end
fun fileToLexer filename = 
    let val inStream = TextIO.openIn(filename)
    in newLexer (fn n => TextIO.inputAll(inStream)) 
    end
fun lexerToParser (lexer) = 
    let val dummyEOF = FlasllexLrVals.Tokens.EOF(0,0)
        val (result,lexer) = invoke lexer
        val (nextToken,lexer) = FlasllexParser.Stream.get lexer 
    in if FlasllexParser.sameToken(nextToken,dummyEOF) then
        result
    else (TextIO.output(TextIO.stdOut, "*** Flasllex PARSER WARNING -- unconsumed input ***\n");
    result) 
    end
val parseString = lexerToParser o stringToLexer 
val parseFile: string -> Argument = lexerToParser o fileToLexer 
 
end 