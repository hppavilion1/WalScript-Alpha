WalScript
=========
The WalScript interpreter (currently in python)

Hello! Welcome to the README!

My FIRST README!

I have no clue what I'm doing! 

And so I shall just explain the syntax. 
a command is written as: 
command}arg}arg}arg}
etc. The commands are:

print}value}value}value…value} - a print statement
var}name}value} - declare or set variable name to value

bool}name}value} - declares or sets a boolean to value (value can be 1,0,or t. t toggles the boolean.)

input}var}message} - get input from prompt “message” and set var to response

binput}bool}message} - get input from prompt “message” and set bool to response

hold} - just waits for the user to hit enter

if}bool} - executes all following statemenst down to endif}, provided bool is true

endif} - closes an if statement

stop} - Stops the program

debugstop}message}message}…message} - Prints the messages and Stops the program after reporting the current runtime data. 
Used mainly for debugging during language development.

Expressions: 
An expression is begun with the left curly bracket ({) 

The math operators are +-*/%^ (addition, subtraction, multipicatation, division, modulus, exponentials.) Up arrow notation is Knott yet supported. Variables can be inserted by surrounding its name in hashtags (e.g. #foo#) 

The Boolean operators are =, !=, <, > , & (and) and | (or)
Booleans are inserted by surrounding it in dollar signs (e.g. $bar$)
