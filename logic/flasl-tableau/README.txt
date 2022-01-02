parseFile is parsing the flasl input and storing the Argument structure in the variable parsed.
This variable is now given as input to proptableau.sml which checks the validity of the Argument and returns the appropriate output.
The output returned is a tuple of bool and prop list. 
This output is then given as input to writeTofile method, which print to appropriate outfile whether the argument is valid or not.
If not valid, it prints the truth assignment.

To run, type sml make.sml in the terminal.