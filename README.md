WalScript
=========
The WalScript interpreter (currently in python)

Hello! Welcome to the README!

My FIRST README!

I have no clue what I'm doing! 

And so I shall just explain the syntax. 
a command is written as:
``` 
command}arg}arg}arg}
```
Commands:
---------
```
import}filename.walrus}      // Imports filename from your libraries, adding all functions, variables, etc. to your runtime and running it. 
print}message}…}message}     // Print message
var}name}value}              // Declare or set variable name to value
bool}name}value}             // Declares or sets a boolean to value (value can be 1,0,or t. t toggles the boolean.)
input}name}message}          // Get input from prompt message and set variable or bool name to evaluated response
rinput}var}message}          // Get input from prompt message and set var to unevaluated response (based on python's raw_input()
hold}                        // Just waits for the user to hit enter
if}bool}                     // Executes all following statemenst down to endif}, provided bool is true
endif}                       // Closes an if statement
while}bool}                  // Executes all following statements down to endwhile}, as long as bool is true
endwhile}                    // Closes a while loop
func}name}args}              // Creates a function executed with args. Args declared as booleans with [ or normal variabless with {
endfunc}                     // Ends a function
stop}                        // Stops the program
debugstop}message}…}message} // Prints message, reports runtime data, and stops the program. Used mainly for debugging during development.
```
Expressions:
------------
```
var}x}5}
print}{1+2-3*4/5%6^#x#}      // this will calculate (((((1+2)-3)*4)/5)%6)^5 (x=5), or 0
```                                  
                             
Boolean Expressions:         
--------------------         
```                          
var}w}5}                     
var}x}1}                     
bool}y}1}                    
bool}z}1}                    
                             
print}{#w#=#x#}              // prints b0, as 5 does not equal 1 (supports booleans and variables)
print}{#w#!=#x#}             // prints b1, as 5 does not equal 1 (supports booleans and variables)
print}{#w#<#x#}              // prints b0, as 5 is not less than 7 (supports variables)
print}{#w#>#x#}              // prints b1, as 5 is greater than 7 (supports variables)
print}{$y$&$z$}              // prints b1, as both y and z are true (supports booleans)
print}{$y$|$z$}              // prints b1, as either y or z is true (supports booleans)
```

Editor Settings:
----------------
Editor settings are a way to configure how the interpreter will work. The are prefixed by an octothorpe and are formatted as setting:value.
Default is value is shown.
```
#oops:^*/%+-
```
Defines the order of operations. Parenthesis ALWAYS come first. Shown is PEMDAS (with modulus.)
