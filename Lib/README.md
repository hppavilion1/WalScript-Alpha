This file is to provide vital information about the libraries that come with WalScript

There are two types of libraries: *.wal and *.wpy (walpy). *.walrus libraries are written in WalScript, whereas *.wp is written in Python.
Math.wpy
=======
A set of usefule mathematical functions, constants, and things
Constants
---------
```
pi
e
phi
```
(ALL THINGS BELOW THIS POINT NOT YET IMPLEMENTED)
Functions
---------
```
abs(x) //Get the absolute value of x
round(x) //round x
ceil(x) //nearest integer greater than x
floor(x) //nearest integer less than x
sqrt(x) //Square root of x
root(x, y) //xth root of y
sin(x) //Sine of x
cos(x) //Cosine of x
tan(x) //Tangent of x
asin(x) //Sine^-1 of x
acos(x) //Cosine^-1 of x
atan(x) //Tangent^-1 of x
```

String.wal
=============
A set of string manipulation and examination functions
Constants:
----------
```
low //lower case alphabet
caps //upper case alphabet
letters //low+caps
digits //Numbers
Alphanum //Letters+digits
ascii //ASCII
```
String Manipulation:
--------------------
```
upper(s) //Full caps of s
lower(s) //Lower case of s
sub(b, e, s) //get substring b-e of s
```
Socket.wpy
==========
A low-level networking library
```
socket}name} //Create a socket
name.bind}hostname}port} //bind a socket
name.listen}num} //TCP listener
name.connect}num} //Initiate TCP connection
```
