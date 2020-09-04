all:
	(ocamllex lexer.mll; ocamlyacc parser.mly; ocamlc -c parser.mli; ocamlc -c lexer.ml; ocamlc -c str.cma backend.ml; ocamlc -c str.cma backend.cma parser.ml; ocamlc -c backend.cma main.ml; ocamlc -o assignment4 str.cma backend.cmo lexer.cmo parser.cmo main.cmo)

clean:
	(rm *.cmo; rm *.cmi; rm lexer.ml; rm parser.ml; rm parser.mli; rm main)