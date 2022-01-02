val args = CommandLine.arguments();
use "load-flasllex-ast.sml";
val parsed = parseFile (hd args ^ ".flasl");
use "proptableau.sml";
val result = ast2flaslfun parsed;
writeTofile (result,hd args ^ ".out");
val _ = OS.Process.exit(OS.Process.success);